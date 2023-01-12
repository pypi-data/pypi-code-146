#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
from .polynomial import polynomial
class species_diffusivity_child(Group):
    """
    'child_object_type' of species_diffusivity.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['option', 'value', 'polynomial']

    option: option = option
    """
    option child of species_diffusivity_child.
    """
    value: value = value
    """
    value child of species_diffusivity_child.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of species_diffusivity_child.
    """
