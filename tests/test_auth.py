from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthViewTest(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'test',
            'password': 'test123456',
            'password2': 'test123456',
            'email': 'test@mail.com',
            'first_name': 'test_first',
            'last_name': 'test_last'
        }

        self.register_url = reverse('auth_register')
        self.obtain_token_url = reverse('token_obtain_pair')
        self.refresh_token_url = reverse('token_refresh')

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_register_user_without_data(self):
        response = self.client.post(self.register_url, None, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_register_when_user_already_exists(self):
        response_initial_register = self.client.post(self.register_url, self.user_data, format='json')
        response_second_attempt = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response_initial_register.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_second_attempt.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_obtain_tokens_when_registered(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.obtain_token_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['access'])
        self.assertIsNotNone(response.data['refresh'])

    def test_cannot_obtain_tokens_when_not_registered(self):
        response = self.client.post(self.obtain_token_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials')

    def test_cannot_obtain_tokens_when_credentials_dont_match(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.obtain_token_url, {'username': 'test', 'password': '1234'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_obtain_refreshed_access_token(self):
        self.client.post(self.register_url, self.user_data, format='json')
        tokens = self.client.post(self.obtain_token_url, self.user_data, format='json')
        refresh_token = tokens.data['refresh']
        access_token_new = self.client.post(self.refresh_token_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(access_token_new.status_code, status.HTTP_200_OK)
