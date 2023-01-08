import dataclasses
import logging
from typing import Optional, Dict, Any

import aiohttp

from plugp100.domain.light_effect import LightEffect
from plugp100.domain.tapo_api import TapoApi
from plugp100.domain.tapo_state import TapoDeviceState
from plugp100.tapo_protocol.methods import GetDeviceInfoMethod
from plugp100.tapo_protocol.methods.get_energy_usage import GetEnergyUsageMethod
from plugp100.tapo_protocol.params import DeviceInfoParams, SwitchParams, LightParams
from plugp100.tapo_protocol.params.device_info_params import LightEffectParams
from plugp100.tapo_protocol.tapo_protocol_client import TapoProtocolClient

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class TapoApiClientConfig:
    address: str
    username: str
    password: str
    session: Optional[aiohttp.ClientSession] = None


class TapoApiClient(TapoApi):
    TERMINAL_UUID = "88-00-DE-AD-52-E1"

    @staticmethod
    def from_config(config: TapoApiClientConfig) -> 'TapoApiClient':
        return TapoApiClient(
            TapoProtocolClient(config.address, config.username, config.password, config.session)
        )

    def __init__(self, client: TapoProtocolClient):
        self.client = client

    async def login(self) -> bool:
        await self.client.login()
        return True

    async def get_state(self) -> TapoDeviceState:
        state_dict = await self.client.send_tapo_request(GetDeviceInfoMethod(None))
        energy_info = await self.__get_energy_usage()
        return TapoDeviceState(state=state_dict, energy_info=energy_info)

    async def on(self) -> bool:
        return await self.__set_device_state(SwitchParams(True))

    async def off(self) -> bool:
        return await self.__set_device_state(SwitchParams(False))

    async def set_brightness(self, brightness: int) -> bool:
        return await self.__set_device_state(LightParams(brightness=brightness))

    async def set_color_temperature(self, color_temperature: int) -> bool:
        return await self.__set_device_state(LightParams(color_temperature=color_temperature, hue=0, saturation=0))

    async def set_hue_saturation(self, hue: int, saturation: int) -> bool:
        return await self.__set_device_state(LightParams(hue=hue, saturation=saturation, color_temperature=0))

    async def set_light_effect(self, effect: LightEffect) -> bool:
        effect_params = LightEffectParams(enable=1, name=effect.name, brightness=100, display_colors=effect.colors)
        return await self.__set_device_state(LightParams(effect=effect_params, hue=0, saturation=0, color_temperature=0))

    async def __set_device_state(self, device_params: DeviceInfoParams) -> bool:
        try:
            await self.client.set_device_state(device_params, self.TERMINAL_UUID)
            return True
        except Exception as e:
            logger.error("Error during set device state %s", str(e))
            return False

    async def __get_energy_usage(self) -> Optional[Dict[str, Any]]:
        try:
            return await self.client.send_tapo_request(GetEnergyUsageMethod(None))
        except (Exception,):
            return None
