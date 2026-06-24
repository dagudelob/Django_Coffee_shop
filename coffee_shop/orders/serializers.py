from rest_framework import serializers
from django.db import transaction
from .models import Order, OrderItem
from products.models import Product
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_details', 'quantity', 'price', 'total_price']
        read_only_fields = ['id', 'price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'username', 'created_at', 'total_value', 'tax_amount', 'total_with_tax', 'items']
        read_only_fields = ['id', 'created_at', 'total_value', 'tax_amount', 'total_with_tax']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        with transaction.atomic():  # type: ignore
            order = Order.objects.create(user=user)
            for item_data in items_data:
                product = item_data['product']
                quantity = item_data['quantity']
                # Determine the current price of the product
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
        return order
