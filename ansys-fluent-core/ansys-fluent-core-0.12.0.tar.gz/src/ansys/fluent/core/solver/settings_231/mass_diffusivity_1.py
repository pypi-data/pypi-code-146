#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .lewis_number import lewis_number
from .mass_diffusivity import mass_diffusivity
from .species_diffusivity import species_diffusivity
from .multicomponent import multicomponent
from .user_defined_function import user_defined_function
class mass_diffusivity(Group):
    """
    'mass_diffusivity' child.
    """

    fluent_name = "mass-diffusivity"

    child_names = \
        ['option', 'lewis_number', 'mass_diffusivity', 'species_diffusivity',
         'multicomponent', 'user_defined_function']

    option: option = option
    """
    option child of mass_diffusivity.
    """
    lewis_number: lewis_number = lewis_number
    """
    lewis_number child of mass_diffusivity.
    """
    mass_diffusivity: mass_diffusivity = mass_diffusivity
    """
    mass_diffusivity child of mass_diffusivity.
    """
    species_diffusivity: species_diffusivity = species_diffusivity
    """
    species_diffusivity child of mass_diffusivity.
    """
    multicomponent: multicomponent = multicomponent
    """
    multicomponent child of mass_diffusivity.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of mass_diffusivity.
    """
