import asyncio
import asyncio.subprocess
import enum
import logging
import os
import shlex
import signal
import subprocess
from asyncio import create_task
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from functools import partial
from pathlib import Path
from subprocess import PIPE, TimeoutExpired
from types import TracebackType
from typing import IO, Any, Mapping, Optional, Sequence, Tuple, Type, Union

from . import exceptions
from .types import AutoStrEnum, CompletedProcess

logger = logging.getLogger(__name__)


class _CloneStderrProtocol(asyncio.subprocess.SubprocessStreamProtocol):
    """Subprocess protocol extending the default one to handle a clone of stderr stream."""

    def __init__(
        self,
        stderr_reader: Optional[asyncio.StreamReader],
        *,
        limit: int,
        loop: asyncio.events.AbstractEventLoop,
    ) -> None:
        super().__init__(limit=limit, loop=loop)
        self._stderr_reader = stderr_reader

    def __repr__(self) -> str:
        base = super().__repr__()[1:-1]
        if self._stderr_reader:
            base += f" stderr(clone)={self._stderr_reader}"
        return f"<{base}>"

    def pipe_data_received(self, fd: int, data: Union[bytes, str]) -> None:
        super().pipe_data_received(fd, data)
        if fd == 2 and self._stderr_reader:
            assert isinstance(data, bytes)
            self._stderr_reader.feed_data(data)

    def pipe_connection_lost(self, fd: int, exc: Optional[Exception]) -> None:
        super().pipe_connection_lost(fd, exc)
        if fd == 2 and self._stderr_reader:
            if exc:
                self._stderr_reader.set_exception(exc)
            else:
                self._stderr_reader.feed_eof()


@asynccontextmanager
async def logged_subprocess_exec(
    program: str,
    *args: str,
    stdin: Union[int, IO[Any], None] = None,
    stdout: Union[int, IO[Any], None] = None,
    stderr: Union[int, IO[Any], None] = None,
    **kwds: Any,
) -> AsyncIterator[asyncio.subprocess.Process]:
    """Context manager starting an asyncio Process while possibly processing its
    stderr stream with 'stderr_handler' callback.

    This is similar quite to asyncio.subprocess.create_subprocess_exec() but
    with a custom protocol to install a cloned stream for stderr.
    """
    loop = asyncio.get_event_loop()
    task = None
    cloned_stderr = None
    if stderr is not None:
        cloned_stderr = asyncio.StreamReader()

        async def handle_stderr(stream: asyncio.StreamReader) -> None:
            async for line in stream:
                logger.debug("%s: %s", program, line.decode("utf-8").rstrip())

        task = create_task(handle_stderr(cloned_stderr))

    protocol_factory = partial(
        _CloneStderrProtocol,
        cloned_stderr,
        limit=2**16,  # asyncio.streams._DEFAULT_LIMIT
        loop=loop,
    )
    transport, protocol = await loop.subprocess_exec(
        protocol_factory,
        program,
        *args,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        **kwds,
    )

    try:
        yield asyncio.subprocess.Process(transport, protocol, loop)
    finally:
        if task and not task.done():
            task.cancel()


def run(
    args: Sequence[str],
    *,
    input: Optional[str] = None,
    check: bool = False,
    timeout: Optional[float] = None,
    **kwargs: Any,
) -> CompletedProcess:
    """Run a command as a subprocess while forwarning its stderr to module 'logger'.

    Standard output and errors of child subprocess are captured by default.

    >>> run(["true"], input="a", capture_output=False)
    CompletedProcess(args=['true'], returncode=0)

    Files can also be used with ``stdout`` and ``stderr`` arguments:

    >>> import tempfile
    >>> with tempfile.NamedTemporaryFile() as f:
    ...     _ = run(["echo", "ahah"], stdout=f, stderr=None)
    ...     with open(f.name) as f:
    ...         print(f.read(), end="")
    ahah

    >>> r = run(["cat", "doesnotexist"], stdout=PIPE, stderr=PIPE, env={"LANG": "C"})
    >>> print(r.stderr, end="")
    cat: doesnotexist: No such file or directory

    With ``check=True``, :class:`~pglift.exceptions.CommandError` is raised
    in case of non-zero return code:

    >>> run(["cat", "doesnotexist"], check=True)
    Traceback (most recent call last):
        ...
    pglift.exceptions.CommandError: Command '['cat', 'doesnotexist']' returned non-zero exit status 1.

    With a non-None timeout argument, a :class:`~subprocess.TimeoutExpired`
    exception might be raised:

    >>> run(["sleep", "0.1"], timeout=0.01)
    Traceback (most recent call last):
        ...
    subprocess.TimeoutExpired: Command '['sleep', '0.1']' timed out after 0.01 seconds
    """
    if not args:
        raise ValueError("empty arguments sequence")

    if input is not None:
        if "stdin" in kwargs:
            raise ValueError("stdin and input arguments may not both be used")
        kwargs["stdin"] = PIPE

    try:
        capture_output = kwargs.pop("capture_output")
    except KeyError:
        kwargs.setdefault("stdout", subprocess.PIPE)
        kwargs.setdefault("stderr", subprocess.PIPE)
    else:
        if capture_output:
            if "stdout" in kwargs or "stderr" in kwargs:
                raise ValueError(
                    "stdout and stderr arguments may not be used with capture_output"
                )
            kwargs["stdout"] = kwargs["stderr"] = subprocess.PIPE

    loop = asyncio.get_event_loop()

    async def run() -> Tuple[asyncio.subprocess.Process, Optional[str], Optional[str]]:
        async with logged_subprocess_exec(*args, **kwargs) as proc:
            aw = proc.communicate(input.encode("utf-8") if input is not None else None)
            if timeout is None:
                out, err = await aw
            else:
                try:
                    out, err = await asyncio.wait_for(aw, timeout)
                except asyncio.TimeoutError:
                    raise TimeoutExpired(args, timeout) from None
        assert proc.returncode is not None
        return (
            proc,
            out.decode("utf-8") if out is not None else None,
            err.decode("utf-8") if err is not None else None,
        )

    proc, out, err = loop.run_until_complete(run())

    if check and proc.returncode:
        raise exceptions.CommandError(proc.returncode, args, out, err)

    assert proc.returncode is not None
    return CompletedProcess(args, proc.returncode, out, err)


