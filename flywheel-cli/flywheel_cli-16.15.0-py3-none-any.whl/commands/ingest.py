"""ingest subcommand"""
# pylint: disable=too-many-lines

import atexit
import copy
import logging
import os
import sys
import time

from flywheel import ApiException
from pydantic import ValidationError

from .. import util
from ..ingest import config, errors, reporter
from ..ingest import schemas as T
from ..ingest import worker
from ..ingest.client import APIClient, DBClient, db

log = logging.getLogger(__name__)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("s3transfer").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)


CLUSTER = [
    {"name": "cluster", "help": "Ingest cluster url", "group": "cluster"},
    {
        "name": "follow",
        "flags": ["-f", "--follow"],
        "help": "Follow the progress of the ingest",
        "group": "cluster",
        "action": "store_true",
    },
]

REPORTER = [
    {
        "name": "save_audit_logs",
        "metavar": "PATH",
        "help": "Save audit log to the specified path on the current machine",
        "group": "reporter",
    },
    {
        "name": "save_deid_logs",
        "metavar": "PATH",
        "help": "Save deid log to the specified path on the current machine",
        "group": "reporter",
    },
    {
        "name": "save_subjects",
        "metavar": "PATH",
        "help": "Save subjects to the specified file",
        "group": "reporter",
    },
]

INGEST = [
    {
        "name": "symlink",
        "help": "Follow symbolic links that resolve to directories",
        "action": "store_true",
    },
    {
        "name": "include_dirs",
        "metavar": "PATTERN",
        "nargs": "+",
        "help": "Patterns of directories to include",
    },
    {
        "name": "exclude_dirs",
        "metavar": "PATTERN",
        "nargs": "+",
        "help": "Patterns of directories to exclude",
    },
    {
        "name": "include",
        "metavar": "PATTERN",
        "nargs": "+",
        "help": "Patterns of filenames to include",
    },
    {
        "name": "exclude",
        "metavar": "PATTERN",
        "nargs": "+",
        "help": "Patterns of filenames to exclude",
    },
    {
        "name": "compression_level",
        "help": (
            "The compression level to use for packfiles -1 by default. "
            "0 for store. "
            "A higher compression level number means more compression."
        ),
    },
    {
        "name": "ignore_unknown_tags",
        "help": "Ignore unknown dicom tags when parsing dicom files",
        "action": "store_true",
    },
    {
        "name": "encodings",
        "nargs": "+",
        "help": "Set character encoding aliases. E.g. win_1251=cp1251",
    },
    {
        "name": "de_identify",
        "help": "De-identify DICOM files",
        "action": "store_true",
    },
    {
        "name": "deid_profile",
        "metavar": "NAME",
        "help": "Use the De-identify profile by name",
    },
    {
        "name": "skip_existing",
        "help": "Skip import of existing files",
        "action": "store_true",
    },
    {
        "name": "no_audit_log",
        "help": "Skip uploading audit log to the target projects",
        "action": "store_true",
    },
    {
        "name": "load_subjects",
        "metavar": "PATH",
        "help": "Load subjects from the specified file",
    },
    {
        "name": "detect_duplicates",
        "help": (
            "Identify duplicate data conflicts within source data "
            "and duplicates between source data and data in Flywheel. "
            "Duplicates are skipped and noted in audit log. "
            "Template and folder ingest skip DD04 and DD07 by default."
        ),
        "action": "store_true",
    },
    {
        "name": "copy_duplicates",
        "help": (
            "Upload duplicates found using --detect-duplicates "
            "to a sidecar project instead of skipping them "
        ),
        "action": "store_true",
    },
    {
        "name": "require_project",
        "help": (
            "Proceed with the ingest process only if the "
            "resolved group and project exists "
        ),
        "action": "store_true",
    },
    {
        "name": "detect_duplicates_project",
        "help": (
            "Specify one or multiple project paths " "to use for detecting duplicates"
        ),
        "nargs": "+",
    },
    {
        "name": "enable_project_files",
        "help": "Enable file uploads to project container",
        "action": "store_true",
    },
    {
        "name": "detect_duplicates_override",
        "help": "Specify error codes to get warnings about",
        "nargs": "+",
    },
    {
        "name": "zip_single_dicom",
        "help": "Create zip for single DICOM",
        "action": "store_true",
    },
]

