from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Task
from .serializers import (
    TaskSerializer, 
    TaskCreateSerializer, 
    TaskStatusSerializer, 
    TaskResultSerializer
)
from .tasks import execute_task

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # this should be authenticated user only, but leaving it open since it is a demo project
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny] 
    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        elif self.action == 'status':
            return TaskStatusSerializer
        elif self.action == 'result':
            return TaskResultSerializer
        return TaskSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        
        execute_task.delay(
            str(task.id), 
            task.task_type, 
            task.parameters
        )
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskStatusSerializer(task)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def result(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskResultSerializer(task)
        return Response(serializer.data)