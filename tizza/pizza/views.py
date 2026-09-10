from django.shortcuts import render
from .models import Pizza
from django.http import HttpResponse,JsonResponse
# Create your views here.
def index(request,pid):
    try:
        pizza=Pizza.objects.get(id=pid)

        return JsonResponse({
            'id':pizza.id,
            'title':pizza.title,
            'description':pizza.description
        })

    except Pizza.DoesNotExist:
        return JsonResponse({
            "status":"error",
            "message":"pizza not found"
        })