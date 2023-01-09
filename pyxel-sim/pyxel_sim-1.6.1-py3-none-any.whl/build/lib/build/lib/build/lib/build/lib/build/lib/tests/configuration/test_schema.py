#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

import json
from pathlib import Path

import jsonschema
import pytest
from jsonschema import Draft7Validator
from yaml import safe_load


@pytest.fixture(scope="session")
def schema() -> dict:
    filename = Path("static/pyxel_schema.json").resolve()
    assert filename.exists()

    with filename.open() as fh:
        content = json.load(fh)

    Draft7Validator.check_schema(content)

    return content


@pytest.mark.parametrize(
    "filename",
    [
        "tests/configuration/data/calibration.yaml",
        "tests/configuration/data/exposure1.yaml",
        "tests/configuration/data/exposure2.yaml",
        "tests/configuration/data/observation_custom.yaml",
        "tests/configuration/data/observation_custom_parallel.yaml",
        "tests/configuration/data/observation_product.yaml",
        "tests/configuration/data/observation_sequential.yaml",
    ],
)
def test_validate_configuration_file(filename: str, schema: dict):
    """Use a JSON schema to validate a YAML configuration file."""

    full_filename = Path(filename).resolve()
    assert full_filename.exists()

    content: str = full_filename.read_text()

    data = safe_load(content)

    jsonschema.validate(data, schema=schema)
