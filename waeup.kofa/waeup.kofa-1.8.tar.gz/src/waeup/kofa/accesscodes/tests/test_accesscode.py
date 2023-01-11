## $Id: test_accesscode.py 12944 2015-05-15 04:57:20Z henrik $
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
import doctest
import os
import re
import shutil
import tempfile
import unittest

from datetime import datetime
from hurry.workflow.interfaces import InvalidTransitionError, IWorkflowState
from zope.component import getUtility
from zope.component.hooks import setSite, clearSite
from zope.interface.verify import verifyObject, verifyClass
from zope.testing import renormalizing
from waeup.kofa.app import University
from waeup.kofa.interfaces import IObjectHistory, IKofaPluggable, IKofaUtils
from waeup.kofa.testing import (
    FunctionalLayer, FunctionalTestCase, setUp, tearDown, getRootFolder)
from waeup.kofa.accesscodes.accesscode import (
    AccessCodeBatch, get_access_code, invalidate_accesscode, AccessCode,
    disable_accesscode, reenable_accesscode, fire_transition,
    AccessCodeBatchContainer, AccessCodePlugin)
from waeup.kofa.accesscodes.interfaces import (
    IAccessCode, IAccessCodeBatch,  IAccessCodeBatchContainer,)
from waeup.kofa.accesscodes.workflow import INITIALIZED, USED, DISABLED


optionflags = (
    doctest.REPORT_NDIFF + doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)

class AccessCodeHelpersTests(FunctionalTestCase):
    # Tests for helpers like get_access_code, disable_accesscode, ...

    layer = FunctionalLayer

    def setUp(self):
        super(AccessCodeHelpersTests, self).setUp()

        # Prepopulate ZODB
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']

        # Create batch
        batch = AccessCodeBatch('now', 'manfred', 'APP', 6.6, 0)
        self.app['accesscodes'].addBatch(batch)

        # Fill batch with accesscodes
        batch.addAccessCode(0, '11111111')
        batch.addAccessCode(1, '22222222')
        batch.addAccessCode(2, '33333333')
        self.ac1 = batch.getAccessCode('APP-1-11111111')
        self.ac2 = batch.getAccessCode('APP-1-22222222')
        self.ac3 = batch.getAccessCode('APP-1-33333333')

        setSite(self.app)
        return

    def tearDown(self):
        shutil.rmtree(self.dc_root)
        super(AccessCodeHelpersTests, self).tearDown()
        return

    def test_get_access_code(self):
        ac = get_access_code('APP-1-11111111')
        assert ac is self.ac1

    def test_get_access_code_not_string(self):
        ac = get_access_code(object())
        assert ac is None

    def test_get_access_code_no_proper_pin(self):
        ac = get_access_code('APP-without_pin')
        assert ac is None

    def test_get_access_code_invalid_batch_num(self):
        ac = get_access_code('APP-invalid-11111111')
        assert ac is None

    def test_get_access_code_invalid_pin(self):
        ac = get_access_code('APP-1-notexistent')
        assert ac is None

    def test_invalidate_accesscode(self):
        assert self.ac1.state != USED
        result = invalidate_accesscode('APP-1-11111111')
        assert self.ac1.state == USED
        assert result is True

    def test_disable_accesscode_unused(self):
        # we can disable initialized acs
        assert self.ac1.state != USED
        disable_accesscode('APP-1-11111111')
        assert self.ac1.state == DISABLED

    def test_disable_accesscode_used(self):
        # we can disable already used acs
        assert self.ac1.state != DISABLED
        invalidate_accesscode('APP-1-11111111')
        disable_accesscode('APP-1-11111111')
        assert self.ac1.state == DISABLED

    def test_reenable_accesscode(self):
        # we can reenable disabled acs
        disable_accesscode('APP-1-11111111')
        result = reenable_accesscode('APP-1-11111111')
        assert result is True
        assert self.ac1.state != USED

    def test_fire_transition(self):
        # we can fire transitions generally
        fire_transition('APP-1-11111111', 'use')
        assert IWorkflowState(self.ac1).getState() is USED

    def test_fire_transition_toward(self):
        # the `toward` keyword is respected
        fire_transition('APP-1-11111111', DISABLED, toward=True)
        assert IWorkflowState(self.ac1).getState() is DISABLED

    def test_fire_transition_no_site(self):
        # when no site is available, we will get a TypeError
        clearSite()
        self.assertRaises(
            KeyError,
            fire_transition, 'APP-1-11111111', 'use')

    def test_fire_transition_broken_ac_id(self):
        # if we get an invalid access code id (of wrong format) we get
        # ValueErrors
        self.assertRaises(
            ValueError,
            fire_transition, '11111111', 'use')

    def test_fire_transition_invalid_batch_id(self):
        # if we request a non-existent batch_id, we'll get a KeyError
        self.assertRaises(
            KeyError,
            fire_transition, 'FOO-1-11111111', 'use')

    def test_fire_transition_invalid_ac(self):
        # if we request a non-exitent access-code, we'll get a KeyError
        self.assertRaises(
            KeyError,
            fire_transition, 'APP-1-NONSENSE', 'use')

    def test_fire_transition_undef_trans_id(self):
        # asking for undefined transition id means a KeyError
        self.assertRaises(
            KeyError,
            fire_transition, 'APP-1-11111111', 'nonsense')

    def test_fire_transition_invalid_transition(self):
        # asking for a forbidden transition will result in
        # InvalidTransitionError
        self.assertRaises(
            InvalidTransitionError,
            fire_transition, 'APP-1-11111111', 'init') # already initialized

    def test_fire_transition_comment(self):
        # when we request a comment, it will also appear in history
        fire_transition('APP-1-11111111', 'use', comment='Hi there!')
        history = IObjectHistory(self.ac1)
        msgs = history.messages
        assert 'Hi there!' in msgs[-1]

    def test_fire_transition_no_comment(self):
        # without comment, the history should be without trailing garbage
        fire_transition('APP-1-11111111', 'use')
        history = IObjectHistory(self.ac1)
        msgs = history.messages
        assert msgs[-1].endswith('used by system')

