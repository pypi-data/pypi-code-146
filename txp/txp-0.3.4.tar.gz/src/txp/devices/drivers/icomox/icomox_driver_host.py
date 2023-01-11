"""
This module implements the driver host used to manage icomox POE devices through
a TCP/IP listener
"""
# ============================ imports =========================================
import multiprocessing
import queue
import threading
import time
from typing import Dict, List
from enum import Enum

from txp.devices.drivers.driver import DriverState, StateReport
from txp.devices.drivers.drivers_host import DriversHost
from txp.devices.drivers.icomox.icomox_datahandling import getHelloMessage, getIcomoxMessageType, IcomoxMessageType, \
    sendGetHelloMessageCommand, resetIcomox, sendSetConfigurationCommand
from txp.common.edge import EdgeDescriptor
from txp.devices.package_queue import PackageQueueProxy
from txp.devices.drivers.icomox.icomox_driver import IcomoxDriver
from txp.common.edge import DeviceId, MagnetometerSignal

from iCOMOXSDK.common.iCOMOX_list import sCOMOX_TCPIP
from iCOMOXSDK.communications.TCP_connectivity import class_iCOMOX_TcpServer

from txp.common.config import settings
from txp.common.utils.local_ip import get_local_ip
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class TcpState(Enum):
    cTCP_STATE_DISCONNECTED = 0
    cTCP_STATE_LISTEN = 1
    cTCP_STATE_CLIENT_DISCONNECTED = 2
    cTCP_STATE_CLIENT_CONNECTED = 3
    cTCP_STATE_iCOMOX_CONNECTED = 4
    cTCP_STATE_ZOMBIE_CLIENT_DETECTED = 5


