# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import base64
import csv
import tarfile
import zipfile
from collections import OrderedDict
from io import BytesIO

import charset_normalizer
import h5py
import numpy as np
from flask import current_app
from flask import json
from flask import send_file
from PIL import Image

import kadi.lib.constants as const
from .files import open_file
from kadi.lib.web import url_for
from kadi.plugins.core import run_hook


# Prefix of the (OpenXML based) MS office MIME types.
MS_OFFICE_PREFIX = "application/vnd.openxmlformats-officedocument"

# MIME types that currently should not be previewed at all, rather than showing an
# "incorrect" preview (namely, the archive one).
IGNORED_MIMETYPES = [
    f"{MS_OFFICE_PREFIX}.wordprocessingml.document",
    f"{MS_OFFICE_PREFIX}.presentationml.presentation",
]

ARCHIVE_MIMETYPES = [
    "application/gzip",
    "application/x-bzip2",
    "application/x-tar",
    "application/zip",
]
AUDIO_MIMETYPES = [
    "audio/flac",
    "audio/mpeg",
    "audio/ogg",
    "audio/wav",
    "audio/x-wav",
]
IMAGE_MIMETYPES = [
    "image/bmp",
    "image/gif",
    "image/tiff",
    "image/x-bmp",
    "image/x-ms-bmp",
]
STL_MIMETYPES = [
    "application/sla",
    "model/stl",
    "model/x.stl-ascii",
    "model/x.stl-binary",
]

# Maximum amount of entries for archive-like previews.
MAX_ARCHIVE_ENTRIES = 250
# Maximum amount of rows for CSV previews.
MAX_CSV_ROWS = 250
# Maximum amount of chars to read for text-based previews.
MAX_TEXT_CHARS = 100_000
# Maximum width/height for image thumbnails.
MAX_THUMBNAIL_RESOLUTION = 1_024


def get_builtin_preview_data(file):
    """Get the preview data of a file based on all built-in preview types.

    :param file: The :class:`.File` to get the preview data of.
    :return: The preview type and preview data as tuple or `None`` if none of the
        built-in preview types are suitable.
    """
    if file.mimetype in IGNORED_MIMETYPES:
        return None

    # Archive preview, which consists of a hierarchical list of entries and metadata.
    if file.magic_mimetype in ARCHIVE_MIMETYPES:
        archive_data = _get_archive_preview(file)

        if archive_data is not None:
            return "archive", archive_data

    # Audio preview, which just returns the download link of the file.
    if file.magic_mimetype in AUDIO_MIMETYPES:
        return "audio", url_for(
            "api.download_file", record_id=file.record_id, file_id=file.id
        )

    # CSV preview, which consists of tabular text data as well as some additional
    # metadata (encoding and whether a header is detected). Note that all text-based
    # mimetypes are allowed as base.
    if file.magic_mimetype.startswith("text/") and file.mimetype == const.MIMETYPE_CSV:
        text_data = _get_text_data(file)

        if text_data is not None:
            csv_data = _get_csv_preview(text_data["data"], text_data["encoding"])

            if csv_data is not None:
                return "csv", csv_data

    # Excel preview, which just returns the download link of the file.
    if file.magic_mimetype == f"{MS_OFFICE_PREFIX}.spreadsheetml.sheet":
        return "excel", url_for(
            "api.download_file", record_id=file.record_id, file_id=file.id
        )

    # HDF5 preview, which consists of a hierarchical list of entries and metadata.
    if file.magic_mimetype == "application/x-hdf":
        hdf_data = _get_hdf_preview(file)

        if hdf_data is not None:
            return "hdf", hdf_data

    # Image preview for images that can be previewed directly, in which case the direct
    # preview link to the file is returned.
    if file.magic_mimetype in const.IMAGE_MIMETYPES:
        return "image", url_for(
            "api.preview_file", record_id=file.record_id, file_id=file.id
        )

    # Image preview for images that cannot be previewed directly. These images are
    # converted to a base64 encoded PNG thumbnail.
    if file.magic_mimetype in IMAGE_MIMETYPES:
        image_data = _get_image_preview(file)

        if image_data is not None:
            return "image", image_data

    # JSON preview, which directly returns the parsed JSON content of the file. If the
    # file exceeds the configured preview max size, the textual fallback will be used
    # instead to preview only a subset of the JSON data.
    if (
        file.magic_mimetype == const.MIMETYPE_JSON
        and file.size <= current_app.config["PREVIEW_MAX_SIZE"]
    ):
        json_data = _get_json_preview(file)

        if json_data is not None:
            return "json", json_data

    # Markdown preview, which consists of lines of text and the corresponding encoding.
    # Note that all text-based mimetypes are allowed as base.
    if file.magic_mimetype.startswith("text/") and file.mimetype == "text/markdown":
        text_data = _get_text_data(file)

        if text_data is not None:
            return "markdown", _get_text_preview(
                text_data["data"], text_data["encoding"]
            )

    # PDF preview, which just returns the direct preview link of the file.
    if file.magic_mimetype == "application/pdf":
        return "pdf", url_for(
            "api.preview_file", record_id=file.record_id, file_id=file.id
        )

    # STL preview, which just returns the download link of the file.
    if (
        file.magic_mimetype in [const.MIMETYPE_DEFAULT, "text/plain"]
        and file.mimetype in STL_MIMETYPES
    ):
        return "stl", url_for(
            "api.download_file", record_id=file.record_id, file_id=file.id
        )

    # Video preview, which just returns the download link of the file.
    if file.magic_mimetype == "video/mp4":
        return "video", url_for(
            "api.download_file", record_id=file.record_id, file_id=file.id
        )

    # Workflow preview, which just returns the download link of the file.
    if file.magic_mimetype == const.MIMETYPE_FLOW:
        return "workflow", url_for(
            "api.download_file", record_id=file.record_id, file_id=file.id
        )

    return None


