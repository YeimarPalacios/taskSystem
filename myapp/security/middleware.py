from django.http import JsonResponse
from django.conf import settings
from jwt import decode, ExpiredSignatureError
import requests


class JWTMiddleware:

    @staticmethod
    def validateJwt(request):
        print("entré a validar el access_token")
        authorization_data = request.session.get('authorization', None)
        if authorization_data is not None and 'access_token' in authorization_data:
            access_token = authorization_data['access_token']
            print("acá hay un access-token")
            print(access_token)
            if access_token:
                try:
                    payload = decode(access_token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
                    # Llamar a la vista IntrospectView para validar el token
                    response = JWTMiddleware.call_introspect(access_token)
                    if response.status_code == 200:
                        return None  # Token is valid, continue processing the request
                    else:
                        # El token es inválido, realizar el proceso de refresh_token
                        refresh_token = authorization_data['refresh_token']
                        response = JWTMiddleware.call_refresh_token(refresh_token)
                        print("refresh por que el instrospect respondio mal")
                        return JWTMiddleware.validate_response_refresh(response, request)
                except ExpiredSignatureError:
                    # El token ha expirado, realizar el proceso de refresh_token
                    refresh_token = authorization_data['refresh_token']
                    response = JWTMiddleware.call_refresh_token(refresh_token)
                    print("refresh por que el access_token es expiró")
                    return JWTMiddleware.validate_response_refresh(response, request)
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=401)
            else:
                return JsonResponse({'error': 'Token no proporcionado'}, status=401)
        else:
            return JsonResponse({'error': 'No has iniciado sesión'}, status=401)

    @staticmethod
    def call_refresh_token(refresh_token):
        return requests.post(f'{settings.API_BASE_URL}/authorization/api/refresh_token/', data={'refresh_token': refresh_token})   

    @staticmethod
    def call_introspect(access_token):
        return requests.post(f'{settings.API_BASE_URL}/authorization/api/introspect/', data={'access_token': access_token})

    @staticmethod
    def validate_response_refresh(response, request):
        if response.status_code == 200:
            request.session['authorization'] = response.json()
            return None  # Continue processing the request after refreshing the token
        else:
            return JsonResponse({'error': 'No autorizado - refresh'}, status=401)