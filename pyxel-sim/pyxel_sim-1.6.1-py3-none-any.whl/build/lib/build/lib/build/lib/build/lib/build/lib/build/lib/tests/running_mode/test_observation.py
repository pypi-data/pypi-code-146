#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

from pathlib import Path

import dask
import numpy as np
import pytest
import xarray as xr

import pyxel
from pyxel.configuration import Configuration
from pyxel.detectors import CCD
from pyxel.observation import Observation, ObservationResult, ParameterMode
from pyxel.pipelines import DetectionPipeline

dask.config.set(scheduler="single-threaded")


@pytest.mark.parametrize("with_dask", [False, True])
def test_product_simple(with_dask: bool):
    """Test running mode 'observation'."""
    filename = Path("tests/running_mode/data/observation_product_simple.yaml")
    assert filename.exists()

    cfg = pyxel.load(filename)
    assert isinstance(cfg, Configuration)

    observation = cfg.observation
    detector = cfg.detector
    pipeline = cfg.pipeline

    observation.with_dask = with_dask

    assert isinstance(observation, Observation)
    assert observation.parameter_mode == ParameterMode.Product

    assert isinstance(detector, CCD)
    assert isinstance(pipeline, DetectionPipeline)

    result = pyxel.observation_mode(
        observation=observation, detector=detector, pipeline=pipeline
    )
    assert isinstance(result, ObservationResult)

    # Check '.dataset'
    ds = result.dataset
    assert isinstance(ds, xr.Dataset)

    assert list(ds["image"].coords) == [
        "readout_time",
        "y",
        "x",
        "level",
        "quantum_efficiency",
    ]
    assert list(ds["image"].coords["readout_time"].values) == [1]
    assert list(ds["image"].coords["y"].values) == list(range(100))
    assert list(ds["image"].coords["x"].values) == list(range(100))
    assert list(ds["image"].coords["level"].values) == [10, 20, 30]
    assert list(ds["image"].coords["quantum_efficiency"].values) == [0.5, 0.8, 0.9]

    # Check '.parameters'
    parameters = result.parameters
    assert isinstance(parameters, xr.Dataset)

    exp_parameters = xr.Dataset(
        {
            "level": xr.DataArray(
                [10, 20, 30], dims="level_id", coords={"level_id": [0, 1, 2]}
            ),
            "quantum_efficiency": xr.DataArray(
                [0.5, 0.8, 0.9],
                dims="quantum_efficiency_id",
                coords={"quantum_efficiency_id": [0, 1, 2]},
            ),
        }
    )
    xr.testing.assert_equal(parameters, exp_parameters)

    # Check '.logs'
    logs = result.logs
    assert isinstance(logs, xr.Dataset)

    exp_logs = xr.Dataset(
        {
            "level": xr.DataArray([10, 10, 10, 20, 20, 20, 30, 30, 30], dims="id"),
            "quantum_efficiency": xr.DataArray(
                [0.5, 0.8, 0.9, 0.5, 0.8, 0.9, 0.5, 0.8, 0.9], dims="id"
            ),
        },
        coords={"id": [0, 1, 2, 3, 4, 5, 6, 7, 8]},
    )
    xr.testing.assert_equal(logs, exp_logs)


