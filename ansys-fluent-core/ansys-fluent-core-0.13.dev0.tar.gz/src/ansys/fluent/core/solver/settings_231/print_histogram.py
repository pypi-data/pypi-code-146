#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .domain import domain
from .cell_function import cell_function
from .min_val import min_val
from .max_val import max_val
from .num_division import num_division
from .set_all_zones import set_all_zones
from .threads_list import threads_list
from .file_name_1 import file_name
from .overwrite import overwrite
class print_histogram(Command):
    """
    Print a histogram of a scalar quantity.
    
    Parameters
    ----------
        domain : str
            'domain' child.
        cell_function : str
            'cell_function' child.
        min_val : real
            'min_val' child.
        max_val : real
            'max_val' child.
        num_division : int
            'num_division' child.
        set_all_zones : bool
            'set_all_zones' child.
        threads_list : typing.List[str]
            'threads_list' child.
        file_name : str
            'file_name' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "print-histogram"

    argument_names = \
        ['domain', 'cell_function', 'min_val', 'max_val', 'num_division',
         'set_all_zones', 'threads_list', 'file_name', 'overwrite']

    domain: domain = domain
    """
    domain argument of print_histogram.
    """
    cell_function: cell_function = cell_function
    """
    cell_function argument of print_histogram.
    """
    min_val: min_val = min_val
    """
    min_val argument of print_histogram.
    """
    max_val: max_val = max_val
    """
    max_val argument of print_histogram.
    """
    num_division: num_division = num_division
    """
    num_division argument of print_histogram.
    """
    set_all_zones: set_all_zones = set_all_zones
    """
    set_all_zones argument of print_histogram.
    """
    threads_list: threads_list = threads_list
    """
    threads_list argument of print_histogram.
    """
    file_name: file_name = file_name
    """
    file_name argument of print_histogram.
    """
    overwrite: overwrite = overwrite
    """
    overwrite argument of print_histogram.
    """
