#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .fixed_periodic import fixed_periodic
from .fixed_periodic_type import fixed_periodic_type
from .fixed_periodic_type_value import fixed_periodic_type_value
from .times_step_periods import times_step_periods
from .total_period_run import total_period_run
class fixed_periodic(Group):
    """
    'fixed_periodic' child.
    """

    fluent_name = "fixed-periodic"

    child_names = \
        ['fixed_periodic', 'fixed_periodic_type', 'fixed_periodic_type_value',
         'times_step_periods', 'total_period_run']

    fixed_periodic: fixed_periodic = fixed_periodic
    """
    fixed_periodic child of fixed_periodic.
    """
    fixed_periodic_type: fixed_periodic_type = fixed_periodic_type
    """
    fixed_periodic_type child of fixed_periodic.
    """
    fixed_periodic_type_value: fixed_periodic_type_value = fixed_periodic_type_value
    """
    fixed_periodic_type_value child of fixed_periodic.
    """
    times_step_periods: times_step_periods = times_step_periods
    """
    times_step_periods child of fixed_periodic.
    """
    total_period_run: total_period_run = total_period_run
    """
    total_period_run child of fixed_periodic.
    """
