#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .surface_id_val import surface_id_val
from .min_feature_size import min_feature_size
from .proj_plane_norm_comp import proj_plane_norm_comp
class projected_surface_area(Command):
    """
    Print total area of the projection of a group of surfaces to a plane.
    
    Parameters
    ----------
        surface_id_val : typing.List[int]
            'surface_id_val' child.
        min_feature_size : real
            'min_feature_size' child.
        proj_plane_norm_comp : typing.Tuple[real, real, real]
            'proj_plane_norm_comp' child.
    
    """

    fluent_name = "projected-surface-area"

    argument_names = \
        ['surface_id_val', 'min_feature_size', 'proj_plane_norm_comp']

    surface_id_val: surface_id_val = surface_id_val
    """
    surface_id_val argument of projected_surface_area.
    """
    min_feature_size: min_feature_size = min_feature_size
    """
    min_feature_size argument of projected_surface_area.
    """
    proj_plane_norm_comp: proj_plane_norm_comp = proj_plane_norm_comp
    """
    proj_plane_norm_comp argument of projected_surface_area.
    """
