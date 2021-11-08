from django.shortcuts import render,redirect
from django.views import View
from .models import MenuItem, Category, OrderModel
from django.core.mail import send_mail

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')




class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        main_course = MenuItem.objects.filter(category__name__contains='Main Course')
        starters = MenuItem.objects.filter(category__name__contains='Starters')
        deserts = MenuItem.objects.filter(category__name__contains='Deserts')
        drinks = MenuItem.objects.filter(category__name__contains='Drinks')

        print(main_course,starters,deserts,drinks);

        # pass into context
        context = {
            'main_course': main_course,
            'starters': starters,
            'deserts': deserts,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'customer/order.html', context)

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
            price = price,
            name = name,
            email = email,
            address = address,
            city = city,
            state = state,
            postal_code = postal_code
            )
        order.items.add(*item_ids)

        #After all things are done confirmation email is to be send

        body = ('Thank you for your order. Your meals will be delivered as soon as possible\n'
            f'Your total: {price}\n'
            'Thank you again for your order')

        send_mail(
            'Thank you for your order',
            body,
            'example@example.com',
            [email],
            fail_silently = False
        )


        context = {
            'items': order_items['items'],
            'price': price
        }
        return redirect('order-confirmation',pk=order.pk)

class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        
        context = {
            'pk' : order.pk,
            'items' : order.items,
            'price' : order.price,
        }

        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwarfs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()
            
        return redirect('payment-confirmation')


class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')
