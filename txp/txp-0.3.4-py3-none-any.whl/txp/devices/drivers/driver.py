"""
This module contains classes to support the Driver conceptualization.
"""

# ============================ imports =========================================
import copy
from enum import Enum
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from txp.common.edge import EdgeDescriptor, SignalMode
from txp.common.edge import DeviceId
from txp.common.edge import Signal
from txp.devices.package import (
    GatewayPackage,
    GatewayPackageMetadata,
)
from txp.devices.package_queue import PackageQueueProxy
from txp.devices.sampling_task import SamplingTask
import numpy as np
import datetime
import queue
import threading
import time
from typing import List, Dict
from txp.common.config import settings
import logging
from collections import deque
import pytz

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


# ==============================================================================
# Class to encapsulate the DriverState
# ==============================================================================
class DriverState(Enum):
    """A Driver state encapsulation to propagate state across components.
    STATES ARE:
    DISCONNECTED: means that the driver is disconnected
    CONNECTED: driver is connected and ready to sample. When driver is sampling it goes from SAMPLING to CONNECTED
               during the sampling window. Meaning that when  connected there are no pending tasks to be performed
               by the driver
    SAMPLING: means that the driver is currently collecting signals measures
    RECOVERING: this can be used by the host to perform an automatic recovery action from the host and avoid to
                notify that the driver is disconnected if it can be reconnected automatically.
    ERRORED: meaning that it wasnt possible to determine a knonw state for the driver. like CONNECTED or DISCONNECTED.
            this is probably the persisten state that must trigger a human interaction with the physical driver
            to determine the source of the error.
    Note: This class is expected to grow with time.

    """
    DISCONNECTED = 0, 'Disconnected'
    CONNECTED = 1, 'Connected'
    SAMPLING = 4, 'Sampling'
    RECOVERING = 2, 'Recovering'
    ERRORED = 3, 'Errored'  # this state means that the device was connected and not having data on a sampling window

    def __new__(cls, *values):
        """This defines the cannonical value (int) for the enum, and allows for other
        values. Useful for human readable strings.

        Reference for this solution:
            https://stackoverflow.com/questions/43202777/get-enum-name-from-multiple-values-python
        """
        obj = object.__new__(cls)
        obj._value_ = values[0]
        for other_value in values[1:]:
            cls._value2member_map_[other_value] = obj
        obj._all_values = values
        # human readable value useful for sending payload information to other systems
        obj.human_readable_value = values[1]
        return obj


@dataclass
class StateReport:
    """
    this class has 2 items of information.
    serial: logical serial id of the driver
    state: ReportingDriverState
    #TODO: Include Task ID for imcompleted task
    """
    logical_id: str
    driver_state: DriverState
    since_datetime: datetime.datetime = None
    driver_context: Dict = field(default_factory=dict)

    def __post_init__(self):
        # Compute datetime for the state
        self.since_datetime = datetime.datetime.now(
            pytz.timezone(settings.gateway.timezone)
        ).replace(microsecond=0)


