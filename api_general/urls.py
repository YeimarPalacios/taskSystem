from django.urls import path
from .task_views import ConsultarTaskView
from .usuario_views import RegisterView

urlpatterns = [
    path('api/tasks/', ConsultarTaskView.as_view(), name='tasks'),
    path('api/register/', RegisterView.as_view(), name='register'),
]
