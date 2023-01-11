from cms.api import add_plugin
from cms.middleware.page import get_page
from cms.models import Placeholder
from cms.plugin_rendering import ContentRenderer
from cms.test_utils.testcases import CMSTestCase
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, override_settings
from django.test.client import RequestFactory

from djangocms_mapycz_markers.cms_plugins import ConnectorCMSPlugin, MapCMSPlugin, MarkerCMSPlugin


class MapCMSPluginTests(TestCase):

    def test_plugin_context(self):
        placeholder = Placeholder.objects.create(slot='test')
        mapcz = add_plugin(placeholder, MapCMSPlugin, 'en')
        plugin_instance = mapcz.get_plugin_class_instance()
        context = plugin_instance.render({}, mapcz, None)
        self.assertEqual(context, {'instance': mapcz, 'placeholder': None})

    def test_plugin_html(self):
        placeholder = Placeholder.objects.create(slot='test')
        mapcz = add_plugin(placeholder, MapCMSPlugin, 'en')
        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(mapcz, {})
        self.assertHTMLEqual(html, f"""
            <div id="mapycz-markers-{mapcz.pk}"
                data-map_width=""
                data-map_height=""
                data-map_latitude="49.64"
                data-map_longitude="15.2"
                data-map_zoom="7"
                data-controls="True"
                data-no_zoom="False"
                data-clusterer="True"
                >
            </div>""")

    def test_plugin_html_with_params(self):
        placeholder = Placeholder.objects.create(slot='test')
        mapcz = add_plugin(
            placeholder,
            MapCMSPlugin,
            'en',
            map_latitude=49.42,
            map_longitude=15.8,
            map_zoom=8,
            map_width="100%",
            map_height="400px",
            controls=False,
            no_zoom=True,
            clusterer=False
        )
        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(mapcz, {})
        self.assertHTMLEqual(html, f"""
            <div id="mapycz-markers-{mapcz.pk}"
                data-map_width="100%"
                data-map_height="400px"
                data-map_latitude="49.42"
                data-map_longitude="15.8"
                data-map_zoom="8"
                data-controls="False"
                data-no_zoom="True"
                data-clusterer="False"
                style="width: 100%; height: 400px;"
            ></div>""")


