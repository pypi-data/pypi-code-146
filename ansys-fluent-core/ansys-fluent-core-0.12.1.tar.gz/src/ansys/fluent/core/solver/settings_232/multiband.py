#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .multiband_child import multiband_child

class multiband(NamedObject[multiband_child], _CreatableNamedObjectMixin[multiband_child]):
    """
    Enter multi-band information.
    """

    fluent_name = "multiband"

    child_object_type: multiband_child = multiband_child
    """
    child_object_type of multiband.
    """
