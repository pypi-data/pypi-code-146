"""Models for plugins."""
import json

from cms.models.pluginmodel import CMSPlugin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


def validate_json(value: str) -> None:
    """Validate format JSON."""
    try:
        json.loads(value)
    except json.decoder.JSONDecodeError as err:
        raise ValidationError(err)


class MapPlugin(CMSPlugin):
    """Map plugin with markers."""

    map_latitude = models.FloatField(verbose_name=_('Map Longitude'), default=49.64)
    map_longitude = models.FloatField(verbose_name=_('Map Latitude'), default=15.2)
    map_zoom = models.IntegerField(verbose_name=_('Map Zoom'), default=7)
    map_width = models.CharField(
        max_length=255, verbose_name=_('Map width'), null=True, blank=True,
        help_text=_("For example 100%"))
    map_height = models.CharField(
        max_length=255, verbose_name=_('Map height'), null=True, blank=True,
        help_text=_("For example 400px"))
    controls = models.BooleanField(verbose_name=_("Map controls"), default=True,
                                   help_text=_("Display map controls - zoom, map slider."))
    no_zoom = models.BooleanField(verbose_name=_("No zoom"), default=False,
                                  help_text=_("Disable scrolling zoom by mouse wheel."))
    clusterer = models.BooleanField(verbose_name=_("Clusterer"), default=True,
                                    help_text=_("Enable Clusterer for display cluster of markers."))

    def __str__(self) -> str:
        if self.plugin_type:
            response = f'{_("Map")} [{self.pk}] {_("at")} "{self.placeholder.page.get_absolute_url()}"'
        else:
            response = f'{_("Map")} [{self.pk}]'
        return response


class MarkerPlugin(CMSPlugin):
    """Marker plugin in the Map."""

    # Position
    address = models.CharField(max_length=255, verbose_name=_('Address'), null=True, blank=True,
                               help_text=_("Street and number, city."))
    latitude = models.CharField(max_length=255, verbose_name=_('Latitude'), help_text=_("Geographical latitude."))
    longitude = models.CharField(max_length=255, verbose_name=_('Longitude'), help_text=_("Geographical longitude."))
    title = models.CharField(max_length=255, verbose_name=_('Title'), null=True, blank=True,
                             help_text=_("Name of marker."))
    # Icon
    img_path = models.CharField(max_length=255, verbose_name=_('Icon'), null=True, blank=True,
                                help_text=_("URL to the icon image or simply one of [red, yellow, blue]."))
    img_styles = models.CharField(
        max_length=255, verbose_name=_('Image styles'), null=True, blank=True, validators=[validate_json],
        help_text=_(
            'Icon styles in JSON. Example: '
            '{"position": "absolute", "left": 0, "top": "2px", "textAlign": "center", "width": "22px", '
            '"color": "white", "fontWeight": "bold"}'
        )
    )
    img_text = models.CharField(max_length=50, verbose_name=_('Icon text'), null=True, blank=True,
                                help_text=_("Icon text."))
    # Card
    card_width = models.IntegerField(verbose_name=_('Card width'), null=True, blank=True)
    card_heigth = models.IntegerField(verbose_name=_('Card heigth'), null=True, blank=True)
    card_header = models.CharField(max_length=255, verbose_name=_('Card header'), null=True, blank=True)
    card_body = models.TextField(verbose_name=_('Card nody'), null=True, blank=True)
    card_footer = models.CharField(max_length=255, verbose_name=_('Card footer'), null=True, blank=True)

    def __str__(self) -> str:
        return self.address if self.address else str(self.pk)


class ConnectorPlugin(CMSPlugin):
    """Connector plugin to connect address and card data with the map."""

    address = models.CharField(max_length=255, verbose_name=_('Address'),
                               help_text=_("Element name for Street and number, city."))
    latitude = models.CharField(max_length=255, verbose_name=_('Latitude'), null=True, blank=True,
                                help_text=_("Element name for geographical latitude."))
    longitude = models.CharField(max_length=255, verbose_name=_('Longitude'), null=True, blank=True,
                                 help_text=_("Element name for geographical longitude."))
    map = models.ForeignKey(MapPlugin, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255, verbose_name=_('Icon title'), null=True, blank=True,
                             help_text=_("Element name for icon title."))
    card_header = models.CharField(max_length=255, verbose_name=_('Card header'), null=True, blank=True,
                                   help_text=_("Element name for Card header."))
    card_body = models.CharField(max_length=255, verbose_name=_('Card body'), null=True, blank=True,
                                 help_text=_("Element names for Card body."))
    card_footer = models.CharField(max_length=255, verbose_name=_('Card footer'), null=True, blank=True,
                                   help_text=_("Element name for Card footer."))

    def __str__(self) -> str:
        return self.address if self.address else str(self.pk)
