import pandas as pd

from lumipy.atlas.utility_functions import (
    _query_data_provider_metadata,
    _query_direct_provider_metadata,
    _process_data_provider_metadata,
    _process_direct_provider_metadata,
)
from lumipy.test.test_infra import BaseIntTest


class AtlasBuildQueryTests(BaseIntTest):

    def test_client_atlas_query_data_providers_metadata(self):
        job = _query_data_provider_metadata(self.client)
        job.monitor()
        df = _process_data_provider_metadata(job.get_result())
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(df.shape[0], 0)
        self.assertEqual(df.shape[1], 14)

    def test_client_atlas_query_direct_providers_metadata(self):
        job = _query_direct_provider_metadata(self.client)
        job.monitor()
        df = _process_direct_provider_metadata(job.get_result())
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(df.shape[0], 0)
        self.assertEqual(df.shape[1], 10)
