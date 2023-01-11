## $Id: test_waeup.py 7811 2012-03-08 19:00:51Z uli $
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
Test setup for the waeup.kofa package.
"""
import grok
import re
import zope.component.eventtesting
from zope.testing import renormalizing
from waeup.kofa.testing import FunctionalLayer

def setUpZope(test):
    zope.component.eventtesting.setUp(test)

checker = renormalizing.RENormalizing([
        (re.compile('[\d]{10}'), '<10-DIGITS>'),
        ])

# Register all tests in the waeup.kofa package
test_suite = grok.testing.register_all_tests(
    'waeup.kofa', checker=checker, usetup=setUpZope,
    layer=FunctionalLayer)
