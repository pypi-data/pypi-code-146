# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.pivot import HAS_PLONE_5_AND_MORE
from collective.pivot.testing import COLLECTIVE_PIVOT_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

if HAS_PLONE_5_AND_MORE:
    from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.pivot is properly installed."""

    layer = COLLECTIVE_PIVOT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if not HAS_PLONE_5_AND_MORE:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        else:
            self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if collective.pivot is installed."""
        if not HAS_PLONE_5_AND_MORE:
            self.assertTrue(self.installer.isProductInstalled("collective.pivot"))
        else:
            self.assertTrue(self.installer.is_product_installed("collective.pivot"))

    def test_browserlayer(self):
        """Test that ICollectivePivotLayer is registered."""
        from collective.pivot.interfaces import ICollectivePivotLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectivePivotLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_PIVOT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        if not HAS_PLONE_5_AND_MORE:
            self.installer = api.portal.get_tool("portal_quickinstaller")
            self.installer.uninstallProducts(["collective.pivot"])
        else:
            self.installer = get_installer(self.portal, self.layer["request"])
            self.installer.uninstall_product("collective.pivot")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.pivot is cleanly uninstalled."""
        if not HAS_PLONE_5_AND_MORE:
            self.assertFalse(self.installer.isProductInstalled("collective.pivot"))
        else:
            self.assertFalse(self.installer.is_product_installed("collective.pivot"))

    def test_browserlayer_removed(self):
        """Test that ICollectivePivotLayer is removed."""
        from collective.pivot.interfaces import ICollectivePivotLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectivePivotLayer, utils.registered_layers())
