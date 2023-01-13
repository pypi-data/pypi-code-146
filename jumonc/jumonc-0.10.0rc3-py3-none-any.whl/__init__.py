"""
jumonc is a programm that lets you monitor and control you simulation using the provided REST-API.

Further informaton can be found in the README.md.
The application cmd arguments can be found in doc/CMD/Parameters.md
The REST API is documented with openapi, and rendered well by gitlab on:
https://gitlab.jsc.fz-juelich.de/witzler1/jumonc/-/blob/CI_fixes/doc/REST_API/openapi.yaml
"""
import logging
import sys

from jumonc import settings
from jumonc._version import __version__
from jumonc.tasks import mpibase


__all__ = ["settings", "__version__", "setup_logging", "reset_logging"]

def setup_logging() -> None:
    handler = logging.StreamHandler(sys.stdout if settings.LOG_STDOUT else sys.stderr)
    if mpibase.size != 1:
        mpi_rank_logging = "[mpi_rank=" + str(mpibase.rank) + "]"
    else:
        mpi_rank_logging = ""
    
    formatter = logging.Formatter(settings.LOG_PREFIX + mpi_rank_logging + settings.LOG_FORMAT)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    
    if mpibase.rank in settings.LOGGING_MPI_RANKS:
        logging.getLogger().setLevel(settings.LOG_LEVEL)
    else:
        logging.getLogger().setLevel("ERROR")
    
    fileHandler = logging.FileHandler('jumonc.log')
    fileHandler.setFormatter(formatter)
    logging.getLogger().addHandler(fileHandler)


setup_logging()


def reset_logging() -> None:
    logger = logging.getLogger()
    while logger.hasHandlers():
        logger.removeHandler(logger.handlers[0])
    setup_logging()
