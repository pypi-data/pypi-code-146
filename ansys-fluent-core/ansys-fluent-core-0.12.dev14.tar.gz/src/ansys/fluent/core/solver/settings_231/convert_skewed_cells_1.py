#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .cell_thread_list import cell_thread_list
from .max_cell_skewness import max_cell_skewness
from .convert_skewed_cells import convert_skewed_cells
class convert_skewed_cells(Command):
    """
    'convert_skewed_cells' command.
    
    Parameters
    ----------
        cell_thread_list : typing.List[str]
            Set zones where cells should be converted.
        max_cell_skewness : real
            Set target maximum cell skewness.
        convert_skewed_cells : bool
            'convert_skewed_cells' child.
    
    """

    fluent_name = "convert-skewed-cells"

    argument_names = \
        ['cell_thread_list', 'max_cell_skewness', 'convert_skewed_cells']

    cell_thread_list: cell_thread_list = cell_thread_list
    """
    cell_thread_list argument of convert_skewed_cells.
    """
    max_cell_skewness: max_cell_skewness = max_cell_skewness
    """
    max_cell_skewness argument of convert_skewed_cells.
    """
    convert_skewed_cells: convert_skewed_cells = convert_skewed_cells
    """
    convert_skewed_cells argument of convert_skewed_cells.
    """
