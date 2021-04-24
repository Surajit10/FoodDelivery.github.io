from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


from .models import Contact, MenuItem, Category, OrderModel
from django.contrib import messages

from .forms import CreateUserForm


@login_required(login_url="login")
def Index(request):
    context = {}
    return render(request, 'customer/index.html', context)


def Register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

        context = {'form': form}
        return render(request, 'customer/register.html', context)


def LoginPage(request):

    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username OR Password is incorrect')

        context = {}
        return render(request, 'customer/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def contact(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print(name, email, phone, message)
        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()

        

    return render(request, 'customer/contact.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        veg = MenuItem.objects.filter(
            category__name__contains='Veg')
        nonveg = MenuItem.objects.filter(category__name__contains='non')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')
        deserts = MenuItem.objects.filter(category__name__contains='Desert')
        # pass into context
        context = {
            'veg': veg,
            'nonveg': nonveg,
            'deserts':deserts,
            'drinks': drinks
            
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):

        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk=item)
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
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )
        order.items.add(*item_ids)

        # After everything is done send confimration email to the user

        body = ('Thank you for your order! Your order has been booked and will be delivered soon!'
                f'Your Total: {price}\n'
                'Thank you again for your order!'
                )

        send_mail(
            'Thank You For Your Order!',
            body,
            'exmaple@example.com',
            [email],
            fail_silently=False
        )
        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        print(request.body)


class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')


class Menu(View):

    def get(self, request, *args, **kwargs):

        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)
