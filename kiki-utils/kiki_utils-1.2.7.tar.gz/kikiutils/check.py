import os
import platform
import re
import subprocess


ALLOWED_EMAILS = [
    'gmail.com',
    'yahoo.com',
    'hotmail.com',
    'aol.com',
    'hotmail.co.uk',
    'hotmail.fr',
    'msn.com',
    'wanadoo.fr',
    'live.com',
    'hotmail.it',
    'qq.com'
]

PING_PARAM = '-n' if platform.system().lower() == 'windows' else '-c'


# Check

def check_domain(domain: str):
    """Check domain ping."""

    return subprocess.call(['ping', PING_PARAM, '1', domain]) == 0


def check_email(email: str):
    """Check email format and ping the domain."""

    if re.match(r'.*[+\-*/\\;&|\s​].*', email):
        return False

    domain = email.split('@')[-1].lower()
    return True if domain.lower() in ALLOWED_EMAILS else check_domain(domain)


def isbytes(*args):
    """Determine whether it is bytes."""

    return all([isinstance(arg, bytes) for arg in args])


def isdict(*args):
    """Determine whether it is dict."""

    return all([isinstance(arg, dict) for arg in args])


def isdir(*args):
    """Determine whether path is dir."""

    return all([os.path.isdir(arg) for arg in args])


def isfile(*args):
    """Determine whether path is file."""

    return all([os.path.isfile(arg) for arg in args])


def isint(*args):
    """Determine whether it is int."""

    return all([isinstance(arg, int) for arg in args])


def islist(*args):
    """Determine whether it is list."""

    return all([isinstance(arg, list) for arg in args])


def isstr(*args):
    """Determine whether it is str."""

    return all([isinstance(arg, str) for arg in args])
