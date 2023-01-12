#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .background import background
from .color_by_type import color_by_type
from .foreground import foreground
from .by_type import by_type
from .by_surface import by_surface
from .far_field_faces import far_field_faces
from .inlet_faces import inlet_faces
from .interior_faces import interior_faces
from .internal_faces import internal_faces
from .outlet_faces import outlet_faces
from .overset_faces import overset_faces
from .periodic_faces import periodic_faces
from .rans_les_interface_faces import rans_les_interface_faces
from .symmetry_faces import symmetry_faces
from .axis_faces import axis_faces
from .free_surface_faces import free_surface_faces
from .traction_faces import traction_faces
from .wall_faces import wall_faces
from .interface_faces import interface_faces
from .surface_2 import surface
from .skip_label import skip_label
from .automatic_skip import automatic_skip
from .reset_colors import reset_colors
from .list_colors import list_colors
class colors(Group):
    """
    'colors' child.
    """

    fluent_name = "colors"

    child_names = \
        ['background', 'color_by_type', 'foreground', 'by_type', 'by_surface',
         'far_field_faces', 'inlet_faces', 'interior_faces', 'internal_faces',
         'outlet_faces', 'overset_faces', 'periodic_faces',
         'rans_les_interface_faces', 'symmetry_faces', 'axis_faces',
         'free_surface_faces', 'traction_faces', 'wall_faces',
         'interface_faces', 'surface', 'skip_label', 'automatic_skip']

    background: background = background
    """
    background child of colors.
    """
    color_by_type: color_by_type = color_by_type
    """
    color_by_type child of colors.
    """
    foreground: foreground = foreground
    """
    foreground child of colors.
    """
    by_type: by_type = by_type
    """
    by_type child of colors.
    """
    by_surface: by_surface = by_surface
    """
    by_surface child of colors.
    """
    far_field_faces: far_field_faces = far_field_faces
    """
    far_field_faces child of colors.
    """
    inlet_faces: inlet_faces = inlet_faces
    """
    inlet_faces child of colors.
    """
    interior_faces: interior_faces = interior_faces
    """
    interior_faces child of colors.
    """
    internal_faces: internal_faces = internal_faces
    """
    internal_faces child of colors.
    """
    outlet_faces: outlet_faces = outlet_faces
    """
    outlet_faces child of colors.
    """
    overset_faces: overset_faces = overset_faces
    """
    overset_faces child of colors.
    """
    periodic_faces: periodic_faces = periodic_faces
    """
    periodic_faces child of colors.
    """
    rans_les_interface_faces: rans_les_interface_faces = rans_les_interface_faces
    """
    rans_les_interface_faces child of colors.
    """
    symmetry_faces: symmetry_faces = symmetry_faces
    """
    symmetry_faces child of colors.
    """
    axis_faces: axis_faces = axis_faces
    """
    axis_faces child of colors.
    """
    free_surface_faces: free_surface_faces = free_surface_faces
    """
    free_surface_faces child of colors.
    """
    traction_faces: traction_faces = traction_faces
    """
    traction_faces child of colors.
    """
    wall_faces: wall_faces = wall_faces
    """
    wall_faces child of colors.
    """
    interface_faces: interface_faces = interface_faces
    """
    interface_faces child of colors.
    """
    surface: surface = surface
    """
    surface child of colors.
    """
    skip_label: skip_label = skip_label
    """
    skip_label child of colors.
    """
    automatic_skip: automatic_skip = automatic_skip
    """
    automatic_skip child of colors.
    """
    command_names = \
        ['reset_colors', 'list_colors']

    reset_colors: reset_colors = reset_colors
    """
    reset_colors command of colors.
    """
    list_colors: list_colors = list_colors
    """
    list_colors command of colors.
    """
