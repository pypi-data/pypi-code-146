#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name_1 import name
from .transparency import transparency
from .colormap_position import colormap_position
from .colormap_left import colormap_left
from .colormap_bottom import colormap_bottom
from .colormap_width import colormap_width
from .colormap_height import colormap_height
class graphics_objects_child(Group):
    """
    'child_object_type' of graphics_objects.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'transparency', 'colormap_position', 'colormap_left',
         'colormap_bottom', 'colormap_width', 'colormap_height']

    name: name = name
    """
    name child of graphics_objects_child.
    """
    transparency: transparency = transparency
    """
    transparency child of graphics_objects_child.
    """
    colormap_position: colormap_position = colormap_position
    """
    colormap_position child of graphics_objects_child.
    """
    colormap_left: colormap_left = colormap_left
    """
    colormap_left child of graphics_objects_child.
    """
    colormap_bottom: colormap_bottom = colormap_bottom
    """
    colormap_bottom child of graphics_objects_child.
    """
    colormap_width: colormap_width = colormap_width
    """
    colormap_width child of graphics_objects_child.
    """
    colormap_height: colormap_height = colormap_height
    """
    colormap_height child of graphics_objects_child.
    """
