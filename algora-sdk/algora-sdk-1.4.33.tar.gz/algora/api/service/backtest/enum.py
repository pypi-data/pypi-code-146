from algora.common.base_enum import BaseEnum


class BacktestType(BaseEnum):
    STRATEGY = 'STRATEGY'
    BACKTEST = 'BACKTEST'


class BacktestStatus(BaseEnum):
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    CANCELED = 'CANCELED'
