"""Module for sync source"""
import io
import json
import logging
import multiprocessing
import os
import re
import tempfile
import threading
import time
import urllib.parse
import zipfile

import dateutil
import flywheel
import requests

from .os_dst import OSDestination

QUEUE_EMPTY = object()
log = logging.getLogger(__name__)


class FWThreadedSource:
    """Generator yielding `read()`-able download targets for a ticket"""

    # pylint: disable=too-few-public-methods, too-many-arguments
    def __init__(
        self,
        client,
        project_id,
        include=None,
        exclude=None,
        include_container_tags=None,
        exclude_container_tags=None,
        include_mlset=None,
        exclude_mlset=None,
        analyses=False,
        metadata=False,
        full_project=False,
        strip_root=False,
        unpack_dir=None,
        export_templates=None,
    ):
        self.client = client
        self.strip_root = strip_root
        self.unpack_dir = unpack_dir

        payload = {"nodes": [{"level": "project", "_id": project_id}]}

        filters = []
        if include:
            filters.append({"types": {"+": include}})
        if exclude:
            filters.append({"types": {"-": exclude}})
        if filters:
            payload["filters"] = filters

        container_tag_filters = []
        for container_type, tags in (include_container_tags or {}).items():
            container_tag_filters.append(
                {"tags": {"plus": tags}, "type": container_type}
            )
        for container_type, tags in (exclude_container_tags or {}).items():
            container_tag_filters.append(
                {"tags": {"minus": tags}, "type": container_type}
            )
        if container_tag_filters:
            payload["container_filters"] = container_tag_filters

        mlset_filters = None
        if include_mlset:
            mlset_filters = {"plus": include_mlset}
        if exclude_mlset:
            mlset_filters = {"minus": exclude_mlset}
        if mlset_filters:
            payload["mlset_filters"] = mlset_filters

        if export_templates:
            payload["export_templates"] = export_templates

        params = {"type": "full", "prefix": ""}
        if analyses or full_project:
            params["analyses"] = True
        if metadata or full_project:
            params["metadata"] = True

        self.payload = payload
        self.params = params

    def __iter__(self):
        response = get_download_targets_response(self.client, self.payload, self.params)
        cnt = 0
        for item in response.iter_lines():
            # remove leading/trailing whitespace
            item = item.strip()
            if item:
                cnt += 1
                target = json.loads(item)
                fwfile = FWFile(
                    self.client,
                    target,
                    strip_root=self.strip_root,
                    unpack_dir=self.unpack_dir,
                )
                log.debug(f"#{cnt} FWFile {fwfile.name}")

                yield fwfile


class FWFile:
    """Enable `read()`-ing download targets"""

    __slots__ = (
        "name",
        "size",
        "modified",
        "client",
        "container_id",
        "filename",
        "file",
        "bytes_read",
        "is_packed",
        "unpack_dir",
        "unpack_lock",
        "unpacked",
        "_members",
        "_tempdir",
        "_zipdir",
        "is_metadata",
    )

    def __init__(self, client, target, strip_root=False, unpack_dir=None):
        strip = r"^/?[^/]+/" if strip_root else r"^/"
        self.name = re.sub(strip, "", target["dst_path"])
        self.size = target["size"]
        self.modified = dateutil.parser.parse(target["modified"]).timestamp()

        self.client = client
        self.container_id = target["container_id"]
        self.filename = target["filename"]
        self.file = None
        self.bytes_read = 0
        self.is_packed = (
            target["filetype"] == "dicom"
            and target["filename"].lower().endswith(".zip")
            and target["download_type"] != "metadata_sidecar"
        )
        self.is_metadata = False

        if target["download_type"] == "metadata_sidecar":
            self.is_metadata = True
            meta = json.dumps(target["metadata"]).encode("utf8")
            self.size = len(meta)
            self.file = io.BytesIO(meta)

        if self.is_packed:
            self.unpack_dir = unpack_dir
            self.unpack_lock = threading.Lock()
            self.unpacked = False
            self._members = None
            self._tempdir = None
            self._zipdir = None

        self._members = None

    def __repr__(self):
        ret = "FWFile("
        for slot in self.__slots__:
            if hasattr(self, slot):
                ret += f"{slot}={getattr(self, slot)}, "

        ret = ret[:-2]
        ret += ")"
        return ret

    def read(self, size=-1):
        """Read `size` bytes from the download target GET response"""
        self._download_file()
        data = self.file.read(size)
        if not data:
            self.file.close()
        self.bytes_read += len(data)
        return data

    def _download_file(self):
        if self.file is None:
            response = get_container_file_response(
                self.client, self.container_id, self.filename
            )
            self.file = response.raw

    @property
    def members(self):
        """Return list of DICOM zip members"""
        if self._members is None:
            info = self.client.get_container_file_zip_info(
                self.container_id, self.filename
            )
            self._members = [
                FWMember(self, member) for member in info.members if member.size
            ]
        return self._members

    def get_members(self, use_local=False):
        """Return list of DICOM zip members with the option of using the downloaded file"""
        if self._members is None:
            if use_local:
                self._members = []
                self._download_file()

                tmp_dir = self.tempdir
                for file_name in list_all_files(tmp_dir):
                    full_path = os.path.join(tmp_dir, file_name)
                    if os.path.isfile(full_path):
                        info = AttrDict(
                            {"size": os.stat(full_path).st_size, "path": file_name}
                        )
                        self._members.append(FWMember(self, info))
            else:
                return self.members

        return self._members

    @property
    def tempdir(self):
        """Return path to the downloaded and extracted DICOM zip"""
        with self.unpack_lock:
            if not self.unpacked:
                # pylint: disable=consider-using-with
                self._zipdir = tempfile.TemporaryDirectory(dir=self.unpack_dir)
                self._tempdir = tempfile.TemporaryDirectory(dir=self.unpack_dir)
                filename = os.path.basename(self.name)
                temp = OSDestination(self._zipdir).file(filename)
                temp.store(self)
                done_ev = multiprocessing.Event()
                proc = multiprocessing.Process(
                    target=_extract_all,
                    args=(temp.filepath, self._tempdir.name, done_ev),
                )
                proc.start()
                # the process sometimes hangs indefinitely and never joins (but reaching the end of the code)
                # hence the Event, and the proc.kill() at the end
                # the other method would be to use "spawn" for start_method
                while not done_ev.is_set():
                    time.sleep(1)
                proc.join(3)
                proc.kill()
                temp.delete()  # slices extracted - remove .zip
                self.unpacked = True
        return self._tempdir.name

    def cleanup(self):
        """Remove the temporary directory of extracted DICOM zip members"""
        if self.is_packed and self.unpacked:
            self._tempdir.cleanup()
            self._zipdir.cleanup()


