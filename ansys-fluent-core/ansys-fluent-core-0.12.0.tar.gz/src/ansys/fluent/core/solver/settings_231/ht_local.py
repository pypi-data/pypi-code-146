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
class ht_local(Group):
    """
    'ht_local' child.
    """

    fluent_name = "ht-local"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of ht_local.
    """
    value: value = value
    """
    value child of ht_local.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of ht_local.
    """
    field_name: field_name = field_name
    """
    field_name child of ht_local.
    """
    udf: udf = udf
    """
    udf child of ht_local.
    """
