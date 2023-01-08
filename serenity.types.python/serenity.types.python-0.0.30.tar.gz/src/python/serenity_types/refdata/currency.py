from serenity_types.refdata.asset import Asset


class Currency(Asset):
    """
    An asset representing a fiat currency like the dollar, euro or yen. Note this will
    need to be extended to link to a fiat_issuance_id for the Exposure UUID once we
    have distinct fiat exposure reference data.
    """

    iso_currency_code: str
    """
    The ISO currency code, e.g. USD or EUR.
    """
