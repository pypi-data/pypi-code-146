"""Utils for CLI"""
# pylint: disable=C0302
import argparse
import collections
import datetime
import errno
import functools
import itertools
import json
import logging
import math
import os
import platform
import re
import stat
import string
import subprocess
import sys
from typing import Any, Dict, Iterable, Iterator, List, Optional
from urllib.parse import parse_qs, urlparse

import dateutil.parser
import flywheel
import fs
import pathvalidate
import pytz
import requests
import tzlocal
from dateutil.parser import parse
from flywheel_migration.dcm import DicomFile
from pydicom.multival import MultiValue

from . import __version__, errors, models

log = logging.getLogger(__name__)

FLYWHEEL_USER_HOME = os.path.expanduser(os.getenv("FLYWHEEL_USER_HOME", "~"))
AUTH_CONFIG_PATH = os.path.join(FLYWHEEL_USER_HOME, ".config/flywheel/user.json")

METADATA_FIELDS = (
    "group._id",
    "group.label",
    "project._id",
    "project.label",
    "session._id",
    "session.uid",
    "session.label",
    "session.timestamp",
    "subject._id",
    "subject.label",
    "acquisition._id",
    "acquisition.uid",
    "acquisition.label",
    "acquisition.timestamp",
)

METADATA_ALIASES = {
    "group": "group._id",
    "project": "project.label",
    "session": "session.label",
    "subject": "subject.label",
    "acquisition": "acquisition.label",
}

METADATA_TYPES = {"group": "string-id", "group._id": "string-id"}

METADATA_EXPR = {"string-id": r"[0-9a-z][0-9a-z.@_-]{0,30}[0-9a-z]", "default": r".+"}

METADATA_FUNC = {"session.timestamp": parse, "acquisition.timestamp": parse}

NO_FILE_CONTAINERS = ["group"]

CONNECT_TIMEOUT: int = int(os.getenv("FLYWHEEL_CLI_CONNECT_TIMEOUT", "30"))
READ_TIMEOUT: int = int(os.getenv("FLYWHEEL_CLI_READ_TIMEOUT", "60"))


try:
    DEFAULT_TZ = tzlocal.get_localzone()
except pytz.exceptions.UnknownTimeZoneError:
    print("Could not determine timezone, defaulting to UTC")
    DEFAULT_TZ = pytz.utc


def sanitize_filename(filename):
    """
    Sanitize filename to be valid on all platforms (Linux/Windows/macOS/Posix)
    The asterisk in t2*, t2 *, t2_* (case insensitive) will be changed to the word "star"
    prior to sanitization
    """
    # IMPORTANT
    # this code has to be the same every other places where we sanitize (CLI, CORE)
    # if it's getting more complicated it has to be moved into it's separate repo
    if filename is None:
        return None
    pathvalidate.validate_pathtype(filename)

    filename = re.sub(r"(t2 ?_?)\*", r"\1star", str(filename), flags=re.IGNORECASE)
    return pathvalidate.sanitize_filename(
        filename, replacement_text="_", platform="universal"
    )


@functools.lru_cache()
def load_auth_config():
    """Load authentication config from file"""
    path = os.path.expanduser(AUTH_CONFIG_PATH)
    try:
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except (IOError, json.decoder.JSONDecodeError):
        config = {}
    return config


def save_api_key(api_key, root=False):
    """Save the given api key to the user's config file.

    If api_key is None, then remove it from the file.
    """
    config = load_auth_config()
    if config is None:
        config = {}

    if api_key is None:
        config.pop("key", None)
        config.pop("root", None)
    else:
        config["key"] = api_key
        config["root"] = root

    path = os.path.expanduser(AUTH_CONFIG_PATH)

    # Ensure directory exists
    config_dir = os.path.dirname(path)
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f)
    if platform.system() != "Windows":
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)


def set_nested_attr(obj, key, value):
    """Set a nested attribute in dictionary, creating sub dictionaries as necessary.

    Arguments:
        obj (dict): The top-level dictionary
        key (str): The dot-separated key
        value: The value to set
    """
    parts = key.split(".")
    for part in parts[:-1]:
        obj.setdefault(part, {})
        obj = obj[part]
    obj[parts[-1]] = value


def get_nested_attr(obj, key):
    """Get a nested attribute from a dictionary

    Args:
        obj (dict): The top-level dictionaty
        key (str): The dot-separated key

    Returns: The value or None
    """
    parts = key.split(".")
    for part in parts[:-1]:
        obj = obj.get(part, {})
    return obj.get(parts[-1])


def sorted_container_nodes(containers):
    """Returns a sorted iterable of containers sorted by label or id (whatever is available)

    Arguments:
        containers (iterable): The the list of containers to sort

    Returns:
        iterable: The sorted set of containers
    """
    return sorted(
        containers, key=lambda x: (x.label or x.id or "").lower(), reverse=True
    )


