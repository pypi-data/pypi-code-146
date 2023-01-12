#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .report_each_line import report_each_line
class chemkin_report_each_line(Command):
    """
    'chemkin_report_each_line' command.
    
    Parameters
    ----------
        report_each_line : bool
            Enable/disable reporting after reading each line.
    
    """

    fluent_name = "chemkin-report-each-line?"

    argument_names = \
        ['report_each_line']

    report_each_line: report_each_line = report_each_line
    """
    report_each_line argument of chemkin_report_each_line.
    """
