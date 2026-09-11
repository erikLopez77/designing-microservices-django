import json
from .models import Pizza
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
# Create your views here.

class GetTenPizzasView(View):
    template_name = 'ten_pizzas.html'
    def get(self, request):
        pizzas = Pizza.objects.order_by('?')[:10]
        return render(request, self.template_name, {'pizzas': pizzas})

@login_required
def index(request,pid):
    if request.method== 'POST':
        data=json.loads(request.body)
        new_pizza=Pizza.objects.create(
            title=data['title'],
            description=data['description'],
            creator=request.user,
        )
        new_pizza.save()
        return JsonResponse(
            content={
                'id': new_pizza.id,
                'title': new_pizza.title,
                'description': new_pizza.description,
            }
        )
    elif request.method== 'GET':
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
    elif request.method == 'DELETE':
        if 'can_delete' in request.user_permissions:
            pizza=Pizza.objects.get(id=pid)
            pizza.delete()
            return JsonResponse(
                content={
                    'id':pizza.id
                }
            )
        else:
            return JsonResponse(status_code=404)