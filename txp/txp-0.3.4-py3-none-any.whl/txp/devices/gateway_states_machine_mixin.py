"""
This module implements the Gateway States Machine Mixin class.

This separates the boilerplate declaration of the states machine
from the Gateway processing code.
"""

# ============================ imports =========================================
import transitions
from typing import List
from txp.devices.gateway_global_state import GatewayGlobalState
from txp.common.configuration import GatewayConfig
from txp.common.edge import EdgeDescriptor, MachineMetadata
from txp.devices.gateway_states_enums import *
from pathlib import Path
import shelve
import os
from txp.common.config import settings
import logging
import datetime

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


# ==============================================================================
# Definition of the Gateway States Machine class.
# ==============================================================================
class GatewayStatesMachineMixin:
    """The Gateway States Machine Mixin offers the functionality of the State
    machine to the Gateway class.

    This class takes care of all the boilerplate of the transitions.Machine
    declaration.

    This class holds a reference to the GatewayGlobalState dataclass which contains
    the Gateway state to be collected in production, and to be persisted.

    Transitions callbacks defined for the States Machine are methods defined by
    the Gateway.
    """

    def __init__(self):
        # State Machine initialization
        # The machine starts in Uninitialized. Later on, when everything is ready,
        # The Gateway will call the first real state.
        self._states_machine: transitions.Machine = transitions.Machine(
            model=self,
            states=GatewayStates,
            initial=GatewayStates.Uninitialized,
            before_state_change="_update_visited_states",
        )

        self._visited_states_stack: List[str] = []
        """_states_registry: A stack of visited states. Currently being used in unit testing to check
        visited states"""

        self._init_transitions()

        self.global_state: GatewayGlobalState = None
    # ================ Property definitions for syntactic sugar access ================================
    @property
    def gateway_config(self) -> GatewayConfig:
        return self.global_state.gateway_conf

    @gateway_config.setter
    def gateway_config(self, new_gateway_conf: GatewayConfig) -> None:
        self.global_state.gateway_conf = new_gateway_conf

    @property
    def machines_configurations(self) -> List[MachineMetadata]:
        return self.global_state.machines_configurations

    @machines_configurations.setter
    def machines_configurations(self, machines_configs: List[MachineMetadata]) -> None:
        self.global_state.machines_configurations = machines_configs

    @property
    def edges_configurations(self) -> List[EdgeDescriptor]:
        return self.global_state.edges_configurations

    @edges_configurations.setter
    def edges_configurations(self, edges_configs: List[EdgeDescriptor]) -> None:
        self.global_state.edges_configurations = edges_configs

    @property
    def status(self):
        """Returns the status value form the Global State.
        Status value is an enumerated member from one of the states status enumerations"""
        return self.global_state.status

    @status.setter
    def status(self, new_status):
        self.global_state.status = new_status

    # ========================== Class Private Methods ================================
    def _load_global_state(self) -> None:
        """Loads the appropriate global state for the Gateway object.

        New Gateway in Production -> New GatewayGlobalState instance.
        Produced Gateway ready to Start -> Recovered GatewayGlobalState from disk.

        If a Gateway started the production phase, and never completed it for some reason,
        then the Gateway will transition to an Error State. For that the marker files are used.
        """
        if not os.path.exists(settings.gateway.initialized_marker_file):
            log.info('No previous marker files found. Initialize a new Gateway')
            self.global_state = self._get_new_state()

        else: 
            # The Gateway must have finished the production phase. Otherwise, Error.
            if not os.path.exists(settings.gateway.ready_marker_file):
                # log.info("The Gateway never completed the Production Phase. Transition to Error State.")
                # self.global_state = self._get_new_state()  # Assigns a not None state
                # self._production_phase_not_completed()  # Transitions to error
                log.info('Previous marker files found, but production never completed. Initialize a new Gateway')
                self.global_state = self._get_new_state()

            else:
                global_state_recovered_db = shelve.open(
                    settings.gateway.global_state_persistence_path
                )
                global_state_recovered = global_state_recovered_db["global_state"]
                global_state_recovered_db.close()
                self.global_state = global_state_recovered
                self.global_state.boot_time = datetime.datetime.now().replace(microsecond=0)

    def _get_new_state(self) -> GatewayGlobalState:
        """Returns a instance of a new Global State with default values"""
        return GatewayGlobalState(
                GatewayConfig(
                    "",
                    "",
                    "",
                    settings.gateway.cloud_region,
                    [],
                    ""
                ),
                [],
                [],
                GatewayStates.Startup,
                StartupStatus.RequestRequiredValues,
                0,
                {},
                0,
                datetime.datetime.now().replace(microsecond=0),
                "0"
        )

    def _init_transitions(self) -> None:
        """Add the transitions to the initialized gateway states machine

        Each transition can have different types of callbacks that will be
        executed when the transition is called.
        https://github.com/pytransitions/transitions#callback-execution-order

        Since the Gateway holds the states machine as internal attribute, the
        transitions will invoke callbacks that are methods of the Gateway.
        """

        transitions_list = [
            {
                "trigger": "begin_startup",
                "source": GatewayStates.Uninitialized,
                "dest": GatewayStates.Startup,
                "after": [
                    "_update_global_state_value",
                    "_step_into_startup"
                ],
            },
            {
                "trigger": "_startup_failed",
                "source": GatewayStates.Startup,
                "dest": GatewayStates.StartupError,
                "after": ["_update_global_state_value", "_step_into_startup_error"],
            },
            {
                "trigger": "_startup_completed",
                "source": GatewayStates.Startup,
                "dest": GatewayStates.ConfigurationReception,
                "after": [
                    "_update_global_state_value",
                    "_step_into_configuration_reception",
                ],
            },
            {
                # This transition can be called from the Startup State OR
                # the Uninitialized State when recovering from previous completed Startup State
                "trigger": "_configuration_reception_completed",
                "source": [
                    GatewayStates.ConfigurationReception,
                    GatewayStates.Uninitialized,
                    GatewayStates.Ready
                ],
                "dest": GatewayStates.ConfigurationValidation,
                "after": [
                    "_update_global_state_value",
                    "_step_into_configuration_validation",
                ],
            },
            {
                "trigger": "_configuration_validation_completed",
                "source": [GatewayStates.ConfigurationValidation, GatewayStates.Uninitialized],
                "dest": GatewayStates.DevicesPairing,
                "after": [
                    "_update_global_state_value",
                    "_step_into_devices_pairing",
                ]
            },
            {
                "trigger": "_production_phase_not_completed",
                "source": GatewayStates.Uninitialized,
                "dest": GatewayStates.Error,
                "after": [
                    "_update_global_state_value",
                    "_step_into_production_not_completed_error"
                ]
            },
            {
                # This transition will put the Gateway in the PreparingDevices state.
                # If a Gateway is already 'produced', it can jump right away to this state
                # to prepare all the DriversHost and Drivers.
                "trigger": "_device_pairing_completed",
                "source": [GatewayStates.DevicesPairing, GatewayStates.ConfigurationValidation],
                "dest": GatewayStates.PreparingDevices,
                "after": [
                    "_update_global_state_value",
                    "_step_into_preparing_devices"
                ]
            },
            {
               # This transition will put the Gateway in the PreparingDevices state when
               # a new configuration has been received and parsed while the Gateway was in
               # Ready or Sample state.
               "trigger": "_prepare_devices_for_new_config",
               "source": [GatewayStates.Ready, GatewayStates.Uninitialized],
               "dest": GatewayStates.PreparingDevices,
               "after": [
                   "_update_global_state_value",
                   "_step_into_preparing_devices"
               ]
            },
            {
                "trigger": "_preparing_devices_completed",
                "source": [GatewayStates.PreparingDevices, GatewayStates.ConfigurationValidation],
                "dest": GatewayStates.Ready, # Uninitialized while production process gets implemented
                "after": [
                    "_update_global_state_value",
                    "_step_into_ready_state"
                ]
            },
            {
                "trigger": "_start_sampling",
                "source": GatewayStates.Ready,
                "dest": GatewayStates.Sampling,
                "after": [
                    "_update_global_state_value",
                    "_step_into_sampling_state"
                ]
            },
            {
                "trigger": "_sampling_completed",
                "source": GatewayStates.Sampling,
                "dest": GatewayStates.Ready,
                "after": [
                    "_update_global_state_value",
                    "_step_into_ready_state"
                ]
            }
        ]

        self._states_machine.add_transitions(transitions_list)

    def _update_visited_states(self, *args, **kwargs):
        """Updates the visited states stack"""
        self._visited_states_stack.insert(0, self.state)

    def _update_global_state_value(self) -> None:
        """Updates the state variable inside the GlobalState attribute to the state
        value inside the machine object"""
        self.global_state.state = self.state

    def _save_global_state(self) -> None:
        """Save the GlobalState instance attribute on disk using shelve."""
        log.debug("Trying to save Global State in file system")
        with shelve.open(settings.gateway.global_state_persistence_path) as db:
            db["global_state"] = self.global_state
            db.close()
        log.debug("Global State saved in file system.")

    def _create_initialized_marker_file(self) -> None:
        """Creates the marker file to indicate that the Gateway started a production phase.

        This marker file indicates that the Gateway started a production phase.
        """
        if not Path(settings.gateway.initialized_marker_file).exists():
            Path(settings.gateway.initialized_marker_file).touch()

    def _create_ready_marker_file(self) -> None:
        """Creates the marker file to indicate that the Gateway completed the production phase.
        """
        if not Path(settings.gateway.ready_marker_file).exists():
            Path(settings.gateway.ready_marker_file).touch(exist_ok=True)

    def _last_visited_state(self) -> GatewayStates:
        return self._visited_states_stack[0]

