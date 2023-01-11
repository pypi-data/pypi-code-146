## $Id: test_export.py 9262 2012-10-01 06:36:33Z henrik $
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
import os
import shutil
import tempfile
import unittest
from zope.component import queryUtility
from zope.interface.verify import verifyObject, verifyClass
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from waeup.kofa.interfaces import ICSVExporter
from waeup.kofa.testing import KofaUnitTestLayer, FunctionalLayer
from waeup.kofa.accesscodes.accesscode import (
    AccessCodeBatchContainer, AccessCodeBatch)
from waeup.kofa.accesscodes.export import AccessCodeBatchExporter


class AccessCodeBatchExporterTest(unittest.TestCase):

    layer = FunctionalLayer

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.outfile = os.path.join(self.workdir, 'myoutput.csv')
        return

    def tearDown(self):
        shutil.rmtree(self.workdir)
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = AccessCodeBatchExporter()
        verifyObject(ICSVExporter, obj)
        verifyClass(ICSVExporter, AccessCodeBatchExporter)
        return

    def test_get_as_utility(self):
        # we can get a faculty exporter as utility
        result = queryUtility(ICSVExporter, name="accesscodebatches")
        self.assertTrue(result is not None)
        return

    def test_export_all(self):
        # we can export all faculties in a site
        container = AccessCodeBatchContainer()
        site = {'accesscodes':container}
        batch1 = AccessCodeBatch('now', 'manfred', 'APP', 6.6, 0)
        batch2 = AccessCodeBatch('now', 'manfred', 'SFE', 6.6, 0)
        container.addBatch(batch1)
        container.addBatch(batch2)
        exporter = AccessCodeBatchExporter()
        exporter.export_all(site, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
             'cost,creation_date,creator,disabled_num,entry_num,num,'
             'prefix,used_num,batch_id\r\n6.6,now,manfred,0,0,1,APP,0,APP-1\r\n'
             '6.6,now,manfred,0,0,0,SFE,0,SFE-0\r\n'
            )
        return

