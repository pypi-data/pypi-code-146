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
class film_height(Group):
    """
    'film_height' child.
    """

    fluent_name = "film-height"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of film_height.
    """
    value: value = value
    """
    value child of film_height.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of film_height.
    """
    field_name: field_name = field_name
    """
    field_name child of film_height.
    """
    udf: udf = udf
    """
    udf child of film_height.
    """
