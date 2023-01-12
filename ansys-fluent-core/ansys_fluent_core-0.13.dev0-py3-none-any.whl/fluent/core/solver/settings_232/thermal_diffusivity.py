#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .species_diffusivity import species_diffusivity
from .user_defined_function import user_defined_function
class thermal_diffusivity(Group):
    """
    'thermal_diffusivity' child.
    """

    fluent_name = "thermal-diffusivity"

    child_names = \
        ['option', 'species_diffusivity', 'user_defined_function']

    option: option = option
    """
    option child of thermal_diffusivity.
    """
    species_diffusivity: species_diffusivity = species_diffusivity
    """
    species_diffusivity child of thermal_diffusivity.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of thermal_diffusivity.
    """
