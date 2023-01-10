from typing import Tuple

from pacwrap.pkgmgr import PackageHandler

LAPT = "apt"


class AptHandler(PackageHandler):
    """Class to handle apt package management."""

    def list_packages(self):
        """List packages."""
        return self.run_pipes_script(("apt list --installed", "sort"))

    def find_action(self, package: str) -> int:
        """Searches for specified package."""
        if self.refresh:
            self.requires_super_user()
            self.run_command((LAPT, "update"))
        cmd = [LAPT, "search"]
        if self.names_only:
            cmd.append("--names-only")
        cmd.append(package)
        return self.run_command(tuple(cmd))

    def _install_action(self, package: str) -> int:
        """Install specified package."""
        if self.refresh:
            self.run_command((LAPT, "update"))
        cmd = (LAPT, "install", package)
        return self.run_command(cmd)

    def _uninstall_action(self, package: str) -> int:
        """Uninstall specified package."""
        cmd = (LAPT, "remove", package)
        return self.run_command(cmd)

    def _file_cmd_args(self, fpn: str) -> Tuple[str, ...]:
        """Return file command args for handler."""
        return ("dpkg", "-S", fpn)

    def _list_package_args(self, package_nm: str) -> Tuple[str, ...]:
        """Return list package command args for handler."""
        return ("dpkg", "-L", package_nm)

    def _info_cmd_args(self, package: str) -> Tuple[str, ...]:
        """Return info command args for handler."""
        return (LAPT, "show", package)
