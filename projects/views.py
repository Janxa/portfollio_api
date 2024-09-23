from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from projects.models import Project
from projects.serializers import ProjectSerializer


@api_view(['GET', 'POST'])
def project_list(request):
    """
    List all code projects, or create a new project.
    """
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def project_detail(request, pk):
    """
    Retrieve, update or delete a project.
    """
    try:
        projects = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(projects)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProjectSerializer(projects, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        projects.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)