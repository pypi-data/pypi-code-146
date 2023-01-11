"""CLI Config"""
import argparse
import configparser
import json
import logging
import logging.handlers
import math
import multiprocessing
import os
import re
import time
import zipfile
import zlib

import yaml
from flywheel_migration import dcm, deidentify

from . import util, walker
from .folder_impl import FSWrapper
from .private_tags import add_private_tags
from .sdk_impl import SdkUploadWrapper

CONFIG_DIRPATH = os.path.join(util.FLYWHEEL_USER_HOME, ".config/flywheel")
CACHE_DIRPATH = os.path.join(util.FLYWHEEL_USER_HOME, ".cache/flywheel")

DEFAULT_CONFIG_PATH = os.path.join(CONFIG_DIRPATH, "cli.cfg")
DEFAULT_CLI_LOG_PATH = os.path.join(CACHE_DIRPATH, "logs/cli.log")

LOG_FILE_PATH = os.path.expanduser(
    os.environ.get("FW_LOG_FILE_PATH", DEFAULT_CLI_LOG_PATH)
)
LOG_FILE_DIRPATH = os.path.dirname(LOG_FILE_PATH)

RE_CONFIG_LINE = re.compile(r"^\s*([-_a-zA-Z0-9]+)\s*([:=]\s*(.+?))?\s*$")

FW_CLI_BOTO_LOG_LEVEL = str(os.environ.get("FW_CLI_BOTO_LOG_LEVEL", "CRITICAL"))
MAX_DEFAULT_JOBS = 4


class ConfigError(Exception):
    """Handling Errors"""

    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return self.msg


