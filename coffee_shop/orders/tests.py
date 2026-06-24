from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product
from .models import Order, OrderItem

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.product1 = Product.objects.create(name="Espresso", description="Fuerte", price=2.50)
        self.product2 = Product.objects.create(name="Croissant", description="Delicioso", price=1.80)

    def test_order_creation_and_auto_now_add(self):
        order = Order.objects.create(user=self.user)
        self.assertIsNotNone(order.created_at)

    def test_order_cascade_delete(self):
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(order=order, product=self.product1, quantity=2, price=self.product1.price)
        
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

        # Delete user
        self.user.delete()

        # Verify order and items are deleted
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderItem.objects.count(), 0)

    def test_order_total_value_calculation(self):
        from decimal import Decimal
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(order=order, product=self.product1, quantity=2, price=2.50) # total = 5.00
        OrderItem.objects.create(order=order, product=self.product2, quantity=3, price=1.80) # total = 5.40

        self.assertEqual(order.total_value, Decimal('10.40'))


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class OrderAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="apipassword123")
        self.staff_user = User.objects.create_superuser(username="adminuser", password="adminpassword123")
        self.product1 = Product.objects.create(name="Latte", description="Rico", price=3.00)

    def test_list_products(self):
        url = reverse('product_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore
        self.assertEqual(len(response.data), 1)  # type: ignore

    def test_create_product_by_anonymous_fails(self):
        url = reverse('product_api')
        data = {"name": "Espresso", "description": "Fuerte", "price": "2.50"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # type: ignore

    def test_create_product_by_staff_succeeds(self):
        self.client.force_authenticate(user=self.staff_user)  # type: ignore
        url = reverse('product_api')
        data = {"name": "Espresso", "description": "Fuerte", "price": "2.50"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore
        self.assertEqual(Product.objects.filter(name="Espresso").count(), 1)

    def test_create_order_authenticated_succeeds(self):
        self.client.force_authenticate(user=self.user)  # type: ignore
        url = reverse('order_api')
        data = {
            "items": [
                {"product": self.product1.id, "quantity": 2}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

