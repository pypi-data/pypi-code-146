#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .heat_exchanger import heat_exchanger
from .fluid_zone import fluid_zone
from .boundary_zone import boundary_zone
from .report_type import report_type
from .write_to_file import write_to_file
from .file_name_1 import file_name
from .append_file import append_file
from .overwrite import overwrite
class specific_heat(Command):
    """
    'specific_heat' command.
    
    Parameters
    ----------
        heat_exchanger : str
            'heat_exchanger' child.
        fluid_zone : str
            'fluid_zone' child.
        boundary_zone : str
            'boundary_zone' child.
        report_type : str
            'report_type' child.
        write_to_file : bool
            'write_to_file' child.
        file_name : str
            'file_name' child.
        append_file : bool
            'append_file' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "specific-heat"

    argument_names = \
        ['heat_exchanger', 'fluid_zone', 'boundary_zone', 'report_type',
         'write_to_file', 'file_name', 'append_file', 'overwrite']

    heat_exchanger: heat_exchanger = heat_exchanger
    """
    heat_exchanger argument of specific_heat.
    """
    fluid_zone: fluid_zone = fluid_zone
    """
    fluid_zone argument of specific_heat.
    """
    boundary_zone: boundary_zone = boundary_zone
    """
    boundary_zone argument of specific_heat.
    """
    report_type: report_type = report_type
    """
    report_type argument of specific_heat.
    """
    write_to_file: write_to_file = write_to_file
    """
    write_to_file argument of specific_heat.
    """
    file_name: file_name = file_name
    """
    file_name argument of specific_heat.
    """
    append_file: append_file = append_file
    """
    append_file argument of specific_heat.
    """
    overwrite: overwrite = overwrite
    """
    overwrite argument of specific_heat.
    """
