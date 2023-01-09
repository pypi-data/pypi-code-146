import requests_mock
from django.db import transaction
from djangoldp_account.models import LDPUser
from rest_framework.test import APITestCase, APIClient, APITransactionTestCase
import json
from pkg_resources import resource_string

from ..models import NeedleActivity

@requests_mock.Mocker(real_http=True)
class TestAnnotationTargetAdd(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def buildUser(self, username):
        user = LDPUser(email=username + '@test.startinblox.com', first_name='Test', last_name='Mactest',
                       username=username,
                       password='glass onion')
        user.save()
        return user

    def test_annotation_parse_real_site(self, m):
        user1 = self.buildUser('user1')
        self.client.force_authenticate(user1)
        self.assertEqual(1, NeedleActivity.objects.count())
