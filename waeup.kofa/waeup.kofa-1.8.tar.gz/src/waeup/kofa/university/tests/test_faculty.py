## $Id: test_faculty.py 7811 2012-03-08 19:00:51Z uli $
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

# Test faculties
import tempfile
import shutil
import unittest
from zope.interface.verify import verifyObject, verifyClass
from waeup.kofa.university import Faculty, Department
from waeup.kofa.university.interfaces import IFaculty, IDepartment

class FacultyAndDepartmentTests(unittest.TestCase):

    def test_ifaces(self):
        # Make sure we implement the promised interfaces
        fac = Faculty()
        verifyClass(IFaculty, Faculty)
        verifyObject(IFaculty, fac)
        dep = Department()
        verifyClass(IDepartment, Department)
        verifyObject(IDepartment, dep)
        return
