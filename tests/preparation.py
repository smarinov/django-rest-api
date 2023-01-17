from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from api.models import Category, Product


class ProductPrepTests(APITestCase):
    def setUp(self):
        self.first_user_data = {
            'username': 'first_test',
            'password': 'test123456',
            'password2': 'test123456',
            'email': 'first_test@mail.com',
            'first_name': 'test_first',
            'last_name': 'test_first'
        }

        self.second_user_data = {
            'username': 'second_test',
            'password': 'test123456',
            'password2': 'test123456',
            'email': 'second_test@mail.com',
            'first_name': 'test_second',
            'last_name': 'test_second'
        }

        self.product_data = {
            'brand': 'test_brand',
            'model': 'test_model',
            'description': 'test_description',
            'category': 1
        }

        self.category_data = {
            'category_name': 'test_category'
        }

        self.register_url = reverse('auth_register')
        self.obtain_token_url = reverse('token_obtain_pair')
        self.products_url = reverse('products-list-create')

    def create_first_user(self):
        user = User.objects.create_user(username=self.first_user_data['username'],
                                        email=self.first_user_data['email'],
                                        password=self.first_user_data['password'])
        return user

    def create_second_user(self):
        user = User.objects.create_user(username=self.second_user_data['username'],
                                        email=self.second_user_data['email'],
                                        password=self.second_user_data['password'])
        return user

    def authorize(self, user_data):
        token = self.client.post(self.obtain_token_url, user_data, format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        return token

    @staticmethod
    def create_category():
        category = Category(category_name='test_category')
        category.save()
        return category

    def create_product(self):
        category = self.create_category()
        product = Product(brand='SomeBrand', model='SomeModel', description='SomeDescription', category=category, seller_id=1)
        product.save()
        return product