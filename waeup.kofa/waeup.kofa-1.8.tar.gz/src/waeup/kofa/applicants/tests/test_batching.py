## $Id: test_batching.py 15553 2019-08-19 19:32:09Z henrik $
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
"""Unit tests for applicants-related data processors.
"""
import datetime
import os
import pytz
import shutil
import tempfile
import unittest
import grok
from time import time
from hurry.workflow.interfaces import IWorkflowState
from zope.component.hooks import setSite, clearSite
from zope.component import createObject
from zope.interface.verify import verifyClass, verifyObject
from zope.event import notify

from waeup.kofa.app import University
from waeup.kofa.applicants.batching import (
    ApplicantsContainerProcessor, ApplicantProcessor,
    ApplicantOnlinePaymentProcessor)
from waeup.kofa.applicants.container import ApplicantsContainer
from waeup.kofa.applicants.applicant import Applicant
from waeup.kofa.university.faculty import Faculty
from waeup.kofa.university.department import Department
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase
from waeup.kofa.interfaces import (
    IBatchProcessor, IUserAccount, DuplicationError)
from waeup.kofa.applicants.workflow import CREATED


# Sample data we can use in tests...
APPS_CONTAINER_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_container_data.csv'),
    'rb').read()

# The header fields of the above CSV snippet
APPS_CONTAINER_HEADER_FIELDS = APPS_CONTAINER_SAMPLE_DATA.split(
    '\n')[0].split(',')

# The same for applicants
APPLICANT_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_applicant_data.csv'),
    'rb').read()
FAULTY_APPLICANT_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__),
                 'sample_faulty_applicant_data.csv'), 'rb').read()

APPLICANT_HEADER_FIELDS = APPLICANT_SAMPLE_DATA.split(
    '\n')[0].split(',')

APPLICANT_SAMPLE_DATA_UPDATE = open(
    os.path.join(os.path.dirname(__file__),
                 'sample_applicant_data_update.csv'), 'rb').read()

APPLICANT_SAMPLE_DATA_UPDATE2 = open(
    os.path.join(os.path.dirname(__file__),
                 'sample_applicant_data_update2.csv'), 'rb').read()

APPLICANT_HEADER_FIELDS_UPDATE = APPLICANT_SAMPLE_DATA_UPDATE.split(
    '\n')[0].split(',')

APPLICANT_HEADER_FIELDS_UPDATE2 = APPLICANT_SAMPLE_DATA_UPDATE2.split(
    '\n')[0].split(',')

PAYMENT_SAMPLE_DATA = open(
    os.path.join(os.path.dirname(__file__), 'sample_payment_data.csv'),
    'rb').read()

PAYMENT_HEADER_FIELDS = PAYMENT_SAMPLE_DATA.split(
    '\n')[0].split(',')

class ApplicantsContainerProcessorTest(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(ApplicantsContainerProcessorTest, self).setUp()

        # Setup a sample site for each test
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']
        self.container = ApplicantsContainer()
        self.container.code = u'dp2011'
        self.app['applicants']['dp2011'] = self.container

        self.processor = ApplicantsContainerProcessor()
        self.workdir = tempfile.mkdtemp()
        self.csv_file = os.path.join(self.workdir, 'sampledata.csv')
        open(self.csv_file, 'wb').write(APPS_CONTAINER_SAMPLE_DATA)
        setSite(self.app)
        return

    def tearDown(self):
        super(ApplicantsContainerProcessorTest, self).tearDown()
        shutil.rmtree(self.workdir)
        shutil.rmtree(self.dc_root)
        clearSite()
        return

    def test_interface(self):
        # Make sure we fulfill the interface contracts.
        assert verifyObject(IBatchProcessor, self.processor) is True
        assert verifyClass(
            IBatchProcessor, ApplicantsContainerProcessor) is True

    def test_parentsExist(self):
        assert self.processor.parentsExist(None, dict()) is False
        assert self.processor.parentsExist(None, self.app) is True

    def test_entryExists(self):
        assert self.processor.entryExists(
            dict(code='REG_NONE'), self.app) is False
        assert self.processor.entryExists(
            dict(code='dp2011'), self.app) is True

    def test_getParent(self):
        parent = self.processor.getParent(None, self.app)
        assert parent is self.app['applicants']

    def test_getEntry(self):
        assert self.processor.getEntry(
            dict(code='REG_NONE'), self.app) is None
        assert self.processor.getEntry(
            dict(code='dp2011'), self.app) is self.container

    def test_addEntry(self):
        self.processor.addEntry(
            'New application', dict(code='dp2012'), self.app)
        assert self.app['applicants']['dp2012'] == 'New application'

    def test_delEntry(self):
        self.processor.delEntry(dict(code='dp2011'), self.app)
        assert 'dp2011' not in self.app['applicants'].keys()

    def test_import(self):
        # Do a real import
        # see local sample_container.csv file for input
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, APPS_CONTAINER_HEADER_FIELDS)
        avail_containers = [x for x in self.app['applicants'].keys()]
        container = self.app['applicants'].get('app2017', None)
        container2 = self.app['applicants'].get('app2018', None)
        self.assertTrue(container is not None)
        self.assertTrue(container2 is not None)

        # check attributes
        self.assertEqual(container.code, u'app2017')
        self.assertEqual(container.title, u'General Studies')
        self.assertEqual(container.prefix, u'app')
        self.assertEqual(container.year, 2017)
        self.assertEqual(container.application_category, 'basic')
        self.assertEqual(
            container.description,
            u'This text can been seen by anonymous users.\n'
            u'>>de<<\nDieser Text kann von anonymen Benutzern '
            u'gelesen werden.')
        self.assertEqual(container.startdate,
                         datetime.datetime(2012, 3, 1, 0, 0, tzinfo=pytz.utc))
        self.assertEqual(container.enddate,
                         datetime.datetime(2012, 4, 25, 0, 0, tzinfo=pytz.utc))
        shutil.rmtree(os.path.dirname(fin_file))

