import logging
import sys
from enum import Enum
from threading import Lock
from time import sleep

import mpi4py
from mpi4py import MPI

from jumonc import settings
from jumonc.tasks.taskSwitcher import task_switcher


logger = logging.getLogger(__name__)


mpi4py.rc.threads = True
mpi4py.rc.thread_level = "serialized"



__keep_running = True

mpi_lock = Lock()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


class MPIGatherFunctionality(Enum):
    MIN = 1
    MAX = 2
    AVERAGE = 3
    SUM = 4
    ONENODE = 5
    ALL = 6


def MPI_barrier(do_barrier:bool = settings.MPI_reduce_idle_CPU_load, wait_timer:float = settings.MPI_sleep_timer) -> None: 
    if do_barrier:
        req = comm.Ibarrier()
        while req.Test() is False:
            sleep(wait_timer)


def keepRunning() -> bool:
    return __keep_running

def stop() -> None:
    global __keep_running
    __keep_running = False
    

    
# stop all MPI handlers
def MPI_fin() -> None:
    logger.debug("MPI stop")
    stop()
    MPI.Finalize()
        
    sys.exit(0)


stop_handlers_id = task_switcher.addFunction(MPI_fin)
gatherid:int = -1
