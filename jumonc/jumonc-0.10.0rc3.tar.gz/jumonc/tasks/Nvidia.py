import logging
from types import ModuleType
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from jumonc.tasks import Plugin
from jumonc.tasks.mpi_helper import multi_node_information
from jumonc.tasks.taskSwitcher import task_switcher


logger = logging.getLogger(__name__)

class _NvidiaPlugin(Plugin.Plugin):
    
    _pynvml: Optional[ModuleType]
    _smi: Optional[ModuleType]
    
    _config = ["driver_version", "count", "name", "serial", "vbios_version",
              "display_mode", "persistence_mode", "compute_mode",
              "pci.bus_id", "pci.bus", "pcie.link.gen.max", "pcie.link.width.max",
              "clocks_throttle_reasons.supported", "clocks.max.graphics", "clocks.max.sm", "clocks.max.memory"
              "power.management", "power.limit", "power.min_limit", "power.max_limit",]
    _status = ["pcie.link.gen.current", "pcie.link.width.current",
              "fan.speed", "power.draw", "pstate",
              "memory.total", "memory.used", "memory.free",
              "utilization.gpu", "utilization.memory",
              "temperature.gpu", "temperature.memory",
              "clocks.current.graphic", "clocks.current.sm", "clocks.current.memory", "clocks.current.video",
              "clocks.applications.graphics", "clocks.applications.memory",
              "mig.mode.current", "mig.mode.pending"]
    
    def __init__(self) -> None:
        """Init pynvml!"""
        super().__init__()
        if self.isWorking():
            if isinstance(self._pynvml, ModuleType):
                try:
                    self._pynvml.nvmlInit()
                    self._status_nvml_id = {"NVML_FI_DEV_NVLINK_THROUGHPUT_DATA_TX": self._pynvml.NVML_PCIE_UTIL_TX_BYTES,
                                            "NVML_FI_DEV_NVLINK_THROUGHPUT_DATA_RX": self._pynvml.NVML_PCIE_UTIL_RX_BYTES }
                    self.handles = []
                    deviceCount = self._pynvml.nvmlDeviceGetCount()
                    for i in range(deviceCount):
                        self.handles.append(self._pynvml.nvmlDeviceGetHandleByIndex(i))
                except self._pynvml.nvml.NVMLError_LibraryNotFound:
                    logger.warning("pynvml cannot find needed gpu libraries, therefore gpu functionality not avaiable")
                    self.notWorkingAnymore()
                    return
                    
            if isinstance(self._smi, ModuleType):
                self.nvsmi = self._smi.smi.nvidia_smi.getInstance()
            else:
                logger.error("Something went wrong, in gpu plugin, pynvml is not ModuleType")
                self.notWorkingAnymore()
        
        self.info_mpi_id = task_switcher.addFunction(self._getInfo)
        self.pci_mpi_id = task_switcher.addFunction(self._getPcieThroughputInfo)

    
    def _isWorking(self) -> bool:
        try:
            self._pynvml = __import__('pynvml')
        except ModuleNotFoundError:
            logger.warning("pynvml can not be imported, therefore gpu functionality not avaiable")
            return False
        try:
            self._smi = __import__('pynvml.smi')
        except ModuleNotFoundError:
            logger.warning("pynvml.smi can not be imported, therefore gpu functionality not avaiable")
            return False
        return True
    
    @multi_node_information()
    def _getInfo(self, name:str) -> Dict[str, Any]:
        return self.nvsmi.DeviceQuery(name)
    
    @multi_node_information()
    def _getPcieThroughputInfo(self, name:str) -> Dict[str,Any]:
        repetitions = 1
        if isinstance(self._pynvml, ModuleType):
            dic:Dict[str, Any] = {"gpu": []}
            result = [0.0]*len(self.handles)
            for i in range(repetitions):
                for i, handler in enumerate(self.handles):
                    result[i] = result[i] + self._pynvml.nvmlDeviceGetPcieThroughput(handler, self._status_nvml_id[name])
            for i in range(len(self.handles)):
                dic["gpu"].append({"pci": {name: result[i]/repetitions, "Unit": "KiB/s"}})
            return dic
        return {}
    
    def getConfigList(self) -> List[str]:
        return self._config
    
    def getStatusList(self) -> List[str]:
        return self._status + list(self._status_nvml_id.keys())
    
    def getConfigData(self, dataType:str) -> Dict[str, Any]:
        if dataType in self._config:
            return self._getInfo(dataType)
        return {}
    
    def getStatusData(self, dataType:str) -> Dict[str, Any]:
        logger.debug("Get GPU Status data for %s", dataType)
        if dataType in self._status:
            return self._getInfo(name=dataType, id=self.info_mpi_id) # type: ignore
        if dataType in self._status_nvml_id:
            return self._getPcieThroughputInfo(name=dataType, id=self.pci_mpi_id) # type: ignore
        return {}
    
    
plugin = _NvidiaPlugin()
