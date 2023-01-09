#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

import pickle
from pathlib import Path

import cloudpickle
import pytest

import pyxel
from pyxel.pipelines import DetectionPipeline


@pytest.fixture
def pipeline_single() -> DetectionPipeline:
    filename_single = Path("tests/data/yaml.yaml")
    assert filename_single.exists()

    cfg = pyxel.load(filename_single)
    pipeline: DetectionPipeline = cfg.pipeline

    return pipeline


@pytest.mark.parametrize("pickle_method", [pickle, cloudpickle])
def test_serialization(pipeline_single: DetectionPipeline, pickle_method):
    """Test serialization/deserialization."""
    data = pickle_method.dumps(pipeline_single)
    assert isinstance(data, bytes)

    obj = pickle_method.loads(data)
    assert isinstance(obj, DetectionPipeline)
    assert obj is not pipeline_single
