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
import glob
import os
import re
import shutil
import sys

import click
from flask import current_app

import kadi.lib.constants as const
from kadi.cli.main import kadi
from kadi.cli.utils import check_env
from kadi.cli.utils import echo
from kadi.cli.utils import echo_danger
from kadi.cli.utils import echo_success
from kadi.cli.utils import echo_warning
from kadi.ext.db import db
from kadi.lib.exceptions import KadiChecksumMismatchError
from kadi.lib.exceptions import KadiFilesizeMismatchError
from kadi.lib.storage.core import get_storage
from kadi.lib.storage.local import create_default_local_storage
from kadi.lib.tasks.models import Task
from kadi.lib.tasks.models import TaskState
from kadi.modules.records.files import remove_file
from kadi.modules.records.files import remove_temporary_file
from kadi.modules.records.models import Chunk
from kadi.modules.records.models import File
from kadi.modules.records.models import FileState
from kadi.modules.records.models import TemporaryFile
from kadi.modules.records.models import TemporaryFileState
from kadi.modules.records.models import Upload
from kadi.modules.records.models import UploadState
from kadi.modules.records.uploads import remove_upload


@kadi.group()
def files():
    """Utility commands for file management."""


def _remove_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


@files.command()
@click.option("--i-am-sure", is_flag=True)
@check_env
def clean(i_am_sure):
    """Remove all files in the configured local storage paths.

    Aside from the files stored in the configured local storage path (STORAGE_PATH),
    this command will also delete all general user uploads (MISC_UPLOADS_PATH).

    Should preferably only be run while the application and Celery are not running.
    """
    storage_path = current_app.config["STORAGE_PATH"]
    misc_uploads_path = current_app.config["MISC_UPLOADS_PATH"]

    if not i_am_sure:
        echo_warning(
            f"This will remove all data in '{storage_path}' and '{misc_uploads_path}'."
            " If you are sure you want to do this, use the flag --i-am-sure."
        )
        sys.exit(1)

    for item in os.listdir(storage_path):
        _remove_path(os.path.join(storage_path, item))

    for item in os.listdir(misc_uploads_path):
        _remove_path(os.path.join(misc_uploads_path, item))

    echo_success("Storage cleaned successfully.")


