#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .cell_function_1 import cell_function
from .load_distribution import load_distribution
from .merge import merge
from .partition_origin_vector import partition_origin_vector
from .pre_test_1 import pre_test
from .smooth_1 import smooth
from .print_verbosity import print_verbosity
from .origin import origin
from .laplace_smoothing import laplace_smoothing
from .nfaces_as_weights_1 import nfaces_as_weights
from .face_area_as_weights import face_area_as_weights
from .layering import layering
from .solid_thread_weight import solid_thread_weight
from .stretched_mesh_enhancement import stretched_mesh_enhancement
from .particle_weight import particle_weight
from .vof_free_surface_weight import vof_free_surface_weight
from .isat_weight import isat_weight
from .fluid_solid_rebalance_after_read_case import fluid_solid_rebalance_after_read_case
from .model_weighted_partition import model_weighted_partition
from .dpm_load_balancing import dpm_load_balancing
from .across_zones_1 import across_zones
from .all_off import all_off
from .all_on import all_on
class set(Group):
    """
    Enter the menu to set partition parameters.
    """

    fluent_name = "set"

    child_names = \
        ['cell_function', 'load_distribution', 'merge',
         'partition_origin_vector', 'pre_test', 'smooth', 'print_verbosity',
         'origin', 'laplace_smoothing', 'nfaces_as_weights',
         'face_area_as_weights', 'layering', 'solid_thread_weight',
         'stretched_mesh_enhancement', 'particle_weight',
         'vof_free_surface_weight', 'isat_weight',
         'fluid_solid_rebalance_after_read_case', 'model_weighted_partition',
         'dpm_load_balancing']

    cell_function: cell_function = cell_function
    """
    cell_function child of set.
    """
    load_distribution: load_distribution = load_distribution
    """
    load_distribution child of set.
    """
    merge: merge = merge
    """
    merge child of set.
    """
    partition_origin_vector: partition_origin_vector = partition_origin_vector
    """
    partition_origin_vector child of set.
    """
    pre_test: pre_test = pre_test
    """
    pre_test child of set.
    """
    smooth: smooth = smooth
    """
    smooth child of set.
    """
    print_verbosity: print_verbosity = print_verbosity
    """
    print_verbosity child of set.
    """
    origin: origin = origin
    """
    origin child of set.
    """
    laplace_smoothing: laplace_smoothing = laplace_smoothing
    """
    laplace_smoothing child of set.
    """
    nfaces_as_weights: nfaces_as_weights = nfaces_as_weights
    """
    nfaces_as_weights child of set.
    """
    face_area_as_weights: face_area_as_weights = face_area_as_weights
    """
    face_area_as_weights child of set.
    """
    layering: layering = layering
    """
    layering child of set.
    """
    solid_thread_weight: solid_thread_weight = solid_thread_weight
    """
    solid_thread_weight child of set.
    """
    stretched_mesh_enhancement: stretched_mesh_enhancement = stretched_mesh_enhancement
    """
    stretched_mesh_enhancement child of set.
    """
    particle_weight: particle_weight = particle_weight
    """
    particle_weight child of set.
    """
    vof_free_surface_weight: vof_free_surface_weight = vof_free_surface_weight
    """
    vof_free_surface_weight child of set.
    """
    isat_weight: isat_weight = isat_weight
    """
    isat_weight child of set.
    """
    fluid_solid_rebalance_after_read_case: fluid_solid_rebalance_after_read_case = fluid_solid_rebalance_after_read_case
    """
    fluid_solid_rebalance_after_read_case child of set.
    """
    model_weighted_partition: model_weighted_partition = model_weighted_partition
    """
    model_weighted_partition child of set.
    """
    dpm_load_balancing: dpm_load_balancing = dpm_load_balancing
    """
    dpm_load_balancing child of set.
    """
    command_names = \
        ['across_zones', 'all_off', 'all_on']

    across_zones: across_zones = across_zones
    """
    across_zones command of set.
    """
    all_off: all_off = all_off
    """
    all_off command of set.
    """
    all_on: all_on = all_on
    """
    all_on command of set.
    """
