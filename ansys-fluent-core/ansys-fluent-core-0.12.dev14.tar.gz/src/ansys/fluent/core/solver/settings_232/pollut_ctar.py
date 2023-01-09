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
class pollut_ctar(Group):
    """
    'pollut_ctar' child.
    """

    fluent_name = "pollut-ctar"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of pollut_ctar.
    """
    value: value = value
    """
    value child of pollut_ctar.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of pollut_ctar.
    """
    field_name: field_name = field_name
    """
    field_name child of pollut_ctar.
    """
    udf: udf = udf
    """
    udf child of pollut_ctar.
    """
