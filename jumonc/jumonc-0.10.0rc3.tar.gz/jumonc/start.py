import logging
import sys
from threading import Thread
from typing import Any

from jumonc import settings
from jumonc._version import __DB_version__
from jumonc._version import __REST_version__
from jumonc._version import __version__
from jumonc.helpers.cmdArguments import parseCMDOptions
from jumonc.helpers.PluginManager import initPluginsREST
from jumonc.helpers.startup import checkIfPluginsAreWorking
from jumonc.helpers.startup import communicateAvaiablePlugins
from jumonc.helpers.startup import setPluginMPIIDs
from jumonc.tasks import mpibase
from jumonc.tasks.taskSwitcher import task_switcher

logger = logging.getLogger(__name__)

def start_jumonc() -> None:
    parseCMDOptions(sys.argv[1:])
    
    logger.info("Using python version: %s", str(sys.version))
    logger.info("Running jumonc with version: %s", __version__)
    logger.debug("Running jumonc with REST-API version: %s", __REST_version__)
    logger.debug("Running jumonc with DB version: %s", __DB_version__)
    logger.info("Running jumonc with mpi size: %s", str(mpibase.size))
    
    checkIfPluginsAreWorking()
    workingPlugins = communicateAvaiablePlugins()
    logger.debug("Pluggins communicated on node %i", mpibase.rank)
    
    setPluginMPIIDs(workingPlugins)

    #pylint: disable=import-outside-toplevel
    if mpibase.rank == 0:
        from jumonc.handlers.base import RESTAPI
        from jumonc.handlers import main
    
        from jumonc.tasks import mpiroot, execute_planed_tasks
        from jumonc.models.cache.database import Base, engine, db_session
        from jumonc.handlers.base import setRESTVersion
        from jumonc.authentication.tokens import registerTokens
    
        mpibase.gatherid = task_switcher.addFunction(mpiroot.gatherResult)

        registerTokens()

        setRESTVersion()
        main.registerRestApiPaths()
        initPluginsREST()

        if settings.SSL_ENABLED:
            jumonc_SSL = settings.SSL_MODE
        else:
            jumonc_SSL = None

        flask_thread = Thread(target = RESTAPI.run,
                              name = "Flask-Thread",
                              kwargs = {'host': settings.FLASK_HOST, 
                                       'debug': settings.FLASK_DEBUG, 
                                       'port': settings.REST_API_PORT, 
                                       'use_reloader': False, 
                                       'ssl_context': jumonc_SSL})
        flask_thread.start()
        
        from jumonc.models.cache import dbmodel
        Base.metadata.create_all(bind=engine)
        dbmodel.check_db_version()

        @RESTAPI.teardown_appcontext
        def shutdown_session(exception:Any = None) -> None:
            db_session.remove()
            if exception:
                logger.warning("DB connection close caused exception: %s", str(exception))
        
        
        execute_planed_tasks.init_scheduling()
    
    
        mpiroot.waitForCommands()
    
    
        flask_thread.join()
    
    else:
        from jumonc.tasks import mpihandler
    
        task_switcher.addFunction(mpihandler.sendResults)

        mpihandler.waitForCommands()
    #pylint: enable=import-outside-toplevel
