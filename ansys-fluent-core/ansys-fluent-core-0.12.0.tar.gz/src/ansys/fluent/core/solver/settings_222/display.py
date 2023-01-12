#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .object_name import object_name
class display(Command):
    """
    'display' command.
    
    Parameters
    ----------
        object_name : str
            'object_name' child.
    
    """

    fluent_name = "display"

    argument_names = \
        ['object_name']

    object_name: object_name = object_name
    """
    object_name argument of display.
    """
