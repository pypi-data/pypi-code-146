"""
This module defines a common USBDriver class intended to be used
as the parent class for all the USB devices that are handled by the USBDriversHost.
"""
# ============================ imports =========================================
from txp.devices.drivers.driver import Driver
from txp.common.edge import EdgeDescriptor
from txp.devices.package_queue import PackageQueueProxy
import queue
from txp.common.config import settings
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


# ==============================================================================
# USBDriver class
# ==============================================================================
class UsbDriver(Driver):
    """This driver is the generic common parent for all USB Drivers implemented in the system
    """
    def __init__(
            self,
            edge_descriptor: EdgeDescriptor,
            gateway_packages_queue: PackageQueueProxy,
            on_driver_state_changed: callable,
            host_clock_notification_queue: queue.Queue
    ):
        Driver.__init__(self, edge_descriptor, gateway_packages_queue,
                        on_driver_state_changed, host_clock_notification_queue)

    @classmethod
    def device_name(cls) -> str:
        return "Usb"
