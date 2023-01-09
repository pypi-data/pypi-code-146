#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .bitrate_scale import bitrate_scale
from .enable_h264 import enable_h264
from .bitrate import bitrate
from .compression_method import compression_method
from .keyframe import keyframe
class advance_quality(Group):
    """
    Advance Quality setting.
    """

    fluent_name = "advance-quality"

    child_names = \
        ['bitrate_scale', 'enable_h264', 'bitrate', 'compression_method',
         'keyframe']

    bitrate_scale: bitrate_scale = bitrate_scale
    """
    bitrate_scale child of advance_quality.
    """
    enable_h264: enable_h264 = enable_h264
    """
    enable_h264 child of advance_quality.
    """
    bitrate: bitrate = bitrate
    """
    bitrate child of advance_quality.
    """
    compression_method: compression_method = compression_method
    """
    compression_method child of advance_quality.
    """
    keyframe: keyframe = keyframe
    """
    keyframe child of advance_quality.
    """
