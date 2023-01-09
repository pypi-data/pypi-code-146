#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .use import use
from .use_user_define_value import use_user_define_value
from .value import value
class solid_thread_weight(Group):
    """
    Use solid thread weights.
    """

    fluent_name = "solid-thread-weight"

    child_names = \
        ['use', 'use_user_define_value', 'value']

    use: use = use
    """
    use child of solid_thread_weight.
    """
    use_user_define_value: use_user_define_value = use_user_define_value
    """
    use_user_define_value child of solid_thread_weight.
    """
    value: value = value
    """
    value child of solid_thread_weight.
    """