class AccessCodeTests(FunctionalTestCase):
    # Tests for AccessCode class

    layer = FunctionalLayer

    def setUp(self):
        super(AccessCodeTests, self).setUp()

        # Prepopulate ZODB
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']

        # Create batch
        batch = AccessCodeBatch('now', 'manfred', 'APP', 6.6, 0)
        self.app['accesscodes'].addBatch(batch)

        # Fill batch with accesscodes
        batch.addAccessCode(0, '11111111')

        self.ac1 = batch.getAccessCode('APP-1-11111111')
        setSite(self.app)
        return

    def tearDown(self):
        shutil.rmtree(self.dc_root)
        super(AccessCodeTests, self).tearDown()
        return

    def test_iface(self):
        # AccessCodes fullfill their iface promises.
        ac = AccessCode('1', '12345678')
        assert verifyObject(IAccessCode, ac)
        assert verifyClass(IAccessCode, AccessCode)

    def test_history(self):
        # Access codes have a history.
        match = re.match(
            '^....-..-.. ..:..:.. .+ - initialized by system',
            self.ac1.history)
        assert match is not None

    def test_cost(self):
        # The cost of an access code will be stored by handle_batch_added
        # right after the batch has been added to the ZODB. Thus after
        # creation of the batch, cost is still 0.0
        cost = self.ac1.cost
        assert cost == 0.0

class AccessCodeBatchTests(FunctionalTestCase):
    # Tests for AccessCodeBatch class

    layer = FunctionalLayer

    def setUp(self):
        super(AccessCodeBatchTests, self).setUp()

        # Prepopulate ZODB
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']

        batch = AccessCodeBatch(    # create batch with zero entries
            datetime.utcnow(), 'testuser', 'FOO', 9.99, 0)
        self.app['accesscodes'].addBatch(batch)

        self.ac1 = AccessCode(0, '11111111')
        self.ac1.cost = 2345.0
        self.ac2 = AccessCode(1, '22222222')
        self.ac3 = AccessCode(2, '33333333')
        batch['FOO-1-11111111'] = self.ac1
        batch['FOO-1-22222222'] = self.ac2
        batch['FOO-1-33333333'] = self.ac3
        self.batch = batch

        setSite(self.app)
        return

    def tearDown(self):
        shutil.rmtree(self.dc_root)
        super(AccessCodeBatchTests, self).tearDown()
        return

    def test_iface(self):
        batch = AccessCodeBatch(
            datetime(2009, 12, 23), 'Fred','APP', 12.12, 3, num=10)
        assert verifyObject(IAccessCodeBatch, batch)
        assert verifyClass(IAccessCodeBatch, AccessCodeBatch)

    def test_container_contents(self):
        assert 'SFE-0' in self.app['accesscodes']
        assert 'HOS-0' in self.app['accesscodes']
        assert 'CLR-0' in self.app['accesscodes']

    def test_csv_export(self):
        # Make sure CSV export of accesscodes works
        batch = self.batch
        invalidate_accesscode('FOO-1-11111111', comment='comment with "quotes"')
        disable_accesscode('FOO-1-33333333')
        basename = batch.archive()
        result_path = os.path.join(batch._getStoragePath(), basename)
        expected = '''
"prefix","serial","ac","state","history","cost","owner"
"FOO","9.99","1","0"
"FOO","0","FOO-1-11111111","used","<YYYY-MM-DD hh:mm:ss> UTC - ...","2345.0",""
"FOO","1","FOO-1-22222222","initialized","<YYYY-MM-DD hh:mm:ss> UTC - ...",""
"FOO","2","FOO-1-33333333","disabled","<YYYY-MM-DD hh:mm:ss> UTC - ...",""
'''[1:]
        contents = open(result_path, 'rb').read()
        self.assertMatches(expected, contents)

