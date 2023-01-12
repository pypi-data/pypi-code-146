#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .set_custom_frames import set_custom_frames
from .video_1 import video
from .read_animation import read_animation
from .write_animation import write_animation
from .stored_view import stored_view
class playback(Group):
    """
    'playback' child.
    """

    fluent_name = "playback"

    child_names = \
        ['set_custom_frames', 'video']

    set_custom_frames: set_custom_frames = set_custom_frames
    """
    set_custom_frames child of playback.
    """
    video: video = video
    """
    video child of playback.
    """
    command_names = \
        ['read_animation', 'write_animation', 'stored_view']

    read_animation: read_animation = read_animation
    """
    read_animation command of playback.
    """
    write_animation: write_animation = write_animation
    """
    write_animation command of playback.
    """
    stored_view: stored_view = stored_view
    """
    stored_view command of playback.
    """
