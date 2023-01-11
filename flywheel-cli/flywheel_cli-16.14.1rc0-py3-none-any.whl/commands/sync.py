"""Sync files from a Flywheel project to a local folder or an S3 bucket.

examples:
  fw sync fw://group/project s3://bucket/prefix
"""
import argparse
import json
import logging
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

import fs.filesize
import ruamel.yaml

from .. import util
from ..sync.fw_threaded_src import FWThreadedSource
from ..sync.os_dst import OSDestination
from ..sync.queue import SyncQueue
from ..sync.s3_dst import S3Destination

log = logging.getLogger(__name__)


def add_command(subparsers, parents):
    """Add fw sync command parser"""
    parser = subparsers.add_parser(
        "sync",
        parents=parents,
        help="Sync files from Flywheel to storage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
    )

    parser.add_argument(
        "src",
        metavar="PROJECT",
        help="Flywheel project to sync from (fw://group/project)",
    )
    parser.add_argument(
        "dst",
        metavar="STORAGE",
        nargs="?",
        help="Destination to sync to (/local/path or s3://bucket)",
    )

    parser.add_argument(
        "-i",
        "--include",
        metavar="T",
        default=[],
        action="append",
        help="Sync only files with the specified types (eg.: -i dicom)",
    )
    parser.add_argument(
        "-e",
        "--exclude",
        metavar="T",
        default=[],
        action="append",
        help="Skip files with the specified types (eg.: -e nifti -e qa)",
    )

    container_tags_arg_group = parser.add_mutually_exclusive_group()
    container_tags_arg_group.add_argument(
        "--include-container-tags",
        metavar="T",
        default={},
        action="store",
        help="Sync only the containers with specified tags and everything under them "
        '(eg.: --include-container-tag \'{"subject": ["some-tag"]}\')',
    )
    container_tags_arg_group.add_argument(
        "--exclude-container-tags",
        metavar="T",
        default={},
        action="store",
        help="Skip the containers with specified tags and everything under them "
        '(eg.: --exclude-container-tag \'{"project": ["some-tag"]}\')',
    )

    mlset_arg_group = parser.add_mutually_exclusive_group()
    mlset_arg_group.add_argument(
        "--include-mlset",
        metavar="T",
        default=[],
        choices=["Training", "Testing", "Validation"],
        action="append",
        type=_lower_and_cap_str,
        help="Sync only the subjects with specified ML Set and everything under them "
        "(eg.: --include-mlset Training)",
    )
    mlset_arg_group.add_argument(
        "--exclude-mlset",
        metavar="T",
        default=[],
        choices=["Training", "Testing", "Validation"],
        action="append",
        type=_lower_and_cap_str,
        help="Skip the subjects with specified ML Set and everything under them "
        "(eg.: --exclude-mlset Validation)",
    )

    parser.add_argument(
        "-a", "--analyses", action="store_true", help="Include analyses"
    )
    parser.add_argument(
        "-m", "--metadata", action="store_true", help="Include metadata"
    )
    parser.add_argument(
        "-x",
        "--full-project",
        action="store_true",
        help="Include analyses and metadata",
    )

    parser.add_argument(
        "-z",
        "--no-unpack",
        dest="unpack",
        action="store_false",
        help="Keep zipped DICOMs intact (default: extract)",
    )
    parser.add_argument(
        "-l",
        "--list-only",
        action="store_true",
        help="Show folder tree on source instead of syncing",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show individual files with --list-only",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Show what sync would do without transferring files",
    )
    parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        metavar="N",
        default=4,
        help="The number of concurrent jobs to run (default: 4)",
    )
    parser.add_argument(
        "--tmp-path",
        help=(
            "Set custom temp dir where the zips will be extracted to (default: system"
            " temp dir)"
        ),
    )

    parser.add_argument(
        "--delete", action="store_true", help="Delete extra files from destination"
    )

    parser.add_argument(
        "--export-templates-file",
        type=str,
        help=("Set export templates YAML file"),
    )

    parser.add_argument(
        "--save-audit-logs",
        type=str,
        help=("Save audit log to the specified path on the current machine"),
    )
    parser.add_argument(
        "--no-audit-log",
        action="store_true",
        help=("Skip uploading audit log to the target project"),
        default=False,
    )

    parser.set_defaults(func=sync)
    parser.set_defaults(parser=parser)
    return parser


