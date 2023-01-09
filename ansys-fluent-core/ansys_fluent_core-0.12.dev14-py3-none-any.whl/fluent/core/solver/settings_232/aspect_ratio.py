#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .width import width
from .height import height
class aspect_ratio(Command):
    """
    Set the aspect ratio of the active window.
    
    Parameters
    ----------
        width : real
            'width' child.
        height : real
            'height' child.
    
    """

    fluent_name = "aspect-ratio"

    argument_names = \
        ['width', 'height']

    width: width = width
    """
    width argument of aspect_ratio.
    """
    height: height = height
    """
    height argument of aspect_ratio.
    """
