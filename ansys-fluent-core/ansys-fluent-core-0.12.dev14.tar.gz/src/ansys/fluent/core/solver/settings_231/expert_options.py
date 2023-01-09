#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .parallel_verbosity_level import parallel_verbosity_level
from .crossover_tolerance import crossover_tolerance
class expert_options(Group):
    """
    'expert_options' child.
    """

    fluent_name = "expert-options"

    child_names = \
        ['parallel_verbosity_level', 'crossover_tolerance']

    parallel_verbosity_level: parallel_verbosity_level = parallel_verbosity_level
    """
    parallel_verbosity_level child of expert_options.
    """
    crossover_tolerance: crossover_tolerance = crossover_tolerance
    """
    crossover_tolerance child of expert_options.
    """
