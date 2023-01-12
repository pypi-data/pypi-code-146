#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_3 import option
from .max_number_of_refinements import max_number_of_refinements
from .tolerance import tolerance
class accuracy_control(Group):
    """
    'accuracy_control' child.
    """

    fluent_name = "accuracy-control"

    child_names = \
        ['option', 'max_number_of_refinements', 'tolerance']

    option: option = option
    """
    option child of accuracy_control.
    """
    max_number_of_refinements: max_number_of_refinements = max_number_of_refinements
    """
    max_number_of_refinements child of accuracy_control.
    """
    tolerance: tolerance = tolerance
    """
    tolerance child of accuracy_control.
    """
