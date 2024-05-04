from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.forms import model_to_dict
import json
# Create your models here.

class Currency(models.Model):
    title = models.CharField(max_length = 255)
    code = models.CharField(max_length = 8)
    
    def __str__(self) -> str:
        return self.title
    
    
class PriceAction(models.Model):
    currency = models.ForeignKey(Currency,on_delete = models.CASCADE) 
    price = models.IntegerField()
    created = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f"{self.currency} - {self.price}"
    
    
@receiver(post_save , sender=PriceAction)
def price_action_sender(sender,instance,created,**kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('prices',{'type':'change','text':json.dumps({'created':str(instance.created),'price':instance.price})})