@override_settings(ROOT_URLCONF='tests.urls')
class MarkerCMSPluginTest(CMSTestCase):

    def setUp(self):
        self.placeholder = Placeholder.objects.create(slot='test')
        self.map = add_plugin(self.placeholder, MapCMSPlugin, 'en')

    def test_plugin_context(self):
        marker = add_plugin(self.placeholder, MarkerCMSPlugin, 'en')
        plugin_instance = marker.get_plugin_class_instance()
        context = plugin_instance.render({}, marker, None)
        self.assertEqual(context, {'instance': marker, 'placeholder': None})

    def test_plugin_html(self):
        marker = add_plugin(
            self.placeholder, MarkerCMSPlugin, 'en',
            target=self.map,
            address='Milešovská 1609/8, Praha 3 - Vinohrady, Česko',
            latitude=50.07946089634304,
            longitude=14.451615666673554
        )
        self.map.child_plugin_instances = [marker]
        request = RequestFactory().get("/")
        request.user = AnonymousUser()
        request.current_page = get_page(request)
        renderer = ContentRenderer(request=request)
        html = renderer.render_plugin(self.map, {"request": request})
        self.assertHTMLEqual(html, f"""
            <div id="mapycz-markers-{self.map.pk}"
                data-map_width=""
                data-map_height=""
                data-map_latitude="49.64"
                data-map_longitude="15.2"
                data-map_zoom="7"
                data-controls="True"
                data-no_zoom="False"
                data-clusterer="True"
            >
                <marker
                    data-longitude="14.451615666673554"
                    data-latitude="50.07946089634304"
                    data-title=""
                    data-address="Milešovská 1609/8, Praha 3 - Vinohrady, Česko"
                    data-card_width=""
                    data-card_heigth=""
                    data-card_header=""
                    data-card_body=""
                    data-card_footer=""
                    data-img_path=""
                    data-img_styles=""
                    data-img_text=""
                ></marker>
            </div>""")

    def _create_map_and_marker(self):
        marker = add_plugin(
            self.placeholder, MarkerCMSPlugin, 'en',
            target=self.map,
            address='Milešovská 1609/8, Praha 3 - Vinohrady, Česko',
            latitude=50.07946089634304,
            longitude=14.451615666673554,
            title="The title",
            card_width=600,
            card_heigth=400,
            card_header="Card header",
            card_body="Card <i>body</i>",
            card_footer="Card footer",
            img_path="image.png",
            img_styles='{"style": "ok"}',
            img_text="Image text"
        )
        self.map.child_plugin_instances = [marker]

    def _create_request(self):
        request = RequestFactory().get("/")
        request.user = AnonymousUser()
        request.current_page = get_page(request)
        return request

    def test_plugin_html_with_params(self):
        self._create_map_and_marker()
        request = self._create_request()
        renderer = ContentRenderer(request=request)
        html = renderer.render_plugin(self.map, {"request": request})
        self.assertHTMLEqual(html, f"""
            <div id="mapycz-markers-{self.map.pk}"
                data-map_width=""
                data-map_height=""
                data-map_latitude="49.64"
                data-map_longitude="15.2"
                data-map_zoom="7"
                data-controls="True"
                data-no_zoom="False"
                data-clusterer="True"
            >
                <marker
                    data-longitude="14.451615666673554"
                    data-latitude="50.07946089634304"
                    data-title="The title"
                    data-address="Milešovská 1609/8, Praha 3 - Vinohrady, Česko"
                    data-card_width="600"
                    data-card_heigth="400"
                    data-card_header="Card header"
                    data-card_body="Card &lt;i&gt;body&lt;/i&gt;"
                    data-card_footer="Card footer"
                    data-img_path="image.png"
                    data-img_styles="{{&quot;style&quot;: &quot;ok&quot;}}"
                    data-img_text="Image text"
                ></marker>
            </div>""")


class ConnectorCMSPluginTest(TestCase):

    def test_plugin_context(self):
        placeholder = Placeholder.objects.create(slot='test')
        connector = add_plugin(placeholder, ConnectorCMSPlugin, 'en')
        plugin_instance = connector.get_plugin_class_instance()
        context = plugin_instance.render({}, connector, None)
        self.assertEqual(context, {'instance': connector, 'placeholder': None})

    def test_plugin_html(self):
        placeholder = Placeholder.objects.create(slot='test')
        connector = add_plugin(placeholder, ConnectorCMSPlugin, 'en')
        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(connector, {})
        self.assertHTMLEqual(html, """
        <mapycz-suggest-address
            data-address=""
            data-latitude=""
            data-longitude=""
        ></mapycz-suggest-address>""")

    def test_plugin_html_with_params(self):
        placeholder = Placeholder.objects.create(slot='test')
        connector = add_plugin(
            placeholder,
            ConnectorCMSPlugin,
            'en',
            address='Street, City, ZIP',
            latitude=42,
            longitude=24
        )
        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(connector, {})
        self.assertHTMLEqual(html, """
        <mapycz-suggest-address
            data-address="Street, City, ZIP"
            data-latitude="42"
            data-longitude="24"
        ></mapycz-suggest-address>""")

    def test_plugin_html_with_all_params(self):
        placeholder = Placeholder.objects.create(slot='test')
        mapplugin = add_plugin(placeholder, MapCMSPlugin, 'en')
        connector = add_plugin(
            placeholder,
            ConnectorCMSPlugin,
            'en',
            address='Street, City, ZIP',
            latitude=42,
            longitude=24,
            map=mapplugin,
            title="field_title",
            card_header="field_header",
            card_body="field_date, field_description",
            card_footer="card_footer"
        )
        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(connector, {})
        self.assertHTMLEqual(html, """
        <mapycz-suggest-address
            data-address="Street, City, ZIP"
            data-latitude="42"
            data-longitude="24"
        ></mapycz-suggest-address>""")
