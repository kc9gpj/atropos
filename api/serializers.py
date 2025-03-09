from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description', 'task_type', 'status', 
            'progress', 'created_at', 'updated_at', 'started_at', 
            'completed_at', 'parameters'
        ]
        read_only_fields = ['id', 'status', 'progress', 'created_at', 
                           'updated_at', 'started_at', 'completed_at']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['name', 'description', 'task_type', 'parameters']

class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'status', 'progress', 'started_at', 'completed_at']

class TaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'status', 'result', 'error', 'completed_at']