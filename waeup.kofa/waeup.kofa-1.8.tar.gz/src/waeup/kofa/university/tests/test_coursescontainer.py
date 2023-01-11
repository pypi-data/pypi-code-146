## $Id: test_coursescontainer.py 7811 2012-03-08 19:00:51Z uli $
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

# Test course containers

import unittest
from zope.interface.verify import verifyClass, verifyObject
from waeup.kofa.university.interfaces import ICoursesContainer
from waeup.kofa.university import CoursesContainer, Course

class CoursesContainerTests(unittest.TestCase):

    def test_ifaces(self):
        container = CoursesContainer()
        self.assertTrue(verifyClass(ICoursesContainer, CoursesContainer))
        self.assertTrue(verifyObject(ICoursesContainer, container))

    def test_setitem_name_ne_code(self):
        # If we add a course under a wrong name that will give an error
        container = CoursesContainer()
        course = Course(code='MYCOURSE')
        self.assertRaises(
            ValueError,
            container.__setitem__, 'NOTMYCOURSE', course)
