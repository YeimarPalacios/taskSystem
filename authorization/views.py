from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.models import Usuario, Oauth
from .serializers import UserSerializer, OauthSerializer
from django.core import serializers
from datetime import datetime, timedelta
import jwt
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password


#@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    def post(self, request):
        print("Invocaste al API ")
        print (request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('correo')
        password = request.data.get('password')
        try:
            user = Usuario.objects.get(correo=email)
        except Usuario.DoesNotExist:
            return Response({"error": "Invalid correo or password"}, status=status.HTTP_400_BAD_REQUEST)
        
        if check_password(password, user.password):
             # Eliminar cualquier token existente para este usuario
            Oauth.objects.filter(user=user).delete()
            access_token = jwt.encode({'usuario_id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=settings.JWT_EXP_DELTA_MINUTES)}, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
            refresh_token = jwt.encode({'usuario_id': user.id, 'exp': datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_EXP_DELTA_DAYS)}, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
            oauth = Oauth(access_token=access_token, refresh_token=refresh_token, expire_token=datetime.utcnow() + timedelta(minutes=settings.JWT_EXP_DELTA_MINUTES), user=user)
            oauth.save()
             # Serializar el usuario en un JSON serializable
            serialized_user = {
                'nombre':user.nombre,
                'apellido':user.apellido,
                'correo':user.correo,
            }
            return Response({'access_token': access_token, 'refresh_token': refresh_token, 'user':serialized_user})
        return Response({"error": "Invalid correo or password"}, status=status.HTTP_400_BAD_REQUEST)

class IntrospectView(APIView):
    def post(self, request):
        access_token = request.data.get('access_token')
        try:
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            oauth = Oauth.objects.get(access_token=access_token)
            if oauth.expire_token < datetime.utcnow():
                return Response({"active": False}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({"active": True})
        except jwt.ExpiredSignatureError:
            return Response({"active": False}, status=status.HTTP_401_UNAUTHORIZED)
        except (jwt.InvalidTokenError, Oauth.DoesNotExist):
            return Response({"active": False}, status=status.HTTP_401_UNAUTHORIZED)

class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            oauth = Oauth.objects.get(refresh_token=refresh_token)
            if oauth.expire_token < datetime.utcnow():
                return Response({"error": "Refresh token expired"}, status=status.HTTP_401_UNAUTHORIZED)
            
            access_token = jwt.encode({'usuario_id': payload['usuario_id'], 'exp': datetime.utcnow() + timedelta(minutes=settings.JWT_EXP_DELTA_MINUTES)}, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
            oauth.access_token = access_token
            oauth.expire_token = datetime.utcnow() + timedelta(minutes=settings.JWT_EXP_DELTA_MINUTES)
            oauth.save()
            return Response({'access_token': access_token})
        except jwt.ExpiredSignatureError:
            return Response({"error": "Refresh token expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except (jwt.InvalidTokenError, Oauth.DoesNotExist):
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        access_token = request.data.get('access_token')
        try:
            oauth = Oauth.objects.get(access_token=access_token)
            oauth.delete()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Oauth.DoesNotExist:
            return Response({"error": "Invalid access token"}, status=status.HTTP_400_BAD_REQUEST)
