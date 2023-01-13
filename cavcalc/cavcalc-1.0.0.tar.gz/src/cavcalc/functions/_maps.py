from ..parameters import ParameterType

from .asymmetric import *
from .resonance import *
from .symmetric import *


RESONANCE_TARGETS_FUNC_MAP = {
    fsr: (
        (ParameterType.CAV_LENGTH,),
        ParameterType.FSR,
    ),
    R1_of_T1L1: (
        (ParameterType.TRANSMISSION_M1, ParameterType.LOSS_M1),
        ParameterType.REFLECTIVITY_M1,
    ),
    T1_of_R1L1: (
        (ParameterType.REFLECTIVITY_M1, ParameterType.LOSS_M1),
        ParameterType.TRANSMISSION_M1,
    ),
    R2_of_T2L2: (
        (ParameterType.TRANSMISSION_M2, ParameterType.LOSS_M2),
        ParameterType.REFLECTIVITY_M2,
    ),
    T2_of_R2L2: (
        (ParameterType.REFLECTIVITY_M2, ParameterType.LOSS_M2),
        ParameterType.TRANSMISSION_M2,
    ),
    finesse: (
        (ParameterType.REFLECTIVITY_M1, ParameterType.REFLECTIVITY_M2),
        ParameterType.FINESSE,
    ),
    fwhm: (
        (ParameterType.CAV_LENGTH, ParameterType.REFLECTIVITY_M1, ParameterType.REFLECTIVITY_M2),
        ParameterType.FWHM,
    ),
    pole: (
        (ParameterType.CAV_LENGTH, ParameterType.REFLECTIVITY_M1, ParameterType.REFLECTIVITY_M2),
        ParameterType.POLE,
    ),
}


SYMMETRIC_TARGETS_FUNC_MAP = {
    w_of_gsingle: (
        (ParameterType.CAV_LENGTH, ParameterType.WAVELENGTH, ParameterType.GFACTOR_SINGLE),
        ParameterType.BEAMSIZE,
    ),
    w0_of_gsingle: (
        (ParameterType.CAV_LENGTH, ParameterType.WAVELENGTH, ParameterType.GFACTOR_SINGLE),
        ParameterType.WAISTSIZE,
    ),
    z0_symmetric: (
        (ParameterType.CAV_LENGTH,),
        ParameterType.WAISTPOS,
    ),
    roc_of_gsingle: (
        (ParameterType.CAV_LENGTH, ParameterType.GFACTOR_SINGLE),
        ParameterType.ROC,
    ),
    gsingle_of_roc: ((ParameterType.CAV_LENGTH, ParameterType.ROC), ParameterType.GFACTOR_SINGLE),
    gsingle_of_w: (
        (ParameterType.CAV_LENGTH, ParameterType.WAVELENGTH, ParameterType.BEAMSIZE),
        ParameterType.GFACTOR_SINGLE,
    ),
    gsingle_of_rtgouy: ((ParameterType.GOUY,), ParameterType.GFACTOR_SINGLE),
    gsingle_of_divang: (
        (ParameterType.CAV_LENGTH, ParameterType.WAVELENGTH, ParameterType.DIVERGENCE),
        ParameterType.GFACTOR_SINGLE,
    ),
    gsingle_of_gcav: ((ParameterType.CAV_GFACTOR,), ParameterType.GFACTOR_SINGLE),
    gcav_of_gsingle: ((ParameterType.GFACTOR_SINGLE,), ParameterType.CAV_GFACTOR),
    rtgouy_of_gsingle: (
        (ParameterType.GFACTOR_SINGLE,),
        ParameterType.GOUY,
    ),
    divang_of_gsingle: (
        (ParameterType.CAV_LENGTH, ParameterType.WAVELENGTH, ParameterType.GFACTOR_SINGLE),
        ParameterType.DIVERGENCE,
    ),
    modesep_of_gsingle: (
        (ParameterType.CAV_LENGTH, ParameterType.GFACTOR_SINGLE),
        ParameterType.MODESEP,
    ),
}


ASYMMETRIC_TARGETS_FUNC_MAP = {
    w1_of_g1g2: (
        (
            ParameterType.CAV_LENGTH,
            ParameterType.WAVELENGTH,
            ParameterType.GFACTOR_M1,
            ParameterType.GFACTOR_M2,
        ),
        ParameterType.BEAMSIZE_M1,
    ),
    w2_of_g1g2: (
        (
            ParameterType.CAV_LENGTH,
            ParameterType.WAVELENGTH,
            ParameterType.GFACTOR_M1,
            ParameterType.GFACTOR_M2,
        ),
        ParameterType.BEAMSIZE_M2,
    ),
    w0_of_g1g2: (
        (
            ParameterType.CAV_LENGTH,
            ParameterType.WAVELENGTH,
            ParameterType.GFACTOR_M1,
            ParameterType.GFACTOR_M2,
        ),
        ParameterType.WAISTSIZE,
    ),
    z0_of_g1g2: (
        (ParameterType.CAV_LENGTH, ParameterType.GFACTOR_M1, ParameterType.GFACTOR_M2),
        ParameterType.WAISTPOS,
    ),
    rtgouy_of_g1g2: (
        (ParameterType.GFACTOR_M1, ParameterType.GFACTOR_M2),
        ParameterType.GOUY,
    ),
    g1_of_Rc1: (
        (ParameterType.CAV_LENGTH, ParameterType.ROC_M1),
        ParameterType.GFACTOR_M1,
    ),
    g2_of_Rc2: (
        (ParameterType.CAV_LENGTH, ParameterType.ROC_M2),
        ParameterType.GFACTOR_M2,
    ),
    g1_of_w1w2: (
        (
            ParameterType.CAV_LENGTH,
            ParameterType.WAVELENGTH,
            ParameterType.BEAMSIZE_M1,
            ParameterType.BEAMSIZE_M2,
        ),
        ParameterType.GFACTOR_M1,
    ),
    g2_of_w1w2: (
        (
            ParameterType.CAV_LENGTH,
            ParameterType.WAVELENGTH,
            ParameterType.BEAMSIZE_M1,
            ParameterType.BEAMSIZE_M2,
        ),
        ParameterType.GFACTOR_M2,
    ),
    g_of_g1g2: (
        (ParameterType.GFACTOR_M1, ParameterType.GFACTOR_M2),
        ParameterType.CAV_GFACTOR,
    ),
    Rc1_of_g1: (
        (ParameterType.CAV_LENGTH, ParameterType.GFACTOR_M1),
        ParameterType.ROC_M1,
    ),
    Rc2_of_g2: (
        (ParameterType.CAV_LENGTH, ParameterType.GFACTOR_M2),
        ParameterType.ROC_M2,
    ),
    modesep_of_g1g2: (
        (ParameterType.CAV_LENGTH, ParameterType.GFACTOR_M1, ParameterType.GFACTOR_M2),
        ParameterType.MODESEP,
    ),
}
