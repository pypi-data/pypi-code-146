#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .write_summary_to_file import write_summary_to_file
from .file_name_1 import file_name
from .include_in_domains_particles import include_in_domains_particles
from .pick_injection import pick_injection
from .injection_1 import injection
class extended_summary(Command):
    """
    Print extended discrete phase summary report of particle fates, with options.
    
    Parameters
    ----------
        write_summary_to_file : bool
            'write_summary_to_file' child.
        file_name : str
            'file_name' child.
        include_in_domains_particles : bool
            'include_in_domains_particles' child.
        pick_injection : bool
            'pick_injection' child.
        injection : str
            'injection' child.
    
    """

    fluent_name = "extended-summary"

    argument_names = \
        ['write_summary_to_file', 'file_name', 'include_in_domains_particles',
         'pick_injection', 'injection']

    write_summary_to_file: write_summary_to_file = write_summary_to_file
    """
    write_summary_to_file argument of extended_summary.
    """
    file_name: file_name = file_name
    """
    file_name argument of extended_summary.
    """
    include_in_domains_particles: include_in_domains_particles = include_in_domains_particles
    """
    include_in_domains_particles argument of extended_summary.
    """
    pick_injection: pick_injection = pick_injection
    """
    pick_injection argument of extended_summary.
    """
    injection: injection = injection
    """
    injection argument of extended_summary.
    """
