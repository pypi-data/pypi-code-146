"""
Definitions of classes to support the concept of perception dimensions in the system.

Classes for Signals are provided, with factory methods to facilitate a single way for Drivers to produce
instances of signals.
"""

# ============================ imports =========================================
from abc import ABC
from enum import Enum
from typing import Tuple, List, Union
from dataclasses import dataclass
import array
import numpy as np
import txp.common.protos.gateway_package_pb2 as package_proto
import enum
from txp.common.config import settings
import logging
import time

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class SignalMode(Enum):
    TIME = 0
    TIME_FFT = 1
    TIME_PSD = 2
    TIME_FFT_PSD = 3
    FFT = 4
    FFT_PSD = 5
    PSD = 6
    IMAGE = 7

    @staticmethod
    def is_image(mode):
        return mode == SignalMode.IMAGE.value

    @staticmethod
    def is_time_only(mode):
        return not SignalMode.is_fft(mode) and not SignalMode.is_psd(mode)

    @staticmethod
    def is_time(mode):
        return mode in [SignalMode.TIME.value, SignalMode.TIME_FFT.value, SignalMode.TIME_FFT_PSD.value,
                        SignalMode.TIME_PSD.value,
                        SignalMode.IMAGE.value]

    @staticmethod
    def is_fft(mode):
        return mode in [SignalMode.TIME_FFT.value, SignalMode.TIME_FFT_PSD.value, SignalMode.FFT.value,
                        SignalMode.FFT_PSD.value]

    @staticmethod
    def is_psd(mode):
        return mode in [SignalMode.TIME_PSD.value, SignalMode.TIME_FFT_PSD.value, SignalMode.PSD.value,
                        SignalMode.FFT_PSD.value]


