from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, Order, OrderItem, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    products = Product.objects.filter(available=True)[:8]
    categories = Category.objects.all()
    return render(request, 'store/index.html', {
        'products': products,
        'categories': categories,
    })


def products(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, 'store/products.html', {
        'products': products,
        'categories': categories,
        'search_query': search_query,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1
    request.session['cart'] = cart
    product = get_object_or_404(Product, id=product_id)
    messages.success(request, f"{product.name} has been added to your cart.")
    return redirect(request.META.get('HTTP_REFERER', 'index'))


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
    request.session['cart'] = cart
    return redirect('cart')


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append(
            {'product': product, 'quantity': quantity, 'subtotal': subtotal})

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('fullname'),
            phone=request.POST.get('phone'),
            secondary_phone=request.POST.get('secondary_phone', ''),
            city=request.POST.get('city'),
            area=request.POST.get('area'),
            street=request.POST.get('street'),
            building=request.POST.get('building'),
            notes=request.POST.get('notes', ''),
            payment_method=request.POST.get(
                'payment_method', 'Cash on Delivery'),
            total=total,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['product'].price,
                quantity=item['quantity'],
            )

        request.session['cart'] = {}
        return redirect('order_success', order_id=order.id)

    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user)
    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'profile': user_profile
    })


@login_required
def orders(request):
    user_orders = Order.objects.filter(
        user=request.user).order_by('-created_at')
    return render(request, 'store/orders.html', {'user_orders': user_orders})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_success.html', {'order': order})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                UserProfile.objects.get_or_create(user=user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('index')


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user)

    if request.method == 'POST':
        user_profile.full_name = request.POST.get('full_name')
        user_profile.phone = request.POST.get('phone')
        user_profile.city = request.POST.get('city')
        user_profile.area = request.POST.get('area')
        user_profile.street = request.POST.get('street')
        user_profile.building = request.POST.get('building')
        user_profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'store/profile.html', {'profile': user_profile})
