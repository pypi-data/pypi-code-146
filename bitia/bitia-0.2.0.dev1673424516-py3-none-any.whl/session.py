"""API module. Uses session to avoid redundant connections"""
import requests
import pickle

import bitia.config as bconfig
from bitia.logger import logger

g_session = requests.Session()
SESSION_PICKLE_FILE = bconfig.bitia_dir() / ".session.pickle"


def fetch_logs(container: str, *, server, timestamps: bool = True):
    """Fetch logs from a container."""
    logger.info(f"Fetching logs for container `{container}`")
    return get(
        f"{server}/container/logs",
        params=dict(container=container, timestamps=timestamps),
        stream=True,
    )


def save_session():
    """Save the current requests session as pickle"""
    global g_session
    with SESSION_PICKLE_FILE.open("wb") as fsession:
        pickle.dump(g_session, fsession)


def load_session(force_new: bool = False):
    """Load the pickled session."""
    global g_session
    if force_new:
        g_session = requests.Session()
        return
    if not SESSION_PICKLE_FILE.is_file():
        g_session = requests.Session()
        return
    with SESSION_PICKLE_FILE.open("rb") as fsession:
        try:
            logger.info(f"Loading session from {fsession.name}")
            g_session = pickle.load(fsession)
        except Exception:
            g_session = requests.Session()


def post(*args, **kwargs):
    return g_session.post(*args, **kwargs)


def get(*args, **kwargs):
    return g_session.get(*args, **kwargs)
