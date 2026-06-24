from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'photo', 'available', 'created', 'updated']
        read_only_fields = ['id', 'created', 'updated']
