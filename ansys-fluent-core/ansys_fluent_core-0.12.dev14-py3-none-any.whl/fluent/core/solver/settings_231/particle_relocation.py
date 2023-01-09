#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .enhanced_cell_relocation_method import enhanced_cell_relocation_method
from .load_legacy_particles import load_legacy_particles
from .overset_relocation_robustness_level import overset_relocation_robustness_level
from .use_legacy_particle_location_method import use_legacy_particle_location_method
class particle_relocation(Group):
    """
    Main menu holding information options to control relocating particles during case file reading or remeshing/adaption.
    """

    fluent_name = "particle-relocation"

    child_names = \
        ['enhanced_cell_relocation_method', 'load_legacy_particles',
         'overset_relocation_robustness_level',
         'use_legacy_particle_location_method']

    enhanced_cell_relocation_method: enhanced_cell_relocation_method = enhanced_cell_relocation_method
    """
    enhanced_cell_relocation_method child of particle_relocation.
    """
    load_legacy_particles: load_legacy_particles = load_legacy_particles
    """
    load_legacy_particles child of particle_relocation.
    """
    overset_relocation_robustness_level: overset_relocation_robustness_level = overset_relocation_robustness_level
    """
    overset_relocation_robustness_level child of particle_relocation.
    """
    use_legacy_particle_location_method: use_legacy_particle_location_method = use_legacy_particle_location_method
    """
    use_legacy_particle_location_method child of particle_relocation.
    """
