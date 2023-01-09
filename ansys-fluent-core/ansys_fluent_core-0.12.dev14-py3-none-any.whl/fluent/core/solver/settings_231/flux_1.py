#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .flux_child import flux_child

class flux(NamedObject[flux_child], _CreatableNamedObjectMixin[flux_child]):
    """
    'flux' child.
    """

    fluent_name = "flux"

    child_object_type: flux_child = flux_child
    """
    child_object_type of flux.
    """
