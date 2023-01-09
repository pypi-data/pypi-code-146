#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .discrete_phase import discrete_phase
from .energy import energy
from .ablation import ablation
from .multiphase import multiphase
from .viscous import viscous
from .optics import optics
from .virtual_blade_model import virtual_blade_model
from .structure import structure
class models(Group):
    """
    'models' child.
    """

    fluent_name = "models"

    child_names = \
        ['discrete_phase', 'energy', 'ablation', 'multiphase', 'viscous',
         'optics', 'virtual_blade_model', 'structure']

    discrete_phase: discrete_phase = discrete_phase
    """
    discrete_phase child of models.
    """
    energy: energy = energy
    """
    energy child of models.
    """
    ablation: ablation = ablation
    """
    ablation child of models.
    """
    multiphase: multiphase = multiphase
    """
    multiphase child of models.
    """
    viscous: viscous = viscous
    """
    viscous child of models.
    """
    optics: optics = optics
    """
    optics child of models.
    """
    virtual_blade_model: virtual_blade_model = virtual_blade_model
    """
    virtual_blade_model child of models.
    """
    structure: structure = structure
    """
    structure child of models.
    """
