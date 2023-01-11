"""
This module defines the main function to be called from the CLI program
for the command: run_vicomox_test
"""
# ============================ imports =========================================
import queue

from txp.devices.drivers.driver import DriverState
from txp.devices.drivers.icomox.icomox_driver import IcomoxDriver
from txp.devices.drivers.icomox.icomox_driver_host import IcomoxDriversHost
from txp.common.edge import EdgeDescriptor, EdgeType, MachineMetadata
from txp.devices.sampling_task import SamplingTask
from txp.common.configuration import SamplingWindow
from txp.devices.package_queue import PackageQueue, PackageQueueProxy
import multiprocessing
from typing import Tuple
import sys
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
        IcomoxDriver._PHYSICAL_ID_PARAM_FIELD : "12A79E50FF0E7D384128040038343038",
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

icomox_2_descriptor: EdgeDescriptor = EdgeDescriptor(
    "icomox_2",
    EdgeType.STREAM_ONLY_DEVICE,
    IcomoxDriver.device_name(),
    {
        IcomoxDriver._PHYSICAL_ID_PARAM_FIELD: "12A79EA8370F5D383C23040038343038",
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

icomox_3_descriptor: EdgeDescriptor = EdgeDescriptor(
    "icomox_3",
    EdgeType.STREAM_ONLY_DEVICE,
    IcomoxDriver.device_name(),
    {
        IcomoxDriver._PHYSICAL_ID_PARAM_FIELD: "12A79E3C872FFD382BEF040038343038",
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

icomox_4_descriptor: EdgeDescriptor = EdgeDescriptor(
    "icomox_4",
    EdgeType.STREAM_ONLY_DEVICE,
    IcomoxDriver.device_name(),
    {
        IcomoxDriver._PHYSICAL_ID_PARAM_FIELD: "12A79E7CC70FDD382C1C040038343038",
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
sampling_window: SamplingWindow = SamplingWindow(120, 100)

state_queue = multiprocessing.Manager().Queue()

def icomox_test(unique_id: Tuple):
    package_queue_proc_manager = ProcessesManager()
    package_queue_proc_manager.start()
    gateway_packages_queue: PackageQueueProxy = package_queue_proc_manager.PackageQueue()
    icomox_host = IcomoxDriversHost(gateway_packages_queue,state_queue)
    icomox_host.connect()
    icomox_host.connect_drivers()

    icomox_host.add_drivers([(icomox_2_descriptor)])
    task2 = SamplingTask(2,sampling_window, 'client')


    while True:
        try:
            state = state_queue.get(False,10).driver_state
            if state == DriverState.CONNECTED:
                icomox_host.receive_sampling_tasks(
                    {
                        icomox_2_descriptor.logical_id: task2
                    }
                )
                icomox_host.start_sampling_windows()
            else:
                print(state)
        except queue.Empty as ex:
            pass




if __name__ == "__main__":
    """Main function to debug if the module is executed."""
    args = sys.argv[1:]

    unique_id = tuple(args[0].split("-"))
    icomox_test(unique_id)
