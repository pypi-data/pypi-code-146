import subprocess  # noqa: S404
import tempfile
from pathlib import Path
from typing import IO, BinaryIO, NoReturn, Optional, Tuple, Union

from wtforglib.versioned import unlink_path

from pacwrap.options import Options

XPERM = 0o755


class Error(Exception):
    """Base class for exceptions in this module."""


class PackageHandler(Options):  # noqa: WPS214
    """Abstract super class to specific handlers."""

    def unhandled(self, action: str) -> NoReturn:
        """Raises NotImplementedError."""
        raise NotImplementedError(
            "class {0} doesn't handle a file {1}!".format(
                self.__class__.__name__,
                action,
            ),
        )

    def file_action(self, fpath: str) -> int:
        """Reports package specified file."""
        return self.run_command(self._file_cmd_args(fpath))

    def find_action(self, package: str) -> int:
        """Searches for specified package."""
        self.unhandled("find")

    def info_action(self, package: str) -> int:
        """Reports info for specified package."""
        return self.run_command(self._info_cmd_args(package))

    def install_action(self, package: str) -> int:
        """Install specified package."""
        self.requires_super_user()
        return self._install_action(package)

    def uninstall_action(self, package: str) -> int:
        """Uninstall specified package."""
        self.requires_super_user()
        return self._uninstall_action(package)

    def list_packages(self) -> int:
        """List packages."""
        self.unhandled("list packages")

    def run_pipes_script(self, cmds: Tuple[str, ...]) -> int:
        """Create a script file of piped commands and run it."""
        joined = " | ".join(cmds)
        if self.test:
            print("noex: {0}".format(joined))
            return 0
        script = "#!/bin/sh\n\n{0}".format(joined)
        fp = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False)
        sname = Path(fp.name)
        print(script, file=fp)
        fp.close()
        sname.chmod(XPERM)
        rtn_val = self.run_command((fp.name,))
        unlink_path(sname, missing_ok=True)
        return rtn_val

    def decode_if(self, bval: Optional[Union[bytes, IO[bytes]]]) -> str:  # noqa:WPS234
        """Decodes darn byte like stuff."""
        if isinstance(bval, bytes):
            return bval.decode("utf-8")
        if isinstance(bval, BinaryIO):
            return bval.read().decode("utf-8")
        print("NOTICE: Unable to decode type: {0}".format(str(type(bval))))
        return ""

    def handle_cmd_out(  # noqa: WPS234
        self,
        out: Optional[Union[bytes, IO[bytes]]],
        err: Optional[Union[bytes, IO[bytes]]],
        rcode: int,
    ) -> None:
        """Manage subprocess outputs."""
        ostr: str
        estr: str
        ostr = self.decode_if(out)
        if rcode:
            estr = self.decode_if(err)
        else:
            estr = ""
        if self.output:
            with open(self.output, "w") as outf:
                outf.write(ostr)
                if estr:
                    outf.write("stderr:\n{0}".format(estr))
        if not self.quiet:
            print(ostr)
            if estr:
                print("stderr:\n{0}".format(estr))

    def run_command(self, args: Tuple[str, ...]) -> int:
        """Runs commands specified by args."""
        if self.test:
            print("noex: {0}".format(" ".join(args)))
            return 0
        res = subprocess.run(args, shell=False, capture_output=True)
        self.handle_cmd_out(res.stdout, res.stderr, res.returncode)
        return res.returncode

    def list_package(self, package_nm: str) -> int:
        """List files in specified package."""
        return self.run_command(self._list_package_args(package_nm))

    def _list_package_args(self, package_nm: str) -> Tuple[str, ...]:
        """Return list package command args for handler."""
        self.unhandled("_list_package_args")

    def _info_cmd_args(self, package_nm: str) -> Tuple[str, ...]:
        """Return info command args for handler."""
        self.unhandled("_info_cmd_args")

    def _install_action(self, package: str) -> int:
        """Install specified package."""
        self.unhandled("_install_action")

    def _uninstall_action(self, package: str) -> int:
        """Install specified package."""
        self.unhandled("_uninstall_action")

    def _file_cmd_args(self, fpath: str) -> Tuple[str, ...]:
        """Return file command args for handler."""
        self.unhandled("_file_cmd_args")
