import pandas

from .data_store import DataStore


class HttpData(DataStore):

    __slots__ = (
        '_df_tcp',
        '_avg_data_speed',
    )

    def __init__(self) -> None:
        self._df_tcp = pandas.DataFrame(columns=[
            # 'TX Bytes',
            # 'RX Bytes',
            'AVG dataspeed',
        ])
        self._avg_data_speed: float = None

    @property
    def df_tcp(self) -> pandas.DataFrame:
        """TCP result history."""
        return self._df_tcp

    @property
    def avg_data_speed(self) -> float:
        """Average data speed in Bytes."""
        return self._avg_data_speed
