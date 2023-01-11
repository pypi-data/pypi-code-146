##
# File: main.py
# Date: 11-Aug-2020
#
# Template/skeleton web service application
#
##
__docformat__ = "google en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"

import logging

from fastapi import FastAPI

from . import ConfigProvider
from . import LogFilterUtils
from . import serverStatus

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
# The following mimics the default Gunicorn logging format
formatter = logging.Formatter("%(asctime)s [%(process)d] [%(levelname)s] [%(module)s.%(funcName)s] %(message)s", "[%Y-%m-%d %H:%M:%S %z]")
# The following mimics the default Uvicorn logging format
# formatter = logging.Formatter("%(levelname)s:     %(asctime)s-%(module)s.%(funcName)s: %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.propagate = True
# Apply logging filters -
lu = LogFilterUtils.LogFilterUtils()
lu.addFilters()
# ---

app = FastAPI()


@app.on_event("startup")
async def startupEvent():
    logger.info("Startup - running application startup placeholder method")
    cp = ConfigProvider.ConfigProvider()
    _ = cp.getConfig()
    _ = cp.getData()
    #


@app.on_event("shutdown")
def shutdownEvent():
    logger.info("Shutdown - running application shutdown placeholder method")


# Example entry point
app.include_router(serverStatus.router)
