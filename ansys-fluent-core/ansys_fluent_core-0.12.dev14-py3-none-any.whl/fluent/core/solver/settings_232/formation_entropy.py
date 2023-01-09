#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class formation_entropy(Group):
    """
    'formation_entropy' child.
    """

    fluent_name = "formation-entropy"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of formation_entropy.
    """
    value: value = value
    """
    value child of formation_entropy.
    """
