#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .icing_child import icing_child

class icing(NamedObject[icing_child], _CreatableNamedObjectMixin[icing_child]):
    """
    'icing' child.
    """

    fluent_name = "icing"

    child_object_type: icing_child = icing_child
    """
    child_object_type of icing.
    """