@dataclass
class Signal(ABC):
    """This Signal abstracts the concept of sampled perception dimensions by Edge devices.

    All signals will be shaped in a matrix. Technically, that matrix is created as a List of native arrays.
    Telemetry Protobuf are designed to hold a matrix.
    This is flexible enough for the use cases:

        - A Scalar perception dimension can be represented as a matrix of one row and one column value:
            [[1]]

        - A single axis / double axis / triple axis / n axis perception dimension can be represented as:
            single axis: [[a1 a2 a3 a4 ...... an]]
            double axis: [[a1 ... an], [b1 ... bn]]
            ...

        - Perception dimensions in higher dimensions can be re-shaped to a matrix.


    Args:
        samples((List of native arrays)): The matrix containing the samples for the perceptions.

        perception_dimensions(Tuple[int]): The tuple of ints which indicates the dimensions of the
            perception.

        signal_frequency: The sampling frequency of the signal.

        sampling_resolution: The sampling resolution of the each sample.

        timestamp: a timestamp in nanoseconds when the signal was captured.
    """
    samples: Union[List[array.array]]
    perception_dimensions: Tuple
    signal_frequency: float
    sampling_resolution: int
    timestamp: int

    @classmethod
    def perception_name(cls) -> str:
        """Returns the perception signal name: Vibration, Temperature, ..."""
        pass

    @classmethod
    def is_scalar(cls) -> bool:
        """Concrete signals can describe if they implement an scalar signal"""
        pass

    @classmethod
    def mode(cls) -> SignalMode:
        """Signals will have a processing mode associated"""
        pass

    def get_proto(self) -> package_proto.SignalProto:
        def map_samples_to_protos():
            list_of_dimensions_samples_protos = []
            for array_samples in self.samples:
                proto = package_proto.DimensionSignalSamplesProto()
                proto.samples.extend(array_samples.tolist())
                list_of_dimensions_samples_protos.append(proto)

            return list_of_dimensions_samples_protos

        samples_arrays_protos = map_samples_to_protos()
        signal_proto = package_proto.SignalProto(
            perception_name=self.perception_name(),
            sampling_resolution=self.sampling_resolution,
            signal_frequency=self.signal_frequency,
            timestamp=self.timestamp
        )
        signal_proto.samples.extend(samples_arrays_protos)
        signal_proto.perception_dimensions.extend(list(self.perception_dimensions))

        return signal_proto

    @classmethod
    def build_from_proto(cls, proto: package_proto.SignalProto) -> "Signal":
        if isinstance(proto, package_proto.SignalProto):
            list_of_dimension_signals: List[array.array] = []
            arrays_of_samples = list(proto.samples)
            for dimension_samples in arrays_of_samples:
                l = [float(sample) for sample in dimension_samples.samples]
                list_of_dimension_signals.append(array.array('f', l))

            signal = cls(
                list_of_dimension_signals,
                tuple(proto.perception_dimensions),
                proto.signal_frequency,
                proto.sampling_resolution,
                proto.timestamp
            )

            return signal

        else:
            raise ValueError(
                "Trying to build GatewayConfig from proto, but the proto instance is unknown"
            )

    @classmethod
    def build_signal_from_lists(
            cls,
            samples: List[List],
            perception_dimensions: Tuple,
            signal_frequency: float,
            sampling_resolution: int,
    ) -> "Signal":
        """Builds a signal based on the matrix built as a List of Lists.

        Args:
            samples((List of native arrays)): The matrix containing the samples for the perceptions.
            perception_dimensions(Tuple[int]): The tuple of ints which indicates the dimensions of the
                perception.
            signal_frequency: The sampling frequency of the signal.
            sampling_resolution: The sampling resolution of the each sample.

        Returns:
            Returns the concrete Signal class instance.
        """
        list_of_array_samples: List = [
            array.array("f", samples[i]) for i in range(perception_dimensions[0])
        ]
        timestamp = time.time_ns()
        return cls(
            list_of_array_samples,
            perception_dimensions,
            signal_frequency,
            sampling_resolution,
            timestamp
        )

    @classmethod
    def build_signal_from_numpy(
            cls,
            samples: np.array,
            perception_dimensions: Tuple,
            signal_frequency: float,
            sampling_resolution: int,
    ) -> "Signal":
        """Builds a Signal based on the matrix built as numpy.array

        Args:
            samples((List of native arrays)): The matrix containing the samples for the perceptions.
            perception_dimensions(Tuple[int]): The tuple of ints which indicates the dimensions of the
                perception.
            signal_frequency: The sampling frequency of the signal.
            sampling_resolution: The sampling resolution of the each sample.

        Returns:
            Returns the concrete Signal class instance.
        """
        list_of_array_samples: List = [
            array.array("f", samples[i].tolist())
            for i in range(perception_dimensions[0])
        ]
        timestamp = time.time_ns()
        return cls(
            list_of_array_samples,
            perception_dimensions,
            signal_frequency,
            sampling_resolution,
            timestamp
        )

    @classmethod
    def build_signal_from_value(
            cls, sample: float, signal_frequency: [float, int] = 0.0, sampling_resolution: int = 0
    ) -> "Signal":
        """Build a signal out of an scalar value.

        Args:
            sample (float): the sampled scalar value
            signal_frequency: the frequency of the signal. Preferred to be constant 0 for scalar values.
            sampling_resolution: The sampling resolution. Preferred to be constant 0
                for scalar values. TODO: Check this with team.

        Returns:
            Returns the concrete Signal class instance.
        """
        list_with_sample = [[sample]]
        perception_dimension = (1,)
        return cls.build_signal_from_lists(
            list_with_sample, perception_dimension,
            signal_frequency, sampling_resolution,
        )


# ==============================================================================
# Definition of Concrete Signals classes
# ==============================================================================
class ImageSignal(Signal, ABC):
    """This class provides factory methods to build image signals."""
    @classmethod
    def perception_name(cls) -> str:
        return "Image"

    @classmethod
    def is_scalar(cls) -> bool:
        return False

    @classmethod
    def mode(cls) -> SignalMode:
        """Todo: Hardcoded mode. This should be passed in the edge configuration"""
        return SignalMode.IMAGE

    @classmethod
    def build_signal_from_lists(
            cls,
            image: List[List],
            perception_dimensions: Tuple,
            signal_frequency: float,
            sampling_resolution: int,
    ):
        """Builds an ImageSignal from a Lists of Lists.

        Args:
            image: The list of list of samples representing the image.
            perception_dimensions: The perception dimensions of the Signal.
            signal_frequency: The frequency of the signal.
            sampling_resolution: The sampling resolution.
        Returns:
            The ImageSignal for the given np.array
        """
        return super(ImageSignal, cls).build_signal_from_lists(image, perception_dimensions, signal_frequency,
                                                   sampling_resolution)

    @classmethod
    def build_signal_from_numpy(
            cls,
            image: np.array,
            perception_dimensions: Tuple,
            signal_frequency: float,
            sampling_resolution: int,
    ):
        """Builds an ImageSignal from a numpy array

        Args:
            image: The numpy.array containing the sample values.
            perception_dimensions: The perception dimensions of the signal.
            signal_frequency: The frequency of the signal.
            sampling_resolution: The sampling resolution.
        Returns:
            The ImageSignal for the given np.array
        """
        return super(ImageSignal, cls).build_signal_from_numpy(image, perception_dimensions, signal_frequency,
                                                   sampling_resolution)


