#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .boundary_thread import boundary_thread
from .flat_init import flat_init
from .wavy_surface_init import wavy_surface_init
class open_channel_auto_init(Group):
    """
    Open channel automatic initialization.
    """

    fluent_name = "open-channel-auto-init"

    child_names = \
        ['boundary_thread', 'flat_init', 'wavy_surface_init']

    boundary_thread: boundary_thread = boundary_thread
    """
    boundary_thread child of open_channel_auto_init.
    """
    flat_init: flat_init = flat_init
    """
    flat_init child of open_channel_auto_init.
    """
    wavy_surface_init: wavy_surface_init = wavy_surface_init
    """
    wavy_surface_init child of open_channel_auto_init.
    """
