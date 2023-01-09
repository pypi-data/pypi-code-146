#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .moments import moments
from .number_density import number_density
class population_balance(Group):
    """
    'population_balance' child.
    """

    fluent_name = "population-balance"

    command_names = \
        ['moments', 'number_density']

    moments: moments = moments
    """
    moments command of population_balance.
    """
    number_density: number_density = number_density
    """
    number_density command of population_balance.
    """
