import subprocess
from pathlib import Path

from ..logger import get_logger


def to_str(arg: str | bytes | Path) -> str:
    if isinstance(arg, str):
        return arg
    elif isinstance(arg, bytes):
        return str(arg, encoding="utf-8")
    else:
        return str(arg)


def execute(
    *args: str | bytes | Path,
    stdin=None,
    stdout=None,
    stderr=None,
    cwd=None,
    capture_output: bool = False,
    check_returncode: bool = True,
) -> subprocess.CompletedProcess:
    logger = get_logger()
    argv: list[str] = list(map(to_str, args))
    message: str = " ".join(argv)
    if cwd:
        message = f"CWD={cwd} " + message
    logger.execute(msg="+ " + message)
    process: subprocess.CompletedProcess = subprocess.run(
        args=argv,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        cwd=cwd,
        capture_output=capture_output,
    )
    if check_returncode:
        process.check_returncode()
    return process
