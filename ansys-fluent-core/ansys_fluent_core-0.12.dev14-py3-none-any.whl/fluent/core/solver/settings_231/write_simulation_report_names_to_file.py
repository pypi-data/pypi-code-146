#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .file_path import file_path
class write_simulation_report_names_to_file(Command):
    """
    Write the list of currently generated report names to a txt file.
    
    Parameters
    ----------
        file_path : str
            'file_path' child.
    
    """

    fluent_name = "write-simulation-report-names-to-file"

    argument_names = \
        ['file_path']

    file_path: file_path = file_path
    """
    file_path argument of write_simulation_report_names_to_file.
    """
