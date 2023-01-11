import importlib
import inspect
import os
import subprocess
import sys
import tarfile
from pathlib import Path
from subprocess import CalledProcessError, CompletedProcess, TimeoutExpired
from typing import Optional, Sequence, Union
from urllib.error import URLError
from urllib.request import urlcleanup, urlretrieve

import click
import requests
from semver import VersionInfo

from .config import ConfigBase, SymConfigFile
from .contexts import push_envs
from .os import has_command, reset_fds

REQ_TIMEOUT = 3
INSTALL_TIMEOUT = 90
FAIL_LOG_PATH = "updater/fail.log"
V0 = VersionInfo.parse("0.0.0")


class SymUpdater:
    def __init__(self, debug: bool = False):
        cli_name = ConfigBase.get_cli_name()
        self.module = importlib.import_module(cli_name.replace("-", "."))
        self.dir = Path(inspect.getfile(self.module)).resolve().parent
        for _ in range(len(cli_name.split("-"))):
            self.dir = self.dir.parent
        self.latest_version: Optional[VersionInfo] = None
        self.url: Optional[dict] = None
        self.cli = cli_name
        self.debug = debug

    def _log(self, s, debug=False, **kwargs):
        if debug and not self.debug:
            return
        click.secho(s, err=True, **kwargs)

    def _fail_log(self, bytes_or_str: Optional[Union[bytes, str]]):
        if not bytes_or_str:
            return

        try:
            log = bytes_or_str.decode("utf-8")
        except (UnicodeDecodeError, AttributeError):
            log = str(bytes_or_str)

        config_file = SymConfigFile(file_name=FAIL_LOG_PATH, uid_scope=False)
        config_file.put(log)
        self._log(f"A log has been written to {config_file.path}", fg="bright_black")

    def should_check(self) -> bool:
        return not self.is_local() and ConfigBase.check_for_update()

    def get_current_version(self) -> VersionInfo:
        try:
            return VersionInfo.parse(self.module.version.__version__)
        except ValueError:
            return V0

    def get_latest_version(self) -> Optional[VersionInfo]:
        try:
            resp = requests.get(
                f"https://pypi.org/pypi/{self.cli}/json",
                timeout=REQ_TIMEOUT,
            ).json()
        except Exception:
            return None

        new_version = self.get_current_version()
        for v in resp.get("releases", {}).keys():
            try:
                version = VersionInfo.parse(v)
            except ValueError:
                continue
            if version > new_version and version.major == new_version.major:
                new_version = version
        self.latest_version = new_version

        try:
            resp2 = requests.get(
                f"https://pypi.org/pypi/{self.cli}/{new_version}/json",
                timeout=REQ_TIMEOUT,
            ).json()
        except Exception:
            return None

        try:
            self.url = next(
                (u for u in resp2["urls"] if u["python_version"] == "source"),
                None,
            )

            version = VersionInfo.parse(resp["info"]["version"])
            if version > new_version:
                self._log(
                    (
                        "A major update is available! "
                        f"Please install it using the install script at https://docs.symops.com/docs/install-{self.cli}."
                    ),
                    fg="white",
                )
        except (ValueError, KeyError):
            pass

        return new_version

    def needs_update(self) -> bool:
        if version := self.get_latest_version():
            return version > self.get_current_version()
        return False

    def _env_is_local(self):
        return (
            os.getenv("SENTRY_ENVIRONMENT") == "development" or os.getenv("CI") == "true"
        )

    def is_local(self):
        return (
            (self.dir / ".git").exists()
            or self.get_current_version() == V0
            or self._env_is_local()
        )

    def is_pipx(self):
        return (Path.home() / ".local" / "pipx") in self.dir.parents

    def is_brew(self):
        return "Cellar" in self.dir.parts

    def is_sitepackage(self):
        return self.dir.name == "site-packages"

    def _update_with_command(
        self, command: Sequence[str], **kwargs
    ) -> Optional[CompletedProcess]:
        if not has_command(command[0]):
            self._log(f"Can't find {command[0]}!", debug=True, fg="red")
            return None
        try:
            return subprocess.run(
                command,
                timeout=INSTALL_TIMEOUT,
                text=True,
                **kwargs,
            )
        except TimeoutExpired as e:
            self._log(
                "Oops! This is taking a little too long, we'll try again later.",
                fg="yellow",
            )
            self._fail_log(e.stderr or e.stdout)
            return None
        except CalledProcessError as e:
            self._log(f"{e.returncode}: {e.stderr or e.stdout}", debug=True, fg="red")
            self._fail_log(e.stderr or e.stdout)
            return None

    def _update_with_checked_command(self, command: Sequence[str], **kwargs):
        return bool(
            self._update_with_command(
                command,
                check=True,
                capture_output=True,
                **kwargs,
            )
        )

    def update_pipx(self) -> bool:
        self._log(
            f"Using pipx. You can also manually run `pipx upgrade {self.cli}`.",
            fg="bright_black",
        )
        if cp := self._update_with_command(["pipx", "upgrade", self.cli, "--force"]):
            return cp.returncode in {0, 1}
        return False

    def update_brew(self) -> bool:
        self._log(
            f"Using brew. You can also manually run `brew upgrade {ConfigBase.get_dir_name()}`.",
            fg="bright_black",
        )
        with push_envs(
            {"HOMEBREW_NO_AUTO_UPDATE": "1", "HOMEBREW_NO_INSTALL_CLEANUP": "1"}
        ):
            res = self._update_with_command(
                ["brew", "--repo", "symopsio/tap"], capture_output=True
            )
            if not res:
                return False

            if not self._update_with_checked_command(
                ["git", "pull", "origin", "master"],
                cwd=res.stdout.strip(),
            ):
                return False

            versioned_name = f"{ConfigBase.get_dir_name()}@{self.latest_version}"

            if self._update_with_checked_command(["brew", "install", versioned_name]):
                return self._update_with_checked_command(
                    ["brew", "link", " --overwrite", "--force", versioned_name]
                )
            else:
                # Make sure we never leave an orphaned install:
                self._update_with_checked_command(
                    ["brew", "link", ConfigBase.get_dir_name()]
                )
                return False

    def update_sitepackage(self) -> bool:
        pip = self.dir.parent.parent.parent / "bin" / "pip"
        if not pip.exists():
            self._log("pip must be installed", fg="red")
            return False
        return self._update_with_checked_command(
            [str(pip), "install", "-U", f"{self.cli}=={self.latest_version}"]
        )

    def update_other(self) -> bool:
        if not self.url:
            return False

        self._log(
            f"Upgrading in-place. You can also manually follow the steps at https://docs.symops.com/docs/install-{self.cli}#manual-install.",
            fg="bright_black",
        )

        try:
            filename, _ = urlretrieve(self.url["url"])
        except URLError:
            urlcleanup()
            return False

        try:
            prefix = f"{self.cli}-{self.latest_version}/"
            with tarfile.open(filename) as tar:
                for member in tar.getmembers():
                    if not member.name.startswith(prefix):
                        continue
                    member.name = str(Path(member.name).relative_to(prefix))
                    tar.extract(member, path=self.dir)
            return True
        except PermissionError:
            self._log(
                f"Permission error. Try running `sudo {ConfigBase.get_dir_name()} update`.",
                fg="red",
            )
            return False
        except tarfile.TarError:
            return False

    def _update(self) -> bool:
        if self.is_pipx():
            return self.update_pipx()
        if self.is_brew():
            return self.update_brew()
        if self.is_sitepackage():
            return self.update_sitepackage()
        return self.update_other()

    def update(self, replace=False):
        self._log("Quickly checking for updates...", fg="white", nl=False)
        if not self.needs_update():
            self._log("no updates found, carry on!", fg="white")
            return
        self._log("found newer version!", fg="white", bold=True)

        self._log(
            f"Updating from v{self.get_current_version()} to v{self.latest_version}..."
        )
        if self._update():
            self._log("Update finished!", fg="green")
            if replace:
                reset_fds()
                os.execvp(sys.argv[0], sys.argv)
        else:
            self._log("Update failed :(", fg="red")

    def auto_update(self):
        try:
            if not self.should_check():
                return
            self.update(replace=True)
        except KeyboardInterrupt:
            self._log("No worries! We'll update some other time :)", fg="white")
        except:  # just to be safe
            pass

    def manual_update(self):
        if self.is_local():
            self._log("Auto-updating is not supported in dev environments!", fg="red")
            return
        self.update()
