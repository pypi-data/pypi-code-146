"""Const variables."""
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass

SENSOR_DEVICE_CLASSES: tuple[str, ...] = tuple(s.lower() for s in SensorDeviceClass)
BINARY_SENSOR_DEVICE_CLASSES: tuple[str, ...] = tuple(
    s.lower() for s in BinarySensorDeviceClass
)
