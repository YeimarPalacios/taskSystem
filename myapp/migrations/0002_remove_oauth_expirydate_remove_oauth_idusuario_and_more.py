# Generated by Django 5.0.6 on 2024-06-22 19:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oauth',
            name='expiryDate',
        ),
        migrations.RemoveField(
            model_name='oauth',
            name='idUsuario',
        ),
        migrations.RemoveField(
            model_name='oauth',
            name='token',
        ),
        migrations.RemoveField(
            model_name='oauth',
            name='tokenRefresh',
        ),
        migrations.AddField(
            model_name='oauth',
            name='access_token',
            field=models.CharField(default='default_access_token', max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='oauth',
            name='expire_token',
            field=models.DateTimeField(default='2024-01-01 00:00:00'),
        ),
        migrations.AddField(
            model_name='oauth',
            name='refresh_token',
            field=models.CharField(default='default_refresh_token', max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='oauth',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.usuario'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='correo',
            field=models.EmailField(max_length=80, unique=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.CharField(max_length=255),
        ),
    ]