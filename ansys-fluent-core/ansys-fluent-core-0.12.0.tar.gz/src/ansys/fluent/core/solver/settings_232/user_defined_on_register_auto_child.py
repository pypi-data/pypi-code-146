#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name_2 import name
from .register import register
from .frequency_2 import frequency
from .active_1 import active
from .verbosity_6 import verbosity
class user_defined_on_register_auto_child(Group):
    """
    'child_object_type' of user_defined_on_register_auto.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'register', 'frequency', 'active', 'verbosity']

    name: name = name
    """
    name child of user_defined_on_register_auto_child.
    """
    register: register = register
    """
    register child of user_defined_on_register_auto_child.
    """
    frequency: frequency = frequency
    """
    frequency child of user_defined_on_register_auto_child.
    """
    active: active = active
    """
    active child of user_defined_on_register_auto_child.
    """
    verbosity: verbosity = verbosity
    """
    verbosity child of user_defined_on_register_auto_child.
    """
