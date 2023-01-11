## $Id: test_refereereport.py 13975 2016-06-22 16:55:37Z henrik $
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
"""Tests for application payments.

"""
import unittest
from datetime import datetime
from zope.interface import verify
from zope.component import createObject
from waeup.kofa.applicants.refereereport import (
    ApplicantRefereeReport, ApplicantRefereeReportFactory)
from waeup.kofa.applicants.interfaces import IApplicantRefereeReport
from waeup.kofa.testing import (FunctionalLayer, FunctionalTestCase)


class ApplicantRefereeReportTest(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(ApplicantRefereeReportTest, self).setUp()
        self.report = createObject(u'waeup.ApplicantRefereeReport')
        self.report.r_id = 'my_report'
        self.applicant = createObject(u'waeup.Applicant')
        self.applicant[self.report.r_id] = self.report
        return

    def tearDown(self):
        super(ApplicantRefereeReportTest, self).tearDown()
        return

    def test_interfaces(self):
        # Make sure the correct interfaces are implemented.
        self.assertTrue(
            verify.verifyClass(
                IApplicantRefereeReport, ApplicantRefereeReport)
            )
        self.assertTrue(
            verify.verifyObject(
                IApplicantRefereeReport, ApplicantRefereeReport())
            )
        return

    def test_report(self):
        self.assertEqual(self.applicant['my_report'], self.report)
        self.assertTrue(isinstance(self.report.creation_date, datetime))
        return


class ApplicantRefereeReportFactoryTest(unittest.TestCase):

    def setUp(self):
        self.factory = ApplicantRefereeReportFactory()
        return

    def test_factory(self):
        obj = self.factory()
        assert isinstance(obj, ApplicantRefereeReport)

    def test_getInterfaces(self):
        implemented_by = self.factory.getInterfaces()
        assert implemented_by.isOrExtends(IApplicantRefereeReport)
