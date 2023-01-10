from typing import Tuple

from pacwrap.pkgmgr import PackageHandler

LPACMAN = "pacman"


class PacmanHandler(PackageHandler):
    """Class to handle the pacman package manager."""

    def list_packages(self):
        """List packages."""
        return self.run_command((LPACMAN, "-Qe"))

    def find_action(self, package: str) -> int:
        """Searches for specified package."""
        switches = "-Ss"
        if self.refresh:
            self.requires_super_user()
            switches = "{0}y".format(switches)
        return self.run_command((LPACMAN, switches, package))

    def _file_cmd_args(self, fpath: str) -> Tuple[str, ...]:
        """Return file command args for handler."""
        return (LPACMAN, "-Qo", fpath)

    def _info_cmd_args(self, package: str) -> Tuple[str, ...]:
        """Return info command args for handler."""
        return (LPACMAN, "-Qi", package)

    def _list_package_args(self, package_nm: str) -> Tuple[str, ...]:
        """Return list package command args for handler."""
        return (LPACMAN, "-Ql", package_nm)

    def _install_action(self, package: str) -> int:
        """Install specified package."""
        switches = "-S"
        if self.refresh:
            switches = "{0}y".format(switches)
        cmd = (LPACMAN, switches, package)
        return self.run_command(cmd)

    def _uninstall_action(self, package: str) -> int:
        """Uninstall specified package."""
        cmd = (LPACMAN, "-R", package)
        return self.run_command(cmd)
