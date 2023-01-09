#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .set_filetype import set_filetype
class set_cgns_export_filetype(Command):
    """
    Select HDF5 or ADF as file format for CGNS.
    
    Parameters
    ----------
        set_filetype : bool
            'set_filetype' child.
    
    """

    fluent_name = "set-cgns-export-filetype"

    argument_names = \
        ['set_filetype']

    set_filetype: set_filetype = set_filetype
    """
    set_filetype argument of set_cgns_export_filetype.
    """