def sync(args):  # pylint: disable=too-many-branches,too-many-statements
    """Run fw sync for the parsed cli args"""
    include_container_tags = _get_container_tag_filters(args.include_container_tags)
    exclude_container_tags = _get_container_tag_filters(args.exclude_container_tags)

    if _check_analysis_tag_filters(
        include_container_tags, exclude_container_tags, args.analyses
    ):
        raise ValueError("Analysis container filtering only works with --analyses flag")

    export_templates = (
        _read_export_templates_file(args.export_templates_file)
        if args.export_templates_file
        else None
    )

    fw = util.get_sdk_client_for_current_user()
    # Eliminate Connection pool is full, discarding connection warnings
    util.set_sdk_connection_pool_size(fw, args.jobs + 2)
    log.debug(f"Checking source {args.src}")
    if os.environ.get("FW_CLI_NO_RESOLVE_PROJECT") == "true":
        group_id, project_label = util.parse_resolver_path(args.src)
        # Find project by label
        log.debug("Getting project container with find_first")
        project = fw.projects.find_first(
            filter=f'parents.group={group_id},label="{project_label}"'
        )
        if not project:
            raise ValueError(f"No project found at {args.src}")
    else:
        project = fw.lookup(util.parse_resolver_path(args.src))
    if project.container_type != "project":
        args.parser.error(f"{args.src} is not a project")
    # create and verify destination (if provided)
    if args.dst:
        log.debug(f"Checking destination {args.dst}")
        s3_match = re.match(r"s3://(?P<bucket>[^/]+)(?P<prefix>.*)", args.dst)
        if s3_match:
            dst = S3Destination(s3_match.group("bucket"), s3_match.group("prefix"))
        else:
            dst = OSDestination(
                args.dst
            )  # simply use args.dst as the destination path for os
        dst.check_perms()

    strip_root = args.src.endswith(
        "/"
    )  # strip root-dir based on trailing slash (like rsync)

    src = FWThreadedSource(
        fw,
        project.id,
        include=args.include,
        exclude=args.exclude,
        include_container_tags=include_container_tags,
        exclude_container_tags=exclude_container_tags,
        include_mlset=args.include_mlset,
        exclude_mlset=args.exclude_mlset,
        analyses=args.analyses,
        metadata=args.metadata,
        full_project=args.full_project,
        strip_root=strip_root,
        unpack_dir=args.tmp_path,
        export_templates=export_templates,
    )

    if args.list_only or args.dst is None:  # print src if dst not given (like rsync)
        print_tree(src, args.src, verbose=args.verbose)
        sys.exit(0)

    queue = SyncQueue(
        dst, args.jobs, assume_yes=args.yes, dry_run=args.dry_run, unpack=args.unpack
    )
    queue.report.start()
    cnt = 0
    try:
        log.debug("Populating sync queue")
        src_names = set()
        for src_file in src:
            src_name = os.path.normpath(src_file.name)
            if src_name not in src_names:
                cnt += 1
                src_names.add(src_name)
                queue.store(src_file)
            else:
                log.debug(f"FWFile {src_name} already added")
                # TODO fix core to not emit any files twice
                # reproducible on dev/scitran/neuro with analyses
        log.debug(f"Starting sync operations ({cnt} items)...")
        queue.start()
        if args.delete:
            cnt = 0
            log.debug("Populating delete queue")
            for dst_file in dst:
                if os.path.normpath(dst_file.name) not in src_names:
                    cnt += 1
                    queue.delete(dst_file)
            log.debug(f"Added all delete operations ({cnt} items)...")
        queue.wait_for_finish()

        if not args.no_audit_log:
            with tempfile.TemporaryDirectory() as tmp_dir:
                filepath = util.get_filepath(tmp_dir, prefix="sync_log")
                filename = Path(filepath).name
                queue.audit_log_fp.seek(0)
                fw.upload("project", project.id, filename, queue.audit_log_fp)

        if args.save_audit_logs:
            queue.audit_log_fp.seek(0)
            with open(args.save_audit_logs, "wb") as out_file:
                shutil.copyfileobj(queue.audit_log_fp, out_file)
            queue.shutdown()
    except KeyboardInterrupt:
        log.debug("Intercepting CTRL-C for graceful queue shutdown")
        queue.shutdown()
        raise


