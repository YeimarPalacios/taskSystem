from django.urls import path
from .views import RegisterView, LoginView, IntrospectView, RefreshTokenView, LogoutView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/authentication/', LoginView.as_view(), name='authentication'),
    path('api/introspect/', IntrospectView.as_view(), name='introspect'),
    path('api/refresh_token/', RefreshTokenView.as_view(), name='refresh_token'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]
