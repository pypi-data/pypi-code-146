import logging
from threading import Thread
from time import sleep

from .const import AromaTherapy, Calefaction, LampMode, Model
from .message_info import SettingsInfo, StatusInfo
from .server import ToloServer

DEFAULT_UPDATE_FREQUENCY = 1

WATER_HEAT_RATE = 7
HUMIDITY_RATE = 5
TEMPERATURE_RATE = 2


logger = logging.getLogger(__name__)


class Simulator(Thread):
    def __init__(
        self, server: ToloServer, update_frequency: float = DEFAULT_UPDATE_FREQUENCY
    ) -> None:
        super().__init__(daemon=True)
        self._server = server
        self._update_frequency = update_frequency

    @property
    def status(self) -> StatusInfo:
        return self._server.status

    @property
    def settings(self) -> SettingsInfo:
        return self._server.settings

    def _init_settings(self) -> None:
        self.settings.target_temperature = 43
        self.settings.target_humidity = 95
        self.settings.power_timer = 45
        self.settings.salt_bath_timer = 30
        self.settings.aroma_therapy = AromaTherapy.B
        self.settings.sweep_timer = 0
        self.settings.lamp_mode = LampMode.MANUAL
        self.settings.fan_timer = 5

    def _init_status(self) -> None:
        self.status.power_on = False
        self.status.current_temperature = 17
        self.status.power_timer = None
        self.status.flow_in = False
        self.status.flow_out = True
        self.status.calefaction = Calefaction.INACTIVE
        self.status.aroma_therapy_on = False
        self.status.sweep_on = False
        # TODO add descaling
        self.status.lamp_on = False
        self.status.water_level = 0
        self.status.fan_on = False
        self.status.fan_timer = None
        self.status.current_humidity = 52
        self.status.tank_temperature = 17
        self.status.model = Model.DOMESTIC
        self.status.salt_bath_on = False
        self.status.salt_bath_timer = 0

    def _update_status(self) -> None:
        if self.status.power_on:
            # power is on
            self.status.flow_out = False

            if self.status.water_level < 3:
                # water level < 3
                self.status.flow_in = True
                self.status.water_level += 1
            else:
                # water level >= 3
                self.status.flow_in = False

            if self.status.tank_temperature < 100:
                # temperature < 100
                self.status.calefaction = Calefaction.HEAT
                self.status.tank_temperature = int(
                    min(
                        self.status.tank_temperature
                        + self._get_diff_by_rate(WATER_HEAT_RATE),
                        100,
                    )
                )
            else:
                # temperature >= 100
                self.status.calefaction = Calefaction.KEEP

                self.status.current_humidity = int(
                    min(
                        self.status.current_humidity
                        + self._get_diff_by_rate(HUMIDITY_RATE),
                        self.settings.target_humidity,
                    )
                )

                self.status.current_temperature = int(
                    min(
                        self.status.current_temperature
                        + self._get_diff_by_rate(TEMPERATURE_RATE),
                        self.settings.target_temperature,
                    )
                )

        else:
            # power is off
            self.status.flow_in = False
            self.status.calefaction = Calefaction.INACTIVE

            if self.status.water_level > 0:
                self.status.flow_out = True
                self.status.water_level -= 1

            # TODO decrease current_temperature
            # TODO decrease current_humidity
            # TODO decrease tank_temperature

    def _get_diff_by_rate(self, rate: float) -> float:
        return rate * self._update_frequency

    def run(self) -> None:
        logger.debug(
            "simulator started with update frequency of %f second(s)"
            % self._update_frequency
        )
        self._init_settings()
        self._init_status()
        while self.is_alive():
            self._update_status()
            sleep(self._update_frequency)
