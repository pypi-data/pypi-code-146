#!/usr/bin/env python

##############################################################################
##
# This file is part of Sardana
##
# http://www.sardana-controls.org/
##
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
# Sardana is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# Sardana is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with Sardana.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

"""Tests for set_user_pos macro"""

import unittest
import functools
import tango
from sardana.macroserver.macros.test import RunMacroTestCase, testRun,\
    getMotors

MOT_NAME1, MOT_NAME2 = getMotors()[:2]
Device = functools.lru_cache(maxsize=1024)(tango.DeviceProxy)


@testRun(macro_params=[MOT_NAME1, "1"],
         wait_timeout=1)
class PosTest(RunMacroTestCase, unittest.TestCase):
    """Test case for position macros
    """
    macro_name = "set_user_pos"


    def test_user_pos_update_limit(self):
        proxy = Device(MOT_NAME1)
        Macro_name = "set_user_pos"
        pos_config = proxy.get_attribute_config('Position')
        pos_config.max_value = '5.0'
        pos_config.min_value = '-2.0'
        proxy.set_attribute_config(pos_config)
        proxy.Offset = 1 
        proxy.DefinePosition(1)

        self.macro_runs(Macro_name, [MOT_NAME1, "-1"])
        expected_high_limit = str(3.0)
        expected_low_limit = str(-4.0)
        
        pos_config = proxy.get_attribute_config('Position')
        high_limit = pos_config.max_value
        low_limit = pos_config.min_value
        msg = 'Motor software limit does not equal the expected value'
        self.assertEqual(expected_high_limit, high_limit, msg)
        self.assertEqual(expected_low_limit, low_limit, msg)

    def test_user_pos_without_limit_update(self):
        proxy = Device(MOT_NAME1)
        Macro_name = "set_user_pos"
        pos_config = proxy.get_attribute_config('Position')
        pos_config.max_value = '5.0'
        pos_config.min_value = '-2.0'
        proxy.set_attribute_config(pos_config)
        proxy.Offset = 1
        proxy.DefinePosition(1)

        self.macro_runs(Macro_name, [MOT_NAME1, "-1", "0"])
        expected_high_limit = str(5.0)
        expected_low_limit = str(-2.0)
        
        pos_config = proxy.get_attribute_config('Position')
        high_limit = pos_config.max_value
        low_limit = pos_config.min_value
        msg = 'Motor software limit does not equal the expected value'
        self.assertEqual(expected_high_limit, high_limit, msg)
        self.assertEqual(expected_low_limit, low_limit, msg)
