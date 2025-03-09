from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<uuid:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<uuid:task_id>/status/', views.task_status, name='task_status'),
    path('tasks/<uuid:task_id>/result/', views.task_result, name='task_result'),
]