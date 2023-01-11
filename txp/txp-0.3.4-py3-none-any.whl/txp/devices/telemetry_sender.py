"""
This module implements the Telemetry Sender object.

The telemetry sender object is responsible for processing the
dispatch of Gateway Packages to the cloud.
"""

# ============================ imports =========================================
from txp.devices.package_queue import PackageQueueProxy
from txp.devices.package import GatewayPackage
from txp.common.configuration import GatewayConfig
from txp.devices.mqtt import GatewayMQTTClient, MQTTMessageType, MQTTSentPayloadContext
from txp.devices.tasks_scheduler import ScheduleTask, TasksScheduler
from typing import Callable, Dict, List, Set, Optional, Union
from txp.devices.exceptions import *
import datetime
import threading
import logging
import time
import base64
import queue
import enum
from txp.common.config import settings

log = logging.getLogger(__name__)

log.setLevel(settings.txp.general_log_level)


# ==============================================================================
# Telemetry Sender class
# ==============================================================================
class OverlappedDispatchError(Exception):
    """Raised when the TelemetrySender is requested to start a dispatch processing, and there's already
    one being executed."""

    pass


class NotDispatchProcessingStarted(Exception):
    """Raised when the TelemetrySender is requested to stop a dispatch processing, and there's already
    one being executed"""

    pass


# ==============================================================================
# _PackagesBuffer class.
# ==============================================================================
class _PackagesBuffer:
    """This class abstracts a buffer used in the telemetry sending logic.

    This buffer allows to store packages per device, and to ask/return packages
    per device.

    It also supports to free itself when the buffer is overflow.
    When this happens, the buffer will return all the packages that contains
    in a sequential interspersed way.

    The buffer will be overflowed at some point, but it'll accept new packages.
    The client class is responsible for detecting the overflow and apply the
    appropriate logic.
    """

    def __init__(
        self,
        max_num_packages: int,
        edges_serials: List[str],
    ):
        """Args:

        max_num_packages: The maximum number of packages before overflow.
        edges_serials: The list of serials of edge devices that will store packages
        """
        self._max_num_packages: int = max_num_packages
        self._curr_num_packages: int = 0
        self._device_packages_table: Dict[str, queue.Queue] = {}
        self._build_device_packages_table(edges_serials)

        self._active_holds_serials: Set[str] = set()
        """_active_holds_serials: a set to know in constant time which serials has packages in
        in the table"""

    def _build_device_packages_table(self, edges_serials: List[str]):
        self._device_packages_table.clear()
        for serial in edges_serials:
            log.debug(f"Serial registered in buffer table: {serial}")
            self._device_packages_table[serial] = queue.Queue()

    def has_package(self, serial: str) -> bool:
        """Return True if the buffer contains a package for the device serial."""
        if serial not in self._device_packages_table:
            raise RuntimeError(f"Edge Serial not found in buffer: {serial}")

        return self._device_packages_table[serial].empty()

    def get_package(self, serial: str) -> GatewayPackage:
        """Returns the most recent package for the given device serial.

        Raises:
            queue.Empty if there's no package to retrieve. Call the has_package()
            method to ensure a safe call.

        Returns:
            GatewayPackage object.
        """
        package = self._device_packages_table[serial].get(block=False)
        self._curr_num_packages = self._curr_num_packages - 1
        if self._device_packages_table[serial].empty():
            self._active_holds_serials.remove(package.metadata.edge_descriptor.logical_id)
        return package

    def overflow(self) -> bool:
        """Returns True if the Gateway reached its max capacity."""
        return self._curr_num_packages >= self._max_num_packages

    def has_packages(self) -> bool:
        """Returns True if the buffer holds 1 or more packages"""
        return bool(self._active_holds_serials)

    def has_valid_packages_from_serials(self, serials: Set[str]) -> bool:
        """Returns True if there is at least one package from one of the
        serials list in the buffer."""
        intersect = self._active_holds_serials.intersection(serials)
        return bool(intersect)

    def get_valid_package_from_serials(self, serials: Set[str]) -> GatewayPackage:
        serial = self._active_holds_serials.intersection(serials).pop()
        return self.get_package(serial)

    def insert_package(self, package: GatewayPackage) -> None:
        """Inserts a package in the Buffer.

        Raises:
            KeyError if the logical_id is not found in the internal table
            of the buffer. This case should never happen.

        Returns:
            None
        """
        logical_id = package.metadata.edge_descriptor.logical_id
        log.debug(f"Package inserted in buffer. Device Serial: {logical_id}")
        self._device_packages_table[logical_id].put(package)
        self._curr_num_packages = self._curr_num_packages + 1
        self._active_holds_serials.add(logical_id)

    def free_buffer(self) -> List[GatewayPackage]:
        """Returns all the packages hold by the buffer and leaves the overflow
        state.

        The packages will be returned in a list in a sequential interspersed way.

        Returns:
            List of GatewayPackage instances
        """
        packages = []
        while self._active_holds_serials:
            for serial in self._active_holds_serials.copy():
                packages.append(self.get_package(serial))

        return packages


