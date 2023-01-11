"""Tests for browser/reports.py.

Most report related things are in fact tested in `students`.

Here we only test the bits that are not covered otherwise.
"""
import shutil
import tempfile
from zope.component.hooks import clearSite
from zope.testbrowser.testing import Browser
from waeup.kofa.app import University
from waeup.kofa.testing import (
    FunctionalLayer, FunctionalTestCase, expensive_actions,
    )


class TestReportsContainerCreate(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(TestReportsContainerCreate, self).setUp()
        # Setup a sample site for each test
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']
        self.browser = Browser()
        self.browser.handleErrors = True

    def tearDown(self):
        super(TestReportsContainerCreate, self).tearDown()
        clearSite()
        shutil.rmtree(self.dc_root)

    def test_block_when_system_load_is_high(self):
        # under high system load we do not generate new reports
        assert self.app['reports'] is not None  # a reports container exists
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        with expensive_actions() as utils:
            utils.expensive_actions_allowed = lambda: False
            self.browser.open('http://localhost/app/reports/@@create')
        # we get a warning message about system load
        self.assertTrue(
            'high system load' in self.browser.contents)
        # we are not redirected to some generator, but back to overview
        self.assertEqual(
            self.browser.url, 'http://localhost/app/reports')

    def test_no_block_when_system_load_low(self):
        # under low system load we can pick a generator
        assert self.app['reports'] is not None  # a reports container exists
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        with expensive_actions() as utils:
            utils.expensive_actions_allowed = lambda: True
            self.browser.open('http://localhost/app/reports/@@create')
        # we do not get a warning message about system load
        self.assertTrue(
            'high system load' not in self.browser.contents)
        # we stay on the page
        self.assertEqual(
            self.browser.url, 'http://localhost/app/reports/@@create')
