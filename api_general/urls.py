
from django.urls import path
from .usuario_views import RegisterView
from .task_views import (
    TareaListCreateAPIView,
    TareaRetrieveUpdateDestroyAPIView,
    TareaAssignUserAPIView,
    TareaChangeStatusAPIView,
)

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),

    path('tareas/', TareaListCreateAPIView.as_view(), name='tarea-list-create'),
    path('tareas/<int:pk>/', TareaRetrieveUpdateDestroyAPIView.as_view(), name='tarea-detail'),
    path('tareas/<int:pk>/asignar-usuario/', TareaAssignUserAPIView.as_view(), name='tarea-assign-user'),
    path('tareas/<int:pk>/cambiar-estado/', TareaChangeStatusAPIView.as_view(), name='tarea-change-status'),
]