# ==============================================================================
# Telemetry Rollover policies
# ==============================================================================
class TelemetryRolloverPolicy(enum.Enum):
    DISCARD = "discard"


# ==============================================================================
# Telemetry Sender class
# ==============================================================================
class TelemetrySender:
    """The TelemetrySender object is designed to deal with all the
    GatewayPackages dispatching activities.

    This object should:
        - Read GatewayPackages from the gateway packages queue.
        - Send the packages in a manner that provides a fair share of
            the connection.
        - Interpret input information that allows it to understand how
            to schedule telemetry sending operations.

    The TelemetrySender scheduling is specified in the configuration of the Job
    currently set in the Gateway. Currently the configuration of the TelemetrySender
    requires:
        - start_date: A date to start the Telemetry Sender.
        - duration: The duration of the telemetry dispatch task.
        - frequency: The frequency to repeat the dispatch.
    """

    def __init__(
            self,
            gateway_packages_queue: PackageQueueProxy,
            gateway_mqtt_client: GatewayMQTTClient,
            gateway_process_stats_callback: Callable,
            telemetry_task_config: Optional[Dict],
            gateway_config: GatewayConfig,
            edge_serials: List[str]
    ):
        """
        Args:
            gateway_packages_queue: The Gateway centralized and shared packages
                Queue.
            gateway_mqtt_client: The GatewayMQTTClient instance used by the Gateway.
            gateway_process_stats_callback: A callback provided by the Gateway to process
                sent packages stats.
            telemetry_task_config: The telemetry task configuration described in the class
                docstring. It can be None at set later with instance methods.
            gateway_process_stats_callback: A callback provided by the Gateway to process
                sent packages stats.
            edge_serials: A list with the edge devices serials monitored by the gateway.
        """
        self._rollover_policy = self._parse_rollover_policy(gateway_config.job.telemetry_rollover_policy)
        log.info(f"Telemetry Sender set rollover policy to: {self._rollover_policy}")

        self._packages_queue: PackageQueueProxy = gateway_packages_queue
        self._mqtt_client: GatewayMQTTClient = gateway_mqtt_client
        self._process_stats: Callable = gateway_process_stats_callback

        self._send_events_thread: threading.Thread = None
        self._send_events_stop: threading.Event = threading.Event()

        # Fair dispatch attributes
        self._serials_weights_table: Dict[str, int] = {}
        """_serials_weights_table: a table of the allowed number of packages per fair segment
        for edge."""
        self._build_serials_weights_table(gateway_config, edge_serials)

        self._sent_packages_table: Dict[str, int] = {}
        """_sent_packages_table: a table to be used when sending packages in fair segments, to hold
        the count of sent packages per serial."""
        self._restart_sent_packages_table()

        self._valid_serials_to_send: Set[str] = set()
        """_valid_serials_to_send: a set of serials that are valid when building a fair segment."""

        # TODO: the max number for the buffer is the number of edges. This should be refined.
        self._buffer: _PackagesBuffer = _PackagesBuffer(len(edge_serials), edge_serials)

        self._unsent_packages_registry: queue.Queue[Union[bytes, str, MQTTSentPayloadContext]] = queue.Queue()

        """_unsent_packages_registry: internal table to hold the unsent packages. This table allows 
        to retry sending unacknowledged messages based on the rollover policies."""
        self._unsent_packages_check_interval: int = settings.gateway.telemetry.unsent_packages_check_interval

        self._TOTAL_PKGS_SENT = 0

    # ============================== Private Methods ================================================
    @staticmethod
    def _parse_rollover_policy(value: str) -> TelemetryRolloverPolicy:
        try:
            policy = TelemetryRolloverPolicy(value)
            return policy
        except:
            log.error("Unknown excpetion while parsing Telemetry Rollover Policy. Set to default Discard.")
            return TelemetryRolloverPolicy.DISCARD

    def _build_serials_weights_table(
            self, gateway_config: GatewayConfig, edge_serials: List[str]
    ):
        """Builds the weights table for the packages.

        Note: Right now, treat all packages as equals, with the same weight of 1.
        TODO: Implement weights compute.

        Args:
            gateway_config: The Gateway Configuration instance.
        """
        for serial in edge_serials:
            self._serials_weights_table[serial] = 1

    def _restart_sent_packages_table(self):
        serials = self._serials_weights_table.keys()
        for serial in serials:
            self._sent_packages_table[serial] = 0

    def _max_packages_reached_per_weight(self):
        serials = self._serials_weights_table.keys()
        return all(
            list(
                map(
                    lambda serial: self._sent_packages_table[serial]
                                   == self._serials_weights_table[serial],
                    serials,
                )
            )
        )

    def _initialize_new_segment(self):
        """Initializes attributes to track the building of a new fair segment"""
        self._restart_sent_packages_table()
        self._valid_serials_to_send = set(self._sent_packages_table.keys())

    def _is_valid(self, package: GatewayPackage):
        """Returns True if sending a package with the serial is fair."""
        serial = package.metadata.edge_descriptor.logical_id
        return (
                self._sent_packages_table.setdefault(serial, 0)
                < self._serials_weights_table[serial]
        )

    def _send_event(self, package: GatewayPackage) -> None:
        """Sends the Package to the cloud."""
        edge_serial = package.metadata.edge_descriptor.logical_id
        telemetry_topic = settings.gateway.mqtt.telemetry_topic_batch_template.format(
            edge_serial
        )

        if settings.gateway.streaming_mode == "REALTIME":
            telemetry_topic = settings.gateway.mqtt.telemetry_topic_realtime_template.format(
                edge_serial
            )

        proto = package.get_proto()
        encoded_payload = base64.b64encode(proto.SerializeToString())
        sent = False
        try:
            if len(encoded_payload) > 250000:
                log.warning(
                    f"Package exceeds max valid size. Will not Publish. Package Size: {len(encoded_payload)}"
                )

            else:
                self._mqtt_client.publish_message(
                    MQTTMessageType.TELEMETRY_MESSAGE,
                    edge_serial,
                    telemetry_topic,
                    encoded_payload,
                    attach=True,
                    track_acknowledge=True,
                    try_reconnect=False
                )
                sent = True
                log.info(f"Sent Package from edge: {edge_serial}")
                self._TOTAL_PKGS_SENT += 1
                log.info(f"TOTAL PACKAGES SENT: {self._TOTAL_PKGS_SENT}")

        except MqttMessageNotPublished:
            log.error(f"Error with disconnected MQTT client while publishing "
                      f"telemetry event.")
            self._unsent_packages_registry.put(
                MQTTSentPayloadContext(
                    edge_serial, telemetry_topic, encoded_payload, True
                )
            )

        except:
            log.error(f"Unknownn exception while publishing telemetry event. ")
            self._unsent_packages_registry.put(
                MQTTSentPayloadContext(
                    edge_serial, telemetry_topic, encoded_payload, True
                )
            )

        finally:
            self._process_stats(package, sent)

    def _check_unsent_events(self) -> List:
        """Checks if there are unsent messages in the physical layer, and clears the
        sent messages from the physical layer."""
        log.debug("Checking if there are unsent events...")
        unsent_messages = self._mqtt_client.get_unacknowledged_messages(MQTTMessageType.TELEMETRY_MESSAGE)
        if unsent_messages:
            log.info(f"Received {len(unsent_messages)} unsent messages to sent in rollover")
            for payload_context in unsent_messages:
                self._unsent_packages_registry.put(payload_context)

        self._mqtt_client.clear_acknowledged_messages(MQTTMessageType.TELEMETRY_MESSAGE)
        log.debug(f"Telemetry current number of unsent packages: {self._unsent_packages_registry.qsize()}")

    def _register_package_sent(self, package: GatewayPackage):
        """Register the sent package in the _sent_packages_table"""
        serial = package.metadata.edge_descriptor.logical_id
        self._sent_packages_table[serial] += 1
        if self._sent_packages_table[serial] == self._serials_weights_table[serial]:
            self._valid_serials_to_send.remove(serial)

    def _send_packages(self, timeout: int) -> None:
        """Private method for sending packages following an algorithm that tries to send
        fair sequences of packages.

        This is the callback to be called by the Tasks in the TaskScheduler, to send
        telemetry.

        Fair sequences are determined by the computed table of weights for the devices.

        This function will loop until the passed callback returns True. This enables to reuse
        accordingly from different places.

        Note: There's a limit of 60.000 messages per minute established by IoT Core.
            https://cloud.google.com/iot/quotas#rate_limits. This code will not surpass that limit.

        Args:
            timeout: the timeout for the sending process to finish.
        """
        total_sent_packages = 0
        sent_messages_limit_count = 0
        limit_per_minute = 60000  # Default 60000 messages per minute
        start_time = datetime.datetime.now()
        elapsed_time = start_time
        unsent_packages_check = start_time
        messages_limit_check = start_time

        log.info(f'Starting scheduled Telemetry sending task at: {start_time}')

        self._initialize_new_segment()

        if self._buffer.has_packages():
            log.warning("Lag: packages found in Buffer from previous run.")

        try:
            while True:
                # Check if Telemetry time is over
                if (elapsed_time - start_time).total_seconds() > timeout:
                    break

                elapsed_time = datetime.datetime.now()

                # Check if a minute has passed to refresh messages limit count
                if (elapsed_time - messages_limit_check).total_seconds() > 60:
                    sent_messages_limit_count = 0
                    messages_limit_check = datetime.datetime.now()

                # If not, then check if messages limit has been surpassed
                elif sent_messages_limit_count == limit_per_minute:
                    wait_time = (
                            (messages_limit_check + datetime.timedelta(minutes=1)) - messages_limit_check
                    ).total_seconds()
                    log.info(f"Published messages limit of 60.000 p/minute reached. Wait for {wait_time} secs")
                    time.sleep(wait_time)

                # Check for unacknowledged packages
                if ((elapsed_time - unsent_packages_check).total_seconds()
                        > self._unsent_packages_check_interval):
                    unsent_packages_check = datetime.datetime.now()
                    self._check_unsent_events()
                    log.debug(f"Telemetry current number of unsent packages: "
                              f"{self._unsent_packages_registry.qsize()}")

                # Check if somebody requested stop.
                if self._send_events_stop.is_set():
                    log.info(f"Dispatch packages completed. Packages sent: {total_sent_packages}")
                    log.info(f'Scheduled Dispatch task finished.')
                    self._discard_policy()
                    return

                # Here starts the sending algorithm
                if self._buffer.has_packages():
                    log.debug("Buffer has packages. Trying to get valid package")
                    if self._buffer.has_valid_packages_from_serials(
                        self._valid_serials_to_send
                    ):
                        log.debug("Buffer has a valid package. Sending package.")
                        package = self._buffer.get_valid_package_from_serials(
                            self._valid_serials_to_send
                        )
                        self._send_event(package)
                        self._register_package_sent(package)
                        total_sent_packages = total_sent_packages + 1  # this might count a fake positive
                        sent_messages_limit_count += 1
                        continue
                    else:
                        log.debug("Buffer has not valid package. Trying to get from Queue.")

                if self._packages_queue.size() == 0:
                    packages = self._buffer.free_buffer()
                    if packages:
                        log.info("No packages received in Queue. Sending the buffered packages anyways.")
                    for package in packages:
                        self._send_event(package)
                        total_sent_packages = total_sent_packages + 1  # this might count a fake positive
                        sent_messages_limit_count += 1
                    self._initialize_new_segment()
                    continue

                try:
                    package = self._packages_queue.get_package()
                except Exception as e:
                    log.error(f"Exception while getting package from Gateway Queue: {e}. ")
                    package = None

                    if isinstance(e, ValueError):
                        log.error(f"Detected {e}. Restart Gateway program")
                        quit(1)

                # Tries to send unacknowledge messages
                if self._unsent_packages_registry.qsize():
                    message_payload = self._unsent_packages_registry.get()
                    log.info("Retry to publish unsent telemetry message")
                    self._retry_sent_payload(message_payload)

                if package is None:
                    log.debug(
                        f"None package received in Queue."
                    )
                    time.sleep(1)
                    continue

                log.debug(
                    f"Package received in Queue from: {package.metadata.edge_descriptor.logical_id}"
                )
                if self._is_valid(package):
                    log.debug("The Package is valid. Sending package.")
                    self._send_event(package)
                    self._register_package_sent(package)
                    total_sent_packages = total_sent_packages + 1  # this might count a fake positive
                    sent_messages_limit_count += 1
                else:
                    log.debug(
                        "The package can not be sent in the current fair segment. Saving package in buffer."
                    )
                    self._buffer.insert_package(package)

                if self._buffer.overflow():
                    log.debug("Buffer has overflow. Sending packages in buffer.")
                    log.info("Buffer has overflow. Sending packages in buffer.")
                    packages = self._buffer.free_buffer()
                    for package in packages:
                        self._send_event(package)
                        total_sent_packages = total_sent_packages + 1  # this might count a fake positive
                        sent_messages_limit_count += 1
                    self._initialize_new_segment()
                    continue

                if self._max_packages_reached_per_weight():
                    log.debug("Fair segment sent. Next iteration will start to build a new fair segment.")
                    self._initialize_new_segment()

            # Check for pending packages
            log.info(f"Dispatch packages completed assigned time. "
                     f"Approximated packages sent: {total_sent_packages}")

            self._check_unsent_events()
            if (
                self._unsent_packages_registry.qsize() > 0 or
                self._packages_queue.size() > 0
            ):
                log.info("There are packages without sending after Telemetry configured time."
                         f"Unsent packages: {self._unsent_packages_registry.qsize()}. "
                         f"Packages in Queue: {self._packages_queue.size()}")
                self._apply_rollover_policy()

        except Exception as e:
            # The _send_packages call will return and the new telemetry task will be scheduled.
            log.error(f'Unexpected exception while sending packages: {e}')

    def _retry_sent_payload(self, payload_context: MQTTSentPayloadContext):
        try:
            self._mqtt_client.publish_message(
                MQTTMessageType.TELEMETRY_MESSAGE,
                payload_context.device_id,
                payload_context.topic,
                payload_context.payload,
                attach=True,
                track_acknowledge=True,
                try_reconnect=False
            )
            sent = True
            log.info(f"Sent Package from edge: {payload_context.device_id}")

        except MqttMessageNotPublished:
            log.error(f"Error with disconnected MQTT client while publishing "
                      f"telemetry event.")
            self._unsent_packages_registry.put(
                MQTTSentPayloadContext(
                    payload_context.device_id, payload_context.topic, payload_context.payload, True
                )
            )

        except:
            log.error(f"Unknownn exception while publishing telemetry event. ")
            self._unsent_packages_registry.put(
                MQTTSentPayloadContext(
                    payload_context.device_id, payload_context.topic, payload_context.payload, True
                )
            )

    def _apply_rollover_policy(self):
        """
        TODO: implement the other policies for Telemetry rollover:
            - next_x_windows: This policy allows to send pending telemetry packages in
                the next X observation times.
        """
        if self._rollover_policy == TelemetryRolloverPolicy.DISCARD:
            self._discard_policy()

    def _discard_policy(self):
        log.info("Telemetry rollover policy 'Discard' will be executed")
        self._unsent_packages_registry = queue.Queue()
        self._packages_queue.clear()
        self._buffer.free_buffer()
        self._initialize_new_segment()  # resets buffer internal tables

    def _get_scheduled_task(self, telemetry_task_config: Dict) -> ScheduleTask:
        """Get a List of scheduled tasks to configure in the TasksScheduler.

        TODO: The task scheduled for telemetry dispatch should be computed based on the Job
            sampling window. This is just filling the required data fields.

        Args:
            telemetry_task_config: A dictionary with the telemetry configuration for the concept of "Job".
        """
        task_end_timeout = telemetry_task_config['duration'] * 60

        start_time = datetime.datetime.strptime(telemetry_task_config['start_time'],
                                                settings.time.time_format)

        week_days_list = list(map(lambda char: int(char), telemetry_task_config['active_week_days']))

        # TODO:Telemetry sending end date should be computed based on the Job end date.
        #   Support this when supporting the full JOB configuration.
        required_fixed_end_date = datetime.datetime.strptime(
            settings.gateway.tasks_scheduler.max_date_string,
            settings.time.datetime_format
        )

        task = ScheduleTask(
            datetime.datetime.now().date(), required_fixed_end_date.date(),
            start_time.time(), start_time.time(),
            week_days_list, self._send_packages, (task_end_timeout,)
        )
        return task

    # ============================== Public Methods ================================================
    def start(self, gateway_conf: GatewayConfig, devices: List[str], timeout: int):
        self._serials_weights_table.clear()
        self._build_serials_weights_table(gateway_conf, devices)
        self._sent_packages_table.clear()
        self._restart_sent_packages_table()
        self._valid_serials_to_send.clear()
        self._buffer = _PackagesBuffer(len(devices), devices)
        self._send_events_thread = threading.Thread(
            target=self._send_packages,
            name="telemetry-sending",
            args=(timeout,)
        )
        self._send_events_thread.start()
        self._send_events_stop.clear()

    def stop(self):
        self._send_events_stop.set()
        while self._send_events_thread.is_alive():
            time.sleep(1)

    def is_running(self) -> bool:
        """Returns True if the TelemetrySender is running some tasks scheduling
        in background"""
        return self._send_events_thread is not None and self._send_events_thread.is_alive()
