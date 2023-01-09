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
class m(Group):
    """
    'm' child.
    """

    fluent_name = "m"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of m.
    """
    value: value = value
    """
    value child of m.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of m.
    """
    field_name: field_name = field_name
    """
    field_name child of m.
    """
    udf: udf = udf
    """
    udf child of m.
    """
