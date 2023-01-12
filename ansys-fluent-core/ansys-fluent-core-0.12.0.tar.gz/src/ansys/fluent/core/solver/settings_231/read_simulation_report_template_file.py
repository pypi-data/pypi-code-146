#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .file_name_path_1 import file_name_path
class read_simulation_report_template_file(Command):
    """
    Read a JSON template file with existing Simulation Report settings.
    
    Parameters
    ----------
        file_name_path : str
            'file_name_path' child.
    
    """

    fluent_name = "read-simulation-report-template-file"

    argument_names = \
        ['file_name_path']

    file_name_path: file_name_path = file_name_path
    """
    file_name_path argument of read_simulation_report_template_file.
    """
