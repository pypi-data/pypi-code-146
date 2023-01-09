#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .fps import fps
from .format_2 import format
from .quality_1 import quality
from .name_3 import name
from .use_original_resolution import use_original_resolution
from .scale_4 import scale
from .set_standard_resolution import set_standard_resolution
from .width_2 import width
from .height_2 import height
from .advance_quality import advance_quality
class video(Group):
    """
    'video' child.
    """

    fluent_name = "video"

    child_names = \
        ['fps', 'format', 'quality', 'name', 'use_original_resolution',
         'scale', 'set_standard_resolution', 'width', 'height',
         'advance_quality']

    fps: fps = fps
    """
    fps child of video.
    """
    format: format = format
    """
    format child of video.
    """
    quality: quality = quality
    """
    quality child of video.
    """
    name: name = name
    """
    name child of video.
    """
    use_original_resolution: use_original_resolution = use_original_resolution
    """
    use_original_resolution child of video.
    """
    scale: scale = scale
    """
    scale child of video.
    """
    set_standard_resolution: set_standard_resolution = set_standard_resolution
    """
    set_standard_resolution child of video.
    """
    width: width = width
    """
    width child of video.
    """
    height: height = height
    """
    height child of video.
    """
    advance_quality: advance_quality = advance_quality
    """
    advance_quality child of video.
    """
