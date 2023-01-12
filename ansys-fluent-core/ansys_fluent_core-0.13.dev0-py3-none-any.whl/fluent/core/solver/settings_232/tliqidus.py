#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class tliqidus(Group):
    """
    'tliqidus' child.
    """

    fluent_name = "tliqidus"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of tliqidus.
    """
    value: value = value
    """
    value child of tliqidus.
    """
