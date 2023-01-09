from __future__ import annotations

import time
from logging import getLogger

from . import Config
from .colors import rgb_to_xy
from .connector import Connector
from .state import State

logger = getLogger(__name__)


def prepare(con: Connector) -> None:
    """Set light to complete red, to avoid short burst of bright light"""
    con.send_state(
        State(
            on=True,
            xy=rgb_to_xy((1, 0, 0)),
            bri=0,
            sat=254,
        )
    )


def scene_1(con: Connector, scene_length_min: float) -> None:
    """Start at dark red and slowly brighten, as well as
    add in green to get an orangy color"""
    logger.info("Starting scene 1")
    step_time_s = (scene_length_min * 60) / 255
    for i in range(255):
        con.send_state(
            State(
                xy=rgb_to_xy((1, i / (255 * 5), 0)),
                bri=i,
            )
        )
        time.sleep(step_time_s)
    logger.info("Finished scene 1")


def scene_2(con: Connector, scene_length_min: float) -> None:
    """Decrease color temperature, to get more white into the color.

    I tried this first with saturation,
    but then it goes into hue-saturation mode,
    which doesn't work, as those weird lights don't understand hue.
    """
    n_decrease = 100
    logger.info("Starting scene 2")
    step_time_s = (scene_length_min * 60) / n_decrease
    if (current_color_temperature := con.get_light_state().ct) is not None:
        for i in range(
            current_color_temperature,
            current_color_temperature - n_decrease,
            -1,
        ):
            con.send_state(State(ct=i))
            time.sleep(step_time_s)
    else:
        raise ValueError("color temperature is None")
    logger.info("Finished scene 2")


def afterglow(scene_length_min: float) -> None:
    """Keep the lights on for a few minutes"""
    logger.info(f"Afterglow for {scene_length_min} minutes")
    time.sleep(scene_length_min * 60)
    logger.info("Finished afterglow")


def sunrise(con: Connector, config: Config) -> None:
    con.connect_to_hub()  # not strictly necessary, but a nice check
    con.check_lights()  # raise error when lights are not reachable
    prepare(con=con)
    scene_1(con=con, scene_length_min=config.total_scene_length_min / 2)
    scene_2(con=con, scene_length_min=config.total_scene_length_min / 2)
    afterglow(scene_length_min=config.afterglow_length_min)
    con.turn_off()
