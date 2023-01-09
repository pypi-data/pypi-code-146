# -*- coding: utf-8 -*-

from collective.pivot import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class IPivotSettings(Interface):
    # https://pivotweb.tourismewallonie.be/PivotWeb-3.1/
    ws_url = schema.TextLine(
        title=_(u"Webservice url"),
        default=u"https://pivotweb.tourismewallonie.be/PivotWeb-3.1/",
        required=True,
    )
    ws_key = schema.TextLine(title=_(u"Webservice (header) key"), required=True)
    zip_codes = schema.List(
        title=_(u"Zip codes"),
        value_type=schema.TextLine(title=_(u"Zip code")),
        required=True,
    )


class PivotControlPanelForm(RegistryEditForm):
    schema = IPivotSettings
    label = _(u"Pivot Settings")


PivotControlPanelView = layout.wrap_form(PivotControlPanelForm, ControlPanelFormWrapper)
