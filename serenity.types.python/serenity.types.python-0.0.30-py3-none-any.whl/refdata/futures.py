from serenity_types.refdata.derivatives import Expiry, ListedDerivative, PayoffType


class Future(ListedDerivative):
    """
    An exchange-listed futures contract.
    """

    expiry: Expiry
    """
    Expiration date and time for this particular term futures contract.
    """

    payoff_type: PayoffType
    """
    Whether the contract tracks the price movement (LINEAR) or its mirror image (INVERSE).
    """


class Perpetual(ListedDerivative):
    """
    An exchange-listed perpetual future, sometimes referred to as a swap.
    """

    payoff_type: PayoffType
    """
    Whether the contract tracks the price movement (LINEAR) or its mirror image (INVERSE).
    """
