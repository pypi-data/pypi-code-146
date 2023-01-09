#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .command_name import command_name
class disable(Command):
    """
    Disable an execute-command.
    
    Parameters
    ----------
        command_name : str
            'command_name' child.
    
    """

    fluent_name = "disable"

    argument_names = \
        ['command_name']

    command_name: command_name = command_name
    """
    command_name argument of disable.
    """
