## $Id: test_root.py 7811 2012-03-08 19:00:51Z uli $
##
## Copyright (C) 2011 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""
Test applicants root.
"""
import logging
import shutil
import tempfile
import unittest
from StringIO import StringIO
from zope.component.hooks import setSite, clearSite
from zope.interface.verify import verifyClass, verifyObject
from waeup.kofa.app import University
from waeup.kofa.applicants import (
    interfaces, Applicant, ApplicantsContainer,
    )
from waeup.kofa.applicants.root import (
    ApplicantsRoot, ApplicantsPlugin,
    )
from waeup.kofa.testing import (
    FunctionalLayer, FunctionalTestCase, remove_logger)


class FakeSite(dict):
    pass

class ApplicantsRootTestCase(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        remove_logger('waeup.kofa.app.applicants')
        super(ApplicantsRootTestCase, self).setUp()
        # Setup a sample site for each test
        # Prepopulate the ZODB...
        app = University()
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']
        setSite(self.app)
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)
        return

    def tearDown(self):
        super(ApplicantsRootTestCase, self).tearDown()
        shutil.rmtree(self.dc_root)
        clearSite()
        return

    def test_interfaces(self):
        # Make sure the correct interfaces are implemented.
        self.assertTrue(
            verifyClass(
                interfaces.IApplicantsRoot, ApplicantsRoot)
            )
        self.assertTrue(
            verifyObject(
                interfaces.IApplicantsRoot, ApplicantsRoot())
            )
        return

    def test_logger(self):
        # We can get a logger from root
        logger = self.app['applicants'].logger
        assert logger is not None
        assert logger.name == 'waeup.kofa.app.applicants'
        handlers = logger.handlers
        assert len(handlers) == 1
        filename = logger.handlers[0].baseFilename
        assert filename.endswith('applicants.log')
        assert filename.startswith(self.dc_root)

    def test_logger_multiple(self):
        # Make sure the logger is still working after 2nd call
        # First time we call it, it might be registered
        logger = self.app['applicants'].logger
        # At second call the already registered logger should be returned
        logger = self.app['applicants'].logger
        assert logger is not None
        assert logger.name == 'waeup.kofa.app.applicants'
        handlers = logger.handlers
        assert len(handlers) == 1
        filename = logger.handlers[0].baseFilename
        assert filename.endswith('applicants.log')
        assert filename.startswith(self.dc_root)

class ApplicantsRootPluginTestCase(unittest.TestCase):
    def create_logger(self):
        # create a logger suitable for local tests.
        test_logger = logging.getLogger('waeup.kofa.applicants.testlogger')
        log = StringIO()
        handler = logging.StreamHandler(log)
        handler.setLevel(logging.DEBUG)
        test_logger.addHandler(handler)
        test_logger.setLevel(logging.DEBUG)
        self.logger = test_logger
        self.log = log
        self.handler = handler
        return self.logger

    def remove_logger(self):
        del self.handler
        del self.logger
        del self.log
        pass

    def get_log(self):
        self.log.seek(0)
        return self.log.read()

    def setUp(self):
        self.create_logger()
        return

    def tearDown(self):
        self.remove_logger()
        return

    # Real tests start here...
    def test_pluginsetup(self):
        # Make sure we can add ApplicantsRoot to sites.
        site = FakeSite()
        plugin = ApplicantsPlugin()
        plugin.setup(site, 'blah', self.logger)
        self.assertTrue('applicants' in site.keys())
        log = self.get_log()
        self.assertTrue('Installed applicants root.' in log)
        return

    def test_update_new(self):
        # Run update on a site without applicants root.
        site = FakeSite()
        plugin = ApplicantsPlugin()
        plugin.update(site, 'blah', self.logger)
        self.assertTrue('applicants' in site.keys())
        log = self.get_log()
        self.assertTrue('Updating site at <Unnamed Site>' in log)
        self.assertTrue('Installed applicants root.' in log)
        return

    def test_update_outdated(self):
        # Run update on a site with outdated applicants root.
        site = FakeSite()
        root = object() # # This is not a proper applicants root
        site['applicants'] = root
        plugin = ApplicantsPlugin()
        plugin.update(site, 'blah', self.logger)
        self.assertTrue(site['applicants'] is not root)
        self.assertTrue(isinstance(site['applicants'], ApplicantsRoot))
        log = self.get_log()
        self.assertTrue('Outdated applicants folder detected' in log)
        self.assertTrue('Updating site at <Unnamed Site>' in log)
        self.assertTrue('Installed applicants root.' in log)
        return

    def test_update_uptodate(self):
        # Run update on a site with proper applicants root.
        site = FakeSite()
        root = ApplicantsRoot()
        site['applicants'] = root
        plugin = ApplicantsPlugin()
        plugin.update(site, 'blah', self.logger)
        self.assertTrue(site['applicants'] is root)
        log = self.get_log()
        self.assertTrue('Updating site at <Unnamed Site>' in log)
        self.assertTrue('Nothing to do' in log)
        return

    def test_update_log(self):
        # Check that sitename is used in log messages on updates.
        site = FakeSite()
        site.__name__ = 'my_site'
        plugin = ApplicantsPlugin()
        plugin.update(site, 'blah', self.logger)
        log = self.get_log()
        self.assertTrue('Updating site at my_site.' in log)
        return

def suite():
    suite = unittest.TestSuite()
    for testcase in [
            ApplicantsRootTestCase,
            ApplicantsRootPluginTestCase,
            ]:
        suite.addTests(unittest.makeSuite(testcase))
    return suite

test_suite = suite
