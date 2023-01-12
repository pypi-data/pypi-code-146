# constant pair fee rate at 0.30%
V2FEES = 0.003
# modifiable price limit to avoid abnormal situations
PRICE_LIMIt = 100000


class UniswapV2PriceCalculator:
    """
    The implementation of UniSwap V2 price calculation. It takes consideration of the pair fee rate(currently 0.30%).
    """
    def __init__(self, v2fees: float = V2FEES, price_limit: float = PRICE_LIMIt):
        """
        :param v2fees: pair fee rate
        :param price_limit: modifiable price limit
        """
        self.v2fees = v2fees
        self.price_limit = price_limit

    def calculate_price(self, nb_base_token: int, price_base_token: float, nb_target_token: int) -> float:
        """
        Calculate the price of maximum target token
        For the simplicity, we do not take consideration of the price_limit(0.3%) in the calculations
        If the price exceeds the given price_limit, zero will be returned
        :param nb_base_token: number of the base token in the pool
        :param price_base_token: price of the base token
        :param nb_target_token: number of the target(counterparty) token in the pool
        :return: the price of the target(counterparty) token
        """
        if nb_base_token <= 0 or price_base_token <= 0 or nb_target_token <= 0:
            raise ValueError("All parameters should be positive")
        price_target_token = (nb_base_token * price_base_token) / nb_target_token
        return price_target_token if price_target_token < self.price_limit else 0
