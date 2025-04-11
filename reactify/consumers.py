import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatRoom, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        # Check if room exists
        room_exists = await self.room_exists(self.room_id)
        if not room_exists:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Add user to room participants if authenticated
        # if self.scope["user"].is_authenticated:
        #     await self.add_user_to_room(self.scope["user"], self.room_id)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        full_name = data.get("full_name")

        # Save message to database
        db_message = await self.save_message(self.room_id, full_name, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "full_name": full_name,
                "message_id": db_message.id,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        full_name = event["full_name"]
        message_id = event["message_id"]

        # Send message to WebSocket
        full_name = event["full_name"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "message_id": message_id,
                    "full_name": full_name,
                }
            )
        )

    @database_sync_to_async
    def room_exists(self, room_id):
        return ChatRoom.objects.filter(id=room_id).exists()

    @database_sync_to_async
    def add_user_to_room(self, user, room_id):
        try:
            room = ChatRoom.objects.get(id=room_id)
            room.participants.add(user)
        except ChatRoom.DoesNotExist:
            pass

    @database_sync_to_async
    def save_message(self, room_id, full_name, message):
        room = ChatRoom.objects.get(id=room_id)
        try:
            return Message.objects.get(room=room, full_name=full_name, content=message)
        except Message.MultipleObjectsReturned:
            return Message.objects.filter(
                room=room, full_name=full_name, content=message
            ).first()
        except Message.DoesNotExist:
            return Message.objects.create(
                room=room, full_name=full_name, content=message
            )
