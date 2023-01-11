## $Id: test_container.py 13165 2015-07-13 07:53:26Z henrik $
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
Tests for students containers.
"""
import tempfile
import shutil
from zope.interface.verify import verifyClass, verifyObject
from zope.component.hooks import setSite, clearSite
from waeup.kofa.app import University
from waeup.kofa.university.department import Department
from waeup.kofa.students.interfaces import (
    IStudentsContainer,
    )
from waeup.kofa.students.container import (
    StudentsContainer, 
    )
from waeup.kofa.testing import (
    FunctionalLayer, FunctionalTestCase, remove_logger)

class StudentsContainerTestCase(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        remove_logger('waeup.kofa.app.students')
        super(StudentsContainerTestCase, self).setUp()
        # Setup a sample site for each test
        # Prepopulate the ZODB...
        app = University()
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']
        setSite(self.app)
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)
        return

    def tearDown(self):
        super(StudentsContainerTestCase, self).tearDown()
        clearSite()
        shutil.rmtree(self.dc_root)
        return

    def test_interfaces(self):
        # Make sure the correct interfaces are implemented.
        self.assertTrue(
            verifyClass(
                IStudentsContainer, StudentsContainer)
            )
        self.assertTrue(
            verifyObject(
                IStudentsContainer, StudentsContainer())
            )
        return

    def test_base(self):
        # We cannot call the fundamental methods of a base in that case
        container = StudentsContainer()
        # We cannot add arbitrary objects
        department = Department()
        self.assertRaises(
            TypeError, container.addStudent, department)


    def test_logger(self):
        # We can get a logger from root
        logger = self.app['students'].logger
        assert logger is not None
        assert logger.name == 'waeup.kofa.app.students'
        handlers = logger.handlers
        assert len(handlers) == 1
        filename = logger.handlers[0].baseFilename
        assert filename.endswith('students.log')
        assert filename.startswith(self.dc_root)

    def test_logger_multiple(self):
        # Make sure the logger is still working after 2nd call
        # First time we call it, it might be registered
        logger = self.app['students'].logger
        # At second call the already registered logger should be returned
        logger = self.app['students'].logger
        assert logger is not None
        assert logger.name == 'waeup.kofa.app.students'
        handlers = logger.handlers
        assert len(handlers) == 1
        filename = logger.handlers[0].baseFilename
        assert filename.endswith('students.log')
        assert filename.startswith(self.dc_root)
