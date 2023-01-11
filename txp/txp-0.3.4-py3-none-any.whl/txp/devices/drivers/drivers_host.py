"""
This module contains the support for the DriversHost conceptualization.
"""

# ============================ imports ==========================================
import multiprocessing
import threading
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional, Callable
from txp.devices.drivers.driver import DriverState, Driver, StateReport
from txp.common.edge import EdgeDescriptor
from txp.devices.drivers.icomox.icomox_driver import IcomoxDriver
from txp.devices.sampling_task import SamplingTask
from txp.devices.package_queue import PackageQueueProxy
from txp.common.edge import DeviceId
import queue
from collections import defaultdict

from txp.common.config import settings
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


# ==============================================================================
# DriversHost class
# ==============================================================================
class DriversHost(ABC):
    """A Drivers Host is a concept that represents a set of remote instances
    of Drivers.

    The 'Remote' word implies that the Drivers within the DriversHost are running
    on its own separated process, with the main responsibility of collecting samples
    from devices.

    The DriversHost can also encapsulate other required instances like managers
    or controllers that interact with the physical devices associated with the
    hosted edge_descriptors.
    """

    _PREDICATE_POWER_ON_KEY = 'power_on'

    def __init__(self, gateway_packages_queue: PackageQueueProxy, drivers_state_queue: multiprocessing.Queue, error_timer_interval_seconds, **kwargs):
        """
        Args:
            gateway_packages_queue: The Gateway package queue used to collect the GatewayPackages.
            drivers_state_queue: The Gateway queue used to collect the driver states.
            **kwargs: named parameters specific for each DriversHost implementation.
        """
        self.gateway_package_queue: PackageQueueProxy = gateway_packages_queue
        self.drivers: List[Driver] = []
        self._drivers_index: Dict[str, Driver] = {}
        self.drivers_state_queue = drivers_state_queue
        """edge_descriptors: internal list of hosted edge_descriptors."""
        self.drivers_revering_from_error: List[str] = []
        self.error_timer_interval_seconds = error_timer_interval_seconds
        self._sampling_started = False
        log.debug(f"DrivesHost {self.get_driver_host_name()} running in pid: {multiprocessing.current_process().pid}")

        self._completed_driver_pulses_queue: threading.queue = queue.Queue()
        """_completed_driver_pulses_queue: internal queue for the host to receive the report 
        of completed clock pulses by the drivers in an sampling window. 
        Note: Currently the reports are the edges logical ids."""

        self._completed_clocks_notif_queue: Dict[str, int] = {}

        # Initializes predicates
        self._predicates_map: Dict[str, Callable] = {
            self._PREDICATE_POWER_ON_KEY: self._predicate_power_on,
        }

    @abstractmethod
    def connect(self):
        """This method will connect the DriversHost with the physical device that
        is connected to the Gateway hardware unit.
        """
        pass

    @abstractmethod
    def disconnect(self):
        """This method will disconnect the DriversHost from the physical device that
        is connected to the Gateway hardware unit.
        """
        pass

    @abstractmethod
    def _add_drivers(self, edges: List[EdgeDescriptor]):
        """Method to be defined by the child classes in order to instantiate the drivers
        with logic-specific code."""
        pass

    def add_drivers(self, edges: List[EdgeDescriptor]):
        """Adds the set of drivers to the host for the specified edge descriptors,
        and creates the necessary internal tables.

        Args:
            edges: List of EdgeDescriptor for the edges.
        """
        self._add_drivers(edges)
        for driver in self.drivers:
            self._drivers_index.update({
                driver.logical_id: driver
            })
            self._completed_clocks_notif_queue[driver.logical_id] = 0

    @abstractmethod
    def discover_physical_ids(self) -> List[DeviceId]:
        """Discovers physical IDs connected available in the system for the Host
        type of device.

        Returns:
            A list of the discovered DeviceId in the physical layer.
        """
        pass

    @abstractmethod
    def get_driver_host_name(self):
        pass

    @abstractmethod
    def take_fix_error_action(self, serial):
        pass

    def _driver_errored_timeout_timer(self,serial):
        driver = list(filter(lambda driver: driver.logical_id == serial, self.drivers)).pop()
        state = driver.get_state()
        if state == DriverState.RECOVERING:
            driver.update_driver_state(DriverState.ERRORED)
            self._add_drivers_state_to_queue(StateReport(serial,DriverState.ERRORED))
        elif state == DriverState.CONNECTED:
            driver.start_sampling_windows()
            log.info("driver was able to be recovered to managed state {} by host serial {} resuming pending tasks".format(state, serial))
        self.drivers_revering_from_error.remove(serial)

    #TODO: try change signature and pass driver instance as a method variable so full control on driver on the error processing. instead of indexing
    def _on_driver_state_changed(self, serial, driver_state):
        if driver_state == DriverState.RECOVERING:
            if self.get_driver_host_name() == IcomoxDriver.device_name():
                self._process_recovery_driver_state(serial)
            else:
                log.warning("{} device does not support {}. it didnt get any signals during a Sampling Window".format(serial,driver_state))
        else:
            log.warning("{} device state has changed new state is {}".format(serial,driver_state))
            driver = list(filter(lambda driver: driver.logical_id == serial, self.drivers)).pop()
            driver.update_driver_state(driver_state)
            self._add_drivers_state_to_queue(StateReport(serial, driver_state))

    def _process_recovery_driver_state(self, serial):
        log.warning("driver on state error started for {}".format(serial))
        driver = list(filter(lambda driver: driver.logical_id == serial, self.drivers)).pop()
        # driver.stop_sampling_windows()
        driver.update_driver_state(DriverState.RECOVERING)
        self._add_drivers_state_to_queue(StateReport(serial, DriverState.RECOVERING))
        self.drivers_revering_from_error.append(serial)
        self.take_fix_error_action(serial)
        timer = threading.Timer(self.error_timer_interval_seconds, self._driver_errored_timeout_timer, args=(serial,))
        timer.start()

    def _add_drivers_state_to_queue(self, state_report: StateReport):
        self.drivers_state_queue.put(state_report)

    def receive_sampling_tasks(self, tasks: Dict[str, SamplingTask]):
        """Receives a list of sampling tasks to be executed by the
        drivers in this hosts.

        Args:
            tasks: Dictionary with the drivers serial as key and the
            corresponding sampling tasks as value.
        """
        for driver in self.drivers:
            if driver.driver_state == DriverState.CONNECTED or driver.driver_state == DriverState.SAMPLING:
                if driver.logical_id in tasks:
                    task = tasks[driver.logical_id]
                    log.info("Sending task to {}".format(
                        driver.logical_id,
                        task.sampling_window.observation_time,
                        task.sampling_window.sampling_time)
                    )
                    driver.receive_sampling_task(task)
            else:
                log.warning("Driver Serial {} is not ready to receive tasks state is {}".format(driver.logical_id, driver.driver_state))

    def receive_sampling_tasks_list(self, tasks: List[Tuple]):
        """Receive a list of sampling tasks to be executed by the drivers on this host."""
        for logical_id, sampling_task in tasks:
            if logical_id in self._drivers_index:
                driver = self._drivers_index[logical_id]
                if driver.driver_state == DriverState.CONNECTED or driver.driver_state == DriverState.SAMPLING:
                    log.info("Sending task to {}, with observation {}s and sampling {}s".format(
                        driver.logical_id,
                        sampling_task.sampling_window.observation_time,
                        sampling_task.sampling_window.sampling_time)
                    )
                    driver.receive_sampling_task(sampling_task)
                else:
                    log.warning("Driver Serial {} is not ready to receive tasks state is {}".format(driver.logical_id,
                                                                                                    driver.driver_state))
            else:
                log.error(f"Unexpected task received in host {self.get_driver_host_name()} for driver {logical_id}. "
                          f"The Driver doesn't belong to this host.")

    def connect_driver(self, edge_serial: str):
        """Connects the driver with the specified serial"""
        driver: Driver = next(
            (driver for driver in self.drivers if driver.logical_id == edge_serial), None
        )
        if driver is None:
            log.warning(
                f"Trying to connect driver {edge_serial}, but the driver was not found in the host."
            )
            return

        driver.disconnect_device()

    def connect_drivers(self):
        """Connects all the edge_descriptors found in the hosts."""
        for driver in self.drivers:
            driver.connect_device()

    def disconnect_driver(self, edge_serial: str):
        """Disconnect the driver with the specified serial"""
        driver: Driver = next(
            (driver for driver in self.drivers if driver.logical_id == edge_serial), None
        )
        if driver is None:
            log.warning(
                f"Trying to disconnect driver {edge_serial}, but the driver was not found in the host."
            )
            return

    def disconnect_drivers(self):
        """Disconnects all the edge_descriptors found in the hosts."""
        for driver in self.drivers:
            driver.disconnect_device()

    def get_drivers_state(self) -> List[DriverState]:
        """Returns the states for the edge_descriptors of this hosts.

        Returns:
            The List of driver states.
        """
        states = [driver.get_state() for driver in self.drivers]
        return states

    def get_drivers_descriptors(self) -> List[EdgeDescriptor]:
        """Returns the description of the hosted edge_descriptors."""
        descriptors = [driver.get_descriptor() for driver in self.drivers]
        return descriptors

    def clear_pending_task_queue(self, logical_id: str):
        log.info(f"Clearing pending SamplingTask Queue for edge {logical_id}")
        self._drivers_index[logical_id].clear_pending_task_queue()

    def start_sampling_windows(self, logical_id: Optional[str] = None):
        """Starts the sampling windows for the hosted drivers.

        Args:
            logical_id: optional unique logical_id. If provided, only that
                driver will be enabled.
        """
        self._sampling_started = True  # At least one driver is sampling.

        if not logical_id:
            for driver in self.drivers:
                if driver.driver_state == DriverState.CONNECTED:
                    driver.start_sampling_windows()
        else:
            self._drivers_index[logical_id].start_sampling_windows()

    def stop_sampling_windows(self):
        """Starts the sampling windows for the hosted drivers"""
        self._sampling_started = False
        for driver in self.drivers:
            driver.stop_sampling_windows()

    def get_driver_observation_pulse(self, logical_id: str) -> int:
        """Returns the observation pulse of the driver."""
        if logical_id not in self._drivers_index:
            log.error(f"Host {self.get_driver_host_name()} was requested to obtain "
                      f"pulse from driver {logical_id}, but the Driver was not found")
            return 0
        pulse = self._drivers_index[logical_id].observation_pulse()
        return pulse

    def notify_sampling_window_completed(self, logical_id: str) -> None:
        """Notifies to the driver that the sampling window was completed"""
        if logical_id not in self._drivers_index:
            log.error(f"Host {self.get_driver_host_name()} was requested to notify sampling window completion "
                      f"to driver {logical_id}, but the Driver was not found")
        else:
            self._drivers_index[logical_id].notify_sampling_window_completed()

    def enable_driver_clock_pulse(self, logical_id: str) -> None:
        """Enables the drivers internal next clock pulse in order to authorize a synchronized
        and controlled driver observation."""
        if logical_id not in self._drivers_index:
            log.error(f"Host {self.get_driver_host_name()} was requested to enable "
                      f"pulse from driver {logical_id}, but the Driver was not found")
        elif self._drivers_index[logical_id].driver_state == DriverState.SAMPLING:
            self._drivers_index[logical_id].enable_observation_pulse()
        else:
            log.warning(f"Trying to enable driver clock pulse, but the driver state is "
                        f"not SAMPLING")

    def disable_current_pulse(self, logical_id: str) -> None:
        """Enable the signal to stop the current sampling collect."""
        if logical_id not in self._drivers_index:
            log.error(f"Host {self.get_driver_host_name()} was requested to stop "
                      f"pulse from driver {logical_id}, but the Driver was not found")
        elif self._drivers_index[logical_id].driver_state == DriverState.SAMPLING:
            self._drivers_index[logical_id].disable_current_pulse()
        else:
            log.warning(f"Trying to disable driver clock pulse, but the driver state is "
                        f"not SAMPLING")

    def is_virtual_driver(self, logical_id: str) -> bool:
        """Returns true if the driver with logical id is virtual."""
        if logical_id not in self._drivers_index:
            log.error(f"Host {self.get_driver_host_name()} was requested to check driver type "
                      f"from driver {logical_id}, but the Driver was not found")
            return False
        return self._drivers_index[logical_id].is_virtual()

    def is_actuator_device(self, logical_id: str) -> bool:
        """Returns true if the logical_id belongs to an actuator device.

        Note: The only Actuator device currently supported is the general
        descriptor for a Robot Driver."""
        return False

    def get_driver_completed_pulses(self, logical_id: str) -> int:
        """Returns the last packages report for the provided logical_id.
        """

        # Update the internal count first
        if self._completed_driver_pulses_queue.qsize():
            log.info(f"Drivers Host {self.get_driver_host_name()} has reports to process.")
            while self._completed_driver_pulses_queue.qsize():
                edge_logical_id = self._completed_driver_pulses_queue.get()
                self._completed_clocks_notif_queue[edge_logical_id] += 1
                log.info(f"Registering new package count for {edge_logical_id}:"
                         f" {self._completed_clocks_notif_queue[edge_logical_id]}")

        packages_count = self._completed_clocks_notif_queue[logical_id]
        return packages_count

    def clear_driver_registered_packages(self, logical_id: str):
        self._completed_clocks_notif_queue[logical_id] = 0

    #######################################################
    # Predicates implementation
    #######################################################
    """
        Below theres the implementation of the predicate evaluation for the 
        drivers hosts. 
        
        The recommended approach is to return True when a Host
        do not implement the predicate. 
    """
    def validate_predicate(self, logical_id: str, predicate: str) -> bool:
        if predicate not in self._predicates_map:
            log.warning(f"Could not find predicate: {predicate} for edge {logical_id} validation."
                        f"Returns False as fallback strategy")
            return False

        return self._predicates_map[predicate](logical_id)

    @abstractmethod
    def _predicate_power_on(self, edge_logical_id: str) -> bool:
        """Implementation for a predicate that allows to know if the asset/machine
        being monitored by the edge is ON or OFF. """
        pass
