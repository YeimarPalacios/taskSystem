from rest_framework import serializers
from myapp.models import Usuario


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre','apellido','correo','password']