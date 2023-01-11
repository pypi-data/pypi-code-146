"""
This module defines the Gateway class and other related class
which support the Gateway conceptualization and functionality.
"""
# ============================ imports =========================================
from txp.common.config import settings
from txp.common.utils.json_complex_encoder import ComplexEncoder
from txp.devices.drivers.arm_robot.arm_controller import ArmControllerError
from txp.devices.job_task_manager import JobTasksManager
from txp.devices.drivers.driver import StateReport, DriverState
from txp.devices.package import GatewayPackage
from txp.devices.package_queue import PackageQueueProxy, PackageQueue
from txp.devices.sampling_task import SamplingTask
from txp.devices.gateway_states_machine_mixin import GatewayStatesMachineMixin
from txp.common.edge import EdgeDescriptor, MachineMetadata, PairedEdgesPayload
from txp.devices.mqtt import GatewayMQTTClient, MQTTMessageType
from txp.devices.telemetry_sender import TelemetrySender
from txp.devices.ux.ux_client import UxClient
import txp.devices.ux.ux_states_protocol as ux_states
from txp.devices.devices_manager import DevicesManager
from collections import defaultdict
from deepdiff import DeepDiff
from txp.devices.production_manager import ProductionManager
from txp.common.configuration import JobConfig
from txp.common.configuration import GatewayConfig
from typing import List, Dict, Optional
from threading import Thread, Event
from queue import SimpleQueue
from multiprocessing import managers
from txp.devices.gateway_states_enums import *
from txp.common.utils.local_ip import get_local_ip
from txp.devices.exceptions import *
from txp.devices.state_payload import GatewayStatePayload
import time
import json
import datetime
import logging
import requests
import sys

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


# ==============================================================================
# Definition of the custom GatewayManager to handle server processes.
# ==============================================================================
class _GatewayManager(managers.BaseManager):
    pass


