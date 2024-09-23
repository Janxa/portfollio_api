from django.db import models


# Create your models here.
class Project(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField()
    git_url = models.CharField(max_length=2048)
    project_url = models.CharField(max_length=2048)

    class Meta:
        ordering = ['created']

class ProjectImage(models.Model):
    file = models.ImageField(upload_to='projectImages/')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.file.name