#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

""":term:`SAR` :term:`ADC` model with noise."""

from typing import Tuple

import numpy as np

from pyxel.detectors import Detector


def apply_sar_adc_with_noise(
    signal_2d: np.ndarray,
    num_rows: int,
    num_cols: int,
    strengths: np.ndarray,
    noises: np.ndarray,
    max_volt: float,
    adc_bits: int,
) -> np.ndarray:
    """Apply :term:`SAR` :term:`ADC` with noise.

    Parameters
    ----------
    signal_2d : ndarray
    num_rows : int
    num_cols : int
    strengths : ndarray
    noises : ndarray
    max_volt : float
        Max volt of the ADC.
    adc_bits : int
        Number of bits the value will be encoded with.

    Returns
    -------
    ndarray
        2D digitized array.
    """
    data_digitized_2d = np.zeros((num_rows, num_cols))

    signal_normalized_2d = signal_2d.copy()

    # Set the reference voltage of the ADC to half the max
    ref_2d = np.full(shape=(num_rows, num_cols), fill_value=max_volt / 2.0)

    # For each bits, compare the value of the ref to the capacitance value
    for i in np.arange(adc_bits):
        strength = strengths[i]
        noise = noises[i]

        # digital value associated with this step
        digital_value: int = 2 ** (adc_bits - (i + 1))

        ref_2d += np.random.normal(loc=strength, scale=noise, size=(num_rows, num_cols))

        # All data that is higher than the ref is equal to the dig. value
        mask_2d: np.ndarray = signal_normalized_2d >= ref_2d
        data_digitized_2d += digital_value * mask_2d

        # Subtract ref value from the data
        signal_normalized_2d -= ref_2d * mask_2d

        # Divide reference voltage by 2 for next step
        ref_2d /= 2.0

    return data_digitized_2d


# TODO: documentation, range volt - only max is used
def sar_adc_with_noise(
    detector: Detector,
    strengths: Tuple[float, ...],
    noises: Tuple[float, ...],
) -> None:
    r"""Digitize signal array using :term:`SAR` (Successive Approximation Register) :term:`ADC` logic with noise.

    Successive-approximation-register (:term:`SAR`) analog-to-digital converters (:term:`ADC`)
    for each bit, will compare the randomly perturbated **reference voltage** to
    the voltage of the pixel, adding the corresponding digital value if it is superior.
    The perturbations are generated randomly for each pixel.

    The reference voltage fluctuations are regulated by two parameters, **strength** and
    **noise**, that are set independently for each bit.

    This model and the notes are based on the work of Emma Esparza Borges
    from :term:`ESO`.

    Parameters
    ----------
    detector : Detector
        Pyxel Detector object.
    strengths : tuple of float
        Sequence of ``detector.characteristics.adc_bit_resolution`` number(s). Unit: V
    noises : tuple of float
        Sequence of ``detector.characteristics.adc_bit_resolution`` number(s). Unit: V

    Raises
    ------
    ValueError
        Raised if parameters ``strengths`` and/or ``noises`` does not have exactly the
        correct numbers of parameters.
        It is expected to have ``detector.characteristics.adc_bit_resolution`` elements.

    Notes
    -----
    The :term:`SAR` :term:`ADC` architecture is based on a binary search algorithm.
    Essentially, it works comparing the analog input to the output of a
    Digital-to-Analog Converter (:term:`DAC`), which is initialized with the
    :term:`MSB` high and all other bits low.
    If the analog sample is higher than the :term:`DAC` output the :term:`MSB` keeps high,
    while if the :term:`DAC` output is higher the :term:`MSB` is set low.
    This comparison is performed for each bit from the :term:`MSB` to the :term:`LSB`
    following the same procedure.

    .. figure:: _static/sar_architecture.png
        :scale: 70%
        :alt: Simplified N-bit SAR ADC architecture.
        :align: center

        Simplified N-bit :term:`SAR` :term:`ADC` architecture
        (see https://www.maximintegrated.com/en/app-notes/index.mvp/id/1080).

    Considering a 8-bits :term:`SAR` :term:`ADC`, for the first comparison the
    8-bit register is set to midscale (`10000000`) forcing the :term:`DAC` output
    (:math:`V_{DAC}`) to be half of the reference voltage:
    :math:`V_{DAC}=\frac{V_{REF}}{2}`.
    For the second comparison, if :math:`V_{DAC} < V_{IN}` then the 8-bit register is set
    to `11000000`, if :math:`V_{DAC} > V_{IN}` then the 8-bit register is set to `01000000`.
    In both cases :math:`V_{DAC} = \frac{V_{REF}}{4}`.

    It is essential that :math:`V_{REF}` remains stable through all comparisons
    to be able to perform an accurate conversion from the analog inputs of
    the instrument.

    A potential sources of digitization issues can be modeled by adding
    voltage fluctuations to :math:`V_{REF}` at each stage of the process.

    These fluctuations can be represented by the vectors :math:`\mathit{strength}` and :math:`\mathit{noise}`.
    For a 8-bits :term:`SAR` :term:`ADC`, we have
    :math:`\mathit{strength} = \begin{pmatrix}\mathit{strength}_\mathit{bit7}\\ \vdots\\
    \mathit{strength}_\mathit{bit0}\end{pmatrix}`
    and
    :math:`noise = \begin{pmatrix}\mathit{noise}_\mathit{bit7}\\ \vdots\\ \mathit{noise}_\mathit{bit0}\end{pmatrix}`.

    The fluctuations at each stage of the process (in this case 8 stages) are represented by
    the vector :math:`V^\mathit{perturbated}_\mathit{REF}` with

    .. math::
       \begin{matrix}
       V^\mathit{perturbated}_{\mathit{REF}_\mathit{bit7}} = V_\mathit{REF}
       \left(1 + \mathit{np.random.normal}(\mathit{strength}_\mathit{bit7}, \mathit{noise}_\mathit{bit7})\right)\\
       \cdots\\
       V^\mathit{perturbated}_{\mathit{REF}_\mathit{bit0}} = V_\mathit{REF}
       \left(1 + \mathit{np.random.normal}(\mathit{strength}_\mathit{bit0}, \mathit{noise}_\mathit{bit0})\right)
       \end{matrix}
    """
    min_volt, max_volt = detector.characteristics.adc_voltage_range
    adc_bits = detector.characteristics.adc_bit_resolution

    if len(strengths) != detector.characteristics.adc_bit_resolution:
        raise ValueError(
            f"Expecting a sequence of {adc_bits} elements for parameter 'strengths'."
        )

    if len(noises) != detector.characteristics.adc_bit_resolution:
        raise ValueError(
            f"Expecting a sequence of {adc_bits} elements for parameter 'noises'."
        )

    image_2d: np.ndarray = apply_sar_adc_with_noise(
        signal_2d=detector.signal.array,
        num_rows=detector.geometry.row,
        num_cols=detector.geometry.col,
        strengths=np.asarray(strengths, dtype=float),
        noises=np.asarray(noises, dtype=float),
        max_volt=max_volt,
        adc_bits=adc_bits,
    )

    detector.image.array = image_2d
