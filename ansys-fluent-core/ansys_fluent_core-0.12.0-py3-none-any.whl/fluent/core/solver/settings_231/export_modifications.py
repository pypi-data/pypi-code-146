#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .command_list import command_list
from .filename import filename
class export_modifications(Command):
    """
    Export all case modifications to a tsv file.
    
    Parameters
    ----------
        command_list : typing.List[str]
            'command_list' child.
        filename : str
            'filename' child.
    
    """

    fluent_name = "export-modifications"

    argument_names = \
        ['command_list', 'filename']

    command_list: command_list = command_list
    """
    command_list argument of export_modifications.
    """
    filename: filename = filename
    """
    filename argument of export_modifications.
    """
