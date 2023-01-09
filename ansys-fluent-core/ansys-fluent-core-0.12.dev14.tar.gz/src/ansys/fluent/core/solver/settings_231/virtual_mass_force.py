#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_7 import option
from .virtual_mass_factor import virtual_mass_factor
class virtual_mass_force(Group):
    """
    'virtual_mass_force' child.
    """

    fluent_name = "virtual-mass-force"

    child_names = \
        ['option', 'virtual_mass_factor']

    option: option = option
    """
    option child of virtual_mass_force.
    """
    virtual_mass_factor: virtual_mass_factor = virtual_mass_factor
    """
    virtual_mass_factor child of virtual_mass_force.
    """
