#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .type_1 import type
class projection(Command):
    """
    Set the camera projection.
    
    Parameters
    ----------
        type : str
            'type' child.
    
    """

    fluent_name = "projection"

    argument_names = \
        ['type']

    type: type = type
    """
    type argument of projection.
    """
