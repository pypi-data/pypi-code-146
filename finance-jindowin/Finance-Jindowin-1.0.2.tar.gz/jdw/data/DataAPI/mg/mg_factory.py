# -*- coding: utf-8 -*-
class EngineFactory():

    def create_engine(self, engine_class):
        return engine_class()

    def __init__(self, engine_class=None):
        self._fetch_engine = self.create_engine(engine_class) \
            if engine_class is not None else None


class ShowFactor(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.show_factor()


class MarketFut(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.market_fut(table_name='market_fut', **kwargs)


class MarketPreFut(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.market_pre_fut(table_name='market_pre_fut',
                                                 **kwargs)


class FutFundamenal(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.fut_fundamenal(table_name='fut_fundamenal',
                                                 **kwargs)


class FutTFFundamenal(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.fut_tf_fundamentals(
            table_name='fut_tf_fundamentals', **kwargs)


class MarketIndexFut(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.market_index_fut(
            table_name='market_index_fut', **kwargs)


class ContractStruct(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.contract_struct(table_name='contract_struct',
                                                  **kwargs)


class Research(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.research(table_name='research', **kwargs)


class FutFactor(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.fut_factor(**kwargs)


class FutBasic(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.fut_basic(table_name='fut_basic', **kwargs)


class FutPortfolio(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.fut_portfolio(table_name='fut_portfolio',
                                                **kwargs)


class SelectedFutFactor(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.selected_fut_factor(
            table_name='selected_fut_factor', **kwargs)


class FactorsCategory(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.factors_category(**kwargs)


#### 股票相关
##### 基本面数据
class FinConsolidatedBalance(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.fin_consolidated_balance(
            table_name='fin_consolidated_balance', **kwargs)


class FinConsolidatedProfit(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.fin_consolidated_profit(
            table_name='fin_consolidated_profit', **kwargs)


class FinConsolidatedCashFlow(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.fin_consolidated_cashflow(
            table_name='fin_consolidated_cashflow', **kwargs)


class FinDerivation(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.fin_derivation(table_name='fin_derivation',
                                                 **kwargs)


##### 北上资金
class HKshszHoldFactory(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.hkshsz_hold(table_name='hkshsz_hold',
                                              **kwargs)


##### 行情数据
class IndexMarketFactory(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.index_market(table_name='index_market',
                                               code_name='codes',
                                               indexs_name='indexCode',
                                               time_name='trade_date',
                                               **kwargs)


class MarketEquFlowOrder(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.market_equflow_order(
            table_name='market_equflow_order',
            code_name='codes',
            indexs_name='code',
            time_name='trade_date',
            **kwargs)


class MarketBeforeFactory(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.market(table_name='market_adj_before',
                                         **kwargs)


class Market(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.market(table_name='market_adj_before',
                                         **kwargs)


##### 基础数据
class MarketFlowFactory(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.market(table_name='market_equ_flow',
                                         **kwargs)


class IndexConstituentFactory(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.index_components(
            table_name='index_components',
            code_name='codes',
            indexs_name='indexCode',
            time_name='trade_date',
            **kwargs)


class IndustryConstituentFactory(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.industry(table_name='industry', **kwargs)


class InstState(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.inst_state(table_name='inst_state',
                                             code_name='codes',
                                             indexs_name='code',
                                             time_name='effDate',
                                             **kwargs)


##### 风险模型数据
class ExposureFactory(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.risk_exposure(table_name='risk_exposure',
                                                **kwargs)


class RiskExposure(EngineFactory):

    def result(self, **kwargs):
        return self._fetch_engine.risk_exposure(table_name='risk_exposure',
                                                **kwargs)