def get_preview_data(file, use_fallback=True):
    """Get the preview data of a file.

    Uses the :func:`kadi.plugins.spec.kadi_get_preview_data` plugin hook for custom
    preview data.

    :param file: The :class:`.File` to get the preview data of.
    :param use_fallback: (optional) Flag indicating whether the file should be checked
        for textual data as fallback.
    :return: The preview type and preview data as tuple, which are always guaranteed to
        be JSON serializable. If either the preview type or data could not be
        determined, ``None`` is returned.
    """
    if file.size == 0:
        return None

    try:
        preview_data = run_hook("kadi_get_preview_data", file=file)
    except Exception as e:
        current_app.logger.exception(e)
        return None

    if preview_data is not None:
        if (
            not isinstance(preview_data, tuple)
            or not len(preview_data) == 2
            or None in preview_data
        ):
            current_app.logger.error(f"Invalid preview data format for {file!r}.")
            return None

        try:
            json.dumps(preview_data)
        except Exception as e:
            current_app.logger.exception(e)
            return None

    if preview_data is None and use_fallback:
        text_data = _get_text_data(file)

        if text_data is not None:
            return "text", _get_text_preview(text_data["data"], text_data["encoding"])

    return preview_data


def preview_file(file):
    """Send a file to a client for previewing in a browser.

    Note that this can potentially pose a security risk, so this should only be used for
    files that are safe for displaying. Uses the content-based MIME type of the file to
    set the content type of the response (see :attr:`.File.magic_mimetype`).

    :param file: The :class:`.File` to send to the client.
    :return: The response object.
    """
    storage = file.storage
    filepath = storage.create_filepath(str(file.id))

    # See ".files.download_file" for why we use a file path here and why the conditional
    # flag is set as it is.
    return send_file(
        filepath,
        mimetype=file.magic_mimetype,
        download_name=file.name,
        etag=False,
        conditional=current_app.environment == const.ENV_DEVELOPMENT,
    )


def _archive_entries_to_list(entries):
    results = []

    for name, entry in entries.items():
        item = {"name": name, **entry}

        if entry["is_dir"]:
            item["children"] = _archive_entries_to_list(item["children"])

        results.append(item)

    return sorted(results, key=lambda item: (not item["is_dir"], item["name"]))


def _get_archive_preview(file):
    filepath = file.storage.create_filepath(str(file.id))
    infolist = []

    if file.magic_mimetype == "application/zip":
        try:
            with zipfile.ZipFile(filepath) as zip_file:
                infolist = zip_file.infolist()[:MAX_ARCHIVE_ENTRIES]

        except zipfile.BadZipFile:
            return None
    else:
        try:
            with tarfile.open(filepath) as tar_file:
                num_items = 0

                for item in tar_file:
                    infolist.append(item)
                    num_items += 1

                    if num_items >= MAX_ARCHIVE_ENTRIES:
                        break

        except tarfile.TarError:
            return None

    entries = OrderedDict()

    for item in infolist:
        if isinstance(item, zipfile.ZipInfo):
            is_dir = item.filename.endswith("/")
            size = item.file_size
            parts = item.filename.split("/")

            if not is_dir:
                name = parts[-1]
                parents = parts[:-1]
            else:
                name = parts[-2]
                parents = parts[:-2]

        elif isinstance(item, tarfile.TarInfo):
            is_dir = item.isdir()
            size = item.size
            parts = item.name.split("/")
            name = parts[-1]
            parents = parts[:-1]

        current_dir = entries

        for parent in parents:
            if parent not in current_dir:
                # Depending on how the archive was created, not all directories might be
                # listed separately.
                current_dir[parent] = {"is_dir": True, "children": OrderedDict()}

            current_dir = current_dir[parent]["children"]

        # Depending on how the archive was created, some entries might be listed
        # multiple times.
        if name in current_dir:
            continue

        current_dir[name] = {"is_dir": is_dir}

        if not is_dir:
            current_dir[name]["size"] = size
        else:
            current_dir[name]["children"] = OrderedDict()

    return _archive_entries_to_list(entries)


