#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .bodies import bodies
from .groups import groups
class parts_child(Group):
    """
    'child_object_type' of parts.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['bodies', 'groups']

    bodies: bodies = bodies
    """
    bodies child of parts_child.
    """
    groups: groups = groups
    """
    groups child of parts_child.
    """
