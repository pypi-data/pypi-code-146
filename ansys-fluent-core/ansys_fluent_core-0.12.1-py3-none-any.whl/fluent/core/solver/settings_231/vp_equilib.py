#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .user_defined_function import user_defined_function
class vp_equilib(Group):
    """
    'vp_equilib' child.
    """

    fluent_name = "vp-equilib"

    child_names = \
        ['option', 'user_defined_function']

    option: option = option
    """
    option child of vp_equilib.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of vp_equilib.
    """