def _get_file_encoding(file):
    encoding = None

    with open_file(file, mode="rb") as f:
        # Limit the amount of bytes to use for the encoding detection, as it may be
        # quite slow otherwise.
        result = charset_normalizer.detect(f.read(16_384))

        if result["encoding"] is not None:
            # Fall back to UTF-8 if the confidence is not high enough.
            encoding = result["encoding"] if result["confidence"] > 0.5 else "utf-8"

    return encoding


def _get_text_data(file):
    encoding = _get_file_encoding(file)

    if encoding is None:
        return None

    try:
        with open_file(file, mode="r", encoding=encoding) as f:
            return {"data": f.read(MAX_TEXT_CHARS), "encoding": encoding}
    except:
        return None


def _get_csv_preview(data, encoding):
    rows = []
    sniffer = csv.Sniffer()

    try:
        dialect = sniffer.sniff(data)
        has_header = sniffer.has_header(data)

        for row in csv.reader(data.splitlines(), dialect=dialect):
            # Ignore completely empty rows.
            if len(row) > 0:
                rows.append(row)

            if len(rows) >= MAX_CSV_ROWS:
                break
    except:
        return None

    return {"rows": rows, "encoding": encoding, "has_header": has_header}


def _convert_hdf_attr(attr):
    if isinstance(attr, np.ndarray):
        attrs = []

        for _attr in attr:
            attrs.append(_convert_hdf_attr(_attr))

        return attrs

    try:
        attr = attr.item()

        if isinstance(attr, bytes):
            attr = attr.decode()

        return attr
    except:
        return str(attr)


def _get_hdf_entries(h5_file, entry_count=0):
    entry = {
        "name": h5_file.name.split("/")[-1] or "/",
        "is_group": False,
        "attrs": {},
    }

    # Record the total amount of entries, taking into account the recursion.
    entry_count += 1

    for key, value in h5_file.attrs.items():
        entry["attrs"][key] = _convert_hdf_attr(value)

    if isinstance(h5_file, h5py.Group):
        entry["is_group"] = True
        entry["children"] = []

        for value in h5_file.values():
            if entry_count >= MAX_ARCHIVE_ENTRIES:
                break

            new_entry, entry_count = _get_hdf_entries(value, entry_count=entry_count)
            entry["children"].append(new_entry)

    else:
        entry["meta"] = {}

        for attr in ["dtype", "ndim", "shape", "maxshape", "size", "nbytes"]:
            entry["meta"][attr] = str(getattr(h5_file, attr, ""))

    return entry, entry_count


def _get_hdf_preview(file):
    with open_file(file) as f:
        try:
            h5_file = h5py.File(f)
            hdf_data = _get_hdf_entries(h5_file)[0]
            return [hdf_data]
        except:
            return None


def _get_image_preview(file):
    image_data = BytesIO()

    with open_file(file) as f:
        try:
            with Image.open(f) as image:
                # Special handling to support 16 bit TIFF images.
                if image.format == "TIFF" and image.mode == "I;16":
                    image = image.point(lambda i: i * (1 / 256)).convert("L")

                image.thumbnail((MAX_THUMBNAIL_RESOLUTION, MAX_THUMBNAIL_RESOLUTION))
                image.save(image_data, format="PNG")

            image_data = base64.b64encode(image_data.getvalue()).decode()
        except:
            return None

    return f"data:image/png;base64,{image_data}"


def _get_json_preview(file):
    encoding = _get_file_encoding(file)

    if encoding is None:
        return None

    try:
        with open_file(file, mode="r", encoding=encoding) as f:
            return {"json": json.load(f), "encoding": encoding}
    except:
        return None


def _get_text_preview(data, encoding):
    return {"lines": data.rstrip().splitlines(), "encoding": encoding}
