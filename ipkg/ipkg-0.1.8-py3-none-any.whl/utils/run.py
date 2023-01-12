import subprocess
import sys

from ..log import get_logger


def run(*args: str, capture_output: bool = False) -> subprocess.CompletedProcess:
    logger = get_logger()
    logger.execute(msg="+ " + " ".join(args))
    return subprocess.run(args=args, stdin=sys.stdin, capture_output=capture_output)
