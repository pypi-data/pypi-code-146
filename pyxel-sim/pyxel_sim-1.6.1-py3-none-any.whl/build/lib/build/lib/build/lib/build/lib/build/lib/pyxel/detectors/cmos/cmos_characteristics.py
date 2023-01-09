#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""TBW."""
from pyxel.detectors.characteristics import Characteristics


class CMOSCharacteristics(Characteristics):
    """Characteristic attributes of a :term:`CMOS`-based detector.

    Parameters
    ----------
    quantum_efficiency : float, optional
        Quantum efficiency.
    charge_to_volt_conversion : float, optional
        Sensitivity of charge readout. Unit: V/e-
    pre_amplification : float, optional
        Gain of pre-amplifier. Unit: V/V
    full_well_capacity : float, optional
        Full well capacity. Unit: e-
    adc_voltage_range : tuple of floats, optional
        ADC voltage range. Unit: V
    adc_bit_resolution : int, optional
        ADC bit resolution.
    """
