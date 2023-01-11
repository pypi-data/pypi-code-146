## $Id: test_batching.py 10448 2013-08-05 06:07:53Z henrik $
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
Tests for hostels and their UI components.
"""
import os
import shutil
import tempfile
import grok
import pytz
from datetime import datetime, timedelta
from zope.event import notify
from zope.interface.verify import verifyClass, verifyObject
from zope.component.hooks import setSite, clearSite
from zope.testbrowser.testing import Browser
from zope.security.interfaces import Unauthorized
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility
from waeup.kofa.app import University
from waeup.kofa.interfaces import IObjectHistory, IKofaPluggable, IKofaUtils
from waeup.kofa.testing import (
    FunctionalLayer, FunctionalTestCase, setUp, tearDown, getRootFolder)
from waeup.kofa.accesscodes.batching import (
    AccessCodeBatchProcessor, AccessCodeProcessor)


BATCH_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_batch_data.csv'),
    'rb').read()

BATCH_HEADER_FIELDS = BATCH_SAMPLE_DATA.split(
    '\n')[0].split(',')

AC_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_ac_data.csv'),
    'rb').read()

AC_HEADER_FIELDS = AC_SAMPLE_DATA.split(
    '\n')[0].split(',')

AC_SAMPLE_DATA_UPDATE = open(
    os.path.join(os.path.dirname(__file__), 'sample_ac_data_update.csv'),
    'rb').read()

AC_HEADER_FIELDS_UPDATE = AC_SAMPLE_DATA_UPDATE.split(
    '\n')[0].split(',')

class ACFullSetup(FunctionalTestCase):

    def setUp(self):
        super(ACFullSetup, self).setUp()

        # Setup a sample site for each test
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        # we add the site immediately after creation to the
        # ZODB. Catalogs and other local utilities are not setup
        # before that step.
        self.app = self.getRootFolder()['app']
        # Set site here. Some of the following setup code might need
        # to access grok.getSite() and should get our new app then
        setSite(app)

        # Put the prepopulated site into test ZODB and prepare test
        # browser
        self.browser = Browser()
        self.browser.handleErrors = False

        self.logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'accesscodes.log')
        self.workdir = tempfile.mkdtemp()

    def tearDown(self):
        super(ACFullSetup, self).tearDown()
        clearSite()
        shutil.rmtree(self.dc_root)
        shutil.rmtree(self.workdir)

class ACBatchProcessorTest(ACFullSetup):

    layer = FunctionalLayer

    def test_import(self):
        self.processor = AccessCodeBatchProcessor()
        self.csv_file = os.path.join(self.workdir, 'sample_batch_data.csv')
        open(self.csv_file, 'wb').write(BATCH_SAMPLE_DATA)
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, BATCH_HEADER_FIELDS)
        self.assertEqual(num_warns,0)
        self.assertEqual(len(self.app['accesscodes'].keys()), 8)
        self.assertEqual(self.app['accesscodes']['CLR-1'].num,1)
        logcontent = open(self.logfile).read()
        self.assertTrue(
            'system - AccessCodeBatch Processor - sample_batch_data - '
            'CLR-1 - updated: '
            'num=1, creator=system, used_num=1, '
            'entry_num=3, creation_date=2012-04-28 07:28:48.719026+00:00, '
            'prefix=CLR, cost=0.0, disabled_num=0'
            in logcontent)
        shutil.rmtree(os.path.dirname(fin_file))
        return

class ACProcessorTest(ACFullSetup):

    layer = FunctionalLayer

    def test_import_create(self):
        self.processor = AccessCodeBatchProcessor()
        self.csv_file = os.path.join(self.workdir, 'sample_batch_data.csv')
        open(self.csv_file, 'wb').write(BATCH_SAMPLE_DATA)
        num, num_warns, fin_file, fail_file =  self.processor.doImport(
            self.csv_file, BATCH_HEADER_FIELDS)
        shutil.rmtree(os.path.dirname(fin_file))

        self.processor = AccessCodeProcessor()
        self.csv_file = os.path.join(self.workdir, 'sample_ac_data.csv')
        open(self.csv_file, 'wb').write(AC_SAMPLE_DATA)
        num, num_warns, fin_file, fail_file =  self.processor.doImport(
            self.csv_file, AC_HEADER_FIELDS)
        self.assertEqual(num_warns,3)
        fail_file = open(fail_file).read()
        self.assertTrue(
            'HOS-1-0007044547,HOS,anything,state: not allowed' in fail_file)
        self.assertTrue(
            'HOS-1-555,HOS,anything,workflow: not allowed' in fail_file)
        self.assertTrue(
            'HOS-1-666,HOS,anything,transition: not allowed' in fail_file)
        self.assertEqual(
            self.app['accesscodes']['HOS-1']['HOS-1-98769876'].state, 'used')
        self.assertEqual(
            self.app['accesscodes']['HOS-1']['HOS-1-76254765'].state,
            'initialized')
        self.assertEqual(
            self.app['accesscodes']['CLR-1']['CLR-1-1625368961'].batch_serial,
            33)
        self.assertEqual(
            self.app['accesscodes']['CLR-1']['CLR-1-1625368961'].random_num,
            '1625368961')
        self.assertEqual(
            self.app['accesscodes']['CLR-1']['CLR-1-1625368961'].state, 'used')
        self.assertMatches(
            self.app['accesscodes']['CLR-1']['CLR-1-1625368961'].history,
            "<YYYY-MM-DD hh:mm:ss> UTC - initialized by system|"
            "|<YYYY-MM-DD hh:mm:ss> UTC - state 'used' set by system")
        self.assertMatches(
            self.app['accesscodes']['HOS-1']['HOS-1-98769876'].history,
            "<YYYY-MM-DD hh:mm:ss> UTC - initialized by system|"
            "|<YYYY-MM-DD hh:mm:ss> UTC - used by system")
        logcontent = open(self.logfile).read()
        self.assertTrue(
            'INFO - system - AccessCode Processor - sample_ac_data - '
            'CLR-1-1625368961 - updated: state=used, '
            'batch_serial=33, random_num=1625368961, '
            'cost=100.0, owner=K1000009'
            in logcontent)
        shutil.rmtree(os.path.dirname(fin_file))
        return

    def test_import_update(self):
        self.processor = AccessCodeBatchProcessor()
        self.csv_file = os.path.join(self.workdir, 'sample_batch_data.csv')
        open(self.csv_file, 'wb').write(BATCH_SAMPLE_DATA)
        num, num_warns, fin_file, fail_file =  self.processor.doImport(
            self.csv_file, BATCH_HEADER_FIELDS)
        shutil.rmtree(os.path.dirname(fin_file))

        self.processor = AccessCodeProcessor()
        self.csv_file = os.path.join(self.workdir, 'sample_ac_data.csv')
        open(self.csv_file, 'wb').write(AC_SAMPLE_DATA)
        num, num_warns, fin_file, fail_file =  self.processor.doImport(
            self.csv_file, AC_HEADER_FIELDS)
        shutil.rmtree(os.path.dirname(fin_file))

        self.assertEqual(self.app['accesscodes']['HOS-1'].used_num, 1)
        self.assertEqual(self.app['accesscodes']['HOS-1'].disabled_num, 0)
        self.assertEqual(self.app['accesscodes']['CLR-1'].used_num, 1)
        self.assertEqual(self.app['accesscodes']['CLR-1'].disabled_num, 0)

        self.csv_file = os.path.join(self.workdir, 'sample_ac_data_update.csv')
        open(self.csv_file, 'wb').write(AC_SAMPLE_DATA_UPDATE)
        num, num_warns, fin_file, fail_file =  self.processor.doImport(
            self.csv_file, AC_HEADER_FIELDS_UPDATE, 'update')
        self.assertEqual(num_warns,0)
        self.assertEqual(
            self.app['accesscodes']['HOS-1']['HOS-1-98769876'].state,
            'disabled')
        self.assertEqual(
            self.app['accesscodes']['CLR-1']['CLR-1-1625368961'].state,
            'disabled')
        self.assertMatches(
            self.app['accesscodes']['CLR-1']['CLR-1-1625368961'].history,
            "<YYYY-MM-DD hh:mm:ss> UTC - initialized by system|"
            "|<YYYY-MM-DD hh:mm:ss> UTC - state 'used' set by system|"
            "|<YYYY-MM-DD hh:mm:ss> UTC - state 'disabled' set by system")
        self.assertMatches(
            self.app['accesscodes']['HOS-1']['HOS-1-98769876'].history,
            "<YYYY-MM-DD hh:mm:ss> UTC - initialized by system|"
            "|<YYYY-MM-DD hh:mm:ss> UTC - used by system|"
            "|<YYYY-MM-DD hh:mm:ss> UTC - disabled by system")
        # When importing transitions the counters are properly set.
        self.assertEqual(self.app['accesscodes']['HOS-1'].used_num, 0)
        self.assertEqual(self.app['accesscodes']['HOS-1'].disabled_num, 1)
        # When importing states the counters remain unchanged.
        self.assertEqual(self.app['accesscodes']['CLR-1'].used_num, 1)
        self.assertEqual(self.app['accesscodes']['CLR-1'].disabled_num, 0)
        shutil.rmtree(os.path.dirname(fin_file))
        return
