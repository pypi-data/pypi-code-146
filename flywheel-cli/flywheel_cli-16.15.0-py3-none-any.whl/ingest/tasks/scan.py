"""Provides ScanTask class."""

import logging

from ... import errors as global_errors
from ... import util
from .. import detect_duplicates
from .. import errors as ingest_errors
from .. import models as M
from .. import schemas as T
from ..scanners.factory import create_scanner
from .abstract import Task

log = logging.getLogger(__name__)


class ScanTask(Task):
    """Scan a given path using the given scanner."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scanner_type = self.task.context["scanner"]["type"]
        self.insert_items = self.db.batch_writer_insert_item()
        self.insert_fw_container_metadata = (
            self.db.batch_writer_insert_fw_container_metadata()
        )
        self.insert_tasks = self.db.batch_writer_insert_task(
            depends_on=self.insert_items
        )
        # UID has a foreign key to the item, so we need to flush the items before the uids
        self.insert_uids = self.db.batch_writer_insert_uid(depends_on=self.insert_items)
        self.insert_errors = self.db.batch_writer_insert_error(
            depends_on=self.insert_tasks
        )

    def _run(self):
        """Scan files in a given folder."""
        dirpath = self.task.context["scanner"]["dir"]
        opts = self.task.context["scanner"].get("opts")
        scanner = create_scanner(
            self.scanner_type,
            self.ingest_config,
            self.strategy_config,
            self.worker_config,
            self.walker,
            opts=opts,
            context=self.task.context,
            get_subject_code_fn=self.db.resolve_subject,
            report_progress_fn=self.report_progress,
        )

        bytes_sum = 0
        cnt = 0

        for scan_result in scanner.scan(dirpath):
            if isinstance(scan_result, T.Item):
                self.insert_items.push(scan_result.dict())
                if self.ingest_config.detect_duplicates:
                    self.extract_uids(scan_result)
                bytes_sum += scan_result.bytes_sum
                cnt += 1
                if cnt % 1000 == 0:
                    self.db.update_item_stat(
                        scan_bytes_sum=M.ItemStat.scan_bytes_sum + bytes_sum
                    )
                    bytes_sum = 0

            elif isinstance(scan_result, T.ItemWithUIDs):
                self.insert_items.push(scan_result.item.dict())
                bytes_sum += scan_result.item.bytes_sum
                cnt += 1
                if cnt % 1000 == 0:
                    self.db.update_item_stat(
                        scan_bytes_sum=M.ItemStat.scan_bytes_sum + bytes_sum
                    )
                    bytes_sum = 0
                if self.ingest_config.detect_duplicates:
                    for uid in scan_result.uids:
                        self.insert_uids.push(uid.dict(exclude_none=True))
                    detect_duplicates.detect_uid_conflicts_in_item(
                        scan_result.item,
                        scan_result.uids,
                        self.insert_errors,
                        self.ingest_config.detect_duplicates_override,
                    )
            elif isinstance(scan_result, T.FWContainerMetadata):
                self.insert_fw_container_metadata.push(scan_result.dict())

            elif isinstance(scan_result, T.TaskIn):
                self.insert_tasks.push(scan_result.dict())
                self.db.update_task_stat(
                    scan_result.type.name,
                    pending=M.TaskStat.pending + 1,
                    total=M.TaskStat.total + 1,
                )
            elif isinstance(scan_result, T.Error):
                scan_result.task_id = self.task.id
                self.insert_errors.push(scan_result.dict())
            else:
                raise ValueError(f"Unexpected type: {type(scan_result)}")

        self.insert_items.flush()
        self.insert_fw_container_metadata.flush()
        self.insert_tasks.flush()
        self.insert_errors.flush()
        self.insert_uids.flush()
        self.db.update_item_stat(scan_bytes_sum=M.ItemStat.scan_bytes_sum + bytes_sum)
        self.db.update_item_stat(scan_total=M.ItemStat.scan_total + cnt)

    def extract_uids(self, item: T.Item) -> None:
        """Create new task for extracting UIDs. In case of DICOM scanner it's already extracted"""
        task = T.TaskIn(type="extract_uid", item_id=item.id)
        self.insert_tasks.push(task.dict())

    def verify_permissions(self):
        """
        Verify that user has enough permission to perform the ingest
        according to the initial context
        """
        # template scanner is the root scanner for all the ingest
        # so do permcheck only in case of that scanner
        if self.scanner_type != "template":
            return

        grp = getattr(
            self.strategy_config, "group_override", self.strategy_config.group
        )
        prj = getattr(
            self.strategy_config, "project_override", self.strategy_config.project
        )
        try:
            self.fw.can_import_into(grp, prj)
        except global_errors.NotEnoughPermissions as exc:
            # translate the error into an ingest error that has error code
            raise ingest_errors.NotEnoughPermissions(str(exc))

        if self.ingest_config.copy_duplicates:
            try:
                self.fw.can_create_project_in_group(grp)
            except global_errors.NotEnoughPermissions as exc:
                raise ingest_errors.NotEnoughPermissions(
                    "User does not have enough permissions to create sidecar project "
                    f"which is required for copy-duplicates. Reason: {exc}"
                )

        if self.ingest_config.detect_duplicates_project:
            ids = set()
            required_actions = {"containers_view_metadata"}
            for path in set(self.ingest_config.detect_duplicates_project):
                try:
                    project = self.fw.safe_lookup(util.parse_resolver_path(path))
                    if not project or project.container_type != "project":
                        self.insert_errors.push(
                            T.Error(
                                code=ingest_errors.ProjectDoesNotExistError.code,
                                message=f"Skipping {path} because it's not a valid container path",
                                task_id=self.task.id,
                            ).dict(exclude_none=True)
                        )
                        continue
                    having_actions = self.fw.get_user_actions(project)
                    if not self.fw.auth_info.is_admin:
                        if not required_actions.issubset(having_actions):
                            req_str = ", ".join(sorted(required_actions))
                            missing_str = ", ".join(
                                sorted(required_actions - having_actions)
                            )
                            msg = (
                                f"User does not have the required permissions ({req_str}) "
                                f"in '{path}'. "
                                f"Missing permissions: {missing_str}"
                            )
                            raise global_errors.NotEnoughPermissions(msg)

                    ids.add(project.id)
                except global_errors.NotEnoughPermissions as exc:
                    raise ingest_errors.NotEnoughPermissions(str(exc))

            self.ingest_config.detect_duplicates_project_ids = ids
            self.db.update_ingest_config(self.ingest_config)

    def _on_success(self):
        # Ingest will stay in scanning if there is extract_meta tasks
        self.db.start_resolving()

    def _on_error(self):
        self.db.fail()
