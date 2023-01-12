#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .nist_fluid import nist_fluid
from .lookup_table import lookup_table
from .pressure_points import pressure_points
from .pressure_minimum import pressure_minimum
from .pressure_maximum import pressure_maximum
from .temperature_points import temperature_points
from .temperature_minimum import temperature_minimum
from .temperature_maximum import temperature_maximum
from .saturation_points import saturation_points
class real_gas_nist(Group):
    """
    'real_gas_nist' child.
    """

    fluent_name = "real-gas-nist"

    child_names = \
        ['nist_fluid', 'lookup_table', 'pressure_points', 'pressure_minimum',
         'pressure_maximum', 'temperature_points', 'temperature_minimum',
         'temperature_maximum', 'saturation_points']

    nist_fluid: nist_fluid = nist_fluid
    """
    nist_fluid child of real_gas_nist.
    """
    lookup_table: lookup_table = lookup_table
    """
    lookup_table child of real_gas_nist.
    """
    pressure_points: pressure_points = pressure_points
    """
    pressure_points child of real_gas_nist.
    """
    pressure_minimum: pressure_minimum = pressure_minimum
    """
    pressure_minimum child of real_gas_nist.
    """
    pressure_maximum: pressure_maximum = pressure_maximum
    """
    pressure_maximum child of real_gas_nist.
    """
    temperature_points: temperature_points = temperature_points
    """
    temperature_points child of real_gas_nist.
    """
    temperature_minimum: temperature_minimum = temperature_minimum
    """
    temperature_minimum child of real_gas_nist.
    """
    temperature_maximum: temperature_maximum = temperature_maximum
    """
    temperature_maximum child of real_gas_nist.
    """
    saturation_points: saturation_points = saturation_points
    """
    saturation_points child of real_gas_nist.
    """
