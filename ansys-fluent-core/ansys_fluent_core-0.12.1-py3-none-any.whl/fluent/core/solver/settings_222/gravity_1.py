#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .gravity import gravity
from .components import components
class gravity(Group):
    """
    'gravity' child.
    """

    fluent_name = "gravity"

    child_names = \
        ['gravity', 'components']

    gravity: gravity = gravity
    """
    gravity child of gravity.
    """
    components: components = components
    """
    components child of gravity.
    """
