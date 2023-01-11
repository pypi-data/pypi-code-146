## $Id: test_browser.py 17261 2023-01-09 21:16:28Z henrik $
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
Test the applicant-related UI components.
"""
import os
import pytz
import shutil
import tempfile
import grok
import logging
from StringIO import StringIO
from datetime import datetime, date, timedelta
from mechanize import LinkNotFoundError
from zc.async.testing import wait_for_result
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.event import notify
from zope.catalog.interfaces import ICatalog
from zope.component import createObject, getUtility
from zope.component.hooks import setSite, clearSite
from zope.security.interfaces import Unauthorized
from zope.testbrowser.testing import Browser
from zope.interface import implementedBy
from zope.schema.fieldproperty import FieldProperty
from hurry.workflow.interfaces import IWorkflowInfo, IWorkflowState
from waeup.kofa.browser.tests.test_pdf import samples_dir
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase
from waeup.kofa.app import University
from waeup.kofa.payments.interfaces import IPayer
from waeup.kofa.configuration import SessionConfiguration
from waeup.kofa.refereeentries import RefereeEntry
from waeup.kofa.applicants.container import ApplicantsContainer
from waeup.kofa.applicants.applicant import Applicant
from waeup.kofa.interfaces import (
    IExtFileStore, IFileStoreNameChooser, IUserAccount, IJobManager)
from waeup.kofa.university.faculty import Faculty
from waeup.kofa.university.department import Department
from waeup.kofa.mandates.mandate import RefereeReportMandate
from waeup.kofa.tests.test_async import FunctionalAsyncTestCase
from waeup.kofa.tests.test_authentication import SECRET

PH_LEN = 15911  # Length of placeholder file

session_1 = datetime.now().year - 2
container_name_1 = u'app%s' % session_1
session_2 = datetime.now().year - 1
container_name_2 = u'app%s' % session_2

SAMPLE_IMAGE = os.path.join(os.path.dirname(__file__), 'test_image.jpg')

class ApplicantsFullSetup(FunctionalTestCase):
    # A test case that only contains a setup and teardown
    #
    # Complete setup for applicants handlings is rather complex and
    # requires lots of things created before we can start. This is a
    # setup that does all this, creates a university, creates PINs,
    # etc.  so that we do not have to bother with that in different
    # test cases.

    layer = FunctionalLayer

    def setUp(self):
        super(ApplicantsFullSetup, self).setUp()

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

        self.login_path = 'http://localhost/app/login'
        self.root_path = 'http://localhost/app/applicants'
        self.search_path = 'http://localhost/app/applicants/search'
        self.manage_root_path = self.root_path + '/@@manage'
        self.add_container_path = self.root_path + '/@@add'
        self.container_path = 'http://localhost/app/applicants/%s' % container_name_1
        self.manage_container_path = self.container_path + '/@@manage'

        # Add an applicants container
        applicantscontainer = ApplicantsContainer()
        applicantscontainer.code = container_name_1
        applicantscontainer.prefix = 'app'
        applicantscontainer.year = session_1
        applicantscontainer.title = u'This is the %s container' % container_name_1
        applicantscontainer.application_category = 'basic'
        applicantscontainer.mode = 'create'
        applicantscontainer.strict_deadline = True
        delta = timedelta(days=10)
        applicantscontainer.startdate = datetime.now(pytz.utc) - delta
        applicantscontainer.enddate = datetime.now(pytz.utc) + delta
        self.app['applicants'][container_name_1] = applicantscontainer
        self.applicantscontainer = self.app['applicants'][container_name_1]

        # Populate university
        certificate = createObject('waeup.Certificate')
        certificate.code = 'CERT1'
        certificate.application_category = 'basic'
        certificate.start_level = 100
        certificate.end_level = 500
        certificate.study_mode = u'ug_ft'
        self.certificate = certificate
        self.app['faculties']['fac1'] = Faculty()
        # The code has explicitely to be set, otherwise we don't
        # find created students in their department
        self.app['faculties']['fac1']['dep1'] = Department(code=u'dep1')
        self.department = self.app['faculties']['fac1']['dep1']
        self.app['faculties']['fac1']['dep1'].certificates.addCertificate(
            certificate)

        # Put the prepopulated site into test ZODB and prepare test
        # browser
        self.browser = Browser()
        self.browser.handleErrors = False

        # Create 5 access codes with prefix'FOO' and cost 9.99 each
        pin_container = self.app['accesscodes']
        pin_container.createBatch(
            datetime.now(), 'some_userid', 'APP', 9.99, 5)
        pins = pin_container[pin_container.keys()[0]].values()
        self.pins = [x.representation for x in pins]
        self.existing_pin = self.pins[0]
        parts = self.existing_pin.split('-')[1:]
        self.existing_series, self.existing_number = parts

        # Add an applicant
        self.applicant = createObject('waeup.Applicant')
        # reg_number is the only field which has to be preset here
        # because managers are allowed to edit this required field
        self.applicant.firstname = u'Joan'
        self.applicant.reg_number = u'1234'
        self.applicant.course1 = certificate
        app['applicants'][container_name_1].addApplicant(self.applicant)
        IUserAccount(
            self.app['applicants'][container_name_1][
            self.applicant.application_number]).setPassword('apwd')
        self.manage_path = 'http://localhost/app/applicants/%s/%s/%s' % (
            container_name_1, self.applicant.application_number, 'manage')
        self.edit_path = 'http://localhost/app/applicants/%s/%s/%s' % (
            container_name_1, self.applicant.application_number, 'edit')
        self.view_path = 'http://localhost/app/applicants/%s/%s' % (
            container_name_1, self.applicant.application_number)

    def login(self):
        # Perform an applicant login. This creates an application record.
        #
        # This helper also sets `self.applicant`, which is the
        # applicant object created.
        self.browser.open(self.login_path)
        self.browser.getControl(
            name="form.login").value = self.applicant.applicant_id
        self.browser.getControl(name="form.password").value = 'apwd'
        self.browser.getControl("Login").click()

    def fill_correct_values(self):
        # Fill the edit form with suitable values
        self.browser.getControl(name="form.firstname").value = 'John'
        self.browser.getControl(name="form.middlename").value = 'Anthony'
        self.browser.getControl(name="form.lastname").value = 'Tester'
        self.browser.getControl(name="form.course1").value = ['CERT1']
        self.browser.getControl(name="form.date_of_birth").value = '09/09/1988'
        self.browser.getControl(name="form.sex").value = ['m']
        self.browser.getControl(name="form.email").value = 'xx@yy.zz'

    def tearDown(self):
        super(ApplicantsFullSetup, self).tearDown()
        clearSite()
        shutil.rmtree(self.dc_root)

class ApplicantsRootUITests(ApplicantsFullSetup):
    # Tests for ApplicantsRoot class

    layer = FunctionalLayer

    def test_anonymous_access(self):
        # Anonymous users can access applicants root
        self.browser.open(self.root_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertFalse(
            'Manage ' in self.browser.contents)
        return

    def test_anonymous_no_actions(self):
        # Make sure anonymous users cannot access actions
        self.browser.open(self.root_path)
        self.assertRaises(
            LookupError, self.browser.getControl, "Add local role")
        # Manage screen neither linked nor accessible for anonymous
        self.assertRaises(
            LinkNotFoundError,
            self.browser.getLink, 'Manage applicants section')
        self.assertRaises(
            Unauthorized, self.browser.open, self.manage_root_path)
        # Add container screen not accessible for anonymous
        self.assertRaises(
            Unauthorized, self.browser.open, self.add_container_path)
        return

    def test_manage_access(self):
        # Managers can access the manage pages of applicants root
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.root_path)
        self.assertTrue('Manage applicants section' in self.browser.contents)
        # There is a manage link
        link = self.browser.getLink('Manage applicants section')
        link.click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.manage_root_path)
        return

    def test_hide_container(self):
        self.browser.open(self.root_path)
        self.assertTrue(
            '<a href="http://localhost/app/applicants/%s">'
            'This is the %s container</a>' % (container_name_1, container_name_1)
            in self.browser.contents)
        self.app['applicants'][container_name_1].hidden = True
        self.browser.open(self.root_path)
        # Anonymous users can't see hidden containers
        self.assertFalse(
            '<a href="http://localhost/app/applicants/%s">'
            'This is the %s container</a>' % (container_name_1, container_name_1)
            in self.browser.contents)
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.root_path)
        self.assertTrue(
            '<a href="http://localhost/app/applicants/%s">'
            'This is the %s container</a>' % (container_name_1, container_name_1)
            in self.browser.contents)
        return

    def test_search(self):
        # Managers can access the manage pages of applicants root
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.manage_path)
        self.fill_correct_values()
        self.browser.getControl("Save").click()
        self.browser.open(self.root_path)
        self.assertTrue('Manage applicants section' in self.browser.contents)
        # There is a search link
        link = self.browser.getLink('Find applicants')
        link.click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        # We can find an applicant ...
        # ... via his name
        self.browser.getControl(name="searchtype").value = ['fullname']
        self.browser.getControl(name="searchterm").value = 'John'
        self.browser.getControl("Find applicant").click()
        self.assertTrue('John Anthony Tester' in self.browser.contents)
        self.browser.getControl(name="searchtype").value = ['fullname']
        self.browser.getControl(name="searchterm").value = 'Tester'
        self.browser.getControl("Find applicant").click()
        self.assertTrue('John Anthony Tester' in self.browser.contents)
        self.browser.open(self.search_path)
        # ... and via his reg_number ...
        self.browser.getControl(name="searchtype").value = ['reg_number']
        self.browser.getControl(name="searchterm").value = '2345'
        self.browser.getControl("Find applicant").click()
        self.assertFalse('John Anthony Tester' in self.browser.contents)
        self.browser.getControl(name="searchtype").value = ['reg_number']
        self.browser.getControl(name="searchterm").value = '1234'
        self.browser.getControl("Find applicant").click()
        self.assertTrue('John Anthony Tester' in self.browser.contents)
        # ... and not via his application_number ...
        self.browser.getControl(name="searchtype").value = ['applicant_id']
        self.browser.getControl(
            name="searchterm").value = self.applicant.application_number
        self.browser.getControl("Find applicant").click()
        self.assertFalse('John Anthony Tester' in self.browser.contents)
        # ... but ia his applicant_id ...
        self.browser.getControl(name="searchtype").value = ['applicant_id']
        self.browser.getControl(
            name="searchterm").value = self.applicant.applicant_id
        self.browser.getControl("Find applicant").click()
        self.assertTrue('John Anthony Tester' in self.browser.contents)
        # ... and via his email
        self.browser.getControl(name="searchtype").value = ['email']
        self.browser.getControl(name="searchterm").value = 'xx@yy.zz'
        self.browser.getControl("Find applicant").click()
        self.assertTrue('John Anthony Tester' in self.browser.contents)
        return

    def test_manage_actions_access(self):
        # Managers can access the action on manage screen
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.manage_root_path)
        self.browser.getControl("Add local role").click()
        self.assertTrue('No user selected' in self.browser.contents)
        return

    def test_local_roles_add_delete(self):
        # Managers can assign and delete local roles of applicants root
        myusers = self.app['users']
        myusers.addUser('bob', 'bobssecret')
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open('http://localhost/app/faculties/fac1/dep1/manage')
        self.browser.getControl(name="user").value = ['bob']
        self.browser.getControl(name="local_role").value = [
            'waeup.local.ApplicationsManager']
        self.browser.getControl("Add local role").click()
        self.assertTrue('<td>bob</td>' in self.browser.contents)
        # Remove the role assigned
        ctrl = self.browser.getControl(name='role_id')
        ctrl.getControl(
            value='bob|waeup.local.ApplicationsManager').selected = True
        self.browser.getControl("Remove selected local roles").click()
        self.assertTrue(
            'Local role successfully removed: bob|waeup.local.ApplicationsManager'
            in self.browser.contents)
        self.assertFalse('<td>bob</td>' in self.browser.contents)
        return

    def test_add_delete_container(self):
        # Managers can add and delete applicants containers
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.manage_root_path)
        self.browser.getControl("Add applicants container").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.add_container_path)
        self.browser.getControl(name="form.prefix").value = ['app']
        self.browser.getControl("Add applicants container").click()
        self.assertTrue(
            'There were errors' in self.browser.contents)
        self.browser.getControl(name="form.prefix").value = ['app']
        self.browser.getControl(name="form.year").value = [str(session_2)]
        self.browser.getControl(name="form.mode").value = ['create']
        self.browser.getControl(
            name="form.application_category").value = ['basic']
        self.browser.getControl("Add applicants container").click()
        self.assertTrue('Added:' in self.browser.contents)
        self.browser.getLink(container_name_1).click()
        self.assertTrue('Manage applicants container'
            in self.browser.contents)
        self.browser.open(self.add_container_path)
        self.browser.getControl("Cancel").click()
        self.assertEqual(self.browser.url, self.manage_root_path)
        self.browser.open(self.add_container_path)
        self.browser.getControl(name="form.prefix").value = ['app']
        self.browser.getControl(name="form.year").value = [str(session_2)]
        self.browser.getControl(name="form.mode").value = ['create']
        self.browser.getControl(
            name="form.application_category").value = ['basic']
        self.browser.getControl("Add applicants container").click()
        self.assertTrue('already exists in the database'
                        in self.browser.contents)
        # Managers can add containers with prefix+number code instead of
        # prefix+year code.
        self.browser.open(self.add_container_path)
        self.browser.getControl(name="form.prefix").value = ['app']
        self.browser.getControl(name="form.year").value = [str(session_2)]
        self.browser.getControl(name="form.container_number").value = ['8']
        self.browser.getControl(name="form.mode").value = ['create']
        self.browser.getControl(
            name="form.application_category").value = ['basic']
        self.browser.getControl("Add applicants container").click()
        self.assertTrue('Added: "app8"' in self.browser.contents)
        self.browser.getLink(container_name_1).click()
        self.assertTrue('Manage applicants container'
            in self.browser.contents)
        self.browser.open(self.manage_root_path)
        ctrl = self.browser.getControl(name='val_id')
        ctrl.getControl(value=container_name_2).selected = True
        self.browser.getControl("Remove selected", index=0).click()
        self.assertTrue('Successfully removed:' in self.browser.contents)
        self.browser.open(self.add_container_path)
        self.browser.getControl(name="form.prefix").value = ['app']
        self.browser.getControl(name="form.year").value = [str(session_2)]
        self.browser.getControl(name="form.mode").value = ['create']
        #self.browser.getControl(name="form.ac_prefix").value = ['APP']
        self.browser.getControl(
            name="form.application_category").value = ['basic']
        self.browser.getControl("Add applicants container").click()
        del self.app['applicants'][container_name_2]
        ctrl = self.browser.getControl(name='val_id')
        ctrl.getControl(value=container_name_2).selected = True
        self.browser.getControl("Remove selected", index=0).click()
        self.assertMatches('...Could not delete...', self.browser.contents)
        return

class ApplicantsContainerUITests(ApplicantsFullSetup):
    # Tests for ApplicantsContainer class views and pages

    layer = FunctionalLayer

    def test_anonymous_access(self):
        # Anonymous users can access applicants containers
        self.browser.open(self.container_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertFalse(
            'Manage ' in self.browser.contents)
        return

    def test_manage_access(self):
        # Managers can access the manage pages of applicants
        # containers and can perform actions
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.manage_container_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.manage_container_path)
        self.browser.getControl(name="form.application_fee").value = '200'
        self.browser.getControl("Save").click()
        self.assertTrue('Form has been saved' in self.browser.contents)
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'applicants.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - applicants.browser.ApplicantsContainerManageFormPage - '
            '%s - saved: application_fee\n' % container_name_1 in logcontent)
        self.browser.getControl("Remove selected", index=0).click()
        self.assertTrue('No applicant selected' in self.browser.contents)
        self.browser.getControl("Add local role").click()
        self.assertTrue('No user selected' in self.browser.contents)
        self.browser.getControl("Cancel", index=0).click()
        self.assertEqual(self.browser.url, self.container_path)
        return

    def test_statistics(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.container_path)
        self.browser.getLink("Container statistics").click()
        self.assertTrue('<td>initialized</td>' in self.browser.contents)
        self.assertTrue('<td>1</td>' in self.browser.contents)
        self.assertEqual(self.applicantscontainer.statistics[0],
            {'not admitted': 0, 'started': 0, 'created': 0,
            'admitted': 0, 'submitted': 0, 'initialized': 1,
            'paid': 0, 'processed': 0})
        #self.assertEqual(self.applicantscontainer.statistics[1],
        #    {u'fac1': 0})
        IWorkflowState(self.applicant).setState('submitted')
        notify(grok.ObjectModifiedEvent(self.applicant))
        self.assertEqual(self.applicantscontainer.statistics[0],
            {'not admitted': 0, 'started': 0, 'created': 0,
            'admitted': 0, 'submitted': 1, 'initialized': 0, 'paid': 0,
            'processed': 0})
        #self.assertEqual(self.applicantscontainer.statistics[1],
        #    {u'fac1': 1})
        return

    def test_add_delete_applicants(self):
        # Check the global role map first
        role_manager = IPrincipalRoleManager(grok.getSite())
        principals = role_manager.getPrincipalsForRole('waeup.Applicant')
        self.assertEqual(len(principals), 1)
        self.assertEqual(principals[0][0], self.applicant.applicant_id)
        # Managers can add and delete applicants
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.add_applicant_path = self.container_path + '/addapplicant'
        self.container_manage_path = self.container_path + '/@@manage'
        self.browser.open(self.container_manage_path)
        self.browser.getLink("Add applicant").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.add_applicant_path)
        self.browser.getControl(name="form.firstname").value = 'Alois'
        self.browser.getControl(name="form.middlename").value = 'Kofi'
        self.browser.getControl(name="form.lastname").value = 'Bettermann'
        self.browser.getControl(name="form.email").value = 'xx@yy.zz'
        self.browser.getControl("Create application record").click()
        self.assertTrue('Application initialized' in self.browser.contents)
        # The global role map has been extended
        role_manager = IPrincipalRoleManager(grok.getSite())
        principals = role_manager.getPrincipalsForRole('waeup.Applicant')
        self.assertEqual(len(principals), 2)
        self.browser.open(self.container_manage_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        ctrl.getControl(value=value).selected = True
        self.browser.getControl("Remove selected", index=0).click()
        self.assertTrue('Successfully removed:' in self.browser.contents)
        # The global role map has been reduced
        role_manager = IPrincipalRoleManager(grok.getSite())
        principals = role_manager.getPrincipalsForRole('waeup.Applicant')
        self.assertEqual(len(principals), 1)
        self.browser.open(self.add_applicant_path)
        self.browser.getControl(name="form.firstname").value = 'Albert'
        self.browser.getControl(name="form.lastname").value = 'Einstein'
        self.browser.getControl(name="form.email").value = 'xx@yy.zz'
        self.browser.getControl("Create application record").click()
        self.assertTrue('Application initialized' in self.browser.contents)
        return

    def test_prefill_purge_container(self):
        # Managers can pre-fill containers in create mode
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.prefill_path = self.container_path + '/prefill'
        self.container_manage_path = self.container_path + '/@@manage'
        self.browser.open(self.container_manage_path)
        self.browser.getLink("Pre-fill").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.url, self.prefill_path)
        self.browser.getControl(name="number").value = ['10']
        self.browser.getControl("Pre-fill").click()
        self.assertTrue('10 application records created.' in self.browser.contents)
        self.browser.open(self.container_manage_path)
        self.assertTrue('This container contains 10 unused pre-filled records.'
            in self.browser.contents)
        self.assertEqual(self.applicantscontainer.counts[0], 11)
        self.assertEqual(self.applicantscontainer.counts[1], 1)
        # In update mode we can't pre-fill the container
        self.applicantscontainer.mode = 'update'
        self.browser.open(self.container_manage_path)
        self.browser.getLink("Pre-fill").click()
        self.assertTrue('Container must be in create mode to be pre-filled.'
            in self.browser.contents)
        self.browser.open(self.manage_root_path)
        # Number of total records is 11
        self.assertTrue('<td>11</td>' in self.browser.contents)
        # The statistics have not changed
        self.browser.open(self.container_path)
        self.browser.getLink("Container statistics").click()
        self.assertTrue('<td>1</td>' in self.browser.contents)
        self.assertEqual(self.applicantscontainer.statistics[0],
            {'not admitted': 0, 'started': 0, 'created': 0,
            'admitted': 0, 'submitted': 0, 'initialized': 1,
            'paid': 0, 'processed': 0})
        # Container can be purged
        IWorkflowState(self.applicant).setState('submitted')
        self.browser.open(self.container_manage_path)
        self.browser.getLink("Purge").click()
        self.browser.getControl("Remove").click()
        self.assertTrue('10 application records purged' in self.browser.contents)
        self.assertEqual(self.applicantscontainer.counts[0], 1)
        self.assertEqual(self.applicantscontainer.counts[1], 1)
        IWorkflowState(self.applicant).setState('initialized')
        self.browser.open(self.container_manage_path)
        self.browser.getLink("Purge").click()
        self.browser.getControl("Remove").click()
        self.assertTrue('1 application records purged' in self.browser.contents)
        self.assertEqual(self.applicantscontainer.counts[0], 0)
        self.assertEqual(self.applicantscontainer.counts[1], 0)
        return

    def init_officer(self):
        # Create application officer
        self.app['users'].addUser('mrappl', SECRET)
        self.app['users']['mrappl'].email = 'mrappl@foo.ng'
        self.app['users']['mrappl'].title = 'Carlo Pitter'
        prmglobal = IPrincipalRoleManager(self.app)
        prmglobal.assignRoleToPrincipal('waeup.ApplicationsManager', 'mrappl')
        # Login as officer
        self.browser.open(self.login_path)
        self.browser.getControl(name="form.login").value = 'mrappl'
        self.browser.getControl(name="form.password").value = SECRET
        self.browser.getControl("Login").click()

    def test_student_creation_permission(self):
        self.init_officer()
        self.browser.open(self.container_path + '/manage')
        self.browser.getControl("Create students").click()
        self.assertTrue('You don\'t have permission to create student records'
            in self.browser.contents)
        prmglobal = IPrincipalRoleManager(self.app)
        prmglobal.assignRoleToPrincipal('waeup.StudentsCreator', 'mrappl')
        self.browser.getControl("Create students").click()
        self.assertTrue('No applicant selected' in self.browser.contents)


class ApplicantUITests(ApplicantsFullSetup):
    # Tests for uploading/browsing the passport image of appplicants

    layer = FunctionalLayer

    def setUp(self):
        super(ApplicantUITests, self).setUp()
        self.setup_logging()
        return

    def tearDown(self):
        super(ApplicantUITests, self).tearDown()
        self.teardown_logging()
        return

    def setup_logging(self):
        # setup a log-handler that catches all fake mailer output
        self.stream = StringIO()
        handler = logging.StreamHandler(self.stream)
        logger = logging.getLogger('test.smtp')
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return

    def get_fake_smtp_output(self):
        # get output generated by fake mailer
        self.stream.flush()
        self.stream.seek(0)
        return self.stream.read()

    def teardown_logging(self):
        # remove the log handler for fake mailer output
        logger = logging.getLogger('test.smtp')
        handlers = [x for x in logger.handlers]
        for handler in handlers:
            logger.removeHandler(handler)
        return

    def test_manage_and_view_applicant(self):
        # Managers can manage applicants
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.slip_path = self.view_path + '/application_slip.pdf'
        self.browser.open(self.manage_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.fill_correct_values()
        # Fire transition
        self.browser.getControl(name="transition").value = ['start']
        self.browser.getControl("Save").click()
        # Be sure that the empty phone field does not show wrong error message
        self.assertFalse('Required input is missing' in self.browser.contents)
        self.assertMatches('...Form has been saved...', self.browser.contents)
        self.assertMatches('...Application started by Manager...',
                           self.browser.contents)
        self.browser.open(self.view_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        # Change course_admitted
        self.browser.open(self.manage_path)
        self.browser.getControl(name="form.course_admitted").value = ['CERT1']
        self.browser.getControl("Save").click()
        self.assertMatches('...Form has been saved...', self.browser.contents)
        # Change password
        self.browser.getControl(name="password").value = 'secret'
        self.browser.getControl(name="control_password").value = 'secre'
        self.browser.getControl("Save").click()
        self.assertMatches('...Passwords do not match...',
                           self.browser.contents)
        self.browser.getControl(name="password").value = 'secret'
        self.browser.getControl(name="control_password").value = 'secret'
        self.browser.getControl("Save").click()
        self.assertMatches('...Form has been saved...', self.browser.contents)
        # Pdf slip can't be opened and download button is not available
        self.assertFalse('Download application slip' in self.browser.contents)
        self.browser.open(self.slip_path)
        self.assertTrue(
            'Please pay and submit before trying to download the application slip.'
            in self.browser.contents)
        # If applicant is in correct state the pdf slip can be opened.
        IWorkflowState(self.applicant).setState('submitted')
        self.browser.open(self.view_path)
        self.browser.getLink("Download application slip").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'],
                         'application/pdf')
        # Managers can view applicants even if certificate has been removed
        del self.app['faculties']['fac1']['dep1'].certificates['CERT1']
        self.browser.open(self.view_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.browser.open(self.slip_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        return

    def test_passport_edit_view(self):
        # We get a default image after login
        self.browser.open(self.login_path)
        self.login()
        self.browser.open(self.browser.url + '/passport.jpg')
        self.assertEqual(self.browser.headers['status'], '200 Ok')
        self.assertEqual(self.browser.headers['content-type'], 'image/jpeg')
        self.assertTrue('JFIF' in self.browser.contents)
        self.assertEqual(
            self.browser.headers['content-length'], str(PH_LEN))

    def test_applicant_login(self):
        self.applicant.suspended = True
        self.login()
        self.assertTrue(
            'You entered invalid credentials.' in self.browser.contents)
        self.applicant.suspended = False
        self.browser.getControl("Login").click()
        self.assertTrue(
            'You logged in as an applicant.' in self.browser.contents)

    def test_maintenance_mode(self):
        config = grok.getSite()['configuration']
        self.login()
        # Applicant  logged in.
        self.assertTrue('You logged in' in self.browser.contents)
        self.assertTrue("Joan None" in self.browser.contents)
        # If maintenance mode is enabled, applicant is immediately logged out.
        config.maintmode_enabled_by = u'any_user'
        self.assertRaises(
            Unauthorized, self.browser.open, 'http://localhost/app/faculties')
        self.browser.open('http://localhost/app/login')
        self.assertTrue('The portal is in maintenance mode' in self.browser.contents)
        # Applicant really can't login if maintenance mode is enabled.
        self.login()
        # A second warning is raised.
        self.assertTrue(
            'The portal is in maintenance mode. You can\'t login!'
            in self.browser.contents)
        return

    def test_applicant_access(self):
        # Applicants can edit their record
        self.browser.open(self.login_path)
        self.login()
        self.assertTrue(
            'You logged in as an applicant.' in self.browser.contents)
        self.browser.open(self.edit_path)
        self.assertTrue(self.browser.url != self.login_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.fill_correct_values()
        self.assertTrue(IUserAccount(self.applicant).checkPassword('apwd'))
        self.browser.getControl("Save").click()
        self.assertMatches('...Form has been saved...', self.browser.contents)
        # Applicants don't see manage and search links ...
        self.browser.open(self.root_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertFalse('Search' in self.browser.contents)
        self.assertFalse('Manage applicants section' in self.browser.contents)
        # ... and can't access the manage page
        self.assertRaises(
            Unauthorized, self.browser.open, self.manage_path)
        return

    def test_message_for_created(self):
        IWorkflowState(self.applicant).setState('created')
        self.applicant.student_id = u'my id'
        self.browser.open(self.login_path)
        self.login()
        self.assertTrue(
            'You logged in as an applicant.' in self.browser.contents)
        self.assertTrue(
            '<strong>Congratulations!</strong> You have been offered provisional'
            ' admission into the %s/%s Academic Session of'
            ' Sample University. Your student record has been created for you.'
            % (session_1, session_1 + 1) in self.browser.contents)
        self.assertTrue(
            'Then enter your new student credentials: user name= my id,'
            ' password = %s.' % self.applicant.application_number
            in self.browser.contents)
        return

    def image_url(self, filename):
        return self.edit_path.replace('edit', filename)

    def test_after_login_default_browsable(self):
        # After login we see the placeholder image in the edit view
        self.login()
        self.assertEqual(self.browser.url, self.view_path)
        self.browser.open(self.edit_path)
        # There is a correct <img> link included
        self.assertTrue(
              '<img src="passport.jpg" height="180px" />' in self.browser.contents)
        # Browsing the link shows a real image
        self.browser.open(self.image_url('passport.jpg'))
        self.assertEqual(
            self.browser.headers['content-type'], 'image/jpeg')
        self.assertEqual(len(self.browser.contents), PH_LEN)

    def test_after_submit_default_browsable(self):
        # After submitting an applicant form the default image is
        # still visible
        self.login()
        self.browser.open(self.edit_path)
        self.browser.getControl("Save").click() # submit form
        # There is a correct <img> link included
        self.assertTrue(
            '<img src="passport.jpg" height="180px" />' in self.browser.contents)
        # Browsing the link shows a real image
        self.browser.open(self.image_url('passport.jpg'))
        self.assertEqual(
            self.browser.headers['content-type'], 'image/jpeg')
        self.assertEqual(len(self.browser.contents), PH_LEN)

    def test_uploaded_image_respects_file_size_restriction(self):
        # When we upload an image that is too big ( > 10 KB) we will
        # get an error message
        self.login()
        self.browser.open(self.edit_path)
        # Create a pseudo image file and select it to be uploaded in form
        photo_content = 'A' * 1024 * 51  # A string of 11 KB size
        pseudo_image = StringIO(photo_content)
        ctrl = self.browser.getControl(name='form.passport')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(pseudo_image, filename='myphoto.jpg')
        self.browser.getControl("Save").click() # submit form
        # There is a correct <img> link included
        self.assertTrue(
            '<img src="passport.jpg" height="180px" />' in self.browser.contents)
        # We get a warning message
        self.assertTrue(
            'Uploaded image is too big' in self.browser.contents)
        # Browsing the image gives us the default image, not the
        # uploaded one.
        self.browser.open(self.image_url('passport.jpg'))
        self.assertEqual(
            self.browser.headers['content-type'], 'image/jpeg')
        self.assertEqual(len(self.browser.contents), PH_LEN)
        # There is really no file stored for the applicant
        img = getUtility(IExtFileStore).getFile(
            IFileStoreNameChooser(self.applicant).chooseName())
        self.assertTrue(img is None)

    def test_uploaded_image_browsable_w_errors(self):
        # We can upload a different image and browse it after submit,
        # even if there are still errors in the form
        self.login()
        self.browser.open(self.edit_path)
        # Create a pseudo image file and select it to be uploaded in form
        photo_content = 'I pretend to be a graphics file'
        pseudo_image = StringIO(photo_content)
        ctrl = self.browser.getControl(name='form.passport')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(pseudo_image, filename='myphoto.jpg')
        self.browser.getControl("Save").click() # submit form
        # There is a correct <img> link included
        self.assertTrue(
            '<img src="passport.jpg" height="180px" />' in self.browser.contents)
        # Browsing the link shows a real image
        self.browser.open(self.image_url('passport.jpg'))
        self.assertEqual(
            self.browser.headers['content-type'], 'image/jpeg')
        self.assertEqual(self.browser.contents, photo_content)

    def test_uploaded_image_stored_in_imagestorage_w_errors(self):
        # After uploading a new passport pic the file is correctly
        # stored in an imagestorage
        self.login()
        self.browser.open(self.edit_path)
        # Create a pseudo image file and select it to be uploaded in form
        pseudo_image = StringIO('I pretend to be a graphics file')
        ctrl = self.browser.getControl(name='form.passport')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(pseudo_image, filename='myphoto.jpg')
        self.browser.getControl("Save").click() # submit form
        storage = getUtility(IExtFileStore)
        file_id = IFileStoreNameChooser(self.applicant).chooseName()
        pseudo_image.seek(0) # reset our file data source
        self.assertEqual(
            storage.getFile(file_id).read(), pseudo_image.read())
        return

    def test_uploaded_image_browsable_wo_errors(self):
        # We can upload a different image and browse it after submit,
        # if there are no errors in form
        self.login()
        self.browser.open(self.edit_path)
        self.fill_correct_values() # fill other fields with correct values
        # Create a pseudo image file and select it to be uploaded in form
        pseudo_image = StringIO('I pretend to be a graphics file')
        ctrl = self.browser.getControl(name='form.passport')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(pseudo_image, filename='myphoto.jpg')
        self.browser.getControl("Save").click() # submit form
        # There is a correct <img> link included
        self.assertTrue(
            '<img src="passport.jpg" height="180px" />' in self.browser.contents)
        # Browsing the link shows a real image
        self.browser.open(self.image_url('passport.jpg'))
        self.assertEqual(
            self.browser.headers['content-type'], 'image/jpeg')
        self.assertEqual(len(self.browser.contents), 31)

    def test_uploaded_image_stored_in_imagestorage_wo_errors(self):
        # After uploading a new passport pic the file is correctly
        # stored in an imagestorage if form contains no errors
        self.login()
        self.browser.open(self.edit_path)
        self.fill_correct_values() # fill other fields with correct values
        # Create a pseudo image file and select it to be uploaded in form
        pseudo_image = StringIO('I pretend to be a graphics file')
        ctrl = self.browser.getControl(name='form.passport')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(pseudo_image, filename='myphoto.jpg')
        self.browser.getControl("Save").click() # submit form
        storage = getUtility(IExtFileStore)
        file_id = IFileStoreNameChooser(self.applicant).chooseName()
        # The stored image can be fetched
        fd = storage.getFile(file_id)
        file_len = len(fd.read())
        self.assertEqual(file_len, 31)
        # When an applicant is removed, also the image is gone.
        del self.app['applicants'][container_name_1][self.applicant.application_number]
        fd = storage.getFile(file_id)
        self.assertTrue(fd is None)

    def test_uploaded_images_equal(self):
        # Make sure uploaded images do really differ if we eject a
        # change notfication (and do not if we don't)
        self.login()
        self.browser.open(self.edit_path)
        self.fill_correct_values() # fill other fields with correct values
        self.browser.getControl("Save").click() # submit form
        # Now go on as an officer
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.manage_path)

        # Create a pseudo image file and select it to be uploaded in form
        pseudo_image = StringIO('I pretend to be a graphics file')
        ctrl = self.browser.getControl(name='form.passport')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(pseudo_image, filename='myphoto.jpg')
        file_id = IFileStoreNameChooser(self.applicant).chooseName()
        setSite(self.app)
        passport0 = getUtility(IExtFileStore).getFile(file_id)
        self.browser.getControl("Save").click() # submit form with changed pic
        passport1 = getUtility(IExtFileStore).getFile(file_id).read()
        self.browser.getControl("Save").click() # submit form w/o changes
        passport2 = getUtility(IExtFileStore).getFile(file_id).read()
        self.assertTrue(passport0 is None)
        self.assertTrue(passport0 != passport1)
        self.assertTrue(passport1 == passport2)
        return

    def test_upload_image_by_manager_with_logging(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.manage_path)
        # Create a pseudo image file and select it to be uploaded in form
        photo_content = 'A' * 1024 * 5  # A string of 5 KB size
        pseudo_image = StringIO(photo_content)
        ctrl = self.browser.getControl(name='form.passport')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(pseudo_image, filename='myphoto.jpg')
        self.browser.getControl("Save").click() # submit form
        # Even though the form could not be saved ...
        self.assertTrue(
            'Required input is missing' in self.browser.contents)
        # ... the file has been successfully uploaded
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'applicants.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - applicants.browser.ApplicantManageFormPage - '
            '%s - saved: passport'
            % (self.applicant.applicant_id)
            in logcontent)

    def test_application_slip_with_non_jpg_image(self):
        IWorkflowState(self.applicant).setState('submitted')
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.manage_path)
        # Create a pseudo image file and select it to be uploaded in form
        photo_content = 'A' * 1024 * 5  # A string of 5 KB size
        pseudo_image = StringIO(photo_content)
        ctrl = self.browser.getControl(name='form.passport')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(pseudo_image, filename='myphoto.jpg')
        self.browser.getControl("Save").click() # submit form
        self.browser.open(self.view_path)
        self.browser.getLink("Download application slip").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertMatches(
            '...Your image file is corrupted. Please replace...',
            self.browser.contents)

    def test_pay_portal_application_fee(self):
        self.login()
        self.browser.open(self.edit_path)
        self.fill_correct_values()
        # We have to save the form otherwise the filled fields will be cleared
        # after adding an online payment, because adding an online payment
        # requires a filled form but does not save it
        self.browser.getControl("Save").click()
        # Payment section does not appear if application fee isn't set
        self.assertFalse('Payment Tickets' in self.browser.contents)
        self.assertFalse('Add online payment' in self.browser.contents)
        self.applicantscontainer.application_fee = 200.0
        self.browser.open(self.edit_path)
        self.browser.getControl("Add online payment ticket").click()
        self.browser.open(self.edit_path)
        self.browser.getControl("Add online payment ticket").click()
        self.assertMatches('...Payment ticket created...',
                           self.browser.contents)
        self.assertMatches('...Activation Code...',
                           self.browser.contents)
        self.assertTrue(
            '<span>200.0</span>' in self.browser.contents)
        # Payment ticket can be removed if they haven't received a
        # valid callback
        self.browser.open(self.edit_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        ctrl.getControl(value=value).selected = True
        self.browser.getControl("Remove selected", index=0).click()
        self.assertMatches('...Successfully removed...', self.browser.contents)
        # We will try the callback request view
        self.browser.getControl("Add online payment ticket").click()
        self.browser.open(self.edit_path)
        ctrl = self.browser.getControl(name='val_id')
        value = ctrl.options[0]
        self.browser.getLink(value).click()
        self.assertMatches('...Amount Authorized...',
                           self.browser.contents)
        payment_url = self.browser.url
        payment_id = self.applicant.keys()[0]
        payment = self.applicant[payment_id]
        self.assertEqual(payment.p_item,'This is the %s container' % container_name_1)
        self.assertEqual(payment.p_session, session_1)
        self.assertEqual(payment.p_category,'application')
        self.assertEqual(payment.amount_auth,200.0)
        # Applicant is payer of the payment ticket.
        self.assertEqual(IPayer(payment).payer, self.applicant)
        self.assertEqual(
            IPayer(payment).display_fullname, 'John Anthony Tester')
        self.assertEqual(
            IPayer(payment).id, self.applicant.applicant_id)
        self.assertEqual(IPayer(payment).faculty, 'N/A')
        self.assertEqual(IPayer(payment).department, 'N/A')
        # The pdf payment slip can't yet be opened
        #self.browser.open(payment_url + '/payment_receipt.pdf')
        #self.assertMatches('...Ticket not yet paid...',
        #                   self.browser.contents)
        # Approve payment
        # Applicants can't approve payments
        self.assertRaises(
            Unauthorized, self.browser.open, payment_url + '/approve')
        # We approve the payment by bypassing the view
        payment.approve()
        # Applicant is is not yet in state 'paid' because it was only
        # the payment which we set to paid
        self.browser.open(self.view_path)
        self.assertMatches('...started...',
                           self.browser.contents)
        self.assertTrue(self.applicant.state == 'started')
        # Let's logout and approve the payment as manager
        self.browser.getLink("Logout").click()
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        # First we reset the payment
        payment.r_amount_approved = 0.0
        payment.r_code = u''
        payment.p_state = 'unpaid'
        payment.r_desc = u''
        payment.payment_date = None
        self.browser.open(payment_url)
        self.browser.getLink("Approve payment").click()
        self.assertEqual(payment.p_state, 'paid')
        self.assertEqual(payment.r_amount_approved, 200.0)
        self.assertEqual(payment.r_code, 'AP')
        self.assertTrue(self.applicant.state == 'paid')
        # Approval is logged in students.log ...
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'applicants.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - applicants.browser.OnlinePaymentApprovePage - '
            '%s - approved' % self.applicant.applicant_id
            in logcontent)
        # ... and in payments.log
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'payments.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            '"zope.mgr",%s,%s,application,200.0,AP,,,,,,\n'
            % (self.applicant.applicant_id, payment.p_id)
            in logcontent)
        # Payment slips can't be downloaded ...
        payment_id = self.applicant.keys()[0]
        self.browser.open(self.view_path + '/' + payment_id)
        self.browser.getLink("Download payment slip").click()
        self.assertTrue(
            'Please submit the application form before trying to download payment slips.'
            in self.browser.contents)
        # ... unless form is submitted.
        self.browser.open(self.view_path + '/edit')
        image = open(SAMPLE_IMAGE, 'rb')
        ctrl = self.browser.getControl(name='form.passport')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(image, filename='myphoto.jpg')
        self.browser.getControl(name="confirm_passport").value = True
        self.browser.getControl("Finally Submit").click()
        self.browser.open(self.view_path + '/' + payment_id)
        self.browser.getLink("Download payment slip").click()
        self.assertEqual(self.browser.headers['Content-Type'],
                 'application/pdf')
        return

    # It was only enabled during implementation of balance payments
    def disabled_test_pay_balance(self):
        # Managers can make balance payment
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.manage_path)
        self.fill_correct_values()
        self.browser.getControl("Save").click()
        self.browser.open(self.view_path + '/addbp')
        self.browser.getControl(name="form.p_category").value = ['donation']
        self.browser.getControl(name="form.balance_amount").value = '10000'
        self.browser.getControl("Create ticket").click()
        self.assertTrue('Wrong state' in self.browser.contents)
        IWorkflowState(self.applicant).setState('submitted')
        self.browser.getControl("Create ticket").click()
        self.assertTrue('Payment ticket created.' in self.browser.contents)
        self.browser.getLink("Approve payment").click()
        self.assertTrue('Payment approved' in self.browser.contents)
        return

    def prepare_special_container(self):
        # Add special application container
        container_name = u'special%s' % session_1
        applicantscontainer = ApplicantsContainer()
        applicantscontainer.code = container_name
        applicantscontainer.prefix = 'special'
        applicantscontainer.year = session_1
        applicantscontainer.title = u'This is a special app container'
        applicantscontainer.application_category = 'no'
        applicantscontainer.mode = 'create'
        applicantscontainer.strict_deadline = True
        delta = timedelta(days=10)
        applicantscontainer.startdate = datetime.now(pytz.utc) - delta
        applicantscontainer.enddate = datetime.now(pytz.utc) + delta
        self.app['applicants'][container_name] = applicantscontainer
        # Add an applicant
        applicant = createObject('waeup.Applicant')
        # reg_number is the only field which has to be preset here
        # because managers are allowed to edit this required field
        applicant.reg_number = u'12345'
        self.special_applicant = applicant
        self.app['applicants'][container_name].addApplicant(applicant)
        IUserAccount(
            self.app['applicants'][container_name][
            applicant.application_number]).setPassword('apwd')
        # Add session configuration object
        self.configuration = SessionConfiguration()
        self.configuration.academic_session = session_1
        #self.configuration.transcript_fee = 200.0
        self.configuration.clearance_fee = 300.0
        self.app['configuration'].addSessionConfiguration(self.configuration)

    def test_pay_special_fee(self):
        self.prepare_special_container()
        # Login
        self.browser.open(self.login_path)
        self.browser.getControl(
            name="form.login").value = self.special_applicant.applicant_id
        self.browser.getControl(name="form.password").value = 'apwd'
        self.browser.getControl("Login").click()
        applicant_path = self.browser.url
        self.browser.getLink("Edit application record").click()
        self.browser.getControl(name="form.firstname").value = 'John'
        self.browser.getControl(name="form.middlename").value = 'Anthony'
        self.browser.getControl(name="form.lastname").value = 'Tester'
        self.browser.getControl(name="form.special_application").value = [
            'transcript']
        self.browser.getControl(name="form.date_of_birth").value = '09/09/1988'
        self.browser.getControl(name="form.email").value = 'xx@yy.zz'
        self.configuration.transcript_fee = 0.0
        self.browser.getControl("Save").click()
        self.browser.getControl("Add online payment ticket").click()
        self.assertMatches('...Amount could not be determined...',
                           self.browser.contents)
        self.configuration.transcript_fee = 200.0
        self.browser.getLink("Edit application record").click()
        self.browser.getControl("Add online payment ticket").click()
        self.assertMatches('...Payment ticket created...',
                           self.browser.contents)
        self.assertTrue(
            '<span>Transcript Fee</span>' in self.browser.contents)
        self.assertTrue(
            'This is a special app container' in self.browser.contents)
        self.assertTrue(
            '<span>200.0</span>' in self.browser.contents)
        self.assertEqual(len(self.special_applicant.keys()), 1)
        # The applicant's workflow state is paid ...
        self.special_applicant.payments[0].approveApplicantPayment()
        self.assertEqual(self.special_applicant.state, 'paid')
        self.browser.open(applicant_path + '/edit')
        # ... but he can create further tickets.
        self.browser.getControl(name="form.special_application").value = [
            'clearance']
        self.browser.getControl("Save").click()
        self.browser.getControl("Add online payment ticket").click()
        self.assertMatches('...Payment ticket created...',
                           self.browser.contents)
        self.browser.open(applicant_path)
        self.assertTrue(
            '<td>Acceptance Fee</td>' in self.browser.contents)
        self.assertEqual(len(self.special_applicant.keys()), 2)
        # Second payment can also be approved wthout error message
        flashtype, msg, log = self.special_applicant.payments[1].approveApplicantPayment()
        self.assertEqual(flashtype, 'success')
        self.assertEqual(msg, 'Payment approved')
        # Payment slips can't be downloaded ...
        payment_id = self.special_applicant.keys()[0]
        self.browser.open(applicant_path + '/' + payment_id)
        self.browser.getLink("Download payment slip").click()
        self.assertTrue(
            'Please submit the application form before trying to download payment slips.'
            in self.browser.contents)
        # ... unless form is submitted.
        self.browser.open(applicant_path + '/edit')
        image = open(SAMPLE_IMAGE, 'rb')
        ctrl = self.browser.getControl(name='form.passport')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(image, filename='myphoto.jpg')
        self.browser.getControl(name="confirm_passport").value = True
        self.browser.getControl("Finally Submit").click()
        self.browser.open(applicant_path + '/' + payment_id)
        self.browser.getLink("Download payment slip").click()
        self.assertEqual(self.browser.headers['Content-Type'],
                 'application/pdf')
        return

    def test_final_submit(self):
        # Make sure that a correctly filled form with passport picture
        # can be submitted (only) after payment
        self.login()
        self.browser.getLink("Edit application record").click()
        self.assertFalse('Finally Submit' in self.browser.contents)
        IWorkflowInfo(self.applicant).fireTransition('pay')
        self.browser.open(self.edit_path)
        self.assertTrue('Finally Submit' in self.browser.contents)
        self.fill_correct_values() # fill other fields with correct values
        self.browser.getControl("Save").click()
        self.browser.getControl("Finally Submit").click()
        # We forgot to upload a passport picture
        self.assertTrue(
            'No passport picture uploaded' in self.browser.contents)
        # Use a real image file and select it to be uploaded in form
        image = open(SAMPLE_IMAGE, 'rb')
        ctrl = self.browser.getControl(name='form.passport')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(image, filename='myphoto.jpg')
        self.browser.getControl("Finally Submit").click() # (finally) submit form
        # The picture has been uploaded but the form cannot be submitted
        # since the passport confirmation box was not ticked
        self.assertTrue(
            'Passport picture confirmation box not ticked'
            in self.browser.contents)
        self.browser.getControl(name="confirm_passport").value = True
        # If application period has expired and strict-deadline is set
        # applicants do notsee edit button and can't open
        # the edit form.
        self.applicantscontainer.enddate = datetime.now(pytz.utc)
        self.browser.open(self.view_path)
        self.assertFalse(
            'Edit application record' in self.browser.contents)
        self.browser.open(self.edit_path)
        self.assertTrue(
            'form is locked' in self.browser.contents)
        # We can either postpone the enddate ...
        self.applicantscontainer.enddate = datetime.now(
            pytz.utc) + timedelta(days=10)
        self.browser.open(self.edit_path)
        self.browser.getControl(name="confirm_passport").value = True
        self.browser.getControl("Finally Submit").click()
        self.assertTrue(
            'Application submitted' in self.browser.contents)
        # ... or allow submission after deadline.
        IWorkflowState(self.applicant).setState('paid')
        self.applicant.locked = False
        self.applicantscontainer.strict_deadline = False
        self.browser.open(self.edit_path)
        self.browser.getControl(name="confirm_passport").value = True
        self.browser.getControl("Finally Submit").click()
        self.assertTrue(
            'Application submitted' in self.browser.contents)
        return

    def test_locking(self):
        # Make sure that locked forms can't be submitted
        self.login()
        self.browser.open(self.edit_path)
        self.fill_correct_values() # fill other fields with correct values
        # Create a pseudo image file and select it to be uploaded in form
        pseudo_image = StringIO('I pretend to be a graphics file')
        ctrl = self.browser.getControl(name='form.passport')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(pseudo_image, filename='myphoto.jpg')
        self.browser.getControl("Save").click()
        # Now we lock the form
        self.applicant.locked = True
        self.browser.open(self.edit_path)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertTrue(
            'The requested form is locked' in self.browser.contents)
        return

    def test_certificate_removed(self):
        self.login()
        self.browser.open(self.edit_path)
        self.fill_correct_values()
        self.browser.getControl("Save").click()
        self.browser.open(self.view_path)
        self.assertTrue(
            'Unnamed Certificate' in self.browser.contents)
        self.browser.open(self.edit_path)
        self.assertTrue(
            '<option selected="selected" value="CERT1">' in self.browser.contents)
        # Now we remove the certificate
        del self.app['faculties']['fac1']['dep1'].certificates['CERT1']
        # The certificate is still shown in display mode
        self.browser.open(self.view_path)
        self.assertTrue(
            'Unnamed Certificate' in self.browser.contents)
        # The certificate is still selectable in edit mode so that it won't
        # be automatically replaced by another (arbitrary) certificate
        self.browser.open(self.edit_path)
        self.assertTrue(
            '<option selected="selected" value="CERT1">' in self.browser.contents)
        # Consequently, the certificate is still shown after saving the form
        self.browser.getControl("Save").click()
        self.browser.open(self.view_path)
        self.assertTrue(
            'Unnamed Certificate' in self.browser.contents)
        # Even if we add a new certificate the previous (removed)
        # certificate is shown
        certificate = createObject('waeup.Certificate')
        certificate.code = 'CERT2'
        certificate.title = 'New Certificate'
        certificate.application_category = 'basic'
        self.app['faculties']['fac1']['dep1'].certificates.addCertificate(
            certificate)
        self.browser.open(self.edit_path)
        self.assertTrue(
            '<option selected="selected" value="CERT1">'
            in self.browser.contents)

    def test_upload_testfile(self):
        self.login()
        self.browser.open(self.edit_path)
        self.fill_correct_values() # fill other fields with correct values       
        # Create a pseudo file with acceptable size
        pdf_content = 'A' * 1024 * 300  # A string of 300 KB size
        pseudo_pdf = StringIO(pdf_content)
        ctrl = self.browser.getControl(name='testfile')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(pseudo_pdf, filename='my_file.pdf')
        self.browser.getControl("Save").click() # submit form
        self.assertTrue('Uploaded file is too big!'
            in self.browser.contents)
        #pdf_content = 'A' * 1024 * 200  # A string of 300 KB size
        #pseudo_pdf = StringIO(pdf_content)
        image = open(SAMPLE_IMAGE, 'rb')
        ctrl = self.browser.getControl(name='testfile')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(image, filename='my_scan.jpg')
        self.browser.getControl("Save").click() # submit form
        # The file has been successfully uploaded
        self.assertTrue('Form has been saved.' in self.browser.contents)
        # There is really a file stored for the applicant
        storage = getUtility(IExtFileStore)
        file_id = IFileStoreNameChooser(self.applicant).chooseName(
            attr='testfile.jpg')
        # The stored file can be fetched
        fd = storage.getFile(file_id)
        file_len = len(fd.read())
        self.assertEqual(file_len, 2787)
        # A file link is displayed on the edit view ...
        self.browser.open(self.edit_path)
        self.assertTrue('<a href="testfile">' in self.browser.contents)
        # ... and on the dislay view
        self.browser.open(self.view_path)
        self.assertTrue('testfile">Test File</a>'
            in self.browser.contents)
        # Adding file is properly logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'applicants.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            '%s - applicants.browser.ApplicantEditFormPage'
            ' - %s - saved: testfile'
            % (self.applicant.applicant_id, self.applicant.applicant_id)
            in logcontent)
        # When an applicant is removed, also the files are gone.
        del self.applicantscontainer[self.applicant.application_number]
        fd = storage.getFile(file_id)
        self.assertTrue(fd is None)
        return

    def test_manage_contact_applicant(self):
        # Managers can contact student
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        # Remove required FieldProperty attribute first ...
        delattr(Applicant, 'email')
        # ... and replace by None
        self.applicant.email = None
        # Now we have to add  the FieldProperty attribute again. Otherwise
        # many other tests below will fail.
        iface = list(implementedBy(Applicant))[0]
        field_property = FieldProperty(iface['email'])
        setattr(Applicant, 'email', field_property)
        self.browser.open(self.view_path)
        self.browser.getLink("Send email").click()
        self.browser.getControl(
            name="form.subject").value = 'Important subject'
        self.browser.getControl(name="form.body").value = 'Hello!'
        self.browser.getControl("Send message now").click()
        self.assertTrue(
            'An smtp server error occurred' in self.browser.contents)
        self.applicant.email = 'xx@yy.zz'
        self.browser.getControl("Send message now").click()
        self.assertTrue('Your message has been sent' in self.browser.contents)
        self.assertMatches(
            'Sending email from no-reply@waeup.org to xx@yy.zz:'
            '\nMessage:'
            '\nmsg: MIME-Version: 1.0'
            '\nmsg: Content-Type: text/plain; charset="us-ascii"'
            '\nmsg: Content-Transfer-Encoding: 7bit'
            '\nmsg: From: Manager <no-reply@waeup.org>'
            '\nmsg: To: Joan None <xx@yy.zz>'
            '\nmsg: Reply-To: Manager <contact@waeup.org>'
            '\nmsg: Subject: Important subject'
            '\nmsg:'
            '\nmsg: Hello!'
            '\nmsg:'
            '\nmsg: ---'
            '\nmsg: Manager (id: zope.mgr)'
            '\nmsg: Sample University'
            '\nmsg:',
            self.get_fake_smtp_output()
            )
        return

    def test_create_student(self):
        # Managers can contact student
        IWorkflowState(self.applicant).setState('admitted')
        self.applicant.certificate = self.certificate
        self.applicant.course_admitted = self.certificate
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.manage_path)
        self.fill_correct_values() 
        image = open(SAMPLE_IMAGE, 'rb')
        ctrl = self.browser.getControl(name='form.passport')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(image, filename='myphoto.jpg')
        self.browser.getControl("Save").click()
        self.browser.open(self.view_path)
        self.browser.getLink("Create student").click()
        self.assertTrue('Student K1000000 created' in self.browser.contents)
        self.assertMatches(
            'Sending email from no-reply@waeup.org to xx@yy.zz:'
            '\nMessage:'
            '\nmsg: MIME-Version: 1.0'
            '\nmsg: Content-Type: text/plain; charset="us-ascii"'
            '\nmsg: Content-Transfer-Encoding: 7bit'
            '\nmsg: From: Administrator <no-reply@waeup.org>'
            '\nmsg: To: John Anthony Tester <xx@yy.zz>'
            '\nmsg: Reply-To: Administrator <contact@waeup.org>'
            '\nmsg: Subject: Your new Kofa student account'
            '\nmsg:'
            '\nmsg: Dear John Anthony Tester,'
            '\nmsg:'
            '\nmsg: Your student record of the Student Registration and Information Portal of'
            '\nmsg: Sample University has been created for you.'
            '\nmsg:'
            '\nmsg: Your user name: K1000000'
            '\nmsg: Your password: %s'
            '\nmsg: Login: http://localhost/app/login?login=K1000000&password=%s'
            '\nmsg:'
            '\nmsg: Or request a new secure password here: http://localhost/app/changepw'
            '\nmsg:'
            '\nmsg: Regards'
            '\nmsg:' % (self.applicant.application_number, self.applicant.application_number),
            self.get_fake_smtp_output()
            )
        return

class ApplicantRegisterTests(ApplicantsFullSetup):
    # Tests for applicant registration

    layer = FunctionalLayer

    def test_register_applicant_create(self):
        config = grok.getSite()['configuration']
        config.maintmode_enabled_by = u'any_user'
        self.assertEqual(len(self.app['applicants'][container_name_1]), 1)
        # An applicant can register himself.
        self.browser.open(self.container_path)
        self.browser.getLink("Register for application").click()
        self.assertTrue(
            'The portal is in maintenance mode' in self.browser.contents)
        config.maintmode_enabled_by = None
        self.browser.getLink("Register for application").click()
        # The edit form now opens and can be filled with suitable values
        self.browser.getControl(name="form.firstname").value = 'Anna'
        self.browser.getControl(name="form.lastname").value = 'Kurios'
        self.browser.getControl(name="form.email").value = 'xx@yy.zz'
        self.browser.getControl(name="form.phone.country").value = ['+234']
        self.browser.getControl(name="form.phone.area").value = '555'
        self.browser.getControl(name="form.phone.ext").value = '6666666'
        self.browser.getControl("Send login credentials").click()
        self.assertEqual(self.browser.url,
            self.container_path + '/registration_complete?email=xx%40yy.zz')
        # A new applicant has been created
        self.assertEqual(len(self.app['applicants'][container_name_1]), 2)
        # The new applicant can be found in the catalog via the email address
        cat = getUtility(ICatalog, name='applicants_catalog')
        results = list(
            cat.searchResults(email=('xx@yy.zz', 'xx@yy.zz')))
        applicant = results[0]
        self.assertEqual(applicant.lastname,'Kurios')
        # The application_id has been copied to the reg_number
        #self.assertEqual(applicant.applicant_id, applicant.reg_number)
        # The applicant can be found in the catalog via the reg_number
        #results = list(
        #    cat.searchResults(
        #    reg_number=(applicant.reg_number, applicant.reg_number)))
        #self.assertEqual(applicant,results[0])
        return

    def test_register_applicant_take_unused_record(self):
        # Create an unused record
        uu_applicant = createObject('waeup.Applicant')
        self.app['applicants'][container_name_1].addApplicant(uu_applicant)
        self.assertEqual(uu_applicant.container_code, container_name_1 + '-')
        self.assertEqual(len(self.app['applicants'][container_name_1]), 2)
        self.browser.open(self.container_path)
        self.browser.getLink("Register for application").click()
        # Fill the edit form with suitable values
        self.browser.getControl(name="form.firstname").value = 'Anna'
        self.browser.getControl(name="form.lastname").value = 'Kurios'
        self.browser.getControl(name="form.email").value = 'xx@yy.zz'
        self.browser.getControl(name="form.phone.country").value = ['+234']
        self.browser.getControl(name="form.phone.area").value = '555'
        self.browser.getControl(name="form.phone.ext").value = '6666666'
        self.browser.getControl("Send login credentials").click()
        # No applicant has been created ...
        self.assertEqual(len(self.app['applicants'][container_name_1]), 2)
        # ... and the existing, formerly unused record has been used instead
        self.assertEqual(uu_applicant.lastname, 'Kurios')
        self.assertEqual(uu_applicant.container_code, container_name_1 + '+')
        return

    def test_register_applicant_update(self):
        # We change the application mode and check if applicants
        # can find and update imported records instead of creating new records.
        # First we check what happens if record does not exist.
        self.applicantscontainer.mode = 'update'
        self.browser.open(self.container_path + '/register')
        self.browser.getControl(name="form.lastname").value = 'Better'
        self.browser.getControl(name="form.reg_number").value = 'anynumber'
        self.browser.getControl(name="form.email").value = 'xx@yy.zz'
        self.browser.getControl("Send login credentials").click()
        self.assertTrue('No application record found.'
            in self.browser.contents)
        # Even with the correct reg_number we can't register
        # because lastname attribute is not set.
        self.applicantscontainer.mode = 'update'
        self.browser.open(self.container_path + '/register')
        self.browser.getControl(name="form.lastname").value = 'Better'
        self.browser.getControl(name="form.reg_number").value = '1234'
        self.browser.getControl(name="form.email").value = 'xx@yy.zz'
        self.browser.getControl("Send login credentials").click()
        self.assertTrue('An error occurred.' in self.browser.contents)
        # Let's set this attribute manually
        # and try to register with a wrong name.
        self.applicant.lastname = u'Better'
        self.browser.open(self.container_path + '/register')
        self.browser.getControl(name="form.lastname").value = 'Worse'
        self.browser.getControl(name="form.reg_number").value = '1234'
        self.browser.getControl(name="form.email").value = 'xx@yy.zz'
        self.browser.getControl("Send login credentials").click()
        # Anonymous is not informed that lastname verification failed.
        # It seems that the record doesn't exist.
        self.assertTrue('No application record found.'
            in self.browser.contents)
        # Even with the correct lastname we can't register if a
        # password has been set and used.
        IWorkflowState(self.applicant).setState('started')
        self.browser.getControl(name="form.lastname").value = 'Better'
        self.browser.getControl(name="form.reg_number").value = '1234'
        self.browser.getControl("Send login credentials").click()
        self.assertTrue('Your password has already been set and used.'
            in self.browser.contents)
        #IUserAccount(
        #    self.app['applicants'][container_name_1][
        #    self.applicant.application_number]).context.password = None
        # Even without unsetting the password we can re-register if state
        # is 'initialized'
        IWorkflowState(self.applicant).setState('initialized')
        self.browser.open(self.container_path + '/register')
        # The lastname field, used for verification, is not case-sensitive.
        self.browser.getControl(name="form.lastname").value = 'bEtter'
        self.browser.getControl(name="form.reg_number").value = '1234'
        self.browser.getControl(name="form.email").value = 'new@yy.zz'
        self.browser.getControl("Send login credentials").click()
        # Yeah, we succeded ...
        self.assertTrue('Your registration was successful.'
            in self.browser.contents)
        # ... and  applicant can be found in the catalog via the email address
        cat = getUtility(ICatalog, name='applicants_catalog')
        results = list(
            cat.searchResults(
            email=('new@yy.zz', 'new@yy.zz')))
        self.assertEqual(self.applicant,results[0])
        return

    def test_change_password_request(self):
        self.browser.open('http://localhost/app/changepw')
        self.browser.getControl(name="form.identifier").value = '1234'
        self.browser.getControl(name="form.email").value = 'aa@aa.ng'
        self.browser.getControl("Send login credentials").click()
        self.assertTrue('No record found' in self.browser.contents)
        self.applicant.email = 'aa@aa.ng'
        # Update the catalog
        notify(grok.ObjectModifiedEvent(self.applicant))
        self.browser.open('http://localhost/app/changepw')
        self.browser.getControl(name="form.identifier").value = '1234'
        self.browser.getControl(name="form.email").value = 'aa@aa.ng'
        self.browser.getControl("Send login credentials").click()
        self.assertTrue(
            'An email with your user name and password has been sent'
            in self.browser.contents)

    def test_check_status(self):
        self.applicant.lastname = u'Lion '
        self.browser.open('http://localhost/app/applicants/checkstatus')
        self.browser.getControl(name="unique_id").value = 'nonsense'
        self.browser.getControl(name="lastname").value = 'Lion'
        self.browser.getControl("Submit").click()
        self.assertTrue('No application record found' in self.browser.contents)
        self.browser.getControl(
          name="unique_id").value = self.applicant.applicant_id
        self.browser.getControl(name="lastname").value = 'nonsense'
        self.browser.getControl("Submit").click()
        self.assertTrue('No application record found' in self.browser.contents)
        self.browser.getControl(
          name="unique_id").value = self.applicant.applicant_id
        self.browser.getControl(name="lastname").value = 'Lion'
        self.browser.getControl("Submit").click()
        self.assertTrue('Admission status of' in self.browser.contents)
        self.assertTrue(
          'You have not yet submitted your application' in self.browser.contents)
        IWorkflowState(self.applicant).setState('admitted')
        self.browser.open('http://localhost/app/applicants/checkstatus')
        self.browser.getControl(
          name="unique_id").value = self.applicant.applicant_id
        # Whitespaces are ignored.
        self.browser.getControl(name="lastname").value = 'Lion'
        self.browser.getControl("Submit").click()
        self.assertTrue('Congratulations!' in self.browser.contents)
        self.assertFalse('Study Course' in self.browser.contents)
        self.applicant.course_admitted = self.certificate
        self.browser.open('http://localhost/app/applicants/checkstatus')
        self.browser.getControl(
          name="unique_id").value = self.applicant.applicant_id
        self.browser.getControl(name="lastname").value = 'Lion'
        self.browser.getControl("Submit").click()
        self.assertTrue('Congratulations!' in self.browser.contents)
        self.assertTrue('Unnamed Certificate (CERT1)' in self.browser.contents)
        self.assertTrue(
          'Department of Unnamed Department (dep1)' in self.browser.contents)
        self.assertTrue(
          'Faculty of Unnamed Faculty (NA)' in self.browser.contents)
        # Also the reg_number can be used and page shows student id and password
        # if applicant is in state created.
        IWorkflowState(self.applicant).setState('created')
        self.applicant.student_id = u'my id'
        self.browser.open('http://localhost/app/applicants/checkstatus')
        self.browser.getControl(
          name="unique_id").value = self.applicant.reg_number
        self.browser.getControl(name="lastname").value = 'Lion'
        self.browser.getControl("Submit").click()
        self.assertTrue('Congratulations!' in self.browser.contents)
        self.assertTrue('Unnamed Certificate (CERT1)' in self.browser.contents)
        self.assertTrue('Department of Unnamed Department (dep1)'
            in self.browser.contents)
        self.assertTrue(
          'Faculty of Unnamed Faculty (NA)' in self.browser.contents)
        self.assertTrue('user name (= student id) is: <strong>my id</strong>'
            in self.browser.contents)
        self.assertTrue(
          'password is: <strong>%s</strong>' % self.applicant.application_number
          in self.browser.contents)

    def test_check_transcript_status(self):
        self.applicant.email = 'aa@aa.aa'
        self.browser.open('http://localhost/app/applicants/checktranscript')
        self.browser.getControl(name="unique_id").value = 'nonsense'
        self.browser.getControl(name="email").value = 'aa@aa.aa'
        self.browser.getControl("Check status now").click()
        self.assertTrue('No student record was found in Kofa'
            in self.browser.contents)

class ApplicantsExportTests(ApplicantsFullSetup, FunctionalAsyncTestCase):
    # Tests for StudentsContainer class views and pages

    layer = FunctionalLayer

    def wait_for_export_jobs_completed(self):
        # helper function waiting until the current export job is completed
        manager = getUtility(IJobManager)
        job_ids = [i[0] for i in self.app['datacenter'].running_exports]
        jobs = [manager.get(job_id) for job_id in job_ids]
        for job in jobs:
            wait_for_result(job)
        return job_ids

    def test_applicants_in_container_export(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        container_path = 'http://localhost/app/applicants/%s' % container_name_1
        self.browser.open(container_path)
        self.browser.getLink("Export application data").click()
        self.browser.getControl("Start new exports").click()
        job_ids = self.wait_for_export_jobs_completed()
        # Three exports were created
        self.assertEqual(len(self.app['datacenter'].running_exports), 3)
       # When the jobs are finished and we reload the page...
        self.browser.open(container_path + '/exports')
        # ... the both csv files can be downloaded ...
        self.browser.getLink("Download", index=0).click()
        self.assertEqual(self.browser.headers['content-type'],
            'text/csv; charset=UTF-8')
        self.assertTrue(
            'filename="WAeUP.Kofa_applicants_%s.csv' % job_ids[0] in
            self.browser.headers['content-disposition'])
        self.browser.open(container_path + '/exports')
        self.browser.getLink("Download", index=1).click()
        self.assertEqual(self.browser.headers['content-type'],
            'text/csv; charset=UTF-8')
        self.assertTrue(
            'filename="WAeUP.Kofa_applicantpayments_%s.csv' % job_ids[1] in
            self.browser.headers['content-disposition'])
        self.browser.open(container_path + '/exports')
        self.browser.getLink("Download", index=2).click()
        self.assertEqual(self.browser.headers['content-type'],
            'text/csv; charset=UTF-8')
        self.assertTrue(
            'filename="WAeUP.Kofa_applicantrefereereports_%s.csv' % job_ids[2] in
            self.browser.headers['content-disposition'])
        # ... and discarded
        self.browser.open(container_path + '/exports')
        self.browser.getControl("Discard", index=0).click()
        self.assertEqual(len(self.app['datacenter'].running_exports), 2)
        self.browser.getControl("Discard", index=0).click()
        self.assertEqual(len(self.app['datacenter'].running_exports), 1)
        self.browser.getControl("Discard").click()
        self.assertEqual(len(self.app['datacenter'].running_exports), 0)
        # Creation, downloading and discarding are logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'datacenter.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - applicants.browser.ExportJobContainerJobStart - '
            'exported: applicants (%s), job_id=%s'
            % (container_name_1, job_ids[0]) in logcontent
            )
        self.assertTrue(
            'zope.mgr - applicants.browser.ExportJobContainerDownload '
            '- downloaded: WAeUP.Kofa_applicants_%s.csv, job_id=%s'
            % (job_ids[0], job_ids[0]) in logcontent
            )
        self.assertTrue(
            'zope.mgr - applicants.browser.ExportJobContainerOverview '
            '- discarded: job_id=%s' % job_ids[0] in logcontent
            )
        self.assertTrue(
            'zope.mgr - applicants.browser.ExportJobContainerJobStart - '
            'exported: applicantpayments (%s), job_id=%s'
            % (container_name_1, job_ids[1]) in logcontent
            )
        self.assertTrue(
            'zope.mgr - applicants.browser.ExportJobContainerDownload '
            '- downloaded: WAeUP.Kofa_applicantpayments_%s.csv, job_id=%s'
            % (job_ids[1], job_ids[1]) in logcontent
            )
        self.assertTrue(
            'zope.mgr - applicants.browser.ExportJobContainerOverview '
            '- discarded: job_id=%s' % job_ids[1] in logcontent
            )
        self.assertTrue(
            'zope.mgr - applicants.browser.ExportJobContainerJobStart - '
            'exported: applicantrefereereports (%s), job_id=%s'
            % (container_name_1, job_ids[2]) in logcontent
            )
        self.assertTrue(
            'zope.mgr - applicants.browser.ExportJobContainerDownload '
            '- downloaded: WAeUP.Kofa_applicantrefereereports_%s.csv, job_id=%s'
            % (job_ids[2], job_ids[2]) in logcontent
            )
        self.assertTrue(
            'zope.mgr - applicants.browser.ExportJobContainerOverview '
            '- discarded: job_id=%s' % job_ids[2] in logcontent
            )

class ApplicantRefereeReportTests(ApplicantsFullSetup, FunctionalAsyncTestCase):
    # Tests for ApplicantRefereeReport class views and pages

    layer = FunctionalLayer

    def setUp(self):
        super(ApplicantRefereeReportTests, self).setUp()
        self.setup_logging()
        return

    def tearDown(self):
        super(ApplicantRefereeReportTests, self).tearDown()
        self.teardown_logging()
        return

    def setup_logging(self):
        # setup a log-handler that catches all fake mailer output
        self.stream = StringIO()
        handler = logging.StreamHandler(self.stream)
        logger = logging.getLogger('test.smtp')
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return

    def get_fake_smtp_output(self):
        # get output generated by fake mailer
        self.stream.flush()
        self.stream.seek(0)
        return self.stream.read()

    def teardown_logging(self):
        # remove the log handler for fake mailer output
        logger = logging.getLogger('test.smtp')
        handlers = [x for x in logger.handlers]
        for handler in handlers:
            logger.removeHandler(handler)
        return

    def test_refereereport_mandate(self):
        mandate = RefereeReportMandate()
        mandate.params['name'] = u'John Referee'
        mandate.params['email'] = 'aa@aa.aa'
        mandate.params['applicant_id'] = self.applicant.applicant_id
        mandate.params[
            'redirect_path'] = '/applicants/%s/%s/addrefereereport' % (
                container_name_1, self.applicant.application_number)
        self.app['mandates'].addMandate(mandate)
        # Let's open the add form page via the mandate view
        self.browser.open('http://localhost/app/mandate?mandate_id=%s'
            % mandate.mandate_id)
        # Form page opens and is prefilled
        self.assertEqual(
            self.browser.url,
            'http://localhost/app/applicants/%s/%s/addrefereereport?mandate_id=%s'
            % (container_name_1, self.applicant.application_number,
            mandate.mandate_id))
        self.assertTrue('value="John Referee"' in self.browser.contents)
        # Let's open the page directly with an invalid mandate
        self.browser.open(
            'http://localhost/app/applicants/%s/%s/addrefereereport?mandate_id=wrongmadate'
            % (container_name_1, self.applicant.application_number))
        self.assertTrue('<div class="alert alert-warning">No mandate.</div>'
            in self.browser.contents)
        self.assertEqual(self.browser.url, 'http://localhost/app')
        # Page is also blocked in maintenance mode
        grok.getSite()['configuration'].maintmode_enabled_by = u'anybody'
        self.browser.open(
            'http://localhost/app/applicants/%s/%s/addrefereereport?mandate_id=%s'
            % (container_name_1, self.applicant.application_number,
            mandate.mandate_id))
        self.assertTrue('<div class="alert alert-warning">The portal is '
                        'in maintenance mode'
            in self.browser.contents)
        self.assertEqual(self.browser.url, 'http://localhost/app')
        return

    def test_add_and_view_manage_reports(self):
        mandate = RefereeReportMandate()
        mandate.params['name'] = u'John Referee'
        mandate.params['email'] = 'aa@aa.aa'
        mandate.params['applicant_id'] = self.applicant.applicant_id
        mandate.params['redirect_path'] = '/applicants/%s/%s/addrefereereport' % (
                container_name_1, self.applicant.application_number)
        mandate.params['redirect_path2'] = ''
        self.app['mandates'].addMandate(mandate)
        self.assertEqual(len(self.app['mandates'].keys()), 1)
        # Let's open the add form page via the mandate view
        self.browser.open('http://localhost/app/mandate?mandate_id=%s'
            % mandate.mandate_id)
        self.assertTrue('Joan None' in self.browser.contents)
        self.assertTrue('John Referee' in self.browser.contents)
        # Report can't be saved without required fields
        self.browser.getControl(name="form.name").value = ''
        self.browser.getControl("Submit").click()
        self.assertTrue('Required input is missing' in self.browser.contents)
        self.browser.getControl(name="form.name").value = 'Johnny Referee'
        self.browser.getControl("Submit").click()
        # Referee will be redirected to the frontpage
        self.assertEqual(self.browser.url, 'http://localhost/app')
        self.assertTrue('Your report has been successfully submitted. '
                        'Please use the report link in the email again '
                        'to download a pdf slip of your report.'
            in self.browser.contents)
        # If they use the mandate again, they will be redirected to a pdf file
        self.browser.open('http://localhost/app/mandate?mandate_id=%s'
            % mandate.mandate_id)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'],
                         'application/pdf')
        path = os.path.join(samples_dir(), 'referee_report.pdf')
        open(path, 'wb').write(self.browser.contents)
        print "Sample PDF referee_report.pdf written to %s" % path
        # Report has been created
        self.assertEqual(len(self.applicant.refereereports), 1)
        report = self.applicant.refereereports[0]
        # The email address has been stored
        self.assertEqual(report.email, 'aa@aa.aa')
        # Referee can use mandate again to download the pdf report
        self.browser.open('http://localhost/app/mandate?mandate_id=%s'
            % mandate.mandate_id)
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'],
                         'application/pdf')
        # Referees can't use another mandate for adding a new report
        mandate2 = RefereeReportMandate()
        mandate2.params['name'] = u'John Referee'
        mandate2.params['email'] = 'aa@aa.aa'
        mandate2.params['applicant_id'] = self.applicant.applicant_id
        mandate2.params['redirect_path'] = '/applicants/%s/%s/addrefereereport' % (
                container_name_1, self.applicant.application_number)
        mandate2.params['redirect_path2'] = ''
        self.app['mandates'].addMandate(mandate2)
        self.browser.open('http://localhost/app/mandate?mandate_id=%s'
            % mandate2.mandate_id)
        self.assertTrue('You have already created a report with another mandate'
            in self.browser.contents)
        # Managers can view the report
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.manage_path)
        self.browser.getLink("%s" % report.r_id).click()
        self.assertEqual(
            self.browser.url, self.view_path  + '/%s' % report.r_id)
        self.assertTrue('Johnny Referee' in self.browser.contents)
        # Managers can download a pdf slip
        self.browser.getLink("Download referee report").click()
        self.assertEqual(self.browser.headers['Status'], '200 Ok')
        self.assertEqual(self.browser.headers['Content-Type'],
                         'application/pdf')
        # Mandate is not deleted ...
        self.assertEqual(len(self.app['mandates'].keys()), 2)
        # ... but redirect_path2 attribute has been set
        redirect_path2 = '/applicants/%s/%s/%s/referee_report.pdf' % (
                container_name_1,
                self.applicant.application_number,
                report.r_id)
        self.assertEqual(
            self.app['mandates'][mandate.mandate_id].params['redirect_path2'],
            redirect_path2)
        # Portal managers can edit referee reports (no button available!)
        self.browser.open(self.view_path + '/%s/manage' % report.r_id)
        self.browser.getControl(name="form.email_pref").value = 'bb@bb.de'
        self.browser.getControl("Save").click()
        self.assertEqual(report.email_pref, 'bb@bb.de')
        # Managers can delete referee reports
        self.browser.open(self.manage_path)
        self.browser.getLink("%s" % report.r_id).click()
        self.assertEqual(len(self.applicant.refereereports), 1)
        self.browser.getLink("Delete").click()
        self.assertEqual(len(self.applicant.refereereports), 0)
        self.assertTrue('Referee report removed.' in self.browser.contents)
        self.assertEqual(self.browser.url, self.view_path)
        # Report creation, managing and deletion is logged
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'applicants.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.anybody - applicants.browser.RefereeReportAddFormPage - '
            '%s - added: %s\n' % (self.applicant.applicant_id, report.r_id)
            in logcontent)
        self.assertTrue(
            'zope.mgr - applicants.browser.RefereeReportManageFormPage - '
            '%s - %s - saved: email_pref\n' % (
            self.applicant.applicant_id, report.r_id) in logcontent)
        self.assertTrue(
            'zope.mgr - applicants.browser.RemoveRefereeReportPage - '
            '%s - removed: %s\n' % (self.applicant.applicant_id, report.r_id)
            in logcontent)
        return

    def test_final_submit_with_referees(self):
        # Add two referees
        referee1 = RefereeEntry()
        referee2 = RefereeEntry()
        referee1.name = u'Linda Tree'
        referee1.email = 'linda@forest.de'
        referee2.name = u'Otis Stone'
        referee2.email = 'otis@stones.de'
        self.applicant.__parent__.send_email = True
        self.applicant.referees = [referee1, referee2]
        self.assertFalse(referee1.email_sent)
        self.assertFalse(referee2.email_sent)
        self.login()
        IWorkflowInfo(self.applicant).fireTransition('pay')
        self.browser.open(self.edit_path)
        self.fill_correct_values() # fill other fields with correct values
        image = open(SAMPLE_IMAGE, 'rb')
        ctrl = self.browser.getControl(name='form.passport')
        file_ctrl = ctrl.mech_control
        file_ctrl.add_file(image, filename='myphoto.jpg')
        self.browser.getControl("Save").click()
        self.browser.getControl(name="confirm_passport").value = True
        self.browser.getControl("Finally Submit").click()
        if self.app['mandates'].values()[0].params['name'] == 'Linda Tree':
            mandate_id_0 = self.app['mandates'].keys()[0]
            mandate_id_1 = self.app['mandates'].keys()[1]
        else:
            mandate_id_0 = self.app['mandates'].keys()[1]
            mandate_id_1 = self.app['mandates'].keys()[0]
        self.assertMatches(
            'Sending email from no-reply@waeup.org to linda@forest.de:'
            '\nMessage:'
            '\nmsg: MIME-Version: 1.0\nmsg: Content-Type: text/plain; charset="us-ascii"'
            '\nmsg: Content-Transfer-Encoding: 7bit'
            '\nmsg: From: Administrator <no-reply@waeup.org>'
            '\nmsg: To: Linda Tree <linda@forest.de>'
            '\nmsg: Reply-To: Administrator <contact@waeup.org>'
            '\nmsg: Subject: Request for referee report from Sample University'
            '\nmsg: '
            '\nmsg: Dear Linda Tree,'
            '\nmsg: '
            '\nmsg: The candidate with Id app%s_372052 and name John Anthony Tester applied to'
            '\nmsg: the Sample University to study Unnamed Certificate for the %s/%s session.'
            '\nmsg: The candidate has listed you as referee. You are, therefore, required to,'
            '\nmsg: kindly, provide your referral remarks on or before <YYYY-MM-DD hh:mm:ss>.<6-DIGITS>+00:00. Please use the'
            '\nmsg: following form:'
            '\nmsg: '
            '\nmsg: Report link: http://localhost/app/mandate?mandate_id=%s'
            '\nmsg: '
            '\nmsg: Thank You'
            '\nmsg: '
            '\nmsg: The Secretary'
            '\nmsg: School of Postgraduate Studies'
            '\nmsg: Sample University'
            '\nmsg: '
            '\nSending email from no-reply@waeup.org to otis@stones.de:'
            '\nMessage:'
            '\nmsg: MIME-Version: 1.0'
            '\nmsg: Content-Type: text/plain; charset="us-ascii"'
            '\nmsg: Content-Transfer-Encoding: 7bit'
            '\nmsg: From: Administrator <no-reply@waeup.org>'
            '\nmsg: To: Otis Stone <otis@stones.de>'
            '\nmsg: Reply-To: Administrator <contact@waeup.org>'
            '\nmsg: Subject: Request for referee report from Sample University'
            '\nmsg: '
            '\nmsg: Dear Otis Stone,'
            '\nmsg: '
            '\nmsg: The candidate with Id app%s_<6-DIGITS> and name John Anthony Tester applied to'
            '\nmsg: the Sample University to study Unnamed Certificate for the %s/%s session.'
            '\nmsg: The candidate has listed you as referee. You are, therefore, required to,'
            '\nmsg: kindly, provide your referral remarks on or before <YYYY-MM-DD hh:mm:ss>.<6-DIGITS>+00:00. Please use the'
            '\nmsg: following form:'
            '\nmsg: '
            '\nmsg: Report link: http://localhost/app/mandate?mandate_id=%s'
            '\nmsg: '
            '\nmsg: Thank You'
            '\nmsg: '
            '\nmsg: The Secretary'
            '\nmsg: School of Postgraduate Studies'
            '\nmsg: Sample University'
            '\nmsg: '
            '\nSending email from no-reply@waeup.org to xx@yy.zz:'
            '\nMessage:'
            '\nmsg: MIME-Version: 1.0'
            '\nmsg: Content-Type: text/plain; charset="us-ascii"'
            '\nmsg: Content-Transfer-Encoding: 7bit'
            '\nmsg: From: Administrator <no-reply@waeup.org>'
            '\nmsg: To: John Anthony Tester <xx@yy.zz>'
            '\nmsg: Reply-To: Administrator <contact@waeup.org>'
            '\nmsg: Subject: Your application form was successfully submitted'
            '\nmsg: '
            '\nmsg: Dear John Anthony Tester,'
            '\nmsg: '
            '\nmsg: Your application app%s_<6-DIGITS> has been successfully submitted to Sample University.'
            '\nmsg: '
            '\nmsg: Regards'
            '\nmsg: '
            % (session_1, session_1, session_2, mandate_id_0,
               session_1, session_1, session_2, mandate_id_1, session_1),
            self.get_fake_smtp_output()
            )
        self.assertTrue(
            'Application submitted' in self.browser.contents)
        self.assertTrue(
            'Form has been successfully submitted and 2 '
            'invitation emails were sent.' in self.browser.contents)
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'applicants.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            '%s - applicants.browser.ApplicantEditFormPage - %s - '
            'email sent: otis@stones.de' %
            (self.applicant.applicant_id, self.applicant.applicant_id)
            in logcontent)
        self.assertTrue(referee1.email_sent)
        self.assertTrue(referee2.email_sent)
        # If the form is being resubmitted, no more emails will be sent
        IWorkflowState(self.applicant).setState('paid')
        self.applicant.locked = False
        self.browser.open(self.edit_path)
        self.browser.getControl(name="confirm_passport").value = True
        self.browser.getControl("Finally Submit").click()
        self.assertTrue(
            'Form has been successfully submitted and 0 '
            'invitation emails were sent.' in self.browser.contents)
        return

    def test_remind_referees(self):
        self.applicant.lastname = u'Mitchell'
        IWorkflowState(self.applicant).setState('submitted')
        # Add two referees
        referee1 = RefereeEntry()
        referee2 = RefereeEntry()
        referee1.name = u'Linda Tree'
        referee1.email = 'linda@forest.de'
        referee2.name = u'Otis Stone'
        referee2.email = 'otis@stones.de'
        referee1.email_sent = True
        referee2.email_sent = True
        self.applicant.referees = [referee1, referee2]
        # Managers can remind referees
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open(self.view_path)
        self.browser.getLink("Remind referees").click()
        self.assertTrue('2 referee(s) have been reminded by email.'
            in self.browser.contents)
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'applicants.log')
        logcontent = open(logfile).read()
        self.assertTrue(
            'zope.mgr - applicants.browser.RefereesRemindPage - %s - '
            'email sent: otis@stones.de' % self.applicant.applicant_id
            in logcontent)
        if self.app['mandates'].values()[0].params['name'] == 'Linda Tree':
            mandate_id_0 = self.app['mandates'].keys()[0]
            mandate_id_1 = self.app['mandates'].keys()[1]
        else:
            mandate_id_0 = self.app['mandates'].keys()[1]
            mandate_id_1 = self.app['mandates'].keys()[0]
        self.assertMatches(
            'Sending email from no-reply@waeup.org to linda@forest.de:'
            '\nMessage:'
            '\nmsg: MIME-Version: 1.0\nmsg: Content-Type: text/plain; charset="us-ascii"'
            '\nmsg: Content-Transfer-Encoding: 7bit'
            '\nmsg: From: Administrator <no-reply@waeup.org>'
            '\nmsg: To: Linda Tree <linda@forest.de>'
            '\nmsg: Reply-To: Administrator <contact@waeup.org>'
            '\nmsg: Subject: Request for referee report from Sample University'
            '\nmsg: '
            '\nmsg: Dear Linda Tree,'
            '\nmsg: '
            '\nmsg: The candidate with Id app%s_372052 and name Joan Mitchell applied to'
            '\nmsg: the Sample University to study Unnamed Certificate for the %s/%s session.'
            '\nmsg: The candidate has listed you as referee. You are, therefore, required to,'
            '\nmsg: kindly, provide your referral remarks on or before <YYYY-MM-DD hh:mm:ss>.<6-DIGITS>+00:00. Please use the'
            '\nmsg: following form:'
            '\nmsg: '
            '\nmsg: Report link: http://localhost/app/mandate?mandate_id=%s'
            '\nmsg: '
            '\nmsg: Thank You'
            '\nmsg: '
            '\nmsg: The Secretary'
            '\nmsg: School of Postgraduate Studies'
            '\nmsg: Sample University'
            '\nmsg: '
            '\nSending email from no-reply@waeup.org to otis@stones.de:'
            '\nMessage:'
            '\nmsg: MIME-Version: 1.0'
            '\nmsg: Content-Type: text/plain; charset="us-ascii"'
            '\nmsg: Content-Transfer-Encoding: 7bit'
            '\nmsg: From: Administrator <no-reply@waeup.org>'
            '\nmsg: To: Otis Stone <otis@stones.de>'
            '\nmsg: Reply-To: Administrator <contact@waeup.org>'
            '\nmsg: Subject: Request for referee report from Sample University'
            '\nmsg: '
            '\nmsg: Dear Otis Stone,'
            '\nmsg: '
            '\nmsg: The candidate with Id app%s_<6-DIGITS> and name Joan Mitchell applied to'
            '\nmsg: the Sample University to study Unnamed Certificate for the %s/%s session.'
            '\nmsg: The candidate has listed you as referee. You are, therefore, required to,'
            '\nmsg: kindly, provide your referral remarks on or before <YYYY-MM-DD hh:mm:ss>.<6-DIGITS>+00:00. Please use the'
            '\nmsg: following form:'
            '\nmsg: '
            '\nmsg: Report link: http://localhost/app/mandate?mandate_id=%s'
            '\nmsg: '
            '\nmsg: Thank You'
            '\nmsg: '
            '\nmsg: The Secretary'
            '\nmsg: School of Postgraduate Studies'
            '\nmsg: Sample University'
            '\nmsg: '
            % (session_1, session_1, session_2, mandate_id_0,
               session_1, session_1, session_2, mandate_id_1,),
            self.get_fake_smtp_output()
            )
        # If a report exists, only one email is being sent to Otis Stone.
        report = createObject(u'waeup.ApplicantRefereeReport')
        report.r_id = 'any_id'
        report.name = u'Liiiinda Tree'
        report.email = 'linda@forest.de'
        self.applicant[report.r_id] = report
        self.browser.open(self.view_path)
        self.browser.getLink("Remind referees").click()
        self.assertTrue('1 referee(s) have been reminded by email.'
            in self.browser.contents)
        return
