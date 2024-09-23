from rest_framework import serializers
from projects.models import Project, ProjectImage

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'file']

    def create(self, validated_data):
        """
        Create a new image instance.
        """
        return ProjectImage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing image instance.
        """
        instance.file = validated_data.get('file', instance.file)
        instance.save()
        return instance

class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True)  # Allow both reading and writing nested images

    class Meta:
        model = Project
        fields = ['id', 'title', 'content', 'git_url', 'project_url', 'images', 'created']

    def create(self, validated_data):
        """
        Create a project and its associated images.
        """
        images_data = validated_data.pop('images', [])
        project = Project.objects.create(**validated_data)

        # Handle image creation
        for image_data in images_data:
            ProjectImage.objects.create(project=project, **image_data)

        return project

    def update(self, instance, validated_data):
        """
        Update project and associated images.
        """
        images_data = validated_data.pop('images', None)

        # Update project fields
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.git_url = validated_data.get('git_url', instance.git_url)
        instance.project_url = validated_data.get('project_url', instance.project_url)
        instance.save()

        if images_data is not None:
            # Delete existing images if any
            instance.images.all().delete()

            # Create or update new images
            for image_data in images_data:
                ProjectImage.objects.create(project=instance, **image_data)

        return instance
