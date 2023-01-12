#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name_1 import name
from .old_props import old_props
from .previous_values_to_consider import previous_values_to_consider
from .initial_values_to_ignore import initial_values_to_ignore
from .iteration_at_creation_or_edit import iteration_at_creation_or_edit
from .stop_criterion import stop_criterion
from .report_defs_1 import report_defs
from .print_1 import print
from .plot import plot
from .cov import cov
from .active import active
from .x_label import x_label
from .previous_values import previous_values
class convergence_reports_child(Group):
    """
    'child_object_type' of convergence_reports.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'old_props', 'previous_values_to_consider',
         'initial_values_to_ignore', 'iteration_at_creation_or_edit',
         'stop_criterion', 'report_defs', 'print', 'plot', 'cov', 'active',
         'x_label', 'previous_values']

    name: name = name
    """
    name child of convergence_reports_child.
    """
    old_props: old_props = old_props
    """
    old_props child of convergence_reports_child.
    """
    previous_values_to_consider: previous_values_to_consider = previous_values_to_consider
    """
    previous_values_to_consider child of convergence_reports_child.
    """
    initial_values_to_ignore: initial_values_to_ignore = initial_values_to_ignore
    """
    initial_values_to_ignore child of convergence_reports_child.
    """
    iteration_at_creation_or_edit: iteration_at_creation_or_edit = iteration_at_creation_or_edit
    """
    iteration_at_creation_or_edit child of convergence_reports_child.
    """
    stop_criterion: stop_criterion = stop_criterion
    """
    stop_criterion child of convergence_reports_child.
    """
    report_defs: report_defs = report_defs
    """
    report_defs child of convergence_reports_child.
    """
    print: print = print
    """
    print child of convergence_reports_child.
    """
    plot: plot = plot
    """
    plot child of convergence_reports_child.
    """
    cov: cov = cov
    """
    cov child of convergence_reports_child.
    """
    active: active = active
    """
    active child of convergence_reports_child.
    """
    x_label: x_label = x_label
    """
    x_label child of convergence_reports_child.
    """
    previous_values: previous_values = previous_values
    """
    previous_values child of convergence_reports_child.
    """
