"""
The type and category enumerations for parameters.
"""

from enum import auto, Enum


class ParameterType(Enum):
    """An enumeration containing each of the physical parameters
    associated with an optical cavity."""

    BEAMSIZE = auto()
    BEAMSIZE_M1 = auto()
    BEAMSIZE_M2 = auto()
    CAV_GFACTOR = auto()
    CAV_LENGTH = auto()
    DIVERGENCE = auto()
    FINESSE = auto()
    FSR = auto()
    FWHM = auto()
    GFACTOR_M1 = auto()
    GFACTOR_M2 = auto()
    GFACTOR_SINGLE = auto()
    GOUY = auto()
    LOSS_M1 = auto()
    LOSS_M2 = auto()
    MODESEP = auto()
    POLE = auto()
    REFLECTIVITY_M1 = auto()
    REFLECTIVITY_M2 = auto()
    ROC = auto()
    ROC_M1 = auto()
    ROC_M2 = auto()
    TRANSMISSION_M1 = auto()
    TRANSMISSION_M2 = auto()
    WAISTPOS = auto()
    WAISTSIZE = auto()
    WAVELENGTH = auto()


class ParameterCategory(Enum):
    """The categories for each physical parameter type."""

    Angle = auto()
    BeamRadius = auto()
    Curvature = auto()
    Distance = auto()
    Frequency = auto()
    Phase = auto()
    Power = auto()
    Stability = auto()
    Wave = auto()
