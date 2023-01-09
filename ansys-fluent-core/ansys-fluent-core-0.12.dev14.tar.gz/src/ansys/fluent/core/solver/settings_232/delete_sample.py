#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .sample import sample
class delete_sample(Command):
    """
    'delete_sample' command.
    
    Parameters
    ----------
        sample : str
            'sample' child.
    
    """

    fluent_name = "delete-sample"

    argument_names = \
        ['sample']

    sample: sample = sample
    """
    sample argument of delete_sample.
    """
