#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_1 import option
from .create_particles_every_particle_step import create_particles_every_particle_step
from .dpm_time_step import dpm_time_step
from .n_time_steps import n_time_steps
from .clear_particles_from_domain import clear_particles_from_domain
class unsteady_tracking(Group):
    """
    'unsteady_tracking' child.
    """

    fluent_name = "unsteady-tracking"

    child_names = \
        ['option', 'create_particles_every_particle_step', 'dpm_time_step',
         'n_time_steps', 'clear_particles_from_domain']

    option: option = option
    """
    option child of unsteady_tracking.
    """
    create_particles_every_particle_step: create_particles_every_particle_step = create_particles_every_particle_step
    """
    create_particles_every_particle_step child of unsteady_tracking.
    """
    dpm_time_step: dpm_time_step = dpm_time_step
    """
    dpm_time_step child of unsteady_tracking.
    """
    n_time_steps: n_time_steps = n_time_steps
    """
    n_time_steps child of unsteady_tracking.
    """
    clear_particles_from_domain: clear_particles_from_domain = clear_particles_from_domain
    """
    clear_particles_from_domain child of unsteady_tracking.
    """
