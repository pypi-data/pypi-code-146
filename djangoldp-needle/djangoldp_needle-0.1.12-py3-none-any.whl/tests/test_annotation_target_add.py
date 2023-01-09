import requests_mock
from django.db import transaction
from djangoldp_account.models import LDPUser
from rest_framework.test import APITestCase, APIClient, APITransactionTestCase
import json
from pkg_resources import resource_string

from ..models import AnnotationTarget

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

        param_list = [
            (
                'data/parsing/base_valid.20221103.html',
                'http://test.startinblox.com',
                'Title',
                'http://test.startinblox.com/img.jpg',
                None
            ),
            (
                'data/parsing/lemonde.20221103.html',
                'https://www.lemonde.fr/international/article/2022/11/03/au-bresil-les-equipes-de-lula-et-de-jair-bolsonaro-entament-la-transition_6148375_3210.html',
                'Au Brésil, la transition entre Lula et Bolsonaro a commencé et de nombreux barrages routiers ont été levés',
                'https://img.lemde.fr/2022/11/03/0/47/3406/2271/1440/960/60/0/3f999da_fw1-brazil-election-1103-11.jpg',
                None
            ),
            (
                'data/parsing/theconversation.20221103.html',
                'http://theconversation.com/cyberattaques-des-hopitaux-que-veulent-les-hackers-192407',
                'Cyberattaques des hôpitaux : que veulent les hackers ?',
                'https://images.theconversation.com/files/492581/original/file-20221031-16-io8s7w.jpg?ixlib=rb-1.1.0&rect=0%2C684%2C7992%2C3996&q=45&auto=format&w=1356&h=668&fit=crop',
                None
            )
        ]
        for site_extract, expected_target, expected_title, expected_img, expected_publication in param_list:
            with transaction.atomic():
                # Creates a new savepoint. Returns the savepoint ID (sid).
                sid = transaction.savepoint()

                self._mock_response_content_from_file(m, site_extract)
                response = self.client.post(
                    "/annotationtargets/",
                    content_type='application/ld+json',
                    data=self._create_annotation_parse_request()
                )
                self.assertEqual(response.status_code, 201)

                response_decoded = json.loads(response.content)
                self.assertEqual(response_decoded['@id'], 'http://happy-dev.fr/annotationtargets/1/')
                self.assertEqual(response_decoded['target'], expected_target)
                self.assertEqual(response_decoded['title'], expected_title)
                self.assertEqual(response_decoded['image'], expected_img)
                self.assertEqual(response_decoded['publication_date'], expected_publication)

                # Rolls back the transaction to savepoint sid.
                transaction.savepoint_rollback(sid)

    def test_annotation_multiple_request_same_target(self, m):
        user1 = self.buildUser('user1')
        self.client.force_authenticate(user1)

        self.assertEqual(0, AnnotationTarget.objects.count())

        self._mock_response_content_from_file(m, 'data/parsing/base_valid.20221103.html')
        response = self.client.post(
            "/annotationtargets/",
            content_type='application/ld+json',
            data=self._create_annotation_parse_request()
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(1, AnnotationTarget.objects.count())

        response = self.client.post(
            "/annotationtargets/",
            content_type='application/ld+json',
            data=self._create_annotation_parse_request()
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, AnnotationTarget.objects.count())

    def test_annotation_invalid(self, m):
        user1 = self.buildUser('user1')
        self.client.force_authenticate(user1)

        self._mock_response_content_from_file(m, 'data/parsing/base_invalid.20221103.html')
        response = self.client.post(
            "/annotationtargets/",
            content_type='application/ld+json',
            data=self._create_annotation_parse_request()
        )
        self.assertEqual(response.status_code, 400)
        response_decoded = json.loads(response.content)
        self.assertEqual(response_decoded['URL'], ['Le lien est invalide'])
        self.assertEqual(0, AnnotationTarget.objects.count())

    def test_annotation_404(self, m):
        user1 = self.buildUser('user1')
        self.client.force_authenticate(user1)

        m.register_uri(
            'GET',
            'http://test.startinblox.com',
            text='',
            status_code=404
        )
        response = self.client.post(
            "/annotationtargets/",
            content_type='application/ld+json',
            data=self._create_annotation_parse_request()
        )
        self.assertEqual(response.status_code, 400)
        response_decoded = json.loads(response.content)
        self.assertEqual(response_decoded['URL'], ['Le lien est invalide'])
        self.assertEqual(0, AnnotationTarget.objects.count())


    def _create_annotation_parse_request(self):
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
                    "target": "http://test.startinblox.com"
                })

    def _mock_response_content_from_file(self, m, file):
        file_content = resource_string(__name__, file).decode("utf-8")
        m.register_uri(
            'GET',
            'http://test.startinblox.com',
            text=file_content,
        )