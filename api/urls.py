from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

public_router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('', include(public_router.urls)),
]