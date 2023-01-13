"""Basic commands module"""
import functools
import logging
import os
import sys

import crayons
import flywheel
from tqdm.auto import tqdm
from tqdm.utils import CallbackIOWrapper

from .. import console, util

STDOUT = object()
DOWNLOAD_WARNING_SIZE = (1024**3) * 10

log = logging.getLogger(__name__)
perror = util.perror  # pylint: disable=invalid-name


def add_commands(subparsers, parsers, parents):
    """Adds basic commands"""
    # Login
    login_parser = subparsers.add_parser("login", help="Login to a Flywheel instance")
    login_parser.add_argument("api_key", help="Your Flywheel API Key")
    login_parser.set_defaults(func=login)
    login_parser.set_defaults(parser=login_parser)
    parsers["login"] = login_parser

    # Logout
    logout_parser = subparsers.add_parser("logout", help="Delete your saved API key")
    logout_parser.set_defaults(func=logout)
    logout_parser.set_defaults(parser=logout_parser)
    parsers["logout"] = logout_parser

    # Status
    status_parser = subparsers.add_parser(
        "status", help="See your current login status"
    )
    status_parser.set_defaults(func=status)
    status_parser.set_defaults(parser=status_parser)
    parsers["status"] = status_parser

    # Version
    version_parser = subparsers.add_parser("version", help="Print CLI version")
    version_parser.set_defaults(func=version)
    version_parser.set_defaults(parser=version_parser)
    parsers["version"] = version_parser

    # Copy
    cp_parser = subparsers.add_parser(
        "cp",
        parents=parents,
        help="Copy a local file to a remote location, or vice-a-versa",
    )
    cp_parser.add_argument(
        "src",
        help="The source path, either a local file or a flywheel file (e.g. fw://)",
    )
    cp_parser.add_argument(
        "dst",
        help="The destination path, either a local file or a flywheel file (e.g. fw://)",
    )
    cp_parser.set_defaults(func=copy_file)
    cp_parser.set_defaults(parser=cp_parser)
    parsers["cp"] = cp_parser

    # List
    ls_parser = subparsers.add_parser("ls", parents=parents, help="Show remote files")
    ls_parser.add_argument(
        "path", nargs="?", default=None, help="The path to list subfolders and files"
    )
    ls_parser.add_argument(
        "--ids", action="store_true", help="Display database identifiers"
    )
    ls_parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Show all",
    )
    ls_parser.set_defaults(func=ls)
    ls_parser.set_defaults(parser=ls_parser)
    parsers["ls"] = ls_parser

    # Download
    dl_parser = subparsers.add_parser(
        "download", parents=parents, help="Download a remote file or container"
    )
    dl_parser.add_argument(
        "src", help="The path to a flywheel file or container (e.g. fw://group/project)"
    )
    dl_parser.add_argument(
        "-o",
        "--output",
        nargs="?",
        const=STDOUT,
        help="Destination filename  (-- for stdout)",
    )
    dl_parser.add_argument(
        "-p",
        "--prefix",
        help="Prefix for downloaded directory structure",
    )
    dl_parser.add_argument(
        "-i", "--include", action="append", help="Download only these types"
    )
    dl_parser.add_argument(
        "-e", "--exclude", action="append", help="Download everything but these types"
    )
    dl_parser.add_argument(
        "--zip", action="store_true", help="Download container in .zip archive format"
    )
    dl_parser.set_defaults(func=download)
    dl_parser.set_defaults(parser=dl_parser)
    parsers["download"] = dl_parser

    # Upload
    ul_parser = subparsers.add_parser(
        "upload", parents=parents, help="Upload a local file to a Flywheel container"
    )
    ul_parser.add_argument("src", help="The source path to a local file")
    ul_parser.add_argument(
        "dst",
        help="The destination path to a Flywheel container (e.g. fw://group/project)",
    )
    ul_parser.set_defaults(func=upload)
    ul_parser.set_defaults(parser=ul_parser)
    parsers["upload"] = ul_parser