WORKER = [
    {
        "name": "jobs",
        "help": "The number of concurrent jobs to run (e.g. scan jobs)",
        "group": "worker",
    },
    {
        "name": "sleep_time",
        "metavar": "SECONDS",
        "help": "Number of seconds to wait before trying to get a task",
        "group": "worker",
    },
    {
        "name": "max_tempfile",
        "help": "The max in-memory tempfile size, in MB, or 0 to always use disk",
        "group": "worker",
    },
]

GENERAL = [
    {
        "name": "config_file",
        "flags": ["-C", "--config-file"],
        "metavar": "PATH",
        "group": "general",
        "help": "Specify configuration options via config file",
        "default": None,
    },
    {
        "name": "no_config",
        "group": "general",
        "help": "Do NOT load the default configuration file",
        "action": "store_true",
    },
    {
        "name": "assume_yes",
        "flags": ["-y", "--yes"],
        "help": "Assume the answer is yes to all prompts",
        "group": "general",
        "action": "store_true",
    },
    {
        "name": "ca_certs",
        "help": "The file to use for SSL Certificate Validation",
        "group": "general",
    },
    {
        "name": "timezone",
        "help": "Set the effective local timezone for imports",
        "group": "general",
    },
    {
        "name": "verbose",
        "flags": ["-v", "--verbose"],
        "help": "Get more detailed output",
        "group": "general",
        "action": "store_true",
    },
    {
        "name": "debug",
        "flags": ["-d", "--debug"],
        "group": "general",
        "help": "Turn on debug logging",
        "action": "store_true",
    },
    {
        "name": "quiet",
        "flags": ["-q", "--quiet"],
        "group": "general",
        "help": "Squelch log messages to the console",
        "action": "store_true",
    },
]


def add_commands(subparsers):
    """Add command to a given subparser"""
    # ingest w dicom strategy
    IngestDicomCommand(subparsers)
    # ingest w folder strategy
    IngestFolderCommand(subparsers)
    # ingest w template strategy
    IngestTemplateCommand(subparsers)
    # ingest w project strategy
    IngestProjectCommand(subparsers)
    # ingest bids
    IngestBidsCommand(subparsers)
    # add follow subcommand
    FollowCommand(subparsers, "follow")
    ## add abort subcommand
    AbortCommand(subparsers, "abort")
    return subparsers


def detect_duplicates_error_codes(exclude=None):
    """Return all the detect duplicates errors but the excluded ones."""
    exclude = exclude or set()
    error_codes = set()
    for item in errors.__dict__.values():
        if hasattr(item, "code") and item.code.startswith("DD"):
            error_codes.add(item.code)
    return sorted(list(error_codes.difference(exclude)))


class Config:  # pylint: disable=R0903
    """Wrapper class around a dict which contains different configurations
    and provides easy access by dot notation
    """

    def __init__(self, configs):
        self.configs = configs

    def __getattr__(self, name):
        conf = self.configs.get(name)
        if not conf:
            raise AttributeError(f"Unknown attribute: {name}")
        return conf


