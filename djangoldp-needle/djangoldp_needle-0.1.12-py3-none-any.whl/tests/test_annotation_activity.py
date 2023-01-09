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

    def test_annotation_activity_create_first_annotation_new_annotation_target_activity(
            self):
        print("test_annotation_activity_create_first_annotation_new_annotation_target_activity")
        user1 = self.buildUser('user1')
        target1 = self.buildAnnotationTarget('target1')

        self.client.force_authenticate(user1)
        self.client.post(
            "/users/user1/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target1)
        )
        result_needle_activity = \
            NeedleActivity.objects.filter(creator=user1,
                                          activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS)

        self.assertEqual(1, result_needle_activity.count())

    def test_annotation_activity_create_first_annotation_already_exist_annotation_target_activity(
            self):
        print("test_annotation_activity_create_first_annotation_already_exist_annotation_target_activity")
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
        result_needle_activity = \
            NeedleActivity.objects.filter(creator=user2,
                                          activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITH_CONNECTIONS)

        self.assertEqual(1, result_needle_activity.count())

    def test_annotation_activity_create_two_annotations_not_and_already_exists_annotation_target_activity(
            self):
        print("test_annotation_activity_create_two_annotations_not_and_already_exists_annotation_target_activity")
        user1 = self.buildUser('user1')
        user2 = self.buildUser('user2')
        target1 = self.buildAnnotationTarget('target1')
        target2 = self.buildAnnotationTarget('target2')

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
            data=self._create_annotation_create(target2)
        )

        result_needle_activity_without = \
            NeedleActivity.objects.filter(creator=user2,
                                          activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS)
        result_needle_activity_with = \
            NeedleActivity.objects.filter(creator=user2,
                                          activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITH_CONNECTIONS)

        self.assertEqual(1, result_needle_activity_without.count())
        self.assertEqual(0, result_needle_activity_with.count())
        self.client.force_authenticate(user2)
        response = self.client.post(
            "/users/user2/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target1)
        )

        self.assertEqual(1, result_needle_activity_without.count())
        self.assertEqual(1, result_needle_activity_with.count())

    def test_annotation_activity_create_two_annotations_already_and_not_exists_annotation_target_activity(
            self):
        print("test_annotation_activity_create_two_annotations_already_and_not_exists_annotation_target_activity")
        user1 = self.buildUser('user1')
        user2 = self.buildUser('user2')
        target1 = self.buildAnnotationTarget('target1')
        target2 = self.buildAnnotationTarget('target2')

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

        result_needle_activity_without = \
            NeedleActivity.objects.filter(creator=user2,
                                          activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS)
        result_needle_activity_with = \
            NeedleActivity.objects.filter(creator=user2,
                                          activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITH_CONNECTIONS)

        self.assertEqual(0, result_needle_activity_without.count())
        self.assertEqual(1, result_needle_activity_with.count())
        self.client.force_authenticate(user2)
        response = self.client.post(
            "/users/user2/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target2)
        )

        self.assertEqual(1, result_needle_activity_without.count())
        self.assertEqual(1, result_needle_activity_with.count())

    def test_annotation_activity_create_two_annotations_already_and_not_exists_annotation_target_activity_two_times(
            self):
        print(
            "test_annotation_activity_create_two_annotations_already_and_not_exists_annotation_target_activity_two_times")
        user1 = self.buildUser('user1')
        user2 = self.buildUser('user2')
        target1 = self.buildAnnotationTarget('target1')
        target2 = self.buildAnnotationTarget('target2')
        target3 = self.buildAnnotationTarget('target3')
        target4 = self.buildAnnotationTarget('target4')

        self.client.force_authenticate(user1)
        self.client.post(
            "/users/user1/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target1)
        )
        self.client.post(
            "/users/user1/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target3)
        )

        self.client.force_authenticate(user2)
        response = self.client.post(
            "/users/user2/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target1)
        )

        result_needle_activity_without = \
            NeedleActivity.objects.filter(creator=user2,
                                          activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS)
        result_needle_activity_with = \
            NeedleActivity.objects.filter(creator=user2,
                                          activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITH_CONNECTIONS)

        self.assertEqual(0, result_needle_activity_without.count())
        self.assertEqual(1, result_needle_activity_with.count())
        self.client.force_authenticate(user2)
        response = self.client.post(
            "/users/user2/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target2)
        )

        self.assertEqual(1, result_needle_activity_without.count())
        self.assertEqual(1, result_needle_activity_with.count())

        self.client.force_authenticate(user2)
        response = self.client.post(
            "/users/user2/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target3)
        )

        self.client.force_authenticate(user2)
        response = self.client.post(
            "/users/user2/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target4)
        )

        result_needle_activity_without = \
            NeedleActivity.objects.filter(creator=user2,
                                          activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS)
        result_needle_activity_with = \
            NeedleActivity.objects.filter(creator=user2,
                                          activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITH_CONNECTIONS)

        self.assertEqual(1, result_needle_activity_without.count())
        self.assertEqual(1, result_needle_activity_with.count())
