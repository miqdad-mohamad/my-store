from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'store/index.html')


def products(request):
    return render(request, 'store/products.html')


def cart(request):
    return render(request, 'store/cart.html')


def checkout(request):
    return render(request, 'store/checkout.html')


def orders(request):
    return render(request, 'store/orders.html')


def login(request):
    return render(request, 'store/login.html')


def register(request):
    return render(request, 'store/register.html')

