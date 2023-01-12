#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class lennard_jones_length(Group):
    """
    'lennard_jones_length' child.
    """

    fluent_name = "lennard-jones-length"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of lennard_jones_length.
    """
    value: value = value
    """
    value child of lennard_jones_length.
    """
