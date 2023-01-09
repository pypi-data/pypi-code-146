#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .expert import expert
from .relative_convergence_criterion import relative_convergence_criterion
from .max_iter_per_timestep_count import max_iter_per_timestep_count
class acoustics_wave_eqn_controls(Group):
    """
    Enter menu for acoustics wave equation solver controls.
    """

    fluent_name = "acoustics-wave-eqn-controls"

    child_names = \
        ['expert', 'relative_convergence_criterion',
         'max_iter_per_timestep_count']

    expert: expert = expert
    """
    expert child of acoustics_wave_eqn_controls.
    """
    relative_convergence_criterion: relative_convergence_criterion = relative_convergence_criterion
    """
    relative_convergence_criterion child of acoustics_wave_eqn_controls.
    """
    max_iter_per_timestep_count: max_iter_per_timestep_count = max_iter_per_timestep_count
    """
    max_iter_per_timestep_count child of acoustics_wave_eqn_controls.
    """
