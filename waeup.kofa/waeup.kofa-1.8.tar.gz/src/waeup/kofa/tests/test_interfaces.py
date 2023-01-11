# -*- coding: utf-8 -*-
## $Id: test_interfaces.py 8638 2012-06-06 13:58:49Z uli $
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

# Tests for interfaces and included components.
import grok
import unittest
from waeup.kofa.interfaces import DuplicationError, RoleSource, check_email
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase

class RegExTests(unittest.TestCase):
    # Let's test regular expressions here

    def check(self, expression, string):
        if expression.match(string) is not None:
            return True
        return False

    def test_check_email_allowed(self):
        # the RE check_email does moderate format checks, allowing
        # also strange looking but valid email addresses
        self.assertTrue(check_email('manfred@domain.com') is not None)
        self.assertTrue(check_email('bob@localhost') is not None)
        self.assertTrue(check_email('bob@h5.waeup.org') is not None)
        self.assertTrue(check_email('bob@idn_with_ümlaut.com') is not None)
        # also unicodes with umlauts work
        self.assertTrue(check_email(u'bob@idn_with_ümlaut.com') is not None)
        self.assertTrue(
            check_email('bob_the-complex+mbox@my.place') is not None)
        return

    def test_check_email_forbidden(self):
        # the RE check_email does moderate format checks, but doesn't
        # accept everything.
        # no domain at all
        self.assertTrue(check_email('bob') is None)
        self.assertTrue(check_email('bob@') is None)
        # each domain part must contain at least something
        self.assertTrue(check_email('bob@h5.waeup.') is None)
        # whitespaces in addresses
        self.assertTrue(check_email('spacey @domain.com') is None)
        self.assertTrue(check_email('tabby\t@domain.com') is None)
        # two dots next to each other in domain (empty domain part)
        self.assertTrue(check_email('bob@some..domain') is None)
        # commas are forbidden
        self.assertTrue(check_email('bob@foo,alice@bar') is None)
        return

class DuplicationErrorTests(unittest.TestCase):

    def test_is_exception(self):
        exc = DuplicationError('Some message')
        self.assertEqual(exc.msg, 'Some message')
        self.assertEqual(exc.entries, [])

    def test_as_string(self):
        exc = DuplicationError('Some message')
        self.assertEqual(exc.__str__(), "'Some message'")


class RoleSourceTests(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(RoleSourceTests, self).setUp()
        # Register a role
        class SomeRole(grok.Role):
            grok.name('waeup.testrole')
            grok.title('RoleWith.DotName')
            grok.permissions('waeup.Public')
        # Register a role not visible to waeup portal as its name does
        # not start with 'waeup.'
        class NonKofaRole(grok.Role):
            grok.name('nonwaeup.testrole')
            grok.title('Role not suitable for waeup')
            grok.permissions('waeup.Public')
        grok.testing.grok_component('SomeRole', SomeRole)
        grok.testing.grok_component('NonKofaRole', NonKofaRole)
        return

    def test_getValues(self):
        source = RoleSource()
        result = source.factory.getValues()
        self.assertTrue(u'waeup.testrole' in result)
        self.assertTrue(u'waeup.PortalManager' in result)
        self.assertTrue(u'nonwaeup.testrole' not in result)

    def test_getTitle(self):
        source = RoleSource()
        result = source.factory.getTitle(u'waeup.PortalManager')
        self.assertEqual(result, 'Portal Manager')

    def test_getTitleWithDot(self):
        # If there is a dot in the role title, we get only the last part
        source = RoleSource()
        result = source.factory.getTitle(u'waeup.testrole')
        self.assertEqual(result, 'DotName')
