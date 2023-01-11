## $Id: test_container.py 13077 2015-06-19 15:36:21Z henrik $
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
Tests for applicants containers.
"""
import unittest
from zope.interface.verify import verifyClass, verifyObject
from waeup.kofa.applicants import interfaces
from waeup.kofa.applicants.container import (
    ApplicantsContainer,
    )

class ApplicantsContainerTestCase(unittest.TestCase):

    def test_interfaces(self):
        # Make sure the correct interfaces are implemented.
        self.assertTrue(
            verifyClass(
                interfaces.IApplicantsContainer, ApplicantsContainer)
            )
        self.assertTrue(
            verifyObject(
                interfaces.IApplicantsContainer, ApplicantsContainer())
            )
        return

def suite():
    suite = unittest.TestSuite()
    for test_case in [
        ApplicantsContainerTestCase,
        ]:
        suite.addTests(
            unittest.TestLoader().loadTestsFromTestCase(test_case))
    return suite

test_suite = suite
