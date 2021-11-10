from django.shortcuts import render
from .models import restaurant_model
# Create your views here.


def index(request):
    rest = restaurant_model.objects.all()
    return render(request, 'restaurant/index.html', {
        "rest": rest
    })


def restaurant_detail(request, id):
    #print(id)
    rest = restaurant_model.objects.get(pk=id)
    return render(request, 'restaurant/restaurant_detail.html', {
        'name': rest.name,
        'description': rest.description,
        'address' : rest.address,
        'phone' : rest.phone,
        'open_time' : rest.open_time,
        'close_time' : rest.close_time,
    })
