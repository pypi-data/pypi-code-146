#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .report_files import report_files
from .report_plots import report_plots
from .convergence_conditions import convergence_conditions
class monitor(Group):
    """
    'monitor' child.
    """

    fluent_name = "monitor"

    child_names = \
        ['report_files', 'report_plots', 'convergence_conditions']

    report_files: report_files = report_files
    """
    report_files child of monitor.
    """
    report_plots: report_plots = report_plots
    """
    report_plots child of monitor.
    """
    convergence_conditions: convergence_conditions = convergence_conditions
    """
    convergence_conditions child of monitor.
    """
