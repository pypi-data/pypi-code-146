# External libraries
import requests

# Internal libraries
from ..exchange_utils import clean_supported_symbols

def get_bitfinex_symbol_pairs():

    # Getting exchange info from Binance's public API endpoint
    res = requests.get('https://api.bitfinex.com/v1/symbols_details')
    symbol_pair_list = res.json()
    
    symbols = []
    for symbol in symbol_pair_list:
        if ':' not in symbol['pair']: symbols.append(symbol['pair'].lower())

    return clean_supported_symbols(symbols)