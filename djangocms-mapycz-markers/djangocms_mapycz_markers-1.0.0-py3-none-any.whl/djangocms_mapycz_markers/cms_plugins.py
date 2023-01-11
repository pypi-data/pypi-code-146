"""Mapy.cz Markers CMS plugins."""

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from .models import ConnectorPlugin, MapPlugin, MarkerPlugin


@plugin_pool.register_plugin
class MapCMSPlugin(CMSPluginBase):
    """Markers CMS plugin."""

    model = MapPlugin
    render_template = 'djangocms_mapycz_markers/map.html'
    name = _('Mapy.cz Markers')
    module = _('Mapy.cz')
    allow_children = True
    child_classes = ['MarkerCMSPlugin']


@plugin_pool.register_plugin
class MarkerCMSPlugin(CMSPluginBase):
    """Marker Item CMS plugin."""

    model = MarkerPlugin
    render_template = 'djangocms_mapycz_markers/marker.html'
    change_form_template = "djangocms_mapycz_markers/marker_admin_form.html"
    name = _('Marker')
    module = _('Mapy.cz')
    parent_classes = ['MapCMSPlugin']


@plugin_pool.register_plugin
class ConnectorCMSPlugin(CMSPluginBase):
    """Suggest Address CMS plugin."""

    model = ConnectorPlugin
    render_template = 'djangocms_mapycz_markers/connector.html'
    name = _('Connect address with the map')
    module = _('Mapy.cz')
