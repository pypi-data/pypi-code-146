#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .wall_distance_free import wall_distance_free
from .cjet import cjet
from .creal import creal
from .cnw_sub import cnw_sub
from .cjet_aux import cjet_aux
from .cbf_lam import cbf_lam
from .cbf_tur import cbf_tur
from .geko_defaults import geko_defaults
class geko_options(Group):
    """
    'geko_options' child.
    """

    fluent_name = "geko-options"

    child_names = \
        ['wall_distance_free', 'cjet', 'creal', 'cnw_sub', 'cjet_aux',
         'cbf_lam', 'cbf_tur']

    wall_distance_free: wall_distance_free = wall_distance_free
    """
    wall_distance_free child of geko_options.
    """
    cjet: cjet = cjet
    """
    cjet child of geko_options.
    """
    creal: creal = creal
    """
    creal child of geko_options.
    """
    cnw_sub: cnw_sub = cnw_sub
    """
    cnw_sub child of geko_options.
    """
    cjet_aux: cjet_aux = cjet_aux
    """
    cjet_aux child of geko_options.
    """
    cbf_lam: cbf_lam = cbf_lam
    """
    cbf_lam child of geko_options.
    """
    cbf_tur: cbf_tur = cbf_tur
    """
    cbf_tur child of geko_options.
    """
    command_names = \
        ['geko_defaults']

    geko_defaults: geko_defaults = geko_defaults
    """
    geko_defaults command of geko_options.
    """