class UnsupportedFilesystemError(Exception):
    """Error for unsupported filesystem type"""


def to_fs_url(path, support_archive=True):
    """Convert path to an fs url (such as osfs://~/data)

    Arguments:
        path (str): The path to convert
        support_archive (bool): Whether or not to support archives

    Returns:
        str: A filesystem url
    """
    if path.find(":") > 1:
        # Likely a filesystem URL
        return path

    # Check if the path actually exists
    if not os.path.exists(path):
        raise UnsupportedFilesystemError(f"Path {path} does not exist!")

    if not os.path.isdir(path):
        if support_archive:
            # Specialized path options for tar/zip files
            if is_tar_file(path):
                return f"tar://{path}"

            if is_zip_file(path):
                return f"zip://{path}"

        log.debug(f"Unknown filesystem type for {path}: stat={os.stat(path)}")
        raise UnsupportedFilesystemError(
            f"Unknown or unsupported filesystem for: {path}"
        )

    # Default is OSFS pointing at directory
    return f"osfs://{path}"


def open_fs(path):
    """Wrapper for fs.open_fs"""
    return fs.open_fs(path)


def is_tar_file(path):
    """Check if path appears to be a tar archive"""
    return bool(re.match(r"^.*(\.tar|\.tgz|\.tar\.gz|\.tar\.bz2)$", path, re.I))


def is_zip_file(path):
    """Check if path appears to be a zip archive"""
    _, ext = fs.path.splitext(path.lower())
    return ext == ".zip"


def is_archive(path):
    """Check if path appears to be a zip or tar archive"""
    return is_zip_file(path) or is_tar_file(path)


def confirmation_prompt(message):
    """Continue prompting at the terminal for a yes/no repsonse

    Arguments:
        message (str): The prompt message

    Returns:
        bool: True if the user responded yes, otherwise False
    """
    responses = {"yes": True, "y": True, "no": False, "n": False}
    while True:
        print(f"{message} (yes/no): ", end="")
        choice = input().lower()
        if choice in responses:
            return responses[choice]
        print('Please respond with "yes" or "no".')


def perror(*args, **kwargs):
    """Print to stderr"""
    kwargs["file"] = sys.stderr
    kwargs["flush"] = True
    print(*args, **kwargs)


def contains_dicoms(walker):
    """Check if the given walker contains dicoms"""
    # If we encounter a single dicom, assume true
    for _, _, files in walker.walk():
        for file_info in files:
            if is_dicom_file(file_info.name):
                return True
    return False


DICOM_EXTENSIONS = (".dcm", ".dcm.gz", ".dicom", ".dicom.gz", ".ima", ".ima.gz")


def is_dicom_file(path):
    """Check if the given path appears to be a dicom file.

    Only looks at the extension, not the contents.

    Args:
        path (str): The path to the dicom file

    Returns:
        bool: True if the file appears to be a dicom file
    """
    path = path.lower()
    for ext in DICOM_EXTENSIONS:
        if path.endswith(ext):
            return True
    return False


def localize_timestamp(timestamp, timezone=None):
    """Localize timestamp"""
    timezone = DEFAULT_TZ if timezone is None else timezone
    return timezone.localize(timestamp)


def split_key_value_argument(val):
    """Split value into a key, value tuple.

    Raises ArgumentTypeError if val is not in key=value form

    Arguments:
        val (str): The key value pair

    Returns:
        tuple: The split key-value pair
    """
    key, delim, value = val.partition("=")

    if not delim:
        raise argparse.ArgumentTypeError(
            "Expected key value pair in the form of: key=value"
        )

    return (key.strip(), value.strip())


def parse_datetime_argument(val):
    """Convert an argument into a datetime value using dateutil.parser.

    Raises ArgumentTypeError if the value is inscrutable

    Arguments:
        val (str): The date-time value string

    Returns:
        datetime: The parsed datetime instance
    """
    try:
        return dateutil.parser.parse(val)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(" ".join(exc.args))


def group_id(group_id):  # pylint: disable=redefined-outer-name
    """Checks if group name is valid"""
    pattern = "^[0-9a-z][0-9a-z.@_-]{0,30}[0-9a-z]$"
    if not re.match(pattern, group_id):
        raise TypeError(f"{group_id} does not match schema {pattern}")
    return group_id


def args_to_list(items):
    """Convert an argument into a list of arguments (by splitting each element on comma)"""
    result = []
    if items is not None:
        for item in items:
            if item:
                for val in item.split(","):
                    val = val.strip()
                    if val:
                        result.append(val)
    return result


