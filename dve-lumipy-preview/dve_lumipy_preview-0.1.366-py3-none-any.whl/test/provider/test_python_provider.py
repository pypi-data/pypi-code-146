import datetime as dt
import os

import lumipy as lm
import lumipy.provider as lp
import numpy as np
import pandas as pd
from lumipy.test.provider.int_test_providers import (
    ParameterAndLimitTestProvider,
    TableParameterTestProvider,
    FilteringTestProvider,
    ColumnValidationTestProvider,
    IntSerialisationBugProvider,
    NothingProvider,
)
from lumipy.test.test_infra import BaseIntTestWithAtlas


class TestPythonProviderIntegration(BaseIntTestWithAtlas):

    manager = None
    df = None

    @classmethod
    def setUpClass(cls) -> None:

        cls.df = pd.DataFrame([
            {f'Col{k}': i * j for i, k in enumerate('ABCDEF')}
            for j in range(1000)
        ])

        providers = [
            lp.PandasProvider(cls.df, 'integration.test', description='This is a test dataframe'),
            FilteringTestProvider(),
            ParameterAndLimitTestProvider(),
            TableParameterTestProvider(),
            ColumnValidationTestProvider(),
            IntSerialisationBugProvider(),
            NothingProvider(),
        ]

        user = os.environ['LUMIPY_PROVIDER_TESTS_USER']
        domain = os.environ['LUMIPY_PROVIDER_TESTS_DOMAIN']

        cls.manager = lp.ProviderManager(
            *providers, user=user, domain=domain, port=5002,
        )
        cls.manager.start()

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.manager.stop()

    def _check_provider_attr_exists(self, attr_name):
        self.assertTrue(
            hasattr(self.atlas, attr_name),
            msg=f'The expected provider \'{attr_name}\' was not found in the atlas'
        )

    def test_pandas_provider(self):

        self._check_provider_attr_exists('pandas_integration_test')

        pit = self.atlas.pandas_integration_test()
        df = pit.select('*').go()

        self.assertSequenceEqual(df.shape, [1000, 6])
        self.assertTrue((self.df == df).all().all())

    def test_filter_pushdown(self):

        self._check_provider_attr_exists('test_pyprovider_filter')

        f = self.atlas.test_pyprovider_filter()
        df = f.select('*').where(f.node_id * 2 >= 0).go()

        self.assertSequenceEqual(df.shape, [5, 3])
        self.assertSequenceEqual(df.OpName.tolist(), ['Gte', 'Multiply', 'ColValue', 'NumValue', 'NumValue'])

    def test_parameters_and_limit(self):

        self._check_provider_attr_exists('test_pyprovider_paramsandlimit')

        para = self.atlas.test_pyprovider_paramsandlimit(param5=dt.date(2022, 1, 1))
        df = para.select('*').limit(100).go()
        self.assertSequenceEqual(df.shape, [7, 3])

        with self.assertRaises(ValueError) as ve:
            self.atlas.test_pyprovider_paramsandlimit().select('*').go()

    def test_table_parameters(self):

        self._check_provider_attr_exists('test_pyprovider_tablevar')

        def random_val(i):
            if i % 4 == 0:
                return np.random.uniform()
            elif i % 4 == 1:
                return np.random.choice(list('zyxwv'))
            elif i % 4 == 2:
                return dt.datetime(2020, 1, 1) + dt.timedelta(days=np.random.randint(0, 100))
            elif i % 4 == 3:
                return np.random.randint(100)

        tv_df = pd.DataFrame([
            {k: random_val(i) for i, k in enumerate('ABCDEF')}
            for _ in range(10)
        ])
        tv = lm.from_pandas(tv_df)
        t = self.atlas.test_pyprovider_tablevar(test_table=tv)

        df = t.select('*').go()

        self.assertSequenceEqual(df.shape, [6, 4])
        self.assertSequenceEqual(df.TableVarNumCols.tolist(), [6] * df.shape[0])
        self.assertSequenceEqual(df.TableVarNumRows.tolist(), [10] * df.shape[0])
        self.assertSequenceEqual(
            df.TableVarColType.tolist(),
            ['float64', 'string', 'datetime64[ns]', 'Int64', 'float64', 'string']
        )
        self.assertSequenceEqual(df.TableVarColName.tolist(), list('ABCDEF'))

    def test_output_dataframe_validation(self):

        self._check_provider_attr_exists('test_pyprovider_dataframe_validation')

        ok_cols = self.atlas.test_pyprovider_dataframe_validation(has_bad_cols=False)
        bad_cols = self.atlas.test_pyprovider_dataframe_validation(has_bad_cols=True)

        ok_df = ok_cols.select('*').go()
        self.assertSequenceEqual(ok_df.shape, [100, 5])

        with self.assertRaises(ValueError) as ve:
            bad_cols.select('*').go()

    def test_serialisation_bug(self):

        self._check_provider_attr_exists('test_pyprovider_deserialisation_bug')

        p = self.atlas.test_pyprovider_deserialisation_bug()
        df = p.select(p.int_value1).go()

        self.assertEqual(df.shape[1], 1)
        self.assertEqual(df[df.IntValue1.isna()].shape[0], 1)
        self.assertEqual(df[~df.IntValue1.isna()].shape[0], 8)

    def test_provider_returns_empty_table(self):

        self._check_provider_attr_exists('test_pyprovider_nothing')

        p = self.atlas.test_pyprovider_nothing()
        df = p.select('*').go()
        self.assertSequenceEqual(df.shape, [0, 2])
