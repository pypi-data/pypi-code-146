"""
This module implements the Device Manager functionality.
The main functionality of the Device Manager is to centralize the
lifecycle of DriversHost processes and to provide collaboration
with higher components like Gateway and user interaction components.
"""


# ============================ imports =========================================
import multiprocessing
import time
from typing import List, Dict, Tuple, Optional

from txp.common.edge import EdgeDescriptor
from txp.devices.drivers.drivers_host import DriversHost
from txp.devices.drivers.icomox.icomox_driver_host import IcomoxDriversHost
from txp.devices.drivers.mock.mock_driver import MockDriversHost
from txp.devices.drivers.voyager.voyager_driver_host import VoyagerDriversHost
from txp.devices.drivers.usb.usb_driver_host import UsbDriversHost
from txp.devices.drivers.generic_driver_host import GenericDriversHost
from txp.devices.drivers.arm_robot.robot_host import RobotDriversHost, ThermalArmHost
from txp.devices.package_queue import PackageQueueProxy
from txp.devices.drivers.device_type import DeviceType
from multiprocessing import managers
from txp.common.config import settings
import itertools
import logging
from txp.devices.sampling_task import SamplingTask
import gc

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class _HostsProcessManager(managers.BaseManager):
    """Internal class used as custom multiprocessing.Manager to create server processes
    for the DriversHost's instances."""

    _host_registered: bool = False

    @classmethod
    def register_hosts_classes(cls):
        """Registers the types and callables for the different DriversHost implementations
        in this multiprocessing Manager class.
        """
        if not cls._host_registered:
            log.debug("Registering DriversHosts in the HostProcessManager")
            cls.register("VoyagerDriversHost", VoyagerDriversHost)
            cls.register("IcomoxDriversHost",IcomoxDriversHost)
            cls.register("MockDriversHost", MockDriversHost)
            cls.register("UsbDriversHost", UsbDriversHost)
            cls.register("GenericDriversHost", GenericDriversHost)
            cls.register("RobotDriversHost", RobotDriversHost)
            cls.register("ThermalArmHost", ThermalArmHost)
            cls._host_registered = True


