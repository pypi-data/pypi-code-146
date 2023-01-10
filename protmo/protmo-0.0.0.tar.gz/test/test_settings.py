from unittest import TestCase
from protmo.settings_loader import SettingsContainer


class TestSettings(TestCase):

    def setUp(self):
        self.settings = SettingsContainer()

    def test_set_and_get(self):
        self.settings['a_key'] = 'a value'
        self.assertEqual('a value', self.settings['a_key'])
        self.assertEqual('a value', self.settings.a_key)

    def test_does_not_exist_via_key(self):
        with self.assertRaises(KeyError):
            self.settings['abc']

    def test_does_not_exist_via_attr(self):
        with self.assertRaises(AttributeError):
            self.settings.abc
