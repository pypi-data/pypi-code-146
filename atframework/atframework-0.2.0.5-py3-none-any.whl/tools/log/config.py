"""
Created on Mar 04, 2021

@author: Siro

"""

import logging.config
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))
conf_path = os.path.join(
    os.path.dirname(os.path.join(os.path.realpath(__file__))), 'log.conf')
print(conf_path)
logging.config.fileConfig(conf_path, disable_existing_loggers=False)

logger = logging.getLogger("case")
logger.info("------Logger starts to work-----")