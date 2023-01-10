# SPDX-License-Identifier: MIT
# Copyright 2020-2022 Big Bad Wolf Security, LLC

import json
from pathlib import Path

def data(filename: str) -> dict:
    with open(Path(__file__).parent / filename, 'r') as fd:
        return json.load(fd)

services = data("services.json")
resource_types = data("resourcetypes.json")
actions = data("actions.json")