def _get_container_tag_filters(container_tag_filters):
    result_dict = None
    if container_tag_filters:
        result_dict = json.loads(container_tag_filters)

    for c_type in (result_dict or {}).keys():
        if c_type in ("group", "project"):
            raise ValueError(
                "Group and project level container tag filters are not allowed"
            )

    return result_dict


def _check_analysis_tag_filters(
    include_container_tags, exclude_container_tags, analyses_flag
):
    return (
        (
            container_tags := {
                **(include_container_tags or {}),
                **(exclude_container_tags or {}),
            }
        )
        and "analysis"
        in container_tags.keys()  # pylint: disable=used-before-assignment
        and not analyses_flag
    )


def _read_export_templates_file(filepath):
    with open(filepath, "r", encoding="utf-8") as yaml_file:
        return ruamel.yaml.load(yaml_file, Loader=ruamel.yaml.Loader)


def _lower_and_cap_str(value):
    """Change value to the correct form"""
    return value.lower().capitalize()


def print_tree(files, fs_url, verbose=False, report_batch=100, fh=sys.stdout):
    """Print a tree representation of files"""
    utf8 = fh.encoding == "UTF-8"
    none_str = "│  " if utf8 else "|  "
    node_str = "├─ " if utf8 else "|- "
    last_str = "└─ " if utf8 else "`- "
    total_size = 0
    total_count = 0

    def report(fs_url, size, count, columns=80, newline="\r"):
        # TODO optimization to terminal size
        size_str = fs.filesize.traditional(size)
        fh.write(f"{fs_url} ({size_str} / {count} files)".ljust(columns))
        fh.write(newline)
        fh.flush()

    def pprint_tree(node, prefix="", last=True):
        print(prefix, last_str if last else node_str, node, file=fh, sep="")
        prefix += "   " if last else none_str
        child_count = len(node.children)
        children = sorted(node.children.values(), key=Node.sort_key)
        for i, child in enumerate(children):
            last = i == (child_count - 1)
            pprint_tree(child, prefix, last)

    root = Node("root")
    for file in files:
        node = root
        parts = file.name.split("/")
        for dirname in parts[:-1]:
            node = node.children.setdefault(dirname, Node(dirname))
        if verbose:  # add files as leaf nodes
            filename = parts[-1]
            node.children.setdefault(filename, Node(filename, size=file.size))
        else:  # sum file size and count in parent node
            node.size += file.size
            node.files += 1
        total_size += file.size
        total_count += 1
        if total_count % report_batch == 0:
            report(fs_url, total_size, total_count)

    report(fs_url, total_size, total_count, newline="\n")

    for child in sorted(root.children.values(), key=Node.sort_key):
        pprint_tree(child)


class Node:
    """File tree node"""

    # pylint: disable=too-few-public-methods

    __slots__ = ("name", "size", "files", "children")

    def __init__(self, name, size=0, files=0):
        self.name = name
        self.size = size
        self.files = files
        self.children = {}

    def __str__(self):
        hrsize = fs.filesize.traditional(self.size)
        plural = "s" if self.files > 1 else ""
        if self.size and self.files:  # container w/ files
            return f"{self.name} ({hrsize} / {self.files} file{plural})"
        if self.size:  # file
            return f"{self.name} ({hrsize})"
        return self.name  # container w/o files

    def sort_key(self):
        """Show leaf nodes first (eg. files, metadata sidecars)"""
        return len(self.children) > 0, self.name
