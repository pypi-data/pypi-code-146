## $Id: test_workflow.py 7811 2012-03-08 19:00:51Z uli $
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
import shutil
import tempfile
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase
from waeup.kofa.accesscodes.workflow import (
    invalidate_action, disable_used_action, disable_unused_action,
    reenable_action,
    )

class WorkflowActionsTests(FunctionalTestCase):
    # Tests for helpers like get_access_code, disable_accesscode, ...

    layer = FunctionalLayer

    def setUp(self):
        super(WorkflowActionsTests, self).setUp()
        self.workdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.workdir)
        super(WorkflowActionsTests, self).tearDown()
        return

    def test_actions_wo_parents(self):
        # We can pass contexts without parent to actions
        context = object() # Some fake context without parent
        self.assertTrue(invalidate_action(None, context) is None)
        self.assertTrue(disable_used_action(None, context) is None)
        self.assertTrue(disable_unused_action(None, context) is None)
        self.assertTrue(reenable_action(None, context) is None)
        return
