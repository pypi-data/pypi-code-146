"""
This module defines the main function to be called from the CLI program
for the command: run_voyager_test
"""
# ============================ imports =========================================
from txp.devices.drivers.voyager.voyager_driver import VoyagerDriver
from txp.devices.drivers.voyager.voyager_driver_host import VoyagerDriversHost
from txp.common.edge import EdgeDescriptor, EdgeType, MachineMetadata
from txp.devices.sampling_task import SamplingTask
from txp.common.configuration import SamplingWindow
from txp.devices.package_queue import PackageQueue, PackageQueueProxy
import multiprocessing
from typing import Tuple
import sys
import time
from txp.common.config import settings
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


# ==============================================================================
# Server process to MOCK the gateway's package queue.
# ==============================================================================
class ProcessesManager(multiprocessing.managers.BaseManager):
    """This class will be used to create the Driver, the SmartMeshManager and the
    PackageQueue in separated processes"""

    pass


ProcessesManager.register("PackageQueue", PackageQueue, proxytype=PackageQueueProxy)

# ==============================================================================
# Declares the EdgeDescriptors for the Voyager instance
# ==============================================================================
machine_metadata: MachineMetadata = MachineMetadata(
    "licuadora_1", "Clasica 4655", "Osterizer", ["voyager_1"]
)

voyager_1_descriptor: EdgeDescriptor = EdgeDescriptor(
    "voyager_1",
    EdgeType.STREAM_ONLY_DEVICE,
    VoyagerDriver.device_name(),
    {},
    {
        "VibrationAcceleration": {
            VoyagerDriver.PERCEPTION_DIMENSIONS_FIELD: [3, 512],
            VoyagerDriver.PERCEPTION_SAMPLING_FREQUENCY_FIELD: 5000
        }
    }
)

# ==============================================================================
# Declares the SamplingWindow for the Voyager instance
# Observation time: 40s
# Sampling time: 20s
# ==============================================================================
sampling_window: SamplingWindow = SamplingWindow(40, 35)


def voyager_test(mac: Tuple):
    package_queue_proc_manager = ProcessesManager()

    package_queue_proc_manager.start()

    gateway_packages_queue: PackageQueueProxy = package_queue_proc_manager.PackageQueue()

    voyagers_host = VoyagerDriversHost(gateway_packages_queue)

    voyagers_host.connect()

    # The driver expects the MAC address as a parameter.
    # This MAC address setup is a responsibility of the Gateway
    # when it's processing the operations configuration.

    voyager_1_descriptor.edge_parameters["mac"] = mac

    voyagers_host.add_drivers([voyager_1_descriptor])

    voyagers_host.connect_drivers()
    devicesId = voyagers_host.discover_physical_ids()

    # voyager_1_descriptor 1 sampling task assigned to collect 2 packages.
    task1 = SamplingTask(2, sampling_window, 'client')
    voyagers_host.receive_sampling_tasks(
        {
            voyager_1_descriptor.logical_id: task1
        }
    )

    voyagers_host.start_sampling_windows()
    while True:
        time.sleep(10)
        #voyagers_host.stop_sampling_windows()

if __name__ == "__main__":
    """Main function to debug if the module is executed."""
    args = sys.argv[1:]

    mac_string = args[0].split("-")
    mac = tuple(int(i,16) for i in mac_string)

    voyager_test(mac)
