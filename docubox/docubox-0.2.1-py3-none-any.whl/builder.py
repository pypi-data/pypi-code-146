import argparse
import hashlib
import importlib.machinery
import importlib.metadata
import importlib.util
import os
import pathlib
import sys
from typing import Any, Optional

from . import config
from . import launcher as _docubox

PROJECT_NAME="docubox"
DIST_DIR = pathlib.Path("dist")
LAUNCHER = "launcher.py"

def is_64bit() -> bool:
    """check if running platform is 64bit python."""
    return sys.maxsize > 1 << 32


def build(name: str, sha: bool, ln: bool, loglevel: str) -> int:
    # PyInstaller arguments
    pyinstaller_args = [
        "--noconfirm",
        "--console",
        "--onefile",
        "--name", name
    ]

    add_arg = "{src:s}" + os.pathsep + "{name:s}"
    for mod in config.collect_all:
        pyinstaller_args.append("--collect-all")
        pyinstaller_args.append(mod)
    for mod in config.package_data:
        origin = importlib.util.find_spec(mod).origin
        if origin is not None:
            pyinstaller_args.append("--add-data")
            pyinstaller_args.append(add_arg.format(src=os.path.dirname(origin), name=mod))
    for mod in config.hiddenimports:
        pyinstaller_args.append("--hidden-import")
        pyinstaller_args.append(mod)
    for sub in config.submodules:
        pyinstaller_args.append("--collect-submodules")
        pyinstaller_args.append(sub)
    for pkg in config.metadata:
        pyinstaller_args.append("--copy-metadata")
        pyinstaller_args.append(pkg)
    for mod in config.excludes:
        pyinstaller_args.append("--exclude-module")
        pyinstaller_args.append(mod)

    # log level default: INFO, can be DEBUG, WARN
    pyinstaller_args.append("--log-level")
    if loglevel is None:
        pyinstaller_args.append("INFO")
    else:
        pyinstaller_args.append(loglevel)
    # give launcher script
    pyinstaller_args.append(os.path.join(os.path.dirname(__file__), LAUNCHER))
    # launch PyInstaller
    from PyInstaller import __main__ as pyinstaller
    pyinstaller.run(pyinstaller_args)
    #
    if sys.platform.startswith("win"):
        # .exe is automatically added on windows
        genfile = name + ".exe"
    else:
        genfile = name
    # Generate sha
    if sha:
        gen_sha(genfile)
    # generate links
    if ln:
        make_link(genfile)
    return 0


def gen_sha(file: str):
    _gen_sha(file, "sha256")
    _gen_sha(file, "sha512")


def _gen_sha(file: str, type: str):
    hash = hashlib.new(type)
    generated = DIST_DIR / file
    with generated.open(mode="rb") as bin:
        hash.update(bin.read())
    hashfile = DIST_DIR / f"{file}.{type}"
    with hashfile.open(mode="w") as f:
        f.write(hash.hexdigest())


def make_link(file: str):
    if sys.platform.startswith("win"):
        # FIXME
        return 0
    # make links for linux and mac
    _make_link(file, PROJECT_NAME)
    for cmd in _docubox.commands:
        _make_link(file, cmd[0])

def _make_link(file, target):
    target_path = pathlib.Path("dist", target)
    target_path.unlink(missing_ok=True)
    os.symlink(file, target_path)


def main(arg: Optional[Any] = None) -> int:
    parse = argparse.ArgumentParser(prog="docubox", description="Standalone binary builder of DocuBox - the swiss army knife for document solution")
    parse.add_argument("-l", "--link", action="store_true", help="Put symbolic links of supported features.")
    parse.add_argument("-n", "--name", nargs=1, help="Specify generated binary name.")
    parse.add_argument("-s", "--sha", action="store_true", help="Generate SHA256 and SHA512 hash files.")
    parse.add_argument("--log-level", nargs=1, help="Specify log level, WARN, INFO, or DEBUG", default="INFO")
    args = parse.parse_args(arg)
    #
    if args.name is not None:
        name = args.name
    else:
        if sys.platform.startswith("win"):
            if is_64bit():
                name = "docubox.windows-x86_64"
            else:
                name = "docubox.windows-x86"
        elif sys.platform.startswith("linux"):
            name = "docubox.linux"
        elif sys.platform.startswith("darwin"):
            name = "docubox.osx"
        else:
            name = "docubox"
    return(build(name, sha=args.sha, ln=args.link, loglevel=args.log_level))


if __name__ == "__main__":
    sys.exit(main(None))
