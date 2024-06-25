from rest_framework import serializers
from myapp.models import Usuario, Tarea

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'password']

class TareaSerializer(serializers.ModelSerializer):
    idUsuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Tarea
        fields = ['id', 'titulo', 'descripcion', 'fechaVencimiento', 'estado', 'idUsuario']
