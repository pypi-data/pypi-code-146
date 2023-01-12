#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .max_fine_relaxations import max_fine_relaxations
from .max_coarse_relaxations import max_coarse_relaxations
class flexible_cycle_parameters(Group):
    """
    'flexible_cycle_parameters' child.
    """

    fluent_name = "flexible-cycle-parameters"

    child_names = \
        ['max_fine_relaxations', 'max_coarse_relaxations']

    max_fine_relaxations: max_fine_relaxations = max_fine_relaxations
    """
    max_fine_relaxations child of flexible_cycle_parameters.
    """
    max_coarse_relaxations: max_coarse_relaxations = max_coarse_relaxations
    """
    max_coarse_relaxations child of flexible_cycle_parameters.
    """
