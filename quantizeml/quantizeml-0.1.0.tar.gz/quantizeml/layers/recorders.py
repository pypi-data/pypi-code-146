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
import keras
import tensorflow as tf
from contextlib import contextmanager

from ..tensors import FixedPoint, QFloat

__all__ = ["recording", "Recorder", "TensorRecorder", "FixedPointRecorder", "QFloatRecorder"]


RECORDING_ENV = "RECORDING_ENABLED"


@contextmanager
def recording(enable):
    """Enable or disable recording.

    Args:
        enable (bool): True to enable recording, False to disable it
    """
    value = "1" if enable else "0"
    _prev_state = os.environ.get(RECORDING_ENV, None)
    try:
        os.environ[RECORDING_ENV] = value
        yield
    finally:
        # Recover default value
        if _prev_state is not None:
            os.environ[RECORDING_ENV] = _prev_state
        else:
            os.environ.pop(RECORDING_ENV)


class Recorder():
    """A class that exhibits a 'recording' property.

    All objects inheriting from this class share the same 'recording' property.

    The property cannot be set: its value is deduced from the RECORDING_ENABLED
    environment variable.
    """

    @property
    def recording(self):
        """Flag to specify if the object is in recording mode or not.

        Returns:
            bool: True if recording mode is enabled, False otherwise.
        """
        value = os.environ.get(RECORDING_ENV, "0")
        return (value == "1")


class TensorRecorder(Recorder, keras.layers.Layer):
    """Wrapper class to store and retrieve a tf.Tensor extracted from a graph.

    This is mainly used to recover FixedPoint alignment shift information.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._var = None

    @property
    def value(self):
        """Get the recorded value.

        Returns:
            :obj:`tf.Tensor`: value of the stored record or None.
        """
        return None if self._var is None else self._var.value()

    def call(self, inputs):
        """Record the values of the inputs if recording is True.

        Args:
            inputs (:obj:`tf.Tensor`): new values.

        Returns:
            :obj:`tf.Tensor`: the inputs.
        """
        if self.recording:
            if self._var is None:
                # Create a new variable to copy values from the graph
                self._var = tf.Variable(
                    inputs,
                    trainable=False,
                    name=self.name + "/record",
                    synchronization=tf.VariableSynchronization.ON_READ
                )
            else:
                # Store the new values
                self._var.assign(inputs)
        return inputs


class FixedPointRecorder(Recorder, keras.layers.Layer):
    """Wrapper class to store and retrieve a FixedPoint extracted from a graph.

    This is mainly used to recover FixedPoint quantized weights.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value_bits = None
        self._values = TensorRecorder()
        self._frac_bits = TensorRecorder()

    @property
    def value(self):
        """Get the recorded value.

        Returns:
            :obj:`FixedPoint`: value of the stored record or None.
        """
        return None if self._value_bits is None else FixedPoint(self._values.value,
                                                                self._value_bits,
                                                                self._frac_bits.value)

    def call(self, inputs):
        """Record the values of the inputs if recording is True.

        Args:
            inputs (:obj:`FixedPoint`): new values.

        Returns:
            :obj:`FixedPoint`: the inputs.
        """
        if self.recording:
            self._value_bits = inputs.value_bits
            self._values(inputs.values)
            self._frac_bits(inputs.frac_bits)
        return inputs


class QFloatRecorder(Recorder, keras.layers.Layer):
    """Wrapper class to store and retrieve a QFloat extracted from a graph.

    This is mainly used to recover QFloat quantized weights.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._fp = FixedPointRecorder()
        self._scales = TensorRecorder()

    @property
    def value(self):
        """Get the recorded value.

        Returns:
            :obj:`QFloat`: value of the stored record or None.
        """
        return None if self._fp.value is None else QFloat(self._fp.value, self._scales.value)

    def call(self, inputs):
        """Record the values of the inputs if recording is True.

        Args:
            inputs (:obj:`QFloat`): new values.

        Returns:
            :obj:`QFloat`: the inputs.
        """
        if self.recording:
            self._fp(inputs.fp)
            self._scales(inputs.scales)
        return inputs
