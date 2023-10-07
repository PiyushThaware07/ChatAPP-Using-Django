from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
import json
from .models import *
from channels.db import database_sync_to_async

''' ===================================================================
Sync Consumer 
=================================================================== '''


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('Websocket Connected...', event)
        # Get a default channel layers from a project.
        print('==========>> Channel Layers : ', self.channel_layer)
        # Get a default channel Name from a project.
        print('==========>> Channel Name : ', self.channel_name)

        # Getting Group Name
        print('====================>> Group Name ',
              self.scope['url_route']['kwargs']['RoomName'])
        self.group_name = self.scope['url_route']['kwargs']['RoomName']
        # Getting User Name
        print('====================>> User Name ',
              self.scope['url_route']['kwargs']['UserName'])
        self.user_name = self.scope['url_route']['kwargs']['UserName']

        # Add different channels or user in a room or group : self.channel_layer.group_add('room name',user or self.channels)
        async_to_sync(self.channel_layer.group_add)(   # add a channel to a new or existing group.
            self.group_name,
            self.channel_name
        )

        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print('Message Received From Client...',
              event["text"])
        # json string to python dict
        mydict = json.loads(event['text'])
        print("String To Python : ", mydict, mydict['msg'], mydict['user'])
        mydict['user'] += self.user_name
        print("String To Python --: ", mydict, mydict['msg'], mydict['user'])

        # Saving To Database
        group = Group.objects.get(name=self.group_name)  # find group object 
        # creating new chat object 
        chat = Chat(content=mydict['msg'],group=group)
        chat.save()

        # Send Received Msg to client as msg is already in text so simple send or forward it to group or room
        async_to_sync(self.channel_layer.group_send)(self.group_name, {
            'type': 'chat.message',  # event following is handler
            'message': json.dumps(mydict)
        })  # abhi is code mein sirf hum n msg ko group mein send kiya hai abhi ye humko group mein bhi send karna hai.

    #  Using This handler you can send data from server to client

    def chat_message(self, event):  # handler for event chat.message
        print('Event...', event, '\n Actual Data : ',
              type(event['message']), event['message'])
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    def websocket_disconnect(self, event):
        # Get a default channel layers from a project.
        print('==========>> Channel Layers : ', self.channel_layer)
        # Get a default channel Name from a project.
        print('==========>> Channel Name : ', self.channel_name)

        ''' =========== Discard Group / Channel =========== '''
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name)

        print('Websocket Disconnected...', event)
        raise StopConsumer()


''' ===================================================================
Async Consumer 
=================================================================== '''

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('Websocket Connected...', event)
        # Get a default channel layers from a project.
        print('==========>> Channel Layers : ', self.channel_layer)
        # Get a default channel Name from a project.
        print('==========>> Channel Name : ', self.channel_name)
        # Getting Group Name
        print('====================>> Group Name ',
              self.scope['url_route']['kwargs']['RoomName'])
        self.group_name = self.scope['url_route']['kwargs']['RoomName']
        # Getting User Name
        print('====================>> User Name ',
              self.scope['url_route']['kwargs']['UserName'])
        self.user_name = self.scope['url_route']['kwargs']['UserName']

        # Add different channels or user in a room or group : self.channel_layer.group_add('room name',user or self.channels)
        await self.channel_layer.group_add(   # add a channel to a new or existing group.
            self.group_name,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    @sync_to_async
    def save_chat_message(self, content, group):
        chat = Chat(content=content, group=group)
        chat.save()

    async def websocket_receive(self, event):
        print('Message Received From Client...',
              event["text"])
        # json string to python dict
        mydict = json.loads(event['text'])
        print("String To Python : ", mydict, mydict['msg'], mydict['user'])
        mydict['user'] += self.user_name
        print("String To Python --: ", mydict, mydict['msg'], mydict['user'])

        # Saving To Database using sync_to_async
        group = await sync_to_async(Group.objects.get)(name=self.group_name)
        await self.save_chat_message(mydict['msg'], group)

        # Send Received Msg to client as msg is already in text so simple send or forward it to group or room
        await self.channel_layer.group_send(self.group_name, {
            'type': 'chat.message',  # event following is handler
            'message': json.dumps(mydict)
        })  # abhi is code mein sirf hum n msg ko group mein send kiya hai abhi ye humko group mein bhi send karna hai.

    #  Using This handler you can send data from server to client

    async def chat_message(self, event):  # handler for event chat.message
        print('Event...', event, '\n Actual Data : ',
              type(event['message']), event['message'])
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    async def websocket_disconnect(self, event):
        # Get a default channel layers from a project.
        print('==========>> Channel Layers : ', self.channel_layer)
        # Get a default channel Name from a project.
        print('==========>> Channel Name : ', self.channel_name)

        ''' =========== Discard Group / Channel =========== '''
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

        print('Websocket Disconnected...', event)
        raise StopConsumer()




