import os
import time

ENV_LOCAL = "LOCAL"
ENV_VDI = "VDI"
ENV_KNADA_GKE = "KNADA_GKE"
OPPFOLGING_ENVS = (ENV_LOCAL, ENV_VDI, ENV_KNADA_GKE)


def get_oppfolging_environment():
    """gets the current OPPFOLGING_ENV"""
    env = os.getenv("OPPFOLGING_ENV")
    if not env:
        raise Exception("OPPFOLGING_ENVIRONMENT not set")
    elif env not in OPPFOLGING_ENVS:
        raise Exception("Unsupported OPPFOLGING_ENVIRONMENT")
    return env


def set_timezone_to_norwegian_time():
    """sets python session timezone to norwegian time"""
    if get_oppfolging_environment() in (ENV_KNADA_GKE, ENV_VDI):
        os.environ["TZ"] = "Europe/Oslo"
        time.tzset()  # pylint: disable=no-member
    else:
        raise Exception("Cannot set time in this environment")
