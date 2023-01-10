"""
Put constants here.
Please use "_" as prefix for internal constants.
"""
from datetime import datetime

DATETIME_FMT_FULL = "%Y-%m-%d %H:%M:%S"
DATETIME_FMT_DATE = "%Y-%m-%d"
DATETIME_FMT_TIME = "%H:%M:%S"
# many systems (e.g. Mongo) does not support default datetime.min (0001-01-01 00:00:00),
# so we have to use a conservative value as minimal datetime.
DATETIME_SAFE_MIN = datetime(1900, 1, 1)

NO_PROJ = -1

POINT_NAME = "point_name"  # point name