#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .convergence_reports import convergence_reports
from .frequency_1 import frequency
from .condition import condition
from .check_for import check_for
class convergence_conditions(Group):
    """
    'convergence_conditions' child.
    """

    fluent_name = "convergence-conditions"

    child_names = \
        ['convergence_reports', 'frequency', 'condition', 'check_for']

    convergence_reports: convergence_reports = convergence_reports
    """
    convergence_reports child of convergence_conditions.
    """
    frequency: frequency = frequency
    """
    frequency child of convergence_conditions.
    """
    condition: condition = condition
    """
    condition child of convergence_conditions.
    """
    check_for: check_for = check_for
    """
    check_for child of convergence_conditions.
    """
