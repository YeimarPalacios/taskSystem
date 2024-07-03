import json
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from myapp.forms.forms import LoginForm, RegistroForm
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from myapp.security.decorators import require_authentication
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
import re


def example_view(request):
    return render(request, 'example.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            password = form.cleaned_data['password']
            serialized_data = {
                'correo': correo,
                'password': password, 
            }
            response = requests.post(
                f'{settings.API_BASE_URL}/authorization/api/authentication/',
                json=serialized_data
            )

            if response.status_code == 200:
                session_info = response.json()
                request.session['authorization'] = session_info
                
                return redirect('panel')
            else:
                # Mostrar un mensaje de error al usuario
                messages.error(request, 'Credenciales inválidas.')
                return render(request, 'login.html', {'form': form, 'error': 'Credenciales inválidas.'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def menu_view(request):
    return render(request, 'menu.html')

@csrf_exempt
@require_authentication
def panel_view(request):
     # Obtén el token JWT almacenado en la sesión
    authorization_data = request.session.get('authorization', None)
    if authorization_data is None:
        # Si no hay token JWT, redirige al login
        return redirect('login')

    user_data = authorization_data['user']
    return render(request, 'panel.html', {'user': user_data})

def historialTarea_View(request):
     # Obtén el token JWT almacenado en la sesión
    authorization_data = request.session.get('authorization', None)
    if authorization_data is None:
        # Si no hay token JWT, redirige al login
        return redirect('login')

    user_data = authorization_data['user']
    return render(request, 'historialTarea.html', {'user': user_data})


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
                    # Realizar la llamada a la API de registro de usuario
            # Obtener los datos validados del formulario
            form_data = form.cleaned_data

            # Crear un nuevo diccionario con los campos requeridos para la serialización
            serialized_data = {
                'nombre': form_data['nombre'],
                'apellido': form_data['apellido'],
                'correo': form_data['correo'],
                'password': form_data['password1'],  # Utiliza password1 en lugar de password
            }
            response = requests.post(
                f'{settings.API_BASE_URL}/services/api/register/',
                json=serialized_data
            )

            if response.status_code == 201:
                # El usuario se registró exitosamente
                messages.success(request, 'Registro exitoso. Por favor, inicia sesión.')
                return redirect('/login/')  # Redireccionar a la página de inicio de sesión
            else:
                # Mostrar un mensaje de error al usuario
                messages.error(request, 'Error al registrar el usuario.')
                return render(request, 'registro.html', {'form': form, 'error': 'Error al registrar el usuario.'})

        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

# @csrf_exempt
# @require_authentication
def asignar_tarea(request):
    if request.method == 'GET':
        # title = request.GET.get('title')
        assign_task = request.GET.get('taskId')
        assign_user = request.GET.get('userId')
        
        serialized_data = {
                'idUsuario': assign_user
            }
        response = requests.put(
                f'{settings.API_BASE_URL}/services/tareas/{assign_task}/',
                json=serialized_data
            )

        if response.status_code == 200:
            user = response.json()
            correo = re.sub(r'[^\w.-]', '', user['correo'])[:100]
            tarea_nombre=  user['tarea']['titulo']
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'user_{correo}',
                {
                    'type': 'send_notification',
                    'message': f'Nueva tarea asignada: { tarea_nombre }'
                }
        )

        return JsonResponse(response.json())

def logout_view(request):

    if request.method == 'POST':
    # Obtener el token de acceso de la sesión del usuario
        authorization_data = request.session.get('authorization', None)
       
        if authorization_data:
            access_token = authorization_data['access_token']
            # Llamar a la API de cierre de sesión
            response = requests.post(
                f'{settings.API_BASE_URL}/authorization/api/logout/',
                # json=serialized_data
                json={'access_token': access_token}
            )
            
            if response.status_code == 200:
                # Eliminar la información de autorización de la sesión
                del request.session['authorization']
                return redirect('login')
            else:
                return JsonResponse(response.json())
        else:
            return JsonResponse({'error': 'no esta autenticado'})
