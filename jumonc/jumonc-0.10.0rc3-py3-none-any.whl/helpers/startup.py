import logging
from typing import List

from mpi4py import MPI

from jumonc.helpers.PluginManager import setPluginsWorkingStatus
from jumonc.models import pluginInformation


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

logger = logging.getLogger(__name__)

_plugin_check_done = False


def setPluginMPIIDs(workingPlugins: List[str]) -> None:
    # we know the plugins ar ein the same order on every node, 
    # because we add them in the same order for all nodes in communicateAvaiablePlugins(),
    # therefore each node assigns the same IDs to the plugins
    for plugin in workingPlugins:
        pluginInformation.addMPIIDsForPlugin(plugin)

def communicateAvaiablePlugins() -> List[str]:
    working: List[str] = []
    not_working: List[str] = []
    numTests = 0
    name = ""
    
    if rank == 0:
        for name, works in pluginInformation.get_plugin_items():
            if works is True:
                numTests = numTests + 1
        comm.bcast((numTests), root=0)
        for name, works in pluginInformation.get_plugin_items():
            logging.debug("%s: %s", name, str(works))
            if works is True:
                comm.bcast(name, root=0)
                
                working_everywhere = comm.allreduce(int(works), op=MPI.PROD)
            
                if working_everywhere == 1:
                    working.append(name)
                else:
                    pluginInformation.disablePlugin(name)
                    not_working.append(name)
                    
            else:
                not_working.append(name)
        logger.info("Working plugins: %s", str(working))
        if len(not_working) > 0:
            logger.warning("Not working plugins: %s", str(not_working))
    else:
        numTests = comm.bcast(numTests, root=0)
        for _ in range(numTests):
            name = comm.bcast(name, root=0)
            try:
                works = pluginInformation.pluginIsWorking(name)
            except KeyError:
                works = False
            
            working_everywhere = comm.allreduce(int(works), op=MPI.PROD)
            
            if not working_everywhere:
                pluginInformation.disablePlugin(name)
                
            
    return working


def checkIfPluginsAreWorking() -> None:
    global _plugin_check_done
    if _plugin_check_done is True:
        return
    
    test_papi()
    test_nv()
    test_linuxNet()
    test_cpu()
    test_mem()
    test_disk()
    test_slurm()
    test_job()
    
    setPluginsWorkingStatus()
    
    _plugin_check_done = True


def test_papi() -> None:
    #pylint: disable=import-outside-toplevel
    from jumonc.tasks.Papi import PapiPlugin
    #pylint: enable=import-outside-toplevel
        
    plugin_p = PapiPlugin()
    if plugin_p.isWorking() is False:
        if rank == 0:
            logger.warning("Could not load PAPI plugin")
        else:
            logger.debug("Could not load PAPI plugin")
            

def test_nv() -> None:
    #pylint: disable=import-outside-toplevel
    from jumonc.tasks import Nvidia
    #pylint: enable=import-outside-toplevel
        
    plugin_n = Nvidia.plugin
    if plugin_n.isWorking() is False:
        if rank == 0:
            logger.warning("Could not load Nvidia plugin")
        else:
            logger.debug("Could not load Nvidia plugin")
            
            
def test_linuxNet() -> None:
    #pylint: disable=import-outside-toplevel
    from jumonc.tasks import LinuxNetwork
    #pylint: enable=import-outside-toplevel
        
    plugin_net = LinuxNetwork.plugin
    if plugin_net.isWorking() is False:
        if rank == 0:
            logger.warning("Could not load Linux network plugin")
        else:
            logger.debug("Could not load Linux network plugin")


def test_cpu() -> None:
    #pylint: disable=import-outside-toplevel
    from jumonc.tasks import CPU
    #pylint: enable=import-outside-toplevel
        
    plugin_cpu = CPU.plugin
    if plugin_cpu.isWorking() is False:
        if rank == 0:
            logger.warning("Could not load Linux CPU plugin")
        else:
            logger.debug("Could not load Linux CPU plugin")
    
def test_mem() -> None:
    #pylint: disable=import-outside-toplevel
    from jumonc.tasks import memory
    #pylint: enable=import-outside-toplevel
        
    plugin_mem = memory.plugin
    if plugin_mem.isWorking() is False:
        if rank == 0:
            logger.warning("Could not load Linux memory plugin")
        else:
            logger.debug("Could not load Linux memory plugin")


def test_disk() -> None:
    #pylint: disable=import-outside-toplevel
    from jumonc.tasks import disk
    #pylint: enable=import-outside-toplevel
        
    plugin_disk = disk.plugin
    if plugin_disk.isWorking() is False:
        if rank == 0:
            logger.warning("Could not load Linux disk plugin")
        else:
            logger.debug("Could not load Linux disk plugin")
    

def test_slurm() -> None:
    #pylint: disable=import-outside-toplevel
    from jumonc.tasks import Slurm
    #pylint: enable=import-outside-toplevel
            
    plugin_s = Slurm.plugin
    if plugin_s.isWorking() is False:
        if rank == 0:
            logger.warning("Could not load Slurm plugin")
        else:
            logger.debug("Could not load Slurm plugin")
    

def test_job() -> None:
    #pylint: disable=import-outside-toplevel
    from jumonc.tasks import job
    #pylint: enable=import-outside-toplevel
            
    plugin_j = job.plugin
    if plugin_j.isWorking() is False:
        if rank == 0:
            logger.warning("Could not load Job plugin")
        else:
            logger.debug("Could not load Job plugin")