class FWMember:
    """Enable `read()`-ing (DICOM) zip members from a locally unpacked FWFile"""

    # pylint: disable=too-few-public-methods
    __slots__ = ("name", "size", "modified", "packfile", "path", "file", "bytes_read")

    def __init__(self, packfile, member):
        # NOTE using member basenames instead of full paths (assumes unique names within zip)
        dirname = re.sub(
            r"(\.(dcm|dicom))?\.zip$", "/", packfile.name, flags=re.IGNORECASE
        )
        self.name = dirname + os.path.basename(member.path)
        self.size = member.size
        self.modified = packfile.modified

        self.packfile = packfile
        self.path = member.path
        self.file = None
        self.bytes_read = 0

    def read(self, size=-1):
        """Read `size` bytes from the locally unpacked DICOM zip member"""
        if self.file is None:
            filepath = f"{self.packfile.tempdir}/{self.path}"
            self.file = open(filepath, mode="rb")  # pylint: disable=consider-using-with
        data = self.file.read(size)
        self.bytes_read += len(data)
        if not data:
            self.file.close()
        return data

    def cleanup(self):
        """Remove the locally unpacked DICOM slice"""
        if self.packfile.unpacked:
            os.remove(f"{self.packfile.tempdir}/{self.path}")


def retry(func):
    """Decorator for retrying temporary HTTP errors with exponential backoff"""

    def wrapped(*args, **kwargs):
        # pylint: disable=broad-except, no-member
        attempt = 0
        retries = 5
        while True:
            attempt += 1
            retriable = False
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                if isinstance(exc, requests.ConnectionError):
                    # NOTE low-level network issues
                    retriable = True
                if isinstance(exc, requests.HTTPError):
                    # NOTE 429 for (future) google storage rate-limit error support
                    retriable = 500 <= exc.status_code < 600 or exc.status_code == 429
                if isinstance(exc, flywheel.ApiException):
                    # TODO retry functionality in SDK instead
                    retriable = 500 <= exc.status < 600
                if attempt > retries or not retriable:
                    raise
                time.sleep(2**attempt)

    return wrapped


@retry
def get_download_targets_response(client, payload, params):
    """Get download target response"""
    response = client.api_client.call_api(
        "/download/targets",
        "POST",
        auth_settings=["ApiKey"],
        query_params=list(params.items()),
        body=payload,
        _return_http_data_only=True,
        _preload_content=False,
    )
    response.raise_for_status()
    return response


@retry
def get_container_file_response(client, container_id, filename):
    """Get container file response"""
    filename = urllib.parse.quote(filename, safe="")
    response = client.api_client.call_api(
        f"/containers/{container_id}/files/{filename}",
        "GET",
        auth_settings=["ApiKey"],
        _return_http_data_only=True,
        _preload_content=False,
    )
    response.raise_for_status()
    return response


@retry
def get_container_file_zip_info(client, container_id, filename):
    """Get container file zip info"""
    return client.get_container_file_zip_info(container_id, filename)


class AttrDict(dict):
    """Simple attrdict"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


def list_all_files(dir_path):
    """List all files in dir and subdirs"""
    list_of_files = os.listdir(dir_path)
    all_files = []
    for entry in list_of_files:
        full_path = os.path.join(dir_path, entry)
        if os.path.isdir(full_path):
            sub_files = list_all_files(full_path)
            all_files = all_files + [os.path.join(entry, f) for f in sub_files]
        else:
            all_files.append(entry)

    return all_files


def _extract_all(src_path, dst_path, done_ev):
    with zipfile.ZipFile(src_path) as zf:
        zf.extractall(dst_path)
    done_ev.set()
