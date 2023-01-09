#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""TBW.

References
----------
[1] Leonardo MW Ltd., Electrical Interface Document for SAPHIRA (ME1000) in a 68-pin LLC
(3313-520-), issue 1A, 2012.

[2] I. Pastrana et al., HgCdTe SAPHIRA arrays: individual pixel measurement of charge gain and
node capacitance utilizing a stable IR LED, in High Energy, Optical, and Infrared Detectors for
Astronomy VIII, 2018, vol. 10709, no. July 2018, 2018, p. 37.

[3] S. B. Goebel et al., Overview of the SAPHIRA detector for adaptive optics applications, in
Journal of Astronomical Telescopes, Instruments, and Systems, 2018, vol. 4, no. 02, p. 1.

[4] G. Finger et al., Sub-electron read noise and millisecond full-frame readout with the near
infrared eAPD array SAPHIRA, in Adaptive Optics Systems V, 2016, vol. 9909, no. July 2016, p.
990912.

[5] I. M. Baker et al., Linear-mode avalanche photodiode arrays in HgCdTe at Leonardo, UK: the
current status, in Image Sensing Technologies: Materials, Devices, Systems, and Applications VI,
2019, vol. 10980, no. May, p. 20.
"""

import math
from typing import Mapping, Optional, Tuple

import numpy as np
from toolz import dicttoolz

from pyxel.util.memory import get_size


class APDCharacteristics:
    """Characteristic attributes of the APD detector.

    Parameters
    ----------
    roic_gain
        Gain of the read-out integrated circuit. Unit: V/V
    quantum_efficiency : float, optional
        Quantum efficiency.
    full_well_capacity : float, optional
        Full well capacity. Unit: e-
    adc_bit_resolution : int, optional
        ADC bit resolution.
    adc_voltage_range : tuple of floats, optional
        ADC voltage range. Unit: V
    avalanche_gain : float, optional
        APD gain. Unit: electron/electron
    pixel_reset_voltage : float
        DC voltage going into the detector, not the voltage of a reset pixel. Unit: V
    common_voltage : float
        Common voltage. Unit: V
    """

    def __init__(
        self,
        roic_gain: float,  # unit: V
        quantum_efficiency: Optional[float] = None,  # unit: NA
        full_well_capacity: Optional[float] = None,  # unit: electron
        adc_bit_resolution: Optional[int] = None,
        adc_voltage_range: Optional[Tuple[float, float]] = None,  # unit: V
        avalanche_gain: Optional[float] = None,  # unit: electron/electron
        pixel_reset_voltage: Optional[float] = None,  # unit: V
        common_voltage: Optional[float] = None,  # unit: V
    ):

        self._avalanche_gain = avalanche_gain
        self._common_voltage = common_voltage
        self._pixel_reset_voltage = pixel_reset_voltage

        if avalanche_gain and pixel_reset_voltage and common_voltage:
            raise ValueError(
                "Please only specify two inputs out of: avalanche gain, pixel reset voltage, common voltage."
            )
        elif avalanche_gain and pixel_reset_voltage and not common_voltage:
            self._avalanche_bias = self.gain_to_bias_saphira(avalanche_gain)
            self._common_voltage = pixel_reset_voltage - self.avalanche_bias
        elif avalanche_gain and common_voltage and not pixel_reset_voltage:
            self._avalanche_bias = self.gain_to_bias_saphira(avalanche_gain)
            self._pixel_reset_voltage = common_voltage + self.avalanche_bias
        elif common_voltage and pixel_reset_voltage and not avalanche_gain:
            self._avalanche_bias = pixel_reset_voltage - common_voltage
            self._avalanche_gain = self.bias_to_gain_saphira(self.avalanche_bias)
        else:
            raise ValueError(
                "Not enough input parameters provided to calculate avalanche bias!"
            )

        if quantum_efficiency and not (0.0 <= quantum_efficiency <= 1.0):
            raise ValueError("'quantum_efficiency' must be between 0.0 and 1.0.")
        if avalanche_gain and not (1.0 <= avalanche_gain <= 1000.0):
            raise ValueError("'apd_gain' must be between 1.0 and 1000.0.")
        if adc_bit_resolution and not (4 <= adc_bit_resolution <= 64):
            raise ValueError("'adc_bit_resolution' must be between 4 and 64.")
        if adc_voltage_range and not len(adc_voltage_range) == 2:
            raise ValueError("Voltage range must have length of 2.")
        if full_well_capacity and not (0.0 <= full_well_capacity <= 1.0e7):
            raise ValueError("'full_well_capacity' must be between 0 and 1e7.")

        self._quantum_efficiency = quantum_efficiency
        self._full_well_capacity = full_well_capacity
        self._adc_voltage_range = adc_voltage_range
        self._adc_bit_resolution = adc_bit_resolution
        self._node_capacitance: float = self.bias_to_node_capacitance_saphira(
            self.avalanche_bias
        )
        self._roic_gain = roic_gain
        self._charge_to_volt_conversion: float = self.detector_gain_saphira(
            capacitance=self.node_capacitance, roic_gain=self.roic_gain
        )
        self._numbytes = 0

    def __eq__(self, other) -> bool:
        return (
            type(self) == type(other)
            and self._quantum_efficiency == other._quantum_efficiency
            and self._full_well_capacity == other._full_well_capacity
            and self._adc_bit_resolution == other._adc_bit_resolution
            and self._adc_voltage_range == other._adc_voltage_range
            and self._avalanche_gain == other._avalanche_gain
            and self._pixel_reset_voltage == other._pixel_reset_voltage
            and self._common_voltage == other._common_voltage
        )

    @property
    def quantum_efficiency(self) -> float:
        """Get Quantum efficiency."""
        if self._quantum_efficiency:
            return self._quantum_efficiency
        else:
            raise ValueError(
                "'quantum_efficiency' not specified in detector characteristics."
            )

    @quantum_efficiency.setter
    def quantum_efficiency(self, value: float) -> None:
        """Set Quantum efficiency."""
        if np.min(value) < 0.0 and np.max(value) <= 1.0:
            raise ValueError("'quantum_efficiency' values must be between 0.0 and 1.0.")

        self._quantum_efficiency = value

    @property
    def avalanche_gain(self) -> float:
        """Get APD gain."""
        if self._avalanche_gain:
            return self._avalanche_gain
        else:
            raise ValueError("'apd_gain' not specified in detector characteristics.")

    @avalanche_gain.setter
    def avalanche_gain(self, value: float) -> None:
        """Set APD gain."""
        if np.min(value) < 1.0 and np.max(value) <= 1000.0:
            raise ValueError("'apd_gain' values must be between 1.0 and 1000.")
        self._avalanche_gain = value
        self._avalanche_bias = self.gain_to_bias_saphira(value)
        self._common_voltage = self.pixel_reset_voltage - self.avalanche_bias

    @property
    def pixel_reset_voltage(self) -> float:
        """Get pixel reset voltage."""
        if self._pixel_reset_voltage:
            return self._pixel_reset_voltage
        else:
            raise ValueError("'apd_gain' not specified in detector characteristics.")

    @pixel_reset_voltage.setter
    def pixel_reset_voltage(self, value: float) -> None:
        """Set pixel reset voltage."""
        self._avalanche_bias = value - self.common_voltage
        self._avalanche_gain = self.bias_to_gain_saphira(self.avalanche_bias)
        self._pixel_reset_voltage = value

    @property
    def common_voltage(self) -> float:
        """Get common voltage."""
        if self._common_voltage:
            return self._common_voltage
        else:
            raise ValueError("'apd_gain' not specified in detector characteristics.")

    @common_voltage.setter
    def common_voltage(self, value: float) -> None:
        """Set common voltage."""
        self._avalanche_bias = self.pixel_reset_voltage - value
        self._avalanche_gain = self.bias_to_gain_saphira(self.avalanche_bias)
        self._common_voltage = value

    @property
    def avalanche_bias(self) -> float:
        """Get avalanche bias."""
        if self._avalanche_bias:
            return self._avalanche_bias
        else:
            raise ValueError("'apd_gain' not specified in detector characteristics.")

    @property
    def roic_gain(self) -> float:
        """Get roic gainn."""
        if self._roic_gain:
            return self._roic_gain
        else:
            raise ValueError("'roic_gain' not specified in detector characteristics.")

    @property
    def node_capacitance(self) -> float:
        """Get node capacitance."""
        self._node_capacitance = self.bias_to_node_capacitance_saphira(
            self.avalanche_bias
        )
        return self._node_capacitance

    @property
    def charge_to_volt_conversion(self):
        """Get charge to voltage conversion factor."""
        self._charge_to_volt_conversion = self.detector_gain_saphira(
            capacitance=self.node_capacitance, roic_gain=self.roic_gain
        )
        return self._charge_to_volt_conversion

    @property
    def adc_bit_resolution(self) -> int:
        """Get bit resolution of the Analog-Digital Converter."""
        if self._adc_bit_resolution:
            return self._adc_bit_resolution
        else:
            raise ValueError(
                "'adc_bit_resolution' not specified in detector characteristics."
            )

    @adc_bit_resolution.setter
    def adc_bit_resolution(self, value: int) -> None:
        """Set bit resolution of the Analog-Digital Converter."""
        self._adc_bit_resolution = value

    @property
    def adc_voltage_range(self) -> Tuple[float, float]:
        """Get voltage range of the Analog-Digital Converter."""
        if self._adc_voltage_range:
            return self._adc_voltage_range
        else:
            raise ValueError(
                "'adc_voltage_range' not specified in detector characteristics."
            )

    @adc_voltage_range.setter
    def adc_voltage_range(self, value: Tuple[float, float]) -> None:
        """Set voltage range of the Analog-Digital Converter."""
        self._adc_voltage_range = value

    @property
    def full_well_capacity(self) -> float:
        """Get Full well capacity."""
        if self._full_well_capacity:
            return self._full_well_capacity
        else:
            raise ValueError(
                "'full_well_capacity' not specified in detector characteristics."
            )

    @full_well_capacity.setter
    def full_well_capacity(self, value: float) -> None:
        """Set Full well capacity."""
        if value not in range(10000001):
            raise ValueError("'full_well_capacity' must be between 0 and 1e+7.")

        self._full_well_capacity = value

    @property
    def system_gain(self) -> float:
        """Get system gain."""
        return (
            self.quantum_efficiency
            * self.avalanche_gain
            * self.charge_to_volt_conversion
            * 2**self.adc_bit_resolution
        ) / (max(self.adc_voltage_range) - min(self.adc_voltage_range))

    @property
    def numbytes(self) -> int:
        """Recursively calculates object size in bytes using Pympler library.

        Returns
        -------
        int
            Size of the object in bytes.
        """
        self._numbytes = get_size(self)
        return self._numbytes

    @staticmethod
    def bias_to_node_capacitance_saphira(bias: float) -> float:
        """Pixel integrating node capacitance in F.

        The below interpolates empirical published data, however note that
        Node C = Charge Gain / Voltage Gain
        So can be calculated by measuring V gain (varying PRV) and chg gain (PTC); see [2]

        Parameters
        ----------
        bias: float

        Returns
        -------
        output_capacitance: float
        """
        if bias < 1:
            raise ValueError(
                "Warning! Node capacitance calculation is inaccurate for bias voltages <1 V!"
            )

        # From [2] (Mk13 ME1000; data supplied by Leonardo):
        bias_list = [1, 1.5, 2.5, 3.5, 4.5, 6.5, 8.5, 10.5]
        capacitance = [46.5, 41.3, 37.3, 34.8, 33.2, 31.4, 30.7, 30.4]

        output_capacitance = float(np.interp(x=bias, xp=bias_list, fp=capacitance))

        return output_capacitance * 1.0e-15

    @staticmethod
    def bias_to_gain_saphira(bias: float) -> float:
        """Calculate gain from bias.

        The formula ignores the soft knee between the linear and unity gain ranges,
        but should be close enough. [2] (Mk13 ME1000)

        Parameters
        ----------
        bias: float

        Returns
        -------
        gain: float
        """

        gain = 2 ** ((bias - 2.65) / 2.17)

        if gain < 1.0:
            gain = 1.0  # Unity gain is lowest

        return gain

    @staticmethod
    def gain_to_bias_saphira(gain: float) -> float:
        """Calculate bias from gain.

        The formula ignores the soft knee between the linear and
        unity gain ranges, but should be close enough. [2] (Mk13 ME1000)

        Parameters
        ----------
        gain: float

        Returns
        -------
        bias: float
        """

        bias = (2.17 * math.log2(gain)) + 2.65

        return bias

    @staticmethod
    def detector_gain_saphira(capacitance: float, roic_gain: float) -> float:
        """Saphira detector gain.

        Parameters
        ----------
        capacitance: float
        roic_gain: float

        Returns
        -------
        float
        """
        # Late import to speedup start-up time
        import astropy.constants as const

        return roic_gain * (const.e.value / capacitance)

    def to_dict(self) -> Mapping:
        """Get the attributes of this instance as a `dict`."""
        if self._avalanche_gain and self._pixel_reset_voltage:
            dct = {
                "avalanche_gain": self._avalanche_gain,
                "common_voltage": None,
                "pixel_reset_voltage": self._pixel_reset_voltage,
            }
        elif self._avalanche_gain and self._common_voltage:
            dct = {
                "avalanche_gain": self._avalanche_gain,
                "common_voltage": self._common_voltage,
                "pixel_reset_voltage": None,
            }
        elif self._common_voltage and self._pixel_reset_voltage:
            dct = {
                "avalanche_gain": None,
                "common_voltage": self._common_voltage,
                "pixel_reset_voltage": self._pixel_reset_voltage,
            }
        else:
            raise NotImplementedError

        other_dct = {
            "quantum_efficiency": self._quantum_efficiency,
            "full_well_capacity": self._full_well_capacity,
            "adc_voltage_range": self._adc_voltage_range,
            "adc_bit_resolution": self._adc_bit_resolution,
            "roic_gain": self._roic_gain,
        }

        return {**dct, **other_dct}

    @classmethod
    def from_dict(cls, dct: Mapping):
        """Create a new instance from a `dict`."""
        if "adc_voltage_range" in dct:
            new_dct: Mapping = dicttoolz.dissoc(dct, "adc_voltage_range")
            adc_voltage_range = dct["adc_voltage_range"]

            if adc_voltage_range is not None:
                adc_voltage_range = tuple(adc_voltage_range)

            return cls(adc_voltage_range=adc_voltage_range, **new_dct)

        return cls(**dct)
