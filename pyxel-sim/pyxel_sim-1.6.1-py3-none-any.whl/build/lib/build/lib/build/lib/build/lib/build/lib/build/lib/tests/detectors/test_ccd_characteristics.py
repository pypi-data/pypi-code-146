#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

from copy import deepcopy

import pytest

from pyxel.detectors import CCDCharacteristics, Characteristics


@pytest.mark.parametrize(
    "quantum_efficiency, charge_to_volt_conversion, pre_amplification, "
    "full_well_capacity, adc_voltage_range, adc_bit_resolution",
    [
        (0, 0, 0, 0, None, None),
        (1.0, 1.0, 100.0, 10_000_000, None, None),
        (1.0, 1.0, 100.0, 10_000_000, [0.0, 3.0], 16),
    ],
)
def test_create_valid_ccdcharacteristics(
    quantum_efficiency,
    charge_to_volt_conversion,
    pre_amplification,
    full_well_capacity,
    adc_voltage_range,
    adc_bit_resolution,
):
    """Test when creating a valid `CCDCharacteristics` object."""
    _ = CCDCharacteristics(
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
        pytest.param(CCDCharacteristics(), False, id="Empty 'CCDCharacteristics'"),
        pytest.param(
            CCDCharacteristics(quantum_efficiency=0.1), False, id="Only one parameter"
        ),
        pytest.param(
            Characteristics(
                quantum_efficiency=0.1,
                charge_to_volt_conversion=0.2,
                pre_amplification=4.4,
            ),
            False,
            id="Wrong type",
        ),
        pytest.param(
            CCDCharacteristics(
                quantum_efficiency=0.1,
                charge_to_volt_conversion=0.2,
                pre_amplification=4.4,
                full_well_capacity=10,
            ),
            False,
            id="Missing some parameters",
        ),
        pytest.param(
            CCDCharacteristics(
                quantum_efficiency=0.1,
                charge_to_volt_conversion=0.2,
                pre_amplification=4.4,
                full_well_capacity=10,
                adc_voltage_range=(0.0, 10.0),
                adc_bit_resolution=16,
            ),
            True,
            id="Same parameters, same class",
        ),
    ],
)
def test_is_equal(other_obj, is_equal):
    """Test equality statement for `CCDCharacteristics`."""
    obj = CCDCharacteristics(
        quantum_efficiency=0.1,
        charge_to_volt_conversion=0.2,
        pre_amplification=4.4,
        full_well_capacity=10,
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
            CCDCharacteristics(
                quantum_efficiency=0.1,
                charge_to_volt_conversion=0.2,
                pre_amplification=4.4,
                full_well_capacity=10,
            ),
            {
                "quantum_efficiency": 0.1,
                "charge_to_volt_conversion": 0.2,
                "pre_amplification": 4.4,
                "full_well_capacity": 10,
                "adc_bit_resolution": None,
                "adc_voltage_range": None,
            },
        ),
        (
            CCDCharacteristics(
                quantum_efficiency=0.1,
                charge_to_volt_conversion=0.2,
                pre_amplification=4.4,
                full_well_capacity=10,
                adc_voltage_range=(0.0, 10.0),
                adc_bit_resolution=16,
            ),
            {
                "quantum_efficiency": 0.1,
                "charge_to_volt_conversion": 0.2,
                "pre_amplification": 4.4,
                "full_well_capacity": 10,
                "adc_voltage_range": (0.0, 10.0),
                "adc_bit_resolution": 16,
            },
        ),
    ],
)
def test_to_and_from_dict(obj, exp_dict):
    """Test methods 'to_dict', 'from_dict'."""
    assert type(obj) == CCDCharacteristics

    # Convert from `CCDCharacteristics` to a `dict`
    dct = obj.to_dict()
    assert dct == exp_dict

    # Copy 'exp_dict'
    copied_dct = deepcopy(exp_dict)  # create a new dict
    assert copied_dct is not exp_dict
    assert copied_dct == exp_dict

    # Convert from `dict` to `CCDCharacteristics`
    other_obj = CCDCharacteristics.from_dict(copied_dct)
    assert type(other_obj) == CCDCharacteristics
    assert obj == other_obj
    assert obj is not other_obj
    assert copied_dct == exp_dict