class Command:
    """Base command that adds the general configutaion"""

    configs = {}
    arg_table = []
    arg_groups = {
        "general": {"title": "General"},
    }

    def __init__(self, parent, name, defaults_args=None, **parser_kwargs):
        self.config = None
        self.defaults_args = defaults_args
        # setup parser
        if parser_kwargs.get("add_help", True):
            parser_kwargs.setdefault("help", self.__class__.__doc__)
        self.parser = parent.add_parser(name, **parser_kwargs)
        self.parser.set_defaults(func=self.run)
        self.parser.set_defaults(config=self.load_config)
        # setup configs
        self.configs = {
            "general": config.GeneralConfig,
            **self.configs,
        }
        # finally add config arguments to the parser
        self.add_arguments()

    def add_argument_groups(self):
        """Add argument groups"""
        groups = {}
        for name, orig_opts in self.arg_groups.items():
            if name not in groups:
                opts = copy.deepcopy(orig_opts)
                group_type = opts.pop("type", "argument")
                groups[name] = getattr(self.parser, f"add_{group_type}_group")(**opts)
        return groups

    def add_arguments(self):  # pylint: disable=too-many-branches
        """Add all config arguments to the parser"""
        self.default_values = {}
        groups = self.add_argument_groups()

        arg_names = set()
        args = []
        pos_args = []
        for opts in self.arg_table:
            name = opts.get("name")
            is_positional = opts.get("positional", False)
            if is_positional:
                pos_args.append(copy.deepcopy(opts))
            elif name not in arg_names:
                arg_names.add(name)
                args.append(copy.deepcopy(opts))

        args = sorted(args, key=lambda item: item.get("name"))
        args = pos_args + args
        arg_names = set()

        for opts in args:
            group_name = opts.pop("group", None)
            if group_name:
                arg_parser = groups.get(group_name, self.parser)
            else:
                arg_parser = self.parser

            kwargs = {}

            name = opts.pop("name")
            if name in arg_names:
                continue
            arg_names.add(name)

            is_positional = opts.pop("positional", False)
            if is_positional:
                # can't set dest for positional argument
                flags = name
            else:
                flags = opts.pop("flags", f"--{name.replace('_', '-')}")
                kwargs["dest"] = name
            if not isinstance(flags, list):
                flags = [flags]

            # add the remainder opts as is to the kwargs
            kwargs.update(opts)

            if "help" in kwargs and "default:" not in kwargs["help"]:
                default = kwargs.get("default", self.get_default_value_for_opt(name))
                if default is not None and default != []:
                    kwargs["help"] = f"{kwargs['help']} (default: {default})"

            if "default" in kwargs:
                default = kwargs.get("default")
                self.default_values[name] = default
            kwargs.setdefault("default", None)

            arg_parser.add_argument(*flags, **kwargs)

    def get_default_value_for_opt(self, opt_name):
        """Get the default value for option from the config class"""
        for cls in self.configs.values():
            schema = cls.schema()
            properties = schema.get("properties", {})
            if opt_name in properties:
                return properties.get(opt_name).get("default", None)
        return None

    def load_config(self, args):
        """Load all config"""
        if self.defaults_args:
            for key in self.defaults_args:
                if hasattr(args, key) and getattr(args, key) is None:
                    setattr(args, key, self.defaults_args[key])

        if "--detect-duplicates-override" in sys.argv:
            # FLYW-7019
            args.detect_duplicates = True

        if getattr(args, "help", False):
            self.parser.print_help()
            sys.exit(0)
            return
        loaded = {}
        for name, cls in self.configs.items():
            try:
                loaded[name] = config.load_config(cls, args, self.default_values)
            except ValidationError as err:
                msg = "\n".join(f"{e['loc'][0]}: {e['msg']}" for e in err.errors())
                self.parser.error(
                    f"The following errors found during parsing configuration:\n{msg}"
                )

        self.config = Config(loaded)
        self.config.general.startup_initialize()

    def run(self, args):
        """Body of the command"""


class IngestCommand(Command):
    """Ingest subcommand"""

    configs = {
        "ingest": config.IngestConfig,
        "reporter": config.ReporterConfig,
        "cluster": config.ClusterConfig,
        "worker": config.WorkerConfig,
    }

    def __init__(self, strategy_config_cls, *args, **kwargs):
        self.arg_groups = {
            **self.arg_groups,
            **{
                "reporter": {
                    "title": "Reporter",
                    "description": (
                        "These config options are only available when using "
                        "cluster mode with the --follow argument "
                        "or when using local worker."
                    ),
                },
                "cluster": {
                    "title": "Cluster",
                    "description": "These config options apply when using a cluster to ingest data.",
                },
                "worker": {
                    "title": "Worker",
                    "description": (
                        "These config options are only available when using "
                        "local worker (--cluster is not defined)"
                    ),
                },
            },
        }

        self.configs = {"strategy": strategy_config_cls, **self.configs}
        super().__init__(*args, **kwargs)

    def run(self, args):

        if self.config.cluster.cluster:
            self.run_cluster_ingest()
        else:
            self.run_local_ingest()

    def run_local_ingest(self):
        """Run local ingest with local workers and sqlite databse backend"""
        log.debug(f"Using database: {self.config.worker.db_url}")
        if not self.config.general.debug:
            # delete db file on exit if not in debug mode
            filepath = self.config.worker.db_url.replace("sqlite:///", "")
            atexit.register(delete_file, filepath)
        # essetial to start workers (fork) before initiating flywheel client anywhere
        worker_pool = worker.WorkerPool(self.config.worker)
        worker_pool.start()
        db.set_lock(worker_pool.lock)
        ingest_db = DBClient(self.config.worker.db_url)
        ingest_db.create_ingest(self.config.ingest, self.config.strategy)
        self.load_subjects(ingest_db)
        ingest_db.start()
        reporter_ = reporter.Reporter(ingest_db, self.config.reporter)
        try:
            reporter_.run()
        except KeyboardInterrupt:
            ingest_db.abort()
            while not T.IngestStatus.is_terminal(ingest_db.ingest.status):
                time.sleep(1)
            # and print the final report
            reporter_.final_report()
        finally:
            log.debug("Shutting down workers gracefully")
            worker_pool.shutdown()

    def run_cluster_ingest(self):
        """Run cluster managed ingest"""
        ingest_api = APIClient(self.config.cluster.cluster)
        ingest_api.create_ingest(self.config.ingest, self.config.strategy)
        self.load_subjects(ingest_api)
        ingest_url = self.config.cluster.save_ingest_operation_url(ingest_api.ingest_id)
        ingest_api.start()

        print(f"Started ingest {ingest_url}")
        print("Use `fw ingest follow` to see progress or `fw ingest abort` to abort it")

        if self.config.cluster.follow:
            reporter.Reporter(ingest_api, self.config.reporter).run()

    def load_subjects(self, client):
        """Load subjects if it was requested"""
        if self.config.ingest.load_subjects:
            with open(self.config.ingest.load_subjects, "r", encoding="utf-8") as fp:
                client.load_subject_csv(fp)


