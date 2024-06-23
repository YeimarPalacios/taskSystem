from functools import wraps
from django.http import JsonResponse
from myapp.security.middleware import JWTMiddleware


def require_authentication(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        response = JWTMiddleware.validateJwt(request)
        if isinstance(response, JsonResponse):
            return response
        return view_func(request, *args, **kwargs)
    return wrapper