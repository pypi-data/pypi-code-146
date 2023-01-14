import shlex
import subprocess
from pathlib import Path

from ..log import Action, get_logger


def run(
    *args: str | Path,
    stdin=None,
    stdout=None,
    stderr=None,
    cwd=None,
    capture_output: bool = False,
    check_returncode: bool = True,
) -> subprocess.CompletedProcess:
    logger = get_logger()
    logger.running(action=Action.RUN, message="+ " + shlex.join(list(map(str, args))))
    process: subprocess.CompletedProcess = subprocess.run(
        args=args,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        cwd=cwd,
        capture_output=capture_output,
    )
    if check_returncode:
        process.check_returncode()
    return process
