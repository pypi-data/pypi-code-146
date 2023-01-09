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
    MKID,
    Detector,
    Environment,
    MKIDCharacteristics,
    MKIDGeometry,
)


@pytest.fixture
def valid_mkid() -> MKID:
    """Create a valid `MKID`."""
    return MKID(
        geometry=MKIDGeometry(
            row=100,
            col=120,
            total_thickness=123.1,
            pixel_horz_size=12.4,
            pixel_vert_size=34.5,
        ),
        environment=Environment(temperature=100.1),
        characteristics=MKIDCharacteristics(
            quantum_efficiency=0.1,
            charge_to_volt_conversion=0.2,
            pre_amplification=3.3,
        ),
    )


@pytest.mark.parametrize(
    "other_obj, is_equal",
    [
        pytest.param(None, False, id="None"),
        pytest.param(
            MKID(
                geometry=MKIDGeometry(row=100, col=120),
                environment=Environment(),
                characteristics=MKIDCharacteristics(),
            ),
            False,
            id="Empty 'MKID'",
        ),
        pytest.param(
            MKID(
                geometry=MKIDGeometry(
                    row=100,
                    col=120,
                    total_thickness=123.1,
                    pixel_horz_size=12.4,
                    pixel_vert_size=34.5,
                ),
                environment=Environment(),
                characteristics=MKIDCharacteristics(),
            ),
            False,
            id="Almost same parameters, different class",
        ),
        pytest.param(
            MKID(
                geometry=MKIDGeometry(
                    row=100,
                    col=120,
                    total_thickness=123.1,
                    pixel_horz_size=12.4,
                    pixel_vert_size=34.5,
                ),
                environment=Environment(temperature=100.1),
                characteristics=MKIDCharacteristics(
                    quantum_efficiency=0.1,
                    charge_to_volt_conversion=0.2,
                    pre_amplification=3.3,
                ),
            ),
            True,
            id="Same parameters, same class",
        ),
    ],
)
def test_is_equal(valid_mkid: MKID, other_obj, is_equal):
    """Test equality statement for `MKID`."""

    if is_equal:
        assert valid_mkid == other_obj
    else:
        assert valid_mkid != other_obj


def test_is_equal_with_arrays(valid_mkid: MKID):
    other_detector = deepcopy(valid_mkid)

    assert valid_mkid.geometry is not other_detector.geometry
    assert valid_mkid.environment is not other_detector.environment
    assert valid_mkid.characteristics is not other_detector.characteristics
    assert valid_mkid._photon is not other_detector._photon
    assert valid_mkid._charge is not other_detector._charge
    assert valid_mkid._pixel is not other_detector._pixel
    assert valid_mkid._signal is not other_detector._signal
    assert valid_mkid._image is not other_detector._image
    assert valid_mkid._phase is not other_detector._phase

    shape = valid_mkid.geometry.row, valid_mkid.geometry.col
    photon: np.ndarray = np.random.random(size=shape)
    pixel: np.ndarray = np.random.random(size=shape)
    signal: np.ndarray = np.random.random(size=shape)
    image: np.ndarray = np.random.random(size=shape)
    charge: np.ndarray = np.random.random(size=shape)
    phase: np.ndarray = np.random.random(size=shape)

    valid_mkid.photon.array = photon.copy()
    valid_mkid.pixel.array = pixel.copy()
    valid_mkid.signal.array = signal.copy()
    valid_mkid.image.array = image.copy()
    valid_mkid.phase.array = phase.copy()

    valid_mkid.charge._array = charge.copy()
    valid_mkid.charge._frame.append({"charge": 1}, ignore_index=True)

    other_detector.photon.array = photon.copy()
    other_detector.pixel.array = pixel.copy()
    other_detector.signal.array = signal.copy()
    other_detector.image.array = image.copy()
    other_detector.phase.array = phase.copy()

    other_detector.charge._array = charge.copy()
    other_detector.charge._frame.append({"charge": 1}, ignore_index=True)

    assert valid_mkid == other_detector


def comparison(dct, other_dct):
    assert set(dct) == set(other_dct) == {"version", "type", "data", "properties"}
    assert dct["version"] == other_dct["version"]
    assert dct["type"] == other_dct["type"]
    assert dct["properties"] == other_dct["properties"]

    assert (
        set(dct["data"])
        == set(other_dct["data"])
        == {
            "photon",
            "scene",
            "pixel",
            "signal",
            "image",
            "phase",
            "charge",
            "processed_data",
        }
    )
    np.testing.assert_equal(dct["data"]["photon"], other_dct["data"]["photon"])
    np.testing.assert_equal(dct["data"]["pixel"], other_dct["data"]["pixel"])
    np.testing.assert_equal(dct["data"]["signal"], other_dct["data"]["signal"])
    np.testing.assert_equal(dct["data"]["image"], other_dct["data"]["image"])
    np.testing.assert_equal(dct["data"]["phase"], other_dct["data"]["phase"])

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


@pytest.mark.parametrize("klass", [MKID, Detector])
@pytest.mark.parametrize(
    "obj, exp_dict",
    [
        pytest.param(
            MKID(
                geometry=MKIDGeometry(row=100, col=120),
                environment=Environment(),
                characteristics=MKIDCharacteristics(),
            ),
            {
                "version": 1,
                "type": "MKID",
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
                    "phase": np.zeros(shape=(100, 120)),
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
            id="Default Parameters",
        ),
        pytest.param(
            MKID(
                geometry=MKIDGeometry(
                    row=100,
                    col=120,
                    total_thickness=123.1,
                    pixel_horz_size=12.4,
                    pixel_vert_size=34.5,
                ),
                environment=Environment(temperature=100.1),
                characteristics=MKIDCharacteristics(
                    quantum_efficiency=0.1,
                    charge_to_volt_conversion=0.2,
                    pre_amplification=3.3,
                    adc_bit_resolution=16,
                    adc_voltage_range=(0.0, 10.0),
                ),
            ),
            {
                "version": 1,
                "type": "MKID",
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
                        "full_well_capacity": None,
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
                    "phase": np.zeros(shape=(100, 120)),
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
            id="MKID fully defined",
        ),
    ],
)
def test_to_and_from_dict(klass, obj, exp_dict):
    """Test methods 'to_dict', 'from_dict'."""
    assert type(obj) == MKID

    # Convert from `MKID` to a `dict`
    dct = obj.to_dict()
    comparison(dct, exp_dict)

    # Copy 'exp_dict'
    copied_dct = deepcopy(exp_dict)  # create a new dict
    assert copied_dct is not exp_dict
    comparison(copied_dct, exp_dict)

    # Convert from `dict` to `MKID`
    other_obj = klass.from_dict(copied_dct)
    assert type(other_obj) == MKID
    assert obj == other_obj
    assert obj is not other_obj
    comparison(copied_dct, exp_dict)
