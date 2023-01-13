import logging
import threading
from typing import Any
from typing import Dict
from typing import Optional



logger = logging.getLogger(__name__)


__data_lock: threading.Lock = threading.Lock()
__data: Dict[int, Optional[Any]] = {}

__id_lock: threading.Lock = threading.Lock()
__last_id: int = 0

def getNextDataID() -> int:
    global __last_id
    logger.debug("Waiting for next ID")
    with __id_lock:
        __last_id = __last_id + 1
        logging.debug("Next Id generated: %i", __last_id)
        return __last_id
    
def addResult(dataID: int, result: Optional[Any]) -> None:
    logger.debug("Waiting for access to data store")
    if dataID > 0:
        with __data_lock:
            __data[dataID] = result
            logging.debug("Data (%s) for ID %i stored", str(result), dataID)
    
def getResult(dataID: int) -> Optional[Any]:
    logger.debug("Waiting for access to data store")
    with __data_lock:
        result = __data[dataID]
        logging.debug("Data (%s) for ID %i retrived", str(result), dataID)
        return result
    
def removeResult(dataID: int) -> None:
    logger.debug("Waiting for access to data store")
    with __data_lock:
        del __data[dataID]
        logging.debug("Data for ID %i removed", dataID)
