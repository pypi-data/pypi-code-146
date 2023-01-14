import shlex
import subprocess

from ..log import Action, get_logger


def run(*args: str) -> subprocess.CompletedProcess:
    logger = get_logger()
    logger.running(action=Action.RUN, message="+ " + shlex.join(args))
    complete: subprocess.CompletedProcess = subprocess.run(args=args)
    return complete