@pytest.mark.parametrize("with_dask", [False, True])
def test_product(with_dask: bool):
    """Test running mode 'observation'."""
    filename = Path("tests/running_mode/data/observation_product.yaml")
    assert filename.exists()

    cfg = pyxel.load(filename)
    assert isinstance(cfg, Configuration)

    observation = cfg.observation
    detector = cfg.detector
    pipeline = cfg.pipeline

    observation.with_dask = with_dask

    assert isinstance(observation, Observation)
    assert observation.parameter_mode == ParameterMode.Product

    assert isinstance(detector, CCD)
    assert isinstance(pipeline, DetectionPipeline)

    result = pyxel.observation_mode(
        observation=observation, detector=detector, pipeline=pipeline
    )
    assert isinstance(result, ObservationResult)

    # Check '.dataset'
    ds = result.dataset
    assert isinstance(ds, xr.Dataset)

    assert list(ds["image"].coords) == [
        "readout_time",
        "y",
        "x",
        "illumination_uniform.level",
        "illumination_elliptic.level",
        "quantum_efficiency",
    ]
    assert list(ds["image"].coords["readout_time"].values) == [1]
    assert list(ds["image"].coords["y"].values) == list(range(100))
    assert list(ds["image"].coords["x"].values) == list(range(100))
    assert list(ds["image"].coords["illumination_uniform.level"].values) == [10, 20, 30]
    assert list(ds["image"].coords["illumination_elliptic.level"].values) == [
        100,
        200,
        300,
    ]
    assert list(ds["image"].coords["quantum_efficiency"].values) == [0.5, 0.8, 0.9]

    # Check '.parameters'
    parameters = result.parameters
    assert isinstance(parameters, xr.Dataset)

    exp_parameters = xr.Dataset(
        {
            "illumination_uniform.level": xr.DataArray(
                [10, 20, 30],
                dims="illumination_uniform.level_id",
                coords={"illumination_uniform.level_id": [0, 1, 2]},
            ),
            "illumination_elliptic.level": xr.DataArray(
                [100, 200, 300],
                dims="illumination_elliptic.level_id",
                coords={"illumination_elliptic.level_id": [0, 1, 2]},
            ),
            "quantum_efficiency": xr.DataArray(
                [0.5, 0.8, 0.9],
                dims="quantum_efficiency_id",
                coords={"quantum_efficiency_id": [0, 1, 2]},
            ),
        }
    )
    xr.testing.assert_equal(parameters, exp_parameters)

    # Check '.logs'
    logs = result.logs
    assert isinstance(logs, xr.Dataset)

    exp_logs = xr.Dataset(
        {
            "level": xr.DataArray(
                ([100] * 3 + [200] * 3 + [300] * 3) * 3,
                dims="id",
            ),
            "quantum_efficiency": xr.DataArray(
                [0.5, 0.8, 0.9] * 9,
                dims="id",
            ),
        },
        coords={"id": range(27)},
    )
    xr.testing.assert_equal(logs, exp_logs)


@pytest.mark.parametrize("with_dask", [False, True])
def test_sequential_simple(with_dask: bool):
    """Test running mode 'sequential'."""
    filename = Path("tests/running_mode/data/observation_sequential_simple.yaml")
    assert filename.exists()

    cfg = pyxel.load(filename)
    assert isinstance(cfg, Configuration)

    observation = cfg.observation
    detector = cfg.detector
    pipeline = cfg.pipeline

    observation.with_dask = with_dask

    assert isinstance(observation, Observation)
    assert observation.parameter_mode == ParameterMode.Sequential

    assert isinstance(detector, CCD)
    assert isinstance(pipeline, DetectionPipeline)

    result = pyxel.observation_mode(
        observation=observation, detector=detector, pipeline=pipeline
    )
    assert isinstance(result, ObservationResult)

    # Check '.dataset'
    ds_dict = result.dataset
    assert isinstance(ds_dict, dict)

    assert list(ds_dict) == ["level", "quantum_efficiency"]

    assert isinstance(ds_dict["level"], xr.Dataset)

    assert list(ds_dict["level"]["image"].coords) == ["readout_time", "y", "x", "level"]

    assert list(ds_dict["level"]["image"].coords["readout_time"].values) == [1]
    assert list(ds_dict["level"]["image"].coords["y"].values) == list(range(100))
    assert list(ds_dict["level"]["image"].coords["x"].values) == list(range(100))
    assert list(ds_dict["level"]["image"].coords["level"].values) == [10, 20, 30]

    assert list(ds_dict["quantum_efficiency"]["image"].coords) == [
        "readout_time",
        "y",
        "x",
        "quantum_efficiency",
    ]

    assert list(
        ds_dict["quantum_efficiency"]["image"].coords["readout_time"].values
    ) == [1]
    assert list(ds_dict["quantum_efficiency"]["image"].coords["y"].values) == list(
        range(100)
    )
    assert list(ds_dict["quantum_efficiency"]["image"].coords["x"].values) == list(
        range(100)
    )
    assert list(
        ds_dict["quantum_efficiency"]["image"].coords["quantum_efficiency"].values
    ) == [0.5, 0.8, 0.9]

    # Check '.parameters'
    parameters = result.parameters
    assert isinstance(parameters, xr.Dataset)

    exp_parameters = xr.Dataset(
        {
            "level": xr.DataArray(
                [10, 20, 30], dims="level_id", coords={"level_id": [0, 1, 2]}
            ),
            "quantum_efficiency": xr.DataArray(
                [0.5, 0.8, 0.9],
                dims="quantum_efficiency_id",
                coords={"quantum_efficiency_id": [0, 1, 2]},
            ),
        }
    )
    xr.testing.assert_equal(parameters, exp_parameters)

    # Check '.logs'
    logs = result.logs
    assert isinstance(logs, xr.Dataset)

    exp_logs = xr.Dataset(
        {
            "level": xr.DataArray(
                [10.0, 20.0, 30.0, np.nan, np.nan, np.nan], dims="id"
            ),
            "quantum_efficiency": xr.DataArray(
                [np.nan, np.nan, np.nan, 0.5, 0.8, 0.9], dims="id"
            ),
        },
        coords={"id": [0, 1, 2, 3, 4, 5]},
    )
    xr.testing.assert_equal(logs, exp_logs)


