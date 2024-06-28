
from django.urls import path
from .usuario_views import RegisterView, UserListView
from .task_views import (
    TareaListCreateAPIView,
    TareaRetrieveUpdateDestroyAPIView,
)
from .historialTarea_views import HistorialTareaListCreateAPIView, HistorialTareaDetailAPIView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),

    path('usuarios/', UserListView.as_view(), name='user-list'),
    path('usuarios/<int:pk>/', UserListView.as_view(), name='user-detail'),
    path('tareas/', TareaListCreateAPIView.as_view(), name='tarea-list-create'),
    path('tareas/<int:pk>/', TareaRetrieveUpdateDestroyAPIView.as_view(), name='tarea-detail'),

    path('historial_tareas/', HistorialTareaListCreateAPIView.as_view(), name='historial-tarea-list-create'),
    path('historial_tareas/<int:idTarea>/', HistorialTareaDetailAPIView.as_view(), name='historial_tarea_detail'),
]
