#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .type_1 import type
from .name_1 import name
class copy_by_name(Command):
    """
    Copy a material from the database (pick by name).
    
    Parameters
    ----------
        type : str
            'type' child.
        name : str
            'name' child.
    
    """

    fluent_name = "copy-by-name"

    argument_names = \
        ['type', 'name']

    type: type = type
    """
    type argument of copy_by_name.
    """
    name: name = name
    """
    name argument of copy_by_name.
    """
