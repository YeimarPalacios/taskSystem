from django.urls import path
from .views import LoginView, IntrospectView, RefreshTokenView, LogoutView

urlpatterns = [
    path('api/authentication/', LoginView.as_view(), name='authentication'),
    path('api/introspect/', IntrospectView.as_view(), name='introspect'),
    path('api/refresh_token/', RefreshTokenView.as_view(), name='refresh_token'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
]
