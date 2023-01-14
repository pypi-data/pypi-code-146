import functools
import subprocess

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def execute_shell(cmd, timeout, verbose=False):
    if isinstance(cmd, str):
        cmd = cmd.split()

    if verbose:
        print("Command: ", " ".join(cmd))

    stdout_ = ""
    stderr_ = ""
    returncode = None
    timed_out = False

    try:
        res = subprocess.run(cmd, capture_output=True, timeout=timeout)
        stdout_ = res.stdout.decode("utf-8")
        stderr_ = res.stderr.decode("utf-8")
        returncode = res.returncode
    except subprocess.CalledProcessError as e:
        stdout_ = e.stdout.decode("utf-8") if e.stdout else e.stdout
        stderr_ = e.stderr.decode("utf-8") if e.stderr else e.stderr
        returncode = e.returncode
    except subprocess.TimeoutExpired as e:
        stdout_ = e.stdout.decode("utf-8") if e.stdout else e.stdout
        stderr_ = e.stderr.decode("utf-8") if e.stderr else e.stderr
        returncode = 124  # Usual shell error code for timeouts
        timed_out = True

    # TODO Handle other types of exceptions
    return stdout_, stderr_, returncode, timed_out


def get_session():
    session = requests.Session()

    # Retry for:
    # Request Timeout, Locked, Too Early, Too Many Requests
    # Internal Server Error, Gateway Timeout
    retries = Retry(total=5, backoff_factor=0.2, status_forcelist=[408, 423, 425, 429, 500, 504])

    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.mount("https://", HTTPAdapter(max_retries=retries))

    # set timeout to 15s
    session.request = functools.partial(session.request, timeout=15)
    return session
