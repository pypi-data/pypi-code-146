"""Provides FinalizeTask class"""

import logging
import tempfile
from pathlib import Path

from ... import util
from .. import models as M
from .. import schemas as T
from .abstract import Task

log = logging.getLogger(__name__)


class FinalizeTask(Task):
    """Finalize ingest. Currently uploading audit log to target projects."""

    def _run(self):
        """Upload audit log to every project that we identified
        TODO: group logs by project
        """
        if self.ingest_config.no_audit_log:
            log.debug("Audit log turned off, so skip uploading it")
            return

        self.report_progress(total=self.db.count_all_item())

        containers = []
        project_containers = self.db.get_all_container(
            M.Container.level == T.ContainerLevel.project
        )
        for container in project_containers:
            if container.dst_context:
                containers.append(container)

        if containers:
            with tempfile.TemporaryDirectory() as tmp_dir:
                filepath = util.get_filepath(tmp_dir, prefix="audit_log")
                filename = Path(filepath).name

                with open(filepath, "w", encoding="utf-8") as fp:
                    for log_line in self.db.audit_logs:
                        fp.write(log_line)
                        # report progress
                        self.report_progress(completed=1)

                with open(filepath, "rb") as fp:
                    for container in containers:
                        fp.seek(0)
                        self.fw.upload(
                            container.level.name,
                            container.dst_context.id,
                            filename,
                            fp,
                            metadata={
                                "info": self.ingest.dict(
                                    include={
                                        "label",
                                        "config",
                                        "strategy_config",
                                        "created",
                                    }
                                )
                            },
                        )

    def _on_success(self):
        self.db.set_ingest_status(T.IngestStatus.finished)

    def _on_error(self):
        self.db.fail()

    def _on_aborting(self):
        """Called when ingest is in aborting status."""
        self.db.set_ingest_status(T.IngestStatus.aborted)
