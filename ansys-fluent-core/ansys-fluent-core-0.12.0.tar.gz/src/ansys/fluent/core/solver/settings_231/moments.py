#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .surface_list import surface_list
from .volume_list import volume_list
from .num_of_moments import num_of_moments
from .write_to_file import write_to_file
from .filename import filename
from .overwrite import overwrite
class moments(Command):
    """
    Set moments for population balance.
    
    Parameters
    ----------
        surface_list : typing.List[str]
            'surface_list' child.
        volume_list : typing.List[str]
            'volume_list' child.
        num_of_moments : int
            'num_of_moments' child.
        write_to_file : bool
            'write_to_file' child.
        filename : str
            'filename' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "moments"

    argument_names = \
        ['surface_list', 'volume_list', 'num_of_moments', 'write_to_file',
         'filename', 'overwrite']

    surface_list: surface_list = surface_list
    """
    surface_list argument of moments.
    """
    volume_list: volume_list = volume_list
    """
    volume_list argument of moments.
    """
    num_of_moments: num_of_moments = num_of_moments
    """
    num_of_moments argument of moments.
    """
    write_to_file: write_to_file = write_to_file
    """
    write_to_file argument of moments.
    """
    filename: filename = filename
    """
    filename argument of moments.
    """
    overwrite: overwrite = overwrite
    """
    overwrite argument of moments.
    """
