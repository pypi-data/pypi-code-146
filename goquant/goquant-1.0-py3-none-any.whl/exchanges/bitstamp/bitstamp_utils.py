# External libraries
import requests

# Internal libraries
from ..exchange_utils import clean_supported_symbols

def get_bitstamp_symbol_pairs():

    res = requests.get('https://www.bitstamp.net/api/v2/trading-pairs-info/')
    symbol_pair_list = res.json()
    
    symbols = []
    for symbol in symbol_pair_list:
        symbols.append(symbol['url_symbol'].lower())

    return clean_supported_symbols(symbols)