class IngestDicomCommand(IngestCommand):
    """Ingest dicom command"""

    arg_table = (
        [
            {
                "name": "src_fs",
                "positional": True,
                "metavar": "SRC",
                "help": "The path to the folder to import",
            },
            {
                "name": "group",
                "positional": True,
                "nargs": "?",
                "metavar": "GROUP_ID",
                "help": "The id of the group",
            },
            {
                "name": "project",
                "positional": True,
                "nargs": "?",
                "metavar": "PROJECT_LABEL",
                "help": "The label of the project",
            },
            {
                "name": "subject",
                "metavar": "LABEL",
                "help": "Override value for the subject label",
            },
            {
                "name": "session",
                "metavar": "LABEL",
                "help": "Override value for the session label",
            },
            {
                "name": "force_scan",
                "help": 'Try to parse all files as DICOM regardless of the DICM prefix (might want to use --include "*")',
                "action": "store_true",
            },
            {
                "name": "include",
                "metavar": "PATTERN",
                "nargs": "+",
                "help": "Patterns of filenames to include",
                "default": [
                    "*.[dD][cC][mM]",
                    "*.[dD][cC][mM].[gG][zZ]",
                    "*.[dD][iI][cC][oO][mM]",
                    "*.[dD][iI][cC][oO][mM].[gGzZ]",
                    "*.[iI][mM][aA]",
                    "*.[iI][mM][aA].[gG][zZ]",
                    "[0-9]*[0-9.]*[0-9]",
                ],
            },
            {
                "name": "repack",
                "help": "Extract and scan the first DICOM from ZIPs for hierarchy creation then upload all DICOMs",
                "action": "store_true",
            },
            {
                "name": "strict_uid",
                "help": "Group DICOMs in sessions and acquisitions by StudyInstanceUID and SeriesInstanceUID",
                "action": "store_true",
            },
        ]
        + INGEST
        + REPORTER
        + CLUSTER
        + WORKER
        + GENERAL
    )

    def __init__(self, subparsers):
        super().__init__(
            config.DicomConfig, subparsers, "dicom", help="Ingest dicom files"
        )


class IngestFolderCommand(IngestCommand):
    """Ingest folder command"""

    arg_table = (
        [
            {
                "name": "src_fs",
                "positional": True,
                "metavar": "SRC",
                "help": "The path to the folder to import",
            },
            {
                "name": "group",
                "flags": ["-g", "--group"],
                "metavar": "ID",
                "help": "The id of the group, if not in folder structure",
            },
            {
                "name": "project",
                "flags": ["-p", "--project"],
                "metavar": "LABEL",
                "help": "The label of the project, if not in folder structure",
            },
            {
                "name": "dicom",
                "metavar": "NAME",
                "help": "The name of dicom subfolders to be zipped prior to upload",
            },
            {
                "name": "pack_acquisitions",
                "metavar": "TYPE",
                "help": "Acquisition folders only contain acquisitions of TYPE and are zipped prior to upload",
            },
            {
                "name": "root_dirs",
                "help": "The number of directories to discard before matching",
            },
            {
                "name": "no_subjects",
                "help": "no subject level (create a subject for every session)",
                "default": False,
                "action": "store_true",
            },
            {
                "name": "no_sessions",
                "help": "no session level (create a session for every subject)",
                "default": False,
                "action": "store_true",
            },
            {
                "name": "group_override",
                "flags": ["--group-override"],
                "metavar": "ID",
                "help": "Force using this group id",
            },
            {
                "name": "project_override",
                "flags": ["--project-override"],
                "metavar": "LABEL",
                "help": "Force using this project label",
            },
            {
                "name": "force_scan",
                "help": "Try to parse all files as DICOM regardless of the DICM prefix.",
                "action": "store_true",
            },
            {
                "name": "detect_duplicates_override",
                "help": "Specify error codes to get warnings about",
                "nargs": "+",
                "default": detect_duplicates_error_codes(
                    exclude={
                        errors.DuplicatedStudyInstanceUID.code,
                        errors.DuplicatedSeriesInstanceUID.code,
                    }
                ),
            },
        ]
        + INGEST
        + REPORTER
        + CLUSTER
        + WORKER
        + GENERAL
    )

    def __init__(self, subparsers):
        super().__init__(
            config.FolderConfig, subparsers, "folder", help="Ingest a folder"
        )


