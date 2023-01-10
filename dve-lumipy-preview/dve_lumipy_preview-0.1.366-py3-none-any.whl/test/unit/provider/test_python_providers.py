import datetime as dt
import io
import time
import unittest

import pandas as pd
import pytz
import requests as r
from sklearn.datasets import load_iris, load_digits, load_diabetes

import lumipy.provider as lp
from lumipy.test.provider.int_test_providers import (
    TestLogAndErrorLines, ColumnValidationTestProvider, NothingProvider,
    TestErrorWhenNotReturningGenerator,
)
from lumipy.test.unit.utilities.test_utils import standardise_sql_string
from lumipy.typing.sql_value_type import SqlValType


def get_csv(url, params=None, throw_on_err=True):
    params = {} if params is None else params
    sess = r.Session()
    with sess.post(url, json=params) as res:
        res.raise_for_status()
        csv_str = '\n'.join(map(lambda x: x.decode('utf-8'), res.iter_lines()))
        sio = io.StringIO(csv_str)
        df = pd.read_csv(sio, header=None)

        err_df = df[df.iloc[:, -2] == 'error']
        if throw_on_err and err_df.shape[0] > 0:
            err = err_df.iloc[0, -1]
            raise ValueError(f'There was an error line in the data stream: {err}')

        return df


