#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .table_name import table_name
from .column_with_diameters import column_with_diameters
from .column_with_number_fractions import column_with_number_fractions
from .column_with_mass_fractions import column_with_mass_fractions
from .accumulated_number_fraction import accumulated_number_fraction
from .accumulated_mass_fraction import accumulated_mass_fraction
class tabulated_size_settings(Group):
    """
    'tabulated_size_settings' child.
    """

    fluent_name = "tabulated-size-settings"

    child_names = \
        ['table_name', 'column_with_diameters',
         'column_with_number_fractions', 'column_with_mass_fractions',
         'accumulated_number_fraction', 'accumulated_mass_fraction']

    table_name: table_name = table_name
    """
    table_name child of tabulated_size_settings.
    """
    column_with_diameters: column_with_diameters = column_with_diameters
    """
    column_with_diameters child of tabulated_size_settings.
    """
    column_with_number_fractions: column_with_number_fractions = column_with_number_fractions
    """
    column_with_number_fractions child of tabulated_size_settings.
    """
    column_with_mass_fractions: column_with_mass_fractions = column_with_mass_fractions
    """
    column_with_mass_fractions child of tabulated_size_settings.
    """
    accumulated_number_fraction: accumulated_number_fraction = accumulated_number_fraction
    """
    accumulated_number_fraction child of tabulated_size_settings.
    """
    accumulated_mass_fraction: accumulated_mass_fraction = accumulated_mass_fraction
    """
    accumulated_mass_fraction child of tabulated_size_settings.
    """
