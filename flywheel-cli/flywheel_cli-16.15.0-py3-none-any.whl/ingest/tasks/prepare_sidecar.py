"""Provides PrepareSidecarTask class."""
import logging
import tempfile
import time

from ... import util
from .. import models as M
from .. import schemas as T
from .prepare import PrepareTask

log = logging.getLogger(__name__)


class PrepareSidecarTask(PrepareTask):
    """Creating sidecar project and containers if needed"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.insert_containers = self.db.batch_writer_insert_container()
        self.update_items = self.db.batch_writer_update_item(
            depends_on=self.insert_containers
        )
        self.update_containers = self.db.batch_writer_update_container()
        self.insert_tasks = self.db.batch_writer_insert_task(
            depends_on=self.update_containers
        )
        self.cache = util.LRUCache(self.update_containers.batch_size)

        self.container_replace_map = {}
        self.sidecar_project_name = None
        self.original_project = None
        self.original_project_name = None
        self.item_ids = set()

    def _run(self):
        """Create the sidecar container hierarchy"""
        # pylint: disable=C0121
        all_items = self.db.count_all_items(M.Item.skipped == True)
        self.report_progress(total=all_items * 2)
        self._create_sidecar_containers()
        self.update_items.flush()
        # its not needed anymore, free up memory
        del self.container_replace_map

        all_containers = self.db.count_all_containers(
            M.Container.sidecar == True
        )  # pylint: disable=C0121
        self.report_progress(total=all_containers - all_items)
        # create new containers in FW
        for container in self.db.get_all_containers(M.Container.sidecar):
            # get parents here to keep cache warm
            parents = self._get_parents_dst_context(container)
            if not container.dst_context:
                self._create_container(container, parents)
            # cache the container
            self.cache[container.id] = container
            self.report_progress(completed=1)

        upload_task_num = 0
        for item_id in self.item_ids:
            self.insert_tasks.push(
                T.TaskIn(
                    type=T.TaskType.upload,
                    item_id=item_id,
                ).dict()
            )
            upload_task_num += 1

        self.insert_tasks.flush()
        self.db.update_task_stat(
            T.TaskType.prepare_sidecar.name,
            pending=M.TaskStat.pending + upload_task_num,
            total=M.TaskStat.total + upload_task_num,
        )

        self.report_progress(force=True)

        self.db.set_ingest_status(status=T.IngestStatus.uploading)

    def _create_container(self, container, parents):
        """Create the container in FW, and copy the original permissions and rules"""
        super()._create_container(container, parents)
        if container.level.name == "project":
            orig_project_id = self.original_project.dst_context.id
            side_project_id = container.dst_context.id
            orig_project = self.fw.get_project(orig_project_id)
            side_project = self.fw.get_project(side_project_id)
            # permissions
            side_perms = {}
            for permission in side_project.permissions:
                side_perms.setdefault(permission.id, []).append(permission.access)
            for permission in orig_project.permissions:
                if (
                    permission.id not in side_perms
                    or permission.access not in side_perms[permission.id]
                ):
                    self.fw.add_project_permission(side_project_id, permission)

            # gear rules
            rules = self.fw.api_client.call_api(
                f"/projects/{orig_project_id}/rules",
                "GET",
                auth_settings=["ApiKey"],
                response_type=object,
                _return_http_data_only=True,
            )

            existing_rules = self.fw.api_client.call_api(
                f"/projects/{side_project_id}/rules",
                "GET",
                auth_settings=["ApiKey"],
                response_type=object,
                _return_http_data_only=True,
            )
            # delete existing rule from new project(gear rule template) and copy the project's rules
            for rule in existing_rules:
                self.fw.remove_project_rule(side_project_id, rule["_id"])

            for rule in rules:
                for key in ["_id", "created", "modified", "revision"]:
                    rule.pop(key, None)
                rule["project_id"] = side_project_id
                for fixed_input in rule.get("fixed_inputs", []):
                    resp = self.fw.api_client.call_api(
                        f"/containers/{fixed_input['id']}/files/{fixed_input['name']}",
                        "GET",
                        auth_settings=["ApiKey"],
                        _return_http_data_only=True,
                        _preload_content=False,
                    )
                    with tempfile.TemporaryFile() as tmpfile:
                        tmpfile.write(resp.content)
                        tmpfile.seek(0)
                        self.fw.upload(
                            "project",
                            side_project_id,
                            fixed_input["name"],
                            tmpfile,
                        )
                    fixed_input["id"] = side_project_id
                self.fw.add_project_rule(side_project_id, rule)

    def _create_sidecar_containers(self):
        """Create the sidecar container, and update the item to use the new container"""
        # iterate all skipped items that needs to be uploaded to the sidecar project
        for item in self.db.get_sidecar_items_with_container():
            replace_container_id = self._create_sidecar_container_hierarchy(
                item.container_id
            )
            self.item_ids.add(item.id)
            self.update_items.push(
                {"id": item.id, "container_id": replace_container_id}
            )
            self.report_progress(completed=1)

    def _create_sidecar_container_hierarchy(self, orig_project_id):
        """Create the replacement containers"""
        # in most cases it will return the replacement container's id from the container_replace_map
        if orig_project_id in self.container_replace_map:
            return self.container_replace_map[orig_project_id]

        container = self.cache.get(orig_project_id)
        if not container:
            container = self.db.get_container(orig_project_id)
            self.cache[container.id] = container

        if container.level.name == "group":
            # the group container will remain the same, no replacement
            self.container_replace_map[container.id] = container.id
            return container.id

        replace_parent_id = None
        if container.parent_id:
            replace_parent_id = self._create_sidecar_container_hierarchy(
                container.parent_id
            )

        new_container = T.Container(
            path=container.path,
            level=container.level,
            src_context=container.src_context,
            parent_id=replace_parent_id,
            sidecar=True,
        )

        # TODO dst_path?

        # original project name + timestamp
        if container.level.name == "project":
            label = container.src_context.label
            if self.sidecar_project_name is None:
                self.original_project = container
                self.original_project_name = label
                self.sidecar_project_name = f"{label}_{int(time.time())}"
                log.debug(f"Sidecar project name: {self.sidecar_project_name}")

            new_container.src_context.label = self.sidecar_project_name

        new_container.path = container.path.replace(
            self.original_project_name, self.sidecar_project_name, 1
        )

        self.insert_containers.push(new_container.dict())
        self.container_replace_map[orig_project_id] = new_container.id
        return new_container.id
