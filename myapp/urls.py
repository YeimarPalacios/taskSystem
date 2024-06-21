from django.urls import path
from . import views

urlpatterns = [
    path('', views.example_view, name='example'),
    path('login/', views.login_view, name='login'),
    path('menu/', views.menu_view, name='menu'),
    path('panel/', views.panel_view, name='panel'),
    path('registro/', views.registro_view, name='registro'),
    path('tarea/<int:tarea_id>/', views.task_item_view, name='task_item'),
    # Otras rutas que puedas tener
]
