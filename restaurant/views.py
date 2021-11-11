from django.shortcuts import render
from .models import restaurant_model
from customer.models import MenuItem
from django.views import View

# Create your views here.


def index(request):
    rest = restaurant_model.objects.all()
    return render(request, 'restaurant/index.html', {
        "rest": rest
    })


class restaurant_detail(View):
    def get(self, request, *args, **kwargs):
        searchkey = ''
        rest_id = kwargs['id']
        if 'search' in request.GET:
            searchkey = request.GET['search']
        print(searchkey)
        rest = restaurant_model.objects.get(pk=rest_id)

        main_course = MenuItem.objects.filter(restaurant__id=rest_id).filter(
            category__name__contains='Main Course').filter(name__contains=searchkey)
        starters = MenuItem.objects.filter(restaurant__id=rest_id).filter(
            category__name__contains='Starters').filter(name__contains=searchkey)
        deserts = MenuItem.objects.filter(restaurant__id=rest_id).filter(
            category__name__contains='Deserts').filter(name__contains=searchkey)
        drinks = MenuItem.objects.filter(restaurant__id=rest_id).filter(
            category__name__contains='Drinks').filter(name__contains=searchkey)

        context = {
            'restaurant': rest.name,
            'main_course': main_course,
            'starters': starters,
            'deserts': deserts,
            'drinks': drinks,
        }
        return render(request, 'restaurant/restaurant_detail.html', context)

    def post(self, request, *args, **kwargs):
        pass