class ApplicantImportExportSetup(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(ApplicantImportExportSetup, self).setUp()
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

        # Add an applicants container
        self.container = ApplicantsContainer()
        self.container.code = u'dp2011'
        self.container.application_category = u'basic'
        self.app['applicants']['dp2011'] = self.container

        # Populate university
        self.certificate = createObject('waeup.Certificate')
        self.certificate.code = 'CERT1'
        self.certificate.application_category = 'basic'
        self.certificate.start_level = 100
        self.certificate.end_level = 500
        self.app['faculties']['fac1'] = Faculty()
        self.app['faculties']['fac1']['dep1'] = Department()
        self.app['faculties']['fac1']['dep1'].certificates.addCertificate(
            self.certificate)
        self.certificate2 = createObject('waeup.Certificate')
        self.certificate2.code = 'CERT2'
        self.certificate2.application_category = 'xyz'
        self.app['faculties']['fac1']['dep1'].certificates.addCertificate(
            self.certificate2)

        # Add applicant with subobjects
        applicant = Applicant()
        applicant.firstname = u'Anna'
        applicant.lastname = u'Tester'
        self.app['applicants']['dp2011'].addApplicant(applicant)
        self.application_number = applicant.application_number
        self.applicant = self.app['applicants']['dp2011'][
            self.application_number]
        self.workdir = tempfile.mkdtemp()

        self.logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'applicants.log')
        return

    def tearDown(self):
        super(ApplicantImportExportSetup, self).tearDown()
        shutil.rmtree(self.workdir)
        shutil.rmtree(self.dc_root)
        clearSite()
        return

