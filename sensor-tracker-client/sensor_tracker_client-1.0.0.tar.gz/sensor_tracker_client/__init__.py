__version__ = '1.0.0'

from .sensor_tracker_client import SensorTrackerClient
from .sensor_tracker_proxy import SensorTrackerClientProxy
sensor_tracker_client = SensorTrackerClient()
sensor_tracker_proxy = SensorTrackerClientProxy(sensor_tracker_client)
del SensorTrackerClient
