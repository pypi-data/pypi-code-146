## $Id: test_catalog.py 12110 2014-12-02 06:43:10Z henrik $
##
## Copyright (C) 2012 Uli Fouquet & Henrik Bettermann
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
"""Tests for basic catalog components.
"""
import grok
import unittest
from grok import index
from zope.catalog.interfaces import ICatalog
from zope.component import getUtility
from zope.component.hooks import setSite
from zope.interface import Interface, Attribute
from zope.interface.verify import verifyClass, verifyObject
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase
from waeup.kofa.catalog import FilteredQueryBase, FilteredCatalogQueryBase
from waeup.kofa.interfaces import IFilteredQuery, IFilteredCatalogQuery

class FilteredQueryBaseTests(unittest.TestCase):

    def test_iface(self):
        # make sure, we correctly implement interface requirements
        obj = FilteredQueryBase()
        verifyClass(IFilteredQuery, FilteredQueryBase)
        verifyObject(IFilteredQuery, obj)
        return

    def test_kw(self):
        # keywords are set correctly on construction
        q1 = FilteredQueryBase()
        self.assertEqual(q1._kw, dict())
        q2 = FilteredQueryBase(name='Bob')
        self.assertEqual(q2._kw, dict(name='Bob'))
        return

    def test_kw_defaults(self):
        # defaults are set initially but can be overridden.
        class MyFilter(FilteredQueryBase):
            defaults=dict(name='Bob')
        q1 = MyFilter()
        self.assertEqual(q1._kw, dict(name='Bob'))
        q2 = MyFilter(name='Alice', age=29)
        self.assertEqual(q2._kw, dict(name='Alice', age=29))
        return

    def test_query_not_implemented(self):
        # we are warned when using `query()`
        q = FilteredQueryBase()
        self.assertRaises(NotImplementedError, q.query)
        return


# A sample catalog environment. Has to be grokked to work
class Herd(grok.Container, grok.Application):
    pass

class IMammoth(Interface):
    age = Attribute('Age')
    name = Attribute('Name')

    def message():
        """Message for the world.
        """

class MammothCatalog(grok.Indexes):
    grok.site(Herd)
    grok.context(IMammoth)
    grok.name('mammoths')

    name = index.Field(attribute='name')
    age = index.Field(attribute='age')

class Mammoth(grok.Model):
    grok.implements(IMammoth)

    def __init__(self, name, age, message):
        self.age = age
        self.name = name
        self._message = message

    def message(self):
        return self._message

setup_done = False
class FilteredCatalogQueryBaseTests(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        global setup_done
        super(FilteredCatalogQueryBaseTests, self).setUp()
        if not setup_done:
            # grok this module to register indexes etc. defined above
            # ...and do this only once
            # XXX workaround because functional test cases do not support
            #     classmethod setUp
            grok.testing.grok(self.__module__)
            setup_done = True
        self.root = self.getRootFolder()
        self.getRootFolder()['herd'] = Herd()
        self.herd = self.root['herd']
        self.populate_catalog()
        self.catalog = getUtility(
            ICatalog, context=self.herd, name='mammoths')
        return

    def populate_catalog(self):
        setSite(self.herd)
        self.herd['bob'] = Mammoth('Bob', 21, 'Hi there!')
        self.herd['alice'] = Mammoth('Alice', 22, 'Hello!')
        return

    def test_iface(self):
        # make sure, we correctly implement interface requirements
        obj = FilteredCatalogQueryBase()
        verifyClass(IFilteredCatalogQuery, FilteredCatalogQueryBase)
        verifyObject(IFilteredCatalogQuery, obj)
        return

    def test_cat_name_respected(self):
        # a set cat_name is respected when doing the query
        q = FilteredCatalogQueryBase(name='Bob')
        q.cat_name = 'mammoths' # set a registered catalog name
        result = q.query()
        self.assertEqual([x.name for x in result], ['Bob'])
        return

    def test_query_catalog(self):
        # we can pass in a catalog instance
        q = FilteredCatalogQueryBase(name='Bob')
        result = q.query_catalog(catalog=self.catalog)
        self.assertEqual([x.name for x in result], ['Bob'])
        return

    def test_query_catalog_value_ranges(self):
        # we can ask for value ranges
        q = FilteredCatalogQueryBase(name=('Alice', 'Bob'))
        result = q.query_catalog(catalog=self.catalog)
        self.assertEqual([x.name for x in result], ['Bob', 'Alice'])
        return

    def test_query_value_ranges(self):
        # we can ask for value ranges instead of single values
        q = FilteredCatalogQueryBase(name=('Alice', 'Bob'))
        q.cat_name = 'mammoths'
        result = q.query()
        self.assertEqual([x.name for x in result], ['Bob', 'Alice'])
        return

    def test_query_mixed_values(self):
        # we can ask for different values at the same time
        q = FilteredCatalogQueryBase(name=('Alice', 'Bob'), age=22)
        q.cat_name = 'mammoths'
        result = q.query()
        self.assertEqual([x.name for x in result], ['Alice'])
        return

    def test_query_invalid_cat_name(self):
        # with an invalid catalog name we get empty results
        q = FilteredCatalogQueryBase(name='Bob')
        q.cat_name = 'NOT-EXISTING'
        result = q.query()
        self.assertEqual([x.name for x in result], [])
        return

    def test_query_catalog_no_site(self):
        # without a site with catalog we get empty results
        setSite(None) # unset current site
        q = FilteredCatalogQueryBase(name='Bob')
        q.cat_name = 'mammoths'
        result = q.query()
        self.assertEqual([x.name for x in result], [])
        return
