#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .playback import playback
class animations(Group):
    """
    'animations' child.
    """

    fluent_name = "animations"

    child_names = \
        ['playback']

    playback: playback = playback
    """
    playback child of animations.
    """
