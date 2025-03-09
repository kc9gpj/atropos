from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from api.models import Task
from api.tasks import execute_task
import json

def index(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'tasks': tasks})

def create_task(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('taskName')
            description = request.POST.get('taskDescription')
            task_type = request.POST.get('taskType')
            
            parameters = {}
            parameters_text = request.POST.get('taskParameters')
            if parameters_text.strip():
                parameters = json.loads(parameters_text)
            
            task = Task.objects.create(
                name=name,
                description=description,
                task_type=task_type,
                parameters=parameters
            )
            
            execute_task.delay(str(task.id), task.task_type, task.parameters)
            
            messages.success(request, 'Task created successfully!')
            return redirect('index')
            
        except json.JSONDecodeError:
            messages.error(request, 'Invalid JSON in parameters field')
        except Exception as e:
            messages.error(request, f'Error creating task: {str(e)}')
    
    return redirect('index')

def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task_detail.html', {'task': task})

def task_status(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    data = {
        'id': str(task.id),
        'status': task.status,
        'progress': task.progress,
        'started_at': task.started_at,
        'completed_at': task.completed_at
    }
    return JsonResponse(data)

def task_result(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    data = {
        'id': str(task.id),
        'status': task.status,
        'result': task.result,
        'error': task.error,
        'completed_at': task.completed_at
    }
    return JsonResponse(data)