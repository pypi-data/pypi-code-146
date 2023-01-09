from rest_framework.test import APIClient, APITestCase


class BaseAPIClient(APIClient):
    ACCEPT_HEADER = "application/json"


class BaseAPITestCase(APITestCase):
    client_class = BaseAPIClient  # type: ignore
