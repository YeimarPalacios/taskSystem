from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from .custom_session_info import CustomSessionInfo
from .custom_anonymous_user import CustomAnonymousUser
import json

class CustomAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        print("Estoy en CustomAuthMiddleware::::")
        # Obtener la información de la sesión desde el Singleton
        session_info = CustomSessionInfo().get_session_info()
        print ("EStoy usando el singleton")
        if session_info is not None:
            #user = session_info['user']
            scope['user'] = session_info
            print("singleton lleno")
        else:
            scope['user'] = CustomAnonymousUser()
            print("singleton vacio")

        return await super().__call__(scope, receive, send)

def CustomAuthMiddlewareStack(inner):
    return CustomAuthMiddleware(inner)
