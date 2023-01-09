#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .file_type import file_type
from .file_name_1 import file_name
from .pdf_file_name import pdf_file_name
from .lightweight_setup import lightweight_setup
class read_data(Command):
    """
    'read_data' command.
    
    Parameters
    ----------
        file_type : str
            'file_type' child.
        file_name : str
            'file_name' child.
        pdf_file_name : str
            'pdf_file_name' child.
        lightweight_setup : bool
            'lightweight_setup' child.
    
    """

    fluent_name = "read-data"

    argument_names = \
        ['file_type', 'file_name', 'pdf_file_name', 'lightweight_setup']

    file_type: file_type = file_type
    """
    file_type argument of read_data.
    """
    file_name: file_name = file_name
    """
    file_name argument of read_data.
    """
    pdf_file_name: pdf_file_name = pdf_file_name
    """
    pdf_file_name argument of read_data.
    """
    lightweight_setup: lightweight_setup = lightweight_setup
    """
    lightweight_setup argument of read_data.
    """
