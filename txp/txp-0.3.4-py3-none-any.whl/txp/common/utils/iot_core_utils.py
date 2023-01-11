"""
    This module provides functions and classes that helps with programmatic interaction with
    IoT core service.
"""

from google.cloud import iot_v1
import logging
from datetime import datetime
from txp.common.config import settings


class IoTDevice:
    """A wrapper dataclass for the Device type from iot_v1 library:

    https://googleapis.dev/python/cloudiot/latest/iot_v1/types.html#google.cloud.iot_v1.types.Device
    """
    def __init__(self, device_response):
        self.heartbeat: datetime = datetime(
            device_response.last_heartbeat_time.year,
            device_response.last_heartbeat_time.month,
            device_response.last_heartbeat_time.day,
            device_response.last_heartbeat_time.hour,
            device_response.last_heartbeat_time.minute,
            device_response.last_heartbeat_time.second
        )

        self.last_config_ack: datetime = datetime(
            device_response.last_config_ack_time.year,
            device_response.last_config_ack_time.month,
            device_response.last_config_ack_time.day,
            device_response.last_config_ack_time.hour,
            device_response.last_config_ack_time.minute,
            device_response.last_config_ack_time.second
        )

        self.last_error_msg: str = device_response.last_error_status.message

        self.last_error_time: datetime = datetime(
            device_response.last_error_time.year,
            device_response.last_error_time.month,
            device_response.last_error_time.day,
            device_response.last_error_time.hour,
            device_response.last_error_time.minute,
            device_response.last_error_time.second
        )

        self.last_state_time: datetime = datetime(
            device_response.last_state_time.year,
            device_response.last_state_time.month,
            device_response.last_state_time.day,
            device_response.last_state_time.hour,
            device_response.last_state_time.minute,
            device_response.last_state_time.second
        )


log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


def get_authenticate_client(service_account_credentials) -> iot_v1.DeviceManagerClient:
    """Returns a Device Manager client authenticated to perform operations against Core IoT.

    The google.cloud.iot_v1.types.Device instance for the selected device.

    https://googleapis.dev/python/cloudiot/latest/iot_v1/device_manager.html
    """
    # Create a client
    client = iot_v1.DeviceManagerClient(
        credentials=service_account_credentials
    )
    return client


def get_device_state(
    iot_client: iot_v1.DeviceManagerClient,
    project_id: str,
    cloud_region: str,
    registry_id: str,
    gateway_id: str,
) -> IoTDevice:
    """
    Args:
        iot_client: The IoT core device client.
        project_id: The project ID to which the device belong.
        cloud_region:
        registry_id:
        gateway_id:

    Returns:

    """
    device_path = iot_client.device_path(
        project_id,
        cloud_region,
        registry_id,
        gateway_id
    )

    response = iot_client.get_device(
        name=device_path
    )

    if response:
        device_instance = IoTDevice(response)
        return device_instance
    else:
        return None







