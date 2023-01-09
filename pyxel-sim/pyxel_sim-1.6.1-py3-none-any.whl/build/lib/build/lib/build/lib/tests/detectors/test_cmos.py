#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

from copy import deepcopy
from typing import Tuple

import numpy as np
import pandas as pd
import pytest

from pyxel.detectors import (
    CMOS,
    CMOSCharacteristics,
    CMOSGeometry,
    Detector,
    Environment,
)


@pytest.fixture
def valid_cmos() -> CMOS:
    """Create a valid `CMOS`."""
    return CMOS(
        geometry=CMOSGeometry(
            row=100,
            col=120,
            total_thickness=123.1,
            pixel_horz_size=12.4,
            pixel_vert_size=34.5,
        ),
        environment=Environment(temperature=100.1),
        characteristics=CMOSCharacteristics(
            quantum_efficiency=0.1,
            charge_to_volt_conversion=0.2,
            pre_amplification=3.3,
            full_well_capacity=4.4,
        ),
    )


@pytest.mark.parametrize(
    "other_obj, is_equal",
    [
        pytest.param(None, False, id="None"),
        pytest.param(
            CMOS(
                geometry=CMOSGeometry(row=100, col=120),
                environment=Environment(),
                characteristics=CMOSCharacteristics(),
            ),
            False,
            id="Empty 'CMOS'",
        ),
        pytest.param(
            CMOS(
                geometry=CMOSGeometry(
                    row=100,
                    col=120,
                    total_thickness=123.1,
                    pixel_horz_size=12.4,
                    pixel_vert_size=34.5,
                ),
                environment=Environment(),
                characteristics=CMOSCharacteristics(),
            ),
            False,
            id="Almost same parameters, different class",
        ),
        pytest.param(
            CMOS(
                geometry=CMOSGeometry(
                    row=100,
                    col=120,
                    total_thickness=123.1,
                    pixel_horz_size=12.4,
                    pixel_vert_size=34.5,
                ),
                environment=Environment(temperature=100.1),
                characteristics=CMOSCharacteristics(
                    quantum_efficiency=0.1,
                    charge_to_volt_conversion=0.2,
                    pre_amplification=3.3,
                    full_well_capacity=4.4,
                ),
            ),
            True,
            id="Same parameters, same class",
        ),
    ],
)
def test_is_equal(valid_cmos: CMOS, other_obj, is_equal):
    """Test equality statement for `CMOS`."""

    if is_equal:
        assert valid_cmos == other_obj
    else:
        assert valid_cmos != other_obj


def test_is_equal_with_arrays(valid_cmos: CMOS):
    other_detector = deepcopy(valid_cmos)

    assert valid_cmos.geometry is not other_detector.geometry
    assert valid_cmos.environment is not other_detector.environment
    assert valid_cmos.characteristics is not other_detector.characteristics
    assert valid_cmos._photon is not other_detector._photon
    assert valid_cmos._charge is not other_detector._charge
    assert valid_cmos._pixel is not other_detector._pixel
    assert valid_cmos._signal is not other_detector._signal
    assert valid_cmos._image is not other_detector._image

    shape = valid_cmos.geometry.row, valid_cmos.geometry.col
    photon: np.ndarray = np.random.random(size=shape)
    pixel: np.ndarray = np.random.random(size=shape)
    signal: np.ndarray = np.random.random(size=shape)
    image: np.ndarray = np.random.random(size=shape)
    charge: np.ndarray = np.random.random(size=shape)

    valid_cmos.photon.array = photon.copy()
    valid_cmos.pixel.array = pixel.copy()
    valid_cmos.signal.array = signal.copy()
    valid_cmos.image.array = image.copy()

    valid_cmos.charge._array = charge.copy()
    valid_cmos.charge._frame.append({"charge": 1}, ignore_index=True)

    other_detector.photon.array = photon.copy()
    other_detector.pixel.array = pixel.copy()
    other_detector.signal.array = signal.copy()
    other_detector.image.array = image.copy()

    other_detector.charge._array = charge.copy()
    other_detector.charge._frame.append({"charge": 1}, ignore_index=True)

    assert valid_cmos == other_detector


def comparison(dct, other_dct):
    assert set(dct) == set(other_dct) == {"version", "type", "data", "properties"}
    assert dct["version"] == other_dct["version"]
    assert dct["type"] == other_dct["type"]
    assert dct["properties"] == other_dct["properties"]

    assert (
        set(dct["data"])
        == set(other_dct["data"])
        == {"photon", "scene", "pixel", "signal", "image", "charge", "processed_data"}
    )
    np.testing.assert_equal(dct["data"]["photon"], other_dct["data"]["photon"])
    np.testing.assert_equal(dct["data"]["pixel"], other_dct["data"]["pixel"])
    np.testing.assert_equal(dct["data"]["signal"], other_dct["data"]["signal"])
    np.testing.assert_equal(dct["data"]["image"], other_dct["data"]["image"])

    assert (
        set(dct["data"]["charge"])
        == set(other_dct["data"]["charge"])
        == {"array", "frame"}
    )
    np.testing.assert_equal(
        dct["data"]["charge"]["array"], other_dct["data"]["charge"]["array"]
    )
    pd.testing.assert_frame_equal(
        dct["data"]["charge"]["frame"], other_dct["data"]["charge"]["frame"]
    )


