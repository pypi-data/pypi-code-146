#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .radius_ratio import radius_ratio
from .chord import chord
from .twist import twist
from .airfoil_data_file import airfoil_data_file
class geometry_child(Group):
    """
    'child_object_type' of geometry.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['radius_ratio', 'chord', 'twist', 'airfoil_data_file']

    radius_ratio: radius_ratio = radius_ratio
    """
    radius_ratio child of geometry_child.
    """
    chord: chord = chord
    """
    chord child of geometry_child.
    """
    twist: twist = twist
    """
    twist child of geometry_child.
    """
    airfoil_data_file: airfoil_data_file = airfoil_data_file
    """
    airfoil_data_file child of geometry_child.
    """