def execute_program(
    cmd: Sequence[str], *, env: Optional[Mapping[str, str]] = None
) -> None:
    """Execute program described by 'cmd', replacing the current process.

    :raises ValueError: if program path is not absolute.
    """
    program = cmd[0]
    if not Path(program).is_absolute():
        raise ValueError(f"expecting an absolute program path {program}")
    logger.debug("executing program '%s'", shlex.join(cmd))
    if env is not None:
        os.execve(program, list(cmd), env)  # nosec
    else:
        os.execv(program, list(cmd))  # nosec


class Status(AutoStrEnum):
    running = enum.auto()
    not_running = enum.auto()
    dangling = enum.auto()


def status_program(pidfile: Path) -> Status:
    """Return the status of a program which PID is in 'pidfile'.

    :raises ~exceptions.SystemError: if the program is already running.
    :raises ~exceptions.CommandError: in case program execution terminates
        after `timeout`.
    """
    if pidfile.exists():
        with pidfile.open() as f:
            pid = f.readline().rstrip()
        if (Path("/proc") / pid).exists():
            return Status.running
        else:
            return Status.dangling
    return Status.not_running


class Program:
    """Start program described by 'cmd' and possibly store its PID in 'pidfile'.

    This is aimed at starting daemon programs.

    :raises ~exceptions.SystemError: if the program is already running.
    :raises ~exceptions.CommandError: in case program execution terminates
        after `timeout`.

    When used as a context manager, any exception raised within the block will
    trigger program termination at exit. This can be used to perform sanity
    checks shortly after program startup.
    """

    def __init__(
        self,
        cmd: Sequence[str],
        pidfile: Optional[Path],
        *,
        timeout: float = 1,
        env: Optional[Mapping[str, str]] = None,
        capture_output: bool = True,
    ) -> None:
        self.pidfile = pidfile
        self.program = cmd[0]
        self.args = cmd
        self.proc = self._start(
            cmd, timeout=timeout, env=env, capture_output=capture_output
        )

    def _start(
        self,
        cmd: Sequence[str],
        *,
        timeout: float = 1,
        env: Optional[Mapping[str, str]] = None,
        capture_output: bool = True,
    ) -> asyncio.subprocess.Process:
        if self.pidfile is not None:
            self._check_pidfile()
        stdout = stderr = None
        if capture_output:
            stdout = stderr = subprocess.PIPE
        logger.debug("starting program '%s'", shlex.join(cmd))

        async def run() -> asyncio.subprocess.Process:
            async with logged_subprocess_exec(
                *cmd, stdout=stdout, stderr=stderr, env=env
            ) as proc:
                aw = proc.communicate()
                try:
                    __, errs = await asyncio.wait_for(aw, timeout)
                except asyncio.TimeoutError:
                    if self.pidfile is not None:
                        self.pidfile.parent.mkdir(parents=True, exist_ok=True)
                        self.pidfile.write_text(str(proc.pid))
                    return proc
                else:
                    assert proc.returncode is not None
                    assert (
                        proc.returncode != 0
                    ), f"{self.program} terminated with exit code 0"
                    raise exceptions.CommandError(
                        proc.returncode,
                        cmd,
                        stderr=errs.decode("utf-8") if errs is not None else None,
                    )

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(run())

    def _check_pidfile(self) -> None:
        """Use specified pidfile, when not None, to check if the program is
        already running or dangling.
        """
        pidfile = self.pidfile
        assert pidfile is not None
        status = status_program(pidfile)
        if status in (Status.running, Status.dangling):
            pid = pidfile.read_text()
            if status == Status.running:
                raise exceptions.SystemError(
                    f"program {self.program} seems to be running already with PID {pid}"
                )
            elif status == Status.dangling:
                logger.warning(
                    "program %s is supposed to be running with PID %s but "
                    "it's apparently not; starting anyway",
                    self.program,
                    pid,
                )
                pidfile.unlink()

    def __enter__(self) -> "Program":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: BaseException,
        traceback: Optional[TracebackType],
    ) -> None:
        if exc_value is not None:
            cmd = shlex.join(self.args)
            logger.warning("terminating program '%s'", cmd)
            try:
                self.proc.terminate()
            except ProcessLookupError:
                logger.debug("program %s already terminated", self.args[0])
            if self.proc.stderr is not None:

                async def exit(stderr: asyncio.StreamReader) -> None:
                    async for line in stderr:
                        logger.debug(
                            "%s: %s", self.program, line.decode("utf-8").rstrip()
                        )

                loop = asyncio.get_event_loop()
                loop.run_until_complete(exit(self.proc.stderr))
            if self.pidfile is not None:
                self.pidfile.unlink()
            raise exc_value


