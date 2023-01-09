#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .all_var_num_of_bins import all_var_num_of_bins
class all_variables_number_of_bins(Command):
    """
    Set the number of bins to be used for ALL variables in the data reduction.
    
    Parameters
    ----------
        all_var_num_of_bins : int
            'all_var_num_of_bins' child.
    
    """

    fluent_name = "all-variables-number-of-bins"

    argument_names = \
        ['all_var_num_of_bins']

    all_var_num_of_bins: all_var_num_of_bins = all_var_num_of_bins
    """
    all_var_num_of_bins argument of all_variables_number_of_bins.
    """
