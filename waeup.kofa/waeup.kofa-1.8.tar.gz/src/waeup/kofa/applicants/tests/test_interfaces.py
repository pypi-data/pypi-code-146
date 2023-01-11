## $Id: test_interfaces.py 10208 2013-05-23 05:39:45Z henrik $
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
Test components defined in interface module.
"""
import unittest
from zc.sourcefactory.browser.source import FactoredTerms
from zope.publisher.browser import TestRequest
from waeup.kofa.students.vocabularies import GenderSource

class InterfacesTest(unittest.TestCase):

    def setUp(self):
        self.source = GenderSource()
        self.request = TestRequest()
        self.terms = FactoredTerms(self.source, self.request)
        return

    def tearDown(self):
        pass

    def test_GenderSource_list(self):
        result = list(self.source)
        self.assertEqual(result, ['m', 'f'])

    def test_GenderSource_term_male(self):
        term = self.terms.getTerm('m')
        assert term.title == 'male'
        assert term.token == 'm'
        assert term.value == 'm'

    def test_GenderSource_term_female(self):
        term = self.terms.getTerm('f')
        assert term.title == 'female'
        assert term.token == 'f'
        assert term.value == 'f'

    def test_GernderSource_term_invalid(self):
        term_inv = self.terms.getTerm('Invalid')
        assert term_inv.title is None
        assert term_inv.token == 'i'

def suite():
    suite = unittest.TestSuite()
    for testcase in [
            InterfacesTest,
            ]:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testcase))
    return suite

test_suite = suite


