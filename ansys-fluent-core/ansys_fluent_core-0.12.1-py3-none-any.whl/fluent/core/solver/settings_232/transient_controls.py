#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .type_1 import type
from .method_1 import method
from .specified_time_step import specified_time_step
from .incremental_time import incremental_time
from .max_iter_per_time_step import max_iter_per_time_step
from .time_step_count_1 import time_step_count
from .total_time_step_count import total_time_step_count
from .total_time import total_time
from .time_step_size import time_step_size
from .solution_status import solution_status
from .extrapolate_vars import extrapolate_vars
from .max_flow_time import max_flow_time
from .control_time_step_size_variation import control_time_step_size_variation
from .use_average_cfl import use_average_cfl
from .cfl_type import cfl_type
from .cfl_based_time_stepping import cfl_based_time_stepping
from .error_based_time_stepping import error_based_time_stepping
from .undo_timestep import undo_timestep
from .predict_next import predict_next
from .rotating_mesh_flow_predictor import rotating_mesh_flow_predictor
from .mp_specific_time_stepping import mp_specific_time_stepping
from .udf_hook import udf_hook
from .fixed_periodic_1 import fixed_periodic
from .duration_specification_method import duration_specification_method
from .multiphase_specific_time_constraints import multiphase_specific_time_constraints
from .solid_time_step_size import solid_time_step_size
from .time_step_size_for_acoustic_export import time_step_size_for_acoustic_export
from .extrapolate_eqn_vars import extrapolate_eqn_vars
class transient_controls(Group):
    """
    'transient_controls' child.
    """

    fluent_name = "transient-controls"

    child_names = \
        ['type', 'method', 'specified_time_step', 'incremental_time',
         'max_iter_per_time_step', 'time_step_count', 'total_time_step_count',
         'total_time', 'time_step_size', 'solution_status',
         'extrapolate_vars', 'max_flow_time',
         'control_time_step_size_variation', 'use_average_cfl', 'cfl_type',
         'cfl_based_time_stepping', 'error_based_time_stepping',
         'undo_timestep', 'predict_next', 'rotating_mesh_flow_predictor',
         'mp_specific_time_stepping', 'udf_hook', 'fixed_periodic',
         'duration_specification_method',
         'multiphase_specific_time_constraints', 'solid_time_step_size',
         'time_step_size_for_acoustic_export', 'extrapolate_eqn_vars']

    type: type = type
    """
    type child of transient_controls.
    """
    method: method = method
    """
    method child of transient_controls.
    """
    specified_time_step: specified_time_step = specified_time_step
    """
    specified_time_step child of transient_controls.
    """
    incremental_time: incremental_time = incremental_time
    """
    incremental_time child of transient_controls.
    """
    max_iter_per_time_step: max_iter_per_time_step = max_iter_per_time_step
    """
    max_iter_per_time_step child of transient_controls.
    """
    time_step_count: time_step_count = time_step_count
    """
    time_step_count child of transient_controls.
    """
    total_time_step_count: total_time_step_count = total_time_step_count
    """
    total_time_step_count child of transient_controls.
    """
    total_time: total_time = total_time
    """
    total_time child of transient_controls.
    """
    time_step_size: time_step_size = time_step_size
    """
    time_step_size child of transient_controls.
    """
    solution_status: solution_status = solution_status
    """
    solution_status child of transient_controls.
    """
    extrapolate_vars: extrapolate_vars = extrapolate_vars
    """
    extrapolate_vars child of transient_controls.
    """
    max_flow_time: max_flow_time = max_flow_time
    """
    max_flow_time child of transient_controls.
    """
    control_time_step_size_variation: control_time_step_size_variation = control_time_step_size_variation
    """
    control_time_step_size_variation child of transient_controls.
    """
    use_average_cfl: use_average_cfl = use_average_cfl
    """
    use_average_cfl child of transient_controls.
    """
    cfl_type: cfl_type = cfl_type
    """
    cfl_type child of transient_controls.
    """
    cfl_based_time_stepping: cfl_based_time_stepping = cfl_based_time_stepping
    """
    cfl_based_time_stepping child of transient_controls.
    """
    error_based_time_stepping: error_based_time_stepping = error_based_time_stepping
    """
    error_based_time_stepping child of transient_controls.
    """
    undo_timestep: undo_timestep = undo_timestep
    """
    undo_timestep child of transient_controls.
    """
    predict_next: predict_next = predict_next
    """
    predict_next child of transient_controls.
    """
    rotating_mesh_flow_predictor: rotating_mesh_flow_predictor = rotating_mesh_flow_predictor
    """
    rotating_mesh_flow_predictor child of transient_controls.
    """
    mp_specific_time_stepping: mp_specific_time_stepping = mp_specific_time_stepping
    """
    mp_specific_time_stepping child of transient_controls.
    """
    udf_hook: udf_hook = udf_hook
    """
    udf_hook child of transient_controls.
    """
    fixed_periodic: fixed_periodic = fixed_periodic
    """
    fixed_periodic child of transient_controls.
    """
    duration_specification_method: duration_specification_method = duration_specification_method
    """
    duration_specification_method child of transient_controls.
    """
    multiphase_specific_time_constraints: multiphase_specific_time_constraints = multiphase_specific_time_constraints
    """
    multiphase_specific_time_constraints child of transient_controls.
    """
    solid_time_step_size: solid_time_step_size = solid_time_step_size
    """
    solid_time_step_size child of transient_controls.
    """
    time_step_size_for_acoustic_export: time_step_size_for_acoustic_export = time_step_size_for_acoustic_export
    """
    time_step_size_for_acoustic_export child of transient_controls.
    """
    extrapolate_eqn_vars: extrapolate_eqn_vars = extrapolate_eqn_vars
    """
    extrapolate_eqn_vars child of transient_controls.
    """
