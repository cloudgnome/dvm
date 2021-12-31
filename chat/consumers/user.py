from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils.translation import gettext_lazy as _
from chat.models import Chat,History
from chat.middleware.auth import login
from user.models import Session
from chat.views import serialize
from json import dumps,loads

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            self.scope['chat'] = Chat.objects.get(user_id=self.scope['user'],closed=False)
            # Send message to room group
            self.room_group_name = str(self.scope['user'].id)

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': {'history':serialize(History.objects.filter(chat=self.scope['chat']))},
                }
            )
        except Chat.DoesNotExist:
            self.scope['chat'] = Chat.objects.create(user_id=self.scope['user'].id)
            self.room_group_name = str(self.scope['chat'].id)

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        self.scope['user'].offline()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {'status':False},
            }
        )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        message = loads(text_data)['message']

        if not self.scope['chat'].notified:
            await self.channel_layer.group_send(
                'admin_channel',
                {
                    'type':'chat_message',
                    'message':{'name':self.scope['user'].full_name,'id':self.scope['chat'].id,'notified':self.scope['chat'].notified}
                }
            )

        # Send message to room group
        await self.channel_layer.group_send(
            str(self.scope['chat'].id),
            {
                'type': 'chat_message',
                'message': {'name':self.scope['user'].full_name,'text':message,'type':'user'}
            }
        )

        History.objects.create(message=message,chat=self.scope['chat'],admin=False)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=dumps({'message': message}))