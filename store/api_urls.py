from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .api_views import ProductViewSet, CategoryViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'orders', OrderViewSet, basename='orders')


urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]