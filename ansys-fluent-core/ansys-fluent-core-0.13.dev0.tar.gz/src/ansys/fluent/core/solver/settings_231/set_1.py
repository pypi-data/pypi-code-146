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
class set(Group):
    """
    Edit a definition for automatic poor mesh numerics.
    """

    fluent_name = "set"

    child_names = \
        ['name', 'register', 'frequency', 'active', 'verbosity']

    name: name = name
    """
    name child of set.
    """
    register: register = register
    """
    register child of set.
    """
    frequency: frequency = frequency
    """
    frequency child of set.
    """
    active: active = active
    """
    active child of set.
    """
    verbosity: verbosity = verbosity
    """
    verbosity child of set.
    """