class IngestTemplateCommand(IngestCommand):
    """Ingest template command"""

    arg_table = (
        [
            {
                "name": "template",
                "positional": True,
                "nargs": "?",
                "metavar": "TEMPLATE",
                "help": "Template string or a file containing the ingest template",
            },
            {
                "name": "src_fs",
                "positional": True,
                "metavar": "SRC",
                "help": "The path to the folder to import",
            },
            {
                "name": "group",
                "flags": ["-g", "--group"],
                "metavar": "ID",
                "help": "The id of the group, if not in folder structure",
            },
            {
                "name": "project",
                "flags": ["-p", "--project"],
                "metavar": "LABEL",
                "help": "The label of the project, if not in folder structure",
            },
            {
                "name": "no_subjects",
                "help": "no subject level (create a subject for every session)",
                "default": False,
                "action": "store_true",
            },
            {
                "name": "no_sessions",
                "help": "no session level (create a session for every subject)",
                "default": False,
                "action": "store_true",
            },
            {
                "name": "group_override",
                "flags": ["--group-override"],
                "metavar": "ID",
                "help": "Force using this group id",
            },
            {
                "name": "project_override",
                "flags": ["--project-override"],
                "metavar": "LABEL",
                "help": "Force using this project label",
            },
            {
                "name": "set_var",
                "metavar": "KEY=VALUE",
                "nargs": "+",
                "help": "Set arbitrary key-value pairs",
            },
            {
                "name": "force_scan",
                "help": 'Try to parse all files as DICOM regardless of the DICM prefix (might want to use --include "*")',
                "action": "store_true",
            },
            {
                "name": "detect_duplicates_override",
                "help": "Specify error codes to get warnings about",
                "nargs": "+",
                "default": detect_duplicates_error_codes(
                    exclude={
                        errors.DuplicatedStudyInstanceUID.code,
                        errors.DuplicatedSeriesInstanceUID.code,
                    }
                ),
            },
            {
                "name": "strict_uid",
                "help": "Group DICOMs in sessions and acquisitions by StudyInstanceUID and SeriesInstanceUID",
                "action": "store_true",
            },
        ]
        + INGEST
        + REPORTER
        + CLUSTER
        + WORKER
        + GENERAL
    )

    def __init__(self, subparsers):
        super().__init__(
            config.TemplateConfig,
            subparsers,
            "template",
            help="Ingest a folder using a template",
        )


class IngestProjectCommand(IngestCommand):
    """Ingest project command"""

    arg_table = (
        [
            {
                "name": "src_fs",
                "positional": True,
                "metavar": "SRC",
                "help": "The path to the folder to import (e.g.: fw://group-name/project-name/)",
            },
            {
                "name": "fw_walker_api_key",
                "positional": True,
                "metavar": "FW_WALKER_API_KEY",
                "help": "API key for FW (e.g.: flywheel.io:yiLr8PHLtpe33IdYJ5)",
            },
            {
                "name": "group",
                "flags": ["-g", "--group"],
                "metavar": "ID",
                "help": "The id of the destination group (default comes from SRC)",
            },
            {
                "name": "project",
                "flags": ["-p", "--project"],
                "metavar": "LABEL",
                "help": "The label of the destination project (default comes from SRC)",
            },
            {
                "name": "no_metadata",
                "flags": ["--no-metadata"],
                "action": "store_true",
                "help": "Skip copying file and container metadata from source project",
            },
            {
                "name": "deid_log_exists",
                "flags": ["--deid-log-exists"],
                "action": "store_true",
                "help": "The data to be ingested has already been de-identified and contains a valid file.deid_log_id",
            },
        ]
        + INGEST
        + REPORTER
        + CLUSTER
        + WORKER
        + GENERAL
    )

    def __init__(self, subparsers):
        super().__init__(
            config.ProjectConfig,
            subparsers,
            "project",
            help="Ingest a project from a Flywheel instance",
        )

    def load_config(self, args):
        if args.de_identify and args.deid_log_exists:
            print(
                "Argument '--deid-log-exists' is used for data that has already been de-identified "
                "and can not be used when specifying additional de-identification options."
            )
            sys.exit(1)
        super().load_config(args)


