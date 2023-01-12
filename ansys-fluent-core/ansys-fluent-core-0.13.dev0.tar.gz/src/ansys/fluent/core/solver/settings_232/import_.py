#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .create_zones_from_ccl import create_zones_from_ccl
from .read import read
from .chemkin_report_each_line import chemkin_report_each_line
from .import_fmu import import_fmu
class import_(Group):
    """
    'import' child.
    """

    fluent_name = "import"

    child_names = \
        ['create_zones_from_ccl']

    create_zones_from_ccl: create_zones_from_ccl = create_zones_from_ccl
    """
    create_zones_from_ccl child of import_.
    """
    command_names = \
        ['read', 'chemkin_report_each_line', 'import_fmu']

    read: read = read
    """
    read command of import_.
    """
    chemkin_report_each_line: chemkin_report_each_line = chemkin_report_each_line
    """
    chemkin_report_each_line command of import_.
    """
    import_fmu: import_fmu = import_fmu
    """
    import_fmu command of import_.
    """
