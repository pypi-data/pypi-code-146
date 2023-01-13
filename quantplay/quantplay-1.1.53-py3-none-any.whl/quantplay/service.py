from quantplay.services.market import Market
from quantplay.services.tradelens import TradeLens
from quantplay.backtest.backtest_trades import Backtesting

market = Market()
backtesting = Backtesting(market)
tradelens = TradeLens

