
from django.urls import path
from .usuario_views import RegisterView, UserListView
from .task_views import (
    TareaListCreateAPIView,
    TareaRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),

    path('usuarios/', UserListView.as_view(), name='user-list'),
    path('tareas/', TareaListCreateAPIView.as_view(), name='tarea-list-create'),
    path('tareas/<int:pk>/', TareaRetrieveUpdateDestroyAPIView.as_view(), name='tarea-detail'),
]
