from pandas import DataFrame


class PredictabilityBean:

    def __init__(
            self,
            df_historical: DataFrame,
            df_by_measure: DataFrame,
            df_by_key: DataFrame,
    ):
        self._df_historical = df_historical
        self._df_by_measure = df_by_measure
        self._df_by_key = df_by_key

    @property
    def df_historical(self) -> DataFrame:
        return self._df_historical

    @property
    def df_by_measure(self) -> DataFrame:
        return self._df_by_measure

    @property
    def df_by_key(self) -> DataFrame:
        return self._df_by_key



# class PredictabilityBeanLegacy:
#
#     def __init__(
#             self,
#             df_by_measure: DataFrame,
#             df_by_period: DataFrame,
#             df_by_key: DataFrame,
#     ):
#         self._df_by_measure = df_by_measure
#         self._df_by_period = df_by_period
#         self._df_by_key = df_by_key
#
#     @property
#     def df_by_measure(self) -> DataFrame:
#         return self._df_by_measure
#
#     @property
#     def df_by_period(self) -> DataFrame:
#         return self._df_by_period
#
#     @property
#     def df_by_key(self) -> DataFrame:
#         return self._df_by_key
