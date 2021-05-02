import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

from .models import Message, ChatRoom, AddToFriendNotification
from .logic.serialilazer import get_message_data_as_dict, get_notification_data_as_dict


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message_text = text_data_json['message']
        author = text_data_json['author']

        new_message = await self.create_new_message(message_text)
        time_sended = new_message.sended.strftime("%B %d, %Y, %H:%M")

        message = await database_sync_to_async(get_message_data_as_dict)(author=author, text=message_text, message_sended=time_sended)

        await  self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    
    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
        }))

    
    @database_sync_to_async
    def create_new_message(self, text):
        from_user = self.scope['user']
        chat_room = ChatRoom.objects.get(name=self.room_name)
        new_message = Message.objects.create(
            from_user=from_user, chat_room=chat_room, text=text
        )
        return new_message



class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            self.user_id = self.scope['user'].id
            self.user_group_name = f'user_{self.user_id}'
            await self.channel_layer.group_add(
                self.user_group_name,
                self.channel_name
            )

        await self.accept()

    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        notification_to = text_data_json['notification_to']
        if notification_to:
            notification_from = self.scope['user'].id
            notification = await self.create_new_notification(from_user=notification_from, to_user=notification_to)
            # notif = await get_notification_data_as_dict(notif_id=notification.id)
            notif = {
                'send_from': notification.send_from.username,
                'send_from_url': '#',
            }
            await self.channel_layer.group_send(
                f'user_{notification_to}',
                {
                    'type': 'new_notification',
                    'notif': notif
                }
            )


    @database_sync_to_async
    def create_new_notification(self, from_user, to_user):
        send_from_user = User.objects.get(id=int(from_user))
        send_to_user = User.objects.get(id=int(to_user))
        # new_notif = AddToFriendNotification.objects.create(send_from=send_from_user, send_to=send_to_user)
        new_notif = AddToFriendNotification(send_from=send_from_user, send_to=send_to_user)
        return new_notif 


    
    async def new_notification(self, event):
        notif = event['notif']
        await self.send(text_data=json.dumps({
            'notif': notif
        }))


    async def disconnect(self, exit_code):
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )