# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.pivot.testing import COLLECTIVE_PIVOT_INTEGRATION_TESTING  # noqa: E501

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest


class TestVocabularies(unittest.TestCase):

    layer = COLLECTIVE_PIVOT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]

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
