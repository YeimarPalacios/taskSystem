from rest_framework import serializers
from myapp.models import  Oauth


class OauthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oauth
        fields = ['access_token', 'refresh_token', 'expire_token', 'usuario']
