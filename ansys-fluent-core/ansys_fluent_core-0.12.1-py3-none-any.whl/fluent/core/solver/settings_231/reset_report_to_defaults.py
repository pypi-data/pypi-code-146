#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .report_name import report_name
class reset_report_to_defaults(Command):
    """
    Reset all report settings to default for the provided simulation report.
    
    Parameters
    ----------
        report_name : str
            'report_name' child.
    
    """

    fluent_name = "reset-report-to-defaults"

    argument_names = \
        ['report_name']

    report_name: report_name = report_name
    """
    report_name argument of reset_report_to_defaults.
    """
