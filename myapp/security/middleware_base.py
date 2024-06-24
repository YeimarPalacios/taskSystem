from django.http import JsonResponse
from django.conf import settings
from jwt import decode, ExpiredSignatureError
from django.shortcuts import redirect
import requests
from .custom_session_info import CustomSessionInfo


class BaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("estoy pasando por el middleware base")
        authorization_data = request.session.get('authorization', None)
        if authorization_data is not None and 'access_token' in authorization_data:
            token = authorization_data['access_token']
            if token:
                print("desde middleware base con sesión")
                CustomSessionInfo().set_session_info(authorization_data['user'])  # Guardar la información en el Singleton

        return self.get_response(request)
           