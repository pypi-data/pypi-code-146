#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .check_reduction_wt import check_reduction_wt
from .file_name_1 import file_name
from .overwrite import overwrite
class reduce_picked_sample(Command):
    """
    Reduce a sample after first picking it and setting up all data-reduction options and parameters.
    
    Parameters
    ----------
        check_reduction_wt : bool
            'check_reduction_wt' child.
        file_name : str
            'file_name' child.
        overwrite : bool
            'overwrite' child.
    
    """

    fluent_name = "reduce-picked-sample"

    argument_names = \
        ['check_reduction_wt', 'file_name', 'overwrite']

    check_reduction_wt: check_reduction_wt = check_reduction_wt
    """
    check_reduction_wt argument of reduce_picked_sample.
    """
    file_name: file_name = file_name
    """
    file_name argument of reduce_picked_sample.
    """
    overwrite: overwrite = overwrite
    """
    overwrite argument of reduce_picked_sample.
    """
