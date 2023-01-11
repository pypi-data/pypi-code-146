"""Provides DetectDuplicatesTask class"""

import itertools
import os

from ... import util
from .. import errors
from .. import models as M
from .. import schemas as T
from .abstract import Task

UID_BATCH_SIZE = int(os.environ.get("FW_CLI_UID_BATCH_SIZE", "10000"))


class DetectDuplicatesTask(Task):
    """Detecting duplicated data task"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.insert_errors = self.db.batch_writer_insert_error()
        self.update_containers = self.db.batch_writer_update_container()
        self.update_items = self.db.batch_writer_update_item()
        self.error_item_ids = []
        self.error_container_ids = set()
        self.pid_path_map = {}

        self.checks = {
            self._check_path: {
                errors.DuplicateFilepathInFlywheel.code,
                errors.DuplicateFilepathInUploadSet.code,
            },
            self._check_sop_instance_uid: {errors.DuplicatedSOPInstanceUID.code},
            self._one_session_multi_study_uids: {
                errors.DuplicatedStudyInstanceUID.code
            },
            self._one_study_uid_multi_containers: {
                errors.DuplicatedStudyInstanceUIDInContainers.code
            },
            self._one_acquisition_multi_series_uids: {
                errors.DuplicatedSeriesInstanceUID.code
            },
            self._one_series_uid_multi_containers: {
                errors.DuplicatedSeriesInstanceUIDInContainers.code
            },
            self._check_new_session_container_study_instance_uids: {
                errors.StudyInstanceUIDExists.code
            },
            self._check_new_acquisition_container_study_instance_uids: {
                errors.SeriesInstanceUIDExists.code
            },
        }

    def _run(self):
        self.report_progress(total=self.db.count_all_item())

        overrides = set(self.ingest_config.detect_duplicates_override)
        for dup_check_fn, error_set in self.checks.items():
            allowed_errors = error_set.intersection(overrides)
            if not overrides or allowed_errors:
                if len(error_set) > 1 and overrides:
                    dup_check_fn(allowed_errors)
                else:
                    dup_check_fn()

        # set the error flag for containers and child containers
        # chunking item ids because sqlite limitation
        # SQLITE_MAX_VARIABLE_NUMBER defaults to 999 prior 3.32.0
        # use 900 to be sure since iter_query also adds some other variable
        for chunk in util.chunks(self.error_item_ids, 900):
            for containerid in self.db.find_all_containers_with_item_id(chunk):
                self.error_container_ids.add(containerid.container_id)

        for container in self.db.get_all_container():
            if (
                container.id in self.error_container_ids
                or container.parent_id in self.error_container_ids
            ):
                self.update_containers.push({"id": container.id, "error": True})
                self.error_container_ids.add(container.id)
            # this might be needed only because of the test...might be good in the future
            if container.error:
                self.error_container_ids.add(container.id)

        self.insert_errors.flush()
        self.update_containers.flush()
        self.update_items.flush()

    def _check_path(self, allowed_errors=None):
        """Check items and add duplicated path errors"""
        allowed_errors = allowed_errors or {
            errors.DuplicateFilepathInFlywheel.code,
            errors.DuplicateFilepathInUploadSet.code,
        }
        filenames = set()
        prev_item = None
        prev_item_conflict = False
        for item in self.db.get_items_sorted_by_dst_path():
            # filepath conflicts in Flywheel
            if prev_item and prev_item.container_path != item.container_path:
                filenames = set()

            if (
                item.existing
                and errors.DuplicateFilepathInFlywheel.code in allowed_errors
            ):
                self._add_error(
                    item,
                    errors.DuplicateFilepathInFlywheel,
                    conflict_path=f"fw://{item.existing_in}",
                )

            # filepath conflicts in upload set
            if (
                prev_item
                and prev_item.container_path == item.container_path
                and prev_item.filename == item.filename
            ):
                if errors.DuplicateFilepathInUploadSet.code in allowed_errors:
                    self._add_error(item, errors.DuplicateFilepathInUploadSet)
                safe_filename = util.create_unique_filename(item.filename, filenames)
                filenames.add(safe_filename)

                self.update_items.push({"id": item.id, "safe_filename": safe_filename})

                prev_item_conflict = True
            else:
                if (
                    prev_item_conflict
                    and errors.DuplicateFilepathInUploadSet.code in allowed_errors
                ):
                    # mark prev_item also as duplicate if we found any similar item
                    self._add_error(prev_item, errors.DuplicateFilepathInUploadSet)
                prev_item = item
                prev_item_conflict = False
                filenames.add(item.filename)

            # update progress
            self.report_progress(completed=1)

        # check last prev_item
        # filepath conflict in upload set
        if (
            prev_item_conflict
            and errors.DuplicateFilepathInFlywheel.code in allowed_errors
        ):
            self._add_error(prev_item, errors.DuplicateFilepathInUploadSet)

    def _check_sop_instance_uid(self):
        item_ids = self.db.duplicated_sop_instance_uid_item_ids()
        self.error_item_ids.extend(item_ids)
        self._add_errors(item_ids, errors.DuplicatedSOPInstanceUID)

    def _one_session_multi_study_uids(self):
        item_ids = self.db.one_session_container_multiple_study_instance_uid_item_ids()
        self.error_item_ids.extend(item_ids)
        self._add_errors(item_ids, errors.DuplicatedStudyInstanceUID)

    def _one_study_uid_multi_containers(self):
        item_ids = self.db.one_study_instance_uid_multiple_session_container_item_ids()
        self.error_item_ids.extend(item_ids)
        self._add_errors(item_ids, errors.DuplicatedStudyInstanceUIDInContainers)

    def _one_acquisition_multi_series_uids(self):
        item_ids = (
            self.db.one_acquisition_container_multiple_series_instance_uid_item_ids()
        )
        self.error_item_ids.extend(item_ids)
        self._add_errors(item_ids, errors.DuplicatedSeriesInstanceUID)

    def _one_series_uid_multi_containers(self):
        item_ids = (
            self.db.one_series_instance_uid_multiple_acquisition_container_item_ids()
        )
        self.error_item_ids.extend(item_ids)
        self._add_errors(item_ids, errors.DuplicatedSeriesInstanceUIDInContainers)

    def _check_new_session_container_study_instance_uids(self):
        """Check study instance uids in new session containers"""
        project_ids = self._get_dd_project_ids()
        if not project_ids:
            # only check if at least 1 destination project exists
            return
        uids = self.db.study_instance_uids_in_new_session_container()
        if len(uids) < 1:
            return

        response = self.fw.call_api(
            "/uids/projects",
            "POST",
            body={"sessions": list(uids), "project_ids": project_ids},
            response_type=object,
        )

        uid_path_map = {}
        for container_id, value in response.items():
            fw_path = self._get_pid_fw_path(container_id)
            for uid in value["sessions"]:
                uid_path_map.setdefault(uid, set())
                uid_path_map[uid].add(fw_path)

        item_ids = set()
        for item in self.db.find_all_items_with_uid(
            M.UID.study_instance_uid.in_(uid_path_map.keys())
        ):
            self.error_item_ids.append(item.item_id)
            if not item.item_id in item_ids:
                conflict_paths = ", ".join(uid_path_map[item.study_instance_uid])
                self._add_error(
                    item.item_id, errors.StudyInstanceUIDExists, conflict_paths
                )
                item_ids.add(item.item_id)
                self.error_container_ids.add(item.acquisition_container_id)
                self.error_container_ids.add(item.session_container_id)

    def _get_pid_fw_path(self, pid):
        if pid in self.pid_path_map:
            return self.pid_path_map[pid]

        project = self.fw.call_api(
            f"/projects/{pid}",
            "GET",
            response_type=object,
        )

        path = f"fw://{project['group']}/{project['label']}"
        self.pid_path_map[pid] = path
        return path

    def _check_new_acquisition_container_study_instance_uids(self):
        """Check series instance uids in new acquisition containers"""
        project_ids = self._get_dd_project_ids()
        if not project_ids:
            # only check if at least 1 destination project exists
            return
        item_ids = set()

        uids = self.db.series_instance_uids_in_new_acquisition_container()
        if len(uids) < 1:
            return
        uids_itr = iter(uids)
        while True:
            uids_batch = list(itertools.islice(uids_itr, UID_BATCH_SIZE))
            if not uids_batch:
                break
            response = self.fw.call_api(
                "/uids/projects",
                "POST",
                body={"acquisitions": uids_batch, "project_ids": project_ids},
                response_type=object,
            )

            uid_path_map = {}
            for container_id, value in response.items():
                fw_path = self._get_pid_fw_path(container_id)
                for uid in value["acquisitions"]:
                    uid_path_map.setdefault(uid, set())
                    uid_path_map[uid].add(fw_path)

            for item in self.db.find_all_items_with_uid(
                M.UID.series_instance_uid.in_(uid_path_map.keys())
            ):
                self.error_item_ids.append(item.item_id)
                if item.item_id not in item_ids:
                    conflict_paths = ", ".join(uid_path_map[item.series_instance_uid])
                    self._add_error(
                        item.item_id, errors.SeriesInstanceUIDExists, conflict_paths
                    )
                    item_ids.add(item.item_id)
                    self.error_container_ids.add(item.acquisition_container_id)

    def _get_dd_project_ids(self):
        project_ids = set(self.ingest_config.detect_duplicates_project_ids)
        project_container = self.db.find_one_container(
            M.Container.level == T.ContainerLevel.project
        )
        if project_container.dst_context and project_container.dst_context.id:
            project_ids.add(project_container.dst_context.id)

        return list(project_ids)

    def _add_error(self, item, error_type, conflict_path=None) -> None:
        """Add error for the specified item with the specified error type"""
        item_id = item.id if hasattr(item, "id") else item
        self.insert_errors.push(
            T.Error(
                item_id=item_id, code=error_type.code, conflict_path=conflict_path
            ).dict(exclude_none=True)
        )

    def _add_errors(self, item_ids, error_type):
        for item_id in item_ids:
            self._add_error(item_id, error_type)

    def _on_success(self):
        self.db.set_ingest_status(status=T.IngestStatus.in_review)
        if self.ingest_config.assume_yes:
            # ingest was started with assume yes so accept the review
            self.db.review()

    def _on_error(self):
        self.db.fail()
