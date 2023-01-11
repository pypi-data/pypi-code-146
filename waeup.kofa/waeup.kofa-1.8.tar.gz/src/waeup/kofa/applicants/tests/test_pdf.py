## $Id: test_pdf.py 7811 2012-03-08 19:00:51Z uli $
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
"""Test PDF components.
"""
import unittest

from zope.component import getAdapter
from zope.interface import verify
from waeup.kofa.applicants.pdf import IPDF, PDFApplicationSlip
from waeup.kofa.applicants.tests.test_browser import ApplicantsFullSetup
from waeup.kofa.interfaces import IPDF
from waeup.kofa.testing import FunctionalTestCase, FunctionalLayer

class PDFApplicationSlipTests(ApplicantsFullSetup):

    layer = FunctionalLayer

    def test_ifaces(self):
        # make sure we implement/provide the promised interfaces
        obj = PDFApplicationSlip(self.applicant)
        verify.verifyClass(IPDF, PDFApplicationSlip)
        verify.verifyObject(IPDF, obj)
        return

    def test_adapter(self):
        # we can get PDFs by adapter lookup
        pdfcreator = getAdapter(self.applicant, IPDF, name='application_slip')
        self.assertTrue(pdfcreator is not None)
        return

    def test_call(self):
        # we can generate PDFs from applicants
        pdfcreator = PDFApplicationSlip(self.applicant)
        result = pdfcreator()
        self.assertTrue(result.startswith('%PDF-1.4'))
        return

    def test_call_with_admission_set(self):
        # we can generate PDF if admission course is set.
        # XXX: implement test
        pass

    def test_call_with_view(self):
        # we can provide extra info if we have a view
        # XXX: implement test
        pass
