#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .injection_names import injection_names
class particle_summary(Command):
    """
    Print summary report for all current particles.
    
    Parameters
    ----------
        injection_names : typing.List[str]
            'injection_names' child.
    
    """

    fluent_name = "particle-summary"

    argument_names = \
        ['injection_names']

    injection_names: injection_names = injection_names
    """
    injection_names argument of particle_summary.
    """
