from abc import ABCMeta, abstractmethod


from plugp100.domain.tapo_state import TapoDeviceState
from plugp100.tapo_protocol.params import LightEffectData


class TapoApi:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def login(self) -> bool: raise NotImplementedError

    @abstractmethod
    async def get_state(self) -> TapoDeviceState: raise NotImplementedError

    @abstractmethod
    async def on(self) -> bool: raise NotImplementedError

    @abstractmethod
    async def off(self) -> bool: raise NotImplementedError

    @abstractmethod
    async def set_brightness(self, brightness: int) -> bool: raise NotImplementedError

    @abstractmethod
    async def set_color_temperature(self, color_temperature: int) -> bool: raise NotImplementedError

    @abstractmethod
    async def set_hue_saturation(self, hue: int, saturation: int) -> bool: raise NotImplementedError

    @abstractmethod
    async def set_light_effect(self, effect: LightEffectData) -> bool: raise NotImplementedError
