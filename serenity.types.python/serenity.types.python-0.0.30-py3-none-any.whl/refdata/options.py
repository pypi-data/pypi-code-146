from enum import Enum

from serenity_types.refdata.derivatives import Expiry, ListedDerivative


class OptionStyle(Enum):
    """
    Variety of option supported. Right now we only support vanilla European options.
    """

    AMERICAN = 'AMERICAN'
    """
    An option that can be exercised at any time up to the expiry date.
    """

    EUROPEAN = 'EUROPEAN'
    """
    An option that can only be exercised on the expiry date.
    """


class OptionType(Enum):
    """
    Put/call flag for options.
    """

    PUT = 'PUT'
    """
    The right but not the obligation to sell the underlier at the strike price on exercise.
    """

    CALL = 'CALL'
    """
    The right but not the obligation to buy the underlier at the strike price on exercise.
    """


class ListedOption(ListedDerivative):
    """
    An exchange-listed vanilla option.
    """

    option_type: OptionType
    """
    Whether this is a put or call contract.
    """

    option_style: OptionStyle
    """
    Exercise type for this option, e.g. European exercise.
    """

    strike_price: float
    """
    Strike price for the option contract, e.g. 20000.
    """

    expiry: Expiry
    """
    Expiration date and time for this option.
    """
