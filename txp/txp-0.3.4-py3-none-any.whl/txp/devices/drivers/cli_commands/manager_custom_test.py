"""
This module defines the main function to be called from the CLI program
for the command: ru_device_manager
"""
# ============================ imports =========================================

from txp.devices.devices_manager import DevicesManager
from txp.devices.drivers.icomox.icomox_driver import IcomoxDriver
from txp.common.edge import EdgeDescriptor, EdgeType, MachineMetadata
from txp.devices.sampling_task import SamplingTask
from txp.common.configuration import SamplingWindow
from txp.devices.package_queue import PackageQueue, PackageQueueProxy
from txp.common.configuration import SamplingParameters
import multiprocessing
from typing import Tuple
import datetime
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
# Declares the EdgeDescriptors for the Icomox instance
# ==============================================================================
machine_metadata: MachineMetadata = MachineMetadata(
    "licuadora_1", "Clasica 4655", "Osterizer", ["icomox_1"]
)

icomox_1_descriptor: EdgeDescriptor = EdgeDescriptor(
    "icomox_1",
    EdgeType.STREAM_ONLY_DEVICE,
    IcomoxDriver.device_name(),
    {
        IcomoxDriver._PHYSICAL_ID_PARAM_FIELD : "12A79EA89FFE7C394EFC030038343038",
    },
    {
        "VibrationAcceleration": {
            IcomoxDriver.PERCEPTION_DIMENSIONS_FIELD: [3, 1024],
            IcomoxDriver.PERCEPTION_SAMPLING_FREQUENCY_FIELD: 3611.11
        },
        "VibrationSpeed": {
            IcomoxDriver.PERCEPTION_DIMENSIONS_FIELD: [3, 512],
            IcomoxDriver.PERCEPTION_SAMPLING_FREQUENCY_FIELD: 399.60
        },
        "Magnetometer": {
            IcomoxDriver.PERCEPTION_DIMENSIONS_FIELD: [3, 512],
            IcomoxDriver.PERCEPTION_SAMPLING_FREQUENCY_FIELD: 334.36
        },
        "Microphone": {
            IcomoxDriver.PERCEPTION_DIMENSIONS_FIELD: [1, 512],
            IcomoxDriver.PERCEPTION_SAMPLING_FREQUENCY_FIELD: 20312.5
        }
    }
)


# ==============================================================================
# Declares the SamplingWindow
# Observation time: 40s
# Sampling time: 20s
# ==============================================================================
sampling_window: SamplingWindow = SamplingWindow(40, 35)
start_date = datetime.datetime.now().date()
end_date = start_date + datetime.timedelta(days=1)
start_time = (datetime.datetime.now() + datetime.timedelta(seconds=15)).time()
end_time = (datetime.datetime.now() + datetime.timedelta(minutes=4)).time()
sampling_parameters: SamplingParameters = SamplingParameters(
    sampling_window,
    start_date,
    end_date,
    "1111111",
    start_time,
    end_time,
    []
)
state_queue = multiprocessing.Manager().Queue()
tasks = {
    icomox_1_descriptor.logical_id:SamplingTask("0", sampling_parameters, "labshowroom-001")
}


def device_manager_test(unique_id: Tuple):
    devices_manager = DevicesManager()
    try:
        package_queue_proc_manager = ProcessesManager()
        package_queue_proc_manager.start()
        gateway_packages_queue: PackageQueueProxy = package_queue_proc_manager.PackageQueue()

        #device manager initialization
        devices_manager.create_host(IcomoxDriver.device_name(),gateway_packages_queue)
        devices_manager.initialize_drivers([icomox_1_descriptor])
        devices_manager.start()
        devices_manager.receive_sampling_tasks(tasks)

        #for this example I will only wait for the first device to report it is connected in order to start sampling
        #this method should be used in the backgound to update the states of drivers table handled by the gateway.
        while True:
            states = devices_manager.get_state_changed_queued_items()
            if len(states) > 0:
                break

        devices_manager.start_sampling_windows()

        while True:
            time.sleep(10)
    finally:
        devices_manager.stop()

if __name__ == "__main__":
    """Main function to debug if the module is executed."""
    args = sys.argv[1:]

    unique_id = tuple(args[0].split("-"))
    device_manager_test(unique_id)