class IngestBidsCommand(Command):
    """Ingest bids command"""

    arg_table = [
        {
            "name": "folder",
            "positional": True,
            "metavar": "SRC",
            "help": "The path to the folder to import",
        },
        {
            "name": "group",
            "positional": True,
            "metavar": "ID",
            "help": "The id of the group",
        },
        {
            "name": "project",
            "flags": ["-p", "--project"],
            "metavar": "LABEL",
            "help": "The label of the destination project (default comes from SRC)",
        },
        {
            "name": "subject",
            "flags": ["--subject"],
            "metavar": "LABEL",
            "help": "Only upload data from single subject folder (e.g. sub-01)",
        },
        {
            "name": "session",
            "flags": ["--session"],
            "metavar": "LABEL",
            "help": "Only upload data from single session folder (e.g. ses-01)",
        },
        {
            "name": "debug",
            "flags": ["-d", "--debug"],
            "group": "general",
            "help": "Turn on debug logging",
            "action": "store_true",
        },
        {
            "name": "quiet",
            "flags": ["-q", "--quiet"],
            "group": "general",
            "help": "Squelch log messages to the console",
            "action": "store_true",
        },
    ]

    def __init__(self, subparsers):
        self.configs = {"strategy": config.BidsConfig}
        super().__init__(subparsers, "bids", help="Ingest BIDS")

    def run(self, args):
        import flywheel_bids.upload_bids  # pylint: disable=import-outside-toplevel

        fw = util.get_sdk_client_for_current_user()
        try:
            fw.lookup(args.group)
        except ApiException as exc:
            if exc.status == 404:
                print(f"Group {args.group} was not found, creating...")
                group = {"_id": args.group, "label": args.group}
                fw.add_group(group)
            else:
                print(exc.detail)

        flywheel_bids.upload_bids.upload_bids(
            fw,
            args.folder,
            args.group,
            project_label=args.project,
            validate=False,
            subject_label=args.subject,
            session_label=args.session,
        )


class FollowCommand(Command):
    """Follow the progress of a cluster managed ingest operation"""

    configs = {
        "reporter": config.ReporterConfig,
        "manage": config.ManageConfig,
    }

    arg_table = (
        [
            {
                "name": "ingest_url",
                "positional": True,
                "nargs": "?",
                "metavar": "INGEST_URL",
                "help": "The url of the ingest to manage (<cluster_host>/ingests/<ingest_id>)",
            }
        ]
        + REPORTER
        + GENERAL
    )

    def run(self, args):
        ingest_api = APIClient.from_url(
            self.config.manage.cluster, self.config.manage.ingest_id
        )
        reporter.Reporter(ingest_api, self.config.reporter).run()


class AbortCommand(Command):
    """Abort a cluster managed ingest operation"""

    configs = {"manage": config.ManageConfig}

    arg_table = [
        {
            "name": "ingest_url",
            "positional": True,
            "nargs": "?",
            "metavar": "INGEST_URL",
            "help": "The url of the ingest to manage (<cluster_host>/ingests/<ingest_id>)",
        }
    ] + GENERAL

    def run(self, args):
        ingest_api = APIClient.from_url(
            self.config.manage.cluster, self.config.manage.ingest_id
        )
        ingest = ingest_api.ingest
        if T.IngestStatus.is_terminal(ingest.status):
            print(f"Ingest already {ingest.status}")
            return
        msg = "Are you sure you want to abort the ingest?"
        if self.config.general.assume_yes or util.confirmation_prompt(msg):
            ingest_api.abort()


def delete_file(filepath):
    """Delete a given file if exists"""
    if os.path.exists(filepath):
        log.debug(f"Clean up file: {filepath}")
        os.remove(filepath)
