#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .controls import controls
from .methods_1 import methods
from .report_definitions import report_definitions
from .monitor import monitor
from .cell_registers import cell_registers
from .initialization import initialization
from .calculation_activity import calculation_activity
from .run_calculation import run_calculation
class solution(Group):
    """
    'solution' child.
    """

    fluent_name = "solution"

    child_names = \
        ['controls', 'methods', 'report_definitions', 'monitor',
         'cell_registers', 'initialization', 'calculation_activity',
         'run_calculation']

    controls: controls = controls
    """
    controls child of solution.
    """
    methods: methods = methods
    """
    methods child of solution.
    """
    report_definitions: report_definitions = report_definitions
    """
    report_definitions child of solution.
    """
    monitor: monitor = monitor
    """
    monitor child of solution.
    """
    cell_registers: cell_registers = cell_registers
    """
    cell_registers child of solution.
    """
    initialization: initialization = initialization
    """
    initialization child of solution.
    """
    calculation_activity: calculation_activity = calculation_activity
    """
    calculation_activity child of solution.
    """
    run_calculation: run_calculation = run_calculation
    """
    run_calculation child of solution.
    """
