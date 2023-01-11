"""
This module declares a MockDriver that is currently used in some
unit test.
"""
# ============================ imports =========================================
from txp.common.edge import EdgeDescriptor
from txp.common.edge import DeviceId
from txp.common.edge import (
    VibrationMock, ImageMock
)
from txp.devices.package_queue import PackageQueueProxy
from txp.devices.drivers.drivers_host import DriversHost
from txp.devices.drivers.driver import (
    Driver,
    DriverState,
    StateReport,
    MalformedEdgeParameterError
)
import threading
import time
import numpy as np
from typing import List, Tuple, Set
import multiprocessing
from txp.common.config import settings
import logging
from enum import Enum
from dataclasses import dataclass
import queue
import os

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


# ==============================================================================
# Class to define a signal component in the frequency domain
# ==============================================================================

class ComponentType(Enum):
    Sine = "sine"
    Cosine = "cosine"
    ComplexExponential = "exp"


@dataclass
class SignalComponentDefinition:
    amplitude: float  # any sematic unit
    frequency: float  # Hertz: cycles per seconds
    phase: float  # seconds
    component_type: ComponentType = ComponentType.Sine

    @property
    def angular_frequency(self) -> float:
        return self.frequency * 2.0 * np.pi

    @property
    def phase_in_radians(self) -> float:
        return self.phase * 2.0 * np.pi


default_components = [
    SignalComponentDefinition(amplitude=3, frequency=1000.0, phase=0.0),
]


# =============================================================================
# Class and functions to define and work with signals
# =============================================================================


@dataclass
class SignalComponent:
    """Spectral Component of a signal class.

    You can define a component for a signal using this class

    Args:
        sampling_frequency: frecuency of sampling.
        definition: SignalComponentDefinition instance for parameters of the spectral component.
        time_axis: Component time axis.
    """

    definition: SignalComponentDefinition
    sampling_frequency: float
    time_axis: np.ndarray

    @property
    def values(self) -> np.ndarray:
        """Given the time axis received in the constructor, we compute
        the values of the signal component."""
        if self.definition.component_type == ComponentType.Sine:
            return self.definition.amplitude * np.sin(self.definition.angular_frequency * self.time_axis)
        if self.definition.component_type == ComponentType.Cosine:
            return self.definition.amplitude * np.cos(self.definition.angular_frequency * self.time_axis)
        if self.definition.component_type == ComponentType.ComplexExponential:
            return np.exp(1.j * self.definition.angular_frequency * self.time_axis)
        else:
            raise Exception("No supported component")


class Signal:
    """Signal class.

    Defines the signal of a dimension in the mock driver

    Args:
        periods_to_synthetize: .
        sampling_frequency: Frequency of sampling.
        spectral_components: List of SignalComponentDefinition, a signal is composed of many components.
    """

    def __init__(self, periods_to_synthetize: float = 38.0, sampling_frequency: float = 800,
                 spectral_components: List[SignalComponentDefinition] = default_components) -> None:
        self.periods_to_synthetize = periods_to_synthetize
        self.sampling_frequency = sampling_frequency
        self.spectral_components = spectral_components
        self.frequencies = [sc.frequency for sc in self.spectral_components]
        self.highest_frequency = max(self.frequencies)
        if (2 * self.highest_frequency) > self.sampling_frequency:
            print("WARNING: your sampling frequency is too low!!!")
        self.lowest_frequency = min(self.frequencies)
        self.signal_period = 1.0 / self.lowest_frequency
        self.sample_count = int((self.sampling_frequency / self.lowest_frequency) * self.periods_to_synthetize)
        self.end_time = self.signal_period * self.periods_to_synthetize
        self.time_axis = np.linspace(0.0, self.end_time, self.sample_count, endpoint=False)
        self.components = [SignalComponent(component, self.sampling_frequency, self.time_axis)
                           for component in self.spectral_components]
        self.signal_amplitude_axis = sum([c.values for c in self.components])
        assert self.sample_count == len(self.signal_amplitude_axis)


