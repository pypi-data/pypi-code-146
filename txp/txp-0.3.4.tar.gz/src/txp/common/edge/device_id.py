# ============================ imports =========================================
from dataclasses import dataclass


@dataclass
class DeviceId:
    """This class encapsulates the defined Device ID of a txp device.

    The Device ID of a device is composed of:
        - The logical_id for the device
        - The physical_id, a piece of information provided by the device which is unique
            for each physical device, in string format

    Args:
        logical_id(str): A logical_id string which is a logical identifier for the
            type of the edge device.
        physical_id(str): A device-specific-unique piece of data.
    """
    logical_id: str = ""
    physical_id: str = ""
