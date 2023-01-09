#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .command_name_1 import command_name
from .tsv_file_name import tsv_file_name
class export(Command):
    """
    Export execute-commands to a TSV file.
    
    Parameters
    ----------
        command_name : typing.List[str]
            'command_name' child.
        tsv_file_name : str
            'tsv_file_name' child.
    
    """

    fluent_name = "export"

    argument_names = \
        ['command_name', 'tsv_file_name']

    command_name: command_name = command_name
    """
    command_name argument of export.
    """
    tsv_file_name: tsv_file_name = tsv_file_name
    """
    tsv_file_name argument of export.
    """
