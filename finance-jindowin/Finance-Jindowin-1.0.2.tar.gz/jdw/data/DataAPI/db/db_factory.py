# -*- coding: utf-8 -*-

import pdb
import pandas as pd
from sqlalchemy import create_engine, select, and_, or_
from sqlalchemy import outerjoin, join
from sqlalchemy.sql.selectable import Join
from jdw.kdutils.logger import kd_logger


class JoinTable(object):

    def __init__(self,
                 base_table,
                 left_table,
                 right_table,
                 on,
                 how,
                 on_conds=None):
        self._base_table = base_table
        self._left_table = left_table
        self._right_table = right_table
        self._on = on
        self._join_func = outerjoin if how != 'inner' else join
        self._on_conds = on_conds or []

    def bigtable(self):
        ## fixed 校验是否是索引
        conds = and_(self._left_table.flag == 1, self._right_table.flag == 1)
        if self._on:
            conds.append(self._left_table.__dict__[self._on] ==
                         self._right_table.__dict__[self._on])
        for c in self._on_conds:
            conds.append(c)

        base_table = self._base_table if self._base_table is not None else self._left_table
        return self._join_func(base_table, self._right_table, conds)


class EngineFactory():

    __name__ = None

    def create_engine(self, engine_class):
        return engine_class()

    def __init__(self, engine_class):
        self._fetch_engine = self.create_engine(engine_class)

    def name(self):
        return self._fetch_engine.name(self.__name__)

    def bigtable(self,
                 base_table,
                 left_table,
                 right_table,
                 on,
                 how,
                 on_conds=None):
        bigttable = JoinTable(base_table=base_table,
                              left_table=left_table,
                              right_table=right_table,
                              on=on,
                              how=how,
                              on_conds=on_conds).bigtable()
        return bigttable

    def join(self, big_table, clause_list, columns):

        def all_table(big_table, table_res):
            if isinstance(big_table, Join):
                all_table(big_table.left, table_res)
                table_res[big_table.right.name] = big_table.right
            else:
                table_res[big_table.name] = big_table

        table_res = {}
        all_table(big_table=big_table, table_res=table_res)
        table_list = list(table_res.values())
        new_list = and_(table_list[0].columns.flag == 1,
                        table_list[0].columns.flag.isnot(None))
        for d in table_list[1:]:
            new_list.append(d.columns.flag == 1)
            new_list.append(d.columns.flag.isnot(None))

        for clause in clause_list:
            indices = self._fetch_engine.show_indexs(clause.left.table.name)
            if clause.left.name in indices:
                new_list.append(clause)
            else:
                kd_logger.warning("{0} not indices".format(clause.left.name))
                raise ("{0} not indices".format(clause.left.name))

        return self._fetch_engine.join(big_table=big_table,
                                       clause_list=new_list,
                                       columns=columns)

    def custom(self, clause_list, columns=None, method='and'):
        table = self._fetch_engine.name(self.__name__)
        operator = and_ if method == 'and' else or_
        new_list = operator(table.__dict__['flag'] == 1,
                            table.__dict__['flag'].isnot(None))
        indices = self._fetch_engine.show_indexs(self.__name__)
        for clause in clause_list:
            if clause.left.name in indices:
                new_list.append(clause)
            else:
                kd_logger.warning("{0} not indices".format(clause.left.name))
                raise ("{0} not indices".format(clause.left.name))
        if len(new_list) <= 2:
            kd_logger.error("unconditional query is not allowed")
            return pd.DataFrame()
        return self._fetch_engine.custom(table=table,
                                         clause_list=new_list,
                                         columns=columns)


class ShowColumnsFactory(EngineFactory):

    def result(self, name):
        return self._fetch_engine.show_cloumns(name=name)


class JoinFactory(EngineFactory):

    def name(self, name=None):
        return self._fetch_engine.name(name)


class CustomizeFactory(EngineFactory):

    def name(self, name=None):
        return self._fetch_engine.name(name)

    def custom(self, clause_list, name, columns=None, method='and'):
        table = self._fetch_engine.name(name)
        new_list = and_(table.__dict__['flag'] == 1,
                        table.__dict__['flag'].isnot(None))
        indices = self._fetch_engine.show_indexs(name)
        for clause in clause_list:
            if clause.left.name in indices:
                new_list.append(clause)
            else:
                kd_logger.warning("{0} not indices".format(clause.left.name))
        if len(new_list) <= 2:
            kd_logger.error("unconditional query is not allowed")
            return pd.DataFrame()
        return self._fetch_engine.custom(table=table,
                                         clause_list=new_list,
                                         columns=columns)


