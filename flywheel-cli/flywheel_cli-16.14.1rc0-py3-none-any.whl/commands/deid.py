"""ingest subcommand"""

import logging
import os
import sys
import zipfile

import crayons

from .. import config as root_config
from ..ingest import config as i_config
from ..ingest import deid
from ..ingest import schemas as T
from ..ingest.client import db
from ..ingest.scanners import dicom
from ..ingest.strategies import dicom as dicom_strategy
from ..ingest.tasks import upload
from .ingest import Command as BaseCommand


def add_commands(subparsers):
    """Add command to a given subparser"""
    DeidTestCommand(subparsers)
    DeidCreateCommand(subparsers)
    return subparsers


class Command(BaseCommand):
    """Command"""

    arg_groups = {}

    def __init__(self, parent, name, defaults_args=None, **parser_kwargs):
        super().__init__(parent, name, defaults_args, **parser_kwargs)
        self.parser.set_defaults(config=self.configure)
        self._fh = sys.stdout

    def configure(self, args):
        """Validate all config"""

    def print_msg(self, msg, replace=False):
        """Print"""
        if replace:
            msg = f"\r{msg}\033[K"
        else:
            msg = f"{msg}\n"
        self._fh.write(msg)
        self._fh.flush()


class DeidTestCommand(Command):
    """Ingest dicom command"""

    arg_table = [
        {
            "name": "src_path",
            "positional": True,
            "metavar": "SRC",
            "help": "The path to the folder to test",
        },
        {
            "name": "deid_profile_path",
            "positional": True,
            "metavar": "PROFILE",
            "help": "Path to file containing the de-id profile",
        },
        {
            "name": "dst_path",
            "metavar": "PATH",
            "help": "Save test results to the specified path on the current machine",
            "positional": True,
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
            "name": "debug",
            "flags": ["-d", "--debug"],
            "group": "general",
            "help": "Turn on debug logging",
            "default": False,
            "action": "store_true",
        },
    ]

    def __init__(self, subparsers):
        super().__init__(
            subparsers, "test", help="Test your de-identification template"
        )

        self.logs = []
        self.progress = T.StageCount()

    def configure(self, args):
        """Validate all config"""
        path = args.deid_profile_path
        if not os.path.exists(path):
            raise AttributeError(f"The profile file path '{path}' does not exist")

        profile = i_config.read_config_file(path)
        profile.pop("deid-log", None)
        profile["name"] = "custom"
        args.deid_profiles = [profile]

        if not os.path.exists(args.dst_path):
            raise AttributeError(f"The path '{args.dst_path}' does not exist")

        args.group = "group"
        args.project = "project"
        args.deid_profile = "custom"

        root_config.Config.configure_logging(args)

    def run(self, args):
        """Run the deid test command"""
        ingest_config = i_config.IngestConfig(
            src_fs=args.src_path,
            de_identify=True,
            deid_profile=args.deid_profile,
            deid_profiles=args.deid_profiles,
            include=[
                "*.dcm",
                "*.dcm.gz",
                "*.dicom",
                "*.dicom.gz",
                "*.ima",
                "*.ima.gz",
            ],
        )
        walker = ingest_config.create_walker()

        # scan
        items = self._scan(args, ingest_config, walker)

        # deid
        deid_profile = self._configure_deid(ingest_config)

        # process files
        self._process_files(items, deid_profile, walker)

        # write logs
        self.print_msg(str(crayons.magenta("\nWriting log file", bold=True)))
        path = os.path.join(args.dst_path, "deid_log.csv")
        with open(path, "w", encoding="utf-8") as fh:
            for line in db.deid_logs(deid_profile, self.logs):
                fh.write(line)

        self.print_msg(str(crayons.magenta("\nDe-Id test complete", bold=True)))
        self.print_msg(f"Log is generated and saved to {path}")

    def _scan(self, args, ingest_config, walker):
        def progress_fn(*_, **kwargs):
            """Function for collecting scan progress"""
            if kwargs.get("total", None):
                self.progress.total = kwargs["total"]

            if kwargs.get("completed", None):
                self.progress.completed += kwargs["completed"]

            if self.progress.total > 0:
                self.print_msg(
                    f"{self.progress.completed} / {self.progress.total}",
                    replace=True,
                )

        self.print_msg(str(crayons.magenta("Scanning", bold=True)))

        strategy = dicom_strategy.DicomStrategy(args)
        scanner = dicom.DicomScanner(
            ingest_config=ingest_config,
            strategy_config=None,
            worker_config=i_config.WorkerConfig(),
            walker=walker,
            context=strategy.initial_context(),
            report_progress_fn=progress_fn,
        )

        return list(scanner.scan(""))

    def _configure_deid(self, ingest_config):
        def write_log(entry):
            self.logs.append(entry)

        # disable logging as the we've already logged these errors in scan
        logger = logging.getLogger("flywheel_migration.deidentify.dicom_file_profile")
        logger.disabled = True

        # It's needed to initialize the deid profile twice beacuse it inverts the fiels
        # in the profile and this way it produces the expected output
        deid_profile = deid.load_deid_profile(
            ingest_config.deid_profile, ingest_config.deid_profiles
        )
        deid_profile.initialize()

        deid_profile = deid.load_deid_profile(
            ingest_config.deid_profile, ingest_config.deid_profiles
        )
        logger.disabled = False
        deid_logger = deid.DeidLogger(write_log)
        for file_profile in deid_profile.file_profiles:
            file_profile.set_log(deid_logger)
        deid_profile.initialize()

        return deid_profile

    def _process_files(self, items, deid_profile, walker):
        self.print_msg(str(crayons.magenta("\nProcessing files", bold=True)))

        total = len(items)
        completed = 0

        for uid_item in items:
            self.print_msg(f"{completed} / {total}", replace=True)
            completed += 1
            if isinstance(uid_item, T.ItemWithUIDs):
                item = uid_item.item
                if item.type == "packfile":
                    file_obj, _, _ = upload.create_packfile(
                        walker,
                        item.safe_filename
                        if item.safe_filename is not None
                        else item.filename,
                        item.files,
                        item.dir,
                        item.context,
                        deid_profile=deid_profile,
                        compression=zipfile.ZIP_STORED,
                    )
                    file_obj.close()
                else:
                    self.print_msg("\nnot a packfile")
            else:
                self.print_msg("\nnot ItemWithUIDs")

        self.print_msg(f"{completed} / {total}", replace=True)