class AccessCodeBatchContainerTests(FunctionalTestCase):
    # Tests for AccessCodeContainer class

    layer = FunctionalLayer

    def setUp(self):
        super(AccessCodeBatchContainerTests, self).setUp()

        # Prepopulate ZODB
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']

        self.import_sample1_src = os.path.join(
            os.path.dirname(__file__), 'sample_import.csv')

        batch = AccessCodeBatch(    # create batch with zero entries
            datetime.now(), 'testuser', 'BAR', 9.99, 0)
        self.app['accesscodes'].addBatch(batch)

        self.ac1 = AccessCode(0, '11111111')
        self.ac2 = AccessCode(1, '22222222')
        self.ac3 = AccessCode(2, '33333333')
        batch['BAR-1-11111111'] = self.ac1
        batch['BAR-1-22222222'] = self.ac2
        batch['BAR-1-33333333'] = self.ac3
        self.batch = batch

        setSite(self.app)
        return

    def tearDown(self):
        shutil.rmtree(self.dc_root)
        super(AccessCodeBatchContainerTests, self).tearDown()
        return

    def test_iface(self):
        accesscodes = AccessCodeBatchContainer()
        assert verifyObject(IAccessCodeBatchContainer, accesscodes)
        assert verifyClass(IAccessCodeBatchContainer, AccessCodeBatchContainer)

    def test_existing_batches(self):
        self.assertEqual(sorted(self.app['accesscodes'].keys()),
            [u'BAR-1', u'CLR-0', u'HOS-0', u'SFE-0', u'TSC-0'])

    def test_csv_import(self):
        # Make sure we can reimport sample data from local sample_import.csv
        batchcontainer = self.app['accesscodes']
        shutil.copyfile(        # Copy sample to import dir
            os.path.join(os.path.dirname(__file__), 'sample_import.csv'),
            os.path.join(batchcontainer._getStoragePath(), 'sample_import.csv')
            )
        batchcontainer.reimport('sample_import.csv')
        batch = batchcontainer.get(u'FOO-1', None)
        self.assertTrue(batch is not None)
        keys = [x for x in batch.keys()]
        self.assertEqual(
            keys,
            [u'FOO-1-11111111', u'FOO-1-22222222', u'FOO-1-33333333'])
        # Also cost has been stored correctly
        self.assertEqual(batch['FOO-1-11111111'].cost,1000.0)

    def test_getAccessCode(self):
        batchcontainer = self.app['accesscodes']
        result1 = batchcontainer.getAccessCode('BAR-1-11111111')
        result2 = batchcontainer.getAccessCode('BAR-1-not-existent')
        assert isinstance(result1, AccessCode)
        assert result2 is None

    def test_disableAccessCode(self):
        batchcontainer = self.app['accesscodes']
        result1 = batchcontainer.disable('BAR-1-11111111')
        result2 = batchcontainer.disable('BAR-1-not-existent')
        assert self.ac1.state is DISABLED
        assert result2 is None

    def test_enableAccessCode(self):
        batchcontainer = self.app['accesscodes']
        batchcontainer.disable('BAR-1-11111111')
        result1 = batchcontainer.enable('BAR-1-11111111')
        result2 = batchcontainer.enable('BAR-1-not-existent')
        assert self.ac1.state is INITIALIZED
        assert result2 is None

class AccessCodePluginTests(FunctionalTestCase):
    # Tests for AccessCodeContainer class

    layer = FunctionalLayer

    def setUp(self):
        super(AccessCodePluginTests, self).setUp()

        # Prepopulate ZODB
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']

    def tearDown(self):
        shutil.rmtree(self.dc_root)
        super(AccessCodePluginTests, self).tearDown()
        return

    def test_iface(self):
        plugin = AccessCodePlugin()
        assert verifyObject(IKofaPluggable, plugin)
        assert verifyClass(IKofaPluggable, AccessCodePlugin)

    def test_update_w_ac_container(self):
        # The plugin changes nothing, if there is already a container
        plugin = AccessCodePlugin()
        site = self.app
        logger = site.logger
        accesscodes = site['accesscodes']
        plugin.update(site, 'app', logger)
        assert site['accesscodes'] is accesscodes

    def test_update_wo_ac_container(self):
        # The plugin creates a new accesscodes container if it is missing
        plugin = AccessCodePlugin()
        site = self.app
        logger = site.logger
        del site['accesscodes']
        plugin.update(site, 'app', logger)
        assert 'accesscodes' in site

checker = renormalizing.RENormalizing([
        (re.compile('[\d]{10}'), '<10-DIGITS>'),
        ])


def test_suite():
    suite = unittest.TestSuite()
    for testcase in [
        AccessCodeHelpersTests,
        AccessCodeTests,
        AccessCodeBatchTests,
        AccessCodeBatchContainerTests,
        AccessCodePluginTests,
        ]:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testcase))
    for filename in [
        '../doctests/accesscode_browser.txt'
        ]:
        path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), filename)
        test = doctest.DocFileSuite(
            path,
            module_relative=False,
            setUp=setUp, tearDown=tearDown,
            globs = dict(getRootFolder = getRootFolder),
            optionflags = doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE,
            checker = checker,
            )
        test.layer = FunctionalLayer
        suite.addTest(test)
    return suite
