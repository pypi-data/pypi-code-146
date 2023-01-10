import datetime as dt
from typing import Optional, Dict, Union

from pandas import DataFrame

from lumipy.provider.base_provider import BaseProvider
from lumipy.provider.metadata import ColumnMeta, ParamMeta, TableParam
from lumipy.typing.sql_value_type import SqlValType


class CreatePortfolioTestData(BaseProvider):

    """Create portfolio test data

    """

    def __init__(self):

        columns = [
            ColumnMeta('PortfolioScope', SqlValType.Text),
            ColumnMeta('BaseCurrency', SqlValType.Text),
            ColumnMeta('PortfolioCode', SqlValType.Text),
            ColumnMeta('PortfolioType', SqlValType.Text),
            ColumnMeta('DisplayName', SqlValType.Text),
            ColumnMeta('Description', SqlValType.Text),
            ColumnMeta('Created', SqlValType.DateTime),
            ColumnMeta('SubHoldingKeys', SqlValType.Text),
        ]

        params = [
            ParamMeta('Scope', SqlValType.Text, is_required=True),
        ]

        super().__init__(
            'Lab.TestData.Lusid.Portfolio',
            columns,
            params,
            description=self.__doc__
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        if limit is None:
            raise ValueError("You must apply a limit to this table.")

        return DataFrame(
            {
                'PortfolioScope': params['Scope'],
                'BaseCurrency': 'GBP',
                'PortfolioCode': f'lumi-test-pf-{i}',
                'PortfolioType': 'Transaction',
                'DisplayName': f'lumi-test-pf-{i}',
                'Description': f'perf test portfolio',
                'Created': dt.datetime(2010, 1, 1),
                'SubHoldingKeys': '',
            }
            for i in range(limit)
        )


class CreateInstrumentTestData(BaseProvider):

    def __init__(self):

        columns = [
            ColumnMeta('DisplayName', SqlValType.Text),
            ColumnMeta('ClientInternal', SqlValType.Text),
            ColumnMeta('DomCcy', SqlValType.Text),
        ]
        super().__init__(
            'Lab.TestData.Lusid.Instrument',
            columns,
            description=self.__doc__
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        if limit is None:
            raise ValueError("You must apply a limit to this table.")

        return DataFrame(
            {
                'DisplayName': f'Test Instrument {i}',
                'ClientInternal': f'lumi-test-instrument-{i}',
                'DomCcy': 'USD',
            }
            for i in range(limit)
        )


class CreateTransactionTestData(BaseProvider):

    def __init__(self):

        columns = [
            ColumnMeta('PortfolioScope', SqlValType.Text),
            ColumnMeta('PortfolioCode', SqlValType.Text),
            ColumnMeta('TxnId', SqlValType.Text),
            ColumnMeta('LusidInstrumentId', SqlValType.Text),
            ColumnMeta('Type', SqlValType.Text),
            ColumnMeta('Status', SqlValType.Text),
            ColumnMeta('SettlementDate', SqlValType.DateTime),
            ColumnMeta('TransactionDate', SqlValType.DateTime),
            ColumnMeta('Units', SqlValType.Int),
            ColumnMeta('SettlementCurrency', SqlValType.Text),
            ColumnMeta('TransactionPrice', SqlValType.Int),
        ]

        params = [
            ParamMeta('Scope', SqlValType.Text, is_required=True),
            ParamMeta('NumPortfolios', SqlValType.Int, is_required=True),
            ParamMeta('InstrumentsPerPortfolio', SqlValType.Int, is_required=True),
            ParamMeta('TxnsPerInstrument', SqlValType.Int, is_required=True),
        ]

        table_params = [TableParam("Luids")]

        super().__init__(
            'Lab.TestData.Lusid.Transaction',
            columns=columns,
            parameters=params,
            table_parameters=table_params,
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        scope = params.get('Scope')
        n_pf = params.get('NumPortfolios')
        n_inst = params.get('InstrumentsPerPortfolio')
        n_txn_per_inst = params.get('TxnsPerInstrument')

        luids = params.get('Luids').LusidInstrumentId.tolist()

        def make_rows():
            for pf_i in range(n_pf):
                count = 0
                for in_i in range(n_inst):
                    for tx_i in range(n_txn_per_inst):
                        yield {
                            'PortfolioScope': scope,
                            'PortfolioCode': f'lumi-test-pf-{pf_i}',
                            'TxnId': f'lumi-test-trade-{count}',
                            'LusidInstrumentId': luids[in_i],
                            'Type': 'Buy',
                            'Status': 'Active',
                            'SettlementDate': dt.datetime(2010, 1, 2) + dt.timedelta(hours=tx_i),
                            'TransactionDate': dt.datetime(2010, 1, 2) + dt.timedelta(hours=tx_i),
                            'Units': 100 * (1 + tx_i % 10),
                            'SettlementCurrency': 'GBP',
                            'TransactionPrice': 100,
                        }
                        count += 1

        return DataFrame(make_rows())


class CreateHoldingTestData(BaseProvider):

    def __init__(self):

        columns = [
            ColumnMeta('PortfolioScope', SqlValType.Text),
            ColumnMeta('PortfolioCode', SqlValType.Text),
            ColumnMeta('LusidInstrumentId', SqlValType.Text),
            ColumnMeta('HoldingType', SqlValType.Text),
            ColumnMeta('Units', SqlValType.Int),
            ColumnMeta('EffectiveAt', SqlValType.DateTime),
            ColumnMeta('CostCurrency', SqlValType.Text),
        ]
        params = [
            ParamMeta('Scope', SqlValType.Text, is_required=True),
            ParamMeta('NumPortfolios', SqlValType.Int, is_required=True),
            ParamMeta('InstrumentsPerPortfolio', SqlValType.Int, is_required=True),
            ParamMeta('EffectiveAtsPerInstrument', SqlValType.Int, is_required=True)
        ]
        table_params = [TableParam("Luids")]

        super().__init__(
            'Lab.TestData.Lusid.Holding',
            columns=columns,
            parameters=params,
            table_parameters=table_params,
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        scope = params.get('Scope')
        luids = params.get('Luids').LusidInstrumentId.tolist()
        n_pf = params.get('NumPortfolios')
        n_inst = params.get('InstrumentsPerPortfolio')
        n_eff_at_per_inst = params.get('EffectiveAtsPerInstrument')

        def make_rows():
            for pf_i in range(n_pf):
                for in_i in range(n_inst):
                    for ea_i in range(n_eff_at_per_inst):
                        yield {
                            'PortfolioScope': scope,
                            'PortfolioCode': f'lumi-test-pf-{pf_i}',
                            'LusidInstrumentId': luids[in_i],
                            'HoldingType': 'Position',
                            'Units': 100 * (1 + ea_i % 10),
                            'EffectiveAt': dt.datetime(2010, 1, 1) + dt.timedelta(hours=ea_i),
                            'CostCurrency': 'GBP',
                        }

        return DataFrame(make_rows())
