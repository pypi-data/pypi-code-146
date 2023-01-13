import logging
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple

from mpi4py import MPI

from jumonc.models import dataStore
from jumonc.tasks import mpibase
from jumonc.tasks import taskPool
from jumonc.tasks.taskSwitcher import task_switcher


logger = logging.getLogger(__name__)


__comm = MPI.COMM_WORLD



def waitForCommands() -> None:
    data: Optional[List[int]] = None
    taskPool.setupTaskPool()
    while mpibase.keepRunning():
        with mpibase.mpi_lock:
            logger.debug("rank %i waiting for mpi command", __comm.Get_rank())
            mpibase.MPI_barrier()
            data = __comm.bcast(data, root=0)
        logger.debug("recieved mpi command with data: %s", str(data))
        task_switcher.addTask(data)


def sendResults(dataIDs: List[int]) -> None:  
    
    for dataID in dataIDs:
        with mpibase.mpi_lock:
            mpiOperation = 6


            if mpiOperation == mpibase.MPIGatherFunctionality.ONENODE.value:
                pass

            (rec_res_avai, result) = __testResultAvaiable(dataID)
            if rec_res_avai == 1:
                if mpiOperation == mpibase.MPIGatherFunctionality.MIN.value:
                    __comm.reduce(result, op = MPI.MIN, root = 0)
                elif mpiOperation == mpibase.MPIGatherFunctionality.MAX.value:
                    __comm.reduce(result, op = MPI.MAX, root = 0)
                elif mpiOperation == mpibase.MPIGatherFunctionality.AVERAGE.value:
                    __comm.reduce(result, op = MPI.SUM, root = 0)
                elif mpiOperation == mpibase.MPIGatherFunctionality.SUM.value:
                    __comm.reduce(result, op = MPI.SUM, root = 0)
                elif mpiOperation == mpibase.MPIGatherFunctionality.ALL.value:
                    __comm.gather(result, root=0)
                dataStore.removeResult(dataID)

        
def __testResultAvaiable(dataID: int) -> Tuple[int, Optional[Any]]:
    result_avaiable: int = 0
    result: Optional[Any] = None
    try:
        result = dataStore.getResult(dataID)
        result_avaiable = 1
    except KeyError:
        result_avaiable = 0
        
    rec_res_avai: int = 0
    __comm.gather(result_avaiable, root=0)
    res = 0
    rec_res_avai = __comm.bcast(res, root=0)
    return (rec_res_avai, result)
