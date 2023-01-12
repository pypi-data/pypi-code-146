#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .include_convective_heat_transfer import include_convective_heat_transfer
from .include_lwf_particles_in_dpm_concentration import include_lwf_particles_in_dpm_concentration
from .wall_film_temperature_limiter import wall_film_temperature_limiter
class wall_film(Group):
    """
    'wall_film' child.
    """

    fluent_name = "wall-film"

    child_names = \
        ['include_convective_heat_transfer',
         'include_lwf_particles_in_dpm_concentration',
         'wall_film_temperature_limiter']

    include_convective_heat_transfer: include_convective_heat_transfer = include_convective_heat_transfer
    """
    include_convective_heat_transfer child of wall_film.
    """
    include_lwf_particles_in_dpm_concentration: include_lwf_particles_in_dpm_concentration = include_lwf_particles_in_dpm_concentration
    """
    include_lwf_particles_in_dpm_concentration child of wall_film.
    """
    wall_film_temperature_limiter: wall_film_temperature_limiter = wall_film_temperature_limiter
    """
    wall_film_temperature_limiter child of wall_film.
    """
