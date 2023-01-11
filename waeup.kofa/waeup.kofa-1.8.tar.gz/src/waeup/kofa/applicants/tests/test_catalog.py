## $Id: test_catalog.py 8700 2012-06-12 21:01:17Z henrik $
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
Tests for applicants specific catalog (currently only one).
"""
import shutil
import tempfile
import grok
from zope.component import getUtility, createObject
from hurry.query import Eq
from hurry.query.interfaces import IQuery
from zope.catalog.interfaces import ICatalog
from zope.component import getUtility
from zope.component.hooks import setSite
from zope.component.interfaces import ComponentLookupError
from zope.testbrowser.testing import Browser
from waeup.kofa.app import University
from waeup.kofa.applicants.container import ApplicantsContainer
from waeup.kofa.applicants.applicant import Applicant
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase

class CatalogTests(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(CatalogTests, self).setUp()

        # Setup a sample site for each test
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']
        self.browser = Browser()
        self.browser.handleErrors = False

    def tearDown(self):
        super(CatalogTests, self).tearDown()
        shutil.rmtree(self.dc_root)

    def create_applicant(self):
        # Create an applicant in an applicants container
        self.container = ApplicantsContainer()
        self.container.code = u"mystuff"
        setSite(self.app)
        self.app['applicants']['mystuff'] = self.container
        self.applicant = Applicant()
        self.app['applicants']['mystuff'].addApplicant(self.applicant)
        return

    def test_get_applicants_catalog(self):
        # There is no global applicants catalog, but one for each site.
        self.assertRaises(
            ComponentLookupError,
            getUtility, ICatalog, name='applicants_catalog')
        # If we are 'in the local site' we can get an applicants catalog.
        setSite(self.app)
        cat = getUtility(ICatalog, name='applicants_catalog')
        self.assertTrue(ICatalog.providedBy(cat))

    def test_get_applicant(self):
        # Make sure that applicants are really catalogued on creation.
        self.create_applicant()
        q = getUtility(IQuery)
        subquery = Eq(('applicants_catalog', 'applicant_id'),
            self.applicant.applicant_id)
        results = list(q.searchResults(subquery))
        self.assertEqual(len(results), 1)
        result_applicant = results[0]
        self.assertTrue(isinstance(result_applicant, Applicant))
        self.assertEqual(result_applicant.applicant_id, self.applicant.applicant_id)

    def test_get_payment(self):
        self.create_applicant()
        q = getUtility(IQuery)
        subquery = Eq(('applicants_catalog', 'applicant_id'),
            self.applicant.applicant_id)
        results = list(q.searchResults(subquery))
        self.assertEqual(len(results), 1)
        result_applicant = results[0]
        payment = createObject('waeup.ApplicantOnlinePayment')
        payment.p_id = 'p1234567890'
        payment.p_item = u'Payment Item'
        payment.p_session = 2011
        payment.p_category = 'application'
        result_applicant[payment.p_id] = payment
        # We can find a payment ticket by the payment session ...
        cat = getUtility(ICatalog, name='payments_catalog')
        results = cat.searchResults(p_session=(2011, 2011))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is result_applicant['p1234567890']
        # ... and by the payment id
        results = cat.searchResults(p_id=('p1234567890', 'p1234567890'))
        assert len(results) == 1
        # If we remove the applicant also the payment disappears
        del self.app['applicants']['mystuff'][result_applicant.application_number]
        results = cat.searchResults(p_id=('p1234567890', 'p1234567890'))
        assert len(results) == 0
