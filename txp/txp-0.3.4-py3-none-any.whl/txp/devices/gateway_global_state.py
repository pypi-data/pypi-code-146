"""
This module implements the Gateway Global State.

The Gateway Global State is responsible to hold:
    - The Gateway States Machine.
    - The Persistence of the system.
    - Any kind of information that needs to be persisted when the
        Gateway transitions between states.
"""
# ============================ imports =========================================
from typing import List, Dict
from txp.common.configuration import GatewayConfig
from txp.common.edge import EdgeDescriptor, MachineMetadata
from txp.devices.gateway_states_enums import *
from dataclasses import dataclass
from txp.common.config import settings
import datetime
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


@dataclass
class GatewayGlobalState:
    """The Gateway Global state class. This dataclass defines Gateway attributes that are
    collected in the configuration process, and needs to be persisted.
    """

    gateway_conf: GatewayConfig
    """gateway_config: The current GatewayConfig of the Gateway."""
    machines_configurations: List[MachineMetadata]
    """machines_configurations: The logical configurations for the Machines monitored by the 
    Gateway"""
    edges_configurations: List[EdgeDescriptor]
    """edges_configurations: The logical configurations for the Edges configured to work with 
    this Gateway"""
    state: GatewayStates
    """state: The current state value of the Gateway"""
    status: ...
    """status: An status member defined in the status enumeration for the current state"""
    packages_collected: int
    """packages_collected: an attribute to track how many packages has been collected by the Gateway."""
    collected_packages_by_edge: Dict[str, int]
    """collected_package_by_edge: A table to count the number of packages collected by edges using the serial as key"""
    packages_sent: int
    """packages_sent: an attribute to track how many packages has been sent to the cloud"""
    boot_time: datetime
    """boot_time: The boot time of the Gateway instance."""
    last_configuration_id: str
    """last_configuration_id: The last configuration ID received in the Gateway."""