def login(args):
    """Login"""
    try:
        # Get current user
        fw = util.get_sdk_client(args.api_key)
        # Save credentials
        util.save_api_key(args.api_key, root=fw.auth_info.is_admin)

        user_name = util.get_authenticated_name(
            fw.auth_info.user_id, is_device=fw.auth_info.is_device
        )

        print(f"You are now logged in as: {user_name}!")
    except Exception as exc:  # pylint: disable=broad-except
        log.debug("Login error", exc_info=True)
        perror(f"Error logging in: {str(exc)}")
        sys.exit(1)


def logout(_):
    """Logout"""
    util.save_api_key(None)
    print("You are now logged out.")


def status(_):
    """Login status check"""
    fw = util.get_sdk_client_for_current_user()
    user_name = util.get_authenticated_name(
        fw.auth_info.user_id, is_device=fw.auth_info.is_device
    )
    print(f"You are currently logged in as {user_name} to {fw.host}")


def version(_):
    """Get CLI version"""
    version = util.get_cli_version()  # pylint: disable=redefined-outer-name

    print("flywheel-cli")
    print(f"  version: {version}\n")


def copy_file(args):
    """Copy Files"""
    src_is_fw = args.src.startswith("fw://")
    dst_is_fw = args.dst.startswith("fw://")
    if src_is_fw == dst_is_fw:
        perror("Must specify exactly one Flywheel location (fw://<path>)!")
        sys.exit(1)

    if src_is_fw:
        # Download, must reference a file
        download_file(args.src, args.dst)
    else:
        # Upload, must reference a valid destination container
        upload_file(args.src, args.dst)


def upload(args):
    """Upload a local file"""
    if not args.dst.startswith("fw://"):
        perror("Must specify a Flywheel localtion (fw://<path>)")
        sys.exit(1)
    upload_file(args.src, args.dst)


