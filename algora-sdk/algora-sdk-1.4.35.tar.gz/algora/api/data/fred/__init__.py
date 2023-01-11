"""
Data API query functions for [FRED](https://fred.stlouisfed.org/) data.
"""
from algora.api.data.fred.asynchronous import async_get_series
from algora.api.data.fred.synchronous import get_series
