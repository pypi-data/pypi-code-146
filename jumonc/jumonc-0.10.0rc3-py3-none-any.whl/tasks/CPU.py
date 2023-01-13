import logging
from types import ModuleType
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from jumonc.tasks import Plugin
from jumonc.tasks.mpi_helper import multi_node_information
from jumonc.tasks.taskSwitcher import task_switcher


logger = logging.getLogger(__name__)



class _CPUPlugin(Plugin.Plugin): 
    
    _psutil: Optional[ModuleType]
    
    def __init__(self) -> None:
        super().__init__()
        if self.isWorking():
            if isinstance(self._psutil, ModuleType):
                self._psutil.getloadavg() # make sure it is correctly init even for windows
            else:
                self.notWorkingAnymore()
                logger.warning("CPU plugin disabled, because psutil import is missing")
        
        self.perc_mpi_id = task_switcher.addFunction(self.getPerc)
        self.freq_mpi_id = task_switcher.addFunction(self.getFreq)
        self.load_mpi_id = task_switcher.addFunction(self.getLoad)

    
    
    def _isWorking(self) -> bool:
        try:
            self._psutil = __import__('psutil')
        except ModuleNotFoundError:
            logger.warning("psutil can not be imported, therefore CPU functionality not avaiable")
            return False
        return True
    
    @multi_node_information()
    def getLoad(self) -> List[float]:
        if self.works is True:
            if isinstance(self._psutil, ModuleType):
                return self._psutil.getloadavg()[0]
            logger.error("CPU plugin has no psutil module, \"getLoad\" should not be called")
            raise RuntimeError("CPU plugin has no psutil module, \"getLoad\" should not be called")
        logger.error("CPU plugin is disabled, \"getLoad\" should not be called")
        raise RuntimeError("CPU plugin is disabled, \"getLoad\" should not be called")
    
    
    @multi_node_information()
    def getFreq(self) -> float:
        if self.works is True:
            if isinstance(self._psutil, ModuleType):
                return self._psutil.cpu_freq().current
            logger.error("CPU plugin has no psutil module, \"getFreq\" should not be called")
            raise RuntimeError("CPU plugin has no psutil module, \"getFreq\" should not be called")
        logger.error("CPU plugin is disabled, \"getFreq\" should not be called")
        raise RuntimeError("CPU plugin is disabled, \"getFreq\" should not be called")

    @multi_node_information()
    def getPerc(self) -> float:
        if self.works is True:
            if isinstance(self._psutil, ModuleType):
                return self._psutil.cpu_percent()
            logger.error("CPU plugin has no psutil module, \"getPerc\" should not be called")
            raise RuntimeError("CPU plugin has no psutil module, \"getPerc\" should not be called")
        logger.error("CPU plugin is disabled, \"getPerc\" should not be called")
        raise RuntimeError("CPU plugin is disabled, \"getPerc\" should not be called")
    
    def getStatusData(self,
                      dataType: str, 
                      overrideHumanReadableWithValue: Optional[bool] = None) -> List[Dict[str, Union[bool, int, float ,str]]]:
        logger.debug("get CPU status data with type=%s, overrride humand readable=%s",
                     str(dataType),
                     str(overrideHumanReadableWithValue))
        if dataType == "load":
            load = self.getLoad(id=self.load_mpi_id) # type: ignore
            if isinstance(load, (int, float)):
                return [{"CPU load": load}]
            return [{"CPU load": str(load)}]
            #return [{"load_1": load[0],
            #         "load_5": load[1],
            #         "load_15": load[2]}]
        if dataType == "percent":
            percent_load = self.getPerc(id=self.perc_mpi_id) # type: ignore
            if isinstance(percent_load, (int, float)):
                return [{"CPU utilization": percent_load}]
            return [{"CPU utilization": str(percent_load)}]
        if dataType == "frequency":
            frequency = self.getFreq(id=self.freq_mpi_id) # type: ignore
            if isinstance(frequency, (int, float)):
                return [{"CPU frequency": frequency}]
            return [{"CPU frequency": str(frequency)}]
        return []
    
    
    def getConfigData(self,
                      dataType: str, 
                      overrideHumanReadableWithValue: Optional[bool] = None) -> List[Dict[str, Union[bool, int, float ,str]]]:
        logger.debug("get CPU config data with type=%s, overrride humand readable=%s",
                     str(dataType),
                     str(overrideHumanReadableWithValue))
        return []
    
    
plugin = _CPUPlugin()