@pytest.mark.skip(reason="Fix this test")
@pytest.mark.parametrize("with_dask", [False, True])
def test_sequential(with_dask: bool):
    """Test running mode 'sequential'."""
    filename = Path("tests/running_mode/data/observation_sequential.yaml")
    assert filename.exists()

    cfg = pyxel.load(filename)
    assert isinstance(cfg, Configuration)

    observation = cfg.observation
    detector = cfg.detector
    pipeline = cfg.pipeline

    observation.with_dask = with_dask

    assert isinstance(observation, Observation)
    assert observation.parameter_mode == ParameterMode.Sequential

    assert isinstance(detector, CCD)
    assert isinstance(pipeline, DetectionPipeline)

    result = pyxel.observation_mode(
        observation=observation, detector=detector, pipeline=pipeline
    )
    assert isinstance(result, ObservationResult)

    # Check '.dataset'
    ds_dict = result.dataset
    assert isinstance(ds_dict, dict)

    assert list(ds_dict) == [
        "illumination_uniform.level",
        "illumination_elliptic.level",
        "quantum_efficiency",
    ]

    assert isinstance(ds_dict["illumination_uniform"], xr.Dataset)

    assert list(ds_dict["illumination_uniform.level"]["image"].coords) == [
        "readout_time",
        "y",
        "x",
        "illumination_uniform.level",
    ]

    assert list(
        ds_dict["illumination_uniform.level"]["image"].coords["readout_time"].values
    ) == [1]
    assert list(
        ds_dict["illumination_uniform.level"]["image"].coords["y"].values
    ) == list(range(100))
    assert list(
        ds_dict["illumination_uniform.level"]["image"].coords["x"].values
    ) == list(range(100))
    assert list(
        ds_dict["illumination_uniform.level"]["image"]
        .coords["illumination_uniform.level"]
        .values
    ) == [10, 20, 30]

    assert list(ds_dict["quantum_efficiency"]["image"].coords) == [
        "readout_time",
        "y",
        "x",
        "quantum_efficiency",
    ]

    assert list(
        ds_dict["quantum_efficiency"]["image"].coords["readout_time"].values
    ) == [1]
    assert list(ds_dict["quantum_efficiency"]["image"].coords["y"].values) == list(
        range(100)
    )
    assert list(ds_dict["quantum_efficiency"]["image"].coords["x"].values) == list(
        range(100)
    )
    assert list(
        ds_dict["quantum_efficiency"]["image"].coords["quantum_efficiency"].values
    ) == [0.5, 0.8, 0.9]

    # Check '.parameters'
    parameters = result.parameters
    assert isinstance(parameters, xr.Dataset)

    exp_parameters = xr.Dataset(
        {
            "level": xr.DataArray(
                [10, 20, 30], dims="level_id", coords={"level_id": [0, 1, 2]}
            ),
            "quantum_efficiency": xr.DataArray(
                [0.5, 0.8, 0.9],
                dims="quantum_efficiency_id",
                coords={"quantum_efficiency_id": [0, 1, 2]},
            ),
        }
    )
    xr.testing.assert_equal(parameters, exp_parameters)

    # Check '.logs'
    logs = result.logs
    assert isinstance(logs, xr.Dataset)

    exp_logs = xr.Dataset(
        {
            "level": xr.DataArray(
                [10.0, 20.0, 30.0, np.nan, np.nan, np.nan], dims="id"
            ),
            "quantum_efficiency": xr.DataArray(
                [np.nan, np.nan, np.nan, 0.5, 0.8, 0.9], dims="id"
            ),
        },
        coords={"id": [0, 1, 2, 3, 4, 5]},
    )
    xr.testing.assert_equal(logs, exp_logs)
