from enum import Enum
from uuid import UUID

from serenity_types.utils.serialization import CamelModel


class NetworkType(Enum):
    """
    Categories of decentralized network.
    """

    BLOCKCHAIN = 'BLOCKCHAIN'
    """
    An L1 blockchain network, e.g. Ethereum.
    """

    L2_PROTOCOL = 'L2_PROTOCOL'
    """
    An L2 (Layer 2) network like Optimism or Arbitrum.
    """

    BRIDGE = 'L2_PROTOCOL'
    """
    A bridge that connects other networks like the Wormhole bridge.
    """


class Network(CamelModel):
    """
    Reference data describing a decentralized network protocol, e.g. an L1 blockchain or bridge.
    """

    network_id: UUID
    """
    Unique ID for this blockchain, bridge, etc..
    """

    network_type: NetworkType
    """
    Category of decentralized network.
    """

    short_name: str
    """
    One-word, lowercase code for this Network, e.g. bitcoin.
    """

    display_name: str
    """
    Human-friendly name for this Network, e.g. Bitcoin.
    """
