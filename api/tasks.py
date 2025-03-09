import time
import random
from celery import shared_task
from django.utils import timezone

@shared_task(bind=True)
def execute_task(self, task_id, task_type, parameters):
    from .models import Task
    
    try:
        task = Task.objects.get(id=task_id)
        task.status = 'RUNNING'
        task.started_at = timezone.now()
        task.celery_task_id = self.request.id
        task.save()
        
        total_iterations = 10
        for i in range(total_iterations):
            time.sleep(2)
            
            progress = int((i + 1) / total_iterations * 100)
            self.update_state(state='RUNNING', meta={'progress': progress})
            
            task.progress = progress
            task.save(update_fields=['progress', 'updated_at'])
        
        if task_type == 'data_processing':
            result = process_data(parameters)
        elif task_type == 'report_generation':
            result = generate_report(parameters)
        elif task_type == 'video_processing':
            result = process_video(parameters)
        else:
            result = dummy_processing(parameters)
        
        task.status = 'COMPLETED'
        task.result = result
        task.completed_at = timezone.now()
        task.save()
        
        return result
    
    except Task.DoesNotExist:
        return {"error": "Task not found"}
    except Exception as e:
        try:
            task.status = 'FAILED'
            task.error = str(e)
            task.save()
        except:
            pass
        raise

def process_data(parameters):
    time.sleep(random.randint(2, 5))
    sample_size = parameters.get('sample_size', 100)
    return {
        'processed_rows': sample_size,
        'anomalies_detected': random.randint(0, int(sample_size * 0.1)),
        'processing_time': f"{random.uniform(1.0, 10.0):.2f} seconds"
    }

def generate_report(parameters):
    time.sleep(random.randint(3, 7))
    report_type = parameters.get('report_type', 'summary')
    period = parameters.get('period', 'monthly')
    
    return {
        'report_type': report_type,
        'period': period,
        'total_records': random.randint(1000, 5000),
        'generated_at': timezone.now().isoformat(),
        'report_url': f"https://example.com/reports/{random.randint(10000, 99999)}.pdf"
    }

def process_video(parameters):
    time.sleep(random.randint(5, 10))
    resolution = parameters.get('resolution', '720p')
    format_type = parameters.get('format', 'mp4')
    
    return {
        'original_duration': f"{random.uniform(10.0, 60.0):.2f} seconds",
        'processed_duration': f"{random.uniform(9.0, 55.0):.2f} seconds",
        'output_resolution': resolution,
        'output_format': format_type,
        'output_url': f"https://example.com/videos/{random.randint(10000, 99999)}.{format_type}"
    }

def dummy_processing(parameters):
    time.sleep(random.randint(1, 3))
    
    return {
        'parameters_received': parameters,
        'random_number': random.randint(1, 100),
        'timestamp': timezone.now().isoformat()
    }