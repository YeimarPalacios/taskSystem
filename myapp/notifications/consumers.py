# myapp/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from myapp.security.custom_anonymous_user import CustomAnonymousUser
import re

class NotificationConsumer(AsyncWebsocketConsumer):
    print ("Estoy en NotificationConsumer")

    async def connect(self):
        print("estoy conectado a NotificationConsumer")
        self.user = self.scope["user"]
        #print(f'user_{self.user.nombre}{self.user.apellido}')
        correo = re.sub(r'[^\w.-]', '', self.user['correo'])[:100]
        print(f'user_{correo}')
        self.group_name = f'user_{correo}'

        if isinstance(self.user, CustomAnonymousUser):
            await self.close()
        else:
            self.group_name = f'user_{correo}'
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def send_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
