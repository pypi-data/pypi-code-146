from __future__ import annotations

from dataclasses import asdict, dataclass
from logging import getLogger

import requests

from . import Config
from .colors import rgb_to_xy
from .state import State

logger = getLogger(__name__)


@dataclass
class Connector:
    base_url: str  # bridge_ip_address / api / user_name
    lights: list[str]

    @classmethod
    def from_config(cls, config: Config) -> Connector:
        if (ip := config.bridge_ip_address) is None:
            raise ValueError(
                """You need to set the ip address of your bridge
                before you can can run any scenes. Use
                >>> hue-sunrise register
                or
                >>> hue-sunrise config ip
                """
            )
        if (user := config.bridge_username) is None:
            raise ValueError(
                """You need to register your hue bridge first.
                Run the following command to do that
                >>> hue-sunrise register
                """
            )

        return Connector(
            base_url=f"http://{ip}/api/{user}",
            lights=config.lights,
        )

    def connect_to_hub(self) -> None:
        response = requests.get(self.base_url)
        if not response.status_code == 200:
            logger.error(
                f"Could not connect due to status code {response.status_code}"
            )
            exit()
        logger.info("Connection successful")

    def get_light_ids(self) -> list[str]:
        response = requests.get(f"{self.base_url}/lights")
        return list(response.json().keys())

    def get_light_product_names(self) -> None:
        for light in self.get_light_ids():
            print(
                requests.get(f"{self.base_url}/lights/{light}").json()[
                    "productname"
                ]
            )

    def check_lights(self) -> None:
        for light in self.lights:
            response = requests.get(f"{self.base_url}/lights/{light}")
            if not response.json()["state"]["reachable"]:
                raise ConnectionError(f"Light {light} is not reachable")

    def send_state(self, state: State) -> None:
        for light in self.lights:
            response = requests.put(
                f"{self.base_url}/lights/{light}/state/",
                json=asdict(
                    state,
                    dict_factory=lambda x: {
                        k: v for k, v in x if v is not None
                    },
                ),
            )
            if response.status_code != 200:
                raise ConnectionError(f"Failed with {response.json()}")

    def get_light_state(self, light: str | None = None) -> State:
        if light is None:
            light = self.lights[0]
        state = requests.get(f"{self.base_url}/lights/{light}").json()["state"]
        return State(
            xy=state["xy"],
            bri=state["bri"],
            sat=state["sat"],
            ct=state["ct"],
            on=state["on"],
        )

    def turn_off(self) -> None:
        logger.info("Turning off")
        self.send_state(
            State(
                xy=rgb_to_xy((1, 0, 0)),
                bri=0,
                sat=254,
            )
        )
        self.send_state(State(on=False))
