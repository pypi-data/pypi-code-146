from typing import List
from uuid import UUID

from serenity_types.utils.serialization import CamelModel


class AssetPosition(CamelModel):
    """
    A simple representation of holding a certain amount of a given asset.
    This is going to be replaced with a much more flexible Portfolio
    representation in Q1'23.
    """

    asset_id: UUID
    """
    Unique identifier of the asset from Serenity's asset master database.
    """

    quantity: float
    """
    The number of tokens, shares, contracts, etc. held in this position.
    If positive this indicates a long position; if negative, a short one.
    """


class SimplePortfolio(CamelModel):
    """
    A simple portfolio representation that just maps the positions to
    positive or negative quantities for long and short. There is no
    history, detail on custody or any other context.
    """

    portfolio_id: UUID
    """
    Unique ID; in the initial implementation this is assigned locally in
    a client installation-hosted database.
    """

    base_currency_id: UUID
    """
    Asset ID of the base currency for this portfolio.
    """

    portfolio_name: str
    """
    Descriptive name for this portfolio, for display only.
    """

    portfolio_manager: str
    """
    In the initial implementation, a text field for the PM;
    eventually will link to user ID in the database.
    """

    asset_positions: List[AssetPosition]
    """
    List of positions in the portfolio.
    """