def files_equal(walker, path1, path2):
    """Checks if two files are equal"""
    chunk_size = 8192

    with walker.open(path1, "rb") as f1, walker.open(path2, "rb") as f2:
        while True:
            chunk1 = f1.read(chunk_size)
            chunk2 = f2.read(chunk_size)

            if chunk1 != chunk2:
                return False

            if not chunk1:
                return True


def regex_for_property(name):
    """Get the regular expression match template for property name

    Arguments:
        name (str): The property name

    Returns:
        str: The regular expression for that property name
    """
    property_type = METADATA_TYPES.get(name, "default")
    if property_type in METADATA_EXPR:
        return METADATA_EXPR[property_type]
    return METADATA_EXPR["default"]


def str_to_python_id(val):
    """Convert a string to a valid python id in a reversible way

    Arguments:
        val (str): The value to convert

    Returns:
        str: The valid python id
    """
    result = ""
    for char in val:
        if char in string.ascii_letters or char == "_":
            result = result + char
        else:
            result = result + f"__{ord(char) or 0:02x}__"
    return result


def python_id_to_str(val):
    """Convert a python id string to a normal string

    Arguments:
        val (str): The value to convert

    Returns:
        str: The converted value
    """
    return re.sub("__([a-f0-9]{2})__", _repl_hex, val)


def _repl_hex(match):
    return chr(int(match.group(1), 16))


def hrsize(size: int) -> str:
    """Return human-readable size from size value"""
    if size < 1000:
        return f"{size}B"
    for suffix in "KMGTPEZY":
        size /= 1024.0
        if size < 10.0:
            return f"{round(size, 1)}{suffix}B"
        if size < 1000.0:
            return f"{int(round(size, 0))}{suffix}B"
    return f"{int(round(size, 0))}YB"


