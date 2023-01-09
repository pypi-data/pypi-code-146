import pandas

from ..storage.tcp import HttpData
from .data_analyser import DataAnalyser


class HttpDataAnalyser(DataAnalyser):

    __slots__ = (
        '_http_data',
        # '_df_tx',
        # '_df_rx',
        '_df_dataspeed',
    )

    def __init__(self, http_data: HttpData) -> None:
        super().__init__()
        self._http_data = http_data
        # self._df_tx: pandas.DataFrame = None
        # self._df_rx: pandas.DataFrame = None
        self._df_dataspeed: pandas.DataFrame = None

    def analyse(self) -> None:
        """
        .. note::
           Currently, no pass/fail criteria.
        """
        # Get the data
        df_tcp = self._http_data.df_tcp
        # self._df_tx = df_tcp[['TX Bytes']]
        # self._df_rx = df_tcp[['RX Bytes']]
        self._df_dataspeed = df_tcp[['AVG dataspeed']]
        avg_data_speed = self._http_data.avg_data_speed

        self._set_log(f'Average data speed: {avg_data_speed} Bytes/s')
        self._set_result(True)

    # @property
    # def df_tx(self) -> pandas.DataFrame:
    #     return self._df_tx

    # @property
    # def df_rx(self) -> pandas.DataFrame:
    #     return self._df_rx

    @property
    def df_dataspeed(self) -> pandas.DataFrame:
        return self._df_dataspeed
