#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .display import display
from .lic_child import lic_child

class lic(NamedObject[lic_child], _CreatableNamedObjectMixin[lic_child]):
    """
    'lic' child.
    """

    fluent_name = "lic"

    command_names = \
        ['display']

    display: display = display
    """
    display command of lic.
    """
    child_object_type: lic_child = lic_child
    """
    child_object_type of lic.
    """