def get_signals_per_dimension(edge):
    """Creates signals of each dimension specified in edge descriptor given as argument.
    Args:
        edge: edge with configuration for signals, this function is assuming only one perception.
    """
    components_per_dimension = []
    for components_per_dim in edge.perceptions[VibrationMock.perception_name()][
                                                                            MockDriver.PARAM_COMPONENTS_PER_DIMENSION]:
        components = []
        for component in components_per_dim["components"]:
            components.append(
                SignalComponentDefinition(amplitude=component["amplitude"],
                                          frequency=component["frequency"],
                                          phase=component["phase"],
                                          component_type=ComponentType(component["component_type"]))
            )
        components_per_dimension.append(components)
    signals_per_dimension = []
    for i in range(0, edge.perceptions[VibrationMock.perception_name()][MockDriver.PERCEPTION_DIMENSIONS_FIELD][0]):
        signal = Signal(sampling_frequency=edge.perceptions[VibrationMock.perception_name()][
            MockDriver.PERCEPTION_SAMPLING_FREQUENCY_FIELD],
                        spectral_components=components_per_dimension[i])
        signals_per_dimension.append(signal)
    return signals_per_dimension


def get_image_bytes(image_location):
    with open(image_location, "rb") as image_file:
        image_bytes = image_file.read()
    img = list(image_bytes)
    return (1, len(img)), [img]


# ==============================================================================
# MockDriver class used to test the state machine
# ==============================================================================
class MockDriver(Driver):
    """Mock driver class.

    Defines a known signals generator device for infrastructure testing.

    """

    PARAM_SAMPLE_ALL = "all_possible_samples"
    PARAM_COMPONENTS_PER_DIMENSION = "components_per_dimension"
    CLOCK_PULSE_PARAM = "clock_pulse"

    def __init__(
            self,
            edge_descriptor: EdgeDescriptor,
            package_queue: PackageQueueProxy,
            on_driver_state_changed: callable,
            on_driver_change_state_callback: callable,
            host_clock_notification_queue: queue.Queue
    ):
        Driver.__init__(self, edge_descriptor, package_queue, on_driver_state_changed, host_clock_notification_queue)

        self.on_driver_change_state_callback = on_driver_change_state_callback
        self.vibration_params = {}
        self.image_params = {}
        if VibrationMock.perception_name() in self.perceptions:
            vibration_descriptor = self.perceptions[VibrationMock.perception_name()]
            if len(vibration_descriptor[self.PARAM_COMPONENTS_PER_DIMENSION]) != \
                    vibration_descriptor[self.PERCEPTION_DIMENSIONS_FIELD][0]:
                error = f"""MockDriver: components per dimension list length does not equal edge num of dimensions list 
                length: {len(vibration_descriptor[self.PARAM_COMPONENTS_PER_DIMENSION])} num of dimensions: 
                {vibration_descriptor[self.PERCEPTION_DIMENSIONS_FIELD][0]}
                """
                log.error(error)
                raise MalformedEdgeParameterError(error)

            self.vibration_params["signals_per_dimension"] = get_signals_per_dimension(edge_descriptor)
            self.vibration_params["number_of_dimensions"] = vibration_descriptor[self.PERCEPTION_DIMENSIONS_FIELD][0]
            self.vibration_params["sample_count"] = vibration_descriptor[self.PERCEPTION_DIMENSIONS_FIELD][1]
            sample_count = self.vibration_params["sample_count"]
            for i, signal in enumerate(self.vibration_params["signals_per_dimension"]):
                if signal.sample_count > sample_count:
                    warning = (
                        f"MockDriver. dimension: {i} needs a minimum sampling count of {signal.sample_count} but "
                        f"the configuration is set to {sample_count}. The slower frequencies generated by "
                        f"the mock can be lost.")
                    log.warning(warning)
                elif signal.sample_count <= sample_count:
                    message = (f"MockDriver. dimension: {i} has sampling count = {signal.sample_count} but "
                               f"the configuration is set to {sample_count}")
                    log.info(message)
            self.vibration_params["sampling_frequency"] = vibration_descriptor[
                self.PERCEPTION_SAMPLING_FREQUENCY_FIELD]
            self.vibration_params["sampling_resolution"] = 16

        if ImageMock.perception_name() in self.perceptions:
            image_descriptor = self.perceptions[ImageMock.perception_name()]
            path = os.path.join("resources", image_descriptor["image"])
            file_directory = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(file_directory, path)
            self.image_params["shape"], self.image_params["image"] = get_image_bytes(path)

        self._sample_all_possible = edge_descriptor.edge_parameters.get(self.PARAM_SAMPLE_ALL, False)

        if self.CLOCK_PULSE_PARAM in self.edge_parameters:
            self._clock_pulse: int = self.edge_parameters[self.CLOCK_PULSE_PARAM]
        else:
            self._clock_pulse: int = 20

    @classmethod
    def device_name(cls) -> str:
        return "Mock"

    def observation_pulse(self) -> int:
        return self._clock_pulse

    @classmethod
    def is_virtual(cls) -> bool:
        return False

    def connect_device(self):
        log.info(f"Connecting MockDriver {self.logical_id}")
        self.on_driver_change_state_callback(
            self.logical_id, DriverState.CONNECTED
        )

    def disconnect_device(self):
        log.info(f"Disconnecting MockDriver {self.logical_id}")
        self.on_driver_change_state_callback(
            self.logical_id, DriverState.DISCONNECTED
        )

    def _start_sampling_collect(
            self
    ) -> List["Signals"]:
        signals = []

        while True:
            if self.vibration_params:
                data = []
                for signal in self.vibration_params["signals_per_dimension"]:
                    data.append(signal.signal_amplitude_axis)
                signal = VibrationMock.build_signal_from_numpy(
                    np.array(data),
                    (self.vibration_params["number_of_dimensions"], self.vibration_params["sample_count"]),
                    self.vibration_params["sampling_frequency"],
                    self.vibration_params["sampling_resolution"],
                )
                signals.append(signal)
            if self.image_params:
                signal = ImageMock.build_signal_from_lists(
                    self.image_params["image"],
                    self.image_params["shape"],
                    0,
                    0
                )
                signals.append(signal)
            if self.image_params:
                pass
            if not self._sample_all_possible:
                break   # TODO: Sample all possible not supported right now
            else:
                time.sleep(1)

        log.debug(f"{self.logical_id} will return from sampling collect")
        return signals

    def _stop_sampling_collect(self):
        pass


