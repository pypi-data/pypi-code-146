#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .report_type import report_type
from .thread_id_list import thread_id_list
from .domain import domain
from .cell_function import cell_function
from .current_domain import current_domain
from .write_to_file import write_to_file
from .file_name_1 import file_name
from .append_data import append_data
from .overwrite import overwrite
class volume_integrals(Command):
    """
    'volume_integrals' command.
    
    Parameters
    ----------
        report_type : str
            'report_type' child.
        thread_id_list : typing.List[str]
            'thread_id_list' child.
        domain : str
            'domain' child.
        cell_function : str
            'cell_function' child.
        current_domain : str
            'current_domain' child.
        write_to_file : bool
            'write_to_file' child.
        file_name : str
            'file_name' child.
        append_data : bool
            'append_data' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "volume-integrals"

    argument_names = \
        ['report_type', 'thread_id_list', 'domain', 'cell_function',
         'current_domain', 'write_to_file', 'file_name', 'append_data',
         'overwrite']

    report_type: report_type = report_type
    """
    report_type argument of volume_integrals.
    """
    thread_id_list: thread_id_list = thread_id_list
    """
    thread_id_list argument of volume_integrals.
    """
    domain: domain = domain
    """
    domain argument of volume_integrals.
    """
    cell_function: cell_function = cell_function
    """
    cell_function argument of volume_integrals.
    """
    current_domain: current_domain = current_domain
    """
    current_domain argument of volume_integrals.
    """
    write_to_file: write_to_file = write_to_file
    """
    write_to_file argument of volume_integrals.
    """
    file_name: file_name = file_name
    """
    file_name argument of volume_integrals.
    """
    append_data: append_data = append_data
    """
    append_data argument of volume_integrals.
    """
    overwrite: overwrite = overwrite
    """
    overwrite argument of volume_integrals.
    """
