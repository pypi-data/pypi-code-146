#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .aeromechanics_child import aeromechanics_child

class aeromechanics(NamedObject[aeromechanics_child], _CreatableNamedObjectMixin[aeromechanics_child]):
    """
    'aeromechanics' child.
    """

    fluent_name = "aeromechanics"

    child_object_type: aeromechanics_child = aeromechanics_child
    """
    child_object_type of aeromechanics.
    """
