# -*- coding: utf-8 -*-
import os
import rqdatac
from jdw.kdutils.logger import kd_logger

if 'RQ_TOKEN' in os.environ:
    kd_logger.info("ricequant init")
    rqdatac.init('license', os.environ['RQ_TOKEN'])