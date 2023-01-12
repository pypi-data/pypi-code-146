#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .database_type import database_type
from .copy_by_formula import copy_by_formula
from .copy_by_name import copy_by_name
from .list_materials import list_materials
from .list_properties import list_properties
class database(Group):
    """
    'database' child.
    """

    fluent_name = "database"

    child_names = \
        ['database_type']

    database_type: database_type = database_type
    """
    database_type child of database.
    """
    command_names = \
        ['copy_by_formula', 'copy_by_name', 'list_materials',
         'list_properties']

    copy_by_formula: copy_by_formula = copy_by_formula
    """
    copy_by_formula command of database.
    """
    copy_by_name: copy_by_name = copy_by_name
    """
    copy_by_name command of database.
    """
    list_materials: list_materials = list_materials
    """
    list_materials command of database.
    """
    list_properties: list_properties = list_properties
    """
    list_properties command of database.
    """
