# -*- coding: utf-8 -*-
from collective.pivot.config import getFamilyProperties
from collective.pivot.utils import _
from collective.pivot.utils import add_family
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

PIVOT_FOLDER = "Pivot"


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "collective.pivot:install-base",
            "collective.pivot:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'collective.pivot.upgrades',
        ]

def post_install(context):
    """Post install script"""
    site = api.portal.get()
    if not site.get(PIVOT_FOLDER):
        folder = api.content.create(
            type="Folder",
            container=site,
            title=_(PIVOT_FOLDER, context=site),
        )
        add_default_categories(folder)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def add_default_categories(context):
    """Add Pivot categories"""
    add_family(
        context,
        getFamilyProperties().get("hosting").get("urn"),
        _("Hosting", context=context),
    )
    add_family(
        context,
        getFamilyProperties().get("leisure").get("urn"),
        _("Leisure / discovery", context=context),
    )
    add_family(
        context,
        getFamilyProperties().get("tourism_organizations").get("urn"),
        _("Tourism organizations", context=context),
    )
    add_family(
        context,
        getFamilyProperties().get("events").get("urn"),
        _("Events", context=context),
    )
    add_family(
        context,
        getFamilyProperties().get("terroir").get("urn"),
        _("Terroir", context=context),
    )
