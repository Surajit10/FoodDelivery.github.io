"""deliver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from customer import views
from customer.views import Order, OrderConfirmation, OrderPayConfirmation, Menu, MenuSearch

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index, name='index'),
    path('restuarant/', include('restuarant.urls')),
    path('logout/', views.logoutUser, name="logout"),
    path("register/", views.Register, name="register"),
    path('login/', views.LoginPage, name='login'),
    path('contact/', views.contact, name='contact'),
    path('order/', Order.as_view(), name='order'),
    path('order-confirmation/<int:pk>',
         OrderConfirmation.as_view(), name="order-confirmation"),
    path('payment-confirmation/', OrderConfirmation.as_view(),
         name='payment-submitted'),
    path('menu/', Menu.as_view(), name='menu'),
    path('menu/search/', MenuSearch.as_view(), name='menu-search'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
