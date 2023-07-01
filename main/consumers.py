from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .models import Message, EndUser, Creator
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

class BoothConsumer(WebsocketConsumer):

    def fetch_message(self, data):
        messages = Message.objects.order_by('-time_stamp')[:10]
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages[::-1])
        }
        self.send_chat_message(content)



    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.time_stamp),
            'receiver': message.receiver.username,
        }
    def new_message(self, data):
        author = data['from']
        author_user = User.objects.get(username=author)

        receiver = data['to']
        try:
            receiver_user = User.objects.get(username=receiver)
        except User.DoesNotExist:
            # Handle the case when the receiver user does not exist
            # You can raise an exception, send an error message to the client, or log the error
            # Here, we're raising a ValueError and sending an error message to the client
            error_message = 'Receiver user does not exist'
            content = {
                'command': 'error',
                'message': error_message
            }
            return self.send_chat_message(content)

        message = Message.objects.create(
            author=author_user,
            content=data['message'],
            receiver=receiver_user
        )

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    commands = {
        'fetch_messages': fetch_message,
        'new_message': new_message
    }

    def connect(self):
        self.booth_name = self.scope['url_route']['kwargs']['booth_name']
        self.booth_group_name = 'creator_chat_%s' % self.booth_name

        async_to_sync(self.channel_layer.group_add)(
            self.booth_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.booth_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.booth_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chatroom_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
