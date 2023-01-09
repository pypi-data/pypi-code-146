from chipmunkdb.ChipmunkDb import ChipmunkDb

from coinlib.feature.CoinlibFeature import CoinlibFeature
from abc import abstractmethod

from coinlib.feature.FeatureDTO import FeatureData, ProcessResponse, FeatureFetcherDTO


class CoinlibFeatureFetcher(CoinlibFeature):

    def start_fetch_data(self, data: FeatureFetcherDTO) -> ProcessResponse:
        self.fetcher_info = data
        resp = self.loop.run_until_complete(self.fetch_data(data))
        if self.is_data_open():
            self.saveDataAfterWriteTimeout()
        return resp

    async def save_dataframe(self, df2, columns, databaseServer: str, databaseId: str):
        try:
            chipmunkDb = ChipmunkDb(self.registrar.get_chipmunkdb_host(self.fetcher_info["targetDatabase"]["chipmunkdbHost"]))
            chipmunkDb.save_as_pandas(df2, self.fetcher_info["targetDatabase"]["workspace_id"],
                                       mode="append")

            self.save_statistics(columns, df2.shape[0])
        except Exception as e:
            self.logger().error("ERror in saving data to dtaframe %s", str(e))
        return True

    @abstractmethod
    async def fetch_data(self, data: FeatureFetcherDTO) -> ProcessResponse:
        pass
