# External libraries
import requests

# Internal libraries
from ..exchange_utils import clean_supported_symbols

def get_okex_symbol_pairs():

    # Getting exchange info from Binance's public API endpoint
    res = requests.get('https://www.okx.com/api/v5/public/instruments?instType=SPOT')
    symbol_pair_list = res.json()['data']

    symbols = []
    for symbol in symbol_pair_list:
        symbols.append(symbol['instId'].lower())

    return clean_supported_symbols(symbols)