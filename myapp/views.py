import json
import requests
from django.shortcuts import render, redirect
from myapp.forms.forms import LoginForm, RegistroForm
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .decorators import require_authentication

def vista_no_protegida(request):
    # Esta vista solo será accesible si el usuario está autenticado
    return JsonResponse({'mensaje': 'publico'})


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
                request.session['authorization'] = response.json()
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

#@csrf_exempt
#@require_authentication
def panel_view(request):
     # Obtén el token JWT almacenado en la sesión
    authorization_data = request.session.get('authorization', None)
    if authorization_data is None:
        # Si no hay token JWT, redirige al login
        return redirect('login')

    user_data = authorization_data['user']
    return render(request, 'panel.html', {'user': user_data})

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
                f'{settings.API_BASE_URL}/authorization/api/register/',
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


def render_task_item(request):
    if request.method == 'GET':
        title = request.GET.get('title')
        desc = request.GET.get('desc')
        assign_email = request.GET.get('assign')

        correo = re.sub(r'[^\w.-]', '', assign_email)[:100]
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     f'user_{correo}',
        #     {
        #         'type': 'send_notification',
        #         'message': f'Nueva tarea asignada: {title}'
        #     }
        # )

        context = {
            'title': title,
            'desc': desc,
            'assign': assign_email,
            'user': correo
        }

        html = render_to_string('task_item.html', context=context)
        return JsonResponse({'html': html})
    return JsonResponse({'error': 'Método no permitido'})
        