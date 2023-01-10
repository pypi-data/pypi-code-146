from bittrade_kraken_rest.connection.observable import prepare_private
from bittrade_kraken_rest.connection.result import send_and_map_to_result

GetAccountBalanceResult = dict[str, str]


def get_account_balance_request():
    """
    Get account balances
    :return:
    """
    return prepare_private(url="/0/private/Balance")


def get_account_balance_result():
    return send_and_map_to_result(GetAccountBalanceResult)
