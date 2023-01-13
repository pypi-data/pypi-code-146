import logging
from types import ModuleType
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from jumonc import settings
from jumonc.helpers import convertNumbers
from jumonc.tasks import Plugin
from jumonc.tasks.mpi_helper import multi_node_information
from jumonc.tasks.taskSwitcher import task_switcher


logger = logging.getLogger(__name__)


class _diskPlugin(Plugin.Plugin): 
    
    _psutil: Optional[ModuleType]
    
    def __init__(self) -> None:
        super().__init__()
        if self.isWorking():
            if isinstance(self._psutil, ModuleType):
                self._initValues = self._psutil.disk_io_counters()
                if self._initValues is None:
                    self.notWorkingAnymore()
                logger.debug("IO initial values: %s", str(self._initValues))
            else:
                logger.error("Something went wrong, in disk plugin psutil is not ModuleType")
                self.notWorkingAnymore()
        
        self.rc_mpi_id = task_switcher.addFunction(self.getReadCount)
        self.wc_mpi_id = task_switcher.addFunction(self.getWriteCount)
        self.rb_mpi_id = task_switcher.addFunction(self.getReadBytes)
        self.rw_mpi_id = task_switcher.addFunction(self.getWriteBytes)
        self.rt_mpi_id = task_switcher.addFunction(self.getReadTime)
        self.wt_mpi_id = task_switcher.addFunction(self.getWriteTime)
        self.rmc_mpi_id = task_switcher.addFunction(self.getReadMergedCount)
        self.wmc_mpi_id = task_switcher.addFunction(self.getWriteMergedCount)
        self.bt_mpi_id = task_switcher.addFunction(self.getBusyTime)
            
    
    
    def _isWorking(self) -> bool:
        try:
            self._psutil = __import__('psutil')
        except ModuleNotFoundError:
            logger.warning("psutil can not be imported, therefore disk functionality not avaiable")
            return False
        return True
    
    @multi_node_information()
    def getReadCount(self) -> int:
        if isinstance(self._psutil, ModuleType):
            return self._psutil.disk_io_counters().read_count - self._initValues.read_count
        logger.error("Something went wrong, in disk plugin psutil is not ModuleType")
        return -1
    
    @multi_node_information()
    def getWriteCount(self) -> int:
        if isinstance(self._psutil, ModuleType):
            return self._psutil.disk_io_counters().write_count - self._initValues.write_count
        logger.error("Something went wrong, in disk plugin psutil is not ModuleType")
        return -1
    
    @multi_node_information()
    def getReadBytes(self) -> int:
        if isinstance(self._psutil, ModuleType):
            return self._psutil.disk_io_counters().read_bytes - self._initValues.read_bytes
        logger.error("Something went wrong, in disk plugin psutil is not ModuleType")
        return -1
    
    @multi_node_information()
    def getWriteBytes(self) -> int:
        if isinstance(self._psutil, ModuleType):
            return self._psutil.disk_io_counters().write_bytes - self._initValues.write_bytes
        logger.error("Something went wrong, in disk plugin psutil is not ModuleType")
        return -1
    
    @multi_node_information()
    def getReadTime(self) -> int:
        if isinstance(self._psutil, ModuleType):
            return self._psutil.disk_io_counters().read_time - self._initValues.read_time
        logger.error("Something went wrong, in disk plugin psutil is not ModuleType")
        return -1
    
    @multi_node_information()
    def getWriteTime(self) -> int:
        if isinstance(self._psutil, ModuleType):
            return self._psutil.disk_io_counters().write_time - self._initValues.write_time
        logger.error("Something went wrong, in disk plugin psutil is not ModuleType")
        return -1
    
    @multi_node_information()
    def getReadMergedCount(self) -> int:
        if isinstance(self._psutil, ModuleType):
            return self._psutil.disk_io_counters().read_merged_count - self._initValues.read_merged_count
        logger.error("Something went wrong, in disk plugin psutil is not ModuleType")
        return -1
    
    @multi_node_information()
    def getWriteMergedCount(self) -> int:
        if isinstance(self._psutil, ModuleType):
            return self._psutil.disk_io_counters().write_merged_count - self._initValues.write_merged_count
        logger.error("Something went wrong, in disk plugin psutil is not ModuleType")
        return -1
    
    @multi_node_information()
    def getBusyTime(self) -> int:
        if isinstance(self._psutil, ModuleType):
            return self._psutil.disk_io_counters().busy_time - self._initValues.busy_time
        logger.error("Something went wrong, in disk plugin psutil is not ModuleType")
        return -1
    
    def getStatusData(self,
                      dataType: str, 
                      duration: float = -1.0, 
                      overrideHumanReadableWithValue: Optional[bool] = None) -> List[Dict[str, Union[bool, int, float ,str]]]:
        logger.debug("get disk status data with type=%s, duration=%s, overrride humand readable=%s",
                     str(dataType),
                     str(duration),
                     str(overrideHumanReadableWithValue))
        if dataType == "write_count":
            return [self.convertNumber(self.getWriteCount(id=self.wc_mpi_id), "write count", "", overrideHumanReadableWithValue)] # type: ignore
        if dataType == "read_count":
            return [self.convertNumber(self.getReadCount(id=self.wc_mpi_id), "read count", "", overrideHumanReadableWithValue)] # type: ignore
        if dataType == "write_bytes":
            return [self.convertNumber(self.getWriteBytes(id=self.wc_mpi_id), "write", "B", overrideHumanReadableWithValue)] # type: ignore
        if dataType == "read_bytes":
            return [self.convertNumber(self.getReadBytes(id=self.wc_mpi_id), "read", "B", overrideHumanReadableWithValue)] # type: ignore
        if dataType == "write_time":
            return [self.convertNumber(self.getWriteTime(id=self.wc_mpi_id), "write", "ms", overrideHumanReadableWithValue)] # type: ignore
        if dataType == "read_time":
            return [self.convertNumber(self.getReadTime(id=self.wc_mpi_id), "read", "ms", overrideHumanReadableWithValue)] # type: ignore
        if dataType == "write_merged_count":
            return [self.convertNumber(self.getWriteMergedCount(id=self.wc_mpi_id), "merged write", "", overrideHumanReadableWithValue)] # type: ignore
        if dataType == "read_merged_count":
            return [self.convertNumber(self.getReadMergedCount(id=self.wc_mpi_id), "merged read", "", overrideHumanReadableWithValue)] # type: ignore
        if dataType == "busy_time":
            return [self.convertNumber(self.getBusyTime(id=self.wc_mpi_id), "busy", "ms", overrideHumanReadableWithValue)] # type: ignore
        return []
    
    
    def getConfigData(self,
                      dataType: str, 
                      overrideHumanReadableWithValue: Optional[bool] = None) -> List[Dict[str, Union[bool, int, float ,str]]]:
        logger.debug("get disk config data with type=%s, overrride humand readable=%s",
                     str(dataType),
                     str(overrideHumanReadableWithValue))
        return []
    
    
    def convertNumber(self, 
                      num: Any, 
                      name: str, 
                      unit: str, 
                      overrideHumanReadableWithValue: Optional[bool]
                ) -> Dict[str, Union[bool, int, float ,str]]:
        if overrideHumanReadableWithValue or (overrideHumanReadableWithValue is None and settings.DEFAULT_TO_HUMAN_READABLE_NUMBERS) :
            (value, unitPrefix) = convertNumbers.convertBinaryPrefix(num)
            return {name + "[" + unitPrefix + unit + "]" : value}
        
        return {name + "[" + unit + "]" : str(num)}
    
    
plugin = _diskPlugin()
