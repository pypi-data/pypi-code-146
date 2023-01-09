#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .options_11 import options
from .domain_val import domain_val
from .all_wall_zones import all_wall_zones
from .wall_thread_list import wall_thread_list
from .direction_vector_1 import direction_vector
from .momentum_center import momentum_center
from .momentum_axis import momentum_axis
from .pressure_coordinate import pressure_coordinate
from .coord_val import coord_val
from .write_to_file import write_to_file
from .file_name_1 import file_name
from .append_data import append_data
from .overwrite import overwrite
class forces(Command):
    """
    'forces' command.
    
    Parameters
    ----------
        options : str
            'options' child.
        domain_val : str
            'domain_val' child.
        all_wall_zones : bool
            Select all wall zones available.
        wall_thread_list : typing.List[str]
            'wall_thread_list' child.
        direction_vector : typing.Tuple[real, real, real]
            'direction_vector' child.
        momentum_center : typing.Tuple[real, real, real]
            'momentum_center' child.
        momentum_axis : typing.Tuple[real, real, real]
            'momentum_axis' child.
        pressure_coordinate : str
            'pressure_coordinate' child.
        coord_val : real
            'coord_val' child.
        write_to_file : bool
            'write_to_file' child.
        file_name : str
            'file_name' child.
        append_data : bool
            'append_data' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "forces"

    argument_names = \
        ['options', 'domain_val', 'all_wall_zones', 'wall_thread_list',
         'direction_vector', 'momentum_center', 'momentum_axis',
         'pressure_coordinate', 'coord_val', 'write_to_file', 'file_name',
         'append_data', 'overwrite']

    options: options = options
    """
    options argument of forces.
    """
    domain_val: domain_val = domain_val
    """
    domain_val argument of forces.
    """
    all_wall_zones: all_wall_zones = all_wall_zones
    """
    all_wall_zones argument of forces.
    """
    wall_thread_list: wall_thread_list = wall_thread_list
    """
    wall_thread_list argument of forces.
    """
    direction_vector: direction_vector = direction_vector
    """
    direction_vector argument of forces.
    """
    momentum_center: momentum_center = momentum_center
    """
    momentum_center argument of forces.
    """
    momentum_axis: momentum_axis = momentum_axis
    """
    momentum_axis argument of forces.
    """
    pressure_coordinate: pressure_coordinate = pressure_coordinate
    """
    pressure_coordinate argument of forces.
    """
    coord_val: coord_val = coord_val
    """
    coord_val argument of forces.
    """
    write_to_file: write_to_file = write_to_file
    """
    write_to_file argument of forces.
    """
    file_name: file_name = file_name
    """
    file_name argument of forces.
    """
    append_data: append_data = append_data
    """
    append_data argument of forces.
    """
    overwrite: overwrite = overwrite
    """
    overwrite argument of forces.
    """
