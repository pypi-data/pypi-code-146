from cms.api import add_plugin, create_page
from cms.models import Placeholder
from cms.test_utils.testcases import CMSTestCase
from django.core.exceptions import ValidationError
from django.test import TestCase

from djangocms_mapycz_markers.cms_plugins import MapCMSPlugin
from djangocms_mapycz_markers.models import ConnectorPlugin, MapPlugin, MarkerPlugin


class MapPluginTest(CMSTestCase):

    def test_pk(self):
        model = MapPlugin(pk=42)
        self.assertEqual(str(model), "Map [42]")

    def test_pk_plugin(self):
        page = create_page('home', 'page.html', 'en-us')
        placeholder = Placeholder.objects.create(slot='test', page=page)
        marker = add_plugin(placeholder, MapCMSPlugin, 'en')
        self.assertEqual(str(marker), f'Map [{marker.pk}] at "/home/"')


class MarkerPluginTest(TestCase):

    def test_pk(self):
        model = MarkerPlugin(pk=42)
        self.assertEqual(str(model), "42")

    def test_address(self):
        model = MarkerPlugin(address="The Address")
        self.assertEqual(str(model), "The Address")

    def test_empty_address(self):
        model = MarkerPlugin(pk=42, address="")
        self.assertEqual(str(model), "42")

    def test_img_styles(self):
        model = MarkerPlugin(pk=42, latitude=42, longitude=24, img_styles='{"test": "ok"}')
        model.clean_fields()
        self.assertEqual(str(model), "42")

    def test_invlaid_img_styles(self):
        model = MarkerPlugin(latitude=42, longitude=24, img_styles='{"test": "ok}')
        with self.assertRaisesMessage(ValidationError, 'Unterminated string starting at: line 1 column 10 (char 9)'):
            model.clean_fields()


class ConnectorPluginTest(TestCase):

    def test_pk(self):
        model = ConnectorPlugin(pk=42)
        self.assertEqual(str(model), "42")

    def test_address(self):
        model = ConnectorPlugin(address="The Address")
        self.assertEqual(str(model), "The Address")

    def test_empty_address(self):
        model = ConnectorPlugin(pk=42, address="")
        self.assertEqual(str(model), "42")
