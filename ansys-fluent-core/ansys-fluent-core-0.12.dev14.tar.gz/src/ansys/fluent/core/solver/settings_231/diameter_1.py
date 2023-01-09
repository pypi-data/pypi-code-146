#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .diameter import diameter
from .diameter_2 import diameter_2
from .option_2 import option
from .rosin_rammler_settings import rosin_rammler_settings
from .tabulated_size_settings import tabulated_size_settings
class diameter(Group):
    """
    'diameter' child.
    """

    fluent_name = "diameter"

    child_names = \
        ['diameter', 'diameter_2', 'option', 'rosin_rammler_settings',
         'tabulated_size_settings']

    diameter: diameter = diameter
    """
    diameter child of diameter.
    """
    diameter_2: diameter_2 = diameter_2
    """
    diameter_2 child of diameter.
    """
    option: option = option
    """
    option child of diameter.
    """
    rosin_rammler_settings: rosin_rammler_settings = rosin_rammler_settings
    """
    rosin_rammler_settings child of diameter.
    """
    tabulated_size_settings: tabulated_size_settings = tabulated_size_settings
    """
    tabulated_size_settings child of diameter.
    """
