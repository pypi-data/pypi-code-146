# -*- coding: utf-8 -*-
import os
import tushare as ts
from jdw.kdutils.logger import kd_logger

pro = None
if 'TS_TOKEN' in os.environ:
    kd_logger.info("tushare init")
    ts.set_token(os.environ['TS_TOKEN'])
    pro = ts.pro_api(os.environ['TS_TOKEN'])
