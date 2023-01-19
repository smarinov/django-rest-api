from rest_framework import serializers
from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.category_name')
    seller_name = serializers.ReadOnlyField(source='seller.username')

    class Meta:
        model = Product
        exclude = ['seller']


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'products']