def upload_file(src, dst):
    """Upload file to container"""
    valid_containers = ("project", "subject", "session", "acquisition")

    # Determine destination
    fw = util.get_sdk_client_for_current_user()

    # Verify src exists
    src_path = os.path.abspath(src)
    if not os.path.isfile(src_path):
        perror(f"File {src_path} does not exist!")
        sys.exit(1)

    try:
        dst_path = util.parse_resolver_path(dst)
        dst_cont = fw.lookup(dst_path)
    except Exception as error:  # pylint: disable=broad-except
        perror(f"{error}\n")
        perror("Could not resolve dst_contination container")
        sys.exit(1)

    if dst_cont.container_type not in valid_containers:
        perror(f"Cannot upload to {dst_cont.container_type}")
        sys.exit(1)

    print(f"Uploading to {dst_cont.container_type}... ", end="", flush=True)

    try:
        with open(src_path, "rb") as file_obj:
            with tqdm(
                total=os.stat(file_obj.name).st_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as t:
                file_obj = CallbackIOWrapper(t.update, file_obj, "read")
                fw.upload(
                    dst_cont.container_type,
                    dst_cont.id,
                    os.path.basename(src_path),
                    file_obj,
                )
                t.reset()
        print("Done")
    except Exception as exc:  # pylint: disable=broad-except
        print("ERROR")
        perror(f"\n{exc}")


# pylint: disable=too-many-statements, too-many-branches
def download(args):
    """Download a remote file or container"""
    # pylint: disable=too-many-branches, too-many-statements
    fw = util.get_sdk_client_for_current_user()
    stdout = args.output == STDOUT
    _print = functools.partial(print, file=(sys.stderr if stdout else sys.stdout))

    try:
        if util.parse_resolver_path(args.src)[0] == "collections":
            src_path = util.parse_resolver_path(args.src)
            result = fw.collections.find_first(f"label={src_path[-1]}")
            src_cont = fw.collections_api.get_collection_acquisitions(result.id)[0]
        else:
            src_path = util.parse_resolver_path(args.src)
            result = fw.resolve(src_path)
            src_cont = result.path[-1]
    except Exception as exc:  # pylint: disable=broad-except
        perror(f"{exc}\n")
        perror("Could not resolve source container")
        sys.exit(1)

    if stdout:
        # --output specified without value
        dst = sys.stdout
    else:
        dst = args.output
        if not dst:
            # --output is not specified
            if src_cont.container_type == "file":
                dst = src_cont.name
            elif args.zip:
                dst = f"{src_cont.label}.zip"
            else:
                dst = f"{src_cont.label}.tar"
        dst = util.get_incremental_filename(os.path.abspath(dst))
        util.create_missing_dirs(dst)

    if src_cont.container_type == "file":
        src_name = src_cont.name
        parent_cont = result.path[-2]
        download_fn = get_single_file_download_fn(fw, parent_cont, src_name)

    else:
        src_name = src_cont.label
        nodes = [flywheel.DownloadNode(level=src_cont.container_type, id=src_cont.id)]
        type_filter = flywheel.DownloadFilterDefinition(
            plus=args.include,
            minus=args.exclude,
        )
        download_filters = [flywheel.DownloadFilter(types=type_filter)]
        if args.prefix:
            prefix = args.prefix
        else:
            prefix = ""
        # Create download request
        request = flywheel.Download(
            nodes=nodes, filters=download_filters, optional=True
        )

        summary = fw.create_download_ticket(request, prefix=prefix)
        file_size = util.hrsize(summary["size"])
        recommended_size = util.hrsize(DOWNLOAD_WARNING_SIZE)
        if summary["size"] >= DOWNLOAD_WARNING_SIZE:
            _print(
                crayons.yellow(
                    f"Warning: the dataset you are requesting to download is {file_size} "
                    f"and over the recommended size of {recommended_size} for the ‘fw download’ command."
                    "\n It is recommended to use the ‘fw sync’ command for larger datasets like downloading a Project."
                    " See more: https://docs.flywheel.io/hc/en-us/articles/360038098094-CLI-Sync"
                )
            )
        _print(
            f"This download will be about {file_size} "
            f"comprising {summary['file_cnt']} files."
        )
        if stdout or args.config.assume_yes or util.confirmation_prompt("Continue?"):
            query = [("ticket", summary["ticket"])]
            if args.zip:
                query.append(("format", "zip"))
            download_fn = functools.partial(
                fw.call_api,
                "/download",
                "GET",
                query_params=query,
                _return_http_data_only=True,
                _preload_content=False,
            )
        else:
            perror("Canceled")
            sys.exit(1)

    process_download(download_fn, src_name, dst)


def download_file(src, dst):
    """Download file from container"""
    # Determine source
    fw = util.get_sdk_client_for_current_user()

    try:
        src_path = util.parse_resolver_path(src)
        result = fw.resolve(src_path)
        src_cont = result.path[-1]
    except Exception as exc:  # pylint: disable=broad-except
        perror(f"{exc}\n")
        perror("Could not resolve source container")
        sys.exit(1)

    if src_cont.container_type != "file":
        perror(f"Can only copy files, not a {src_cont.container_type}")
        sys.exit(1)

    dst_path = os.path.abspath(dst)
    util.create_missing_dirs(dst_path)

    src_name = src_cont.name
    parent_cont = result.path[-2]
    download_fn = get_single_file_download_fn(fw, parent_cont, src_name)
    process_download(download_fn, src_name, dst_path)


def get_single_file_download_fn(fw, parent_cont, filename):
    """Get sdk client download function for a single file"""
    if parent_cont.container_type == "analysis":
        container_api = getattr(fw, "analyses_api")
        download_fn = getattr(
            container_api,
            f"download_output_from_{parent_cont.container_type}_with_http_info",
        )
    else:
        container_api = getattr(fw, f"{parent_cont.container_type}s_api")
        download_fn = getattr(
            container_api,
            f"download_file_from_{parent_cont.container_type}_with_http_info",
        )

    download_fn = functools.partial(
        download_fn,
        parent_cont.id,
        filename,
        _return_http_data_only=True,
        _preload_content=False,
    )
    return download_fn


def process_download(download_fn, src_name, output):
    """
    Download data using the given download function to the output.

    Output can be a filepath or sys.stdout.
    """
    stdout = output == sys.stdout
    _print = functools.partial(print, file=(sys.stderr if stdout else sys.stdout))
    _print(f"Downloading {src_name}... ", end="", flush=True)
    try:
        if stdout:
            wrote_bytes = write_stream_to_file(download_fn, sys.stdout.buffer)
        else:
            with open(output, "wb") as fp:
                wrote_bytes = write_stream_to_file(download_fn, fp)
    except Exception:
        _print("ERROR")
        raise

    _print("DONE")
    msg = f"Wrote {util.hrsize(wrote_bytes)}"
    if not stdout:
        msg = f"{msg} to {output}"
    _print(msg)


def write_stream_to_file(download_fn, dest_file):
    """
    Call download function which should return a stream response
    and write its content to the destination file like object
    """
    resp = download_fn()
    wrote_bytes = 0
    try:
        for chunk in resp.iter_content(chunk_size=65536):
            wrote_bytes += len(chunk)
            dest_file.write(chunk)
    finally:
        resp.close()
    return wrote_bytes


TIME_FORMAT_YEAR = "%b %d %Y %H:%M"


def ls(args):
    """Print container contents"""
    fw = util.get_sdk_client_for_current_user()

    try:
        user = fw.get_current_user()
    except Exception:  # pylint: disable=broad-except
        user = None

    kwargs = {}
    if args.all:
        if not fw.auth_info.is_admin:
            perror("The '--all' flag is available only for site admins")
            sys.exit(1)
        kwargs["exhaustive"] = True

    path = util.parse_resolver_path(args.path)
    result = fw.resolve(path, **kwargs)
    permissions = None

    if result.path:
        parent = result.path[-1]
        if parent.container_type == "gear":
            permissions = None
        elif parent.container_type in ("group", "project"):
            permissions = result.path[0].permissions
        else:
            # Project permissions for all lower children will use project.
            # We always have a project at this point in the hierarchy
            permissions = result.path[1].permissions
    else:
        parent = None

    table = []
    for child in result.children:
        table.append(_get_row_for_container(child, parent, user, args.ids, permissions))

    if not table:
        for child in result.path:
            if child.get("name") == path[-1]:
                table.append(
                    _get_row_for_container(child, parent, user, args.ids, permissions)
                )
                break

    console.print_table(sys.stdout, table)


def _get_row_for_container(
    cont, parent, user, show_ids, permissions
):  # pylint: disable=too-many-branches
    if user is None:
        level = "admin"
    else:
        if parent is None:
            # This happens when we resolve the root and get a list of children only
            permissions = getattr(cont, "permissions", None)
        level = _get_permission_level(permissions, user.id)

    size = ""
    modified = None
    if cont.container_type in ("session", "acquisition"):
        modified = cont.timestamp
    if cont.container_type == "file":
        modified = cont.modified
        size = util.hrsize(cont.size).rjust(6)

    if modified:
        time_format = TIME_FORMAT_YEAR
        modified = modified.strftime(time_format)
    else:
        modified = ""

    if cont.container_type == "group":
        name = crayons.blue(cont.id, bold=True)
    elif cont.container_type == "analysis":
        name = crayons.green(f"analyses/{cont.label}", bold=True)
    elif cont.container_type == "file":
        name = f"files/{cont.name}"
    else:
        name = cont.get("label") or cont.get("code")
        if name:
            name = crayons.blue(name, bold=True)
        else:
            name = crayons.red("UNLABELED")

    if show_ids:
        cid = "" if cont.container_type == "file" else f"<id:{cont.id}>"
        return (cid, level, size, modified, name)
    return (level, size, modified, name)


def _get_permission_level(permissions, uid):
    if permissions is not None:
        for perm in permissions:
            # prefer roles (from project level)
            if perm.id == uid and getattr(perm, "role_ids", None):
                # if container has roles fetch them
                return ", ".join(_get_role_names(perm.role_ids))
            # fallback to access property (group level)
            if perm.id == uid and getattr(perm, "access", None):
                return perm.access
    return "UNKNOWN"


def _get_role_names(role_ids):
    fw = util.get_sdk_client_for_current_user()
    return map(lambda role: role.label, [fw.get_role(role_id) for role_id in role_ids])
