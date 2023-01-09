#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .lookup_table import lookup_table
from .composition_type import composition_type
from .species_fractions import species_fractions
from .pressure_points import pressure_points
from .pressure_minimum import pressure_minimum
from .pressure_maximum import pressure_maximum
from .temperature_points import temperature_points
from .temperature_minimum import temperature_minimum
from .temperature_maximum import temperature_maximum
class real_gas_nist_mixture(Group):
    """
    'real_gas_nist_mixture' child.
    """

    fluent_name = "real-gas-nist-mixture"

    child_names = \
        ['lookup_table', 'composition_type', 'species_fractions',
         'pressure_points', 'pressure_minimum', 'pressure_maximum',
         'temperature_points', 'temperature_minimum', 'temperature_maximum']

    lookup_table: lookup_table = lookup_table
    """
    lookup_table child of real_gas_nist_mixture.
    """
    composition_type: composition_type = composition_type
    """
    composition_type child of real_gas_nist_mixture.
    """
    species_fractions: species_fractions = species_fractions
    """
    species_fractions child of real_gas_nist_mixture.
    """
    pressure_points: pressure_points = pressure_points
    """
    pressure_points child of real_gas_nist_mixture.
    """
    pressure_minimum: pressure_minimum = pressure_minimum
    """
    pressure_minimum child of real_gas_nist_mixture.
    """
    pressure_maximum: pressure_maximum = pressure_maximum
    """
    pressure_maximum child of real_gas_nist_mixture.
    """
    temperature_points: temperature_points = temperature_points
    """
    temperature_points child of real_gas_nist_mixture.
    """
    temperature_minimum: temperature_minimum = temperature_minimum
    """
    temperature_minimum child of real_gas_nist_mixture.
    """
    temperature_maximum: temperature_maximum = temperature_maximum
    """
    temperature_maximum child of real_gas_nist_mixture.
    """
