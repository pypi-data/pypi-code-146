## $Id: test_university.py 12951 2015-05-15 08:56:17Z henrik $
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

# Test the public API part of the university subpackage
import unittest
from waeup.kofa.university import *
from waeup.kofa.testing import get_doctest_suite

class UniversitySubpackageTests(unittest.TestCase):

    def test_public_api(self):
        names = globals().keys()
        self.assertTrue('Course' in names)
        self.assertTrue('CoursesContainer' in names)
        self.assertTrue('Faculty' in names)
        self.assertTrue('FacultiesContainer' in names)

def test_suite():
    # collect doctests for university subpackage
    suite = get_doctest_suite(['doctests/certcourse.txt',])
    # add local unittests (actually only one)
    for testcase in [UniversitySubpackageTests,]:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
                testcase))
    return suite