# ==============================================================================
# IcomoxDriversHost
# ==============================================================================
class IcomoxDriversHost(DriversHost):
    """Concrete implementation of a DriversHost for Icomox edge_descriptors.

    This class is executed as a separated process, and it's responsible for:
        - Start TCP/IP listener.
        - Host and configure icomox drivers connected to the listener
    """
    port = 1201
    connected_devices: Dict[str, str] = {}
    drivers_packets_queues: Dict[str, queue.PriorityQueue] = {}
    icomox_driver_errored_timeout_seconds = 15

    def __init__(self, gateway_packages_queue: PackageQueueProxy, drivers_state_queue: multiprocessing.Queue, **kwargs):

        """
        Args:
            gateway_packages_queue: The Gateway package queue used to collect the GatewayPackages.
            drivers_state_queue: The Gateway queue used to collect the driver states.
            **kwargs: named parameters specific to this IcomoxDriversHost implementation.
        """
        local_ip_add = get_local_ip()
        log.info(f"Icomox Hosts set ip_server_address to: {local_ip_add}")
        self.ip_server_address = local_ip_add

        log.info("Init TCP/IP listener for Icomox POE devices")
        super(IcomoxDriversHost, self).__init__(gateway_packages_queue,drivers_state_queue, self.icomox_driver_errored_timeout_seconds,**kwargs)

        try:
            self._tcpIpCommunication: class_iCOMOX_TcpServer = class_iCOMOX_TcpServer(
                callback_process_message = self._on_process_messages,
                callback_state_changed = self._on_tcpip_state_changed
                )

        except Exception as ex:
            log.error("Icomox SDK error creating class_iCOMOX_TcpServer")

        self._drivers_map: Dict[str, IcomoxDriver] = {}

        """
            _drivers_power_off_reported: this attribute allows to control the
                sending of packages only once when the power_on predicate 
                is True. We want to report the first detection of RPM 0, and then
                report again when a RPM value > 0 is detected. 
        """
        self._drivers_power_off_reported: Dict[str, bool] = {}

    def connect(self):
        """Starts Icomox listener"""
        max_time_waiting_for_listener = 5

        self._tcpIpCommunication.start(self.ip_server_address, self.port)

        listener_time_finished = threading.Event()
        wait_for_server_timer = threading.Timer(
            max_time_waiting_for_listener,
            lambda e: e.set(),
            (listener_time_finished,),
        )

        wait_for_server_timer.start()

        while not self._tcpIpCommunication.is_listening() or listener_time_finished.isSet():
            time.sleep(0.5)

        if not self._tcpIpCommunication.is_listening():
            raise Exception("Error starting Icomox listener.")
        else:
            log.info("{} host is listening on address {} and port {}".format(self.get_driver_host_name(),self.ip_server_address,self.port))

    def disconnect(self):
        """Stops Icomox listener"""
        if self._tcpIpCommunication.is_listening():
            self._tcpIpCommunication.close()

    def discover_physical_ids(self) -> List[DeviceId]:
        """Returns the set of found DeviceId in the icomox network.

        Returns:
            List of device Ids
        """
        result = list()
        for value in self.connected_devices.values():
            if value != "":
                dev_id = DeviceId("", value)
                result.append(dev_id)
        return result

    def get_driver_host_name(self):
        return IcomoxDriver.device_name()

    def _add_drivers(self, edges: List[EdgeDescriptor]):
        """Adds the set of drivers for the specified edges in the host.

        Args:
            edges: List of EdgeDescriptor's for the drivers to be creted in
                the host instance.
        """
        #TODO: THIS CAN BE MOVED TO BASE CLASS. THE INSTANCE TYPE CAN BE CALCULLATED WITH NAME ATTRIBUTE OF THE HOST AND CREATOR CAN BE GOTTEN AS ATTRIBUTE AND ALL DRIVERS HANDLE SAME WAY
        for descriptor in edges:
            edge_queue = queue.PriorityQueue()
            self.drivers_packets_queues[descriptor.edge_parameters[IcomoxDriver._PHYSICAL_ID_PARAM_FIELD]] = edge_queue
            driver = IcomoxDriver(descriptor, self.gateway_package_queue, edge_queue, self._on_driver_state_changed,
                                  self._completed_driver_pulses_queue)
            self.drivers.append(driver)
            self._drivers_map[driver.logical_id] = driver
            self._drivers_power_off_reported[driver.logical_id] = False

    def take_fix_error_action(self, serial):
        for driver in self.drivers:
            if driver.logical_id == serial:
                resetIcomox(driver.get_complete_device_id().physical_id)

    def _on_process_messages(self, msg, iComox: sCOMOX_TCPIP =None):
        unique_id = self._get_unique_id_from_message(iComox, msg)
        self._add_message_to_queue(msg, unique_id)

    def _add_message_to_queue(self, msg, unique_id):
        # TODO: Check the correct timestamp
        timestamp = 1
        # Put the package in the driver priority queue, with the priority set to timestamp
        if self._sampling_started:
            if self.drivers_packets_queues.keys() is not None:
                if unique_id in self.drivers_packets_queues.keys():
                    self.drivers_packets_queues[unique_id].put((timestamp, msg))
                    log.debug("Package sent to driver")
                else:
                    log.warning('DEVICE NOT REGISTERED TO THIS GATEWAY {}'.format(unique_id))

    def _get_unique_id_from_message(self, iComox, msg):
        if iComox is None:
            raise Exception("on_process_messages(): iComox is None")
        unique_id = None
        if iComox.Hello is None:
            if getIcomoxMessageType(msg) == IcomoxMessageType.HELLO:
                iComox.Hello = msg
                hello_message = getHelloMessage(msg, iComox)
                # TODO: shall we add this parsed hello message to ICOMOX Driver Class as an attribute?
                if hello_message is not None:
                    unique_id = hello_message.getMcuSerialNumberString()
                    self._validate_icomox_physical_id_endpoints(unique_id)
                    self.connected_devices[iComox.remoteAddress] = unique_id
                    sendSetConfigurationCommand(unique_id,False) #making sure icomox will not send any data until it is requested to do it.
                    self._change_driver_state(unique_id, DriverState.CONNECTED)
            else:
                log.warning("ICOMOX device message is not Hello. Cant retrieve uniqueId")
                sendGetHelloMessageCommand(iComox)
        else:
            unique_id = iComox.UniqueIDString()
        return unique_id

    def _on_tcpip_state_changed(self, tcpState, iComox: sCOMOX_TCPIP = None):
        current_state = TcpState(tcpState)
        if current_state == TcpState.cTCP_STATE_CLIENT_CONNECTED:
            if iComox.remoteAddress not in self.connected_devices:
                self.connected_devices[iComox.remoteAddress] = "" #UniqueID not available yet
        elif current_state == TcpState.cTCP_STATE_CLIENT_DISCONNECTED:
            self._process_icomox_removal(iComox.remoteAddress)

    def _process_icomox_removal(self, address):
        if address in self.connected_devices:
            unique_id = self.connected_devices.pop(address)
            if unique_id != "":
                log.info("Icomox disconnected remote address {} and unique id {}".format(address, unique_id))
                self._change_driver_state(unique_id, DriverState.DISCONNECTED)
                self.clear_measured_enqueued_items(unique_id)

    def clear_measured_enqueued_items(self,physical_id):
        q = self.drivers_packets_queues[physical_id]
        try:
            while True:
                q.get_nowait()
                q.task_done()
        except queue.Empty:
            log.info("Queue for device {} physical ID has been cleared due to a disconnection".format(physical_id))
        except ValueError:
            log.info("Queue for device {} physical ID has been cleared due to a disconnection".format(physical_id))

    #TODO: we need to put down in base class of driver the physiical id artribute so we can generalize the behavior.
    def _change_driver_state(self, physical_id, driver_state):
        drivers = list(filter(lambda driver : driver.get_complete_device_id().physical_id == physical_id,self.drivers))
        if len(drivers) > 0:
            driver = drivers.pop()
            if driver_state  == DriverState.DISCONNECTED:
                driver.stop_sampling_windows()
            driver.update_driver_state(driver_state)
            self._add_drivers_state_to_queue(StateReport(driver.logical_id, driver_state))
        else:
            log.error("{} DEVICE IS NOT IN THE CURRENT  GATEWAY CONFIGURATION. ILLEGAL CONNECTION FROM SERIAL {}".format(self.get_driver_host_name(), physical_id))

    def _validate_icomox_physical_id_endpoints(self, unique_id):
        removable_address = None
        for ip,id in self.connected_devices.items():
            if id == unique_id:
                self._change_driver_state(unique_id,DriverState.DISCONNECTED)
                removable_address = ip
        if removable_address is not None:
            self._process_icomox_removal(removable_address)

    def _predicate_power_on(self, edge_logical_id: str) -> bool:
        log.info(f"{self.__class__.__name__} requested to validate"
                 f" POWER_ON for {edge_logical_id}")
        driver = self._drivers_map[edge_logical_id]
        if driver.driver_state == DriverState.CONNECTED:
            log.info(f"The driver: {edge_logical_id} is connected and it can validate POWER_ON")
            self._sampling_started = True
            signals = driver._start_sampling_collect()  # TODO: I'm sure this is illegal
            self._sampling_started = False

            magnetometer_signal = next(filter(
                lambda sig: sig.perception_name() == MagnetometerSignal.perception_name(),
                signals
            ))

            rpm = self.compute_rpm(magnetometer_signal.samples)
            log.info(f"RPM ON SIGNALS : {rpm}")

            # RPM detected
            if rpm > 0:
                self._drivers_power_off_reported[edge_logical_id] = False
                return True

            # If not speed is detected, then send the 0 value only once.
            if not self._drivers_power_off_reported[edge_logical_id]:
                log.info(f"Detected 0 RPM, but first occurrence will be reported...")
                self._drivers_power_off_reported[edge_logical_id] = True
                return True

        return False

    def compute_rpm(self, mag_axis_data):
        """
        TODO: Required information motor specific should be pulled down from persistence layer.
        """
        from iCOMOXSDK.sensors import BMM150

        rpm_axis = []
        BMM150_quantile_for_noise_floor_estimator = 0.25
        BMM150_minimum_SNR_for_speed_detection_dB = 20
        BMM150_ = BMM150.class_BMM150(
            quantile_for_noise_floor_estimator=BMM150_quantile_for_noise_floor_estimator,
            minimum_SNR_for_speed_detection_dB=BMM150_minimum_SNR_for_speed_detection_dB,
        )

        for axis in mag_axis_data:
            ASYNC_MOTOR_number_of_poles_pairs = 2
            ASYNC_MOTOR_slip_factor_percentages = 0.0
            network_frequency_Hz = BMM150_.maximum_of_PSD(axis)
            synchronous_frequency_Hz = (
                    network_frequency_Hz / ASYNC_MOTOR_number_of_poles_pairs
            )
            rotor_frequency_Hz = synchronous_frequency_Hz * (
                    1 - ASYNC_MOTOR_slip_factor_percentages / 100
            )
            rpm = rotor_frequency_Hz * 60
            rpm_axis.append(rpm)
        return rpm_axis[0]
