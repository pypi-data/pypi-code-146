#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .start_frame import start_frame
from .end_frame import end_frame
from .increment import increment
class set_custom_frames(Group):
    """
    Set custom frames start, end, skip frames for video export.
    """

    fluent_name = "set-custom-frames"

    child_names = \
        ['start_frame', 'end_frame', 'increment']

    start_frame: start_frame = start_frame
    """
    start_frame child of set_custom_frames.
    """
    end_frame: end_frame = end_frame
    """
    end_frame child of set_custom_frames.
    """
    increment: increment = increment
    """
    increment child of set_custom_frames.
    """