# ==============================================================================
# MockDriversHost is the Host for mock drivers used in unit testing.
# ==============================================================================
class MockDriversHost(DriversHost):
    # Value requested by the super class.
    mock_driver_errored_timeout_seconds = 15

    def __init__(self, gateway_packages_queue: PackageQueueProxy,
                 drivers_state_queue: multiprocessing.Queue, **kwargs):
        """
        Args:
            gateway_packages_queue: The Gateway package queue to be used by Drivers
                to send collected GatewayPackages.
            **discovered_identifiers: identifiers to mock discovered physical devices.
        """
        super(MockDriversHost, self).__init__(gateway_packages_queue, drivers_state_queue,
                                              self.mock_driver_errored_timeout_seconds, **kwargs)

    def discover_physical_ids(self) -> Set[DeviceId]:
        import random, string
        result = []
        random_string_physical_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        result.append(DeviceId("", random_string_physical_id))
        return result

    def connect(self):
        log.debug("connecting MockDriversHost SDK")
        time.sleep(1)
        log.debug("MockDriversHost SDK connected")

    def disconnect(self):
        log.debug("Disconnecting MockDriversHost SDK")
        time.sleep(1)
        for d in self.drivers:
            d.disconnect_device()
        log.debug("MockDriversHost SDK disconnected")

    def _add_drivers(self, edges: List[EdgeDescriptor]):
        for descriptor in edges:
            driver = MockDriver(descriptor, self.gateway_package_queue,
                                self._on_driver_state_changed, self._change_driver_state,
                                self._completed_driver_pulses_queue)
            self.drivers.append(driver)
            driver.connect_device()  # Connect the driver to update states queue

    def get_driver_host_name(self):
        return MockDriver.device_name()

    def take_fix_error_action(self, serial):
        pass

    def _change_driver_state(self, serial: Tuple, driver_state):
        driver = list(filter(lambda driver: driver.logical_id == serial, self.drivers)).pop()
        driver.update_driver_state(driver_state)
        self._add_drivers_state_to_queue(StateReport(driver.logical_id, driver_state))

    def _predicate_power_on(self, edge_logical_id: str) -> bool:
        return True
