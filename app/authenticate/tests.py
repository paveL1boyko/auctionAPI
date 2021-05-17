from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from authenticate.models import CustomUser
from authenticate.serializer import UserSerializer


class RegistrationAPIViewTest(APITestCase):
    client = APIClient()

    def test_create_new_user(self):
        response = self.client.post(reverse('authenticate:registration'),
                                    {'username': 'admin', 'password': '12345678'},
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data.get('token'))
        self.assertIsNotNone(response.data.get('username'))


class LoginAPIViewAPIViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = CustomUser.objects.create_user(password='test', username='admin')

    def test_create_new_user(self):
        response = self.client.post(reverse('authenticate:token'),
                                    {'username': 'admin', 'password': 'test'},
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('token', None))


class UserRetrieveAPIViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = CustomUser.objects.create_user(password='test', username='admin', balance=10000,
                                                   email='test@gmail.com', last_name='adminovich', first_name='admin')

    def test_create_new_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.token)
        response = self.client.get(reverse('authenticate:user_data'), format='json')
        serializer = UserSerializer(CustomUser.objects.get(pk=self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)
