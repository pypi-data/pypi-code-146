#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

from pathlib import Path

import pytest

import pyxel
from pyxel.observation import Observation
from pyxel.pipelines import Processor


@pytest.mark.parametrize(
    "filename, exp_exc, exp_msg",
    [
        (
            Path("observation_missing_param.yaml"),
            KeyError,
            "Missing parameter: 'pipeline.charge_generation.dark_current.arguments.temperature'",
        ),
        (
            Path("observation_not_enabled.yaml"),
            ValueError,
            "The 'pipeline.charge_generation.dark_current' model referenced in Observation "
            "configuration has not been enabled",
        ),
    ],
)
def test_validate_steps(filename: Path, exp_exc, exp_msg: str):
    """Test method 'Observation.validate_steps'."""
    folder = Path("tests/pipelines/observation/config").resolve()
    assert folder.exists()

    filename = folder / filename
    assert filename.exists()

    # Read the configuration file
    cfg = pyxel.load(filename)

    # Get running mode
    observation = cfg.running_mode
    assert isinstance(observation, Observation)

    # Create a 'Processor' object
    processor = Processor(detector=cfg.detector, pipeline=cfg.pipeline)

    with pytest.raises(exp_exc, match=exp_msg):
        observation.validate_steps(processor)
