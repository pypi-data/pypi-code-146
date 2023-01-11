"""Actions for DjangoCMS plugin Mapy.cz Markers.

Usage:
    site/settings.py:
        MAPYCZ_ADD_MARKER_TO_MAP = callack (see function add_plugin_marker_into_map)

    site/admin.py:
        from django.contrib.admin import site
        from djangocms_mapycz_markers.actions import mapycz_add_marker
        site.add_action(mapycz_add_marker)
"""

import re
from typing import List, Optional, Set, Tuple, Union, cast

from aldryn_forms.admin import FormSubmissionAdmin
from aldryn_forms.models import FormPlugin, FormSubmission
from cms.api import add_plugin
from cms.models.pagemodel import Page
from cms.models.placeholdermodel import Placeholder
from django.conf import settings
from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .cms_plugins import ConnectorCMSPlugin, MarkerCMSPlugin
from .models import ConnectorPlugin, MapPlugin, MarkerPlugin

UsedCoordinates = Tuple[int, int, int, str]  # latitude, longitude, map_id, language


def add_plugin_marker_into_map(
    request: HttpRequest,
    placeholder: Placeholder,
    language: str,
    target: MapPlugin,
    latitude: Union[str, int],
    longitude: Union[str, int],
    address: str,
    title: Optional[str],
    card_header: Optional[str],
    card_body: Optional[str],
    card_footer: Optional[str]
) -> Optional[MarkerPlugin]:
    """Add plugin Marker into the map."""
    return add_plugin(
        placeholder,
        MarkerCMSPlugin,
        language,
        target=target,
        latitude=latitude,
        longitude=longitude,
        address=address,
        title=title,
        card_header=card_header,
        card_body=card_body,
        card_footer=card_footer
    )


def apply_form(
    request: HttpRequest,
    submission: FormSubmission,
    connector: ConnectorPlugin,
    saved_markers: List[UsedCoordinates]
) -> Tuple[Optional[MarkerPlugin], Optional[UsedCoordinates]]:
    """Apply form data into the map."""
    if connector.latitude is None or connector.longitude is None:
        return None, None  # Geographical coordinate names missing.
    post = {field.name: field.value for field in submission.get_form_data()}
    latitude, longitude = post.get(connector.latitude), post.get(connector.longitude)
    if latitude is None or longitude is None:
        return None, None  # Geographical coordinate values missing.
    address = post.get(connector.address)
    if MarkerPlugin.objects.filter(
        latitude=latitude, longitude=longitude, parent_id=connector.map.pk, language=submission.language
    ).exists():
        if (latitude, longitude, connector.map.pk, submission.language) not in saved_markers:
            messages.info(request, _('Marker "%s" already exists.') % address)
        coordinates = (cast(int, latitude), cast(int, longitude), cast(int, connector.map.pk), submission.language)
        return None, coordinates  # This Marker already exists.

    title = post.get(connector.title) if connector.title else None
    card_header = post.get(connector.card_header) if connector.card_header else None
    card_footer = post.get(connector.card_footer) if connector.card_footer else None
    card_body = None
    if connector.card_body:
        body = []
        for name in re.split('[,; ]+', connector.card_body):
            text = post.get(name)
            if text is not None:
                body.append(text)
        if body:
            card_body = ' '.join(body)

    if hasattr(settings, 'MAPYCZ_ADD_MARKER_TO_MAP'):
        add_marker = import_string(settings.MAPYCZ_ADD_MARKER_TO_MAP)
    else:
        add_marker = add_plugin_marker_into_map
    marker = add_marker(
        request, connector.map.placeholder, submission.language, connector.map, latitude, longitude, address, title,
        card_header, card_body, card_footer
    )
    if marker:
        messages.success(request, _('Marker[%(pk)d] created "%(address)s".') % {'pk': marker.pk, 'address': address})
        coordinates = (marker.latitude, marker.longitude, connector.map.pk, marker.language)
    return marker, coordinates


def mapycz_add_marker(modeladmin: ModelAdmin, request: HttpRequest, queryset: QuerySet) -> None:
    """Add Markers into Mapy.cz."""
    if not isinstance(modeladmin, FormSubmissionAdmin):
        messages.info(request, _("Command cannot be used on this data type."))
        return  # This is not required instance.

    saved_markers: List[UsedCoordinates] = []
    pages: Set[Tuple[Page, str]] = set()

    for submitted_form in queryset.all():
        for form in FormPlugin.objects.filter(name=submitted_form.name):
            plugin: Optional[ConnectorCMSPlugin] = form.get_children().filter(plugin_type='ConnectorCMSPlugin').first()
            if plugin is None:
                continue  # Form does not have the ConnectorPlugin.
            connector = plugin.get_plugin_instance()[0]  # (instance, class)
            if connector.map is None:
                continue  # MapPlugin is not defined.
            marker, coordinates = apply_form(request, submitted_form, connector, saved_markers)
            if marker:
                pages.add((connector.map.placeholder.page, submitted_form.language))
            if coordinates:
                saved_markers.append(coordinates)

    for page, language in pages:
        page.publish(language)
        messages.success(request, mark_safe(_('Page <a href="%(href)s" target="_top">%(href)s</a> published.') % {
            'href': page.get_absolute_url()}))


mapycz_add_marker.allowed_permissions = ('change', )  # type: ignore[attr-defined]
mapycz_add_marker.short_description = _("Add Markers into Mapy.cz")  # type: ignore[attr-defined]
