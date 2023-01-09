# -*- coding: utf-8 -*-
import os
from uqer import DataAPI
import uqer
from jdw.kdutils.logger import kd_logger

if 'UQER_TOKEN' in os.environ:
    kd_logger.info("uquer init")
    client = uqer.Client(token=os.environ['UQER_TOKEN'])