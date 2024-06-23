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

class ConsultarTaskView(APIView):
    def get(self, request):
       return Response({"message": "aca se debe hacer la consulta de las tareas"}, status=status.HTTP_200_OK)

class EliminarTaskView(APIView):
    def delete(self, request):
        return Response({"message": "aca se debe eliminar las tareas"}, status=status.HTTP_200_OK)

