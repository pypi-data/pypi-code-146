#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .const_number_in_parcel import const_number_in_parcel
from .const_parcel_mass import const_parcel_mass
from .const_parcel_diameter import const_parcel_diameter
class parcel_method(Group):
    """
    'parcel_method' child.
    """

    fluent_name = "parcel-method"

    child_names = \
        ['option', 'const_number_in_parcel', 'const_parcel_mass',
         'const_parcel_diameter']

    option: option = option
    """
    option child of parcel_method.
    """
    const_number_in_parcel: const_number_in_parcel = const_number_in_parcel
    """
    const_number_in_parcel child of parcel_method.
    """
    const_parcel_mass: const_parcel_mass = const_parcel_mass
    """
    const_parcel_mass child of parcel_method.
    """
    const_parcel_diameter: const_parcel_diameter = const_parcel_diameter
    """
    const_parcel_diameter child of parcel_method.
    """
