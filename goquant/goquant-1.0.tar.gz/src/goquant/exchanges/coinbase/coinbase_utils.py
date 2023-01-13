# Extrnal libraries
import requests

# Internal libraries
from ..exchange_utils import clean_supported_symbols

def get_coinbase_symbol_pairs():

    # Getting exchange info from Binance's public API endpoint
    res = requests.get('https://api.exchange.coinbase.com/products')
    symbol_pair_list = res.json()
    
    symbols = []
    for symbol in symbol_pair_list:
        symbols.append(symbol['id'].lower())

    return clean_supported_symbols(symbols)