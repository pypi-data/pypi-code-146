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

from pyxel.detectors import CCD, CCDCharacteristics, CCDGeometry, Detector, Environment


@pytest.fixture
def valid_ccd() -> CCD:
    """Create a valid `CCD`."""
    return CCD(
        geometry=CCDGeometry(
            row=100,
            col=120,
            total_thickness=123.1,
            pixel_horz_size=12.4,
            pixel_vert_size=34.5,
        ),
        environment=Environment(temperature=100.1),
        characteristics=CCDCharacteristics(
            quantum_efficiency=0.1,
            charge_to_volt_conversion=0.2,
            pre_amplification=3.3,
            full_well_capacity=10,
        ),
    )


@pytest.mark.parametrize(
    "other_obj, is_equal",
    [
        pytest.param(None, False, id="None"),
        pytest.param(
            CCD(
                geometry=CCDGeometry(row=100, col=120),
                environment=Environment(),
                characteristics=CCDCharacteristics(),
            ),
            False,
            id="Empty 'CCD'",
        ),
        pytest.param(
            CCD(
                geometry=CCDGeometry(
                    row=100,
                    col=120,
                    total_thickness=123.1,
                    pixel_horz_size=12.4,
                    pixel_vert_size=34.5,
                ),
                environment=Environment(),
                characteristics=CCDCharacteristics(),
            ),
            False,
            id="Almost same parameters, different class",
        ),
        pytest.param(
            CCD(
                geometry=CCDGeometry(
                    row=100,
                    col=120,
                    total_thickness=123.1,
                    pixel_horz_size=12.4,
                    pixel_vert_size=34.5,
                ),
                environment=Environment(temperature=100.1),
                characteristics=CCDCharacteristics(
                    quantum_efficiency=0.1,
                    charge_to_volt_conversion=0.2,
                    pre_amplification=3.3,
                    full_well_capacity=10,
                ),
            ),
            True,
            id="Same parameters, same class",
        ),
    ],
)
def test_is_equal(valid_ccd: CCD, other_obj, is_equal):
    """Test equality statement for `CCD`."""

    if is_equal:
        assert valid_ccd == other_obj
    else:
        assert valid_ccd != other_obj


def test_is_equal_with_arrays(valid_ccd: CCD):
    other_detector = deepcopy(valid_ccd)

    # Check that the deepcopy was applied
    assert valid_ccd.geometry is not other_detector.geometry
    assert valid_ccd.environment is not other_detector.environment
    assert valid_ccd.characteristics is not other_detector.characteristics
    assert valid_ccd._photon is not other_detector._photon
    assert valid_ccd._charge is not other_detector._charge
    assert valid_ccd._pixel is not other_detector._pixel
    assert valid_ccd._signal is not other_detector._signal
    assert valid_ccd._image is not other_detector._image

    # Generate random data
    shape = valid_ccd.geometry.row, valid_ccd.geometry.col
    photon_2d: np.ndarray = np.random.random(size=shape)
    pixel_2d: np.ndarray = np.random.random(size=shape)
    signal_2d: np.ndarray = np.random.random(size=shape)
    image_2d: np.ndarray = np.random.random(size=shape)
    charge_2d: np.ndarray = np.random.random(size=shape)

    # Apply the random data to 'valid_ccd' and 'other_detector'
    valid_ccd.photon.array = photon_2d.copy()
    valid_ccd.pixel.array = pixel_2d.copy()
    valid_ccd.signal.array = signal_2d.copy()
    valid_ccd.image.array = image_2d.copy()

    valid_ccd.charge._array = charge_2d.copy()
    valid_ccd.charge._frame = valid_ccd.charge._frame.append(
        {"charge": 1}, ignore_index=True
    )

    other_detector.photon.array = photon_2d.copy()
    other_detector.pixel.array = pixel_2d.copy()
    other_detector.signal.array = signal_2d.copy()
    other_detector.image.array = image_2d.copy()

    other_detector.charge._array = charge_2d.copy()
    other_detector.charge._frame = other_detector.charge._frame.append(
        {"charge": 1}, ignore_index=True
    )

    assert valid_ccd == other_detector


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


