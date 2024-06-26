from django.urls import path
from . import views
from django.urls import include
from .notifications import routing  

urlpatterns = [
    path('', views.example_view, name='example'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('menu/', views.menu_view, name='menu'),
    path('panel/', views.panel_view, name='panel'),
    path('registro/', views.registro_view, name='registro'),
    path('ws/', include(routing.websocket_urlpatterns)),  # Rutas WebSocket de tu aplicación
    path('render_task_item/', views.render_task_item, name='render_task_item'),
]
