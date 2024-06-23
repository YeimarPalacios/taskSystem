from django.http import JsonResponse
from django.conf import settings
from jwt import decode, ExpiredSignatureError
from django.shortcuts import redirect
import requests


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info.lstrip('/')
        print("mirame aqui")
        print(path)
        if not any(path.startswith(url) for url in settings.PUBLIC_URLS):
            # Obtén el token JWT almacenado en la sesión
            authorization_data = request.session.get('authorization', None)
            if authorization_data is not None and 'access_token' in authorization_data:
                token = authorization_data['access_token']

                if token:
                    try:
                        # Decodificar el token para validar su validez y obtener el usuario_id
                        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
                        usuario_id = payload['usuario_id']

                        # Llamar a la vista IntrospectView para validar el token
                        response = requests.post(f'{settings.API_BASE_URL}/authorization/api/introspect', data={'token': token})
                        if response.status_code == 200:
                            # El token es válido, continuar con la solicitud
                            request.usuario_id = usuario_id
                            return self.get_response(request)
                        else:
                            # El token es inválido, realizar el proceso de refresh_token
                            return JsonResponse({'error': 'Token inválido'}, status=401)
                    except ExpiredSignatureError:
                        # El token ha expirado, realizar el proceso de refresh_token
                        return JsonResponse({'error': 'Token expirado'}, status=401)
                    except Exception as e:
                        return JsonResponse({'error': str(e)}, status=401)
                else:
                    return JsonResponse({'error': 'Token no proporcionado'}, status=401)
            else:
                #return redirect('login')
                return JsonResponse({'error': 'No has iniciado sesión'}, status=401)
        return self.get_response(request)