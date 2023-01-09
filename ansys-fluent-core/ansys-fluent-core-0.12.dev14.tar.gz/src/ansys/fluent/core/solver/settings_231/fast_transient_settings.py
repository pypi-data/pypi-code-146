#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .runge_kutta import runge_kutta
class fast_transient_settings(Group):
    """
    Enter the fast transient settings menu.
    """

    fluent_name = "fast-transient-settings"

    child_names = \
        ['runge_kutta']

    runge_kutta: runge_kutta = runge_kutta
    """
    runge_kutta child of fast_transient_settings.
    """
