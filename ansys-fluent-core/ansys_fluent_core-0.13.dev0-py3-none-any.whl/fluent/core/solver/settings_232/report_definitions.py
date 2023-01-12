#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .mesh_1 import mesh
from .surface_1 import surface
from .volume import volume
from .force import force
from .lift import lift
from .drag import drag
from .moment import moment
from .flux_1 import flux
from .injection import injection
from .user_defined_1 import user_defined
from .aeromechanics import aeromechanics
from .icing import icing
from .expression_1 import expression
from .single_val_expression import single_val_expression
from .custom import custom
from .compute_1 import compute
from .copy_1 import copy
from .list import list
class report_definitions(Group, _ChildNamedObjectAccessorMixin):
    """
    'report_definitions' child.
    """

    fluent_name = "report-definitions"

    child_names = \
        ['mesh', 'surface', 'volume', 'force', 'lift', 'drag', 'moment',
         'flux', 'injection', 'user_defined', 'aeromechanics', 'icing',
         'expression', 'single_val_expression', 'custom']

    mesh: mesh = mesh
    """
    mesh child of report_definitions.
    """
    surface: surface = surface
    """
    surface child of report_definitions.
    """
    volume: volume = volume
    """
    volume child of report_definitions.
    """
    force: force = force
    """
    force child of report_definitions.
    """
    lift: lift = lift
    """
    lift child of report_definitions.
    """
    drag: drag = drag
    """
    drag child of report_definitions.
    """
    moment: moment = moment
    """
    moment child of report_definitions.
    """
    flux: flux = flux
    """
    flux child of report_definitions.
    """
    injection: injection = injection
    """
    injection child of report_definitions.
    """
    user_defined: user_defined = user_defined
    """
    user_defined child of report_definitions.
    """
    aeromechanics: aeromechanics = aeromechanics
    """
    aeromechanics child of report_definitions.
    """
    icing: icing = icing
    """
    icing child of report_definitions.
    """
    expression: expression = expression
    """
    expression child of report_definitions.
    """
    single_val_expression: single_val_expression = single_val_expression
    """
    single_val_expression child of report_definitions.
    """
    custom: custom = custom
    """
    custom child of report_definitions.
    """
    command_names = \
        ['compute', 'copy', 'list']

    compute: compute = compute
    """
    compute command of report_definitions.
    """
    copy: copy = copy
    """
    copy command of report_definitions.
    """
    list: list = list
    """
    list command of report_definitions.
    """
