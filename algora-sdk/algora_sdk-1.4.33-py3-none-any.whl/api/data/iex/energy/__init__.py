"""
Data API query functions for [IEX](https://iexcloud.io/) energy data.
"""
from algora.api.data.iex.energy.asynchronous import async_historical_oil_prices
from algora.api.data.iex.energy.synchronous import historical_oil_prices
