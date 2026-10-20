from rest_framework import viewsets, filters
from .models import Product, Category, Order
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer
from .permissions import IsOwnerOrReadOnly 
from rest_framework.permissions import IsAuthenticated

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('category')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Order.objects.all().select_related('user').prefetch_related('items__product')
        
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)