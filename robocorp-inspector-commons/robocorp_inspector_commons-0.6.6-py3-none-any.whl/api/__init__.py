from inspector_commons.utils import IS_WINDOWS

from .bridge_interface import BrowserBridgeConnector, RecorderBridgeConnector
from .database_interface import DatabaseConnector

if IS_WINDOWS:
    from .bridge_interface import WindowsBridgeConnector
