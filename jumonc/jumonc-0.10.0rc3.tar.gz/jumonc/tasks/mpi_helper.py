import logging
import sys
from functools import wraps
from typing import Any
from typing import Callable
from typing import cast
from typing import List
from typing import TypeVar
from typing import Union

from jumonc.models import dataStore
from jumonc.tasks import mpibase
from jumonc.tasks import mpiroot
#from mpi4py import MPI


logger = logging.getLogger(__name__)

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec


def build_mpi_command(mpi_id: int, resultids:List[int], kwargs: Any, block_communication:bool = True) -> List[int]:
    logger.debug("mpi command with: %i, %s", mpi_id, str(block_communication))
    logger.debug("kwargs: %s", str(kwargs))
    
    data:List[Any] = [mpi_id]
    data.append(block_communication)
    data.append(kwargs)
    data.append(resultids)
    return data


F = TypeVar('F', bound=Callable[..., Any])
P = ParamSpec('P')
T = TypeVar('T')

def multi_node_information(results:int = 1) ->  Callable[[F], F]:
    def wrap(func: Callable[P, T]) -> Callable[P, Union[T, List[T]]]:
        @wraps(func)
        def decorated_function(*args: P.args, **kwargs: P.kwargs) -> Union[T, List[T]]:
            logger.debug("args    %s", type(args))
            logger.debug("kwargs: %s", type(kwargs))
            if mpibase.size == 1:
                kwargs.pop("id", None)
                return func(*args, **kwargs)
            if "already_task" in kwargs:
                kwargs.pop("already_task", None)
                kwargs.pop("id", None)
                logger.debug("multi_node_information is already a task")
                return func(*args, **kwargs)
            if mpibase.rank == 0:
                kwargs["already_task"] = True
                resultids = []
                for _ in range(results):
                    resultids.append(dataStore.getNextDataID())
                mpi_id = kwargs["id"]
                if not isinstance(mpi_id, int):
                    logger.error("Invalid mpi id")
                    return func(*args, **kwargs)
                mpiroot.sendCommand(build_mpi_command(mpi_id = mpi_id, 
                                                      resultids = resultids, 
                                                      kwargs = kwargs))
                
                mpiroot.sendCommand(build_mpi_command(mpi_id = mpibase.gatherid, 
                                                      resultids = [-1], 
                                                      block_communication = True, 
                                                      kwargs = {"dataIDs": resultids}))
                
                return cast(Union[T, List[T]], dataStore.getResult(resultids[0]))
            logger.error("multi_node_information: should not reach here")
            return func(*args, **kwargs)
            
        return decorated_function
    return wrap # type: ignore