@files.command()
@click.option(
    "-c",
    "--checksums",
    "validate_checksums",
    is_flag=True,
    help="Validate the checksum of each active file instead of just its size.",
)
@click.option(
    "-s",
    "--storage",
    "check_storage",
    is_flag=True,
    help="Also check the configured local storage path (STORAGE_PATH) for"
    " inconsistencies.",
)
def check(validate_checksums, check_storage):
    """Check all files stored in the database for inconsistencies.

    Should preferably be run while the application and Celery are not running.
    """
    num_inconsistencies = 0
    inconsistent_items = []

    # Check files in the database.
    files_query = File.query.with_entities(
        File.id, File.size, File.checksum, File.storage_type, File.state
    )
    echo(f"Checking {files_query.count()} files in database...")

    for file in files_query.order_by(File.last_modified.desc()):
        storage = get_storage(file.storage_type)
        filepath = storage.create_filepath(str(file.id))

        # If an active file exists in storage, we validate its integrity by either
        # verifying its checksum or size, otherwise there is an inconsistency.
        if file.state == FileState.ACTIVE:
            if storage.exists(filepath):
                try:
                    if validate_checksums:
                        storage.validate_checksum(filepath, file.checksum)
                    else:
                        storage.validate_size(filepath, file.size)

                except (KadiChecksumMismatchError, KadiFilesizeMismatchError):
                    num_inconsistencies += 1
                    inconsistent_items.append(File.query.get(file.id))

                    echo_danger(
                        f"[{num_inconsistencies}] Mismatched"
                        f" {'checksum' if validate_checksums else 'size'} for active"
                        f" file object in database with ID '{file.id}' and data at"
                        f" '{filepath}'."
                    )
            else:
                num_inconsistencies += 1
                inconsistent_items.append(File.query.get(file.id))

                echo_danger(
                    f"[{num_inconsistencies}] Found orphaned active file object in"
                    f" database with ID '{file.id}'."
                )

        # Inactive files will be handled by the periodic cleanup task eventually.
        elif file.state == FileState.INACTIVE:
            pass

        # Deleted file objects should not have any data associated with them anymore.
        elif file.state == FileState.DELETED and storage.exists(filepath):
            num_inconsistencies += 1
            inconsistent_items.append(File.query.get(file.id))

            echo_danger(
                f"[{num_inconsistencies}] Found deleted file object in database with ID"
                f" '{file.id}' and data at '{filepath}'."
            )

    # Check uploads in the database.
    uploads_query = Upload.query.with_entities(Upload.id, Upload.state)
    echo(f"Checking {uploads_query.count()} uploads in database...")

    for upload in uploads_query.order_by(Upload.last_modified.desc()):
        # Active uploads will either be handled once they are finished or by the
        # periodic cleanup task eventually.
        if upload.state == UploadState.ACTIVE:
            pass

        # Inactive uploads will be handled by the periodic cleanup task eventually.
        elif upload.state == UploadState.INACTIVE:
            pass

        # If an upload is still processing (which is only relevant for chunked uploads),
        # check if the corresponding task is still pending. If so, it is up to the task
        # to decide if the processing should complete or not, otherwise the task may
        # have been canceled forcefully.
        elif upload.state == UploadState.PROCESSING:
            task = Task.query.filter(
                Task.name == const.TASK_MERGE_CHUNKS,
                Task.arguments["args"][0].astext == str(upload.id),
            ).first()

            if task is None or task.state != TaskState.PENDING:
                num_inconsistencies += 1
                inconsistent_items.append(Upload.query.get(upload.id))

                if task is not None:
                    inconsistent_items.append(task)

                echo_danger(
                    f"[{num_inconsistencies}] Found processing upload object in"
                    f" database with ID '{upload.id}' and non-pending task with ID"
                    f" '{task.id}'."
                )

    # Check temporary files in the database.
    temporary_files_query = TemporaryFile.query.with_entities(
        TemporaryFile.id, TemporaryFile.state
    )
    echo(f"Checking {temporary_files_query.count()} temporary files in database...")

    for temporary_file in temporary_files_query.order_by(
        TemporaryFile.last_modified.desc()
    ):
        storage = create_default_local_storage()
        filepath = storage.create_filepath(str(temporary_file.id))

        # Check if an active temporary file at least exists in storage.
        if temporary_file.state == TemporaryFileState.ACTIVE and not storage.exists(
            filepath
        ):
            num_inconsistencies += 1
            inconsistent_items.append(TemporaryFile.query.get(temporary_file.id))

            echo_danger(
                f"[{num_inconsistencies}] Found orphaned active temporary file object"
                f" in database with ID '{temporary_file.id}'."
            )

        # Inactive temporary files will be handled by the periodic cleanup task
        # eventually.
        elif temporary_file.state == TemporaryFileState.INACTIVE:
            pass

    # Check the configured local storage path, if applicable.
    if check_storage:
        storage_path = current_app.config["STORAGE_PATH"]
        filename_re = re.compile(
            "^([0-9a-f]{{2}}{sep}[0-9a-f]{{2}}{sep}[0-9a-f]{{2}}{sep}[0-9a-f]{{2}}"
            "-[0-9a-f]{{4}}-[0-9a-f]{{4}}-[0-9a-f]{{4}}-[0-9a-f]{{12}})"
            "(-[0-9]+)?$".format(sep=os.sep)
        )

        echo(f"Checking file storage at '{storage_path}'...")

        for path in glob.iglob(os.path.join(storage_path, "**", "*"), recursive=True):
            if os.path.isfile(path):
                filename = os.path.relpath(path, storage_path)
                match = filename_re.match(filename)

                # This should normally not happen, but we check for it just in case.
                if match is None:
                    echo_warning(f"Found unexpected data at '{path}'.")
                    continue

                object_id = match.group(1).replace(os.sep, "")

                # Matched a potential file, upload or temporary file.
                if match.group(2) is None:
                    file_exists = (
                        File.query.filter(File.id == object_id)
                        .with_entities(File.id)
                        .first()
                        is not None
                    )
                    upload_exists = (
                        Upload.query.filter(Upload.id == object_id)
                        .with_entities(Upload.id)
                        .first()
                        is not None
                    )
                    temporary_file_exists = (
                        TemporaryFile.query.filter(TemporaryFile.id == object_id)
                        .with_entities(TemporaryFile.id)
                        .first()
                        is not None
                    )

                    if (
                        not file_exists
                        and not upload_exists
                        and not temporary_file_exists
                    ):
                        num_inconsistencies += 1
                        inconsistent_items.append(path)

                        echo_danger(
                            f"[{num_inconsistencies}] Found orphaned file data at"
                            f" '{path}'."
                        )

                # Matched a potential chunk.
                else:
                    chunk_index = match.group(2)[1:]
                    chunk_exists = False

                    upload = (
                        Upload.query.filter(Upload.id == object_id)
                        .with_entities(Upload.id)
                        .first()
                    )

                    if upload is not None:
                        chunk_exists = (
                            Chunk.query.filter(
                                Chunk.upload_id == upload.id, Chunk.index == chunk_index
                            )
                            .with_entities(Chunk.id)
                            .first()
                            is not None
                        )

                    if not chunk_exists:
                        num_inconsistencies += 1
                        inconsistent_items.append(path)

                        echo_danger(
                            f"[{num_inconsistencies}] Found orphaned chunk data at"
                            f" '{path}'."
                        )

    if num_inconsistencies == 0:
        echo_success("Files checked successfully.")
    else:
        echo_warning(
            f"Found {num_inconsistencies}"
            f" {'inconsistency' if num_inconsistencies == 1 else 'inconsistencies'}."
        )

        if click.confirm(
            "Do you want to resolve all inconsistencies automatically by deleting all"
            " inconsistent database objects and/or files?"
        ):
            for item in inconsistent_items:
                if isinstance(item, File):
                    remove_file(item)

                elif isinstance(item, Upload):
                    remove_upload(item)

                elif isinstance(item, TemporaryFile):
                    remove_temporary_file(item)

                elif isinstance(item, Task):
                    # Cancel all file upload related tasks that may be in an
                    # inconsistent state as well.
                    item.revoke()
                    db.session.commit()

                elif isinstance(item, str):
                    # Note that this might potentially leave some empty directories
                    # behind.
                    os.remove(item)

            echo_success("Inconsistencies resolved successfully.")
