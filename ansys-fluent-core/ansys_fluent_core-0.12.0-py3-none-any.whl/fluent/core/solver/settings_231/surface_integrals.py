#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .report_type import report_type
from .surface_id import surface_id
from .add_custome_vector import add_custome_vector
from .cust_vec_name import cust_vec_name
from .domain_cx import domain_cx
from .cell_cx import cell_cx
from .domain_cy import domain_cy
from .cell_cy import cell_cy
from .domain_cz import domain_cz
from .cell_cz import cell_cz
from .cust_vec_func import cust_vec_func
from .domain_report import domain_report
from .cell_report import cell_report
from .current_domain import current_domain
from .write_to_file import write_to_file
from .file_name_1 import file_name
from .append_data import append_data
from .overwrite import overwrite
class surface_integrals(Command):
    """
    'surface_integrals' command.
    
    Parameters
    ----------
        report_type : str
            'report_type' child.
        surface_id : typing.List[str]
            'surface_id' child.
        add_custome_vector : bool
            'add_custome_vector' child.
        cust_vec_name : str
            'cust_vec_name' child.
        domain_cx : str
            'domain_cx' child.
        cell_cx : str
            'cell_cx' child.
        domain_cy : str
            'domain_cy' child.
        cell_cy : str
            'cell_cy' child.
        domain_cz : str
            'domain_cz' child.
        cell_cz : str
            'cell_cz' child.
        cust_vec_func : str
            'cust_vec_func' child.
        domain_report : str
            'domain_report' child.
        cell_report : str
            'cell_report' child.
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

    fluent_name = "surface-integrals"

    argument_names = \
        ['report_type', 'surface_id', 'add_custome_vector', 'cust_vec_name',
         'domain_cx', 'cell_cx', 'domain_cy', 'cell_cy', 'domain_cz',
         'cell_cz', 'cust_vec_func', 'domain_report', 'cell_report',
         'current_domain', 'write_to_file', 'file_name', 'append_data',
         'overwrite']

    report_type: report_type = report_type
    """
    report_type argument of surface_integrals.
    """
    surface_id: surface_id = surface_id
    """
    surface_id argument of surface_integrals.
    """
    add_custome_vector: add_custome_vector = add_custome_vector
    """
    add_custome_vector argument of surface_integrals.
    """
    cust_vec_name: cust_vec_name = cust_vec_name
    """
    cust_vec_name argument of surface_integrals.
    """
    domain_cx: domain_cx = domain_cx
    """
    domain_cx argument of surface_integrals.
    """
    cell_cx: cell_cx = cell_cx
    """
    cell_cx argument of surface_integrals.
    """
    domain_cy: domain_cy = domain_cy
    """
    domain_cy argument of surface_integrals.
    """
    cell_cy: cell_cy = cell_cy
    """
    cell_cy argument of surface_integrals.
    """
    domain_cz: domain_cz = domain_cz
    """
    domain_cz argument of surface_integrals.
    """
    cell_cz: cell_cz = cell_cz
    """
    cell_cz argument of surface_integrals.
    """
    cust_vec_func: cust_vec_func = cust_vec_func
    """
    cust_vec_func argument of surface_integrals.
    """
    domain_report: domain_report = domain_report
    """
    domain_report argument of surface_integrals.
    """
    cell_report: cell_report = cell_report
    """
    cell_report argument of surface_integrals.
    """
    current_domain: current_domain = current_domain
    """
    current_domain argument of surface_integrals.
    """
    write_to_file: write_to_file = write_to_file
    """
    write_to_file argument of surface_integrals.
    """
    file_name: file_name = file_name
    """
    file_name argument of surface_integrals.
    """
    append_data: append_data = append_data
    """
    append_data argument of surface_integrals.
    """
    overwrite: overwrite = overwrite
    """
    overwrite argument of surface_integrals.
    """
