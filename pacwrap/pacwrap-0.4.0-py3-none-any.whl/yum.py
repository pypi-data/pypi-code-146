from typing import Optional, Tuple

from wtforglib.kinds import StrAnyDict

from pacwrap.pkgmgr import PackageHandler


class YumHandler(PackageHandler):
    """Class to handle yum package management."""

    def __init__(self, opts: Optional[StrAnyDict] = None):
        """Creates a yum package handler."""
        super().__init__(opts)
        self.pkgcmd = "yum"

    def list_packages(self):
        """List packages."""
        cmds = (
            "rpm -qa --qf '%{name}-%{version}-%{release}.%{arch}.rpm\\n'",  # noqa: WPS342, E501
            "sort",
        )
        return self.run_pipes_script(cmds)

    def find_action(self, package: str) -> int:
        """Searches for specified package."""
        cmd = [self.pkgcmd, "search", package]
        if self.refresh:
            self.requires_super_user()
            cmd.insert(1, "--refresh")
        return self.run_command(tuple(cmd))

    def _file_cmd_args(self, fpath: str) -> Tuple[str, ...]:
        """Return file command args for handler."""
        return ("rpm", "-qf", fpath)

    def _info_cmd_args(self, package) -> Tuple[str, ...]:
        """Return info command args for handler."""
        return ("rpm", "-qi", package)

    def _list_package_args(self, package_nm: str) -> Tuple[str, ...]:
        """Return list package command args for handler."""
        return ("rpm", "-ql", package_nm)

    def _install_action(self, package: str) -> int:
        """Install specified package."""
        cmd = [self.pkgcmd, "install", package]
        if self.refresh:
            cmd.insert(1, "--refresh")
        return self.run_command(tuple(cmd))

    def _uninstall_action(self, package: str) -> int:
        """Uninstall specified package."""
        cmd = (self.pkgcmd, "remove", package)
        return self.run_command(cmd)
