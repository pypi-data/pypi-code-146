#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .report_name import report_name
from .output_dir import output_dir
class export_simulation_report_as_html(Command):
    """
    Export the provided simulation report as HTML.
    
    Parameters
    ----------
        report_name : str
            'report_name' child.
        output_dir : str
            'output_dir' child.
    
    """

    fluent_name = "export-simulation-report-as-html"

    argument_names = \
        ['report_name', 'output_dir']

    report_name: report_name = report_name
    """
    report_name argument of export_simulation_report_as_html.
    """
    output_dir: output_dir = output_dir
    """
    output_dir argument of export_simulation_report_as_html.
    """
