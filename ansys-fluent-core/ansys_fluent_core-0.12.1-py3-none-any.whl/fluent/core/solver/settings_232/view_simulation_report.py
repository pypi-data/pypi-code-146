#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .report_name import report_name
class view_simulation_report(Command):
    """
    View a simulation report that has already been generated. In batch mode this will print the report's URL.
    
    Parameters
    ----------
        report_name : str
            'report_name' child.
    
    """

    fluent_name = "view-simulation-report"

    argument_names = \
        ['report_name']

    report_name: report_name = report_name
    """
    report_name argument of view_simulation_report.
    """
