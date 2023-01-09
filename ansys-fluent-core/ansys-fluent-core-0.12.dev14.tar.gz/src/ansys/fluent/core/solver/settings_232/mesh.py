#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .adapt import adapt
from .check_before_solve import check_before_solve
from .check_verbosity import check_verbosity
from .enhanced_orthogonal_quality import enhanced_orthogonal_quality
from .matching_tolerance import matching_tolerance
from .show_periodic_shadow_zones import show_periodic_shadow_zones
from .reorder import reorder
from .repair_improve import repair_improve
from .surface_mesh import surface_mesh
from .polyhedra import polyhedra
from .adjacency import adjacency
from .check import check
from .memory_usage import memory_usage
from .mesh_info import mesh_info
from .quality import quality
from .rotate import rotate
from .scale import scale
from .size_info import size_info
from .redistribute_boundary_layer import redistribute_boundary_layer
from .swap_mesh_faces import swap_mesh_faces
from .smooth_mesh import smooth_mesh
from .replace import replace
from .translate import translate
class mesh(Group):
    """
    'mesh' child.
    """

    fluent_name = "mesh"

    child_names = \
        ['adapt', 'check_before_solve', 'check_verbosity',
         'enhanced_orthogonal_quality', 'matching_tolerance',
         'show_periodic_shadow_zones', 'reorder', 'repair_improve',
         'surface_mesh', 'polyhedra']

    adapt: adapt = adapt
    """
    adapt child of mesh.
    """
    check_before_solve: check_before_solve = check_before_solve
    """
    check_before_solve child of mesh.
    """
    check_verbosity: check_verbosity = check_verbosity
    """
    check_verbosity child of mesh.
    """
    enhanced_orthogonal_quality: enhanced_orthogonal_quality = enhanced_orthogonal_quality
    """
    enhanced_orthogonal_quality child of mesh.
    """
    matching_tolerance: matching_tolerance = matching_tolerance
    """
    matching_tolerance child of mesh.
    """
    show_periodic_shadow_zones: show_periodic_shadow_zones = show_periodic_shadow_zones
    """
    show_periodic_shadow_zones child of mesh.
    """
    reorder: reorder = reorder
    """
    reorder child of mesh.
    """
    repair_improve: repair_improve = repair_improve
    """
    repair_improve child of mesh.
    """
    surface_mesh: surface_mesh = surface_mesh
    """
    surface_mesh child of mesh.
    """
    polyhedra: polyhedra = polyhedra
    """
    polyhedra child of mesh.
    """
    command_names = \
        ['adjacency', 'check', 'memory_usage', 'mesh_info', 'quality',
         'rotate', 'scale', 'size_info', 'redistribute_boundary_layer',
         'swap_mesh_faces', 'smooth_mesh', 'replace', 'translate']

    adjacency: adjacency = adjacency
    """
    adjacency command of mesh.
    """
    check: check = check
    """
    check command of mesh.
    """
    memory_usage: memory_usage = memory_usage
    """
    memory_usage command of mesh.
    """
    mesh_info: mesh_info = mesh_info
    """
    mesh_info command of mesh.
    """
    quality: quality = quality
    """
    quality command of mesh.
    """
    rotate: rotate = rotate
    """
    rotate command of mesh.
    """
    scale: scale = scale
    """
    scale command of mesh.
    """
    size_info: size_info = size_info
    """
    size_info command of mesh.
    """
    redistribute_boundary_layer: redistribute_boundary_layer = redistribute_boundary_layer
    """
    redistribute_boundary_layer command of mesh.
    """
    swap_mesh_faces: swap_mesh_faces = swap_mesh_faces
    """
    swap_mesh_faces command of mesh.
    """
    smooth_mesh: smooth_mesh = smooth_mesh
    """
    smooth_mesh command of mesh.
    """
    replace: replace = replace
    """
    replace command of mesh.
    """
    translate: translate = translate
    """
    translate command of mesh.
    """
