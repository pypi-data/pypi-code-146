# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.pivot.contents.family.endpoint import PivotEndpoint
from collective.pivot.contents.family.endpoint import PivotEndpointGet
from collective.pivot.testing import COLLECTIVE_PIVOT_INTEGRATION_TESTING  # noqa: E501
from collective.pivot.utils import add_family
from plone.app.testing import login
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility

import json
import os
import requests_mock
import unittest


class TestPivotEndpoint(unittest.TestCase):

    layer = COLLECTIVE_PIVOT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        login(self.portal, "test")
        self.request = self.portal.REQUEST
        with open(
            os.path.join(
                os.path.dirname(__file__),
                "resources/pivot_family_hosting_raw_mock.json",
            ),
        ) as json_file:
            self.json_pivot_family_hosting_raw_mock = json.load(json_file)
        with open(
            os.path.join(
                os.path.dirname(__file__),
                "resources/pivot_family_hosting_render_mock.json",
            ),
        ) as json_file:
            self.json_pivot_family_hosting_render_mock = json.load(json_file)

        self.Family = add_family(self.portal, u"urn:fam:1", u"Hosting")

    def test_vocabulary_keys(self):
        name = "collective.pivot.vocabularies.Families"
        factory = getUtility(IVocabularyFactory, name)
        vocabulary = factory(self.portal)
        keys = vocabulary.by_value.keys()
        self.assertIn("urn:fam:1", keys)
        self.assertIn("urn:fam:2", keys)
        self.assertIn("urn:fam:3", keys)
        self.assertIn("urn:fam:5", keys)
        self.assertIn("urn:fam:6", keys)

    def test_call(self):
        with requests_mock.Mocker() as m:
            m.get(
                "https://pivotweb.tourismewallonie.be/PivotWeb-3.1/query/OTH-A0-003P-2PWS;content=1;pretty=true;fmt=json;param=cp:5530",
                text=json.dumps(self.json_pivot_family_hosting_raw_mock),
            )
            endpoint = PivotEndpoint(self.Family, self.request)
            endpoint()

    def test_getResult(self):
        with requests_mock.Mocker() as m:
            m.get(
                "https://pivotweb.tourismewallonie.be/PivotWeb-3.1/query/OTH-A0-003P-2PWS;content=1;pretty=true;fmt=json;param=cp:5530",
                text=json.dumps(self.json_pivot_family_hosting_raw_mock),
            )
            endpoint = PivotEndpoint(self.Family, self.request)
            result = endpoint.getResult()
            self.assertDictEqual(result, self.json_pivot_family_hosting_raw_mock)

    def test_zip_codes(self):
        login(self.portal, "test")
        endpoint = PivotEndpoint(self.Family, self.request)
        self.assertEqual(endpoint.zip_codes, [u"5530"])
        self.Family.zip_codes = [u"5000", u"7000"]
        self.assertEqual(endpoint.zip_codes, [u"5000", u"7000"])

    def test_treatResult(self):
        self.maxDiff = None
        endpoint = PivotEndpoint(self.portal, self.request)
        result = endpoint.treatResult(self.json_pivot_family_hosting_raw_mock)
        self.assertDictEqual(result, self.json_pivot_family_hosting_render_mock)

    # def test_render(self):
    #     with PivotEndpoint(self.Family, self.request) as endpoint:
    #         service = PivotEndpointGet()
    #         service.render()
