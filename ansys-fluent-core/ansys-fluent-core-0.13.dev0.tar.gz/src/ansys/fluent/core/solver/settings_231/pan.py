#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .right import right
from .up import up
class pan(Command):
    """
    Adjust the camera position without modifying the position.
    
    Parameters
    ----------
        right : real
            'right' child.
        up : real
            'up' child.
    
    """

    fluent_name = "pan"

    argument_names = \
        ['right', 'up']

    right: right = right
    """
    right argument of pan.
    """
    up: up = up
    """
    up argument of pan.
    """
