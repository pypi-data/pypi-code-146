#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class lennard_jones_energy(Group):
    """
    'lennard_jones_energy' child.
    """

    fluent_name = "lennard-jones-energy"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of lennard_jones_energy.
    """
    value: value = value
    """
    value child of lennard_jones_energy.
    """
