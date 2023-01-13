# External libraries
import requests

# Internal libraries
from ..exchange_utils import clean_supported_symbols

def get_binance_symbol_pairs():

    # Getting exchange info from Binance's public API endpoint
    res = requests.get('https://api.binance.com/api/v3/exchangeInfo')
    symbol_pair_list = res.json()['symbols']
    
    symbols = []
    for symbol in symbol_pair_list:
        symbols.append(symbol['symbol'].lower())

    return clean_supported_symbols(symbols)