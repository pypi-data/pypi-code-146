#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .use import use
from .user_defined_2 import user_defined
from .value import value
class vof_free_surface_weight(Group):
    """
    Set VOF free surface weight.
    """

    fluent_name = "vof-free-surface-weight"

    child_names = \
        ['use', 'user_defined', 'value']

    use: use = use
    """
    use child of vof_free_surface_weight.
    """
    user_defined: user_defined = user_defined
    """
    user_defined child of vof_free_surface_weight.
    """
    value: value = value
    """
    value child of vof_free_surface_weight.
    """
