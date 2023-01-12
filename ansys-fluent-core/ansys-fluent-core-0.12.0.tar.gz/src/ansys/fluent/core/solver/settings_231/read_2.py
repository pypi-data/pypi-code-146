#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .filename import filename
from .unit import unit
class read(Command):
    """
    Read surface meshes.
    
    Parameters
    ----------
        filename : str
            'filename' child.
        unit : str
            'unit' child.
    
    """

    fluent_name = "read"

    argument_names = \
        ['filename', 'unit']

    filename: filename = filename
    """
    filename argument of read.
    """
    unit: unit = unit
    """
    unit argument of read.
    """
