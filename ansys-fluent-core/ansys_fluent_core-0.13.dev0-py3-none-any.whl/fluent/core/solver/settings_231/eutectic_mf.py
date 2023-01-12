#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class eutectic_mf(Group):
    """
    'eutectic_mf' child.
    """

    fluent_name = "eutectic-mf"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of eutectic_mf.
    """
    value: value = value
    """
    value child of eutectic_mf.
    """
