from functools import wraps
from django.http import JsonResponse

def require_authentication(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if hasattr(request, 'usuario_id'):
            # Si el usuario_id está presente en la solicitud, significa que el token JWT es válido
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'error': 'Autenticación requerida'}, status=401)
    return wrapper
