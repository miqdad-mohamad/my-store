from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products', views.products, name='products'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('orders', views.orders, name='orders'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),

]
