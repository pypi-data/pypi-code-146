from enum import Enum
from uuid import UUID

from serenity_types.utils.serialization import CamelModel


class OrganizationType(Enum):
    """
    Category of legal entity; generally used when referring to who provides
    information, prices, positions, etc..
    """

    EXCHANGE = 'EXCHANGE'
    """
    A centralized exchange, e.g. Binance or Deribit.
    """

    DEALER = 'DEALER'
    """
    A broker/dealer, prime broker, OTC desk associated with a prop trading
    firm or market maker, or any other entity that does OTC deals and otherwise
    could be a counterparty.
    """

    INDEX_PROVIDER = 'INDEX_PROVIDER'
    """
    A benchmark or other index provider like S&P.
    """

    DATA_PROVIDER = 'DATA_PROVIDER'
    """
    A data vendor like Kaiko or Amberdata. This is to allow for the possibility
    that data might come either directly from an exchange or indirectly via
    a data aggregator of some kind.
    """

    ORACLE = 'ORACLE'
    """
    A price oracle like ChainLink or Pyth.
    """

    DAO = 'DAO'
    """
    A Decentralized Autonomous Organization (DAO); generally associated with DeFi
    and other protocols as the owner, e.g. MakerDAO.
    """

    OTHER = 'OTHER'
    """
    Any other kind of organization we wish to track.
    """


class Organization(CamelModel):
    organization_id: UUID
    """
    Unique ID for this organization.
    """

    organization_type: OrganizationType
    """
    Catagory of organization, e.g. an exchange.
    """

    short_name: str
    """
    One-word, lowercase code for this organization, e.g. spdix.
    """

    display_name: str
    """
    Human-friend name for this organization, e.g. S&P Dow Jones Indices.
    """
