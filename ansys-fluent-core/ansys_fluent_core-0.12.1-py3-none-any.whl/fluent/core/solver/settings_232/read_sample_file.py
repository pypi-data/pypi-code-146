#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .sample_file import sample_file
class read_sample_file(Command):
    """
    Read a sample file and add it to the sample list.
    
    Parameters
    ----------
        sample_file : str
            Enter the name of a sample file to be loaded.
    
    """

    fluent_name = "read-sample-file"

    argument_names = \
        ['sample_file']

    sample_file: sample_file = sample_file
    """
    sample_file argument of read_sample_file.
    """
