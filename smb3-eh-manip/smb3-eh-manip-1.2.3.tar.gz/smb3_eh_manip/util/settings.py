from configparser import ConfigParser
import logging

config = ConfigParser()
result = config.read("config.ini")
if not result:
    logging.warning("Failed to read config.ini! Using sample.")
    config.read("config.ini.sample")

NES_FRAMERATE = 1008307711 / 256 / 65536
NES_MS_PER_FRAME = 1000.0 / NES_FRAMERATE
DEFAULT_DOMAIN = "app"
FREQUENCY = 24


def get(name, domain=DEFAULT_DOMAIN, fallback=None):
    return config.get(domain, name, fallback=fallback)


def get_boolean(name, domain=DEFAULT_DOMAIN, fallback=None):
    return config.getboolean(domain, name, fallback=fallback)


def get_int(name, domain=DEFAULT_DOMAIN, fallback=None):
    return config.getint(domain, name, fallback=fallback)


def get_config_region(name, domain=DEFAULT_DOMAIN, fallback=None):
    """Parse a region str from ini"""
    return get_list(name, domain=domain, fallback=fallback)


def get_frame_windows(name, domain=DEFAULT_DOMAIN, fallback=None):
    """Parse a frame windows str from ini"""
    frame_windows = config.get(domain, name, fallback=fallback)
    if frame_windows:
        return list(
            map(lambda str: list(map(int, str.split("-"))), frame_windows.split(","))
        )
    return None


def get_list(name, domain=DEFAULT_DOMAIN, fallback=None):
    """Parse a region str from ini"""
    list_str = config.get(domain, name, fallback=fallback)
    if list_str:
        return list(map(int, list_str.split(",")))
    return None


def get_action_frames():
    frames = get_list("eh_action_frames")
    return (
        frames
        if frames
        else [270, 1659, 16000, 16828, 18046, 18654, 19947, 20611, 22670, 23952]
    )


def set(name, value, domain=DEFAULT_DOMAIN):
    return config.set(domain, name, value)


ACTION_FRAMES = get_action_frames()
