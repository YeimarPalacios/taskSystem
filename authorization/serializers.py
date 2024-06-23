from rest_framework import serializers
from myapp.models import Usuario, Oauth


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre','apellido','correo','password']

class OauthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oauth
        fields = ['access_token', 'refresh_token', 'expire_token', 'usuario']
