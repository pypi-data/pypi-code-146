#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .name import name
from .surface_name_list import surface_name_list
from .structural_analysis import structural_analysis
from .write_loads import write_loads
from .loads import loads
class abaqus(Command):
    """
    Write an ABAQUS file.
    
    Parameters
    ----------
        name : str
            'name' child.
        surface_name_list : typing.List[str]
            'surface_name_list' child.
        structural_analysis : bool
            'structural_analysis' child.
        write_loads : bool
            'write_loads' child.
        loads : typing.List[str]
            'loads' child.
    
    """

    fluent_name = "abaqus"

    argument_names = \
        ['name', 'surface_name_list', 'structural_analysis', 'write_loads',
         'loads']

    name: name = name
    """
    name argument of abaqus.
    """
    surface_name_list: surface_name_list = surface_name_list
    """
    surface_name_list argument of abaqus.
    """
    structural_analysis: structural_analysis = structural_analysis
    """
    structural_analysis argument of abaqus.
    """
    write_loads: write_loads = write_loads
    """
    write_loads argument of abaqus.
    """
    loads: loads = loads
    """
    loads argument of abaqus.
    """
