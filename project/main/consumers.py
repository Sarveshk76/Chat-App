import random
from channels.generic.websocket import  AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from accounts.models import User
import json



class ChatRoomConsumer(AsyncJsonWebsocketConsumer):

    groups = ["broadcast"]

    async def connect(self):
        self.my_id = self.scope['user'].id
        self.other_user_id = self.scope['url_route']['kwargs']['id']

        if int(self.my_id)>int(self.other_user_id):
            self.room_name = f'{self.my_id}-{self.other_user_id}'
        else:
            self.room_name = f'{self.other_user_id}-{self.my_id}'
        # self.scope["session"]["seed"] = random.randint(1, 1000)

        self.room_group_name = 'chat_%s' % self.room_name


        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.set_status_online()


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        try:
            message = text_data_json['message']
        except:
            print(text_data_json)
        channel_layer = get_channel_layer()
        try:
            await channel_layer.group_send(
            self.room_group_name,
            {
            'type': 'chat_message',
            'message': message,
            'my_user': self.my_id,
            }
            )
        except:
            pass


    async def chat_message(self, event):
        message = event["message"]
        my_user = await database_sync_to_async(User.objects.get)(id=event['my_user'])
        
        await self.send(text_data=json.dumps({"message": message, "my_user": {'id':my_user.id, 'name':my_user.full_name}}))

    # Function to update online status
    @database_sync_to_async
    def set_status_online(self):
        User.objects.filter(id=self.my_id).update(is_online=True)
    
    @database_sync_to_async
    def set_status_offline(self):
        User.objects.filter(id=self.my_id).update(is_online=False)
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        await self.set_status_offline()

        print("Disconnected!!")


class UserConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        pass

    async def recieve(self, text_data):
        pass

    async def disconnect(self, code):
        pass
