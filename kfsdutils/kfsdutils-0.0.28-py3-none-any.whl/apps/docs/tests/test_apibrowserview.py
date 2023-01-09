from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone


class APIBrowserViewTests(APITestCase):
    def setUp(self):
        self.__apiBrowserViewUrl = reverse("schema-browser")
        return super().setUp()

    def test_get_apidoc(self):
        apiBrowserResponse = self.client.get(self.__apiBrowserViewUrl, format='json')
        self.assertEqual(apiBrowserResponse.status_code, status.HTTP_200_OK)
