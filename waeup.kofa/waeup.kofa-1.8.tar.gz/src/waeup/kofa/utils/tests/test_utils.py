# -*- coding: utf-8 -*-

## $Id: test_utils.py 15476 2019-06-27 06:07:52Z henrik $
##
## Copyright (C) 2014 Uli Fouquet & Henrik Bettermann
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
import psutil
import sys
import unittest
from waeup.kofa.interfaces import IKofaUtils
from waeup.kofa.utils.utils import KofaUtils
from zope.interface import verify


class KofaUtilsTestCase(unittest.TestCase):

    def setUp(self):
        self.max_vmem = psutil.virtual_memory().total
        self.max_smem = psutil.swap_memory().total

    def get_cleared_util(self):
        # Helper: get a `KofUtil` instance with all values of
        # SYSTEM_MAX_LOAD dict set to ``None``
        util = KofaUtils()
        for key, val in util.SYSTEM_MAX_LOAD.items():
            util.SYSTEM_MAX_LOAD[key] = None
        return util

    def test_iface(self):
        # KofaUtils fullfill IKofaUtils expectations
        utils = KofaUtils()
        verify.verifyClass(IKofaUtils, KofaUtils)
        verify.verifyObject(IKofaUtils, utils)

    def test_expensive_actions_allowed_swap_none(self):
        # unset swap maximum values make KofUtils ignore swap values
        utils = self.get_cleared_util()
        utils.SYSTEM_MAX_LOAD['swap-mem'] = None
        assert utils.expensive_actions_allowed() == True
        # even not-set values won't block us
        del utils.SYSTEM_MAX_LOAD['swap-mem']
        assert utils.expensive_actions_allowed() == True

    @unittest.skipIf(
        psutil.swap_memory().percent >= 99.0,
        reason="System swap use over 99%. Cannot set higher allowed value.")
    def test_expensive_actions_allowed_swap_ok(self):
        # We can react to high swap values
        utils = self.get_cleared_util()
        utils.SYSTEM_MAX_LOAD['swap-mem'] = 99.0           # positive float
        assert utils.expensive_actions_allowed() == True
        utils.SYSTEM_MAX_LOAD['swap-mem'] = -1.0           # negative float
        assert utils.expensive_actions_allowed() == True
        utils.SYSTEM_MAX_LOAD['swap-mem'] = sys.maxint     # positive int
        assert utils.expensive_actions_allowed() == True
        utils.SYSTEM_MAX_LOAD['swap-mem'] = -1             # negative int
        assert utils.expensive_actions_allowed() == True

    @unittest.skipIf(
        not psutil.swap_memory().percent,
        reason="Can test swapping behavior only if actually swapping")
    def test_expensive_actions_allowed_swap_too_much(self):
        # We can react if too much swap is used
        utils = self.get_cleared_util()
        utils.SYSTEM_MAX_LOAD['swap-mem'] = 0.0            # positive float
        assert utils.expensive_actions_allowed() == False
        utils.SYSTEM_MAX_LOAD['swap-mem'] = -100.0         # negative float
        assert utils.expensive_actions_allowed() == False
        utils.SYSTEM_MAX_LOAD['swap-mem'] = 0              # positive int
        assert utils.expensive_actions_allowed() == False
        utils.SYSTEM_MAX_LOAD['swap-mem'] = -(sys.maxint)  # negative int
        assert utils.expensive_actions_allowed() == False

    def test_expensive_actions_allowed_virtmem_none(self):
        # unset virtmem maximum values make KofUtils ignore virtmem values
        utils = self.get_cleared_util()
        utils.SYSTEM_MAX_LOAD['virt-mem'] = None
        assert utils.expensive_actions_allowed() == True
        # even not-set values won't block us
        del utils.SYSTEM_MAX_LOAD['virt-mem']
        assert utils.expensive_actions_allowed() == True

    @unittest.skipIf(
        psutil.virtual_memory().percent >= 99.0,
        reason="System virtmem use over 99%. Cannot set higher allowed value.")
    def test_expensive_actions_allowed_virtmem_ok(self):
        # We can react to high virtmem values
        utils = self.get_cleared_util()
        utils.SYSTEM_MAX_LOAD['virt-mem'] = 99.0           # positive float
        assert utils.expensive_actions_allowed() == True
        utils.SYSTEM_MAX_LOAD['virt-mem'] = -1.0           # negative float
        assert utils.expensive_actions_allowed() == True
        utils.SYSTEM_MAX_LOAD['virt-mem'] = sys.maxint     # positive int
        assert utils.expensive_actions_allowed() == True
        utils.SYSTEM_MAX_LOAD['virt-mem'] = -1             # negative int
        assert utils.expensive_actions_allowed() == True

    @unittest.skipIf(
        not psutil.virtual_memory().percent,
        reason="Can test virtmem behavior only if actually using some")
    def test_expensive_actions_allowed_virtmem_too_much(self):
        # We can react if too much virtmem is used
        utils = self.get_cleared_util()
        utils.SYSTEM_MAX_LOAD['virt-mem'] = 0.0            # positive float
        assert utils.expensive_actions_allowed() == False
        utils.SYSTEM_MAX_LOAD['virt-mem'] = -100.0         # negative float
        assert utils.expensive_actions_allowed() == False
        utils.SYSTEM_MAX_LOAD['virt-mem'] = 0              # positive int
        assert utils.expensive_actions_allowed() == False
        utils.SYSTEM_MAX_LOAD['virt-mem'] = -(sys.maxint)  # negative int
        assert utils.expensive_actions_allowed() == False

    def test_format_float(self):
        format_float= KofaUtils().format_float
        # This is the floating point problem ...
        self.assertEqual(4.6*100, 459.99999999999994)
        # ... which is solved in format_float
        self.assertEqual(format_float(4.6 ,1), '4.6')
        self.assertEqual(format_float(4.6 ,2), '4.60')
        self.assertEqual(format_float(4.6 ,3), '4.600')
        self.assertEqual(format_float(4.6 ,4), '4.6000')
