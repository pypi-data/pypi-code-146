## $Id: test_catalog.py 8321 2012-05-02 06:24:42Z henrik $
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
import shutil
import tempfile
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility
from zope.component.hooks import setSite
from zope.interface.verify import verifyClass, verifyObject
from waeup.kofa.app import University
from waeup.kofa.interfaces import IQueryResultItem
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase
from waeup.kofa.accesscodes.accesscode import (
    AccessCodeBatch, invalidate_accesscode, disable_accesscode)
from waeup.kofa.accesscodes.workflow import INITIALIZED, USED, DISABLED
from waeup.kofa.accesscodes.catalog import AccessCodeQueryResultItem, search

class CatalogTestSetup(FunctionalTestCase):
    # A setup for testing accesscode catalog related stuff.
    #
    # sets up a site with some accesscode batches already created.
    layer = FunctionalLayer

    def setUp(self):
        super(CatalogTestSetup, self).setUp()

        # Prepopulate ZODB
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']
        setSite(self.app)

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
        return

    def tearDown(self):
        shutil.rmtree(self.dc_root)
        super(CatalogTestSetup, self).tearDown()
        return


class AccessCodeCatalogTests(CatalogTestSetup):
    # Tests for helpers like get_access_code, disable_accesscode, ...

    layer = FunctionalLayer

    def test_get_catalog(self):
        # We can get an accesscodes catalog if we wish
        cat = queryUtility(ICatalog, name='accesscodes_catalog')
        assert cat is not None

    def test_search_by_code(self):
        # We can find a certain code
        cat = queryUtility(ICatalog, name='accesscodes_catalog')
        results = cat.searchResults(code=('APP-1-11111111', 'APP-1-11111111'))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.ac1

    def test_search_code_not_existent(self):
        # Not existent codes will not be found
        cat = queryUtility(ICatalog, name='accesscodes_catalog')
        results = cat.searchResults(code=('APP-1-blah', 'APP-1-blah'))
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 0

    def test_search_history(self):
        # We can search for certain history entries
        # To update history we use `invalidate_accesscode`
        invalidate_accesscode(
            'APP-1-11111111', comment='used by Tester')

        # Now we want to find the term ``Tester`` in histories of all acs
        cat = queryUtility(ICatalog, name='accesscodes_catalog')
        results = cat.searchResults(history='Tester')
        results = [x for x in results] # Turn results generator into list
        assert len(results) == 1
        assert results[0] is self.ac1

    def test_search_disabled(self):
        # We can seach for disabled access codes
        disable_accesscode('APP-1-11111111')
        # Now we want to find the disabled access code
        cat = queryUtility(ICatalog, name='accesscodes_catalog')
        results1 = cat.searchResults(state=(DISABLED, DISABLED))
        results2 = cat.searchResults(state=(INITIALIZED, INITIALIZED))
        results1 = [x for x in results1] # Turn results generator into list
        # We found 1 accescode disabled
        assert len(results1) == 1
        assert results1[0] is self.ac1
        # We found 2 accesscodes not disabled
        assert len(results2) == 2
        assert [x for x in results2] == [self.ac2, self.ac3]

    def test_search_used(self):
        # We can search for used/unused access codes
        invalidate_accesscode('APP-1-11111111')
        # Now we want to find the invalidated access code
        cat = queryUtility(ICatalog, name='accesscodes_catalog')
        results1 = cat.searchResults(state=(USED, USED))
        results2 = cat.searchResults(state=(INITIALIZED, INITIALIZED))
        results1 = [x for x in results1] # Turn results generator into list
        # We found 1 accescode used
        assert len(results1) == 1
        assert results1[0] is self.ac1
        # We found 2 accesscodes not used
        assert len(results2) == 2
        assert [x for x in results2] == [self.ac2, self.ac3]

    def test_search_mixed(self):
        # We can ask for several attributes at the same time
        invalidate_accesscode('APP-1-11111111', comment='Used by Tester')
        disable_accesscode('APP-1-33333333', comment='Disabled by Tester')
        cat = queryUtility(ICatalog, name='accesscodes_catalog')
        # Now we search for an applicants code that has 'Tester'
        # mentioned in history, is used, and has a code between
        # 'APP-1-11111111' and 'APP-2-11111111'. This should find
        # exactly one access code.
        results = cat.searchResults(history='Tester',
                                    state=(USED, USED),
                                    code=('APP-1-11111111', 'APP-1-22222222'))
        assert len(results) == 1
        assert self.ac1 in results

    def test_ac_change(self):
        # When an AC is changed, that change will be reflected
        # immediately in catalog
        cat = queryUtility(ICatalog, name='accesscodes_catalog')
        result = cat.searchResults(state=(USED, USED))
        assert len(result) == 0
        invalidate_accesscode('APP-1-11111111')
        result = cat.searchResults(state=(USED, USED))
        assert len(result) == 1

class FakeView(object):
    # A view we can use in tests. Provides only the neccessary methods.
    flashed = []
    def url(self, context):
        pass
    def flash(self, msg):
        self.flashed.append(msg)

class AccessCodeQueryResultItemTests(CatalogTestSetup):
    # Test query result items

    layer = FunctionalLayer

    def test_ifaces(self):
        # Make sure we implement the interfaces correctly
        view = FakeView()
        self.assertTrue(verifyClass(
                IQueryResultItem, AccessCodeQueryResultItem))
        item = AccessCodeQueryResultItem(self.ac1, view)
        self.assertTrue(verifyObject(
                IQueryResultItem, item))
        return

class SearchTests(CatalogTestSetup):
    # Tests for the search() function

    layer = FunctionalLayer

    def setUp(self):
        super(SearchTests, self).setUp()
        self.view = FakeView()
        return

    def test_search_none(self):
        # if we search none we will get it. Also a warning is displayed.
        result = search(view=self.view)
        self.assertTrue(result is None)
        self.assertEqual(self.view.flashed, ['Empty search string.'])
        return

    def test_search_history(self):
        # we can search for history entries
        result = search(
            query='initialized', # A word that appears in all items' hist
            searchtype='history', view=self.view)
        self.assertEqual(len(result), 3)
        return

    def test_search_batch_serial(self):
        # we can search for batch serials
        result = search(
            query=2,
            searchtype='batch_serial', view=self.view)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].code, 'APP-1-33333333')
        return

    def test_search_freestyle(self):
        # we can even search for arbitrary fields
        result = search(
            query='APP-1-11111111',
            searchtype='code', view=self.view)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].code, 'APP-1-11111111')
        return