class DeidCreateCommand(Command):
    """Ingest dicom command"""

    arg_table = [
        {
            "name": "dst_path",
            "metavar": "PATH",
            "help": "Save sample template to the specified path on the current machine",
            "positional": True,
        },
        {
            "name": "debug",
            "flags": ["-d", "--debug"],
            "group": "general",
            "help": "Turn on debug logging",
            "default": False,
            "action": "store_true",
        },
    ]

    def __init__(self, subparsers):
        super().__init__(
            subparsers, "create", help="Generate a sample de-identification template"
        )

    def configure(self, args):
        """Validate all config"""
        path = args.dst_path
        _, file_extension = os.path.splitext(path)
        if file_extension.lower() not in [".yaml", ".yml"]:
            raise AttributeError("The path has to end with .yaml or .yml")
        if not os.path.exists(path) and not os.path.exists(os.path.dirname(path)):
            dirname = os.path.dirname(path)
            if dirname:
                os.makedirs(dirname, exist_ok=True)

        root_config.Config.configure_logging(args)

    def run(self, args):
        """Run the deid create command"""
        with open(args.dst_path, "w", encoding="utf-8") as fh:
            fh.write(SAMPLE_DEID_PROFILE)

        self.print_msg("Sample template successfully created")


SAMPLE_DEID_PROFILE = """
# You can give your de-identification profile a name

name: custom

# Indicates where you want to place the de-id log. You will use this log file to preview
# the de-id updates before uploading
# The option is ignored in ingest, you can use --save-deid-logs PATH to save the log.

deid-log: ~/Documents/deid_log.csv

# Sets the filetype to DICOM

dicom:

  # Date-increment controls how many days to offset each date field
  # where the increment-date (shown below) is configured.
  #Positive values will result in later dates, negative
  # values will result in earlier dates.

  date-increment: -17

  # patient-age-from-birthdate sets the DICOM header as a 3-digit value with a suffix
  # be 091D, and that same age in months would be 003M. By default, if
  # the age fits in days, then days will be used,
  # otherwise if it fits in months, then months
  # will be used, otherwise years will be used

  patient-age-from-birthdate: true

  # Set patient age units as Years. Other options include months (M) and days (D)

  patient-age-units: Y

  # The following are field transformations.
  # Remove, replace-with, increment-date, hash, and hashuid can be used with any DICOM
  # field. Replace name with the DICOM field "keyword" by the DICOM standard
  fields:

    # Use remove Remove a dicom field Removes the field from the DICOM entirely.
    # If removal is not supported then this field will be blank.
    # This example removes PatientID.

    - name: PatientID
      remove: true

    # Replace a dicom field with the value provided.
    # This example replaces “StationName” with "XXXX" in Flywheel

    - name: StationName
      replace-with: XXXX

    # Offsets the date by the number of days defined in
    # the date-increment setting above, preserving the time
    # and timezone. In this example, StudyDate appears as 17 days earlier

    - name: StudyDate
      increment-date: true

    # One-Way hash a dicom field to a unique string

    - name: AccessionNumber
      hash: true

     # Replaces a UID field with a hashed version of that
     # field. The first four nodes (prefix) and last node
     # (suffix) will be preserved, with the middle being
     # replaced by the hashed value

    - name: ConcatenationUID
      hashuid: true
"""
