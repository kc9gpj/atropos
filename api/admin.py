from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'task_type', 'status', 'progress', 'created_at', 'completed_at')
    list_filter = ('status', 'task_type')
    search_fields = ('name', 'description')
    readonly_fields = ('id', 'celery_task_id', 'created_at', 'updated_at', 'started_at', 
                      'completed_at', 'status', 'progress', 'result', 'error')