#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .refine_mesh import refine_mesh
from .boundary_zones import boundary_zones
from .layer_count import layer_count
from .parameters import parameters
class multi_layer_refinement(Group):
    """
    Enter the multiple boundary layer refinement menu.
    """

    fluent_name = "multi-layer-refinement"

    command_names = \
        ['refine_mesh', 'boundary_zones', 'layer_count', 'parameters']

    refine_mesh: refine_mesh = refine_mesh
    """
    refine_mesh command of multi_layer_refinement.
    """
    boundary_zones: boundary_zones = boundary_zones
    """
    boundary_zones command of multi_layer_refinement.
    """
    layer_count: layer_count = layer_count
    """
    layer_count command of multi_layer_refinement.
    """
    parameters: parameters = parameters
    """
    parameters command of multi_layer_refinement.
    """
