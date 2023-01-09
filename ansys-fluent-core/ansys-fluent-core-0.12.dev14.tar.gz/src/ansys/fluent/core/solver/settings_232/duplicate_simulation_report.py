#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .report_name import report_name
class duplicate_simulation_report(Command):
    """
    Duplicate the provided simulation report.
    
    Parameters
    ----------
        report_name : str
            'report_name' child.
    
    """

    fluent_name = "duplicate-simulation-report"

    argument_names = \
        ['report_name']

    report_name: report_name = report_name
    """
    report_name argument of duplicate_simulation_report.
    """
