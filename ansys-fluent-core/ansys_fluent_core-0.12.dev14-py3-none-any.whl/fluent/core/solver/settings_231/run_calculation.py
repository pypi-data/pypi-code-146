#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .adaptive_time_stepping import adaptive_time_stepping
from .cfl_based_adaptive_time_stepping import cfl_based_adaptive_time_stepping
from .data_sampling_1 import data_sampling
from .transient_controls import transient_controls
from .pseudo_time_settings import pseudo_time_settings
from .data_sampling_options import data_sampling_options
from .iter_count_2 import iter_count
from .reporting_interval import reporting_interval
from .residual_verbosity import residual_verbosity
from .time_step_count_2 import time_step_count
from .dual_time_iterate import dual_time_iterate
from .iterate import iterate
from .calculate import calculate
from .interrupt import interrupt
from .iterating import iterating
class run_calculation(Group):
    """
    'run_calculation' child.
    """

    fluent_name = "run-calculation"

    child_names = \
        ['adaptive_time_stepping', 'cfl_based_adaptive_time_stepping',
         'data_sampling', 'transient_controls', 'pseudo_time_settings',
         'data_sampling_options', 'iter_count', 'reporting_interval',
         'residual_verbosity', 'time_step_count']

    adaptive_time_stepping: adaptive_time_stepping = adaptive_time_stepping
    """
    adaptive_time_stepping child of run_calculation.
    """
    cfl_based_adaptive_time_stepping: cfl_based_adaptive_time_stepping = cfl_based_adaptive_time_stepping
    """
    cfl_based_adaptive_time_stepping child of run_calculation.
    """
    data_sampling: data_sampling = data_sampling
    """
    data_sampling child of run_calculation.
    """
    transient_controls: transient_controls = transient_controls
    """
    transient_controls child of run_calculation.
    """
    pseudo_time_settings: pseudo_time_settings = pseudo_time_settings
    """
    pseudo_time_settings child of run_calculation.
    """
    data_sampling_options: data_sampling_options = data_sampling_options
    """
    data_sampling_options child of run_calculation.
    """
    iter_count: iter_count = iter_count
    """
    iter_count child of run_calculation.
    """
    reporting_interval: reporting_interval = reporting_interval
    """
    reporting_interval child of run_calculation.
    """
    residual_verbosity: residual_verbosity = residual_verbosity
    """
    residual_verbosity child of run_calculation.
    """
    time_step_count: time_step_count = time_step_count
    """
    time_step_count child of run_calculation.
    """
    command_names = \
        ['dual_time_iterate', 'iterate', 'calculate', 'interrupt']

    dual_time_iterate: dual_time_iterate = dual_time_iterate
    """
    dual_time_iterate command of run_calculation.
    """
    iterate: iterate = iterate
    """
    iterate command of run_calculation.
    """
    calculate: calculate = calculate
    """
    calculate command of run_calculation.
    """
    interrupt: interrupt = interrupt
    """
    interrupt command of run_calculation.
    """
    query_names = \
        ['iterating']

    iterating: iterating = iterating
    """
    iterating query of run_calculation.
    """
