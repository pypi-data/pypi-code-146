#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .skewness_correction_itr_count import skewness_correction_itr_count
from .neighbor_correction_itr_count import neighbor_correction_itr_count
from .skewness_neighbor_coupling import skewness_neighbor_coupling
from .vof_correction_itr_count import vof_correction_itr_count
from .explicit_momentum_under_relaxation import explicit_momentum_under_relaxation
from .explicit_pressure_under_relaxation import explicit_pressure_under_relaxation
from .flow_courant_number import flow_courant_number
from .volume_fraction_courant_number import volume_fraction_courant_number
from .explicit_volume_fraction_under_relaxation import explicit_volume_fraction_under_relaxation
class p_v_controls(Group):
    """
    'p_v_controls' child.
    """

    fluent_name = "p-v-controls"

    child_names = \
        ['skewness_correction_itr_count', 'neighbor_correction_itr_count',
         'skewness_neighbor_coupling', 'vof_correction_itr_count',
         'explicit_momentum_under_relaxation',
         'explicit_pressure_under_relaxation', 'flow_courant_number',
         'volume_fraction_courant_number',
         'explicit_volume_fraction_under_relaxation']

    skewness_correction_itr_count: skewness_correction_itr_count = skewness_correction_itr_count
    """
    skewness_correction_itr_count child of p_v_controls.
    """
    neighbor_correction_itr_count: neighbor_correction_itr_count = neighbor_correction_itr_count
    """
    neighbor_correction_itr_count child of p_v_controls.
    """
    skewness_neighbor_coupling: skewness_neighbor_coupling = skewness_neighbor_coupling
    """
    skewness_neighbor_coupling child of p_v_controls.
    """
    vof_correction_itr_count: vof_correction_itr_count = vof_correction_itr_count
    """
    vof_correction_itr_count child of p_v_controls.
    """
    explicit_momentum_under_relaxation: explicit_momentum_under_relaxation = explicit_momentum_under_relaxation
    """
    explicit_momentum_under_relaxation child of p_v_controls.
    """
    explicit_pressure_under_relaxation: explicit_pressure_under_relaxation = explicit_pressure_under_relaxation
    """
    explicit_pressure_under_relaxation child of p_v_controls.
    """
    flow_courant_number: flow_courant_number = flow_courant_number
    """
    flow_courant_number child of p_v_controls.
    """
    volume_fraction_courant_number: volume_fraction_courant_number = volume_fraction_courant_number
    """
    volume_fraction_courant_number child of p_v_controls.
    """
    explicit_volume_fraction_under_relaxation: explicit_volume_fraction_under_relaxation = explicit_volume_fraction_under_relaxation
    """
    explicit_volume_fraction_under_relaxation child of p_v_controls.
    """
