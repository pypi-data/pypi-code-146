#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .value import value
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class q_dot(Group):
    """
    'q_dot' child.
    """

    fluent_name = "q-dot"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of q_dot.
    """
    value: value = value
    """
    value child of q_dot.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of q_dot.
    """
    field_name: field_name = field_name
    """
    field_name child of q_dot.
    """
    udf: udf = udf
    """
    udf child of q_dot.
    """
