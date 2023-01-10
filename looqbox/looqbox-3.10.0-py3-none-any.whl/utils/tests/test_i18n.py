import unittest
from looqbox.utils.utils import *
from looqbox.utils.i18n.internationalization_manager import I18nManager


class TestI18n(unittest.TestCase):

    def setUp(self):
        self.vocabulary_test = {
            "pt-br": {"A": 1, "B": 1, "A-B": 1},
            "en-us": {"A": 2, "B": 2, "A-B": 2}
        }

        self.vocabulary_fail_test = {
            "pt-br": {"A": 1, "B": 1, "C": 1},
            "en-us": {"A": 2, "B": 2}
        }

    def test_i18n_creation(self):
        i18n_model = I18nManager()
        i18n_model.add_label(self.vocabulary_test)

        i18n_test = create_i18n_vocabulary(self.vocabulary_test)
        self.assertEqual(i18n_model, i18n_test)

    def test_I18nManager_inheritance(self):
        i18n_test = create_i18n_vocabulary(self.vocabulary_test)
        self.assertIsInstance(i18n_test, I18nManager)

    def test_i18n_keys_exception(self):
        self.assertRaises(Exception, I18nManager.add_label, self.vocabulary_fail_test)

    def test_i18n_property(self):
        i18n_model = I18nManager()
        i18n_model.language = "pt-br"
        i18n_model.add_label(self.vocabulary_test)

        self.assertEqual(i18n_model.A, 1)
        self.assertEqual(i18n_model.B, 1)

    def test_i18n_getitem(self):
        i18n_model = I18nManager()
        i18n_model.language = "pt-br"
        i18n_model.add_label(self.vocabulary_test)

        self.assertEqual(i18n_model["A-B"], 1)
