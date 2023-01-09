#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .retain_instantaneous_values import retain_instantaneous_values
from .list_valid_report_names import list_valid_report_names
from .define import define
from .average_over import average_over
from .old_props import old_props
class single_val_expression_child(Group):
    """
    'child_object_type' of single_val_expression.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['retain_instantaneous_values', 'list_valid_report_names', 'define',
         'average_over', 'old_props']

    retain_instantaneous_values: retain_instantaneous_values = retain_instantaneous_values
    """
    retain_instantaneous_values child of single_val_expression_child.
    """
    list_valid_report_names: list_valid_report_names = list_valid_report_names
    """
    list_valid_report_names child of single_val_expression_child.
    """
    define: define = define
    """
    define child of single_val_expression_child.
    """
    average_over: average_over = average_over
    """
    average_over child of single_val_expression_child.
    """
    old_props: old_props = old_props
    """
    old_props child of single_val_expression_child.
    """
