from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime, timedelta
from customer.models import OrderModel
# Create your views here.


class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):

        orders = OrderModel.objects.filter(
            created_on__gte=datetime.now() - timedelta(days=1))

        print(orders)

        # loop through the orders and add the price value, check if order is not shipped
        c = 0
        unshipped_orders = []
        total_revenue = 0
        for order in orders:
            c = 1
            total_revenue += order.price
            if not order.is_shipped:
                unshipped_orders.append(order)

        print(c)

        # pass total number of orders and total revenue into template
        context = {
            'orders': unshipped_orders,
            'total_revenue': total_revenue,
            'total_orders': len(orders)
        }

        return render(request, 'restuarant/dashboard.html', context)

    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        order.is_shipped = True
        order.save()

        context = {
            'order': order
        }

        return render(request, 'restuarant/dashboard.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='staff').exists()


class OrderDetails(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order': order
        }

        return render(request, 'restuarant/order-details.html', context)

    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        order.is_shipped = True
        order.save()

        context = {
            'order': order
        }

        return render(request, 'restuarant/order-details.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='staff').exists()