class ApplicantProcessorTest(ApplicantImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(ApplicantProcessorTest, self).setUp()
        self.processor = ApplicantProcessor()
        self.csv_file = os.path.join(self.workdir, 'sample_applicant_data.csv')
        self.csv_file_faulty = os.path.join(self.workdir,
                                            'faulty_applicant_data.csv')
        self.csv_file_update = os.path.join(
            self.workdir, 'sample_applicant_data_update.csv')
        self.csv_file_update2 = os.path.join(
            self.workdir, 'sample_applicant_data_update2.csv')
        open(self.csv_file, 'wb').write(APPLICANT_SAMPLE_DATA)
        open(self.csv_file_faulty, 'wb').write(FAULTY_APPLICANT_SAMPLE_DATA)
        open(self.csv_file_update, 'wb').write(APPLICANT_SAMPLE_DATA_UPDATE)
        open(self.csv_file_update2, 'wb').write(APPLICANT_SAMPLE_DATA_UPDATE2)

    def test_interface(self):
        # Make sure we fulfill the interface contracts.
        assert verifyObject(IBatchProcessor, self.processor) is True
        assert verifyClass(
            IBatchProcessor, ApplicantProcessor) is True

    def test_entryExists(self):
        assert self.processor.entryExists(
            dict(container_code='dp2011', application_number='999'),
            self.app) is False

    def test_getEntry(self):
        applicant = self.processor.getEntry(
            dict(container_code='dp2011',
                 application_number=self.application_number), self.app)
        self.assertEqual(applicant.applicant_id, self.applicant.applicant_id)

    def test_addEntry(self):
        new_applicant = Applicant()
        self.processor.addEntry(
            new_applicant, dict(container_code='dp2011'), self.app)
        assert len(self.app['applicants']['dp2011'].keys()) == 2

    def test_delEntry(self):
        assert self.application_number in self.app[
            'applicants']['dp2011'].keys()
        self.processor.delEntry(
            dict(container_code='dp2011',
                application_number=self.application_number), self.app)
        assert self.application_number not in self.app[
            'applicants']['dp2011'].keys()

    def test_import(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, APPLICANT_HEADER_FIELDS)
        self.assertEqual(num_warns,0)
        keys = self.app['applicants']['dp2011'].keys()
        assert len(keys) == 5
        container = self.app['applicants']['dp2011']
        assert  container.__implemented__.__name__ == (
            'waeup.kofa.applicants.container.ApplicantsContainer')
        applicant = container[keys[0]]
        assert applicant.__implemented__.__name__ == (
            'waeup.kofa.applicants.applicant.Applicant')
        logcontent = open(self.logfile).read()
        # Logging message from updateEntry,
        # create applicant with given application_number
        self.assertTrue(
            'Applicant Processor - sample_applicant_data - imported: '
            'applicant_id=dp2011_1234, password=mypwd1, '
            'reg_number=1001, firstname=Aaren, middlename=Peter, lastname=Pieri, '
            'sex=m, course1=CERT1, date_of_birth=1990-01-02, email=xx@yy.zz' in
            logcontent)
        # create applicant with random application_number which is
        # not shown in the log file
        self.assertTrue(
            'Applicant Processor - sample_applicant_data - imported: '
            'reg_number=1003, firstname=Aaren, '
            'middlename=Alfons, lastname=Berson, sex=m, course1=CERT1, '
            'date_of_birth=1990-01-04, email=xx@yy.zz' in
            logcontent)
        # Logging message from handle_applicant_transition_event
        self.assertTrue(
            'dp2011_1234 - Application initialized' in
            logcontent)
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_faulty(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file_faulty, APPLICANT_HEADER_FIELDS)
        # we cannot import data with faulty dates. A date is faulty
        # when in format xx/yy/zzzz as we cannot say whether it is
        # meant as dd/mm/yyyy or mm/dd/yyyy. We therefore require yyyy-mm-dd
        for applicant in self.app['applicants']['dp2011'].values():
            if applicant.date_of_birth == datetime.date(1990, 1, 2):
                self.fail(
                    'Wrong birthdate of imported applicant '
                    '(1990-01-02, should be: 1990-02-01)')
        self.assertEqual(num_warns,4)
        fail_contents = open(fail_file, 'rb').read()
        # CERT2 is in wrong category ...
        self.assertTrue('course1: wrong application category' in fail_contents)
        # ... and CERT3 does not exist.
        self.assertTrue('course1: Invalid value' in fail_contents)
        # Conversion checking already fails because Mister or Miss No's 
        # container does not exist.
        self.assertTrue('no@yy.zz,container: not found' in fail_contents)
        self.assertTrue('nobody@yy.zz,container: not found' in fail_contents)
        shutil.rmtree(os.path.dirname(fail_file))
        return

    def test_import_update(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, APPLICANT_HEADER_FIELDS)
        shutil.rmtree(os.path.dirname(fin_file))
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file_update, APPLICANT_HEADER_FIELDS_UPDATE, 'update')
        self.assertEqual(num_warns,0)
        # The middlename import value was None.
        # Confirm that middlename has not been deleted.
        container = self.app['applicants']['dp2011']
        self.assertEqual(container['1234'].middlename, 'Peter')
        # state of Pieri has not changed
        self.assertEqual(container['1234'].state,'initialized')
        # state of Finau has changed
        self.assertEqual(container['2345'].state,'admitted')
        # password of Pieri has been set
        self.assertTrue(IUserAccount(container['1234']).checkPassword('mypwd1'))
        # password of Finau is still unset
        self.assertEqual(IUserAccount(container['2345']).password,None)
        # password of Simon was encrypted already
        self.assertTrue(
            IUserAccount(container['4567']).checkPassword('mypwd1'))
        # reg_number of Finau has changed
        self.assertEqual(container['2345'].reg_number, '6666')
        logcontent = open(self.logfile).read()
        # Logging message from updateEntry,
        # reg_number is locator
        self.assertTrue(
            'Applicant Processor - sample_applicant_data_update - updated: '
            'reg_number=1001, firstname=Aaren' in
            logcontent)
        # applicant_id is locator
        self.assertTrue(
            'Applicant Processor - sample_applicant_data_update - updated: '
            'state=admitted, reg_number=6666, '
            'firstname=Alfons, applicant_id=dp2011_2345' in
            logcontent)
        shutil.rmtree(os.path.dirname(fin_file))

        # Now we import another file which clears all middlename attributes
        # and uses the new reg_number as locator. This test also checks
        # if the catalog has been informed about the reg_no change and if
        # applicants in state created are really blocked.
        IWorkflowState(container['4567']).setState(CREATED)
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file_update2, APPLICANT_HEADER_FIELDS_UPDATE2, 'update')
        failcontent = open(fail_file).read()
        self.assertTrue('Applicant is blocked' in failcontent)
        self.assertEqual(num_warns,1)
        # Middlename is cleared.
        assert container['1234'].middlename is None
        # Firstname of applicant in state created isn't changed.
        self.assertEqual(container['4567'].firstname, 'Simon')
        shutil.rmtree(os.path.dirname(fin_file))

    def test_import_remove(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, APPLICANT_HEADER_FIELDS)
        shutil.rmtree(os.path.dirname(fin_file))
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file_update, APPLICANT_HEADER_FIELDS_UPDATE, 'remove')
        self.assertEqual(num_warns,0)
        logcontent = open(self.logfile).read()
        # Logging message from handle_applicant_transition_event
        self.assertTrue(
            'dp2011_1234 - Application record removed' in
            logcontent)
        shutil.rmtree(os.path.dirname(fin_file))

