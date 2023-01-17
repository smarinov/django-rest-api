from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from api.models import Product
from tests.preparation import ProductPrepTests


class ListCreateProductsViewTest(ProductPrepTests):
    def test_get_all_products(self):
        response = self.client.get(self.products_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_create_product_when_authenticated(self):
        self.create_first_user()
        self.authorize(self.first_user_data)
        self.create_category()
        response = self.client.post(self.products_url, self.product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_create_product_when_unauthenticated(self):
        self.create_category()
        response = self.client.post(self.products_url, self.product_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RetrieveUpdateDestroyProductViewTest(ProductPrepTests):
    def test_can_get_product_detail_when_authenticated(self):
        self.create_first_user()
        self.authorize(self.first_user_data)
        self.create_product()
        response = self.client.get(reverse('product-details', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_get_product_detail_when_unauthenticated(self):
        self.create_first_user()
        self.create_product()
        response = self.client.get(reverse('product-details', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_update_product_detail_when_user_is_not_owner(self):
        self.create_first_user()
        self.create_product()
        self.create_second_user()
        self.authorize(self.second_user_data)
        update_data = {'brand': 'updated brand'}
        response = self.client.patch(reverse('product-details', args=[1]), update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')

    def test_can_update_product_detail_when_user_is_owner(self):
        self.create_first_user()
        self.authorize(self.first_user_data)
        self.create_product()
        update_data = {'brand': 'updated brand'}
        response = self.client.patch(reverse('product-details', args=[1]), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['brand'], 'updated brand')

    def test_cannot_delete_product_when_user_is_not_owner(self):
        self.create_first_user()
        self.create_product()
        self.create_second_user()
        self.authorize(self.second_user_data)
        response = self.client.delete(reverse('product-details', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')

    def test_can_delete_product_when_user_is_owner(self):
        self.create_first_user()
        self.authorize(self.first_user_data)
        self.create_product()
        products = Product.objects.all()
        response = self.client.delete(reverse('product-details', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(products.count(), 0)
        self.assertFalse(products.count())
