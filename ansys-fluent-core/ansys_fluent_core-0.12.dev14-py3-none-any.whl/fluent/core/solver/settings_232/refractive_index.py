#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
from .gray_band_coefficients import gray_band_coefficients
class refractive_index(Group):
    """
    'refractive_index' child.
    """

    fluent_name = "refractive-index"

    child_names = \
        ['option', 'value', 'gray_band_coefficients']

    option: option = option
    """
    option child of refractive_index.
    """
    value: value = value
    """
    value child of refractive_index.
    """
    gray_band_coefficients: gray_band_coefficients = gray_band_coefficients
    """
    gray_band_coefficients child of refractive_index.
    """