# ==============================================================================
# DeviceManager class to be used at initialization time.
# ==============================================================================
class DevicesManager:
    """This class is the top-level manager used to manage the lifecycle of the
    DriversHost processes for the devices connected to the Gateway.

    This DeviceManager provides collaboration methods that are used by higher level
    components such as:
        - Gateway component
        - User interaction component for pairing logic
    """

    def __init__(self):
        _HostsProcessManager.register_hosts_classes()

        self._hosts_processes: List[_HostsProcessManager] = []
        """_hosts_processes: A List of the used _HostsProcessManagers created to 
        serve the DriversHosts."""
        self.hosts: List[DriversHost] = []
        """hosts: the set of DriversHost references created by this device manager."""
        self.drivers_status_queue = multiprocessing.Manager().Queue()

        self._driver_to_host: Dict[str, DriversHost] = {}
        """_driver_to_host: internal map to known in which host reference lives a Driver."""

        self._virtual_devices_table: Dict[str, bool] = {}
        """_virtual_devices_table: this dict is used internally to know which logical id
            is virtual or not."""

        self._drivers_clock_values: Dict[str, int] = {}
        """_devices_clock_values: this dict is used internally to know which is the value
        of a driver instance clock.
        """

    def create_host(
        self,
        host_device: str,
        gateway_package_queue: PackageQueueProxy,
        host_kwargs: Dict = {},
    ):
        """Create the instance for the specified DriversHosts.

        This allows client components to decide which devices hosts needs to be created
        based on their own business logic.

        Args:
            host_device: name of the device equals to a Driver.device_name() implementation.
            gateway_package_queue: The Gateway central package Queue to be distributed
                to all the DriersHosts.
            host_kwargs: Dict of specific parameters for the DriversHost device implementation.

        Returns:
            None
        """
        process_manager = _HostsProcessManager()
        process_manager.start()
        process_manager.connect()
        host = DeviceType(host_device).build_host_process(process_manager, gateway_package_queue, self.drivers_status_queue, **host_kwargs)
        self.hosts.append(host)
        self._hosts_processes.append(process_manager)

    def initialize_drivers(self, edges: List[EdgeDescriptor]):
        """
        This funtion initializes all edges configured.
        """
        for host in self.hosts:
            edges_filtered = list(filter(lambda edge: self._get_drivers_by_host(host.get_driver_host_name(), edge), edges))
            host.add_drivers(edges_filtered)
            self._driver_to_host.update({
                edge.logical_id: host for edge in edges_filtered
            })
            self._virtual_devices_table.update({
                edge.logical_id: self.is_virtual_driver(edge.logical_id)
                for edge in edges_filtered
            })
            self._drivers_clock_values.update({
                edge.logical_id: host.get_driver_observation_pulse(edge.logical_id)
                for edge in edges_filtered
            })

    def start(self):
        """
        Starts all registered edges related connection handlers. DriverHost associated registered instances.

        """
        try:
            for host in self.hosts:
                host.connect()
        except Exception as ex:
            log.error("Error starting gateway host: {}".format(host.get_driver_host_name()))
            raise

    def stop(self):
        """
        Stops all registered edges related connection handlers. DriverHost associated registered instances.

        """
        for host in self.hosts:
            host.disconnect()

    def clear_devices(self):
        """Clear the DriversHost from the device manager.

        The hosts will be stopped first. After that, the manager processes
        are explicitly "shutdown". Finally, the references are cleared
        from the DeviceManager, in order to be garbage collected.
        """
        if self.hosts:
            log.info("Stopping DeviceManager hosts")
            self.stop()

            log.info("Clearing DeviceManager hosts")
            self.hosts = []

            for manager in self._hosts_processes:
                manager.shutdown()

            self._hosts_processes = []
            self._driver_to_host.clear()
            self._virtual_devices_table.clear()
            self._drivers_clock_values.clear()

            gc.collect()

        else:
            log.info("DevicesManager does not have hosts to clear.")

    def get_state_changed_queued_items(self):
        """
        gets that contains serial and state of the edge that changed its state.
        :return: a list of StateReports. Empty list if no queue state changed
        """
        edges_states_reports = []
        while self.drivers_status_queue.qsize():
            state_report = self.drivers_status_queue.get(False)
            edges_states_reports.append(state_report)
            log.debug(edges_states_reports)

        return edges_states_reports

    def receive_sampling_tasks(self, tasks: Dict[str, SamplingTask]):
        for host in self.hosts:
            host.receive_sampling_tasks(tasks)

    def receive_sampling_tasks_list(self, tasks: List[Tuple]) -> None:
        """Receive the sampling tasks lists and send those tasks to the drivers."""
        tasks_with_host = []
        for logical_id, task in tasks:
            tasks_with_host.append((logical_id, task, self._driver_to_host[logical_id]))

        for host, entries in itertools.groupby(tasks_with_host, lambda entry: entry[2]):
            log.debug(f"Host {host.get_driver_host_name()} will receive the tasks: {entries}")
            tasks_for_host = list(map(
                lambda entry: (entry[0], entry[1]),
                entries
            ))
            host.receive_sampling_tasks_list(tasks_for_host)

    def notify_sampling_window_completed(self, logical_ids: Optional[List[str]] = None):
        """Notifies to the drivers that the current sampling window was completed.

        Args:
            logical_ids: An optional list of drivers to enable. If not provided,
                then all drivers in the device manager will be enabled.
        """
        for logical_id in logical_ids:
            if logical_id not in self._driver_to_host:
                log.error("Devices Manager requested to notify sampling window completion"
                          f"the device: {logical_id}, but the device was not found")
            else:
                self._driver_to_host[logical_id].notify_sampling_window_completed(logical_id)

    def start_sampling_windows(
        self, logical_ids: Optional[List[str]] = None,
        task_predicates: List[str] = []
    ):
        """Starts the drivers internal sampling windows loop.

        Args:
            logical_ids: An optional list of drivers to enable. If not provided,
                then all drivers in the device manager will be enabled.
            task_predicates: List of task predicates names to validate in order to start
                the task.
        """
        if not logical_ids:
            for host in self.hosts:
                host.start_sampling_windows()
        else:
            edges_to_enable = []
            edges_to_disable = []
            for logical_id in logical_ids:
                if logical_id not in self._driver_to_host:
                    log.error("Devices Manager requested to enable a windows loop for "
                              f"the device: {logical_id}, but the device was not found")
                else:
                    if self.validate_predicates(logical_id, task_predicates):
                        log.info(f"All Predicates were True for {logical_id}. "
                                 f"Start sampling window for edge.")
                        edges_to_enable.append(logical_id)
                    else:
                        log.warning(f"Some value predicates forbids edge "
                                    f"{logical_id} from starting up a new sampling window.")
                        edges_to_disable.append(logical_id)
            for edge in edges_to_enable:
                self._driver_to_host[edge].start_sampling_windows(edge)

            for edge in edges_to_disable:
                self._driver_to_host[edge].clear_pending_task_queue(edge)

    def stop_sampling_windows(self, logical_ids: Optional[List[str]] = None):
        """Stops the drivers intenral sampling windows loop.

        Args:
            logical_ids: An optional list of drivers to disable. If not provided,
                then all drivers in the device manager will be call to disable.
        """
        if not logical_ids:
            for host in self.hosts:
                host.stop_sampling_windows()
        else:
            for logical_id in logical_ids:
                if logical_id not in self._driver_to_host:
                    log.error("Devices Manager requested to disable a windows loop for "
                              f"the device: {logical_id}, but the device was not found")
                else:
                    self._driver_to_host[logical_id].stop_sampling_windows()

    def reset(self,host_device):
        """
        Intended to reset an edge type.

        :param host_device: Driver.get_name attribute to reset this type of edge

        """
        for host in self.hosts:
            if host_device == host.get_driver_host_name():
                host.disconnect()
                time.sleep(5)
                host.connect()

    def _get_drivers_by_host(self, driver_name: str, edge: EdgeDescriptor):
        edge_descriptor = edge
        if driver_name == edge_descriptor.device_kind:
            return True
        else:
            return False

    def get_drivers_observation_pulse(self, logical_ids: List[str]) -> List:
        """Returns the observation pulses of the corresponding drivers."""
        ret = []
        for logical_id in logical_ids:
            if logical_id not in self._driver_to_host:
                log.error("Devices Manager requested to obtain pulse from a "
                          "Host that has not been created")
                continue

            pulse = self._driver_to_host[logical_id].get_driver_observation_pulse(logical_id)
            ret.append((logical_id, pulse))
        return ret

    def get_driver_observation_pulse(self, logical_id: str) -> int:
        """Returns the observation pulses of the driver."""
        if logical_id not in self._drivers_clock_values:
            log.error("Devices Manager requested to obtain clock value from a "
                      f"unknown driver {logical_id}")
            return 0

        return self._drivers_clock_values[logical_id]

    def enable_drivers_clock_pulse(self, logical_ids: List[str]) -> None:
        """Enables the distributed drivers to execute an observation pulse."""
        for logical_id in logical_ids:
            if logical_id not in self._driver_to_host:
                log.error("Devices Manager requested to obtain pulse from a "
                          "Host that has not been created")
                continue

            self._driver_to_host[logical_id].enable_driver_clock_pulse(logical_id)

    def disable_drivers_clock_pulse(self, logical_ids: List[str]) -> None:
        """Disables the drivers current clock pulse sample collect"""
        for logical_id in logical_ids:
            if logical_id not in self._driver_to_host:
                log.error("Devices Manager requested to obtain pulse from a "
                          "Host that has not been created")
                continue

            self._driver_to_host[logical_id].disable_current_pulse(logical_id)

    def get_drivers_completed_clock(self, logical_ids: List[str]) -> Dict[str, int]:
        d = {}
        for logical_id in logical_ids:
            if logical_id not in self._driver_to_host:
                log.error("Devices Manager requested to obtain completed clocks from a "
                          "Host that has not been created")
            else:
                p = self._driver_to_host[logical_id].get_driver_completed_pulses(logical_id)
                log.debug(f"Host reported {p} completed clock pulses for {logical_id}")
                d[logical_id] = p

        return d

    def clear_drivers_completed_clocks(self, logical_ids: List[str]) -> None:
        """Clear the drivers completed pulses registered in the drivers hosts.
        """
        for logical_id in logical_ids:
            if logical_id not in self._driver_to_host:
                log.error("Devices Manager requested to clear completed clocks register from a "
                          "Host that has not been created")
            else:
                self._driver_to_host[logical_id].clear_driver_registered_packages(logical_id)
                log.debug(f"Clearing completed registered packages for driver {logical_id}")

    def is_virtual_driver(self, logical_id: str) -> bool:
        if logical_id not in self._driver_to_host:
            log.error("Devices Manager requested to obtain virtual type from a "
                      "Host that has not been created")
            return False
        return self._driver_to_host[logical_id].is_virtual_driver(logical_id)

    def is_actuator_device(self, logical_id: str) -> bool:
        """Returns true if the logical_id provided belongs to an
        actuator device type.

        The only supported expected actuator device is a logical id
        for a Robotic arm.
        """
        if logical_id not in self._driver_to_host:
            log.error(f"Devices Manager was requested to check driver actuator type "
                      f"from driver {logical_id}, but the Driver was not found")
            return False
        return self._driver_to_host[logical_id].is_actuator_device(logical_id)

    def get_drivers_completed_clock(self, logical_ids: List[str]) -> Dict[str, int]:
        d = {}
        for logical_id in logical_ids:
            if logical_id not in self._driver_to_host:
                log.error("Devices Manager requested to obtain completed clocks from a "
                          "Host that has not been created")
            else:
                p = self._driver_to_host[logical_id].get_driver_completed_pulses(logical_id)
                log.debug(f"Host reported {p} completed clock pulses for {logical_id}")
                d[logical_id] = p

        return d

    def validate_predicates(self, logical_id, predicates: List[str]) -> bool:
        """Given the predicates of a SamplingTask configuration, it will validate those
        by requesting the operation to the appropriated DriversHost.

        Returns:
            True if the predicates are valid for the Sampling Task. False otherwise.
        """
        # We validate each predicate for the edge
        valid = []
        for p in predicates:
            logging.info(f"Validating Predicate {p} for device {logical_id}")
            valid.append(self._driver_to_host[logical_id].validate_predicate(logical_id, p))

        return all(valid)
