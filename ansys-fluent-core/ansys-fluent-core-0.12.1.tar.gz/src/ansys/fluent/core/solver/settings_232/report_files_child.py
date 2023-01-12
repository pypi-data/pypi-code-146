#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name_1 import name
from .old_props import old_props
from .file_name import file_name
from .frequency import frequency
from .flow_frequency import flow_frequency
from .itr_index import itr_index
from .run_index import run_index
from .frequency_of import frequency_of
from .report_defs import report_defs
from .print_1 import print
from .active import active
from .write_instantaneous_values import write_instantaneous_values
class report_files_child(Group):
    """
    'child_object_type' of report_files.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'old_props', 'file_name', 'frequency', 'flow_frequency',
         'itr_index', 'run_index', 'frequency_of', 'report_defs', 'print',
         'active', 'write_instantaneous_values']

    name: name = name
    """
    name child of report_files_child.
    """
    old_props: old_props = old_props
    """
    old_props child of report_files_child.
    """
    file_name: file_name = file_name
    """
    file_name child of report_files_child.
    """
    frequency: frequency = frequency
    """
    frequency child of report_files_child.
    """
    flow_frequency: flow_frequency = flow_frequency
    """
    flow_frequency child of report_files_child.
    """
    itr_index: itr_index = itr_index
    """
    itr_index child of report_files_child.
    """
    run_index: run_index = run_index
    """
    run_index child of report_files_child.
    """
    frequency_of: frequency_of = frequency_of
    """
    frequency_of child of report_files_child.
    """
    report_defs: report_defs = report_defs
    """
    report_defs child of report_files_child.
    """
    print: print = print
    """
    print child of report_files_child.
    """
    active: active = active
    """
    active child of report_files_child.
    """
    write_instantaneous_values: write_instantaneous_values = write_instantaneous_values
    """
    write_instantaneous_values child of report_files_child.
    """
