from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
# Create your views here.
from customer.models import OrderModel
class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        #get the today's date
        today = datetime.today()
        orders = OrderModel.objects.filter(created_on__year=today.year, created_on__month=today.month, created_on__day=today.day)

        #loop though the orders and add the price value
        total_revenue = 0
        for order in orders:
            total_revenue += order.price

        context = {
            'orders' : orders,
            'total_revenue' : total_revenue,
            'toal_amount' : len(orders)

        }

        #pass total no. of orders and total revenue into template
        return render(request, 'restaurant_dash/dashboard.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='Staff').exists()
