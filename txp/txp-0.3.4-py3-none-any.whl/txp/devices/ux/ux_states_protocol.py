"""
This module defines the classes used to exchange information between
the Gateway process and the UI process.
"""
# ==================== Imports ===================================
from dataclasses import dataclass
from typing import List, Set, Optional, Dict
from txp.common.edge import MachineMetadata, EdgeDescriptor
from txp.devices.gateway_states_enums import *
from txp.devices.drivers.driver import DriverState
import copy
import enum


# =================== Ux States Classes ====================================
# UX States classes are designed to represent the Gateway State in the UX process,
# along with attributes used to track the Ux state itself.
@dataclass
class UxDetails:
    class Kind(enum.Enum):
        Warning=1
        Info=2
        Error=3

    """A dataclass to hold and give structure to string messages that
    provide human readable details about some state
    
    This enumeration can be used with streamlit to provide visual feedback
    using st.warning, st.error or st.info.
    """
    kind: Kind
    message: str


@dataclass
class UxStateBase:
    """A base class which defines the common attributes for all the
    messages passed between the Gateway and the UX process"""
    state: GatewayStates
    """state: A member of the GatewayStates enumeration"""
    status: "Status"
    """status: A member of some Status enumeration defined in the 
        gateway enumerations"""
    details: Optional[UxDetails]
    """An optional UxDetails field to provide human readable details 
        about the current state"""


@dataclass
class UxStartupState(UxStateBase):
    """The UX state to work with the Gateway Startup state.

    In Startup, the UX will require from the user all the pre-conditioned
    values that are required to operate.

    All the values requested to the user will be individual attributes in
    this class.
    """
    gateway_id: str
    """The gateway device ID / Serial configured in the Cloud IoT management"""
    registry_id: str
    """The IoT registry to which the gateway belongs"""
    private_key_received: bool
    """private_key_received: True if the UX already received the private key file upload"""
    gateway_serial_received: bool
    """gateway_serial_received: True if the UX already received the Gateway Serial"""
    registry_name_received: bool
    """registry_name_received: True if the UX already received the IoT registry name"""
    project_id_received: bool
    project_id: str


@dataclass
class UxConfigurationReceptionState(UxStateBase):
    """Contains the received configurations from the cloud

    The Gateway will be updating the state as it
    receives the remote configurations.

    At this point, the Gateway will send the GatewayConfig
    instead of inividual attributes for the gateway device ID
    and the registry ID.
    """
    gateway_conf: "GatewayConfig"
    """gateway_conf: The GatewayConfig instance received from cloud."""
    machines: List[MachineMetadata]
    """machines: The Machines logical information received from cloud."""
    edges: List[EdgeDescriptor]
    """edges: The EdgeDescriptors received from cloud"""
    all_received: bool
    """all_received: True if all the configurations were received."""


@dataclass
class UxConfigurationValidationState(UxStateBase):
    """Contains the information used during the Configuration Validation Step.

    Note: Currently, the Gateway waits for the acknowledge of the user in order to move
    to the next state.
    This State allows Restart of the Gateway.
    """
    gateway_conf: "GatewayConfig"
    """gateway_conf: The GatewayConfig instance received from cloud."""
    machines: List[MachineMetadata]
    """machines: The Machines logical information received from cloud."""
    edges: List[EdgeDescriptor]
    """edges: The EdgeDescriptors received from cloud"""


@dataclass
class UxDevicePairingState(UxStateBase):
    gateway_conf: "GatewayConfig"
    machines: List[MachineMetadata]
    edges: List[EdgeDescriptor]
    props: Dict

    def copy(self) -> "UxDevicePairingState":
        return copy.deepcopy(self)

@dataclass
class UxPreparingDevicesState(UxStateBase):
    """Preparing Devices State to be received in the UI process
    when the gateway is preparing the devices.
    """
    gateway_conf: "GatewayConfig"
    machines: List[MachineMetadata]
    edges: List[EdgeDescriptor]
    devices_connection_table: Dict[str, DriverState]


@dataclass
class UxErrorState(UxStateBase):
    """The UxErrorState to communicate an error state to the UI process.
    """
    pass


@dataclass
class UxReadyState(UxStateBase):
    gateway_conf: "GatewayConfig"
    machines: List[MachineMetadata]
    edges: List[EdgeDescriptor]
    collected_packages: int
    sent_packages: int
    completed_package_cycles: int
    packages_received_by_edge: Dict[str, int]
    devices_connection_table: Dict[str, DriverState]


@dataclass
class UxErrorState(UxStateBase):
    """The UxErrorState to communicate an error state to the UI process.
    """
    pass


# =================== Ux Deprecated Mock Classes ====================================
# Deprecated classes used in the first version of the streamlit app to test the Raspberry OS.
# If some part of the UX is still mocked, it's using these classes.
# TODO. Remove this classes and create the final UXStateBase implementations for the rest of states.

@dataclass
class GatewayCommonMetadata:
    """A base class which shares attributes common for all the UX Gateway
    states classes.

    Each state will contain all this information.

    Note: if there's a piece of information that requires to be shared
    progressively across all states, it probably should be defined as an
    attribute here.

    TODO: Deprecated. This was used for mocking in the Raspberry image.
    """

    device_id: str
    """The gateway device ID"""
    registry_id: str
    """The IoT registry to which the gateway belongs"""
    state: GatewayStates
    """The gateway state value"""
    status: enum.Enum
    """The current status for the state"""

@dataclass
class UxSamplingState(GatewayCommonMetadata):
    """Contains information about the collected Packages, while being
    in the Sampling State.

    TODO: Information about packaging is better to have it as a GlobalState
        value. A State that the Gateway object uses to handle global
        information collected during the Gateway lifecycle.
        A reference to that State might be received here. That'll simplify a lot
        the states declared in the Ux.
    """

    gateway_conf: "GatewayConfig"
    machines: List[MachineMetadata]
    edges: List[EdgeDescriptor]
    paired_devices: Set[str]
    expected_devices: Set[str]
    collected_packages: int
    sent_packages: int
    completed_package_cycles: int
    packages_received_by_edge: Dict[str, int]
