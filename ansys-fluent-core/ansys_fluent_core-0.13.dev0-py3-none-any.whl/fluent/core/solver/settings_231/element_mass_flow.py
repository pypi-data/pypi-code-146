#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .domain_val import domain_val
class element_mass_flow(Command):
    """
    'element_mass_flow' command.
    
    Parameters
    ----------
        domain_val : str
            'domain_val' child.
    
    """

    fluent_name = "element-mass-flow"

    argument_names = \
        ['domain_val']

    domain_val: domain_val = domain_val
    """
    domain_val argument of element_mass_flow.
    """
