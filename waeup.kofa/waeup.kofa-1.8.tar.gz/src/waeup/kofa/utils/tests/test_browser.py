## $Id: test_browser.py 16037 2020-03-13 10:55:28Z henrik $
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
Test the student-related UI components.
"""
import shutil
import tempfile
import pytz
from datetime import datetime, timedelta
from StringIO import StringIO
import os
import grok
from zope.event import notify
from zope.component import createObject, queryUtility
from zope.component.hooks import setSite, clearSite
from zope.catalog.interfaces import ICatalog
from zope.security.interfaces import Unauthorized
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase

from waeup.kofa.utils.browser import replaceStudentMessages
from waeup.kofa.students.tests.test_browser import StudentsFullSetup
from waeup.kofa.applicants.tests.test_browser import ApplicantsFullSetup

class StudentUtilsUITests(StudentsFullSetup):

    layer = FunctionalLayer

    def test_replace_student_messages(self):
        self.assertTrue('Record created by system' in
            self.student.history.messages[0])
        replaceStudentMessages('system', 'me')
        self.assertTrue('Record created by me' in
            self.student.history.messages[0])

    def test_modify_all_student_history(self):
        self.assertTrue('Record created by system' in
            self.student.history.messages[0])
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open('http://localhost/app/modify_student_history')
        self.assertTrue(
            'Syntax: /modify_student_history?old=[old string]&new=[new string]'
            in self.browser.contents)
        self.browser.open(
            'http://localhost/app/modify_student_history?old=by system&new=by me')
        self.assertTrue('Finished' in self.browser.contents)
        self.assertTrue('Record created by me' in
            self.student.history.messages[0])

    def test_remove_student_history_message(self):
        self.assertTrue('Record created by system' in
            self.student.history.messages[0])
        self.assertEqual(len(self.student.history.messages),1)
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open('http://localhost/app/remove_student_history_message')
        self.assertTrue(
            'Syntax: /remove_student_history_message?student_id=[id]&number=[line number, starting with 0]'
            in self.browser.contents)
        self.browser.open(
            'http://localhost/app/remove_student_history_message?student_id=%s&number=0' % self.student.student_id)
        self.assertTrue('Finished' in self.browser.contents)
        self.assertEqual(len(self.student.history.messages),0)
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'main.log')
        logcontent = open(logfile).read()
        self.assertMatches(
            "...zope.mgr - line '<YYYY-MM-DD hh:mm:ss> UTC - "
            "Record created by system' removed in K1000000 history",
            logcontent)

    def test_reindex(self):
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open('http://localhost/app/reindex')
        self.assertTrue('No catalog name provided' in self.browser.contents)
        self.browser.open('http://localhost/app/reindex?ctlg=xyz')
        self.assertTrue('xyz_catalog does not exist' in self.browser.contents)
        cat = queryUtility(ICatalog, name='students_catalog')
        results = cat.searchResults(student_id=(None, None))
        self.assertEqual(len(results),1)
        self.browser.open('http://localhost/app/reindex?ctlg=students')
        self.assertTrue('1 students re-indexed' in self.browser.contents)
        cat.clear()
        results = cat.searchResults(student_id=(None, None))
        self.assertEqual(len(results),0)
        self.browser.open('http://localhost/app/reindex?ctlg=students')
        # No docids found, the new reindex method does only reindex existing
        # catalog entries.
        self.assertTrue('0 students re-indexed' in self.browser.contents)
        results = cat.searchResults(student_id=(None, None))
        self.assertEqual(len(results),0)

class ApplicantUtilsUITests(ApplicantsFullSetup):

    layer = FunctionalLayer

    def test_modify_all_applicant_history(self):
        self.assertTrue('Application initialized by system' in
            self.applicant.history.messages[0])
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open('http://localhost/app/modify_applicant_history')
        self.assertTrue(
            'Syntax: /modify_applicant_history?old=[old string]&new=[new string]'
            in self.browser.contents)
        self.browser.open(
            'http://localhost/app/modify_applicant_history?old=by system&new=by me')
        self.assertTrue('Finished' in self.browser.contents)
        self.assertTrue('Application initialized by me' in
            self.applicant.history.messages[0])

    def test_remove_applicant_history_message(self):
        self.assertTrue('Application initialized by system' in
            self.applicant.history.messages[0])
        self.assertEqual(len(self.applicant.history.messages),1)
        self.browser.addHeader('Authorization', 'Basic mgr:mgrpw')
        self.browser.open('http://localhost/app/remove_applicant_history_message')
        self.assertTrue(
            'Syntax: /remove_applicant_history_message?applicant_id=[id]&number=[line number, starting with 0]'
            in self.browser.contents)
        self.browser.open(
            'http://localhost/app/remove_applicant_history_message?applicant_id=%s&number=0' % self.applicant.applicant_id)
        self.assertTrue('Finished' in self.browser.contents)
        self.assertEqual(len(self.applicant.history.messages),0)
        logfile = os.path.join(
            self.app['datacenter'].storage, 'logs', 'main.log')
        logcontent = open(logfile).read()
        self.assertMatches(
            "...zope.mgr - line '<YYYY-MM-DD hh:mm:ss> UTC - "
            "Application initialized by system' removed in %s history"
            % self.applicant.applicant_id, logcontent)