from rest_framework import serializers
from myapp.models import Usuario, Tarea, HistorialTarea

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id','nombre', 'apellido', 'correo', 'password']

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['id', 'titulo', 'descripcion', 'fechaVencimiento', 'estado', 'idUsuario']


class HistorialTareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialTarea
        fields = ['idTarea', 'detalle']