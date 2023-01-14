# import actual context
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Vendoring: add vendor directory to module search path
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, '_vendor')
if os.path.exists(vendor_dir):
    for vendor_path in os.listdir(vendor_dir):
        sys.path.append(os.path.join(vendor_dir, vendor_path))

from .discover import TapoApiDiscover
from plugp100.tapo_protocol.params import SwitchParams, LightParams
from plugp100.api.tapo_api_client import TapoApiClient, TapoApiClientConfig
from plugp100.domain.energy_info import EnergyInfo
from plugp100.domain.tapo_api import TapoApi
from plugp100.domain.tapo_state import TapoDeviceState
from plugp100.domain.tapo_exception import TapoException, TapoError
from plugp100.domain.light_effect import LightEffect

__all__ = [
    "TapoApi",
    "TapoApiClient",
    "LightEffect",
    "TapoApiClientConfig",
    "TapoDeviceState",
    "TapoApiDiscover",
    "EnergyInfo",
    "TapoDeviceState",
    "TapoException",
    "TapoError"
]

__version__ = "2.3.1"
