#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .tsv_file_name import tsv_file_name
class import_(Command):
    """
    Import execute-commands from a TSV file.
    
    Parameters
    ----------
        tsv_file_name : str
            'tsv_file_name' child.
    
    """

    fluent_name = "import"

    argument_names = \
        ['tsv_file_name']

    tsv_file_name: tsv_file_name = tsv_file_name
    """
    tsv_file_name argument of import_.
    """
