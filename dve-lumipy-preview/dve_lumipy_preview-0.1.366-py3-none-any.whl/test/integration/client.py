import time

import pandas as pd
from lumipy.query.query_job import QueryJob
from lumipy.test.test_infra import BaseIntTest


class ClientTests(BaseIntTest):

    def test_client_synchronous_query(self):
        df = self.client.query_and_fetch('select ^ from lusid.portfolio limit 10')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (10, 4))

    def test_client_background_query(self):
        sql_str = "select * from Sys.Field limit 100"
        ex_id = self.client.start_query(sql_str)
        self.assertIsInstance(ex_id, str)
        self.assertGreater(len(ex_id), 0)

        status = self.client.get_status(ex_id)
        while not status['status'] == 'RanToCompletion':
            status = self.client.get_status(ex_id)
            time.sleep(1)

        df = self.client.get_result(ex_id)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 100)

    def test_client_field_table_catalog(self):
        df = self.client.table_field_catalog()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(df.shape[0], 0)

    def test_client_run_synchronous(self):
        df = self.client.run('select ^ from lusid.portfolio limit 10')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (10, 4))

    def test_client_run_asynchronous(self):
        job = self.client.run('select ^ from lusid.portfolio limit 10', return_job=True)
        self.assertIsInstance(job, QueryJob)

        job.monitor()
        df = job.get_result()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (10, 4))

        log = job.get_progress()
        self.assertIsInstance(log, str)
        self.assertGreater(len(log), 0)

    def test_pandas_read_csv_passdown(self):
        sql_str = "select ^, 'N/A' as NA_TEST from Sys.Field limit 100"
        ex_id = self.client.start_query(sql_str)
        self.assertIsInstance(ex_id, str)
        self.assertGreater(len(ex_id), 0)

        status = self.client.get_status(ex_id)
        while not status['status'] == 'RanToCompletion':
            status = self.client.get_status(ex_id)
            time.sleep(1)

        # Keep N/A
        df = self.client.get_result(ex_id, keep_default_na=False, na_values=['NULL'])
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 100)
        self.assertEqual(df[~df.NA_TEST.isna()].shape[0], 100)

        # N/A as nan
        df = self.client.get_result(ex_id)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 100)
        self.assertEqual(df[~df.NA_TEST.isna()].shape[0], 0)
