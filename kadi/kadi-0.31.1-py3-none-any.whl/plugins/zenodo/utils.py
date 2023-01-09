# Copyright 2022 Karlsruhe Institute of Technology
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
import os

from flask_babel import lazy_gettext as _l
from zipstream import ZipStream

from kadi.lib.utils import is_iterable
from kadi.modules.records.export import get_export_data
from kadi.plugins import BooleanField
from kadi.plugins import const
from kadi.plugins import db
from kadi.plugins import JSONField
from kadi.plugins import KadiForm
from kadi.plugins import SelectField


class ExportFilterField(JSONField):
    """Custom field to process and validate export filter data.

    Only performs some basic validation to make sure the overall structure of the filter
    is valid.
    """

    def __init__(self, *args, **kwargs):
        kwargs["default"] = {}
        super().__init__(*args, **kwargs)

    def process_formdata(self, valuelist):
        super().process_formdata(valuelist)

        if valuelist:
            if not isinstance(self.data, dict):
                self.data = self.default
                raise ValueError("Invalid data structure.")


class BaseZenodoForm(KadiForm):
    """Base form class for use in publishing resources via Zenodo."""

    class Meta:
        """Container to store meta class attributes."""

        csrf = False

    export_type = SelectField(
        _l("Include export data"),
        choices=[
            ("", _l("No")),
            ("json", "JSON"),
            ("pdf", "PDF"),
            ("both", _l("Both")),
        ],
        description=_l(
            "Upload exported record data in different formats as additional files,"
            " using the record identifier as base name for each exported file."
        ),
    )

    export_filter = ExportFilterField(_l("Export data to exclude"))


class RecordZenodoForm(BaseZenodoForm):
    """A form for customizing the publishing of records via Zenodo."""

    package_data = BooleanField(
        _l("Package record data"),
        description=_l(
            "Upload all record data in a single ZIP archive rather than individually."
        ),
    )


class CollectionZenodoForm(BaseZenodoForm):
    """A form for customizing the publishing of collections via Zenodo."""

    package_data = BooleanField(
        _l("Package collection data"),
        description=_l(
            "Upload all collection data in a single ZIP archive rather than using an"
            " individual archive for each record."
        ),
    )


class UploadCanceledException(Exception):
    """For exceptions related to canceled uploads."""


class BaseStreamGenerator:
    """Base helper class to handle streamed uploads.

    Offers functionality to register a callback that is periodically invoked each time a
    certain amount of data has been streamed.
    """

    def __init__(self, size, callback, threshold=10 * const.ONE_MB):
        self.size = size
        self.callback = callback
        self.threshold = threshold

        # Current size of the data that was streamed since the last time a check of the
        # task was performed.
        self._current_size = 0
        # Total size of the data that was streamed so far.
        self._total_size = 0

    def _update_size(self, size):
        self._current_size += size
        self._total_size += size

        if self._current_size >= self.threshold:
            self._current_size = 0
            self.callback(self._total_size)

    def __len__(self):
        return self.size


class ZipStreamGenerator(BaseStreamGenerator):
    """Helper class to handle ZIP stream uploads."""

    def __init__(
        self,
        record_or_records,
        export_types,
        export_filter,
        user,
        task,
        update_task=True,
    ):
        self.zip_stream = ZipStream(sized=True)
        self.task = task
        self.update_task = update_task

        # Whether to use record identifiers as folder names inside the ZIP archive,
        # depending on whether a single record or an iterable of records was given.
        use_folders = True

        if not is_iterable(record_or_records):
            use_folders = False
            record_or_records = [record_or_records]

        for record in record_or_records:
            # Add all record files to the ZIP stream.
            for file in record.active_files:
                # Ignore empty files.
                if file.size == 0:
                    continue

                filepath = file.storage.create_filepath(str(file.id))
                arcname = file.name

                if use_folders:
                    arcname = os.path.join(record.identifier, arcname)

                self.zip_stream.add_path(filepath, arcname=arcname)

            # Add all record export data to the ZIP stream.
            for export_type in export_types:
                export_data = get_export_data(
                    record, export_type, export_filter=export_filter, user=user
                )
                arcname = f"{record.identifier}.{export_type}"

                if use_folders:
                    arcname = os.path.join(record.identifier, arcname)

                self.zip_stream.add(export_data, arcname=arcname)

        super().__init__(len(self.zip_stream), self._callback)

    def __iter__(self):
        for chunk in self.zip_stream:
            self._update_size(len(chunk))

            yield chunk

    def _callback(self, current_size):
        if self.task is not None:
            if self.task.is_revoked:
                raise UploadCanceledException

            if self.update_task:
                self.task.update_progress(current_size / len(self) * 100)
                db.session.commit()


class FileStreamGenerator(BaseStreamGenerator):
    """Helper class to handle file stream uploads."""

    def __init__(self, file, size, task):
        self.file = file
        self.task = task

        super().__init__(size, self._callback)

    def __iter__(self):
        while True:
            chunk = self.file.read(8_192)

            if not chunk:
                break

            self._update_size(len(chunk))

            yield chunk

    def _callback(self, current_size):
        if self.task is not None:
            if self.task.is_revoked:
                raise UploadCanceledException
