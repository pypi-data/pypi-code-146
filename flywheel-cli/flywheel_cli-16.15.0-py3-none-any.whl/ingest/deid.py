"""Provides load_deid_profile function"""

import itertools
import typing

from flywheel_migration import deidentify
from flywheel_migration.deidentify.deid_log import DeIdLog

from . import errors, schemas


def load_deid_profile(profile_name, profiles):
    """Get deid profile"""
    profile_name = profile_name or "minimal"

    if profiles:
        loaded_profiles = []
        for config in profiles:
            profile = deidentify.DeIdProfile()
            profile.load_config(config)
            loaded_profiles.append(profile)
        profiles = loaded_profiles

    default_profiles = deidentify.load_default_profiles()
    for profile in itertools.chain(profiles, default_profiles):
        if profile.name == profile_name:
            profile_errors = profile.validate()
            if profile_errors:
                raise errors.InvalidDeidProfile("Invalid deid profile", profile_errors)
            return profile
    raise errors.InvalidDeidProfile("Unknown deid profile")


class DeidLogger(DeIdLog):  # pylint: disable=too-few-public-methods
    """Replecment of migrations-toolkit default csv logger that can write
    logs into the database.

    See:
    https://gitlab.com/flywheel-io/public/migration-toolkit/-/blob/master/flywheel_migration/deidentify/deid_log.py#L35
    """

    def __init__(self, write_func: typing.Callable):
        self.write_func = write_func
        self.temp_logs = {}

    def write_entry(self, entry, **kwargs):
        """Write log entry.

        Args:
            entry (dict): Log entry

        """
        path = entry.pop("path")
        log_type = entry.pop("type")

        if log_type == "before":
            self.temp_logs[path] = entry
        elif log_type == "after":
            before = self.temp_logs.pop(path)
            after = entry
            deid_log = schemas.DeidLogIn(
                src_path=path,
                tags_before=before,
                tags_after=after,
            )
            self.write_func(deid_log)

    def to_config_str(self):
        return None

    def initialize(self, profile):
        pass

    def close(self):
        pass


class DeidLogPayloadLogger(DeIdLog):
    """Logger for creating payload that is sent to the Deid-Log API.

    See: https://gitlab.com/flywheel-io/tools/app/deid-log#flywheeldeid-log
    """

    indexed_fields = {
        "AccessionNumber",
        "PatientBirthDate",
        "PatientID",
        "PatientName",
        "StudyInstanceUID",
        "StudyID",
        "StudyDate",
        "StudyTime",
        "StudyDateTime",
        "StudyDescription",
        "SeriesInstanceUID",
        "SeriesDate",
        "SeriesTime",
        "SeriesDateTime",
        "SeriesDescription",
        "TimezoneOffsetFromUTC",
    }

    def __init__(self, add_deidentified_tags=False):
        self.logs = {}
        self.add_deidentified_tags = add_deidentified_tags

    def write_entry(
        self, entry, **kwargs
    ):  # pylint: disable=unused-argument,too-many-nested-blocks
        """Write log entry."""
        entry_type = kwargs.get("entry_type")
        if entry_type == "before":
            logged_fields = kwargs.get("logged_fields")
            record = kwargs.get("record")
            path = kwargs.get("path")
            payload = {"indexed_fields": {}, "deidentified_tags": {}}
            for field in self.indexed_fields:
                if record.get(field, None) is not None:
                    payload["indexed_fields"][field] = str(record.get(field))

            if self.add_deidentified_tags:
                for deid_field in logged_fields.values():
                    for field in deid_field.list_fieldname(record):
                        fieldname = str(field)
                        data_elem = None
                        if fieldname not in record:
                            tag = field.dicom_tag
                            if tag and tag in record:
                                data_elem = record[tag]
                        else:
                            data_elem = record[fieldname]

                        if data_elem:
                            tag = (
                                f"{data_elem.tag.group:04x}{data_elem.tag.element:04x}"
                            )
                            payload["deidentified_tags"][tag] = data_elem.to_json_dict(
                                1024, None
                            )
            self.logs[path] = payload

    def to_config_str(self):
        return None

    def initialize(self, profile):
        pass

    def close(self):
        pass
