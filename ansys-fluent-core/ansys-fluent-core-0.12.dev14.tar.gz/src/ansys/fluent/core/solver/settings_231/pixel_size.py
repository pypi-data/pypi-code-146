#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .width_1 import width
from .height_1 import height
from .margin_1 import margin
class pixel_size(Group):
    """
    'pixel_size' child.
    """

    fluent_name = "pixel-size"

    child_names = \
        ['width', 'height', 'margin']

    width: width = width
    """
    width child of pixel_size.
    """
    height: height = height
    """
    height child of pixel_size.
    """
    margin: margin = margin
    """
    margin child of pixel_size.
    """