@pytest.mark.parametrize("klass", [CCD, Detector])
@pytest.mark.parametrize(
    "obj, exp_dict",
    [
        pytest.param(
            CCD(
                geometry=CCDGeometry(row=100, col=120),
                environment=Environment(),
                characteristics=CCDCharacteristics(),
            ),
            {
                "version": 1,
                "type": "CCD",
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
            CCD(
                geometry=CCDGeometry(
                    row=100,
                    col=120,
                    total_thickness=123.1,
                    pixel_horz_size=12.4,
                    pixel_vert_size=34.5,
                ),
                environment=Environment(temperature=100.1),
                characteristics=CCDCharacteristics(
                    quantum_efficiency=0.1,
                    charge_to_volt_conversion=0.2,
                    pre_amplification=3.3,
                    full_well_capacity=10,
                    adc_bit_resolution=16,
                    adc_voltage_range=(0.0, 10.0),
                ),
            ),
            {
                "version": 1,
                "type": "CCD",
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
                        "full_well_capacity": 10,
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
            id="CCD fully defined",
        ),
    ],
)
def test_to_and_from_dict(klass, obj, exp_dict):
    """Test methods 'to_dict', 'from_dict'."""
    assert type(obj) == CCD

    # Convert from `CCD` to a `dict`
    dct = obj.to_dict()
    comparison(dct, exp_dict)

    # Copy 'exp_dict'
    copied_dct = deepcopy(exp_dict)  # create a new dict
    assert copied_dct is not exp_dict
    comparison(copied_dct, exp_dict)

    # Convert from `dict` to `CCD`
    other_obj = klass.from_dict(copied_dct)
    assert type(other_obj) == CCD
    assert obj == other_obj
    assert obj is not other_obj
    comparison(copied_dct, exp_dict)


@pytest.mark.parametrize("klass", [CCD, Detector])
def test_to_and_from_dict_with_arrays_no_frame(valid_ccd: CCD, klass):
    # Generate random data
    shape = valid_ccd.geometry.row, valid_ccd.geometry.col
    photon_2d: np.ndarray = np.random.random(size=shape)
    pixel_2d: np.ndarray = np.random.random(size=shape)
    signal_2d: np.ndarray = np.random.random(size=shape)
    image_2d: np.ndarray = np.random.random(size=shape)
    charge_2d: np.ndarray = np.random.random(size=shape)

    valid_ccd.photon.array = photon_2d.copy()
    valid_ccd.pixel.array = pixel_2d.copy()
    valid_ccd.signal.array = signal_2d.copy()
    valid_ccd.image.array = image_2d.copy()

    valid_ccd.charge._array = charge_2d.copy()
    # valid_ccd.charge._frame=valid_ccd.charge._frame.append({"charge": 1}, ignore_index=True)

    # Convert from the detector to a `dict`
    dct = valid_ccd.to_dict()

    exp_dict = {
        "version": 1,
        "type": "CCD",
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
                "full_well_capacity": 10,
                "adc_bit_resolution": None,
                "adc_voltage_range": None,
            },
        },
        "data": {
            "photon": photon_2d.copy(),
            "scene": None,
            "pixel": pixel_2d.copy(),
            "signal": signal_2d.copy(),
            "image": image_2d.copy(),
            "charge": {
                "array": charge_2d.copy(),
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
            "processed_data": {"coords": {}, "attrs": {}, "dims": {}, "data_vars": {}},
        },
    }

    comparison(dct, exp_dict)

    # Copy 'exp_dict'
    copied_dct = deepcopy(exp_dict)  # create a new dict
    assert copied_dct is not exp_dict
    comparison(copied_dct, exp_dict)

    # Convert from `dict` to `CCD`
    new_detector = klass.from_dict(copied_dct)
    assert type(new_detector) == CCD
    assert valid_ccd == new_detector
    assert valid_ccd is not new_detector
    comparison(copied_dct, exp_dict)
