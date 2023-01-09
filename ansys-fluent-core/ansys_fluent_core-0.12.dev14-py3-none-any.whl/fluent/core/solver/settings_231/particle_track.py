#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .display_1 import display
from .copy_3 import copy
from .add_to_graphics import add_to_graphics
from .clear_history import clear_history
from .particle_track_child import particle_track_child

class particle_track(NamedObject[particle_track_child], _CreatableNamedObjectMixin[particle_track_child]):
    """
    'particle_track' child.
    """

    fluent_name = "particle-track"

    command_names = \
        ['display', 'copy', 'add_to_graphics', 'clear_history']

    display: display = display
    """
    display command of particle_track.
    """
    copy: copy = copy
    """
    copy command of particle_track.
    """
    add_to_graphics: add_to_graphics = add_to_graphics
    """
    add_to_graphics command of particle_track.
    """
    clear_history: clear_history = clear_history
    """
    clear_history command of particle_track.
    """
    child_object_type: particle_track_child = particle_track_child
    """
    child_object_type of particle_track.
    """
