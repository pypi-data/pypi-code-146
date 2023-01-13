import logging
from platform import node
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from jumonc.tasks import Plugin
from jumonc.tasks.mpi_helper import multi_node_information
from jumonc.tasks.taskSwitcher import task_switcher


logger = logging.getLogger(__name__)


class _JOBPlugin(Plugin.Plugin): 
    
    def __init__(self) -> None:
        super().__init__()
        self.isWorking()
        self.name_mpi_id = task_switcher.addFunction(self.getNodeName)
    
    
    def _isWorking(self) -> bool:
        return True
    
    @multi_node_information()
    def getNodeName(self) -> str:
        if self.works is True:
            return node()
        logger.error("job plugin is disabled, \"getNodeName\" should not be called")
        raise RuntimeError("job plugin is disabled, \"getNodeName\" should not be called")
    
    
    def getStatusData(self,
                      dataType: str, 
                      overrideHumanReadableWithValue: Optional[bool] = None) -> List[Dict[str, Union[bool, int, float ,str]]]:
        logger.debug("get job status data with type=%s, overrride humand readable=%s",
                     str(dataType),
                     str(overrideHumanReadableWithValue))
        return []
    
    def getConfigData(self,
                      dataType: str) -> List[Dict[str, Union[bool, int, float ,str]]]:
        logger.debug("get job config data with type=%s", str(dataType))
        if dataType == "Nodename":
            return [{"node name": str(self.getNodeName(id=self.name_mpi_id))}] # type: ignore
        return []
    
    
plugin = _JOBPlugin()
