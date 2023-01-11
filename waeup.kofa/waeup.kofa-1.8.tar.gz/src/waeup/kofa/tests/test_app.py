## $Id: test_app.py 14511 2017-02-07 08:33:05Z henrik $
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
import tempfile
import shutil
from hurry.file.interfaces import IFileRetrieval
from zope.component import queryUtility
from zope.component.hooks import setSite
from zope.interface.verify import verifyClass, verifyObject
from waeup.kofa.app import University
from waeup.kofa.interfaces import (
    IUniversity, IJobManager, VIRT_JOBS_CONTAINER_NAME)
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase

class UniversityTests(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(UniversityTests, self).setUp()
        self.workdir = tempfile.mkdtemp()
        self.getRootFolder()['app'] = University()
        self.app = self.getRootFolder()['app']
        return

    def tearDown(self):
        super(UniversityTests, self).tearDown()
        shutil.rmtree(self.workdir)
        return

    def test_ifaces(self):
        university = University()
        assert verifyClass(IUniversity, University)
        assert verifyObject(IUniversity, university)
        return

    def test_IFileRetrieval_utility(self):
        # Make sure we can get a local IFileRetrieval utility
        setSite(self.app)
        result = queryUtility(IFileRetrieval, default=None)
        assert result is not None
        assert IFileRetrieval.providedBy(result)
        return

    def disabled_test_update_plugins(self):
        # We can update plugins
        setSite(self.app)
        del self.app['documents']
        self.app.updatePlugins()
        self.assertTrue('documents' in self.app.keys())
        return

    def test_jobs(self):
        # We can get the global job manager when traversing to it...
        result = self.app.traverse(VIRT_JOBS_CONTAINER_NAME)
        self.assertTrue(IJobManager.providedBy(result))
        return
