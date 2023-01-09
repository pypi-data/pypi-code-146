#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name_1 import name
from .plot_window import plot_window
from .old_props import old_props
from .frequency import frequency
from .flow_frequency import flow_frequency
from .frequency_of import frequency_of
from .report_defs import report_defs
from .print_1 import print
from .title import title
from .x_label import x_label
from .y_label import y_label
from .active import active
from .plot_instantaneous_values import plot_instantaneous_values
class report_plots_child(Group):
    """
    'child_object_type' of report_plots.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'plot_window', 'old_props', 'frequency', 'flow_frequency',
         'frequency_of', 'report_defs', 'print', 'title', 'x_label',
         'y_label', 'active', 'plot_instantaneous_values']

    name: name = name
    """
    name child of report_plots_child.
    """
    plot_window: plot_window = plot_window
    """
    plot_window child of report_plots_child.
    """
    old_props: old_props = old_props
    """
    old_props child of report_plots_child.
    """
    frequency: frequency = frequency
    """
    frequency child of report_plots_child.
    """
    flow_frequency: flow_frequency = flow_frequency
    """
    flow_frequency child of report_plots_child.
    """
    frequency_of: frequency_of = frequency_of
    """
    frequency_of child of report_plots_child.
    """
    report_defs: report_defs = report_defs
    """
    report_defs child of report_plots_child.
    """
    print: print = print
    """
    print child of report_plots_child.
    """
    title: title = title
    """
    title child of report_plots_child.
    """
    x_label: x_label = x_label
    """
    x_label child of report_plots_child.
    """
    y_label: y_label = y_label
    """
    y_label child of report_plots_child.
    """
    active: active = active
    """
    active child of report_plots_child.
    """
    plot_instantaneous_values: plot_instantaneous_values = plot_instantaneous_values
    """
    plot_instantaneous_values child of report_plots_child.
    """