@pytest.mark.parametrize("klass", [CMOS, Detector])
@pytest.mark.parametrize(
    "obj, exp_dict",
    [
        pytest.param(
            CMOS(
                geometry=CMOSGeometry(row=100, col=120),
                environment=Environment(),
                characteristics=CMOSCharacteristics(),
            ),
            {
                "version": 1,
                "type": "CMOS",
                "properties": {
                    "geometry": {
                        "row": 100,
                        "col": 120,
                        "total_thickness": None,
                        "pixel_horz_size": None,
                        "pixel_vert_size": None,
                    },
                    "environment": {"temperature": None},
                    "characteristics": {
                        "quantum_efficiency": None,
                        "charge_to_volt_conversion": None,
                        "pre_amplification": None,
                        "full_well_capacity": None,
                        "adc_bit_resolution": None,
                        "adc_voltage_range": None,
                    },
                },
                "data": {
                    "photon": np.zeros(shape=(100, 120)),
                    "scene": None,
                    "pixel": np.zeros(shape=(100, 120)),
                    "signal": np.zeros(shape=(100, 120)),
                    "image": np.zeros(shape=(100, 120)),
                    "charge": {
                        "array": np.zeros(shape=(100, 120)),
                        "frame": pd.DataFrame(
                            columns=[
                                "charge",
                                "number",
                                "init_energy",
                                "energy",
                                "init_pos_ver",
                                "init_pos_hor",
                                "init_pos_z",
                                "position_ver",
                                "position_hor",
                                "position_z",
                                "velocity_ver",
                                "velocity_hor",
                                "velocity_z",
                            ],
                            dtype=float,
                        ),
                    },
                    "processed_data": {
                        "coords": {},
                        "attrs": {},
                        "dims": {},
                        "data_vars": {},
                    },
                },
            },
            id="Default parameters",
        ),
        pytest.param(
            CMOS(
                geometry=CMOSGeometry(
                    row=100,
                    col=120,
                    total_thickness=123.1,
                    pixel_horz_size=12.4,
                    pixel_vert_size=34.5,
                ),
                environment=Environment(temperature=100.1),
                characteristics=CMOSCharacteristics(
                    quantum_efficiency=0.1,
                    charge_to_volt_conversion=0.2,
                    pre_amplification=3.3,
                    full_well_capacity=4.4,
                    adc_bit_resolution=16,
                    adc_voltage_range=(0.0, 10.0),
                ),
            ),
            {
                "version": 1,
                "type": "CMOS",
                "properties": {
                    "geometry": {
                        "row": 100,
                        "col": 120,
                        "total_thickness": 123.1,
                        "pixel_horz_size": 12.4,
                        "pixel_vert_size": 34.5,
                    },
                    "environment": {"temperature": 100.1},
                    "characteristics": {
                        "quantum_efficiency": 0.1,
                        "charge_to_volt_conversion": 0.2,
                        "pre_amplification": 3.3,
                        "full_well_capacity": 4.4,
                        "adc_bit_resolution": 16,
                        "adc_voltage_range": (0.0, 10.0),
                    },
                },
                "data": {
                    "photon": np.zeros(shape=(100, 120)),
                    "scene": None,
                    "pixel": np.zeros(shape=(100, 120)),
                    "signal": np.zeros(shape=(100, 120)),
                    "image": np.zeros(shape=(100, 120)),
                    "charge": {
                        "array": np.zeros(shape=(100, 120)),
                        "frame": pd.DataFrame(
                            columns=[
                                "charge",
                                "number",
                                "init_energy",
                                "energy",
                                "init_pos_ver",
                                "init_pos_hor",
                                "init_pos_z",
                                "position_ver",
                                "position_hor",
                                "position_z",
                                "velocity_ver",
                                "velocity_hor",
                                "velocity_z",
                            ],
                            dtype=float,
                        ),
                    },
                    "processed_data": {
                        "coords": {},
                        "attrs": {},
                        "dims": {},
                        "data_vars": {},
                    },
                },
            },
            id="CMOS fully defined",
        ),
    ],
)
def test_to_and_from_dict(klass, obj, exp_dict):
    """Test methods 'to_dict', 'from_dict'."""
    assert type(obj) == CMOS

    # Convert from `CMOS` to a `dict`
    dct = obj.to_dict()
    comparison(dct, exp_dict)

    # Copy 'exp_dict'
    copied_dct = deepcopy(exp_dict)  # create a new dict
    assert copied_dct is not exp_dict
    comparison(copied_dct, exp_dict)

    # Convert from `dict` to `CMOS`
    other_obj = klass.from_dict(copied_dct)
    assert type(other_obj) == CMOS
    assert obj == other_obj
    assert obj is not other_obj
    comparison(copied_dct, exp_dict)
