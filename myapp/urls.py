from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.example_view, name='example'),
    path('login/', views.login_view, name='login'),
    path('menu/', views.menu_view, name='menu'),
    path('panel/', views.panel_view, name='panel'),
    path('registro/', views.registro_view, name='registro'),
]