# ==============================================================================
# Definition of the Base Driver class
# ==============================================================================
class Driver(ABC):
    """This Driver is the generic concept of a software component that interacts and
    represents one edge device.

    This Driver base class takes care of communication with the associated Gateway. Doing so,
    child drivers will only need to deal with interactions related to the specific hardware device,
    while delegating information sending to the base implemented methods.
    This Driver base supports an internal state machine, which is used to provide
    built-in states and transitions for the derived classes.
    """

    # each package size should be within [170000, 180000]
    _max_size_packages = (170000, 180000)

    # Standard perception dimensions fields common to all edges
    PERCEPTION_DIMENSIONS_FIELD = "dimensions"
    PERCEPTION_SAMPLING_FREQUENCY_FIELD = "sampling_frequency"

    # All drivers must define a physical_id edge parameter.
    _PHYSICAL_ID_PARAM_FIELD = "physical_id"

    def __init__(
            self,
            edge_descriptor: EdgeDescriptor,
            package_queue: PackageQueueProxy,
            on_driver_state_changed: callable,
            completed_clocks_notif_queue: queue.Queue
    ):
        """The Driver initialization process.

        After setting up the attributes for the driver, the machine state is declared.
        However, the Driver instance should call the `connect_device()ß` method to
        initialize the state in the derived class. This allows the derived driver to
        setup any required code at initialization time before trying to connect.

        Args
            edge_descriptor: The description of the edge handled by this driver.
            sampling_window: The sampling configuration window set in the gateway
                for this driver.
            package_queue: The Package queue to send produced packages by this Driver.
            edge_descriptor: The EdgeDescriptor for the edges connected to this driver
            host_notification_queue: The host queue where this driver will publish the
                appropriated reports everytime it finishes an observation window and
                produces a GatewayPackage.
        """
        # Data
        self.logical_id: str = edge_descriptor.logical_id

        self._physical_id: str = edge_descriptor.edge_parameters[self._PHYSICAL_ID_PARAM_FIELD]
        """_physical_id(str): The string representation of the physical ID of the edge, used to define 
        the complete DeviceId"""

        self.device_kind: str = edge_descriptor.device_kind
        self.edge_parameters: Dict = edge_descriptor.edge_parameters

        self.perceptions: Dict = edge_descriptor.perceptions
        """perceptions: The perception dimensions supported by the driver. They are received as a field inside the 
        edge_parameters constructor parameter"""

        if not self.perceptions:
            log.error(
                f"Driver: Empty perceptions received in Edge Descriptor."
            )
            raise EdgeParameterNotFoundError(
                f"Driver: Empty perceptions received in Edge Descriptor"
            )

        self.package_queue: PackageQueueProxy = package_queue
        self.pending_tasks_queue: queue.Queue = queue.Queue()
        self.driver_state = DriverState.DISCONNECTED
        self.on_driver_state_changed = on_driver_state_changed
        self._update_state_lock = threading.Lock()

        """
        Window sampling control attributes
        """
        self._sampling_thread: threading.Thread = None
        """_sampling_thread: is the thread of control that will be used to 
        monitor the sampling process according to the defined cadence."""

        self._sampling_thread_pill: threading.Event = None
        """_sampling_thread_pill: A Kill pill for the thread"""

        self._observation_pulse_signal: threading.Event = threading.Event()
        """_observation_pulse_signal: This control event is used by the upper layers to 
        authorize the driver to start a observation pulse at some point in time."""

        self._stop_current_pulse_signal: threading.Event = threading.Event()
        """_stop_current_pulse_signal: This attribute allows the driver to know if somebody stopped its current
        sampling clock performed by the method _start_sampling_collect."""

        self._completed_clocks_notif_queue: queue.Queue = completed_clocks_notif_queue

        self._sampling_window_finished: threading.Event = threading.Event()
        """_sampling_window_finished: an event that allows the driver to know when a sampling 
        window was completed and the it can proceed to send the packages."""

        self._driver_context: Dict = {}  # A custom driver context to be sent in the edge state report.

    @abstractmethod
    def observation_pulse(self) -> int:
        """Returns the Observation pulse of the Driver which is used for the
        synchronization tasks clock in the system

        Returns:
            The observation pulse in seconds.
        """
        pass

    @classmethod
    @abstractmethod
    def device_name(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def is_virtual(cls) -> bool:
        """Each Driver should declare in the implementation if it is a
        virtual driver or not.
        There's a correspondence between the EdgeDescriptor device_kind and
        the Driver's device_name() method. By knowing the device_kind of an EdgeDescriptor,
        is possible to know if the Driver is virtual or not.
        """
        pass

    def clear_pending_task_queue(self):
        while not self.pending_tasks_queue.empty():
            self.pending_tasks_queue.get()

    def enable_observation_pulse(self) -> None:
        log.info(f"Driver {self.logical_id} was enabled for a new driver's observation period")
        self._observation_pulse_signal.set()

    def disable_current_pulse(self) -> None:
        log.info(f"Driver {self.logical_id} was requested to stop its current sampling collect pulse.")
        self._stop_current_pulse_signal.set()

    def get_complete_device_id(self) -> DeviceId:
        """Returns the defined DeviceId for the edge device.

        The DeviceId for an edge is the combination of the logical_id and the physical_id.
        This association is made through the devices pairing process.
        """
        return DeviceId(self.logical_id, self._physical_id)

    def get_descriptor(self) -> EdgeDescriptor:
        return EdgeDescriptor(
            self.logical_id,
            self.device_kind,
            self.device_name(),
            self.edge_parameters,
            self.perceptions
        )

    def get_state(self) -> DriverState:
        return self.driver_state

    def update_driver_state(self, driver_state: DriverState):
        try:
            self._update_state_lock.acquire(True)
            if self.driver_state == DriverState.DISCONNECTED:
                if driver_state != DriverState.CONNECTED:
                    log.error("{} Invalid transition current state is {} and only allows transitions to: {}".format(
                        self.logical_id, self.driver_state, DriverState.CONNECTED.name))
        finally:
            self.driver_state = driver_state
            log.info("{} device state is {}".format(self.logical_id, self.driver_state))
            self._update_state_lock.release()

    def _send_package_to_gateway(self, package: GatewayPackage):
        """Send the produced package to the central PackageQueue."""
        self.package_queue.add_package(package)

    def receive_sampling_task(self, task: SamplingTask):
        """Receives a new sampling task for this Driver.
        The driver implementation ensures to eventually process this task.
        """
        log.debug(f"Driver {self.logical_id} Receive Sampling Task")
        self.pending_tasks_queue.put(task)

    def has_pending_tasks(self) -> bool:
        """Checks if there are pending tasks to be processed.
        :return: True if there are pending tasks in the queue; otherwise False.
        """
        return not self.pending_tasks_queue.empty()

    @abstractmethod
    def connect_device(self):
        """Connect the device handled by the Driver.

        After the connection succeed or fails, the state of the
        driver should change accordingly. The suggested way is
        to use the defined transitions:
            Connection success:
                self._device_connected()
            Connection Fails:
                self._device_disconnected()
        """
        pass

    @abstractmethod
    def disconnect_device(self):
        """Disconnects the device handled by the  Driver.

        After the device gets disconnected, the state of the driver
        should reflect the change. The suggested way is to use the
        defined transition:
            self._device_disconnected()
        """
        pass

    @abstractmethod
    def _start_sampling_collect(self) -> List[Signal]:
        """This method will collect the samples obtained from the edge device and will
        produce the system Signals to send the package to the gateway.

        This method will collect the samples from a driver clock pulse.
        """
        pass

    @abstractmethod
    def _stop_sampling_collect(self):
        """This method will stop the sampling collection in the driver implementation.
        It can be used to clean resources using during the samples collection process.
        """
        pass

    def start_sampling_windows(self):
        """Call this method to start the _sampling_thread"""
        if self.driver_state == DriverState.CONNECTED:
            if self._sampling_thread is None:
                # Clear timer pill from any previous use
                self._sampling_thread_pill = threading.Event()

                self._sampling_thread = threading.Thread(
                    target=self._sampling_windows_loop,
                    name=f"window_timer_thread_{self.logical_id}",
                    daemon=True,
                    args=(self._sampling_thread_pill,),
                )

                log.info(f"Starting a new sampling thread in Driver: {self.logical_id}")
                self._sampling_thread.start()
            else:
                log.warning(
                    "Trying to start a sampling thread. But there is one already started."
                    "The driver must explicitly stop with _stop_sampling() call."
                )
        else:
            log.warning(
                "Cannot start sampling window. Invalid DriverState. Driver serial {} state {}".format(self.logical_id,
                                                                                                      self.driver_state))

    def notify_sampling_window_completed(self) -> None:
        log.info(f"Driver {self.logical_id} was notified of sampling window completion")
        self._sampling_window_finished.set()

    def stop_sampling_windows(self):
        """Set the _sampling_thread_pill in order to finish the current
        _sampling_thread"""
        if self._sampling_thread is not None:
            self._sampling_thread_pill.set()

            # Todo: Implement a timeout to return and log a Warning
            while (
                    self._sampling_thread is not None and self._sampling_thread.is_alive()
            ):
                time.sleep(0.1)

            self._sampling_thread = (
                None  # The thread eventually will finish thanks to the pill
            )
            log.info(f"Stopping sampling thread in Driver: {self.logical_id}")
            self._report_connected_state_from_sampling()
        else:
            log.info("Trying to stop the sampling_thread, but non thread was found.")
        self._observation_pulse_signal.clear()
        self._stop_current_pulse_signal.clear()
        self._sampling_window_finished.clear()

    def _report_connected_state_from_sampling(self):
        """
        If previous state is not SAMPLING state change will not be reported
        :return:
        """
        if self.driver_state == DriverState.SAMPLING:
            self._notify_new_driver_state_to_host(DriverState.CONNECTED)  # only go back to connected if it makes sense

    def _sampling_windows_loop(self, stop_pill: threading.Event):
        """The loop executed in the _sampling_thread.

        Here is where samples collection will occur, according to the sample
        cadence defined in the SamplingWindow of the Driver and the concrete
        implementation of the methods _start_sampling_collect() and _stop_sampling_collect().
        """
        requested_to_stop: bool = False
        signals = []
        sampling_task: SamplingTask = None

        while True:
            if requested_to_stop:
                break

            self._change_to_sampling_state()
            # No sampling task to collect.

            # Wait for the upper levels to authorize the next observation execution.
            while not self._observation_pulse_signal.is_set():
                time.sleep(0.05)  # TODO: this time should be configurable
                if self._sampling_window_finished.is_set():
                    requested_to_stop = True
                    break

                if not stop_pill.is_set():
                    continue

                else:
                    requested_to_stop = True
                    break

            else:
                self._observation_pulse_signal.clear()

                sampling_task: SamplingTask = self.pending_tasks_queue.get()

                log.info(f"Driver {self.logical_id} will perform a driver observation clock pulse")

                clock_pulse_time_finished = threading.Event()
                dead_time_timer = threading.Timer(
                    self.observation_pulse(),
                    lambda e: e.set(),
                    (clock_pulse_time_finished,),
                )
                dead_time_timer.start()

                # TODO: The driver start_sampling_collect should contemplate an interruption if somebody requested
                #   to stop. Concrete implementations can handle that.
                signals_in_pulse = self._start_sampling_collect()
                signals = signals + signals_in_pulse

                # Extra check to ensure that sampling time has finished.
                while not clock_pulse_time_finished.is_set():
                    if stop_pill.is_set() or self._sampling_window_finished.is_set():
                        requested_to_stop = True
                        log.warning(f"Driver {self.logical_id} requested to stop its sampling while in-middle "
                                    f"of sampling window.")
                        break

                self._stop_sampling_collect()

                log.info("{} Signals measured in last clock pulse: {}.".format(
                    self.logical_id, len(signals_in_pulse)))

                log.debug("{} driver finished a clock pulse at {} hours".format(
                    self.logical_id, datetime.datetime.now().time()))

                self._completed_clocks_notif_queue.put(
                    self.logical_id)  # Puts the logical id when a clock tick finishes.

        if not sampling_task:
            log.warning(f"Driver {self.logical_id} No collected sampling task from Sampling tasks queue."
                        f" No packages to send.")
        else:
            gateway_packs: List[GatewayPackage] = self._build_gateway_packages(signals, sampling_task)
            if len(gateway_packs) > 0:
                log.info("Driver collected {} signals and generated {} subpackages".format(
                    len(signals), len(gateway_packs)
                ))
                for pack in gateway_packs:
                    log.info(f"Package produced by driver {self.logical_id}: "
                             f"observation_timestamp: {pack.metadata.sampling_window.observation_timestamp} - "
                             f"sampling_window_index: {pack.metadata.sampling_window.sampling_window_index} -"
                             f"num_sampling_windows: {pack.metadata.sampling_window.number_of_sampling_windows}")
                    self._send_package_to_gateway(pack)
            else:
                log.info("{} driver collected 0 samplings in the sampling window. Will try to reconnect".format(
                    self.logical_id))
                self._process_no_signals_in_window_error()

        self._observation_pulse_signal.clear()
        self._stop_current_pulse_signal.clear()
        self._sampling_window_finished.clear()
        self._report_connected_state_from_sampling()

    def _change_to_sampling_state(self):
        if self.driver_state == DriverState.CONNECTED:
            self._notify_new_driver_state_to_host(DriverState.SAMPLING)

    def _process_no_signals_in_window_error(self):
        """This method implements the no signals case (driver is not sending any signals).
        """
        if self.driver_state != DriverState.CONNECTED and self.driver_state != DriverState.SAMPLING:
            log.warning("Driver is already disconnected cannot try to recover")
        else:
            self._notify_new_driver_state_to_host(DriverState.RECOVERING)

    def _notify_new_driver_state_to_host(self, driver_state):
        self.on_driver_state_changed(self.logical_id, driver_state)

    @staticmethod
    def _get_bytes_in_signal(signal):
        """ Calculates the size in bytes of a signal
            Args:
                signal: sampled signal
        """
        bytes_in_signal = 0
        if signal.is_scalar():
            bytes_in_signal = 4
        else:
            for sample in signal.samples:
                bytes_in_signal += len(sample) * sample.itemsize
        return bytes_in_signal

    def _save_package(self, gateway_packages, sampling_task, signals_to_pack, current_package_index,
                      package_id_prefix, previous_part_package_index):
        """ Saves package into gateway_packages list
            Args:
                gateway_packages: list containing all list of packages
                sampling_task: current task
                signals_to_pack: signals that will go into the package
                current_package_index: current index into list of packages,
                previous_part_package_index: previous index in the list of packages
        """
        gateway_packages.append(GatewayPackage(
            sampling_task.configuration_id,
            signals_to_pack.copy(),
            GatewayPackageMetadata(
                self.get_descriptor(), sampling_task.sampling_window,
                package_id_prefix + str(current_package_index),
                previous_part_package_index, sampling_task.tenant_id
            ),
        ))
        signals_to_pack.clear()

    @staticmethod
    def _join_signals_of_sampling_window(sampled_signals):
        """This function joins VECTOR signals of the same perception of a sampling window into a single big signal
            If the signal is not a VectorSignal type, it's samples are not joined together.

            Args:
                sampled_signals: all signals sampled in a sampling windows interval
        """
        nonvector_signals = [signal for signal in sampled_signals if SignalMode.is_time_only(signal.mode().value)]
        groups = {}
        for signal in sampled_signals:
            if SignalMode.is_time_only(signal.mode().value):
                continue
            if signal.perception_name() in groups:
                for i, dimension in enumerate(signal.samples):
                    groups[signal.perception_name()].samples[i] = np.concatenate(
                        (groups[signal.perception_name()].samples[i], dimension), axis=None)
            else:
                groups[signal.perception_name()] = signal
        return deque(list(groups.values()) + nonvector_signals)

    def _split_signal(self, signal, accumulated_bytes):
        """Splits a signal according to maximum size interval
            The length of a package should be withing the interval:
                [_max_size_packages[0], _max_size_packages[1]]

                since accumulated_bytes >= _max_size_packages[0] the signal should be split at size:
                    (_max_size_packages[1] - accumulated_bytes) / (signal.perception_dimensions[0] *
                                                                                            signal.samples.itemsize))
            Args:
                signal: Big signal whose size cannot fit into desired interval
                accumulated_bytes: already accumulated bytes into signals_to_pack
        """
        upper_bound = self._max_size_packages[1] - accumulated_bytes
        idx = int(upper_bound / (signal.perception_dimensions[0] * signal.samples[0].itemsize))
        rest = copy.deepcopy(signal)
        for i, dimension in enumerate(signal.samples):
            rest.samples[i] = np.copy(dimension[idx:])
            signal.samples[i] = dimension[:idx]
        return rest

    def _build_gateway_packages(self, sampled_signals, sampling_task: SamplingTask):
        """Build a set List of Gateway Packages based on the received sampled signals by the driver.
            The list of all signals will be distributed in a list of Gateway Packages. The desired behavior is:
                - Put all the possible information inside the Same Gateway Packages. Signals can be spread out
                    in different packages if required.
                - If a signal is spread out in different packages, those packages are referenced as a single linked list
                    and the package Timestamp will be shared for all those packages.
                - If all the signals in the packages are distributed without being shared in different packages,
                    then the packages don't need to be related among them.
            Args:
                sampled_signals: all signals sampled in a sampling windows interval
                sampling_task: sampling task of signals
        """
        sampled_signals = self._join_signals_of_sampling_window(sampled_signals)
        gateway_packs = []
        accumulated_bytes = 0
        signals_to_pack = []
        package_timestamp = 0
        current_package_index = 0
        gateway_package_index = -1

        while len(sampled_signals):
            signal = sampled_signals.popleft()
            sample_bytes = self._get_bytes_in_signal(signal)
            accumulated_bytes += sample_bytes
            if accumulated_bytes >= self._max_size_packages[0] or \
                    (accumulated_bytes <= self._max_size_packages[0] and current_package_index != 0):
                if accumulated_bytes <= self._max_size_packages[1]:
                    signals_to_pack.append(signal)
                    if current_package_index == 0:
                        package_timestamp = time.time_ns()
                    else:
                        gateway_packs[gateway_package_index].metadata.previous_part_index = current_package_index
                    package_id_prefix = f"{package_timestamp}_"
                    previous_part_package_index = 0 if current_package_index == 0 else current_package_index - 1
                    self._save_package(gateway_packs, sampling_task, signals_to_pack, current_package_index,
                                       package_id_prefix, previous_part_package_index)
                    current_package_index = 0
                else:
                    if current_package_index == 0:
                        package_timestamp = time.time_ns()
                        gateway_package_index = len(gateway_packs)
                        if len(signals_to_pack):
                            package_timestamp = time.time_ns()
                            package_id_prefix = f"{package_timestamp}_"
                            self._save_package(gateway_packs, sampling_task, signals_to_pack, 0, package_id_prefix, 0)
                            accumulated_bytes = 0
                            sampled_signals.appendleft(signal)
                            continue

                    accumulated_bytes -= sample_bytes
                    rest = self._split_signal(signal, accumulated_bytes)
                    signals_to_pack.append(signal)
                    package_id_prefix = f"{package_timestamp}_"

                    if not SignalMode.is_time_only(signal.mode().value) and \
                            settings.gateway.streaming_mode == "REALTIME":
                        assert current_package_index == 0
                        self._save_package(gateway_packs, sampling_task, signals_to_pack, current_package_index,
                                           package_id_prefix, 0)
                    else:
                        self._save_package(gateway_packs, sampling_task, signals_to_pack, current_package_index,
                                           package_id_prefix, current_package_index - 1)
                        current_package_index += 1
                        sampled_signals.appendleft(rest)
                accumulated_bytes = 0
            else:
                signals_to_pack.append(signal)

        if len(signals_to_pack) > 0:
            if current_package_index == 0:
                package_timestamp = time.time_ns()
            else:
                gateway_packs[gateway_package_index].metadata.previous_part_index = current_package_index
            package_id_prefix = f"{package_timestamp}_"
            previous_part_package_index = 0 if current_package_index == 0 else current_package_index - 1
            self._save_package(gateway_packs, sampling_task, signals_to_pack, current_package_index,
                               package_id_prefix, previous_part_package_index)

        return gateway_packs


# ==============================================================================
# Custom Exceptions for Driver class
# ==============================================================================


class EdgeParameterNotFoundError(Exception):
    """This exception should be thrown when a Driver does not found an expected
    value in the EdgeDescriptor.edge_parameters dictionary.
    """
    pass


class MalformedEdgeParameterError(Exception):
    """This exception should be thrown when a Driver finds a malformed value in the
    EdgeDescriptor.edge_parameters dictionary.
    """
    pass
