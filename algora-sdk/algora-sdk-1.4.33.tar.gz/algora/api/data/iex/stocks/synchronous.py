from typing import Union, Dict, List

from pandas import DataFrame

from algora.api.data.iex.__util import __base_request
from algora.api.data.iex.stocks.__util import (
    _symbols_request_info, _historical_prices_request_info, _news_request_info, _peer_group_request_info
)
from algora.common.decorators import data_request
from algora.common.function import transform_one_or_many, no_transform, data_required_transform


@data_request
def symbols() -> DataFrame:
    """
    Wrapper for [IEX symbols API](https://iexcloud.io/docs/api/#symbols) to get supported symbols.

    Returns:
         DataFrame: IEX supported symbols
    """
    request_info = _symbols_request_info()
    return __base_request(**request_info)


@data_request(transformers=[
    data_required_transform,
    lambda d: transform_one_or_many(d, 'chart')
])
def historical_prices(*symbol: str, **kwargs) -> Union[DataFrame, Dict[str, DataFrame]]:
    """
    Wrapper for IEX historical stock prices via
    [Time Series API](https://iexcloud.io/docs/api/#time-series-endpoint).

    Args:
         symbol (*str): Stock symbol(s), such as "AAPL" or "AAPL", "FB"
         **kwargs: Optional args to pass to the IEX API

    Returns:
        Union[DataFrame, Dict[str, DataFrame]]: Historical prices for the symbol(s) requested
    """
    # default query params
    request_info = _historical_prices_request_info(*symbol, **kwargs)
    return __base_request(**request_info)


@data_request
def news(symbol: str, **kwargs) -> DataFrame:
    """
    Wrapper for [IEX stock news for given symbol](https://iexcloud.io/docs/api/#news).

    Args:
        symbol (str): Stock symbol, such as AAPL
        **kwargs: Optional args to pass to the IEX API

    Returns:
        DataFrame: News for the symbol requested
    """
    request_info = _news_request_info(symbol, kwargs)
    return __base_request(**request_info)


@data_request(transformers=[no_transform])
def peer_group(symbol: str) -> List[str]:
    """
    Wrapper for [IEX stock peer group](https://iexcloud.io/docs/api/#peers).

    Args:
        symbol (str): Stock symbol, such as AAPL

    Returns:
         List[str]: List of symbols
    """
    request_info = _peer_group_request_info(symbol)
    return __base_request(**request_info)