#### 期货相关接口
class FutBasicFactory(EngineFactory):

    __name__ = 'fut_basic'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               date_key='firstDeliDate'):
        return self._fetch_engine.fut_basic(codes=codes,
                                            key=key,
                                            begin_date=begin_date,
                                            end_date=end_date,
                                            columns=columns,
                                            date_key=date_key)


class SpotdMarketFactory(EngineFactory):

    __name__ = 'spotd_basic'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.spotd_market(codes=codes,
                                               key=key,
                                               begin_date=begin_date,
                                               end_date=end_date,
                                               columns=columns,
                                               freq=freq,
                                               dates=dates)


class FuturesLongPositionsFactory(EngineFactory):
    __name__ = 'fut_long_positions'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fut_positions(codes=codes,
                                                key=key,
                                                types=1,
                                                begin_date=begin_date,
                                                end_date=end_date,
                                                columns=columns,
                                                freq=freq,
                                                dates=dates)


class FuturesShortPositionsFactory(EngineFactory):
    __name__ = 'fut_short_positions'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fut_positions(codes=codes,
                                                key=key,
                                                types=-1,
                                                begin_date=begin_date,
                                                end_date=end_date,
                                                columns=columns,
                                                freq=freq,
                                                dates=dates)


class FuturesPositionsFactory(EngineFactory):

    def result(self,
               codes,
               types,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fut_positions(codes=codes,
                                                key=key,
                                                types=types,
                                                begin_date=begin_date,
                                                end_date=end_date,
                                                columns=columns,
                                                freq=freq,
                                                dates=dates)


class ContractStructFactory(EngineFactory):
    __name__ = 'contract_struct'

    def result(self,
               codes,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.contract_struct(codes=codes,
                                                  key=key,
                                                  begin_date=begin_date,
                                                  end_date=end_date,
                                                  columns=columns)


class FuturesPortfolio(EngineFactory):

    def result(self,
               codes,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.fut_portfolio(codes=codes,
                                                key=key,
                                                columns=columns,
                                                begin_date=begin_date,
                                                end_date=end_date)


class SelFutFactorFactory(EngineFactory):
    __name__ = 'fut_portfolio'

    def result(self, codes, key=None, columns=None):
        return self._fetch_engine.sel_fut_factor(codes=codes,
                                                 key=key,
                                                 columns=columns)


class FuturesMarketFactory(EngineFactory):

    __name__ = 'market_fut'

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.futures_market(codes=codes,
                                                 key=key,
                                                 columns=columns,
                                                 begin_date=begin_date,
                                                 end_date=end_date)


class FutruesPreMarketFactory(EngineFactory):

    __name__ = 'market_pre_fut'

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.futures_pre_market(codes=codes,
                                                     key=key,
                                                     columns=columns,
                                                     begin_date=begin_date,
                                                     end_date=end_date)


class FutruesIndexMarketFactory(EngineFactory):

    __name__ = 'market_index_fut'

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.futures_index_market(codes=codes,
                                                       key=key,
                                                       columns=columns,
                                                       begin_date=begin_date,
                                                       end_date=end_date)


class FuturesFactorsFactory(EngineFactory):

    def result(self,
               codes=None,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.futures_factors(codes=codes,
                                                  key=key,
                                                  begin_date=begin_date,
                                                  end_date=end_date,
                                                  columns=columns,
                                                  freq=freq,
                                                  dates=dates)


class FutWareFactory(EngineFactory):

    __name__ = 'fut_ware'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fut_ware(codes=codes,
                                           key=key,
                                           begin_date=begin_date,
                                           end_date=end_date,
                                           columns=columns,
                                           freq=freq,
                                           dates=dates)


class FutFundamenalFactory(EngineFactory):

    __name__ = 'fut_fundamenal'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fut_fundamenal(codes=codes,
                                                 key=key,
                                                 begin_date=begin_date,
                                                 end_date=end_date,
                                                 columns=columns,
                                                 freq=freq,
                                                 dates=dates)


class FutTFFundamenalFactory(EngineFactory):

    __name__ = 'fut_tf_fundamentals'

    def result(self,
               codes,
               key=None,
               values=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fut_tf_fundamentals(codes=codes,
                                                      key=key,
                                                      values=values,
                                                      begin_date=begin_date,
                                                      end_date=end_date,
                                                      columns=columns,
                                                      freq=freq,
                                                      dates=dates)


class SpotdBasicFactory(EngineFactory):

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.spotd_market(codes=codes,
                                               key=key,
                                               begin_date=begin_date,
                                               end_date=end_date,
                                               columns=columns,
                                               freq=freq,
                                               dates=dates)


#### 股票相关
##### 基本面数据


class FinAvgSale(EngineFactory):

    __name__ = 'fin_avg_sale'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(table_name='fin_avg_sale',
                                              codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class FinQDerived(EngineFactory):

    __name__ = 'fin_qderived'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(table_name='fin_qderived',
                                              codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class FinDupont(EngineFactory):

    __name__ = 'fin_dupont'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(table_name='fin_dupont',
                                              codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class FinMainltData(EngineFactory):

    __name__ = 'fin_mainltdata'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(table_name='fin_mainltdata',
                                              codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class FinConsolidatedBalance(EngineFactory):
    __name__ = 'fin_consolidated_balance'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(
            table_name='fin_consolidated_balance',
            codes=codes,
            key=key,
            begin_date=begin_date,
            end_date=end_date,
            columns=columns,
            freq=freq,
            dates=dates)


class FinConsolidatedProfit(EngineFactory):
    __name__ = 'fin_consolidated_profit'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(
            table_name='fin_consolidated_profit',
            codes=codes,
            key=key,
            begin_date=begin_date,
            end_date=end_date,
            columns=columns,
            freq=freq,
            dates=dates)


class FinConsolidatedCashFlow(EngineFactory):
    __name__ = 'fin_consolidated_cashflow'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(
            table_name='fin_consolidated_cashflow',
            codes=codes,
            key=key,
            begin_date=begin_date,
            end_date=end_date,
            columns=columns,
            freq=freq,
            dates=dates)


class FinDerivation(EngineFactory):
    __name__ = 'fin_derivation'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(table_name='fin_derivation',
                                              codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class FinMainData(EngineFactory):
    __name__ = 'fin_maindata'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(table_name='fin_maindata',
                                              codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class FinCF2018(EngineFactory):
    __name__ = 'fin_cf2018'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(table_name='fin_cf2018',
                                              codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class FinCFLT2018(EngineFactory):
    __name__ = 'fin_cflt2018'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(table_name='fin_cflt2018',
                                              codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class FinBS2018(EngineFactory):
    __name__ = 'fin_bs2018'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(table_name='fin_bs2018',
                                              codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class FinBSLT2018(EngineFactory):
    __name__ = 'fin_bslt2018'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(table_name='fin_bslt2018',
                                              codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class FinIS2018(EngineFactory):
    __name__ = 'fin_is2018'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(table_name='fin_is2018',
                                              codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class FinISLT2018(EngineFactory):
    __name__ = 'fin_islt2018'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(table_name='fin_islt2018',
                                              codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class FinExpress(EngineFactory):
    __name__ = 'fin_express'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(table_name='fin_express',
                                              codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class FinForecast(EngineFactory):
    __name__ = 'fin_forecast'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(table_name='fin_forecast',
                                              codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class FinMainoper(EngineFactory):
    __name__ = 'fin_mainoper'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(table_name='fin_mainoper',
                                              codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class FinCFS(EngineFactory):
    __name__ = 'fin_cfs'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(table_name='fin_cfs',
                                              codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class FinAdminEXP(EngineFactory):
    __name__ = 'fin_adminexp'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.fin_default(table_name='fin_adminexp',
                                              codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


### 北上资金
class CCASSFactory(EngineFactory):
    __name__ = 'ccass'

    def result(self, codes=None, key=None, columns=None):
        return self._fetch_engine.ccass(codes=codes, key=key, columns=columns)


class HKshszDetlFactory(EngineFactory):
    __name__ = 'hkshsz_detl'

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.hkshsz_detl(codes=codes,
                                              key=key,
                                              columns=columns,
                                              begin_date=begin_date,
                                              end_date=end_date)


class HKshszHoldFactory(EngineFactory):

    def result(self,
               codes=None,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.hkshsz_hold(codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


##### 行情数据


class IndexMarketFactory(EngineFactory):
    __name__ = 'index_market'

    def result(self,
               codes,
               key,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.index_market(codes=codes,
                                               key=key,
                                               begin_date=begin_date,
                                               end_date=end_date,
                                               columns=columns,
                                               freq=freq,
                                               dates=dates)


class MarketRankStocksFactory(EngineFactory):

    __name__ = 'market_rank_stocks'

    def result(self,
               codes=None,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.market_rank_stocks(codes=codes,
                                                     key=key,
                                                     begin_date=begin_date,
                                                     end_date=end_date,
                                                     columns=columns,
                                                     freq=freq,
                                                     dates=dates)


class MarketRankSalesFactory(EngineFactory):
    __name__ = 'market_rank_sales'

    def result(self,
               codes=None,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.market_rank_sales(codes=codes,
                                                    key=key,
                                                    begin_date=begin_date,
                                                    end_date=end_date,
                                                    columns=columns,
                                                    freq=freq,
                                                    dates=dates)


class MarketEquFlowOrder(EngineFactory):

    __name__ = 'market_equflow_order'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.market_equflow_order(codes=codes,
                                                       key=key,
                                                       begin_date=begin_date,
                                                       end_date=end_date,
                                                       columns=columns,
                                                       freq=freq,
                                                       dates=dates)


class MarketFactory(EngineFactory):

    __name__ = 'market_stock'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.market(codes=codes,
                                         key=key,
                                         begin_date=begin_date,
                                         end_date=end_date,
                                         columns=columns,
                                         freq=freq,
                                         dates=dates)


class MarketStockFactory(EngineFactory):
    __name__ = 'market_stock'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.market_stock(codes=codes,
                                               key=key,
                                               begin_date=begin_date,
                                               end_date=end_date,
                                               columns=columns,
                                               freq=freq,
                                               dates=dates)


class MarketBeforeFactory(EngineFactory):
    __name__ = 'market_adj_before'

    def result(self,
               codes=None,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.market_before(codes=codes,
                                                key=key,
                                                begin_date=begin_date,
                                                end_date=end_date,
                                                columns=columns,
                                                freq=freq,
                                                dates=dates)


class MarketFlowFactory(EngineFactory):
    __name__ = 'market_equ_flow'

    def result(self,
               codes=None,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.market_flow(codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class PositionFeatureFactory(EngineFactory):
    __name__ = 'market_position_feature'

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.position_feature(codes=codes,
                                                   key=key,
                                                   columns=columns,
                                                   begin_date=begin_date,
                                                   end_date=end_date)


##### 一致预期


class ResReportForeStock(EngineFactory):
    __name__ = 'res_report_forestock'

    def result(self,
               codes=None,
               key='infoStockID',
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.res_report_forestock(codes=codes,
                                                       key=key,
                                                       begin_date=begin_date,
                                                       end_date=end_date,
                                                       columns=columns,
                                                       freq=freq,
                                                       dates=dates)


##### 基础数据


class InternalCodesFactory(EngineFactory):

    def result(self, codes, keys, types='101', columns=None):
        return self._fetch_engine.gl_internal_codes(codes=codes,
                                                    keys=keys,
                                                    types=types,
                                                    columns=columns)


1


class ClassifyConstituent(EngineFactory):

    def result(self, industry=None, codes=None, key=None, columns=None):
        return self._fetch_engine.classify_constituent(industry=industry,
                                                       codes=codes,
                                                       key=key,
                                                       columns=columns)


class SecurityMasterFactory(EngineFactory):
    __name__ = 'security_master'

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.security_master(codes=codes,
                                                  key=key,
                                                  columns=columns,
                                                  begin_date=begin_date,
                                                  end_date=end_date)


class IndustryConstituentFactory(EngineFactory):

    __name__ = 'industry'

    def result(self,
               codes,
               category,
               key,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.industry_constituent(codes=codes,
                                                       category=category,
                                                       key=key,
                                                       begin_date=begin_date,
                                                       end_date=end_date,
                                                       columns=columns,
                                                       freq=freq,
                                                       dates=dates)


class IndexConstituentFactory(EngineFactory):

    __name__ = 'index_components'

    def result(self,
               category,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.index_constituent(category=category,
                                                    key=key,
                                                    begin_date=begin_date,
                                                    end_date=end_date,
                                                    columns=columns,
                                                    freq=freq,
                                                    dates=dates)


class CapitalSalesFactory(EngineFactory):
    __name__ = 'sales_info'

    def result(self, key=None, columns=None):
        return self._fetch_engine.capital_sales(key=key, columns=columns)


class InstState(EngineFactory):

    __name__ = 'inst_state'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.inst_state(codes=codes,
                                             key=key,
                                             begin_date=begin_date,
                                             end_date=end_date,
                                             columns=columns,
                                             freq=freq,
                                             dates=dates)


class StockFactorsFactory(EngineFactory):

    def result(self,
               codes=None,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.stock_factors(codes=codes,
                                                key=key,
                                                begin_date=begin_date,
                                                end_date=end_date,
                                                columns=columns,
                                                freq=freq,
                                                dates=dates)


class FactorsCategory(EngineFactory):

    def result(self, factors):
        return self._fetch_engine.factors_category(factors=factors)


##### 风险模型数据


class RiskCovDayFactory(EngineFactory):
    __name__ = 'risk_cov_day'

    def result(self,
               factors,
               category,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.risk_cov(factors=factors,
                                           category='day',
                                           begin_date=begin_date,
                                           end_date=end_date,
                                           columns=columns,
                                           freq=freq,
                                           dates=dates)


class RiskCovLongFactory(EngineFactory):
    __name__ = 'risk_cov_long'

    def result(self,
               factors,
               category,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.risk_cov(factors=factors,
                                           category='long',
                                           begin_date=begin_date,
                                           end_date=end_date,
                                           columns=columns,
                                           freq=freq,
                                           dates=dates)


class RiskCovShortFactory(EngineFactory):
    __name__ = 'risk_cov_short'

    def result(self,
               factors,
               category,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.risk_cov(factors=factors,
                                           category='short',
                                           begin_date=begin_date,
                                           end_date=end_date,
                                           columns=columns,
                                           freq=freq,
                                           dates=dates)


class RiskCovFactory(EngineFactory):

    def result(self,
               factors,
               category,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.risk_cov(factors=factors,
                                           category=category,
                                           begin_date=begin_date,
                                           end_date=end_date,
                                           columns=columns,
                                           freq=freq,
                                           dates=dates)


class RiskSpecial(EngineFactory):
    __name__ = 'risk_special'

    def result(self,
               codes,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.risk_special(codes=codes,
                                               begin_date=begin_date,
                                               end_date=end_date,
                                               columns=columns,
                                               freq=freq,
                                               dates=dates)


class RiskReturnFactory(EngineFactory):
    __name__ = 'risk_return'

    def result(self,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.risk_return(begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class SpecificReturnFactory(EngineFactory):

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.specific_return(codes=codes,
                                                  key=key,
                                                  begin_date=begin_date,
                                                  end_date=end_date,
                                                  columns=columns,
                                                  freq=freq,
                                                  dates=dates)


class ExposureFactory(EngineFactory):
    __name__ = 'risk_exposure'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.exposure(codes=codes,
                                           key=key,
                                           begin_date=begin_date,
                                           end_date=end_date,
                                           columns=columns,
                                           freq=freq,
                                           dates=dates)


#### 可转债数据
class MarketBondFactory(EngineFactory):
    __name__ = 'market_bond'

    def result(self,
               codes=None,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.market_bond(codes=codes,
                                              key=key,
                                              begin_date=begin_date,
                                              end_date=end_date,
                                              columns=columns,
                                              freq=freq,
                                              dates=dates)


class MarketBondPremiumFactory(EngineFactory):
    __name__ = 'market_bond_premium'

    def result(self,
               codes=None,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.market_bond_premium(codes=codes,
                                                      key=key,
                                                      begin_date=begin_date,
                                                      end_date=end_date,
                                                      columns=columns,
                                                      freq=freq,
                                                      dates=dates)


class BondConvDerivedFactory(EngineFactory):
    __name__ = 'bond_conv_derived'

    def result(self,
               codes=None,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.bond_conv_derived(codes=codes,
                                                    key=key,
                                                    begin_date=begin_date,
                                                    end_date=end_date,
                                                    columns=columns,
                                                    freq=freq,
                                                    dates=dates)


class BondConvChgFactory(EngineFactory):
    __name__ = 'bond_conv_chg'

    def result(self,
               codes=None,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.bond_conv_chg(codes=codes,
                                                key=key,
                                                begin_date=begin_date,
                                                end_date=end_date,
                                                columns=columns,
                                                freq=freq,
                                                dates=dates)


class BondConvCallFactory(EngineFactory):
    __name__ = 'bond_conv_call'

    def result(self,
               codes=None,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               freq=None,
               dates=None):
        return self._fetch_engine.bond_conv_call(codes=codes,
                                                 key=key,
                                                 begin_date=begin_date,
                                                 end_date=end_date,
                                                 columns=columns,
                                                 freq=freq,
                                                 dates=dates)


class BondConvBasicFactory(EngineFactory):
    __name__ = 'bond_conv_basic'

    def result(self,
               codes,
               key=None,
               begin_date=None,
               end_date=None,
               columns=None,
               date_key='firstDeliDate'):
        return self._fetch_engine.bond_conv_basic(codes=codes,
                                                  key=key,
                                                  begin_date=begin_date,
                                                  end_date=end_date,
                                                  columns=columns,
                                                  date_key=date_key)


class BondConvStock(EngineFactory):
    __name__ = 'bond_conv_stock'


#### 舆情事件
class BlockFuzzyInfo(EngineFactory):

    def result(self, key='block_name', words=None, columns=None):
        return self._fetch_engine.block_fuzzy_info(key=key,
                                                   words=words,
                                                   columns=columns)


class BigEventFactory(EngineFactory):

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.market_big_event(codes=codes,
                                                   key=key,
                                                   columns=columns,
                                                   begin_date=begin_date,
                                                   end_date=end_date)


class EventMembersFactory(EngineFactory):

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.market_event_members(codes=codes,
                                                       key=key,
                                                       columns=columns,
                                                       begin_date=begin_date,
                                                       end_date=end_date)


class EventTimelineFactory(EngineFactory):

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.market_event_timeline(codes=codes,
                                                        key=key,
                                                        columns=columns,
                                                        begin_date=begin_date,
                                                        end_date=end_date)


class BlockInfoFactory(EngineFactory):

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.block_info(codes=codes,
                                             key=key,
                                             columns=columns,
                                             begin_date=begin_date,
                                             end_date=end_date)


class BlockMemberFactory(EngineFactory):

    def result(self, codes=None, key=None, columns=None):
        return self._fetch_engine.block_member(codes=codes,
                                               key=key,
                                               columns=columns)


class BlockSinaInfoFactory(EngineFactory):

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.block_sina_info(codes=codes,
                                                  key=key,
                                                  columns=columns,
                                                  begin_date=begin_date,
                                                  end_date=end_date)


class BlockSinaMemberFactory(EngineFactory):

    def result(self, codes=None, key=None, columns=None):
        return self._fetch_engine.block_sina_member(codes=codes,
                                                    key=key,
                                                    columns=columns)


class BlockUqerInfoFactory(EngineFactory):

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.block_uqer_info(codes=codes,
                                                  key=key,
                                                  columns=columns,
                                                  begin_date=begin_date,
                                                  end_date=end_date)


class BlockUqerMemberFactory(EngineFactory):

    def result(self, codes=None, key=None, columns=None):
        return self._fetch_engine.block_uqer_member(codes=codes,
                                                    key=key,
                                                    columns=columns)


class BlockYCJInfoFactory(EngineFactory):

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.block_ycj_info(codes=codes,
                                                 key=key,
                                                 columns=columns,
                                                 begin_date=begin_date,
                                                 end_date=end_date)


class BlockYCJMemberFactory(EngineFactory):

    def result(self, codes=None, key=None, columns=None):
        return self._fetch_engine.block_ycj_member(codes=codes,
                                                   key=key,
                                                   columns=columns)


class BlockYCJFeedFactory(EngineFactory):

    def result(self, codes=None, key=None, columns=None):
        return self._fetch_engine.block_ycj_feed(codes=codes,
                                                 key=key,
                                                 columns=columns)


class BlockTHSInfoFactory(EngineFactory):

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.block_ths_info(codes=codes,
                                                 key=key,
                                                 columns=columns,
                                                 begin_date=begin_date,
                                                 end_date=end_date)


class BlockTHSMemberFactory(EngineFactory):

    def result(self, codes=None, key=None, columns=None):
        return self._fetch_engine.block_ths_member(codes=codes,
                                                   key=key,
                                                   columns=columns)


class BlockTHSFeedFactory(EngineFactory):

    def result(self, codes=None, key=None, columns=None):
        return self._fetch_engine.block_ths_feed(codes=codes,
                                                 key=key,
                                                 columns=columns)


class BlockWanDeInfoFactory(EngineFactory):

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.block_wande_info(codes=codes,
                                                   key=key,
                                                   columns=columns,
                                                   begin_date=begin_date,
                                                   end_date=end_date)


class BlockWanDeMemberFactory(EngineFactory):

    def result(self, codes=None, key=None, columns=None):
        return self._fetch_engine.block_wande_member(codes=codes,
                                                     key=key,
                                                     columns=columns)


class BlockWanDeFeedFactory(EngineFactory):

    def result(self, codes=None, key=None, columns=None):
        return self._fetch_engine.block_wande_feed(codes=codes,
                                                   key=key,
                                                   columns=columns)


class BlockSNSInfoFactory(EngineFactory):

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.block_snssdk_info(codes=codes,
                                                    key=key,
                                                    columns=columns,
                                                    begin_date=begin_date,
                                                    end_date=end_date)


class BlockSNSMemberFactory(EngineFactory):

    def result(self, codes=None, key=None, columns=None):
        return self._fetch_engine.block_snssdk_member(codes=codes,
                                                      key=key,
                                                      columns=columns)


class BlockSNSFeedFactory(EngineFactory):

    def result(self, codes=None, key=None, columns=None):
        return self._fetch_engine.block_snssdk_feed(codes=codes,
                                                    key=key,
                                                    columns=columns)


class BlockCLSMemberFactory(EngineFactory):

    def result(self, codes=None, key=None, columns=None):
        return self._fetch_engine.block_cls_member(codes=codes,
                                                   key=key,
                                                   columns=columns)


class BlockCLSInfoFactory(EngineFactory):

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.block_cls_info(codes=codes,
                                                 key=key,
                                                 columns=columns,
                                                 begin_date=begin_date,
                                                 end_date=end_date)


class BlockCLSFeedFactory(EngineFactory):

    def result(self, codes=None, key=None, columns=None):
        return self._fetch_engine.block_cls_feed(codes=codes,
                                                 key=key,
                                                 columns=columns)


class BlockCSC108InfoFactory(EngineFactory):

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.block_csc108_info(codes=codes,
                                                    key=key,
                                                    columns=columns,
                                                    begin_date=begin_date,
                                                    end_date=end_date)


class BlockCSC108MemberFactory(EngineFactory):

    def result(self, codes=None, key=None, columns=None):
        return self._fetch_engine.block_csc108_member(codes=codes,
                                                      key=key,
                                                      columns=columns)


class BlockCSC108FeedFactory(EngineFactory):

    def result(self, codes=None, key=None, columns=None):
        return self._fetch_engine.block_csc108_feed(codes=codes,
                                                    key=key,
                                                    columns=columns)


class BlockCustomInfoFactory(EngineFactory):

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.block_custom_info(codes=codes,
                                                    key=key,
                                                    columns=columns,
                                                    begin_date=begin_date,
                                                    end_date=end_date)


class BlockCustomMemberFactory(EngineFactory):

    def result(self, codes=None, key=None, columns=None):
        return self._fetch_engine.block_custom_member(codes=codes,
                                                      key=key,
                                                      columns=columns)


class StockBehaviorFactory(EngineFactory):

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_time=None,
               end_time=None):
        return self._fetch_engine.stock_xueqiu_behavior(codes=codes,
                                                        key=key,
                                                        columns=columns,
                                                        begin_time=begin_time,
                                                        end_time=end_time)


class FundMarketFactory(EngineFactory):

    def result(self,
               codes=None,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.fund_market(codes=codes,
                                              key=key,
                                              columns=columns,
                                              begin_date=begin_date,
                                              end_date=end_date)


class FundBasicFactory(EngineFactory):

    def result(self, codes, key=None, columns=None):
        return self._fetch_engine.fund_basic(codes=codes,
                                             key=key,
                                             columns=columns)


class ETFMemberFactory(EngineFactory):

    def result(self,
               codes,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.etf_member(codes=codes,
                                             key=key,
                                             columns=columns,
                                             begin_date=begin_date,
                                             end_date=end_date)


class PortfolioMemberFactory(EngineFactory):

    def result(self,
               codes,
               key=None,
               columns=None,
               begin_date=None,
               end_date=None):
        return self._fetch_engine.portfolio_member(codes=codes,
                                                   key=key,
                                                   columns=columns,
                                                   begin_date=begin_date,
                                                   end_date=end_date)
