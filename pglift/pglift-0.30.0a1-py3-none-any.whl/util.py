import importlib.resources
import logging
import os
import secrets
import shutil
import string
import tempfile
from pathlib import Path
from types import TracebackType
from typing import Any, Optional, Tuple, Type

import humanize

from . import __name__ as pkgname
from . import cmd, exceptions
from .types import CommandRunner

logger = logging.getLogger(__name__)


def template(*args: str) -> str:
    """Return the content of a configuration file template, either found in site configuration or in distribution data."""
    file_content = site_config(*args)
    assert file_content is not None
    return file_content


def etc() -> Path:
    return Path("/etc")


def xdg_config_home() -> Path:
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))


def xdg_data_home() -> Path:
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))


def xdg_runtime_dir(uid: int) -> Path:
    return Path(os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{uid}"))


def etc_config(*parts: str) -> Optional[Path]:
    """Return content of a configuration file in /etc."""
    config = (etc() / pkgname).joinpath(*parts)
    if config.exists():
        return config
    return None


def xdg_config(*parts: str) -> Optional[Path]:
    """Return content of a configuration file in $XDG_CONFIG_HOME."""
    config = (xdg_config_home() / pkgname).joinpath(*parts)
    if config.exists():
        return config
    return None


def custom_config(*parts: str) -> Optional[Path]:
    """Return content of a configuration file in $PGLIFT_CONFIG_PATH."""
    env = os.environ.get("PGLIFT_CONFIG_PATH", None)
    if env:
        path = Path(env)
        assert path.exists(), f"{env} (set via PGLIFT_CONFIG_PATH) does not exist"
        config = path.joinpath(*parts)
        if config.exists():
            return config
    return None


def dist_config(*parts: str) -> Optional[str]:
    """Return content of a configuration file in distribution resources."""
    subpkgs, resource_name = parts[:-1], parts[-1]
    pkg = ".".join([pkgname] + list(subpkgs))
    if importlib.resources.is_resource(pkg, resource_name):
        return importlib.resources.read_text(pkg, resource_name)
    return None


def site_config(*args: str) -> Optional[str]:
    """Lookup for a configuration data in user or site configuration, prior
    to distribution.
    """
    for hdlr in (custom_config, xdg_config, etc_config):
        config = hdlr(*args)
        if config:
            return config.read_text()
    return dist_config(*args)


def with_header(content: str, header: str) -> str:
    """Possibly insert `header` on top of `content`.

    >>> print(with_header("blah", "% head"))
    % head
    blah
    >>> with_header("content", "")
    'content'
    """
    if header:
        content = "\n".join([header, content])
    return content


def generate_certificate(*, run_command: CommandRunner = cmd.run) -> Tuple[str, str]:
    """Generate a self-signed certificate as (crt, key) content."""
    r = run_command(["openssl", "genrsa", "2048"], capture_output=True, check=True)
    key = r.stdout
    with tempfile.NamedTemporaryFile("w") as tempkey:
        tempkey.write(key)
        tempkey.seek(0)
        out = run_command(
            ["openssl", "req", "-new", "-text", "-key", tempkey.name, "-batch"],
            check=True,
        ).stdout
        with tempfile.NamedTemporaryFile("w") as tempcert:
            tempcert.write(out)
            tempcert.seek(0)
            r = run_command(
                [
                    "openssl",
                    "req",
                    "-x509",
                    "-text",
                    "-in",
                    tempcert.name,
                    "-key",
                    tempkey.name,
                ],
                capture_output=True,
                check=True,
            )
            crt = r.stdout

    return crt, key


def generate_password(length: int = 32, letters: bool = True) -> str:
    assert length >= 2
    available_char = string.digits
    if letters:
        available_char += string.ascii_letters
    while True:
        password = [secrets.choice(available_char) for _ in range(length)]
        has_digit = any(c.isdigit() for c in password)
        if (not letters and has_digit) or (
            letters and has_digit and any(c.isalpha() for c in password)
        ):
            break
    return "".join(password)


def short_version(version: int) -> str:
    """Convert a server version as per PQServerVersion to a major version string

    >>> short_version(90603)
    '9.6'
    >>> short_version(100001)
    '10'
    >>> short_version(110011)
    '11'
    """
    ret = version / 10000
    if ret < 10:
        ret = int(ret) + int(version % 1000 / 100) / 10
    else:
        ret = int(ret)
    return str(ret)


def parse_filesize(value: str) -> float:
    """Parse a file size string as float, in bytes unit.

    >>> parse_filesize("6022056 kB")
    6166585344.0
    >>> parse_filesize("0")
    Traceback (most recent call last):
        ...
    ValueError: malformatted file size '0'
    >>> parse_filesize("5 km")
    Traceback (most recent call last):
        ...
    ValueError: invalid unit 'km'
    >>> parse_filesize("5 yb")
    Traceback (most recent call last):
        ...
    ValueError: invalid unit 'yb'
    """
    units = ["B", "K", "M", "G", "T"]
    try:
        val, unit = value.split(None, 1)
        mult, b = list(unit)
    except ValueError:
        raise ValueError(f"malformatted file size '{value}'") from None
    if b.lower() != "b":
        raise ValueError(f"invalid unit '{unit}'")
    try:
        scale = units.index(mult.upper())
    except ValueError:
        raise ValueError(f"invalid unit '{unit}'") from None
    assert isinstance(scale, int)
    return (1024**scale) * float(val)  # type: ignore[no-any-return]


def total_memory(path: Path = Path("/proc/meminfo")) -> float:
    """Read 'MemTotal' field from /proc/meminfo.

    :raise ~exceptions.SystemError: if reading the value failed.
    """
    with path.open() as meminfo:
        for line in meminfo:
            if not line.startswith("MemTotal:"):
                continue
            return parse_filesize(line.split(":", 1)[-1].strip())
        else:
            raise exceptions.SystemError(
                f"could not retrieve memory information from {path}"
            )


def percent_memory(value: str, total: float) -> str:
    """Convert 'value' from a percentage of total memory into a memory setting
    or return (as is if not a percentage value).

    >>> percent_memory(" 1GB", 1)
    '1GB'
    >>> percent_memory("25%", 4e9)
    '1 GB'
    >>> percent_memory("xyz%", 3e9)
    Traceback (most recent call last):
      ...
    ValueError: invalid percent value 'xyz'
    """
    value = value.strip()
    if value.endswith("%"):
        value = value[:-1].strip()
        try:
            percent_value = float(value) / 100
        except ValueError:
            raise ValueError(f"invalid percent value '{value}'")
        value = humanize.naturalsize(total * percent_value, format="%d")
    return value


def rmdir(path: Path) -> bool:
    """Try to remove 'path' directory, log a warning in case of failure,
    return True upon success.
    """
    try:
        path.rmdir()
        return True
    except OSError as e:
        logger.warning("failed to remove directory %s: %s", path, e)
        return False


def rmtree(path: Path, ignore_errors: bool = False) -> None:
    def log(
        func: Any,
        thispath: Any,
        exc_info: Tuple[Type[BaseException], BaseException, TracebackType],
    ) -> None:
        logger.warning(
            "failed to delete %s during tree deletion of %s: %s",
            thispath,
            path,
            exc_info[1],
        )

    shutil.rmtree(path, ignore_errors=ignore_errors, onerror=log)
