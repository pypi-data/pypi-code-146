#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .include_pop_in_fsi_force import include_pop_in_fsi_force
from .steady_2way_fsi import steady_2way_fsi
from .include_viscous_fsi_force import include_viscous_fsi_force
from .explicit_fsi_force import explicit_fsi_force
from .starting_t_re_initialization import starting_t_re_initialization
class expert(Group):
    """
    Enter the structure expert menu.
    """

    fluent_name = "expert"

    child_names = \
        ['include_pop_in_fsi_force', 'steady_2way_fsi',
         'include_viscous_fsi_force', 'explicit_fsi_force',
         'starting_t_re_initialization']

    include_pop_in_fsi_force: include_pop_in_fsi_force = include_pop_in_fsi_force
    """
    include_pop_in_fsi_force child of expert.
    """
    steady_2way_fsi: steady_2way_fsi = steady_2way_fsi
    """
    steady_2way_fsi child of expert.
    """
    include_viscous_fsi_force: include_viscous_fsi_force = include_viscous_fsi_force
    """
    include_viscous_fsi_force child of expert.
    """
    explicit_fsi_force: explicit_fsi_force = explicit_fsi_force
    """
    explicit_fsi_force child of expert.
    """
    starting_t_re_initialization: starting_t_re_initialization = starting_t_re_initialization
    """
    starting_t_re_initialization child of expert.
    """
