#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .x_scale import x_scale
from .y_scale import y_scale
from .z_scale import z_scale
class scale(Command):
    """
    'scale' command.
    
    Parameters
    ----------
        x_scale : real
            'x_scale' child.
        y_scale : real
            'y_scale' child.
        z_scale : real
            'z_scale' child.
    
    """

    fluent_name = "scale"

    argument_names = \
        ['x_scale', 'y_scale', 'z_scale']

    x_scale: x_scale = x_scale
    """
    x_scale argument of scale.
    """
    y_scale: y_scale = y_scale
    """
    y_scale argument of scale.
    """
    z_scale: z_scale = z_scale
    """
    z_scale argument of scale.
    """