def terminate_program(pidfile: Path) -> None:
    """Terminate program matching PID in 'pidfile'.

    Upon successful termination, the 'pidfile' is removed.
    No-op if no process matching PID from 'pidfile' is running.
    """
    status = status_program(pidfile)
    if status == Status.not_running:
        logger.warning("program from %s not running", pidfile)
        return
    elif status == Status.dangling:
        logger.debug("removing dangling PID file %s", pidfile)
        pidfile.unlink()
        return

    with pidfile.open() as f:
        pid = int(f.readline().rstrip())
    logger.debug("terminating process %d", pid)
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError as e:
        logger.warning("failed to kill process %d: %s", pid, e)
    pidfile.unlink()


def _main() -> None:
    import argparse
    import logging
    import sys

    logger = logging.getLogger("stderr")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter(fmt="%(asctime)s - %(message)s", datefmt="[%Xs]")
    )
    logger.addHandler(handler)

    parser = argparse.ArgumentParser(
        __name__,
        description="Run, start or terminate programs while logging their stderr",
    )
    subparsers = parser.add_subparsers(title="Commands")

    run_parser = subparsers.add_parser(
        "run",
        description="Run PROGRAM with positional ARGuments.",
        epilog=f"Example: {__name__} run initdb /tmp/pgdata --debug",
    )
    run_parser.add_argument("program", metavar="PROGRAM")
    run_parser.add_argument("arguments", metavar="ARG", nargs="*")

    def run_func(args: argparse.Namespace, remaining: Sequence[str]) -> None:
        cmd = [args.program] + args.arguments + list(remaining)
        run(cmd, check=True, logger=logger)

    run_parser.set_defaults(func=run_func)

    start_parser = subparsers.add_parser(
        "start",
        description="Start PROGRAM with positional ARGuments.",
        epilog=f"Example: {__name__} start postgres -D /tmp/pgdata -k /tmp",
    )
    start_parser.add_argument("program", metavar="PROGRAM")
    start_parser.add_argument("arguments", metavar="ARG", nargs="*")
    start_parser.add_argument(
        "-p",
        "--pidfile",
        type=Path,
        help="Path to file where PID will be stored.",
    )
    start_parser.add_argument(
        "--timeout", type=float, default=1, help="Liveliness timeout."
    )

    def start_func(args: argparse.Namespace, remaining: Sequence[str]) -> None:
        cmd = [args.program] + args.arguments + list(remaining)
        with Program(cmd, pidfile=args.pidfile, timeout=args.timeout) as p:
            print(f"Program {args.program} running with PID {p.proc.pid}")

    start_parser.set_defaults(func=start_func)

    terminate_parser = subparsers.add_parser("terminate")
    terminate_parser = subparsers.add_parser(
        "terminate",
        description="Terminate process from PIDFILE.",
        epilog=f"Example: {__name__} terminate /tmp/pgdata/postmaster.pid",
    )
    terminate_parser.add_argument("pidfile", metavar="PIDFILE", type=Path)

    def terminate_func(args: argparse.Namespace, remaining: Sequence[str]) -> None:
        terminate_program(args.pidfile)

    terminate_parser.set_defaults(func=terminate_func)

    ns, remaining = parser.parse_known_args()
    ns.func(ns, remaining)


if __name__ == "__main__":
    _main()
