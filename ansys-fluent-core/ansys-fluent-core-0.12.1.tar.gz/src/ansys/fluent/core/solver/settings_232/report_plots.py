#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .report_plots_child import report_plots_child

class report_plots(NamedObject[report_plots_child], _CreatableNamedObjectMixin[report_plots_child]):
    """
    'report_plots' child.
    """

    fluent_name = "report-plots"

    child_object_type: report_plots_child = report_plots_child
    """
    child_object_type of report_plots.
    """