class TestLocalProviderInfra(unittest.TestCase):

    def setUp(self) -> None:

        def get_df_from_load_fn(load_fn):
            data = load_fn(as_frame=True)
            return pd.concat([data['data'], data['target']], axis=1)

        self.test_dfs = {
            "Test": pd.DataFrame([{"A": i, "B": i ** 2, "C": i ** 0.5} for i in range(25)]),
            "Iris": get_df_from_load_fn(load_iris),
            "Diabetes": get_df_from_load_fn(load_diabetes),
            "Digits": get_df_from_load_fn(load_digits),
        }

    def test_local_provider_creation(self):

        for name, df in self.test_dfs.items():

            prv = lp.PandasProvider(df, name)

            self.assertEqual(len(prv.parameters), 1)
            self.assertEqual(prv.name, f'Pandas.{name}')
            self.assertEqual(prv.path_name, f'pandas-{name.lower()}')
            self.assertEqual(prv.df.shape[0], df.shape[0])
            self.assertEqual(prv.df.shape[1], df.shape[1])
            self.assertEqual(len(prv.columns), df.shape[1])

            for c1, c2 in zip(sorted(prv.columns.keys()), sorted(df.columns)):
                col = prv.columns[c1]
                self.assertEqual(col.name, str(c2).replace('.', '_'))

    def test_manager_creation(self):

        providers = []
        for name, df in self.test_dfs.items():
            providers.append(lp.PandasProvider(df, name))

        manager = lp.ProviderManager(*providers)

        # Assert api server is constructed correctly
        prs = manager.api_server.provider_roots
        self.assertEqual(manager.api_server.host, '127.0.0.1')
        self.assertEqual(manager.api_server.port, 5001)

        for pr in prs:
            name = pr['Name']
            url = pr['ApiPath']
            self.assertEqual(
                url,
                f'http://{manager.api_server.host}:{manager.api_server.port}/api/v1/{name.replace(".", "-").lower()}/'
            )

    def test_manager_operation_bernoulli(self):

        # Tests that parameters can be supplied to a provider

        providers = [lp.BernoulliDistProvider()]

        host = 'localhost'
        port = 5004
        manager = lp.ProviderManager(*providers, dry_run=True, host=host, port=port)

        with manager:
            # Test index endpoint
            res = r.get(f'http://{host}:{port}/api/v1/index')
            res.raise_for_status()
            index_json = res.json()
            self.assertEqual(len(index_json), 1)

            # Test provider metadata endpoint
            pr = manager.api_server.provider_roots[0]
            p = manager.api_server.providers[0]

            res = r.get(pr['ApiPath'] + 'metadata')
            res.raise_for_status()
            meta_json = res.json()
            self.assertEqual(len(meta_json['Columns']), len(p.columns))
            self.assertEqual(len(meta_json['Params']), len(p.parameters))
            self.assertEqual(meta_json['Name'], p.name)
            self.assertEqual(meta_json['Description'], p.description)

            # Test provider data endpoint

            df = get_csv(
                pr['ApiPath'] + 'data',
                {'params': [
                    {'name': 'Probability', 'data_type': 'Double', 'value': 0.5},
                ]}
            )
            self.assertEqual(df.shape[0], 100)
            self.assertEqual(df.shape[1] - 2, len(p.columns))

            # Test that the manager has cleaned itself and its dependencies up
        with self.assertRaises(Exception) as e:
            res = r.get(f'http://{host}:{port}')
            res.raise_for_status()

    def test_manager_operation_pandas(self):

        time.sleep(3)

        providers = [lp.PandasProvider(df, name) for name, df in self.test_dfs.items()]

        host = 'localhost'
        port = 5006

        manager = lp.ProviderManager(*providers, dry_run=True, host=host, port=port)

        with manager:
            # Test index endpoint
            res = r.get(f'http://{host}:{port}/api/v1/index')
            res.raise_for_status()
            index_json = res.json()
            self.assertEqual(len(index_json), len(manager.api_server.provider_roots))

            for p, pr in zip(providers, manager.api_server.provider_roots):
                # Test provider metadata endpoint
                res = r.get(pr['ApiPath'] + 'metadata')
                res.raise_for_status()
                meta_json = res.json()
                self.assertEqual(len(meta_json['Columns']), len(p.columns))
                self.assertEqual(len(meta_json['Params']), len(p.parameters))
                self.assertEqual(meta_json['Name'], p.name)
                self.assertEqual(meta_json['Description'], p.description)

                # Test provider data endpoint
                df = get_csv(pr['ApiPath'] + 'data')
                ref_df = p.df
                self.assertSequenceEqual([df.shape[0], df.shape[1] - 2], ref_df.shape,
                                         msg=f'{p.name} result has the wrong shape: {df.shape} vs {ref_df.shape}')

                # Check you can call twice and nothing messes with the original DF
                df = get_csv(pr['ApiPath'] + 'data')
                self.assertSequenceEqual([df.shape[0], df.shape[1] - 2], p.df.shape,
                                         msg=f'{p.name} result has the wrong shape: {df.shape} vs {p.df.shape}')

        # Test that the manager has cleaned itself and its dependencies up
        with self.assertRaises(Exception) as e:
            res = r.get(f'http://{host}:{port}')
            res.raise_for_status()

    def test_pandas_provider_construction_with_datetimes(self):
        t = dt.datetime(2021, 7, 9)
        d = [{'A': k, 'T': t + dt.timedelta(days=i)} for i, k in enumerate('ABCDEFG')]
        df = pd.DataFrame(d)

        # non-tz-aware fails
        with self.assertRaises(ValueError) as ve:
            lp.PandasProvider(df, name='DatetimeTest')
            self.assertIn("Datetime values in pandas providers must be tz-aware", str(ve))
            self.assertIn("df['column'] = df['column'].dt.tz_localize(tz='utc')", str(ve))

        # tz-aware is fine and the col has the right type
        t = dt.datetime(2021, 7, 9, tzinfo=pytz.UTC)
        d = [{'A': k, 'T': t + dt.timedelta(days=i)} for i, k in enumerate('ABCDEFG')]
        df = pd.DataFrame(d)
        p = lp.PandasProvider(df, name='DatetimeTest')

        self.assertEqual(p.columns['A'].data_type, SqlValType.Text)
        self.assertEqual(p.columns['T'].data_type, SqlValType.DateTime)

    def test_manager_input_validation(self):

        time.sleep(3)

        prov = lp.PandasProvider(self.test_dfs['Test'], 'Testing')

        with self.assertRaises(ValueError) as ve:
            lp.ProviderManager(dry_run=True, host='${being mean}', port=5004)

        with self.assertRaises(ValueError) as ve:
            lp.ProviderManager(prov, dry_run=True, host='${being mean}', port=5004)

        with self.assertRaises(ValueError) as ve:
            lp.ProviderManager(prov, dry_run=True, host='localhost', port='${being mean}')

        with self.assertRaises(ValueError) as ve:
            lp.ProviderManager(prov, dry_run=True, host='localhost', port=5004, domain='${being mean}')

        with self.assertRaises(ValueError) as ve:
            lp.ProviderManager(prov, dry_run=True, host='localhost', port=5004, user='${being mean}')

    def test_setup_input_validation(self):

        with self.assertRaises(ValueError) as ve:
            lp.setup('/somewhere', version='${being mean}')

        with self.assertRaises(ValueError) as ve:
            lp.setup('/somewhere', verbosity='${being mean}')

    def test_runtime_error_handlingr(self):
        p = TestLogAndErrorLines()

        host = 'localhost'
        port = 5006
        manager = lp.ProviderManager(p, dry_run=True, host=host, port=port)

        with manager:
            # Test index endpoint
            res = r.get(f'http://{host}:{port}/api/v1/index')
            res.raise_for_status()
            index_json = res.json()
            self.assertEqual(len(index_json), len(manager.api_server.provider_roots))

            pr = manager.api_server.provider_roots[0]
            # Test provider metadata endpoint
            res = r.get(pr['ApiPath'] + 'metadata')
            res.raise_for_status()
            meta_json = res.json()
            self.assertEqual(len(meta_json['Columns']), len(p.columns))
            self.assertEqual(len(meta_json['Params']), len(p.parameters))
            self.assertEqual(meta_json['Name'], p.name)
            self.assertEqual(meta_json['Description'], p.description)

            # Test provider data endpoint
            df = get_csv(pr['ApiPath'] + 'data', throw_on_err=False)

            self.assertEqual(df.shape[0], 48)

            # Check there are the right number of log lines with the right message
            log_lines = df[df.iloc[:, -2] == 'info']
            for _, line in log_lines.iterrows():
                self.assertEqual("I'm a logging message!", line.values[-1])

            # Check last row has the error data
            err_row = df.iloc[-1, -2:].values
            self.assertEqual(err_row[0], 'error')
            self.assertIn('Test error has been triggered!', err_row[1])

    def test_bad_data_shape_from_get_data_raises_error(self):
        p = ColumnValidationTestProvider()

        host = 'localhost'
        port = 5006
        manager = lp.ProviderManager(p, dry_run=True, host=host, port=port)

        with manager:

            # Test provider data endpoint
            pr = manager.api_server.provider_roots[0]
            df = get_csv(
                pr['ApiPath'] + 'data',
                {'params': [{'name': 'HasBadCols', 'data_type': 'Boolean', 'value': 'true'}]},
                throw_on_err=False,
            )

            self.assertIn(
                standardise_sql_string('''
                ValueError: DataFrame column content from ColumnValidationTestProvider.get_data does not match provider spec.
                  Expected: Col0, Col1, Col2, Col3, Col4
                    Actual: Col0, Col1, Col2, Col3
                '''),
                standardise_sql_string(df.iloc[0, -1])
            )

    def test_provider_empty_row_method(self):

        p = NothingProvider()
        row = p.empty_row()
        self.assertSequenceEqual(row.shape, [0, 2])

        csvs = list(p._pipeline({'data_filter': None, 'limit': None, 'params': []}))
        self.assertEqual(0, len(csvs))

    def test_yield_vs_return_bug_resulting_in_empty_generator(self):

        p = TestLogAndErrorLines()

        # Errors
        yield_pipe = p._pipeline({
            'data_filter': None,
            'limit': None,
            'params': [
                {'name': 'yield_or_return', 'data_type': 'Text', 'value': 'yield'}
            ],
        })
        yield_df = pd.read_csv(io.StringIO(''.join(yield_pipe)), header=None)
        self.assertSequenceEqual(yield_df.shape, [48, 4])

        return_pipe = p._pipeline({
            'data_filter': None,
            'limit': None,
            'params': [
                {'name': 'yield_or_return', 'data_type': 'Text', 'value': 'return'}
            ],
        })
        return_df = pd.read_csv(io.StringIO(''.join(return_pipe)), header=None)
        self.assertSequenceEqual(return_df.shape, [1, 4])

        # No Errors
        yield_pipe = p._pipeline({
            'data_filter': None,
            'limit': 10,
            'params': [
                {'name': 'yield_or_return', 'data_type': 'Text', 'value': 'yield'}
            ],
        })
        yield_df = pd.read_csv(io.StringIO(''.join(yield_pipe)), header=None)
        self.assertSequenceEqual(yield_df.shape, [11, 4])

        return_pipe = p._pipeline({
            'data_filter': None,
            'limit': 10,
            'params': [
                {'name': 'yield_or_return', 'data_type': 'Text', 'value': 'return'}
            ],
        })
        return_df = pd.read_csv(io.StringIO(''.join(return_pipe)), header=None)
        self.assertSequenceEqual(return_df.shape, [1, 4])
        self.assertIn(
            'Generator from TestLogAndErrorLines.get_data did not yield any results!',
            return_df.iloc[0, -1],
        )

    def test_error_handling_when_not_returning_generator(self):

        p = TestErrorWhenNotReturningGenerator()

        csvs = ''.join(p._pipeline({'data_filter': None, 'limit': None}))
        df = pd.read_csv(io.StringIO(csvs), header=None)
        err = df.iloc[0, -1]
        self.assertIn('This is a test error!', err)

    def test_error_during_params_parsing_step_is_handled(self):

        p = lp.PandasProvider(self.test_dfs['Iris'], 'iris')
        csvs = p._pipeline({
            'data_filter': None,
            'limit': None,
            'params': [
                {'name': 'UsePandasFilter', 'value': 'NOT_VALID', 'data_type': 'Boolean'}
            ],
        })

        df = pd.read_csv(io.StringIO(''.join(csvs)), header=None)
        err = df.iloc[0, -1]
        self.assertIn("ValueError: invalid truth value 'not_valid'", err)
