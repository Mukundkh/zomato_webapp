from django.shortcuts import render, redirect
from .models import restaurant_model
from django.core.mail import send_mail

from customer.models import MenuItem, OrderModel
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
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            address=address,
            city=city,
            state=state,
            postal_code=postal_code
        )
        order.items.add(*item_ids)

        # After all things are done confirmation email is to be send

        body = ('Thank you for your order. Your meals will be delivered as soon as possible\n'
                f'Your total: {price}\n'
                'Thank you again for your order')

        send_mail(
            'Thank you for your order',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }
        return redirect('order-confirmation', pk=order.pk)

