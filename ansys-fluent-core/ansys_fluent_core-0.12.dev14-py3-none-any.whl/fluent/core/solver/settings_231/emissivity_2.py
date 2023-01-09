#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
class emissivity(Group):
    """
    'emissivity' child.
    """

    fluent_name = "emissivity"

    child_names = \
        ['option']

    option: option = option
    """
    option child of emissivity.
    """
