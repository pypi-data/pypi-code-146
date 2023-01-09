from __future__ import annotations

from dataclasses import asdict
from logging import getLogger

import requests
import typer
from typing import Optional

from . import Config
from .connector import Connector
from .scene import sunrise

logger = getLogger(__name__)

app = typer.Typer()
config_app = typer.Typer()
app.add_typer(config_app, name="config")


@app.command()
def register() -> None:
    config = Config.from_file()
    if config.bridge_ip_address is None:
        config.set_ip(input(">>> Input your hue IP address: "))

    input(">>> Press the button on your hue bridge, then hit enter")
    username = requests.post(
        f"http://{config.bridge_ip_address}/api",
        json={"devicetype": "python_hue"},
    ).json()
    config.set_username(username)


@app.command()
def run(
    scene_length_min: Optional[int] = typer.Option(None),
    afterglow_length_min: Optional[int] = typer.Option(None),
    lights: list[str] = typer.Option([]),
) -> None:
    config = Config.from_file()
    if scene_length_min is not None:
        config.total_scene_length_min = scene_length_min
    if afterglow_length_min is not None:
        config.afterglow_length_min = afterglow_length_min
    if len(lights) > 0:
        config.lights = lights
    con = Connector.from_config(config)
    try:
        sunrise(con, config)
    except ConnectionError:
        logger.error("Connection error, exiting...")
        exit()
    except KeyboardInterrupt:
        con.turn_off()
        exit()
    except Exception as e:
        logger.error("Unexpected error:", exc_info=e)
        con.turn_off()
        exit()


@app.command()
def shutdown() -> None:
    config = Config.from_file()
    con = Connector.from_config(config)
    logger.error("Received SIGTERM, shutting down")
    con.turn_off()


@config_app.command("show")
def get_config() -> None:
    config = Config.from_file()
    for k, v in asdict(config).items():
        print(f"{k:<25} :: {v}")


@config_app.command("ip")
def set_bridge_ip(bridge_ip: str) -> None:
    config = Config.from_file()
    config.set_ip(bridge_ip)
    print("Set bridge ip to", bridge_ip)


@config_app.command("user")
def set_username(username: str) -> None:
    config = Config.from_file()
    config.set_username(username)
    print("Set bridge username to", username)


@config_app.command("lights")
def set_lights(lights: list[str]) -> None:
    config = Config.from_file()
    config.set_lights(lights)
    print("Set lights to", lights)


@config_app.command("scene-length")
def set_scene_length(minutes: int) -> None:
    config = Config.from_file()
    config.set_total_scene_length_min(minutes)
    print("Set total_scene_length_min to", minutes)


@config_app.command("afterglow")
def set_afterglow(minutes: int) -> None:
    config = Config.from_file()
    config.set_afterglow_length_min(minutes)
    print("Set afterglow_length_min to", minutes)


@config_app.command("reset")
def reset_config() -> None:
    Config.from_file().reset()


if __name__ == "__main__":
    app()
