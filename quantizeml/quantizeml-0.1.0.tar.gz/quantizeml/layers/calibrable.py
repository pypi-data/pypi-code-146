#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
import os
from contextlib import contextmanager


__all__ = ["Calibrable", "calibration"]


CALIBRATION_ENV = "CALIBRATION_ENABLED"


@contextmanager
def calibration(enable):
    """Enable or disable calibration.

    Args:
        enable (bool): True to enable calibration, False to disable it
    """
    value = "1" if enable else "0"
    _prev_state = os.environ.get(CALIBRATION_ENV, None)
    try:
        os.environ[CALIBRATION_ENV] = value
        yield
    finally:
        # Recover default value
        if _prev_state is not None:
            os.environ[CALIBRATION_ENV] = _prev_state
        else:
            os.environ.pop(CALIBRATION_ENV)


class Calibrable():
    """A class that exhibits a 'calibration' property.

    All objects inheriting from this class share the same 'calibration' property.

    The property cannot be set: its value is deduced from the CALIBRATION_ENABLED
    environment variable.
    """

    @property
    def calibration(self):
        """Flag to specify if the object is in calibration mode or not.

        Returns:
            bool: True if calibration mode is enabled, False otherwise.
        """
        value = os.environ.get(CALIBRATION_ENV, "0")
        return (value == "1")
