from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Product, Category


class ProductAPITests(APITestCase):

    # Runs before every test method to set up a clean environment
    def setUp(self):
        # Create a dummy category
        self.category = Category.objects.create(
            name="Electronics", slug="electronics")

        # Create a dummy product
        self.product = Product.objects.create(
            category=self.category,
            name="Test Laptop",
            slug="test-laptop",
            price=1000.00,
            available=True
        )

        # Create an admin user to test permissions
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='password123'
        )

    # Test: Anyone (even unauthenticated) can list products
    def test_get_products(self):
        url = reverse('products-list')
        response = self.client.get(url)

        # Assert that the request was successful and returns exactly 1 product
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Test: Unauthenticated users cannot create a product (Permissions test)
    def test_create_product_unauthorized(self):
        url = reverse('products-list')
        data = {
            "category": self.category.id,
            "name": "New Phone",
            "slug": "new-phone",
            "price": 500.00,
            "available": True
        }

        # Send POST request without logging in
        response = self.client.post(url, data, format='json')

        # Assert that access is denied (401 Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test: Admin users can successfully create a product
    def test_create_product_authorized(self):
        url = reverse('products-list')
        data = {
            "category": self.category.id,
            "name": "New Phone",
            "slug": "new-phone",
            "price": 500.00,
            "available": True
        }

        # Authenticate as the admin user
        self.client.force_authenticate(user=self.admin_user)

        # Send POST request
        response = self.client.post(url, data, format='json')

        # Assert that the product was created (201 Created) and count increased to 2
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
