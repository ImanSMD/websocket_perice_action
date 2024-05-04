from datetime import timedelta
from os import sync
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
import asyncio
from asgiref.sync import async_to_sync, sync_to_async


from PriceAction.models import PriceAction

# Create your views here.

def home(request):
    return render(request , 'home.html')


def short(request):
    itemes = PriceAction.objects.filter(created__gt = timezone.now()-timedelta(hours =1))
    return JsonResponse(list(itemes.values()), safe=False)

  
@sync_to_async    
def get_content(from_date):
    return PriceAction.objects.filter(created__gt = from_date)

async def long(request):
    items = []
    for i in range(1,5):
        result = await get_content(request.GET['from'])
        if result.count()>0:
            items = list(result.values())
            break
        print('waiting ... ',i)
        await asyncio.sleep(5)
    return JsonResponse(items , safe=False)