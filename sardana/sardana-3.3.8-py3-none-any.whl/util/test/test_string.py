# -*- coding: utf-8 -*-

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

from sardana.util.string import camel_to_snake

def test_camel_to_snake():
    assert camel_to_snake("Position") == "position"
    assert camel_to_snake("Acceleration") == "acceleration"
    assert camel_to_snake("DialPosition") == "dial_position"
    assert camel_to_snake("Step_per_unit") == "step_per_unit"
    assert camel_to_snake("Base_rate") == "base_rate"
    assert camel_to_snake("ValueRefPattern") == "value_ref_pattern"