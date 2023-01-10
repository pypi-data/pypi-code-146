import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
import mock


UserModel = get_user_model()


class APIUserAPITestCase(APITestCase):

    @pytest.mark.django_db
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='test', email='test@...', password='top_secret')
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


class TestAPI(APIUserAPITestCase):

    @pytest.mark.django_db
    @mock.patch('enough.common.bind.delegate_dns')
    @mock.patch('enough.api.permissions.has_permission')
    def test_delegate_test_dns(self, has_permission, delegate_dns):
        url = reverse('delegate-test-dns')
        delegate_dns.return_value = [{"changed": False}, {"changed": True}, {"changed": False}]
        has_permission.return_value = True
        data = {
            "name": "gyztqojxhe3tinjrbi",
            "ip": "1.2.3.4",
        }

        response = self.client.post(url, data, format='json')

        assert has_permission.called
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()[0], {"changed": False})

    @pytest.mark.django_db
    @mock.patch('enough.common.bind.delegate_dns')
    def test_delegate_dns(self, delegate_dns):
        url = reverse('delegate-dns')
        delegate_dns.return_value = [{"changed": False}, {"changed": True}, {"changed": False}]
        data = {
            "name": "gyztqojxhe3tinjrbi",
            "ip": "1.2.3.4",
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()[0], {"changed": False})

    @pytest.mark.django_db
    def test_ping(self):
        url = reverse('ping')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'pong')
