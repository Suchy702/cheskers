import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

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

    def receive(self, text_data):
        data_json = json.loads(text_data)
        message = data_json['message']
        
        if ('type' in data_json and data_json['type'] == 'initialize'):
            self.initialize(message)
            return

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