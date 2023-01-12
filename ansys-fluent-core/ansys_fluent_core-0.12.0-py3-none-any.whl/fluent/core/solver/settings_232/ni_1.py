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
class ni(Group):
    """
    'ni' child.
    """

    fluent_name = "ni"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of ni.
    """
    value: value = value
    """
    value child of ni.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of ni.
    """
    field_name: field_name = field_name
    """
    field_name child of ni.
    """
    udf: udf = udf
    """
    udf child of ni.
    """
