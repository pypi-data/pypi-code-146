import requests_mock
from django.db import transaction
from djangoldp_account.models import LDPUser
from rest_framework.test import APITestCase, APIClient, APITransactionTestCase
import json
from pkg_resources import resource_string

from ..models import AnnotationTarget, Annotation, NeedleActivity

from ..models.needle_activity import ACTIVITY_TYPE_FIRST_ANNOTATION_WITH_CONNECTIONS, \
    ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS, ACTIVITY_TYPE_NEW_USER


class TestAnnotationTargetAdd(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def buildUser(self, username):
        user = LDPUser(email=username + '@test.startinblox.com', first_name='Test', last_name='Mactest',
                       username=username,
                       password='glass onion')
        user.save()
        return user

    def buildAnnotationTarget(self, target):
        target = AnnotationTarget(target=target)
        target.save()
        return target

    def test_annotation_create(self):
        user1 = self.buildUser('user1')
        self.client.force_authenticate(user1)

        target1 = self.buildAnnotationTarget('target1')
        response = self.client.post(
            "/users/user1/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target1)
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(1, Annotation.objects.count())

    def test_annotation_create_multiple_different_target(self):
        user1 = self.buildUser('user1')
        self.client.force_authenticate(user1)

        target1 = self.buildAnnotationTarget('target1')
        self.client.post(
            "/users/user1/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target1)
        )

        target2 = self.buildAnnotationTarget('target1')
        response = self.client.post(
            "/users/user1/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target2)
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(2, Annotation.objects.count())

    def test_annotation_create_multiple_same_target(self):
        user1 = self.buildUser('user1')
        self.client.force_authenticate(user1)

        target1 = self.buildAnnotationTarget('target1')
        self.client.post(
            "/users/user1/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target1)
        )
        response = self.client.post(
            "/users/user1/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target1)
        )
        self.assertEqual(response.status_code, 400)
        response_decoded = json.loads(response.content)
        self.assertEqual(response_decoded['Attention'], ['Vous avez déjà cette ressource dans votre fil.'])
        self.assertEqual(1, Annotation.objects.count())

    def test_annotation_create_multiple_same_target_different_user(self):
        user1 = self.buildUser('user1')
        user2 = self.buildUser('user2')
        target1 = self.buildAnnotationTarget('target1')

        self.client.force_authenticate(user1)
        self.client.post(
            "/users/user1/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target1)
        )

        self.client.force_authenticate(user2)
        response = self.client.post(
            "/users/user2/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target1)
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(2, Annotation.objects.count())

    def _create_annotation_create(self, target):
        return json.dumps({
            "@context": {"@vocab": "http://happy-dev.fr/owl/#",
                         "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                         "rdfs": "http://www.w3.org/2000/01/rdf-schema#", "ldp": "http://www.w3.org/ns/ldp#",
                         "foaf": "http://xmlns.com/foaf/0.1/", "name": "rdfs:label",
                         "acl": "http://www.w3.org/ns/auth/acl#", "permissions": "acl:accessControl",
                         "mode": "acl:mode", "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#", "lat": "geo:lat",
                         "lng": "geo:long", "entrepreneurProfile": "http://happy-dev.fr/owl/#entrepreneur_profile",
                         "mentorProfile": "http://happy-dev.fr/owl/#mentor_profile", "account": "hd:account",
                         "messageSet": "http://happy-dev.fr/owl/#message_set",
                         "author": "http://happy-dev.fr/owl/#author_user",
                         "title": "http://happy-dev.fr/owl/#title"},
            "target": {
                "@id": target.urlid
            }
        })
