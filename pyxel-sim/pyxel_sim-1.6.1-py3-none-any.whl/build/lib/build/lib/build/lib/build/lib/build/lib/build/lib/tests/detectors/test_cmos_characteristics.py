#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

from copy import deepcopy

import pytest

from pyxel.detectors import Characteristics, CMOSCharacteristics


@pytest.mark.parametrize(
    "quantum_efficiency, charge_to_volt_conversion, pre_amplification, "
    "full_well_capacity, adc_voltage_range, adc_bit_resolution",
    [
        (0, 0, 0, 0, None, None),
        (1.0, 1.0, 100.0, 10_000_000, None, None),
        (1.0, 1.0, 100.0, 10_000_000, [0.0, 3.0], 16),
    ],
)
def test_create_valid_cmoscharacteristics(
    quantum_efficiency,
    charge_to_volt_conversion,
    pre_amplification,
    full_well_capacity,
    adc_voltage_range,
    adc_bit_resolution,
):
    """Test when creating a valid `CMOSCharacteristics` object."""
    _ = CMOSCharacteristics(
        quantum_efficiency=quantum_efficiency,
        charge_to_volt_conversion=charge_to_volt_conversion,
        pre_amplification=pre_amplification,
        full_well_capacity=full_well_capacity,
        adc_voltage_range=adc_voltage_range,
        adc_bit_resolution=adc_bit_resolution,
    )


@pytest.mark.parametrize(
    "other_obj, is_equal",
    [
        pytest.param(None, False, id="None"),
        pytest.param(CMOSCharacteristics(), False, id="Empty 'CMOSCharacteristics'"),
        pytest.param(
            CMOSCharacteristics(quantum_efficiency=0.1), False, id="Only one parameter"
        ),
        pytest.param(
            Characteristics(
                quantum_efficiency=0.1,
                charge_to_volt_conversion=0.2,
                pre_amplification=3.3,
                full_well_capacity=5,
            ),
            False,
            id="Wrong type",
        ),
        pytest.param(
            CMOSCharacteristics(
                quantum_efficiency=0.1,
                charge_to_volt_conversion=0.2,
                pre_amplification=3.3,
                full_well_capacity=5,
                adc_voltage_range=(0.0, 10.0),
                adc_bit_resolution=16,
            ),
            True,
            id="Same parameters, same class",
        ),
    ],
)
def test_is_equal(other_obj, is_equal):
    """Test equality statement for `CMOSCharacteristics`."""
    obj = CMOSCharacteristics(
        quantum_efficiency=0.1,
        charge_to_volt_conversion=0.2,
        pre_amplification=3.3,
        full_well_capacity=5,
        adc_voltage_range=(0.0, 10.0),
        adc_bit_resolution=16,
    )

    if is_equal:
        assert obj == other_obj
    else:
        assert obj != other_obj


@pytest.mark.parametrize(
    "obj, exp_dict",
    [
        (
            CMOSCharacteristics(
                quantum_efficiency=0.1,
                charge_to_volt_conversion=0.2,
                pre_amplification=3.3,
                full_well_capacity=5,
            ),
            {
                "quantum_efficiency": 0.1,
                "charge_to_volt_conversion": 0.2,
                "pre_amplification": 3.3,
                "full_well_capacity": 5,
                "adc_bit_resolution": None,
                "adc_voltage_range": None,
            },
        ),
        (
            CMOSCharacteristics(
                quantum_efficiency=0.1,
                charge_to_volt_conversion=0.2,
                pre_amplification=3.3,
                full_well_capacity=5,
                adc_voltage_range=(0.0, 10.0),
                adc_bit_resolution=16,
            ),
            {
                "quantum_efficiency": 0.1,
                "charge_to_volt_conversion": 0.2,
                "pre_amplification": 3.3,
                "full_well_capacity": 5,
                "adc_voltage_range": (0.0, 10.0),
                "adc_bit_resolution": 16,
            },
        ),
    ],
)
def test_to_and_from_dict(obj, exp_dict):
    """Test methods 'to_dict', 'from_dict'."""
    assert type(obj) == CMOSCharacteristics

    # Convert from `CMOSCharacteristics` to a `dict`
    dct = obj.to_dict()
    assert dct == exp_dict

    # Copy 'exp_dict'
    copied_dct = deepcopy(exp_dict)  # create a new dict
    assert copied_dct is not exp_dict
    assert copied_dct == exp_dict

    # Convert from `dict` to `CMOSCharacteristics`
    other_obj = CMOSCharacteristics.from_dict(copied_dct)
    assert type(other_obj) == CMOSCharacteristics
    assert obj == other_obj
    assert obj is not other_obj
    assert copied_dct == exp_dict
