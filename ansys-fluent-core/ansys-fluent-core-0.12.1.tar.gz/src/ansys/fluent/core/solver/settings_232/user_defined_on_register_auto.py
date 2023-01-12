#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .list_properties_3 import list_properties
from .list_1 import list
from .set_1 import set
from .user_defined_on_register_auto_child import user_defined_on_register_auto_child

class user_defined_on_register_auto(NamedObject[user_defined_on_register_auto_child], _CreatableNamedObjectMixin[user_defined_on_register_auto_child]):
    """
    'user_defined_on_register_auto' child.
    """

    fluent_name = "user-defined-on-register-auto"

    command_names = \
        ['list_properties', 'list', 'set']

    list_properties: list_properties = list_properties
    """
    list_properties command of user_defined_on_register_auto.
    """
    list: list = list
    """
    list command of user_defined_on_register_auto.
    """
    set: set = set
    """
    set command of user_defined_on_register_auto.
    """
    child_object_type: user_defined_on_register_auto_child = user_defined_on_register_auto_child
    """
    child_object_type of user_defined_on_register_auto.
    """
