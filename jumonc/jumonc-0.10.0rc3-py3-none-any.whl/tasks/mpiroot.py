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
    taskPool.setupTaskPool()
    while mpibase.keepRunning():
        task_switcher.executeNextTask()


def sendCommand(data: List[Any]) -> None:
    if mpibase.keepRunning():
        logger.debug("sending mpi command with data: %s", str(data))
        mpibase.MPI_barrier()
        __comm.bcast(data, root=0)
        task_switcher.addTask(data)


def gatherResult(dataIDs: List[int]) -> None:
    logger.debug("Gather Results for dataIDs = %s", str(dataIDs))
    mpiOperation = 6
    
    for dataID in dataIDs:
        with mpibase.mpi_lock:
    
            if mpiOperation == mpibase.MPIGatherFunctionality.ONENODE.value:
                pass

            (rec_res_avai, result) = __testResultAvaiable(dataID)
            if rec_res_avai == 1:
                if mpiOperation == mpibase.MPIGatherFunctionality.MIN.value:
                    resultCom = __comm.reduce(result, op = MPI.MIN, root = 0)
                elif mpiOperation == mpibase.MPIGatherFunctionality.MAX.value:
                    resultCom = __comm.reduce(result, op = MPI.MAX, root = 0)
                elif mpiOperation == mpibase.MPIGatherFunctionality.AVERAGE.value:
                    resultCom = __comm.reduce(result, op = MPI.SUM, root = 0)
                    if isinstance(resultCom,(int, float)):
                        resultCom = resultCom / __comm.Get_size()
                    else:
                        logger.error("MPI reduce did not return a number as expected")
                        return
                elif mpiOperation == mpibase.MPIGatherFunctionality.SUM.value:
                    resultCom = __comm.reduce(result, op = MPI.SUM, root = 0)
                elif mpiOperation == mpibase.MPIGatherFunctionality.ALL.value:
                    resultCom = __comm.gather(result, root=0)
                dataStore.removeResult(dataID)
                dataStore.addResult(dataID, resultCom)
            else: 
                logger.info("Gathering resheduled for data gathering")
                logger.error("Rescheduking still missing")
                #taskSwitcher.tasks.add(command)
    
    


        
def __testResultAvaiable(dataID: int) -> Tuple[int, Optional[Any]]:
    result_avaiable: int = 0
    result: Optional[Any] = None
    try:
        result = dataStore.getResult(dataID)
        result_avaiable = 1
    except KeyError:
        result_avaiable = 0

    rec_res_avai: int = 0
    results_avai = __comm.gather(result_avaiable, root=0)
    res = 1
    if results_avai is not None:
        for avai in results_avai:
            res = res*avai
        rec_res_avai = __comm.bcast(res, root=0)
        return (rec_res_avai, result)
    logger.error("Root did not recieve result")
    return (0, result)