class PaymentProcessorTest(ApplicantImportExportSetup):

    def setUp(self):
        super(PaymentProcessorTest, self).setUp()

        applicant = Applicant()
        applicant.firstname = u'Anna2'
        applicant.lastname = u'Tester'
        applicant.applicant_id = u'dp2011_1234'
        self.app['applicants']['dp2011'].addApplicant(applicant)
        payment = createObject(u'waeup.ApplicantOnlinePayment')
        payment.p_id = 'p120'
        payment.p_session = 2012
        payment.p_category = 'application'
        payment.p_state = 'paid'
        applicant['p120'] = payment
        self.applicant2 = applicant
        self.processor = ApplicantOnlinePaymentProcessor()
        self.csv_file = os.path.join(
            self.workdir, 'sample_payment_data.csv')
        open(self.csv_file, 'wb').write(PAYMENT_SAMPLE_DATA)

    def test_interface(self):
        # Make sure we fulfill the interface contracts.
        assert verifyObject(IBatchProcessor, self.processor) is True
        assert verifyClass(
            IBatchProcessor, ApplicantOnlinePaymentProcessor) is True

    def test_getEntry(self):
        assert self.processor.getEntry(
            dict(applicant_id='ID_NONE', p_id='nonsense'), self.app) is None
        assert self.processor.getEntry(
            dict(applicant_id=self.applicant2.applicant_id, p_id='p120'),
            self.app) is self.applicant2['p120']
        assert self.processor.getEntry(
            dict(applicant_id=self.applicant2.applicant_id, p_id='p120#'),
            self.app) is self.applicant2['p120']

    def test_delEntry(self):
        assert self.processor.getEntry(
            dict(applicant_id=self.applicant2.applicant_id, p_id='p120'),
            self.app) is self.applicant2['p120']
        self.assertEqual(len(self.applicant2.keys()),1)
        self.processor.delEntry(
            dict(applicant_id=self.applicant2.applicant_id, p_id='p120'),
            self.app)
        assert self.processor.getEntry(
            dict(applicant_id=self.applicant2.applicant_id, p_id='p120'),
            self.app) is None
        self.assertEqual(len(self.applicant.keys()),0)

    def test_addEntry(self):
        self.assertEqual(len(self.applicant2.keys()),1)
        self.processor.delEntry(
            dict(applicant_id=self.applicant2.applicant_id, p_id='p120'),
            self.app)
        payment1 = createObject(u'waeup.ApplicantOnlinePayment')
        payment1.p_category = 'application'
        payment1.p_id = 'p234'
        self.processor.addEntry(
            payment1, dict(applicant_id=self.applicant2.applicant_id, p_id='p234'),
            self.app)
        self.assertEqual(len(self.applicant2.keys()),1)
        self.assertEqual(self.applicant2['p234'].p_id, 'p234')
        # Same payment must not exist.
        payment1.p_state = 'paid'
        payment2 = createObject(u'waeup.ApplicantOnlinePayment')
        payment2.p_id = 'p456'
        payment2.p_category = 'application'
        self.assertRaises(
            DuplicationError, self.processor.addEntry, payment2,
            dict(applicant_id=self.applicant2.applicant_id, p_id='p456'), self.app)
        # But we can add a ticket with another p_category.
        payment2.p_category = 'app_balance'
        self.processor.addEntry(
            payment2, dict(applicant_id=self.applicant2.applicant_id, p_id='p456'),
            self.app)
        self.assertEqual(len(self.applicant2.keys()),2)
        self.assertEqual(self.applicant2['p456'].p_id, 'p456')

    def test_checkConversion(self):
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(p_id='<IGNORE>'), mode='create')
        self.assertEqual(len(errs),0)
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(p_id='<IGNORE>'), mode='update')
        self.assertEqual(len(errs),1)
        self.assertEqual(errs[0], ('p_id', u'missing'))
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(p_id='p1266236341955'))
        self.assertEqual(len(errs),0)
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(p_id='nonsense'))
        self.assertEqual(len(errs),1)
        self.assertEqual(errs[0], ('p_id', u'invalid length'))
        timestamp = ("%d" % int(time()*10000))[1:]
        p_id = "p%s" % timestamp
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(p_id=p_id))
        self.assertEqual(len(errs),0)
        dup_payment = createObject(u'waeup.ApplicantOnlinePayment')
        dup_payment.p_id = 'p1266236341955'
        self.applicant2[dup_payment.p_id] = dup_payment
        errs, inv_errs, conv_dict = self.processor.checkConversion(
            dict(p_id='p1266236341955'), mode='create')
        self.assertEqual(len(errs),1)
        self.assertEqual(errs[0], ('p_id', u'p_id exists in dp2011_1234 '))

    def test_import(self):
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, PAYMENT_HEADER_FIELDS,'create')
        self.assertEqual(num_warns,2)
        fail_file = open(fail_file).read()
        self.assertTrue('Payment has already been made' in fail_file)
        self.processor.delEntry(
            dict(applicant_id=self.applicant2.applicant_id, p_id='p120'),
            self.app)
        num, num_warns, fin_file, fail_file = self.processor.doImport(
            self.csv_file, PAYMENT_HEADER_FIELDS,'create')
        # Both records can be imported now.
        self.assertEqual(num_warns,0)
        # One with imported and known p_id ...
        payment = self.processor.getEntry(dict(applicant_id='dp2011_1234',
            p_id='p1266236341955'), self.app)
        self.assertEqual(payment.p_id, 'p1266236341955')
        cdate = payment.creation_date.strftime("%Y-%m-%d %H:%M:%S")
        # Ooooh, still the old problem, see
        # http://mail.dzug.org/mailman/archives/zope/2006-August/001153.html.
        # WAT is interpreted as GMT-1 and not GMT+1
        self.assertEqual(cdate, '2010-11-25 21:16:33')
        self.assertEqual(str(payment.creation_date.tzinfo),'UTC')
        # ... the other one with generated p_id.
        p_id_failed = self.applicant2.keys()[1]
        payment_failed = self.processor.getEntry(dict(applicant_id='dp2011_1234',
            p_id=p_id_failed), self.app)
        self.assertEqual(payment_failed.p_state, 'failed')
        self.assertEqual(payment_failed.amount_auth, 10500.1)
        shutil.rmtree(os.path.dirname(fin_file))
        logcontent = open(self.logfile).read()
        # Logging message from updateEntry
        self.assertTrue(
            'INFO - system - ApplicantOnlinePayment Processor - dp2011_1234 - '
            'previous update cancelled' in logcontent)
        self.assertTrue(
            'INFO - system - ApplicantOnlinePayment Processor - '
            'sample_payment_data - dp2011_1234 - updated: p_id=p1266236341955, '
            'creation_date=2010-11-25 21:16:33.757000+00:00, '
            'r_amount_approved=19500.1, p_category=application, '
            'amount_auth=19500.1, p_session=2015, p_state=paid' in logcontent)
        self.assertTrue(
            'INFO - system - ApplicantOnlinePayment Processor - '
            'sample_payment_data - dp2011_1234 - updated: p_id=%s, '
            'creation_date=2011-11-25 21:16:33.757000+00:00, '
            'r_amount_approved=19500.1, p_category=application, '
            'amount_auth=10500.1, p_session=2016, p_state=failed'
            % p_id_failed in logcontent)
