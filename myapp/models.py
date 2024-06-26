from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
import uuid

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(max_length=80, unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(Usuario, self).save(*args, **kwargs)


class Oauth(models.Model):
    access_token = models.CharField(max_length=255, unique=True, default='default_access_token')
    refresh_token = models.CharField(max_length=255, unique=True, default='default_refresh_token')
    expire_token = models.DateTimeField(default='2024-01-01 00:00:00')
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.token



class Tarea(models.Model):
    idUsuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, blank=True)
    fechaVencimiento = models.DateTimeField(default=timezone.now)  # Valor predeterminado usando timezone.now
    estado = models.CharField(max_length=30) 

    def __str__(self):
        return self.titulo



class HistorialTarea(models.Model):
    idTarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    detalle = models.CharField(max_length=200)

    def __str__(self):
        return self.detalle
