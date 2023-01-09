import json
import os
import sys

from coinlib.brokerWorker.BrokerFactory import BrokerFactory
from coinlib.feature.FeatureFactory import FeatureFactory
from coinlib.helper import pip_install_or_ignore
from logger import  install_cloud_logger
from coinlib.notification.NotificationFactory import NotificationFactory
from coinlib.symbols import SymbolFactory

pip_install_or_ignore("ipynb_path", "ipynb-path", "0.1.4")
# pip_install_or_ignore("import_ipynb", "import_ipynb")
pip_install_or_ignore("websocket", "websocket-client", "0.58.0")
pip_install_or_ignore("plotly", "plotly", "4.14.3")
pip_install_or_ignore("simplejson", "simplejson", "3.17.2")
pip_install_or_ignore("aio_pika", "aio_pika", "6.8.0")
pip_install_or_ignore("grpc", "grpcio-tools", "1.35.0")
pip_install_or_ignore("matplotlib", "matplotlib", "3.3.4")
pip_install_or_ignore("pandas", "pandas", "1.2.4")
#pip_install_or_ignore("timeit", "timeit")
pip_install_or_ignore("dateutil", "python-dateutil", "2.8.1")
pip_install_or_ignore("chipmunkdb", "chipmunkdb-python-client", "2.0.1")


from coinlib.logics import LogicLoader
from coinlib.statistics import StatisticsRuleFactory, StatisticsMethodFactory
from coinlib import ChartsFactory
from coinlib.DataWorker import WorkerJobListener
from coinlib.Registrar import Registrar
import asyncio


registrar = Registrar()

install_cloud_logger()


def run_main_function(worker_modules = []):
    registrar.setEnvironment("live")
    registrar.worker_modules = worker_modules if worker_modules is not None else []
    registrar.statsRuleFactory = StatisticsRuleFactory.StatisticsRuleFactory()
    registrar.statsMethodFactory = StatisticsMethodFactory.StatisticsMethodFactory()
    registrar.chartsFactory = ChartsFactory.ChartsFactory()
    registrar.symbolFactory = SymbolFactory.SymbolFactory()
    registrar.notificationFactory = NotificationFactory()
    registrar.logicFactory = LogicLoader.LogicFactory()
    registrar.brokerFactory = BrokerFactory()
    registrar.featureFactory = FeatureFactory()

    workerJobs = WorkerJobListener()
    workerJobs.start()

    registrar.logger.info("Starting Coinlib Factory")
    registrar.logger.info("Modules: "+','.join(str(e) for e in worker_modules))
    registrar.logger.info("Registry: "+str(os.getenv("REGISTRY")))
    registrar.logger.info("Name: "+str(os.getenv("WORKERNAME")))

    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    finally:
        loop.close()

if __name__ == '__main__':
    worker_modules = []
    if len(sys.argv) > 1:
        worker_modules = sys.argv[1].split(",")
    if os.getenv("MODULES") is not None:
        mods = os.getenv("MODULES")
        if "[" in mods:
            worker_modules = json.loads(mods)
        else:
            mods = os.getenv("MODULES")
            mods = mods.replace("\"", "")
            mods = mods.replace("'", "")
            worker_modules = mods.split(",")
            worker_modules = [x for x in worker_modules if x and x != ""]
    run_main_function(worker_modules)