def hrtime(seconds: int) -> str:
    """Return human-readable time from seconds"""
    remainder = seconds
    parts = []
    units = {"w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1}
    for k, v in units.items():
        quotient, remainder = divmod(remainder, v)
        if (len(parts) > 0 and not quotient) or len(parts) == 2:
            break
        if quotient or (len(parts) == 0 and k == "s"):
            parts.append(f"{int(quotient)}{k}")
    return " ".join(parts)


def edit_file(path):
    """
    Open the given path in a file editor, wait for the editor to exit.

    Arguments:
        path (str): The path to the file to edit
    """
    if sys.platform == "darwin":
        default_editor = "pico"
    elif sys.platform == "win32":
        default_editor = "notepad.exe"
    else:
        default_editor = "nano"

    editor = os.environ.get("EDITOR", default_editor)
    subprocess.call([editor, path])


def package_root():
    """Get a path to the package root folder"""
    pkg_dir = os.path.dirname(__file__)
    return os.path.abspath(pkg_dir)


def get_cli_version():
    """Get the installed CLI version"""
    return __version__


class KeyWithOptions:
    """Encapsulates user-provided configuration where a key field is required.

    Accepts either a dictionary or any other primitive.
    If given a dictionary, pops <key> from the dictionary, and stores it as an attribute.
    Otherwise takes the provided value and stores it as an attribute
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, value, key="name"):
        if isinstance(value, dict):
            self.config = value.copy()
            self.key = self.config.pop(key)
        else:
            self.key = value
            self.config = {}


class Bunch(dict):
    """Provides attribute access to key-value pairs"""

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError as exc:
            raise AttributeError(f"'Bunch' object has no attribute '{attr}'") from exc


def encode_json(obj: Any) -> Any:
    """JSON encode additional data types"""
    if isinstance(obj, set):
        return list(obj)
    if isinstance(obj, datetime.datetime):
        if obj.tzinfo is None:
            obj = pytz.utc.localize(obj)
        return obj.astimezone(pytz.utc).isoformat()
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    # default serialization/raising otherwise
    raise TypeError(repr(obj) + " is not JSON serializable")


# pylint: disable=C0103
json_serializer = functools.partial(
    json.dumps,
    default=encode_json,
    separators=(",", ":"),
)


def merge_lists(list_a, list_b):
    """Merge lists 'list_a' and 'list_b', returning the result or None if the result is empty"""
    result = (list_a or []) + (list_b or [])
    if result:
        return result
    return None


def pluralize(container_type):
    """Convert container_type to plural name

    Simplistic logic that supports:
    group,  project,  session, subject, acquisition, analysis, collection
    """
    if container_type == "analysis":
        return "analyses"
    if not container_type.endswith("s"):
        return container_type + "s"
    return container_type


def path_to_relpath(base, path):
    """Convert path to relpath which not includes base."""
    return fs.path.frombase(
        fs.path.forcedir(fs.path.abspath(base)), fs.path.abspath(path)
    )


def get_filepath(path, prefix=None, extension="csv"):
    """Create random filename with the given prefix if the path is a dir
    otherwise verifies the file not exists yet to prevent overwriting
    anything.

    Returns: filepath or None if couldn't find a proper filename
    """
    path = os.path.expanduser(path)
    if os.path.isdir(path):
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        cli_version = get_cli_version()
        filename = f"{prefix or 'log'}-{timestamp}-{cli_version}.{extension}"
        return os.path.join(path, filename)

    if path.endswith(os.sep):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

    if os.path.isfile(path):
        raise FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST), path)

    return path


def get_incremental_filename(path):
    """Get unique filename by incrementing sequence number in filename"""
    filename, ext = os.path.splitext(os.path.basename(path))
    seq = 0
    match = re.match(r"(?P<name>.*)\((?P<seq>\d+)\)", filename)
    if match:
        filename = match.group("name")
        seq = int(match.group("seq"))

    while os.path.isfile(path):
        seq += 1
        new_filename = f"{filename}({seq})"
        if ext:
            new_filename = f"{new_filename}{ext}"
        path = os.path.join(os.path.dirname(path), new_filename)

    return path


def create_missing_dirs(dst_path: str) -> None:
    """Create missing middle level directories"""
    dst_dir = os.path.dirname(dst_path)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)


def chunks(iterable: Iterable[Any], size: int) -> Iterator[List[Any]]:
    """Break the given iterable into chunks of size N"""
    it = iter(iterable)
    chunk = list(itertools.islice(it, size))
    while chunk:
        yield chunk
        chunk = list(itertools.islice(it, size))


# DICOM utils
# Would be nice to have these in a separate package that shared for example
# between reaper and import/ingest


class DicomUtils:
    """Useful collection of utility methods to extract information from dicom files"""

    required_tags = [
        "Manufacturer",
        "AcquisitionNumber",
        "AcquisitionDate",
        "AcquisitionTime",
        "SeriesDate",
        "SeriesTime",
        "SeriesInstanceUID",
        "SeriesNumber",
        "ImageType",
        "StudyDate",
        "StudyTime",
        "StudyInstanceUID",
        "OperatorsName",
        "PatientName",
        "PatientID",
        "StudyID",
        "SeriesDescription",
        "PatientBirthDate",
        "SOPInstanceUID",
        "Modality",
    ]

    def __init__(self, deid_profile=None, get_subject_code_fn=None):
        self.deid_profile = deid_profile
        self.get_subject_code_fn = get_subject_code_fn

    def determine_subject_code(self, context, dcm):
        """Determine subject code"""
        subject_label = context.get("subject", {}).get("label")
        # Map subject
        if subject_label:
            subject_code = subject_label
        elif self.get_subject_code_fn:
            subject_code = self.get_subject_code_fn(dcm)
        else:
            subject_code = self.get_value(dcm, "PatientID")

        if subject_code is None:
            log.error(
                "Unable to determine valid subject code,"
                " please manually set subject code with --subject flag"
            )
            raise InvalidLabel("subject")

        return subject_code

    def determine_session_label(  # pylint: disable=W0613
        self, context, dcm, uid, timestamp=None
    ):
        """Determine session label from DICOM headers"""
        session_label = context.get("session", {}).get("label")
        if session_label:
            return session_label

        if timestamp:
            return timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return uid

    def determine_acquisition_label(self, context, dcm, uid, timestamp=None):
        """Determine acquisition label from DICOM headers"""
        acquisition_label = context.get("acquisition", {}).get("label")
        if acquisition_label:
            return acquisition_label

        label = self.get_value(dcm, "SeriesDescription")
        series_number = self.get_value(dcm, "SeriesNumber")
        if not label and timestamp:
            label = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        if not label:
            label = uid
        if isinstance(label, MultiValue):
            label = "_".join(label)
        if series_number is not None:
            label = f"{series_number} - {label}"
        return label

    def determine_acquisition_timestamp(self, dcm):
        """Get acquisition timestamp (based on manufacturer)"""
        # Create the acquisition because the acqusition doesn't exist
        if dcm.get_manufacturer() == "SIEMENS":
            timestamp = self.get_timestamp(dcm, "SeriesDate", "SeriesTime")
        else:
            timestamp = self.get_timestamp(dcm, "AcquisitionDate", "AcquisitionTime")
        return timestamp

    @staticmethod
    def determine_dicom_zipname(filenames: Dict[str, str], series_label: str) -> str:
        """Return a filename for the dicom series that is unique to a container

        Args:
            filenames (dict): A map of series uids to filenames
            series_label (str): The base to use for the filename

        Returns:
            str: The filename for the zipped up series
        """
        filename = series_label + ".dicom.zip"
        duplicate = 1
        while filename in filenames.values():
            filename = f"{series_label}_dup-{duplicate}.dicom.zip"
            duplicate += 1
        return filename

    def get_timestamp(self, dcm, date_key, time_key):
        """Get a timestamp value"""
        date_value = self.get_value(dcm, date_key)
        time_value = self.get_value(dcm, time_key)

        return DicomFile.timestamp(date_value, time_value, DEFAULT_TZ)

    def get_value(self, dcm, key, default=None, required=False):
        """Get a transformed value"""
        if self.deid_profile:
            result = self.deid_profile.get_value(None, dcm.raw, key)
            if not result:
                result = default
        else:
            result = dcm.get(key, default)

        if (
            result in (None, "") and required
        ):  # Explicit compare because zero is a valid value
            raise ValueError(f"DICOM is missing {key}")

        return result


class InvalidLabel(Exception):
    """Invalid label for container exception"""

    def __init__(self, container_type):
        self.msg = f"{container_type}.label '' not valid"
        super().__init__(self.msg)


def parse_resolver_path(path: str) -> List[str]:
    """Split out a string path, keeping analyses and files paths"""
    # TODO: Port this to SDK?
    if not path:
        return []

    if path.startswith("fw://"):
        path = path[5:]

    path = (path or "").strip("/")

    if "/files/" in path:
        path, file_path = path.split("/files/")
        file_path = ["files", file_path]
    else:
        file_path = []

    if "/analyses/" in path:
        path, analysis_path = path.split("/analyses/")
        analysis_path = ["analyses", analysis_path]
    else:
        analysis_path = []

    path = path.split("/") or []
    path = path + analysis_path + file_path

    return [path_el for path_el in path if path_el]


def get_api_key() -> str:
    """Return current user's API key from config"""
    config = load_auth_config()
    if not config or not config.get("key"):
        print(
            "Not logged in, please login using `fw login` and your API key",
            file=sys.stderr,
        )
        sys.exit(1)
    return config["key"]


def get_upload_ticket_suggested_headers(response):
    """Read headers response property. Return None if it doesn't exist or is empty"""
    headers = None
    if response is not None:
        try:
            if response["headers"] and isinstance(response["headers"], dict):
                headers = response["headers"]
        except KeyError:
            pass
    return headers


class PartialReader:
    """Wrapper for S3 multipart signed-url upload"""

    def __init__(self, fd, size):
        self._offset = fd.tell()
        self.fd = fd
        self.remaining = size
        self.original = size

    def __getattr__(self, attr):
        return getattr(self.fd, attr)

    def tell(self):
        return self.original - self.remaining

    def seek(self, offset, whence):
        if offset != 0 or whence != 0:
            raise ValueError("Invalid seek!")
        self.fd.seek(self._offset)

    def __len__(self):
        return self.remaining

    def read(self, n=-1):
        if self.remaining == 0:
            # signaling end
            return b""

        if self.remaining < n or n < 0:
            # last acutal chunk
            res = self.fd.read(self.remaining)
            self.remaining = 0
            return res

        self.remaining -= n
        return self.fd.read(n)


@functools.lru_cache(maxsize=16)
def get_sdk_client(api_key: str) -> flywheel.Client:
    """Cache and return SDK client for given API key"""
    client = SDKClient(api_key)
    log.debug(
        f"SDK Version: {flywheel.flywheel.SDK_VERSION}"  # pylint: disable=no-member
    )
    log.debug(f"Flywheel Site URL: {client.api_client.configuration.host}")
    return client


class SDKClient:
    """SDK client w/o version check and w/ request timeouts and signed url support"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        parts = api_key.rsplit(":", maxsplit=1)
        if len(parts) != 2:
            raise errors.AuthenticationError(
                "Invalid api key format. Required format: <host>:<key>"
            )
        self.host, self.key = parts
        self.fw = flywheel.Client(api_key)
        self.fw.enable_feature("multipart_signed_url")
        self.session = self.fw.api_client.rest_client.session
        cli_version = get_cli_version()
        useragent_info = get_useragent_info()
        self.fw.api_client.user_agent = (
            f"Flywheel CLI/{cli_version} ({useragent_info}) "
            + self.fw.api_client.user_agent
        )

        # disable version check
        self.fw.api_client.set_version_check_fn(None)

        # set request timeouts
        request = self.fw.api_client.rest_client.session.request
        timeout = CONNECT_TIMEOUT, READ_TIMEOUT
        request_with_timeout = functools.partial(request, timeout=timeout)
        self.fw.api_client.rest_client.session.request = request_with_timeout

        # check signed url support
        config = self.fw.api_client.call_api(
            "/config", "GET", _return_http_data_only=True, _preload_content=False
        ).json()
        features = config.get("features", {})

        self.deid_log = features.get("deid_log")
        self.deid_log_url = config.get("site", {}).get("deid_log_url")
        self.deid_profile = features.get("deid_profile")
        self.signed_url = features.get("signed_url") or config.get("signed_url")
        self.multiproject = features.get("multiproject", False)
        self.multipart_signed_url = features.get("multipart_signed_url", False)
        self.signed_map = LRUCache()

        self._auth_info = None

    def __getattr__(self, name):
        """Pass-through attribute access to the original client"""
        return getattr(self.fw, name)

    def upload(self, cont_name, cont_id, filename, fileobj, metadata=None):
        """
        Upload file to container
        If signed_url flag is active we try to upload with signed only
        If the multiproject is active we try signed first, fallback to ordinary upload
        """
        signed_successful = False
        sdk_upload = getattr(self.fw, f"upload_file_to_{cont_name}")
        log.debug(f"Uploading {filename} to {cont_name}/{cont_id}")
        size = os.fstat(fileobj.fileno()).st_size
        key = f"{cont_name}{cont_id}"
        if not metadata:
            metadata = {}
        if not metadata.get("size") and self.signed_url and self.multipart_signed_url:
            # It can only be received by core-api if feature is enabled
            metadata["size"] = size
        if self.signed_url or (self.multiproject and self.signed_map.get(key, True)):
            signed_successful = self.signed_url_upload(
                cont_name, cont_id, filename, fileobj, metadata=metadata
            )
            self.signed_map[key] = signed_successful
        if not signed_successful:
            if self.signed_url:
                # with signed_url flag only signed upload is possible
                raise errors.BaseError(
                    f"Could not upload {filename} to {cont_name}/{cont_id} using signed upload"
                )

            filespec = flywheel.FileSpec(filename, fileobj)
            sdk_upload(cont_id, filespec, metadata=json_serializer(metadata))
        log.debug(f"Uploaded {filename} ({fs.filesize.traditional(size)})")

    def signed_url_upload(self, cont_name, cont_id, filename, fileobj, metadata=None):
        """Upload file to container using signed urls"""
        url = f"/{cont_name}s/{cont_id}/files"
        ticket, signed_url, headers = self.create_upload_ticket(
            url, filename, metadata=metadata
        )
        if not ticket:
            log.debug("Can't use signed url upload, fallback")
            return False

        if isinstance(signed_url, list):
            return self.multipart_signed_url_upload(
                url, ticket, signed_url, headers, fileobj, metadata
            )

        log.debug(f"Using simple signed url {signed_url}")
        self.session.put(signed_url, data=fileobj, headers=headers)  # use api session
        self.call_api(url, "POST", query_params=[("ticket", ticket)])
        return True

    def multipart_signed_url_upload(
        self, core_url, ticket, signed_urls, headers, fileobj, metadata
    ):
        log.debug("Using S3 multipart upload")
        if not headers:
            headers = {}
        part_size = math.ceil(metadata["size"] / len(signed_urls))
        log.debug(f"Signed urls: {signed_urls}, part_size={part_size}")
        e_tags = []
        s3_upload_id = None
        for part_num, part_url in enumerate(signed_urls):
            log.debug(f"Upload to {part_url}")
            if not s3_upload_id:
                parsed = urlparse(part_url)
                upload_dict = parse_qs(parsed.query)
                if "uploadId" in upload_dict:
                    s3_upload_id = upload_dict["uploadId"][0]

            # Splitting file into parts with PartialReader
            remaining = metadata["size"] - part_size * part_num
            reader = PartialReader(
                fileobj, remaining if remaining < part_size else part_size
            )
            r = requests.put(part_url, data=reader, headers=headers)
            if not r.ok:
                log.debug(
                    f"Multipart upload failed: {part_url} {r.status_code} {r.content}"
                )
                return False
            etag_dict = r.headers
            if "ETag" in etag_dict:
                e_tags.append(etag_dict["ETag"].strip('"'))
        log.debug(f"Completing ticket {ticket}")
        if s3_upload_id and len(e_tags) != 0:
            self.call_api(
                core_url,
                "POST",
                query_params=[("ticket", ticket)],
                body={"multipart": {"e_tags": e_tags, "upload_id": s3_upload_id}},
            )
        else:
            self.call_api(core_url, "POST", query_params=[("ticket", ticket)])
        return True

    def create_upload_ticket(self, url, filename, metadata=None):
        """Create signed url upload ticket"""
        response = self.call_api(
            url,
            "POST",
            body={"metadata": metadata or {}, "filenames": [filename]},
            query_params=[("ticket", "")],
            response_type=object,
        )
        if "ticket" not in response and "urls" not in response:
            # no signed url support, fallback
            return None, None, None

        headers = get_upload_ticket_suggested_headers(response)
        return response["ticket"], response["urls"][filename], headers

    def post_deid_log(self, payload) -> str:
        """Post deid log payload to the De-Id api"""
        resp = self.session.post(
            f"{self.deid_log_url}/logs",
            json=payload,
            headers={"Authorization": f"scitran-user {self.api_key}"},
        )
        return resp.json()["id"]

    def safe_lookup(self, path: List[str]) -> Any:
        """Lookup with exception handling and caching"""
        path = [i for i in path if i is not None]
        if not path:
            return None

        resolved = None

        try:
            resolved = self.fw.lookup(path)
        except flywheel.ApiException as exc:
            if exc.status == 403:
                path_str = "/".join(path)
                raise errors.NotEnoughPermissions(
                    f"User does not have access to '{path_str}'"
                )
            if exc.status != 404:
                raise
        return resolved

    def can_import_into(  # pylint: disable=R0912
        self, group: Optional[str] = None, project: Optional[str] = None
    ) -> None:
        """Verify that current user can import into the given group and porject"""
        if self.auth_info.is_device:
            # devices have rigths to import anywhere
            return

        if self.auth_info.is_admin:
            # site admins have rigths to import anywhere
            return

        if not group:
            # if group not present can't verify
            return

        resolved_grp = self.safe_lookup([group])

        if not (resolved_grp or self.auth_info.is_admin):
            # only site admin can create new group
            raise errors.NotEnoughPermissions(
                f"User does not have access to create '{group}'"
            )

        if not (resolved_grp and project):
            # skip further check if no project
            return

        resolved_prj = self.safe_lookup([group, project])

        if not (resolved_prj or self.get_group_access(resolved_grp) == "admin"):
            # check that user can create new project in this group
            raise errors.NotEnoughPermissions(
                f"User does not have access to create '{group}/{project}'"
            )

        if not resolved_prj:
            # skip further check if it will be a new project
            return

        # finally check roles
        required_actions = {"containers_create_hierarchy", "files_create_upload"}
        having_actions = self.get_user_actions(resolved_prj)

        if not required_actions.issubset(having_actions):
            req_str = ", ".join(sorted(required_actions))
            missing_str = ", ".join(sorted(required_actions - having_actions))
            msg = (
                f"User does not have the required permissions ({req_str}) "
                f"in '{project}' project. "
                f"Missing permissions: {missing_str}"
            )
            raise errors.NotEnoughPermissions(msg)

    def can_create_project_in_group(self, group: str) -> None:
        """Verify that user can create project in group"""

        if self.auth_info.is_admin:
            # site admins have rigths
            return

        resolved_grp = self.safe_lookup([group])

        if not (resolved_grp or self.auth_info.is_admin):
            # only site admin can create new group
            raise errors.NotEnoughPermissions(
                f"User does not have access to create '{group}'"
            )

        if not resolved_grp:
            return

        if self.get_group_access(resolved_grp) != "admin":
            raise errors.NotEnoughPermissions(
                f"User does not have access to create new project in '{group}'"
            )

    def get_user_actions(self, container) -> List[str]:
        """Return user's permissions in the container"""
        role_ids = []
        for perm in container.permissions:
            if perm.id == self.auth_info.user_id:
                role_ids = perm.role_ids

        having_actions = set()
        for role_id in role_ids:
            role = self.fw.get_role(role_id)

            having_actions.update(role.actions)

        return having_actions

    def get_group_access(self, group: flywheel.models.Group) -> Optional[str]:
        """Get group access of the current user"""
        for perm in group.permissions:
            if perm.id == self.auth_info.user_id:
                return perm.access
        return None

    @property
    def auth_info(self) -> models.FWAuth:
        """Return FWAuth on successful core auth, otherwise raise AuthenticationError"""
        if self._auth_info:
            return self._auth_info

        try:
            auth_status = self.fw.get_auth_status()
        except flywheel.ApiException as exc:
            raise errors.AuthenticationError(exc.reason, exc.status)

        self._auth_info = models.FWAuth(
            api_key=self.api_key,
            host=self.host,
            user_id=auth_status.origin.id,
            is_admin=auth_status.user_is_admin,
            is_device=auth_status.is_device,
        )
        return self._auth_info

    def get_site_name(self):
        """Get site name"""
        config = self.fw.get_config()
        name = config.site.get("name")
        url = config.site.get("api_url", self.fw.api_client.configuration.host)
        hostname = None

        if url:
            try:
                parts = urlparse(url)
                hostname = parts.hostname
            except ValueError:
                pass

        if name:
            if hostname:
                return f"{name} ({hostname})"
            return name
        if hostname:
            return hostname
        return "Unknown Site"

    def is_logged_in(self):
        """Check user is logged in or not"""
        assert self.auth_info

    def call_api(self, resource_path, method, **kwargs):
        """Call api with defaults set to enable accessing the json response"""
        kwargs.setdefault("auth_settings", ["ApiKey"])
        kwargs.setdefault("_return_http_data_only", True)
        kwargs.setdefault("_preload_content", True)
        return self.fw.api_client.call_api(resource_path, method, **kwargs)

    def resolve(self, path, **kwargs):
        """Perform a path based lookup of nodes in the Flywheel hierarchy.
        Overwritten the default resolve as it does not accept kwargs
        """
        if not isinstance(path, list):
            path = path.split("/")

        return self.fw.resolve_path(flywheel.ResolverInput(path=path), **kwargs)

    def get_deid_profile(self, group, project):
        """Fetch the deid profile from the server"""
        resolved_grp = self.safe_lookup([group])
        resolved_prj = self.safe_lookup([group, project])

        def _get_deid_profile(api_url):
            try:
                response = self.call_api(
                    api_url,
                    "GET",
                    response_type=object,
                )
                if (
                    not response
                    or not response.get("deid_profile")
                    or not response.get("deid_profile", {}).get("dicom")
                ):
                    return None
                return response.get("deid_profile")
            except flywheel.rest.ApiException as ex:
                if ex.status not in (403, 404):
                    raise ex

            return None

        if resolved_prj:
            deid_profile = _get_deid_profile(f"/projects/{resolved_prj.id}/settings")
            if deid_profile:
                return deid_profile

        if resolved_grp:
            deid_profile = _get_deid_profile(f"/groups/{resolved_grp.id}/settings")
            if deid_profile:
                return deid_profile

        deid_profile = _get_deid_profile("/site/settings")
        if deid_profile:
            return deid_profile

        return None


@functools.lru_cache()
def get_sdk_client_for_current_user():
    """Cached SDK client for the current session"""
    return get_sdk_client(get_api_key())


def get_authenticated_name(origin_id: str, is_device: Optional[bool] = False) -> str:
    """Get currently authenticated user/device name"""
    fw_client = get_sdk_client_for_current_user()

    if is_device:
        device = fw_client.get_device(origin_id)
        return f'{device.get("type", "device")} - {device.get("name", origin_id)}'

    user = fw_client.get_current_user()
    return f"{user.firstname} {user.lastname}"


class LRUCache:
    """Simple LRU cache"""

    def __init__(self, maxsize=1000):
        self.cache = collections.OrderedDict()
        self.maxsize = maxsize
        self.hits = 0
        self.misses = 0

    def __setitem__(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
        self.cache[key] = value
        if len(self.cache) > self.maxsize:
            self.cache.popitem(last=False)

    def __getitem__(self, key):
        if key in self.cache:
            value = self.cache.pop(key)
            self.hits += 1
            self.cache[key] = value
            return value
        self.misses += 1
        raise KeyError

    def __str__(self):
        return (
            f"LRUCache(hits={self.hits}, misses={self.misses}, "
            f"maxsize={self.maxsize}, currsize={len(self.cache)})"
        )

    def get(self, key, default=None):
        """Get with default"""
        try:
            return self[key]
        except KeyError:
            return default


def get_path_el(c_type, context, use_labels=False):
    """Get the path element for container"""
    if c_type == "group":
        return context.get("_id")
    if use_labels:
        fields = ["label"]
    else:
        fields = ["_id", "label"]
    for field in fields:
        value = context.get(field)
        if not value:
            continue
        if field == "_id":
            return f"<id:{value}>"
        if field == "label":
            return value
    raise TypeError(f"Cannot get {c_type} path element from context {context}")


def create_unique_filename(path: str, path_list: List[str]) -> str:
    """Create unique filename by appending a counter to the end of file name if such file already exists in the given filename set"""
    dirname, full_filename = os.path.split(path)
    parts = full_filename.rsplit(".", 2)
    filename = parts[0]
    extension = ".".join(parts[1:])

    cnt = 1
    while path in path_list:
        path = os.path.join(dirname, f"{filename}_{cnt}.{extension}")
        cnt += 1
    return path


def get_useragent_info() -> str:
    """Get useragent info to pass in the User-Agent header"""
    info = {}
    if len(sys.argv) > 1:
        info["command"] = sys.argv[1]

    # os info Windows, Linux, Darwin
    system = platform.system()
    if not system:  # fallback
        if sys.platform in ("linux", "linux2"):
            system = "Linux"
        elif sys.platform == "darwin":
            system = "Darwin"
        elif sys.platform == "win32":
            system = "Windows"
        else:
            system = "NA"

    if sys.maxsize > 2**32:  # more robust than platform.architecture()
        architecture = "64"
    else:
        architecture = "32"
    machine = platform.machine()  # x86_64
    info["os"] = f"{system}_{machine}_{architecture}"

    return "; ".join(f"{k}:{v}" for k, v in info.items())


def set_sdk_connection_pool_size(client: flywheel.Client, maxsize: int) -> None:
    """Set the maximum number of pooled connections"""
    # Flywheel SDK Internals
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=maxsize, pool_maxsize=maxsize
    )
    client.api_client.rest_client.session.mount("https://", adapter)
