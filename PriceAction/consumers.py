from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class PriceConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)('prices',self.channel_name)
    
    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        self.send("thank you")
        
    def change(self,event):
        self.send(text_data=event['text'])