class Config:
    """CLI Config"""

    default_config = {}

    def __init__(self, args=None):
        # pylint: disable=too-many-statements
        self._resolver = None

        # Configure logging
        if os.environ.get("FW_DISABLE_LOGS") != "1":
            self.configure_logging(args)

        # Set the default compression (used by zipfile/ZipFS)
        self.compression_level = getattr(args, "compression_level", 1)
        if self.compression_level > 0:
            zlib.Z_DEFAULT_COMPRESSION = self.compression_level

        self.cpu_count = getattr(args, "jobs", 1)
        if self.cpu_count == -1:
            self.cpu_count = max(
                1, min(math.floor(multiprocessing.cpu_count() / 2), MAX_DEFAULT_JOBS)
            )

        self.concurrent_uploads = getattr(args, "concurrent_uploads", 4)

        self.follow_symlinks = getattr(args, "symlinks", False)

        self.buffer_size = 65536
        self.max_spool = getattr(args, "max_tempfile", 50) * (
            1024 * 1024
        )  # Max tempfile size before rolling over to disk

        # Assume yes option
        self.assume_yes = getattr(args, "yes", False)
        self.max_retries = getattr(args, "max_retries", 3)
        self.retry_wait = 5  # Wait 5 seconds between retries

        # Certificates
        ca_certs = getattr(args, "ca_certs", None)
        if ca_certs is not None:
            # Monkey patch certifi.where()
            import certifi  # pylint: disable=import-outside-toplevel

            certifi.where = lambda: ca_certs
            logging.info(f"Using certificates override: {certifi.where()}")

        # Time Zone
        timezone = getattr(args, "timezone", None)
        if timezone is not None:
            # Validate the timezone string
            import flywheel_migration  # pylint: disable=import-outside-toplevel
            import pytz  # pylint: disable=import-outside-toplevel

            try:
                tz = pytz.timezone(timezone)
            except pytz.exceptions.UnknownTimeZoneError as exc:
                raise ConfigError(f"Unknown timezone: {timezone}") from exc

            # Update the default timezone for flywheel_migration and util
            util.DEFAULT_TZ = tz
            flywheel_migration.util.DEFAULT_TZ = tz

            # Also set in the environment
            os.environ["TZ"] = timezone

        # Set output folder
        self.output_folder = getattr(args, "output_folder", None)

        # Skip existing files
        self.skip_existing_files = getattr(args, "skip_existing", False)

        # Set use_uids property (default is use uids)
        self.use_uids = not getattr(args, "no_uids", False)

        # Set check_unique_uids property (default is False)
        self.check_unique_uids = getattr(args, "unique_uids", False)

        # Set copy_duplicates property (default is False)
        self.copy_duplicates = getattr(args, "copy_duplicates", False)

        # Set duplicates_folder property (default is None)
        # note that Dicom Scanner defaults to level up from specified import folder
        self.duplicates_folder = getattr(args, "duplicates_folder", None)

        # Get de-identification profile
        profile_name = (
            "minimal"
            if getattr(args, "de_identify", False)
            else getattr(args, "profile", None)
        )

        if not profile_name:
            profile_name = "none"

        try:
            self.deid_profile = self.load_deid_profile(profile_name, args=args)
        except deidentify.ValidationError as exc:  # pylint: disable=no-member
            raise ConfigError(str(exc)) from exc

        # Add private dicom tags
        dicom_tags_file = getattr(args, "private_dicom_tags", None)
        if dicom_tags_file is not None:
            add_private_tags(dicom_tags_file)

        # Handle unknown dicom tags
        if getattr(args, "ignore_unknown_tags", False):
            dcm.global_ignore_unknown_tags()

        # Register encoding aliases
        encoding_aliases = getattr(args, "encodings", None)
        if encoding_aliases is not None:
            Config.register_encoding_aliases(encoding_aliases)

        # An audit file to track which files are being uploaded to where
        self.audit_log = not getattr(args, "no_audit_log", False)
        if self.audit_log:
            self.audit_log = getattr(args, "audit_log_path", None) or True

        self.related_acquisitions = getattr(args, "related_acquisitions", False)

        self.walk_filters = {
            "include": getattr(args, "filter", []),
            "exclude": getattr(args, "exclude", []),
            "include_dirs": getattr(args, "include_dirs", []),
            "exclude_dirs": getattr(args, "exclude_dirs", []),
        }

    def get_compression_type(self):
        """Returns compression type"""
        if self.compression_level == 0:
            return zipfile.ZIP_STORED
        return zipfile.ZIP_DEFLATED

    def get_resolver(self):
        """Configure resolver"""
        if not self._resolver:
            if self.output_folder:
                self._resolver = FSWrapper(self.output_folder)
            else:
                fw = util.get_sdk_client_for_current_user()
                self._resolver = SdkUploadWrapper(fw)

        return self._resolver

    def get_uploader(self):
        """Configure uploader"""
        # Currently all resolvers are uploaders
        return self.get_resolver()

    def create_walker(self, fs_url, **kwargs):
        """Create walker"""
        # Merge include/exclusion lists
        for key in ("include", "exclude", "include_dirs", "exclude_dirs"):
            kwargs[key] = util.merge_lists(kwargs.get(key, []), self.walk_filters[key])
        kwargs.setdefault("follow_symlinks", self.follow_symlinks)

        return walker.create_walker(fs_url, **kwargs)

    @staticmethod
    def load_deid_profile(name, args=None):
        """Set deid profile"""
        if os.path.isfile(name):
            return deidentify.load_profile(name)

        # Load default profiles
        profiles = deidentify.load_default_profiles()
        for profile in profiles:
            if profile.name == name:
                return profile

        msg = f"Unknown de-identification profile: {name}"
        if args:
            args.parser.error(msg)
        raise ValueError(msg)

    @staticmethod
    def configure_logging(args):
        """Logging config"""
        root = logging.getLogger()
        boto3_log = logging.getLogger("botocore")
        # Propagate all debug logging
        root.setLevel(logging.DEBUG)

        boto3_level = getattr(logging, FW_CLI_BOTO_LOG_LEVEL.upper())
        boto3_log.setLevel(boto3_level)

        # Always log to cli log file (except when disabled)
        if os.environ.get("FW_DISABLE_LOG_FILE") != "1":
            log_path = LOG_FILE_PATH
            log_dir = os.path.dirname(log_path)
            if not os.path.isdir(log_dir):
                os.makedirs(log_dir)

            # Use GMT ISO date for logfile
            file_formatter = logging.Formatter(
                fmt="%(asctime)s.%(msecs)03d %(levelname)s %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
            )
            file_formatter.converter = time.gmtime

            # Allow environment overrides for log size and backup count
            log_file_size = int(
                os.environ.get("FW_LOG_FILE_SIZE", "5242880")
            )  # Default is 5 MB
            log_file_backup_count = int(
                os.environ.get("FW_LOG_FILE_COUNT", "2")
            )  # Default is 2

            file_handler = logging.handlers.RotatingFileHandler(
                log_path, maxBytes=log_file_size, backupCount=log_file_backup_count
            )
            file_handler.setFormatter(file_formatter)
            root.addHandler(file_handler)

        # Control how much (if anything) goes to console
        console_log_level = logging.INFO
        if getattr(args, "quiet", False):
            console_log_level = logging.ERROR
        elif getattr(args, "debug", False):
            console_log_level = logging.DEBUG

        console_formatter = logging.Formatter(fmt="%(levelname)s: %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(console_log_level)
        root.addHandler(console_handler)
        # Finally, capture all warnings to the logging framework
        logging.captureWarnings(True)

    @staticmethod
    def get_global_parser():
        """Get global parser"""
        parser = argparse.ArgumentParser(add_help=False)
        config_group = parser.add_mutually_exclusive_group()
        config_group.add_argument(
            "--config-file", "-C", help="Specify configuration options via config file"
        )
        config_group.add_argument(
            "--no-config",
            action="store_true",
            help="Do NOT load the default configuration file",
        )

        parser.add_argument(
            "-y",
            "--yes",
            action="store_true",
            help="Assume the answer is yes to all prompts",
        )
        parser.add_argument(
            "--ca-certs", help="The file to use for SSL Certificate Validation"
        )
        parser.add_argument(
            "--timezone", help="Set the effective local timezone for imports"
        )

        log_group = parser.add_mutually_exclusive_group()
        log_group.add_argument(
            "--debug", action="store_true", help="Turn on debug logging"
        )
        log_group.add_argument(
            "--quiet", action="store_true", help="Squelch log messages to the console"
        )
        return parser

    @staticmethod
    def get_import_parser():
        """Get import parser"""
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            "--max-retries",
            default=3,
            help="Maximum number of retry attempts, if assume yes",
        )
        parser.add_argument(
            "--jobs",
            "-j",
            default=-1,
            type=int,
            help="The number of concurrent jobs to run (e.g. compression jobs)",
        )
        parser.add_argument(
            "--concurrent-uploads",
            default=4,
            type=int,
            help="The maximum number of concurrent uploads",
        )
        parser.add_argument(
            "--compression-level",
            default=1,
            type=int,
            choices=range(-1, 9),
            help="The compression level to use for packfiles. -1 for default, 0 for store",
        )
        parser.add_argument(
            "--symlinks",
            action="store_true",
            help="follow symbolic links that resolve to directories",
        )
        parser.add_argument(
            "--include-dirs",
            action="append",
            dest="include_dirs",
            help="Patterns of directories to include",
        )
        parser.add_argument(
            "--exclude-dirs",
            action="append",
            dest="exclude_dirs",
            help="Patterns of directories to exclude",
        )
        parser.add_argument(
            "--include",
            action="append",
            dest="filter",
            help="Patterns of filenames to include",
        )
        parser.add_argument(
            "--exclude",
            action="append",
            dest="exclude",
            help="Patterns of filenames to exclude",
        )
        parser.add_argument(
            "--output-folder",
            help="Output to the given folder instead of uploading to flywheel",
        )
        parser.add_argument(
            "--no-uids",
            action="store_true",
            help="Ignore UIDs when grouping sessions and acquisitions",
        )
        parser.add_argument(
            "--unique-uids",
            action="store_true",
            help="Warn before creating any containers with duplicate UIDs",
        )
        parser.add_argument(
            "--copy-duplicates",
            action="store_true",
            help="When --unique-uids argument is defined copy the duplicates to a specific folder",
        )
        parser.add_argument(
            "--duplicates-folder",
            help="Copy duplicates into this folder (default: level up from specified import folder)",
        )
        parser.add_argument(
            "--max-tempfile",
            default=50,
            type=int,
            help="The max in-memory tempfile size, in MB, or 0 to always use disk",
        )
        parser.add_argument(
            "--skip-existing", action="store_true", help="Skip import of existing files"
        )
        parser.add_argument(
            "--no-audit-log", action="store_true", help="Don't generate an audit log."
        )
        parser.add_argument("--audit-log-path", help="Location to save audit log")
        parser.add_argument(
            "--private-dicom-tags", help="Path to a private dicoms csv file"
        )
        parser.add_argument(
            "--ignore-unknown-tags",
            action="store_true",
            help="Ignore unknown dicom tags",
        )
        parser.add_argument(
            "--encodings", help="Set character encoding aliases. E.g. win_1251=cp1251"
        )
        parser.add_argument(
            "--related-acquisitions",
            action="store_true",
            help="Store related dicoms in the same acquisition",
        )
        return parser

    @staticmethod
    def get_deid_parser():
        """Get deid parser"""
        parser = argparse.ArgumentParser(add_help=False)
        deid_group = parser.add_mutually_exclusive_group()
        deid_group.add_argument(
            "--de-identify",
            action="store_true",
            help="De-identify DICOM files, e-files and p-files prior to upload",
        )
        deid_group.add_argument(
            "--profile", help="Use the De-identify profile by name or file"
        )
        return parser

    @staticmethod
    def set_defaults(parsers):
        """Set defaults for each subparser"""
        # Read defaults from:
        # ~/.config/flywheel/cli.cfg
        # --config-file, -C
        defaults = Config.read_config_defaults()

        # Then set defaults for each subparser
        for parser in parsers.values():
            if not parser.get_default("skip_load_defaults"):
                parser.set_defaults(**defaults)

    @staticmethod
    def read_config_defaults(args=None):
        """Read config defaults from the default file, and an optional arg file"""

        # Parse config_file argument from command line
        if args is None:
            config_parser = Config.get_global_parser()
            args, _ = config_parser.parse_known_args()

        defaults = {}

        if (getattr(args, "no_config", False)) or (
            getattr(args, "config_file", "") == ""
        ):
            return defaults
        for path in [DEFAULT_CONFIG_PATH, args.config_file]:
            if not path:
                continue

            path = os.path.expanduser(path)
            if os.path.isfile(path):
                if not args.quiet:
                    print(f"Reading config options from: {path}")
                Config.read_config_file(path, defaults)

        return defaults

    @staticmethod
    def load_duplicates(args):
        js = Config.read_config_defaults(args)
        if "detect-duplicates" in js:
            if js["detect-duplicates"] is True:
                args.detect_duplicates = True
        if "detect-duplicates-override" in js:
            args.detect_duplicates_override = js["detect-duplicates-override"]

    @staticmethod
    def read_config_file(path, dest):
        if path.endswith(".yml") or path.endswith(".yaml"):
            try:
                with open(path, "rb") as file:
                    dest.update(yaml.safe_load(file))
            except (OSError, yaml.YAMLError, ValueError):
                logging.exception(f"Error reading YAML config {path}")
                raise

        elif path.endswith(".json"):
            try:
                with open(path, "rb") as file:
                    dest.update(json.load(file))
            except (OSError, json.decoder.JSONDecodeError):
                logging.exception(f"Error reading JSON config {path}")
                raise
        elif path.endswith(".ini"):
            try:
                cf = configparser.ConfigParser()
                cf.read(path)
                for sec in cf.sections():
                    for opt in cf.options(sec):
                        dest[str(opt)] = str(cf.get(sec, opt))
            except (OSError, configparser.Error):
                logging.exception(f"Error reading INI config {path}")
                raise

    @staticmethod
    def register_encoding_aliases(encoding_aliases):
        """Register common encoding aliases"""
        import encodings  # pylint: disable=import-outside-toplevel

        for encoding_spec in re.split(r"[,\s]+", encoding_aliases):
            if not encoding_spec:
                continue
            key, _, value = encoding_spec.partition("=")
            encodings.aliases.aliases[key.strip().lower()] = value.strip().lower()