class ThermalImageSignal(Signal, ABC):
    """This class provides factory methods to build thermal image signals."""
    @classmethod
    def perception_name(cls) -> str:
        return "ThermalImage"

    @classmethod
    def is_scalar(cls) -> bool:
        return False

    @classmethod
    def mode(cls) -> SignalMode:
        """Todo: Hardcoded mode. This should be passed in the edge configuration"""
        return SignalMode.IMAGE

    @classmethod
    def build_signal_from_lists(
            cls,
            image: List[List],
            perception_dimensions: Tuple,
            signal_frequency: float,
            sampling_resolution: int,
    ):
        """Builds an ThermalImageSignal from a Lists of Lists.

        Args:
            image: The list of list of samples representing the image.
            perception_dimensions: The perception dimensions of the Signal.
            signal_frequency: The frequency of the signal.
            sampling_resolution: The sampling resolution.
        Returns:
            The ImageSignal for the given np.array
        """
        return super(ThermalImageSignal, cls).build_signal_from_lists(image, perception_dimensions, signal_frequency,
                                                               sampling_resolution)

    @classmethod
    def build_signal_from_numpy(
            cls,
            image: np.array,
            perception_dimensions: Tuple,
            signal_frequency: float,
            sampling_resolution: int,
    ):
        """Builds an ImageSignal from a numpy array

        Args:
            image: The numpy.array containing the sample values.
            perception_dimensions: The perception dimensions of the signal.
            signal_frequency: The frequency of the signal.
            sampling_resolution: The sampling resolution.
        Returns:
            The ImageSignal for the given np.array
        """
        return super(ImageSignal, cls).build_signal_from_numpy(image, perception_dimensions, signal_frequency,
                                                               sampling_resolution)

class VibrationSpeedSignal(Signal):
    """This encapsulates a Vibration Speed signal sample.

    The recommended way of creating instances of this class is to use
    the provided factory methods from VectorSignal.

    Args:
        samples: The built-in List of built-in arrays containing the samples.
        perception_dimensions: The perception dimensions shape for this signal.
        signal_frequency: The frequecy for the signal.
        sampling_resolution: The sampling resolution for the signal.
    """

    @classmethod
    def is_scalar(cls) -> bool:
        return False

    @classmethod
    def perception_name(cls) -> str:
        return "VibrationSpeed"

    @classmethod
    def mode(cls) -> SignalMode:
        """Todo: Hardcoded mode. This should be passed in the edge configuration"""
        return SignalMode.TIME_FFT_PSD


class VibrationMock(Signal):
    """This encapsulates a Vibration Speed signal sample from the MockDriver.

    The recommended way of creating instances of this class is to use
    the provided factory methods from VectorSignal.

    Args:
        samples: The built-in List of built-in arrays containing the samples.
        perception_dimensions: The perception dimensions shape for this signal.
        signal_frequency: The frequecy for the signal.
        sampling_resolution: The sampling resolution for the signal.
    """

    @classmethod
    def is_scalar(cls) -> bool:
        return False

    @classmethod
    def perception_name(cls) -> str:
        return "VibrationMock"

    @classmethod
    def mode(cls) -> SignalMode:
        """Todo: Hardcoded mode. This should be passed in the edge configuration"""
        return SignalMode.TIME_FFT_PSD


