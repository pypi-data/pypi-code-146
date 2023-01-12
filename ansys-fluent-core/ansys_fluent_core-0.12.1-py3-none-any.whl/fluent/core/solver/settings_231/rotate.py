#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .angle import angle
from .origin import origin
from .axis_components import axis_components
class rotate(Command):
    """
    Rotate the mesh.
    
    Parameters
    ----------
        angle : real
            'angle' child.
        origin : typing.Tuple[real, real, real]
            'origin' child.
        axis_components : typing.Tuple[real, real, real]
            'axis_components' child.
    
    """

    fluent_name = "rotate"

    argument_names = \
        ['angle', 'origin', 'axis_components']

    angle: angle = angle
    """
    angle argument of rotate.
    """
    origin: origin = origin
    """
    origin argument of rotate.
    """
    axis_components: axis_components = axis_components
    """
    axis_components argument of rotate.
    """
