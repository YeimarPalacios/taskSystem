from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.models import Usuario, Oauth
from .serializers import UserSerializer
from django.core import serializers
from datetime import datetime, timedelta
import jwt
import pytz
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    def get(self, request):
        users = Usuario.objects.all()  # Obtén todos los usuarios
        serializer = UserSerializer(users, many=True)  # Serializa los datos de los usuarios

        return Response(serializer.data, status=status.HTTP_200_OK)