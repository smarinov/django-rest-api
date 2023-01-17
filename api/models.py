from django.contrib import auth
from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    @property
    def all_products(self):
        return [f'{product.brand} {product.model}' for product in self.products.all()]

    def __str__(self):
        return self.category_name


class Product(models.Model):
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    description = models.TextField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    seller = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='seller_products')

    def __str__(self):
        return f'{self.brand} {self.model}'

