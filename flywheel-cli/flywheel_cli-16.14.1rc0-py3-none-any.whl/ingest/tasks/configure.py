"""Provides ConfigureTask class."""

import logging

from ... import errors as global_errors
from ... import util
from .. import errors as ingest_errors
from .. import schemas as T
from .abstract import Task

log = logging.getLogger(__name__)


class ConfigureTask(Task):
    """Make the necessary tasks before scanning begins"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scanner_type = self.task.context["scanner"]["type"]
        self.insert_errors = self.db.batch_writer_insert_error()

    def _run(self):
        """Configure ingest."""
        self.verify_permissions()
        self.resolve_detect_duplicates_projects()
        self.fetch_deid_profile()

        self.insert_errors.flush()

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

    def resolve_detect_duplicates_projects(self):
        """Resolve fw path and save project IDs"""
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

    def fetch_deid_profile(self):
        """Fetch deid profile if it exists in the container"""
        if self.fw.deid_profile:
            grp = getattr(
                self.strategy_config, "group_override", self.strategy_config.group
            )
            prj = getattr(
                self.strategy_config, "project_override", self.strategy_config.project
            )

            if not prj:
                self.db.add(
                    T.Error(
                        task_id=self.task.id,
                        code=ingest_errors.GroupOrProjectNotSetError.code,
                    )
                )
                raise ingest_errors.StopIngestError()

            profile = self.fw.get_deid_profile(grp, prj)
            if profile:
                self._set_deid_profile(profile)
            elif (
                self.strategy_config.strategy_name == "dicom"
                and self.fw.deid_log
                and not self.ingest_config.de_identify
            ):
                self.db.add(
                    T.Error(
                        task_id=self.task.id,
                        code=ingest_errors.DeidConfigConflictError.code,
                    )
                )
                raise ingest_errors.StopIngestError()

    def _on_success(self):
        self.db.start_scanning()

    def _on_error(self):
        self.db.fail()
