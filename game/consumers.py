import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import GameSessionModel

class GameSessionConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def initialize(self, data):
        self.room_group_name = data
        print(self.room_group_name, self.channel_name)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

    def is_timeout(self):
        session = GameSessionModel.get_ongoing_session_by_url(self.room_group_name)
        return session is None

    def receive(self, text_data):
        data_json = json.loads(text_data)
        message = data_json['message']
        
        if ('type' in data_json and data_json['type'] == 'initialize'):
            self.initialize(message)
            return

        if self.is_timeout():
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'timeout_message',
                }
            )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'game_message',
                'message': message
            }
        )

    def game_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'message':message
        }))

    def timeout_message(self, event):
        self.send(text_data=json.dumps({
            'type':'timeout_message'
        }))