# ==============================================================================
# Definition of the custom Gateway class
# ==============================================================================
class Gateway(GatewayStatesMachineMixin):
    """This Gateway is the defined Gateway concept in the Tranxpert architecture.

    The Gateway takes care on instantiation of all the configured drivers, by interacting
    with the DriversHosts.

    The Gateway contains a PackageQueue which is shared to all the Driver instances.
    Each driver will drop packages on that queue, and the gateway defines its own
    strategy to consume those packages and send it to the cloud.

    The Gateway instance is designed to exists as soon as the main program process starts,
    and it contains an internal state machine which ensure that the system transitions
    from state to state, collecting all the information required by the gateway to operate.

    """

    def __init__(self):
        """
        Initializes the Gateway states machine.

        This init process annotates attributes of the Gateway object that are expected to be assigned
        when the state machine transitions through the execution flow.
        """
        super(Gateway, self).__init__()

        # Gateway package Queue.
        _GatewayManager.register("PackageQueue", PackageQueue, PackageQueueProxy)
        self._server_process_manager = _GatewayManager()
        self._server_process_manager.start()
        self.package_queue: PackageQueueProxy = (
            self._server_process_manager.PackageQueue()
        )

        self._ux_client: UxClient = UxClient()

        self._ux_client.start_streamlit_app()

        self._mqtt_client: GatewayMQTTClient = None
        """_mqtt_client: The internal MQTT client for the Gateway to use."""

        self._job_manager: JobTasksManager = None

        self._device_manager: DevicesManager = DevicesManager()
        """_device_manager: The DeviceManager is the communication mean between the Gateway and the 
        physical devices connected to it."""

        self._devices_state_table: Dict[str, StateReport] = {}
        """_devices_state_table: a dictionary with the most recent received state for an edge device
        in the DeviceManager"""

        self._production_manager: ProductionManager = None
        """_production_manager: The production manager takes charge of devices pairing in production phase"""

        self._machine_to_edges_table: Dict[str, List[str]] = {}
        """_machines_to_edges_table: a lookup table to get which edges ids are associated to a machine"""

        self._edge_to_machine_id_table: Dict[str, List[str]] = defaultdict(list)
        """_edge_to_machine_id_table: a table to lookup the asset/machine monitored by the edge with 
        logical ID. The value is a list because a virtual edge actuator can be associated with multiple edges."""

        self._machines_table_by_id: Dict[str, MachineMetadata] = {}

        self._edge_logical_id_to_edge_descriptor: Dict[str, EdgeDescriptor] = {}

        self._new_configuration_received_flag: bool = False
        """_new_configuration_received_flag: flag to track when a new configuration was received and some components 
        needs to update accordingly"""

        self._plain_received_configuration: Dict = {}
        """_plain_received_configuration: The Dictionary received by the cloud in the most recent configuration"""

        self._ping_received: bool = False
        """_ping_received: flag to indicate when a configuration was send without changes. This is interpreted
        as a PING request to the Gateway, who then will send the State to the cloud."""

        self._edges_state_diff: bool = False
        """_edges_state_diff: When this flag is True, the Gateway will publish a State report as consequence."""

        # MQTT attributes
        self._mqtt_gateway_commands_topic: str = ""
        self._mqtt_gateway_config_topic: str = ""
        self._mqtt_gateway_errors_topic: str = ""

        # Temporary job_task_finished queue to know when to transition from sampling to ready
        self._job_task_finished_queue: SimpleQueue = None

    def start(self):
        """This method start the Gateway states machine, and delegates the
        execution of the program to the Gateway.

        This method will compute which is the appropriate state to begin in,
        whether this being a new production phase for a new instance, or an
        existent instance that is already configured.

        """

        self._load_global_state()

        if self.global_state.state == GatewayStates.Startup:
            self.begin_startup()

        elif self.global_state.state == GatewayStates.Ready:
            log.info("The Gateway found a previous Global State. "
                     "Trying to pull a new cloud configuration before preparing devices.")
            self._mqtt_client: GatewayMQTTClient = GatewayMQTTClient(self, self._mqtt_on_message_callback)
            self._initialize_mqtt_attributes()

            start_wait = datetime.datetime.now()
            while not self._new_configuration_received_flag and not self._ping_received:
                self._check_connection()
                time.sleep(1)
                if (datetime.datetime.now() - start_wait).total_seconds() > 10:
                    log.warning(f"No configuration received from cloud. Using the previous configuration saved.")
                    break

            if self._new_configuration_received_flag:
                log.info(f"The Gateway received a new configuration update "
                         f"to version: {self.global_state.last_configuration_id}")
            else:
                log.info(f"Configuration has not changed. Using version: {self.global_state.last_configuration_id}")

            self._configuration_reception_completed()

        else:
            raise RuntimeError("Invalid state when calling Gateway start.")

    def stop(self, *args, **kwargs) -> None:
        """Stop method used as callback to the SIGTERM/SIGINT interruptions."""
        log.info("Gateway process was requested to stop. Executing graceful termination...")
        self.package_queue.close()
        exit(0)

    # =========================== Startup State Methods =============================
    def _step_into_startup(self) -> None:
        """Callback to call after begin_startup transition trigger

        This callback will execute itself until the introduced values are valid
        and the Gateway can move to the next state.

        """

        # The Gateway started a production phase. Create the marker file.
        self._create_initialized_marker_file()

        valid_startup_values: bool = False
        retry: bool = False
        deserialization_error: bool = False

        while not valid_startup_values:
            self.status = StartupStatus.RequestRequiredValues
            log.info(self._state_log_msg())

            # Sends new message to UX. If there was an error with previously
            # introduced values, then those Details are sent.
            self._send_startup_ux_message(retry, deserialization_error)

            ux_state_rec: ux_states.UxStartupState = self._ux_client.wait_for_ux_state()

            if not isinstance(ux_state_rec, ux_states.UxStartupState):
                raise RuntimeError(
                    f"Unexpected UxState received in Gateway: {ux_state_rec.state}"
                )

            try:
                valid_startup_values = GatewayMQTTClient.validate_connection_values(
                    ux_state_rec.project_id,
                    self.gateway_config.cloud_region,
                    ux_state_rec.registry_id,
                    ux_state_rec.gateway_id,
                )
            except ValueError as key_deserialization_error:
                log.error(f"ERROR: {key_deserialization_error}")
                deserialization_error = True
            if not valid_startup_values:
                retry = True

        self.gateway_config.gateway_id = ux_state_rec.gateway_id
        self.gateway_config.registry_id = ux_state_rec.registry_id
        self.gateway_config.project_id = ux_state_rec.project_id
        log.info("Gateway: Startup Files Validated")
        self._startup_completed()

    def _send_startup_ux_message(self, retry: bool, deserialization_error: bool):
        """Send a Startup message to the UI application.

        If it's a retry, that means there was some problem with
        the received values.
        """
        if deserialization_error:
            details = ux_states.UxDetails(
                ux_states.UxDetails.Kind.Error,
                settings.ux.startup.invalid_private_key_cert,
            )
        elif retry:
            details = ux_states.UxDetails(
                ux_states.UxDetails.Kind.Warning,
                settings.ux.startup.invalid_values_warning,
            )
        else:
            details = None

        ux_state_sent = ux_states.UxStartupState(
            self.state,
            self.status,
            details,
            self.gateway_config.gateway_id,
            self.gateway_config.registry_id,
            False,
            False,
            False,
            False,
            self.gateway_config.project_id
        )
        self._ux_client.send_state_to_ui(ux_state_sent)

    # ======================== Configuration Reception State Methods ======================
    def _step_into_configuration_reception(self):
        """Callback to be invoked after the _startup_completed_callback trigger.

        This callback will proceed to listen for cloud configurations for the
        Gateway and the devices bound to the Gateway. Specifically, in order:
            - Gateway configuration
            - Machines Metadata configuration
            - Edges configuration
        """
        self.status = ConfigurationReceptionStatus.EstablishCloudConnection
        log.info(self._state_log_msg())

        # Send current state to the UI process
        ux_state_sent = ux_states.UxConfigurationReceptionState(
            self.state,
            self.status,
            None,
            self.gateway_config,
            self.machines_configurations,
            self.edges_configurations,
            False,
        )
        self._ux_client.send_state_to_ui(ux_state_sent)

        self._mqtt_client: GatewayMQTTClient = GatewayMQTTClient(self, self._mqtt_on_message_callback)
        self._initialize_mqtt_attributes()

        self._mqtt_client.subscribe_to_topic(
            self.gateway_config.gateway_id, self._mqtt_gateway_config_topic, False
        )

        self._mqtt_client.subscribe_to_topic(
            self.gateway_config.gateway_id, self._mqtt_gateway_errors_topic, False
        )

        start_wait = datetime.datetime.now()
        while not self._new_configuration_received_flag:
            log.info(f"Waiting for configuration to download in state {self.global_state.state}")

            try:
                self._mqtt_client.enable_incoming_messages_processing(1)
                time.sleep(1)
            except (MqttNetworkingUnavailableError, MqttConnectTimeoutError):
                log.error("Error detected in MQTT Connection while waiting configuration reception.")

            if (datetime.datetime.now() - start_wait).total_seconds() > 10:
                log.error(f"Timeout exceeded while waiting from configuration in state {self.global_state.state}")
                self._production_phase_not_completed()

        while not self.global_state.last_configuration_id != "0":
            log.info(f"Waiting for configuration to process in state {self.global_state.state}")
            time.sleep(1)
            if (datetime.datetime.now() - start_wait).total_seconds() > 10:
                log.error(f"Timeout exceeded while processing received configuration in state {self.global_state.state}")
                self._production_phase_not_completed()

        log.info(f"Configuration successfully processed in state {self.global_state.state}")

        self._configuration_reception_completed()

    # ======================== Configuration Validation State Methods =====================
    def _step_into_configuration_validation(self):
        self.status = ConfigurationValidationStatus.CheckConfigurations
        self._new_configuration_received_flag = False
        ux_state_sent = ux_states.UxConfigurationValidationState(
            self.state,
            self.status,
            None,
            self.gateway_config,
            self.machines_configurations,
            self.edges_configurations,
        )

        # Initialize different in-memory data
        self._build_internal_tables()

        self._ux_client.send_state_to_ui(ux_state_sent)

        num_paired_devices = self._get_number_of_paired_devices()
        log.info(f"Number of paired devices received in configuration: {num_paired_devices}")

        if num_paired_devices != 0 and num_paired_devices != len(self.edges_configurations):
            log.warning("Received non-zero and non-complete set of paired devices.")
            log.error("Partial devices pairing is not supported yet. Moving to error.")
            self._production_phase_not_completed()

        if num_paired_devices == 0:
            log.warning("Received 0 paired devices. Device pairing required. Gateway will move to device pairing")
            self._configuration_validation_completed()  # trigger to device pairing state

        if num_paired_devices == len(self.edges_configurations):
            log.info("All received devices in configuration are paired. Moving to Ready.")
            self._device_pairing_completed()  # Move to device preparing

    # ======================== Devices Pairing State Methods ==============================
    def _step_into_devices_pairing(self):
        """Callback to call when the UX is pairing devices."""

        # We need to check mqtt connection in order to keep alive
        stop_check: Event = Event()
        check_mqtt_conn_thread: Thread = Thread(
            name="check_mqtt_connect_prod",
            daemon=True,
            target=self._check_mqtt_conn_prod,
            args=(stop_check,)
        )
        check_mqtt_conn_thread.start()

        self._save_global_state()
        self._create_production_manager()
        self.status = DevicePairingStatus.SelectDeviceToPair
        ux_state_sent = self._get_ux_device_pairing_initial_state()
        self._ux_client.send_state_to_ui(ux_state_sent)

        # devices pairing information exchange loop with user interface interactions
        while True:
            ux_state = self._ux_client.wait_for_ux_state()

            if isinstance(ux_state, ux_states.UxDevicePairingState):
                device_to_pair_id = ux_state.props['device_to_pair']
                edge_descriptor_for_edge = self._edge_logical_id_to_edge_descriptor[
                    device_to_pair_id
                ]

                if not edge_descriptor_for_edge.is_actuator_device():
                    self._pair_non_virtual_device(
                        ux_state, edge_descriptor_for_edge
                    )
                else:
                    self._pair_virtual_device(
                        ux_state, edge_descriptor_for_edge
                    )

                if self._get_number_of_paired_devices() == len(self.edges_configurations):
                    log.info("All devices were successfully paired."
                             "Leaving the Devices Pairing state")
                    break

            else:
                log.error("Unexpected Error in Gateway. Unknown UX State received.")
                raise RuntimeError("Unexpected Error in Gateway. Unknown UX State received.")

        stop_check.set()
        self._production_manager = None
        self._publish_paired_devices_to_cloud()

        # Wait until the cloud updated the configuration after pairing
        while not self._ping_received:
            log.info("Waiting for cloud configuration acknowledge of paired devices")
            try:
                self._mqtt_client.enable_incoming_messages_processing(2)
            except (MqttNetworkingUnavailableError, MqttConnectTimeoutError):
                log.error("Error detected with MQTT client connection while waiting for "
                          "devices pairing acknowledge from cloud.")
                # TODO: This should put the Gateway in a Irrecoverable state in the States Machine.

        log.info("Received cloud acknowledge of new paired configuration")

        self._device_pairing_completed()

    def _check_mqtt_conn_prod(self, stop: Event):
        while not stop.is_set():
            self._check_connection()

        log.info("Closed check mqtt connection in production")

    def _get_ux_device_pairing_initial_state(self):
        """Returns the initial ux_state for the DevicesPairing state."""
        edges_to_pair = []
        for machine_metadata in self.machines_configurations:
            edges_to_pair.extend(machine_metadata.edges_ids)
        expected_devices = set(edges_to_pair)
        props = {
            "paired_devices": set(),
            "expected_devices": expected_devices,
            "device_to_pair": None,
            "virtual_edge_asset": None
        }
        return ux_states.UxDevicePairingState(
            self.state, self.status, None, self.gateway_config, self.machines_configurations,
            self.edges_configurations, props
        )

    def _pair_non_virtual_device(self, ux_state, edge_descriptor: EdgeDescriptor):
        """This method interacts with the ProductionManager when the device to pair is not virtual"""
        log.info(f"Pairing Device with logical ID: {edge_descriptor.logical_id}")
        ux_state_sent = ux_state.copy()

        ux_state_sent.status = DevicePairingStatus.PairingSelectedDevice  # Update UX to inform the user
        self._ux_client.send_state_to_ui(ux_state_sent)

        self._production_manager.start_listening_for_an_edge(edge_descriptor.device_kind)
        device_wait_result = self._production_manager.wait_for_device_to_connect(
            edge_descriptor.device_kind, 3
        )  # TODO it says minutes. It's really minutes or seconds?

        self._production_manager.stop_listening_for_devices(edge_descriptor.device_kind)

        if device_wait_result:
            device = self._production_manager.get_hosted_device()
            log.info(f"Production Manager obtained device: {device}")

            ux_state_sent.status = DevicePairingStatus.RequestConfirm  # Update UX to request confirmation from user
            self._ux_client.send_state_to_ui(ux_state_sent)

            ux_state = self._ux_client.wait_for_ux_state()  # Wait for user confirmation

            if ux_state.status == DevicePairingStatus.PairingConfirmed:
                log.info("Pairing was confirmed")
                ux_state_sent = ux_state.copy()
                ux_state_sent.status = DevicePairingStatus.SelectDeviceToPair
                ux_state_sent.props['paired_devices'] = (
                    ux_state_sent.props['paired_devices'].union({edge_descriptor.logical_id})
                )
                self._ux_client.send_state_to_ui(ux_state_sent)

                # Update internal configuration with discovered physical ID
                edge_descriptor.set_physical_id(device[1].physical_id)

                log.info(
                    f"Physical ID {device[1].physical_id} added in local configuration "
                    f"for edge: {edge_descriptor.logical_id}"
                )

            elif ux_state.status == DevicePairingStatus.PairingCancelled:
                log.info("Pairing was cancelled")
                ux_state_sent = ux_state.copy()
                ux_state_sent.status = DevicePairingStatus.SelectDeviceToPair  # If cancelled, restart state to select
                self._ux_client.send_state_to_ui(ux_state_sent)

            else:
                log.error("Unexpected Error in Gateway. Unknown UX State received.")
                raise RuntimeError("Unexpected Error in Gateway. Unknown UX State received.")

        else:
            log.error("Error while waiting for device pairing")
            ux_state_sent = ux_state.copy()
            ux_state_sent.status = DevicePairingStatus.PairingError
            self._ux_client.send_state_to_ui(ux_state_sent)

    def _pair_virtual_device(self, ux_state, edge_descriptor: EdgeDescriptor):
        log.info(f"Pairing Virtual Edge arm with logical ID: {edge_descriptor.logical_id}")
        ux_state_sent = ux_state.copy()

        self._production_manager.prepare_virtual_production(edge_descriptor)

        while True:
            next_status_step: DevicePairingStatus = self._production_manager.get_next_virtual_production_step()
            ux_state_sent.props['virtual_production'] = self._production_manager.get_virtual_production_record()
            ux_state_sent.status = next_status_step
            log.info(f"Sent status: {next_status_step} to virtual production UI")
            self._ux_client.send_state_to_ui(ux_state_sent)  # Update UX to request confirmation from user

            ux_state = self._ux_client.wait_for_ux_state()  # Wait for user interaction

            if ux_state.status == DevicePairingStatus.VirtualCameraConnectionConfirmed:
                log.info("User confirmed virtual camera connection. Trying to detect device")
                camera_connected_status = self._production_manager.detect_virtual_camera()
                ux_state_sent = ux_state.copy()
                ux_state_sent.status = camera_connected_status
                self._ux_client.send_state_to_ui(ux_state_sent)
                time.sleep(5)
                continue

            if ux_state.status == DevicePairingStatus.VirtualThermocameraConnectionConfirmed:
                log.info("User confirmed virtual thermo camera connection. Trying to detect device")
                thermocamera_connected_status = self._production_manager.detect_virtual_thermocamera()
                ux_state_sent = ux_state.copy()
                ux_state_sent.status = thermocamera_connected_status
                self._ux_client.send_state_to_ui(ux_state_sent)
                time.sleep(15)  # Sleeps for the user to connect cameras after production
                continue

            else:  # at this point the user will interact with the arm robot in a positions capture loop
                log.info(f"Received requested user next step in virtual production: {ux_state.status}")
                if ux_state.status == DevicePairingStatus.VirtualEnableTorque:
                    self._production_manager.enable_torque()

                if ux_state.status == DevicePairingStatus.VirtualDisableTorque:
                    self._production_manager.disable_torque()

                if ux_state.status == DevicePairingStatus.VirtualCapturePosition:
                    self._production_manager.capture_virtual_pos()

                if ux_state.status == DevicePairingStatus.VirtualRejectCapturedPosition:
                    self._production_manager.reject_captured_pos()

                if ux_state.status == DevicePairingStatus.VirtualConfirmCapturedPosition:
                    virtual_edge_asset = ux_state.props["virtual_edge_asset"]
                    self._production_manager.confirm_captured_pos(edge_descriptor, virtual_edge_asset)

                if ux_state.status == DevicePairingStatus.VirtualConfirmAllPositions:
                    virtual_pos_tuple = self._production_manager.confirm_all_captured_pos(edge_descriptor)
                    virtual_descriptors = [entry[0] for entry in virtual_pos_tuple]
                    machines = [entry[1] for entry in virtual_pos_tuple]

                    self.edges_configurations = self.edges_configurations + virtual_descriptors

                    for i, machine_id in enumerate(machines):
                        self._machines_table_by_id[machine_id].edges_ids = (
                            self._machines_table_by_id[machine_id].edges_ids +
                            [ virtual_descriptors[i].logical_id ]
                        )

                    ux_state_sent = ux_state.copy()
                    ux_state_sent.status = DevicePairingStatus.SelectDeviceToPair
                    ux_state_sent.props['paired_devices'] = (
                        ux_state_sent.props['paired_devices'].union({edge_descriptor.logical_id})
                    )
                    self._ux_client.send_state_to_ui(ux_state_sent)
                    break
        self._build_internal_tables()  # Refresh internal tables after virtual pairing
        self._production_manager.finish_virtual_production()

    def _publish_paired_devices_to_cloud(self) -> None:
        """This method will publish the paired EdgeDescriptor's to the cloud.

        The cloud will take charge of finishing the pairing in the project model.
        """
        try:
            payload = PairedEdgesPayload(
                self.edges_configurations, self.machines_configurations, self.gateway_config.tenant_id
            )  # Not deep copy required
            payload_json = json.dumps(payload, cls=ComplexEncoder, indent=2)
            gateway_devices_pairing_topic = (
                settings.gateway.mqtt.devices_pairing_topic_template.format(
                    self.gateway_config.gateway_id
                )
            )

            self._mqtt_client.publish_message(
                MQTTMessageType.DEVICES_PAIRING_MESSAGE,
                self.gateway_config.gateway_id,
                gateway_devices_pairing_topic,
                payload_json,
                False,
                False
            )

            log.info(f"Publishing paired devices information in MQTT Topic: {gateway_devices_pairing_topic}")
            log.info(f"Published PairedEdgesPayload: {payload_json}")
        except Exception as e:
            log.error(f'Unexpected error while trying to publish paired devices information event. {e}')

    # ======================== Preparing Devices State Methods ==============================
    def _step_into_preparing_devices(self):
        """Callback to be called when the Gateway enters in the Preparing Devices State.

        It will create the DriversHosts, the Drivers, and wait for the devices to connect.

        TODO: Handle possible exceptions in performed tasks by this method.
        TODO: Transition to specific error when some operation failed. That error should
            be communicated to the UI.
        """
        self.global_state.collected_packages_by_edge = dict(map(
            lambda edge_descriptor: (edge_descriptor.logical_id, 0),
            self.edges_configurations
        ))

        # Clear drivers hosts and wait before creating new hosts
        # to avoid state report too fast.
        self._device_manager.clear_devices()
        time.sleep(1.5)

        self.status = PreparingDevicesStatus.CreatingDriversHosts

        self._update_ux_preparing_state(settings.ux.preparing_devices.configuring_devices_info)

        # Create the DriversHost instances
        self._create_drivers_hosts()

        # Create the Drivers Instances
        self.status = PreparingDevicesStatus.CreatingDrivers
        self._create_drivers()

        self._initialize_job_manager()
        self._job_manager.start()

        self.status = PreparingDevicesStatus.WaitingForDevicesToBeConnected

        self._wait_for_drivers_to_be_ready()

        self._preparing_devices_completed()

    def _update_ux_preparing_state(self, message: str) -> None:

        details = ux_states.UxDetails(
            ux_states.UxDetails.Kind.Info,
            message
        )
        ux_state_sent = ux_states.UxPreparingDevicesState(
            self.state, self.status, details,
            self.gateway_config, self.machines_configurations, self.edges_configurations,
            self._devices_state_table
        )

        self._ux_client.send_state_to_ui(ux_state_sent)

    # ======================== Ready - Sampling States Methods ==================================
    def _step_into_ready_state(self):
        """Callback to be called when the Gateway enters the Ready State"""
        self.status = ReadyStatus.Idle
        log.info('Gateway entered the Ready state')
        self._create_ready_marker_file()
        self._save_global_state()

        self._update_edges_states()
        self._publish_states()
        time.sleep(1)
        self._ping_received = False

        while True:
            self._update_ux_ready_state(settings.ux.ready_state.gateway_is_ready)

            if not settings.gateway.offline_mode:
                self._check_connection()

            if self._at_least_one_edge_sampling():
                log.info('Sampling Window in progress. Gateway transition to Sampling')
                self._start_sampling()

            if self._new_configuration_received_flag:
                log.info('Gateway new configuration received. '
                         'The Gateway will proceed to update to the new configuration.')
                self._job_manager.stop()

                log.debug("Gateway moving to Preparing Devices after new configuration received")
                self._configuration_reception_completed()
                # transitions to configuration reception completed

            elif self._ping_received:
                log.debug("Configuration PING received. Sending states to cloud.")
                self._publish_states()
                self._ping_received = False

            elif self._edges_state_diff:
                log.debug("Flag _edges_state_diff holds True. Publishing State Report.")
                self._publish_states()
                self._edges_state_diff = False

            self._update_edges_states()
            time.sleep(5)

    def _update_ux_ready_state(self, message: str) -> None:
        details = ux_states.UxDetails(
            ux_states.UxDetails.Kind.Info,
            message
        )
        ux_state_sent = ux_states.UxReadyState(
            self.state, self.status, details, self.gateway_config,
            self.machines_configurations, self.edges_configurations,
            self.global_state.packages_collected, self.global_state.packages_sent,
            self.global_state.packages_collected, self.global_state.collected_packages_by_edge,
            self._devices_state_table
        )
        self._ux_client.send_state_to_ui(ux_state_sent)

    def _step_into_sampling_state(self):
        """
           The Gateway should keep sampling until some condition happen.
               - Someone commanded the Gateway to Stop.
               - The Gateway detected some condition inside the system that
                   requires the sampling to stop.
        """

        self.status = GatewaySamplingStatus.Sampling
        close_queue_interval = datetime.datetime.now()

        self._update_edges_states()
        self._publish_states()
        time.sleep(1)  # Waits for 1 sec to avoid state publish limit of 1/sec

        while True:
            # TODO: Commenting this break condition because it can overflow the transitions library
            # if self._check_if_edges_finished_sampling():
            #     log.info("Edges finished current task")
            #     self._device_manager.stop_sampling_windows()
            #     break

            if (
                self._job_task_finished_queue.qsize()
                and self._check_if_edges_finished_sampling()
            ):
                task_window_manager_id = self._job_task_finished_queue.get()
                log.info(f"Job Task reported as finished {task_window_manager_id}. "
                         f"Leaving sampling state")

                while self._job_task_finished_queue.qsize():
                    self._job_task_finished_queue.get()

                self._sampling_completed()

            if self._new_configuration_received_flag:
                log.info("New configuration received. Requesting to stop the current sampling")
                self._device_manager.stop_sampling_windows()

                while not self._check_if_edges_finished_sampling():
                    time.sleep(1)

                log.info('The sampling windows has been stopped.')
                break

            log.debug("Waiting for edges to finish the current task.".format(self._devices_state_table))
            if not settings.gateway.offline_mode:
                try:
                    self._check_connection()
                except (MqttNetworkingUnavailableError, MqttConnectTimeoutError):
                    log.error("Error detected with MQTT client while checking connection")

            self._update_edges_states()

            if self._edges_state_diff:
                log.info("Flag _edges_state_diff holds True. Publishing State Report.")
                self._publish_states()
                self._edges_state_diff = False

            elif self._ping_received:
                log.info("Configuration PING received. Sending states to cloud.")
                self._publish_states()
                self._ping_received = False

            time.sleep(5)

        self.status = GatewaySamplingStatus.CollectPackages
        self._sampling_completed()

    def _check_connection(self):
        """Checks the health of the MQTT connection.

        This will:
            - Check the health of the connection.
            - Process any callback for incoming messages that are pending.
        """
        # Call to subscribe to topics, just in case if there was a networking error at initialization
        try:
            self._mqtt_client.subscribe_to_topic(
                self.gateway_config.gateway_id, self._mqtt_gateway_config_topic, False
            )

            self._mqtt_client.subscribe_to_topic(
                self.gateway_config.gateway_id, self._mqtt_gateway_errors_topic, False
            )
            self._mqtt_client.enable_incoming_messages_processing(1)
        except (MqttNetworkingUnavailableError, MqttConnectTimeoutError):
            log.error("Error detected with MQTT client while checking connection")

    # ======================= Error transitions callbacks ===========================
    def _step_into_production_not_completed_error(self):
        """Callback to call when the _production_phase_not_completed trigger is invoked.

        If this callback is called, it meas that the Gateway never completed the Production
        phase, and it will be unusable until restarted outside of the production line.
        """
        self.status =GatewayErrorStatus.ProductionNotCompleted
        details = ux_states.UxDetails(
            ux_states.UxDetails.Kind.Error,
            settings.ux.error.production_not_completed
        )
        ux_state_sent = ux_states.UxErrorState(
            self.state,
            self.status,
            details,
        )

        self._ux_client.send_state_to_ui(ux_state_sent)

        self._ux_client.wait_for_ux_state()  # Hard Block. The Gateway will not operate anymore.

    # ======================= Private helper methods =======================================
    def _parse_gateway_configuration_object(self, config: Dict) -> None:
        """Parses the Job configuration for the Gateway received from cloud.

        This object contains the following first-level attributes:
            - "job": the job configuration for the Gateway operation.
            - "gateway": The GatewayConfig instance for the Gateway
            - "edges": The edges configuration
            - "machines": The machines configurations.
        """
        root_required_fields = [
            "job", "gateway", "machines", "edges", "configuration_id"
        ]

        for field in root_required_fields:
            if field not in config:
                log.error(f'Configuration does not have {field} field. Could not process received configuration')
                return

        if self.global_state.last_configuration_id != config['configuration_id']:  # Configuration Changed

            # Checks if the configuration changed values. If not, then updates only the configuration version
            if not self._check_configuration_diff(config):
                log.info("A new configuration version received, but the values didn't change for this Gateway."
                         " Updating version number")
                self.global_state.last_configuration_id = config['configuration_id']
                log.info(f"New version number set to: {self.global_state.last_configuration_id}")
                return

            # Validates the Job object
            job_config = JobConfig.build_from_dict(config['job'])
            if not job_config:
                log.error("The Gateway could not create the new Job configuration instance. "
                          "Configuration not updated")
                return

            # Validates the GatewayConfig object
            gateway_config = GatewayConfig.build_from_dict(config['gateway'])
            if not gateway_config:
                log.error("The Gateway could not create the new GatewayConfig instance. "
                          "Configuration not updated")
                return

            # Validates the edges
            edges: List[EdgeDescriptor] = []
            for edge_obj in config['edges']:
                edge_descriptor = EdgeDescriptor.build_from_dict(edge_obj)
                if not edge_descriptor:
                    log.error("The Gateway could not create the associated EdgeDescriptor for "
                              f"the edge: {edge_obj.get('logical_id', 'No logical_id found.')}")
                edges.append(edge_descriptor)

            if any(
                list(map(
                    lambda edge: edge is None, edges
                ))
            ):
                return

            # Validates the machines
            machines: List[MachineMetadata] = []
            for machine_obj in config['machines']:
                machine_metadata = MachineMetadata.build_from_dict(machine_obj)
                if not machine_metadata:
                    log.error("The Gateway could not create the associated MachineMetadata for "
                              f"the machine: {machine_obj.get('machine_id', 'No machine_id found.')}")
                machines.append(machine_metadata)

            if any(
                list(map(
                    lambda machine: machine is None, machines
                ))
            ):
                return

            # Note: Additional validations can be performed here.

            log.info(f'New Job received from cloud. Configuration ID: {config["configuration_id"]}')
            log.info(f'New Gateway Configuration received from cloud with machines: {gateway_config.machines_ids}')
            log.info(f'Received {len(edges)} edges in the configuration')
            log.info(f'Received {len(machines)} machines in the configuration')

            self.global_state.last_configuration_id = config["configuration_id"]
            self.gateway_config.machines_ids = gateway_config.machines_ids
            self.gateway_config.job = job_config
            self.machines_configurations = machines
            self.edges_configurations = edges
            self.gateway_config.tenant_id = gateway_config.tenant_id
            self._plain_received_configuration = config
            self._new_configuration_received_flag = True

        else:
            log.info('Configuration received but version has not changed.')
            if not self._new_configuration_received_flag:
                self._ping_received = True

            if not self._plain_received_configuration:
                self._plain_received_configuration = config

    def _check_configuration_diff(self, new_conf: Dict) -> bool:
        """Helper method to check if a received configuration has changes and requires updating
        the current active configuration.

        Returns:
            True if the configuration changed.
        """
        received_config = new_conf.copy()
        received_config.pop("configuration_id")
        previous_received_conf = self._plain_received_configuration.copy()
        previous_received_conf.pop("configuration_id", None)
        return bool(DeepDiff(received_config, previous_received_conf))

    def _build_internal_tables(self) -> None:
        """Build some internal in-memory tables used by the Gateway when a new configuration
        starts to operate."""
        # Initializes States dictionary for the configured edges
        self._devices_state_table.clear()
        for edge_descriptor in self.edges_configurations:
            if edge_descriptor.is_actuator_device():
                continue

            self._devices_state_table[edge_descriptor.logical_id] = StateReport(
                edge_descriptor.logical_id, DriverState.DISCONNECTED
            )

        # Initializes machines to edges dictionary based on configuration
        self._machine_to_edges_table.clear()
        self._machines_table_by_id.clear()
        self._edge_to_machine_id_table.clear()
        self._edge_logical_id_to_edge_descriptor.clear()
        for machine_metadata in self.machines_configurations:
            self._machine_to_edges_table[machine_metadata.machine_id] = machine_metadata.edges_ids
            self._machines_table_by_id[machine_metadata.machine_id] = machine_metadata

            for edge_serial in machine_metadata.edges_ids:
                self._edge_to_machine_id_table[edge_serial].append(machine_metadata.machine_id)

        for edge_des in self.edges_configurations:
            self._edge_logical_id_to_edge_descriptor[edge_des.logical_id] = edge_des

    def _get_number_of_paired_devices(self) -> int:
        """Returns the number of paired devices in the configuration.

        The criteria of pairing is provided by the DeviceId dataclass.
        """
        paired_devices = list(map(lambda edge_des: edge_des.is_paired(), self.edges_configurations))
        num_paired_devices = paired_devices.count(True)
        return num_paired_devices

    def _initialize_job_manager(self) -> None:
        telemetry_sender = TelemetrySender(
            self.package_queue, self._mqtt_client, self._process_package_stats,
            None, self.gateway_config,
            list(map(
                lambda descriptor: descriptor.logical_id, self.edges_configurations
            ))
        )

        self._job_task_finished_queue = SimpleQueue()

        self._job_manager = JobTasksManager(
            self.gateway_config,
            telemetry_sender,
            self._device_manager,
            self.global_state.last_configuration_id,
            self._machines_table_by_id,
            self._job_task_finished_queue
        )

    def _create_production_manager(self) -> ProductionManager:
        """Returns the instance of the Production Manager to use in device pairing"""
        required_drivers_host = set(map(
            lambda edge_descriptor: edge_descriptor.device_kind, self.edges_configurations
        ))
        log.info(f"Production Manager will configure the hosts: {required_drivers_host}")
        self._production_manager = ProductionManager(self.package_queue, list(required_drivers_host))

    def _create_drivers_hosts(self) -> None:
        """Request to the DeviceManager the creation of the required DriversHost"""
        required_drivers_host = set(map(
            lambda edge_descriptor: edge_descriptor.device_kind, self.edges_configurations
        ))
        log.info(f"DriversHost to configure: {required_drivers_host}")

        for drivers_host_type in required_drivers_host:
            self._device_manager.create_host(drivers_host_type, self.package_queue)
            log.info(f"DriversHost created: {drivers_host_type}")

    def _create_drivers(self) -> None:
        """Request to the DeviceManager to create the appropriate Drivers instances
        for the configured edge devices"""
        # Creation of the List of Tuple[EdgeDescriptor, SamplingWindow] to create the Drivers
        self._device_manager.initialize_drivers(self.edges_configurations)
        self._device_manager.start()

        log.debug("Drivers Added to DriversHost")

    def _update_edges_states(self) -> None:
        """Update the edges states table by reading the states reported by the driver.

        If at least one edge changed its previous stored state, then the flag
        _edges_state_diff will change to True.
        """
        received_states = self._device_manager.get_state_changed_queued_items()

        # This code deals with disconnection of camera handlers. It's good enough for now
        #   to detect that here, and to close the application process to release handlers.
        camera_handlers_images_not_taken = False

        for state_report in received_states:
            if 'error' in state_report.driver_context:
                if state_report.driver_context['error'] == ArmControllerError.IMAGE_NOT_TAKEN:
                    camera_handlers_images_not_taken = True

            if state_report.driver_state != self._devices_state_table[state_report.logical_id]:
                self._devices_state_table[state_report.logical_id] = state_report
                self._edges_state_diff = True

        if camera_handlers_images_not_taken:
            log.info(f'The Camera Handlers could not take images. Restarting '
                     f'main process to attempt recovery...')
            self._publish_states()
            self._job_manager.stop()
            self._device_manager.clear_devices()
            sys.exit(1)

    def _wait_for_drivers_to_be_ready(
            self, timeout_scs: int = settings.gateway.wait_for_devices_startup_timeout
    ) -> None:
        """Waits for all edges to be ready to sample.
        """

        log.info("Waiting for all the devices to be CONNECTED.")
        started = datetime.datetime.now()
        while not all(
                list(map(
                    lambda state_report: state_report.driver_state == DriverState.CONNECTED,
                    self._devices_state_table.values()
                ))
        ):
            self._update_edges_states()
            self._update_ux_preparing_state(settings.ux.preparing_devices.waiting_for_devices_to_connect)

            current_time = datetime.datetime.now()
            if (current_time - started).total_seconds() > timeout_scs:
                log.info('Timeout for devices to connect exceeded. Starting Gateway anyways.')
                return

            else:
                time.sleep(5)

        log.info("All expected edge devices are CONNECTED")

    def _check_if_edges_finished_sampling(self) -> bool:
        """Returns True if all edges drivers are in any state different than SAMPLING.
        The queue with the driver state will report this change.
        """
        self._update_edges_states()
        return all(
            list(map(
                lambda state_report: state_report.driver_state != DriverState.SAMPLING,
                self._devices_state_table.values()
            )))

    def _at_least_one_edge_sampling(self) -> bool:
        """Returns True if at least an edge is sampling, which means that some Sampling
        Window has started"""
        value = any(list(map(
                    lambda state_report: state_report.driver_state == DriverState.SAMPLING,
                    self._devices_state_table.values()
                )))
        return value

    def _mqtt_on_message_callback(self, unused_client, unused_userdata, message):
        """Callback to be executed when a message is received in some subscribed topic
        in the MQTT client"""
        log.info(f"Gateway Message received in MQTT in topic: {message.topic}")

        if message.topic == self._mqtt_gateway_config_topic:
            try:
                config = json.loads(message.payload.decode("utf-8"))
            except json.decoder.JSONDecodeError as e:
                log.error('Error parsing received configuration JSON. Configuration update ignored')
                return

            log.info('Gateway configuration received from Cloud')
            self._parse_gateway_configuration_object(config)

        elif message.topic == self._mqtt_gateway_errors_topic:
            try:
                error = json.loads(message.payload.decode("utf-8"))
            except json.decoder.JSONDecodeError as e:
                log.error('Error parsing received error message JSON.')
                return

            log.error(f'Error received from cloud. {error["error_type"]}, '
                      f'caused by device {error["device_id"]}')

            if error["error_type"] == 'GATEWAY_ATTACHMENT_ERROR':
                log.warning('GATEWAY_ATTACHMENT_ERROR can happens because the device does not exist in IoT Core.')
        else:
            log.warning("Unknown Message received from Cloud.")

    def _scheduled_task_callback(self, machines_tasks: Dict[str, Dict[str, SamplingTask]] ):
        """The callback to be called for each scheduled tasks. This callback is forwarded to the TasksScheduler
        hold by the Gateway."""
        log.info(f"Scheduled sampling tasks executed at: {datetime.datetime.now()}")
        for machine, sampling_tasks in machines_tasks.items():
            self._device_manager.receive_sampling_tasks(sampling_tasks)
            self._device_manager.start_sampling_windows()

    def _process_package_stats(self, package: GatewayPackage, sent_to_cloud: bool) -> None:
        """Process the collected package and register the appropriate stats in the
        Global State"""
        self.global_state.packages_collected = self.global_state.packages_collected + 1
        self.global_state.collected_packages_by_edge[package.metadata.edge_descriptor.logical_id] += 1

        if sent_to_cloud:
            self.global_state.packages_sent = self.global_state.packages_sent + 1

    def _initialize_mqtt_attributes(self) -> None:
        """This method will initialize the MQTT related attributes hold by
        the gateway to be used in the callback when receiving a message.

        TODO: This attributes should be initialized in the production phase
            and should be stored in the global state.
            Currently this attributes are initialized after reading the hardwired
                configuration modules.
        """
        self._mqtt_gateway_commands_topic = settings.gateway.mqtt.device_commands_topic_template.format(
            self.gateway_config.gateway_id
        )
        self._mqtt_gateway_config_topic = settings.gateway.mqtt.device_config_topic_template.format(
            self.gateway_config.gateway_id
        )
        self._mqtt_gateway_errors_topic = settings.gateway.mqtt.device_error_topic_template.format(
            self.gateway_config.gateway_id
        )

    def _get_ngrok_public_address(self) -> Optional[str]:
        address = ""
        try:
            r = requests.get(settings.gateway.ngrok_local_address)
            address = json.loads(r.content.decode())['tunnels'][0]['public_url']
        except Exception as e:
            log.error(f"Error when requesting NGROK local server: {e}")
            address = None
        finally:
            return address

    def _get_state_payload(self) -> GatewayStatePayload:
        """Returns the Dictionary with the desired state fields to report to cloud."""
        payload = GatewayStatePayload(
            self.state,
            list(self._devices_state_table.values()),
            self.global_state.boot_time.strftime(
                settings.time.datetime_format
            ),
            self._get_ngrok_public_address(),
            get_local_ip(),
            self.gateway_config.tenant_id,
        )
        return payload

    def _publish_states(self) -> None:
        """This method will publish the state of the gateway and the states of the edge
        devices.
        """
        try:
            state_json_obj = json.dumps(
                self._get_state_payload(), indent=4, cls=ComplexEncoder
            )

            gateway_state_topic = settings.gateway.mqtt.device_state_topic_template.format(
                self.gateway_config.gateway_id
            )
            self._mqtt_client.publish_message(
                MQTTMessageType.STATE_MESSAGE,
                self.gateway_config.gateway_id,
                gateway_state_topic,
                state_json_obj,
                False,
                False,
                delay=1  # We wait 1 second because states requires 1 update/sec
            )

            for edge_serial, state_report in self._devices_state_table.items():
                edge_state = state_report.driver_state
                log.debug(f'Publishing State event for Driver: {edge_serial}')
                edge_topic = settings.gateway.mqtt.device_state_topic_template.format(
                    edge_serial
                )
                self._mqtt_client.publish_message(
                    MQTTMessageType.STATE_MESSAGE,
                    edge_serial,
                    edge_topic,
                    json.dumps({"state": str(edge_state)}),
                    attach=True, track_acknowledge=False,
                    delay=1  # We wait 1 second because states requires 1 update/sec
                )
        except Exception as e:
            log.error(f'Unexpected error while trying to publish the Gateway state: {e}')

    # ======================= Legacy Methods ========================================
    def _state_log_msg(self):
        return f"Gateway enters to {self.state} with status {self.status}"
