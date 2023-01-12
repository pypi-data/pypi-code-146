import inspect
import re
import site
from pathlib import Path

from tecton import conf
from tecton_proto.args.repo_metadata_pb2 import SourceInfo

# Matches frame strings such as "<string>"
SKIP_FRAME_REGEX = re.compile("\<.*\>")


def get_current_workspace():
    return conf.get_or_none("TECTON_WORKSPACE")


def get_fco_source_info() -> SourceInfo:
    """Get the SourceInfo (file name and line number) for an FCO.

    How it works:
    - This function assumed it is being called from the constructor of an FCO
    - inspect.stack() returns the call stack (starting with this function)
    - Walk up the stack frames until the first file within a tecton repo (a child of .tecton) is found
    - The first valid tecton repo file is considered the filename of the FCO.
    """
    from tecton_core.repo_file_handler import _maybe_get_repo_root

    excluded_site_pkgs = site.getsitepackages() + [site.getusersitepackages()]

    source_info = SourceInfo()
    repo_root = _maybe_get_repo_root()
    if not repo_root:
        return source_info

    frames = inspect.stack()
    repo_root_path = Path(repo_root)
    for frame in frames:
        if SKIP_FRAME_REGEX.match(frame.frame.f_code.co_filename) is not None:
            continue
        frame_path = Path(frame.frame.f_code.co_filename).resolve()
        if not frame_path.exists():
            continue
        if any(pkg in frame.frame.f_code.co_filename for pkg in excluded_site_pkgs):
            # This filtering is needed in case `tecton` is installed using a virtual
            # environment that's created *inside* the repo root. Without this check,
            # Tecton SDK files would incorrectly be considered a valid repo files
            # and would be listed as the FCO's source filename.
            continue
        if repo_root_path in frame_path.parents:
            rel_filename = frame_path.relative_to(repo_root_path)
            source_info.source_lineno = str(frame.lineno)
            source_info.source_filename = str(rel_filename)
            break
    return source_info


def get_debug(ctx):
    while ctx.parent:
        ctx = ctx.parent
    return ctx.params["debug"]


def get_verbose(ctx):
    while ctx.parent:
        ctx = ctx.parent
    return ctx.params["verbose"]
