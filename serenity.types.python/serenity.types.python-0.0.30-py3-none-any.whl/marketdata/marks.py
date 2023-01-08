from datetime import datetime
from uuid import UUID

from serenity_types.utils.serialization import CamelModel


class AssetMarkPrice(CamelModel):
    """
    A single asset price as of the chosen MarkTime.
    """

    asset_id: UUID
    """
    Unique ID of the referenced asset.
    """

    mark_time: datetime
    """
    The specific mark time used for latest price.
    """

    mark_price: float
    """
    The price at the mark time.
    """
