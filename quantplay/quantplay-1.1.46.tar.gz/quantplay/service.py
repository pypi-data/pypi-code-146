from quantplay.services.market import Market
from quantplay.backtest.backtest_trades import Backtesting
from quantplay.reporting.strategy_report import StrategyReport

market = Market()
backtesting = Backtesting(market)
tradelens = StrategyReport
