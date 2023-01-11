"""Provides PrepareTask class"""
import logging
import typing as t
from uuid import UUID

import fs

from ... import util
from .. import models as M
from .. import schemas as T
from .abstract import Task

log = logging.getLogger(__name__)


class PrepareTask(Task):
    """
    Pre-processing work like creating containers that not exist in FW
    and create upload tasks
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_containers = self.db.batch_writer_update_container()
        self.update_items = self.db.batch_writer_update_item(
            depends_on=self.update_containers
        )
        self.insert_tasks = self.db.batch_writer_insert_task(
            depends_on=self.update_items
        )
        # cache size == number of container types (group, project, subject, session, acquisiton)
        self.cache = util.LRUCache(5)
        # update containers cache that kept in sync with the batch writer
        self.update_containers_cache = util.LRUCache(self.update_containers.batch_size)
        self.valid_container_paths = set()
        self.valid_item_ids = set()

    def _run(self):
        """Process review, create and enqueue upload tasks"""
        skipped_cnt = 0
        self.report_progress(total=self.db.count_all_container())
        for item in self.db.get_items_with_error_count():
            if item.container_error or self._should_skip_item(item):
                self.update_items.push({"id": item.id, "skipped": True})
                skipped_cnt += 1
                continue
            self.valid_container_paths.add(item.container_path)
            self.valid_item_ids.add(item.id)

        # create new containers
        for container in self.db.get_all_container():
            # check if the container path is in the valid containers
            valid = False
            for path in self.valid_container_paths:
                if f"{path}/".startswith(f"{container.path}/"):
                    valid = True
                    break

            # always create project and group containers
            if (
                not valid
                and container.level.name != "project"
                and container.level.name != "group"
            ):
                # update progress
                self.report_progress(completed=1)
                continue

            # get parents here to keep cache warm
            parents = self._get_parents_dst_context(container)
            if not container.dst_context:
                # if not destination context then we need to create it in flywheel
                self._create_container(container, parents)
                self._add_tags(container)

            # cache the container
            self.cache[container.id] = container

            # update progress
            self.report_progress(completed=1)

        self.report_progress(force=True)

        # make sure that the containers are flushed
        self.update_containers.flush()

        if self.ingest_config.copy_duplicates:
            self.insert_tasks.push(T.TaskIn(type=T.TaskType.prepare_sidecar).dict())
            self.db.set_ingest_status(status=T.IngestStatus.preparing_sidecar)
        else:
            self.db.set_ingest_status(status=T.IngestStatus.uploading)

        upload_task_num = 0
        for item_id in self.valid_item_ids:
            self.insert_tasks.push(
                T.TaskIn(
                    type=T.TaskType.upload,
                    item_id=item_id,
                ).dict()
            )
            upload_task_num += 1

        # this flush implicitly calls update_containers.flush()
        # and update_items.flush() because of dependency
        self.insert_tasks.flush()

        if self.ingest_config.copy_duplicates:
            self.db.update_task_stat(
                T.TaskType.prepare_sidecar.name,
                pending=M.TaskStat.pending + 1,
                total=M.TaskStat.total + 1,
            )
        self.db.update_task_stat(
            T.TaskType.upload.name,
            pending=M.TaskStat.pending + upload_task_num,
            total=M.TaskStat.total + upload_task_num,
        )
        self.db.update_item_stat(upload_skipped=M.ItemStat.upload_skipped + skipped_cnt)

        log.debug(f"Containers cache info: {self.cache}")
        log.debug(f"Update containers cache info: {self.update_containers_cache}")

    def _add_tags(self, container: T.Container) -> None:
        if container.src_context.tags:
            add_tag_fn = getattr(self.fw, f"add_{container.level.name}_tag")
            for tag in container.src_context.tags:
                add_tag_fn(container.dst_context.id, {"value": tag})

    def _create_container(
        self,
        container: T.Container,
        parents: t.Dict[str, t.Tuple[T.DestinationContainerContext, str]],
    ) -> None:
        c_level = container.level.name
        create_fn = getattr(self.fw, f"add_{c_level}")
        payload = container.src_context.dict(
            exclude_none=True, by_alias=True, exclude={"tags"}
        )
        parent_dst_path = ""

        if c_level == "group":
            # set default label for group
            payload.setdefault("label", container.src_context.id)
        else:
            parent_c_level = T.ContainerLevel.get_item(container.level - 1).name
            parent_dst_ctx, parent_dst_path = parents[parent_c_level]

            if c_level == "subject":
                payload.setdefault("code", payload.get("label"))

            if c_level == "session":
                payload["project"] = parents["project"][0].id
                payload["subject"] = {"_id": parent_dst_ctx.id}

            if c_level != "session":
                # set parent ref for all type of container
                # except for session, since it has a special parent ref, see above
                payload[parent_c_level] = parent_dst_ctx.id

        fw_id = create_fn(payload)
        log.debug(f"Created {c_level} container: {payload} as {fw_id}")

        # update container with dst_context and dst_path
        container.dst_context = T.DestinationContainerContext(
            id=fw_id,
            label=payload.get("label"),
            uid=payload.get("uid"),
            info=payload.get("info"),
        )
        container.dst_path = fs.path.combine(
            parent_dst_path,
            util.get_path_el(
                c_level, container.dst_context.dict(by_alias=True), use_labels=True
            ),
        )

        self.update_containers.push(
            {
                "id": container.id,
                "dst_context": container.dst_context.dict(exclude_none=True),
                "dst_path": container.dst_path,
            }
        )
        # put updated item into update containers cache
        self.update_containers_cache[container.id] = container

    def _get_parents_dst_context(
        self, container: T.Container
    ) -> t.Dict[str, t.Tuple[T.DestinationContainerContext, str]]:
        parents = {}
        parent_id = container.parent_id

        while parent_id:
            parent = self._get_prepared_container(parent_id)
            if not (parent.dst_context and parent.dst_path):
                raise ValueError(
                    f"Parent container dst_context or dst_path is not set: {parent.path}"
                )
            parents[parent.level.name] = (parent.dst_context, parent.dst_path)
            parent_id = parent.parent_id

        return parents

    def _should_skip_item(self, item: T.ItemWithErrorCount) -> bool:
        """Determine that item should be skipped or not"""
        if self.ingest_config.skip_existing and item.existing:
            log.debug(f"skip_existing: skipping item {item.id}")
            return True
        if item.error_cnt > 0:
            log.debug(f"error_cnt: skipping item {item.id}")
            return True
        return False

    def _get_prepared_container(self, container_id: UUID) -> T.Container:
        """
        Get container that we already created either from cache or from database if we
        already wrote changes to the db
        """
        container = self.cache.get(container_id)
        if not container:
            # if not in cache try to get from insert cache
            container = self.update_containers_cache.get(container_id)
        if not container:
            # if not in insert cache, it is already written to the db
            # pylint: disable=W0143
            container = self.db.find_one_container(M.Container.id == container_id)
        # update cache, do not update update_containers_cache here
        # because it will get out of sync from the update containers batch writer
        self.cache[container_id] = container
        return container

    def _on_success(self):
        # possible that no upload tasks were created - finalize
        self.db.start_finalizing()

    def _on_error(self):
        self.db.fail()
