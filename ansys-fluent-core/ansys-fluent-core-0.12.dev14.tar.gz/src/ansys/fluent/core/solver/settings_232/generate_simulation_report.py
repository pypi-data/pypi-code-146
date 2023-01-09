#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .report_name import report_name
class generate_simulation_report(Command):
    """
    Generate a new simulation report or regenerate an existing simulation report with the provided name.
    
    Parameters
    ----------
        report_name : str
            'report_name' child.
    
    """

    fluent_name = "generate-simulation-report"

    argument_names = \
        ['report_name']

    report_name: report_name = report_name
    """
    report_name argument of generate_simulation_report.
    """