class VibrationAccelerationSignal(Signal):
    """This encapsulates a Vibration Acceleration signal sample.

    The recommended way of creating instances of this class is to use
    the provided factory methods from VectorSignal.

    Args:
        samples: The built-in List of built-in arrays containing the samples.
        perception_dimensions: The perception dimensions shape for this signal.
        signal_frequency: The frequecy for the signal.
        sampling_resolution: The sampling resolution for the signal.
    """

    @classmethod
    def is_scalar(cls) -> bool:
        return False

    @classmethod
    def perception_name(cls) -> str:
        return "VibrationAcceleration"

    @classmethod
    def mode(cls) -> SignalMode:
        """Todo: Hardcoded mode. This should be passed in the edge configuration"""
        return SignalMode.TIME_FFT_PSD


class MagnetometerSignal(Signal):
    """This encapsulates a Magnetometer signal sample.

    The recommended way of creating instances of this class is to use
    the provided factory methods from VectorSignal.

    Args:
        samples: The built-in List of built-in arrays containing the samples.
        perception_dimensions: The perception dimensions shape for this signal.
        signal_frequency: The frequecy for the signal.
        sampling_resolution: The sampling resolution for the signal.
    """

    @classmethod
    def is_scalar(cls) -> bool:
        return False

    @classmethod
    def perception_name(cls) -> str:
        return "Magnetometer"

    @classmethod
    def mode(cls) -> SignalMode:
        """Todo: Hardcoded mode. This should be passed in the edge configuration"""
        return SignalMode.TIME_FFT_PSD


class MicrophoneSignal(Signal):
    """This encapsulates a Microphone signal sample.

    The recommended way of creating instances of this class is to use
    the provided factory methods from VectorSignal.

    Args:
        samples: The built-in List of built-in arrays containing the samples.
        perception_dimensions: The perception dimensions shape for this signal.
        signal_frequency: The frequecy for the signal.
        sampling_resolution: The sampling resolution for the signal.
    """

    @classmethod
    def is_scalar(cls) -> bool:
        return False

    @classmethod
    def perception_name(cls) -> str:
        return "Microphone"

    @classmethod
    def mode(cls) -> SignalMode:
        """Todo: Hardcoded mode. This should be passed in the edge configuration"""
        return SignalMode.TIME_FFT_PSD


class ImageMock(ImageSignal):
    """This encapsulates an Image signal sample from the MockDriver.

    The recommended way of creating instances of this class is to use
    the provided factory methods from VectorSignal.

    Args:
        image: The built-in List of built-in arrays containing the samples.
        perception_dimensions: The perception dimensions shape for this signal.
        signal_frequency: The frequecy for the signal.
        sampling_resolution: The sampling resolution for the signal.
    """

    @classmethod
    def is_scalar(cls) -> bool:
        return False

    @classmethod
    def perception_name(cls) -> str:
        return "ImageMock"

    @classmethod
    def mode(cls) -> SignalMode:
        """Todo: Hardcoded mode. This should be passed in the edge configuration"""
        return SignalMode.IMAGE


@dataclass
class TemperatureSignal(Signal):
    """This signal encapsulates a temperature measurement as an scalar sample.

    The recommended way of creating instances of this class is to use
    the provided factory methods from ScalarSignal.

    The shape is expected to be described by the tuple value of (1,).
    The samples are expected to be a list of a single array with only one value, in
        order to be consistent with the others signals.
    The signal_frequency is a constant and the
    """
    @classmethod
    def is_scalar(cls) -> bool:
        return True

    @classmethod
    def perception_name(cls) -> str:
        return "Temperature"

    @classmethod
    def mode(cls) -> SignalMode:
        """Todo: Hardcoded mode. This should be passed in the edge configuration"""
        return SignalMode.TIME


class SignalsTableByName(enum.Enum):
    def __new__(cls, signal_class: Signal):
        obj = object.__new__(cls)
        obj._value_ = signal_class.perception_name()
        obj.signal = signal_class
        return obj

    VIBRATION_SPEED = VibrationSpeedSignal
    VIBRATION_ACCELERATION = VibrationAccelerationSignal
    VIBRATION_MOCK = VibrationMock
    MAGNETOMETER = MagnetometerSignal
    MICROPHONE = MicrophoneSignal
    TEMPERATURE = TemperatureSignal
    IMAGE = ImageSignal
    IMAGEMOCK = ImageMock
