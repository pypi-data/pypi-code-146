# External libraries
import requests

# Internal libraries
from ..exchange_utils import clean_supported_symbols

def get_huobi_symbol_pairs():

    # Getting exchange info from Binance's public API endpoint
    res = requests.get('https://api.huobi.pro/v1/common/symbols')
    symbol_pair_list = res.json()['data']

    symbols = []
    for symbol in symbol_pair_list:
        symbols.append(symbol['symbol'].lower())

    return clean_supported_symbols(symbols)