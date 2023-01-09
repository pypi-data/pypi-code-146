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
class qdot(Group):
    """
    'qdot' child.
    """

    fluent_name = "qdot"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of qdot.
    """
    value: value = value
    """
    value child of qdot.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of qdot.
    """
    field_name: field_name = field_name
    """
    field_name child of qdot.
    """
    udf: udf = udf
    """
    udf child of qdot.
    """
