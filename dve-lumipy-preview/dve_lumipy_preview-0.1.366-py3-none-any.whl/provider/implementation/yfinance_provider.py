from typing import Optional, Dict, Union

from pandas import DataFrame
from yfinance import Ticker

from lumipy.provider.base_provider import BaseProvider
from lumipy.provider.metadata import ColumnMeta, ParamMeta
from lumipy.typing.sql_value_type import SqlValType


class YFinanceProvider(BaseProvider):
    """Provider that extracts historical price data from yahoo finance using the yfinance package.

    """

    def __init__(self):

        columns = [
            ColumnMeta('Ticker', SqlValType.Text, 'The stock ticker'),
            ColumnMeta('Date', SqlValType.DateTime, 'The date'),
            ColumnMeta('Open', SqlValType.Double, 'Opening price'),
            ColumnMeta('High', SqlValType.Double, 'High price'),
            ColumnMeta('Low', SqlValType.Double, 'Log price'),
            ColumnMeta('Close', SqlValType.Double, 'Closing price'),
            ColumnMeta('Volume', SqlValType.Double, 'Daily volume'),
            ColumnMeta('Dividends', SqlValType.Double, 'Dividend payment on the date.'),
            ColumnMeta('StockSplits', SqlValType.Double, 'Stock split factor on the date'),
        ]
        params = [
            ParamMeta(
                'Tickers',
                SqlValType.Text,
                'The ticker/tickers to get data for. To specify multiple tickers separate them by a "+"',
                is_required=True
            ),
            ParamMeta('Range', SqlValType.Text, 'How far back to get data for.', 'max'),
        ]

        super().__init__(
            'Test.YFinance.PriceHistory',
            columns,
            params,
            description='Price data from Yahoo finance for a given ticker'
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        tickers = params['Tickers'].strip('+').split('+')

        for i, ticker in enumerate(tickers):

            df = Ticker(ticker).history(period=params['Range']).reset_index()

            if df.shape[0] == 0:
                yield self.progress_line(f'Result for {ticker} was empty! It may not exist or has been delisted.')
                continue

            df.columns = [c.replace(' ', '') for c in df.columns]
            df['Ticker'] = ticker
            yield df
