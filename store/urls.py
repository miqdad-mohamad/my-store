from django.urls import path
from . import views
from .api_views import UserProfileAPIView

urlpatterns = [
    path('', views.index, name='index'),
    path('products', views.products, name='products'),
    path('checkout', views.checkout, name='checkout'),
    path('orders', views.orders, name='orders'),
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('cart', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/',
         views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('logout/', views.logout_view, name='logout'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('order-success/<int:order_id>/',
         views.order_success, name='order_success'),

    path('profile/', views.profile, name='profile'),


]
