#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .iter_count import iter_count
from .solution_stabilization_persistence import solution_stabilization_persistence
from .persistence_fixed_time_steps import persistence_fixed_time_steps
from .persistence_fixed_duration import persistence_fixed_duration
from .extrapolation_method import extrapolation_method
class parameters(Group):
    """
    'parameters' child.
    """

    fluent_name = "parameters"

    child_names = \
        ['iter_count', 'solution_stabilization_persistence',
         'persistence_fixed_time_steps', 'persistence_fixed_duration',
         'extrapolation_method']

    iter_count: iter_count = iter_count
    """
    iter_count child of parameters.
    """
    solution_stabilization_persistence: solution_stabilization_persistence = solution_stabilization_persistence
    """
    solution_stabilization_persistence child of parameters.
    """
    persistence_fixed_time_steps: persistence_fixed_time_steps = persistence_fixed_time_steps
    """
    persistence_fixed_time_steps child of parameters.
    """
    persistence_fixed_duration: persistence_fixed_duration = persistence_fixed_duration
    """
    persistence_fixed_duration child of parameters.
    """
    extrapolation_method: extrapolation_method = extrapolation_method
    """
    extrapolation_method child of parameters.
    """
