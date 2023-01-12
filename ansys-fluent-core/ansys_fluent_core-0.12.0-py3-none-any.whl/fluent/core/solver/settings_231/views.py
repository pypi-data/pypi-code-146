#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .camera import camera
from .display_states import display_states
from .auto_scale_3 import auto_scale
from .reset_to_default_view import reset_to_default_view
from .delete_view import delete_view
from .last_view import last_view
from .next_view import next_view
from .list_views import list_views
from .restore_view import restore_view
from .read_views import read_views
from .save_view import save_view
from .write_views import write_views
class views(Group):
    """
    'views' child.
    """

    fluent_name = "views"

    child_names = \
        ['camera', 'display_states']

    camera: camera = camera
    """
    camera child of views.
    """
    display_states: display_states = display_states
    """
    display_states child of views.
    """
    command_names = \
        ['auto_scale', 'reset_to_default_view', 'delete_view', 'last_view',
         'next_view', 'list_views', 'restore_view', 'read_views', 'save_view',
         'write_views']

    auto_scale: auto_scale = auto_scale
    """
    auto_scale command of views.
    """
    reset_to_default_view: reset_to_default_view = reset_to_default_view
    """
    reset_to_default_view command of views.
    """
    delete_view: delete_view = delete_view
    """
    delete_view command of views.
    """
    last_view: last_view = last_view
    """
    last_view command of views.
    """
    next_view: next_view = next_view
    """
    next_view command of views.
    """
    list_views: list_views = list_views
    """
    list_views command of views.
    """
    restore_view: restore_view = restore_view
    """
    restore_view command of views.
    """
    read_views: read_views = read_views
    """
    read_views command of views.
    """
    save_view: save_view = save_view
    """
    save_view command of views.
    """
    write_views: write_views = write_views
    """
    write_views command of views.
    """
