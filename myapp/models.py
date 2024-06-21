from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(max_length=80)
    password = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class Oauth(models.Model):
    expiryDate = models.DateTimeField()
    token = models.CharField(max_length=255)
    tokenRefresh = models.CharField(max_length=255)
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.token

class Tarea(models.Model):
    idUsuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, blank=True)
    fechaVencimiento = models.DateTimeField(default=timezone.now)  # Valor predeterminado usando timezone.now
    estado = models.CharField(max_length=30, default='pendiente')

    def __str__(self):
        return self.titulo

class HistorialTarea(models.Model):
    idTarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    detalle = models.CharField(max_length=200)

    def __str__(self):
        return self.detalle
