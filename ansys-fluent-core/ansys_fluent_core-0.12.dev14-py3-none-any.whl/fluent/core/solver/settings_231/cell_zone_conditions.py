#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .fluid_1 import fluid
from .solid_1 import solid
from .change_type import change_type
from .activate_cell_zone import activate_cell_zone
from .mrf_to_sliding_mesh import mrf_to_sliding_mesh
from .convert_all_solid_mrf_to_solid_motion import convert_all_solid_mrf_to_solid_motion
from .copy_mrf_to_mesh_motion import copy_mrf_to_mesh_motion
from .copy_mesh_to_mrf_motion import copy_mesh_to_mrf_motion
class cell_zone_conditions(Group, _ChildNamedObjectAccessorMixin):
    """
    'cell_zone_conditions' child.
    """

    fluent_name = "cell-zone-conditions"

    child_names = \
        ['fluid', 'solid']

    fluid: fluid = fluid
    """
    fluid child of cell_zone_conditions.
    """
    solid: solid = solid
    """
    solid child of cell_zone_conditions.
    """
    command_names = \
        ['change_type', 'activate_cell_zone', 'mrf_to_sliding_mesh',
         'convert_all_solid_mrf_to_solid_motion', 'copy_mrf_to_mesh_motion',
         'copy_mesh_to_mrf_motion']

    change_type: change_type = change_type
    """
    change_type command of cell_zone_conditions.
    """
    activate_cell_zone: activate_cell_zone = activate_cell_zone
    """
    activate_cell_zone command of cell_zone_conditions.
    """
    mrf_to_sliding_mesh: mrf_to_sliding_mesh = mrf_to_sliding_mesh
    """
    mrf_to_sliding_mesh command of cell_zone_conditions.
    """
    convert_all_solid_mrf_to_solid_motion: convert_all_solid_mrf_to_solid_motion = convert_all_solid_mrf_to_solid_motion
    """
    convert_all_solid_mrf_to_solid_motion command of cell_zone_conditions.
    """
    copy_mrf_to_mesh_motion: copy_mrf_to_mesh_motion = copy_mrf_to_mesh_motion
    """
    copy_mrf_to_mesh_motion command of cell_zone_conditions.
    """
    copy_mesh_to_mrf_motion: copy_mesh_to_mrf_motion = copy_mesh_to_mrf_motion
    """
    copy_mesh_to_mrf_motion command of cell_zone_conditions.
    """
