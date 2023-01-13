# External libraries
import requests

# Internal libraries
from ..exchange_utils import clean_supported_symbols

def get_bybit_symbol_pairs():

    # Getting exchange info from Binance's public API endpoint
    res = requests.get('https://api.bybit.com/derivatives/v3/public/instruments-info')
    symbol_pair_list = res.json()['result']['list']
    
    symbols = []
    for symbol in symbol_pair_list:
        symbols.append(symbol['symbol'].lower())

    return clean_supported_symbols(symbols)