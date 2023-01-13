"""Provides ResolveTask class."""

import logging
import typing as t
from uuid import UUID

import flywheel
import fs

from ... import errors as global_errors
from ... import util
from .. import errors as ingest_errors
from .. import models as M
from .. import schemas as T
from ..client.db import BatchWriter
from .abstract import Task

log = logging.getLogger(__name__)


class ResolveTask(Task):
    """Resolve containers for review"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visited = set()
        self.insert_containers = ContainerBatchWriter(self.db, "insert", "Container")
        self.update_items = self.db.batch_writer_update_item(
            depends_on=self.insert_containers
        )
        self.update_uids = self.db.batch_writer_update_uid(
            depends_on=self.insert_containers
        )
        self.insert_errors = self.db.batch_writer_insert_error()
        # cache size == number of container types (group, project, subject, session, acquisiton)
        self.cache = util.LRUCache(5)
        self.uid_ids = None
        self.permission_errors = set()
        self.dd_container_paths = []
        self._emptiness_cache = {}

        self.groups_projects = {}
        self.project_path_map = {}

    def _run(self):
        self.report_progress(total=self.db.count_all_item())
        self._get_project_paths()

        for item in self.db.get_all_item():
            container = self._resolve_item_containers(item)
            if not container:
                log.warning(f"Couldn't resolve container for: {item.id}")
                continue

            dst_files = container.dst_context.files if container.dst_context else []
            update = {
                "id": item.id,
                "container_id": container.id,
                "existing": (item.filename in dst_files),
            }
            if update["existing"]:
                update["existing_in"] = container.path
            else:
                for path, files in container.dd_files.items():
                    if item.filename in files:
                        update["existing"] = True
                        update["existing_in"] = path
                        break

            if (
                container.level == T.ContainerLevel.project
                and not self.ingest_config.enable_project_files
            ):
                self.insert_errors.push(
                    T.Error(
                        item_id=item.id, code=ingest_errors.ProjectFileError.code
                    ).dict(exclude_none=True)
                )
                update["skipped"] = True

            self.update_items.push(update)

            # update progress
            self.report_progress(completed=1)

        # flush all remaining items to the db
        self.update_items.flush()
        self.update_uids.flush()
        self.insert_errors.flush()

        if self.permission_errors:
            # TODO: maybe this can be removed once container and item errors are separated?
            # that would allow the user to skip projects with permission error, but
            # import everything else
            for err_msg in self.permission_errors:
                # add error expcept the last one
                self.db.add(
                    T.Error(
                        task_id=self.task.id,
                        code=ingest_errors.NotEnoughPermissions.code,
                        message=err_msg,
                    )
                )
            raise ingest_errors.StopIngestError()

        log.debug(f"Containers cache info: {self.cache}")

        if len(self.groups_projects) > 0 and (
            len(self.groups_projects) > 1
            or len(list(self.groups_projects.values())[0]) > 1
        ):
            self.db.add(
                T.Error(
                    task_id=self.task.id,
                    code=ingest_errors.MultipleGroupOrProjectError.code,
                )
            )
            raise ingest_errors.StopIngestError()

    def _get_project_paths(self):
        for project_id in self.ingest_config.detect_duplicates_project_ids:
            container = self.fw.get_container(project_id)
            self.dd_container_paths.append([container.group, container.label])

    def _resolve_item_containers(self, item: T.Item) -> t.Optional[T.Container]:
        last = None
        path = []
        uid_path = []
        uid_updates = {}
        uid_ids = None

        def add_update(uids, container_type, container_id):
            for uid in uids:
                if not uid in uid_updates:
                    uid_updates[uid] = {"id": uid}
                uid_updates[uid][container_type] = container_id

        for c_level in T.ContainerLevel:
            cont_ctx = getattr(item.context, c_level.name, None)
            if not cont_ctx:
                break

            if cont_ctx.uid:
                uid_path.append(cont_ctx.uid)
            else:
                uid_path.append(
                    util.get_path_el(c_level.name, cont_ctx.dict(by_alias=True))
                )
            path.append(util.get_path_el(c_level.name, cont_ctx.dict(by_alias=True)))
            last = self._resolve_container(c_level, path, uid_path, cont_ctx, last)

            if self.ingest_config.detect_duplicates:
                if not uid_ids:
                    # cache uid ids for the current item, otherwise it would be retrieved
                    # for
                    uid_ids = self._get_uid_ids_for_item(item)
                if last.level == T.ContainerLevel.session:
                    add_update(uid_ids, "session_container_id", last.id)

                if last.level == T.ContainerLevel.acquisition:
                    add_update(uid_ids, "acquisition_container_id", last.id)

        for update in uid_updates.values():
            self.update_uids.push(update)
        return last

    def _resolve_container(
        self,
        c_level: T.ContainerLevel,
        path: t.List[str],
        uid_path: t.List[str],
        context: T.SourceContainerContext,
        parent: t.Optional[T.Container],
    ) -> T.Container:

        if self.ingest_config.strict_uid:
            path_str = fs.path.join(*uid_path)
        else:
            path_str = fs.path.join(*path)

        if path_str in self.visited:
            # already resolved container with this path
            return self._get_visited_container(path_str)

        self._check_container_permission(c_level, path)

        if c_level == T.ContainerLevel.group:
            self.groups_projects.setdefault(context.id, set())
        elif c_level == T.ContainerLevel.project:
            self.groups_projects.setdefault(parent.src_context.id, set())
            self.groups_projects[parent.src_context.id].add(context.label)

        if self.strategy_config.strategy_name == "project" and len(path) > 2:
            # we only have metadata for containers under group/projects/ hence the
            # check above on the path
            fw_metadata_path = "/".join(path[2:])
            fw_md = self.db.find_one_fw_container_metadata(
                M.FWContainerMetadata.path == fw_metadata_path
            )
            for k, v in fw_md.content.items():
                if hasattr(context, k):
                    setattr(context, k, v)

        # create new container node
        child = T.Container(
            path=path_str,
            level=c_level,
            src_context=context,
            parent_id=parent.id if parent else None,
            dd_files=self._get_dd_files(path),
        )

        # we will try to find container in destination FW if:
        # - it has no parent
        # - it has parent and the parent has destination path and its level is
        #   subject/session/acquisiton
        # - it has parent and the parent has destination path and its level is
        #   project/group and that container in the destination is empty.
        if not parent or (
            parent.dst_path
            and (
                parent.level > T.ContainerLevel.project  # like subject, session, acq
                or (parent.dst_context.id and not self._is_empty_dst_container(parent))
            )
        ):
            # try to resolve if parent exists
            resolved = self._find_container_in_fw(path, c_level, context)

            if resolved:
                if c_level == T.ContainerLevel.project:
                    self.project_path_map[context.label] = resolved.id
                child.existing = True
                child.dst_context = resolved
                child.dst_path = util.get_path_el(
                    c_level.name, child.dst_context.dict(by_alias=True), use_labels=True
                )
                if parent and parent.dst_path:
                    child.dst_path = fs.path.join(parent.dst_path, child.dst_path)

        self._check_require_container(child)

        log.debug(f"Resolved {c_level.name} container: {path_str}")
        self.visited.add(path_str)
        self.insert_containers.push_container(path_str, child)

        # store container in cache to make resolving faster
        self.cache[path_str] = child
        return child

    def _is_empty_dst_container(  # pylint: disable=invalid-name
        self, c: T.Container
    ) -> bool:
        """Checks if a container is empty in the destination"""
        if T.ContainerLevel.acquisition == c.level:
            return False

        cont_id = c.dst_context.id
        if self._emptiness_cache.get((cont_id, c.level)):
            return self._emptiness_cache[(cont_id, c.level)]

        level_keys = ["groups", "projects", "subjects", "sessions", "acquisitions"]
        level_key = level_keys[c.level]
        sub_level_key = level_keys[c.level + 1]

        resource_path = f"/{level_key}/{cont_id}/{sub_level_key}?limit=1"
        resp = self.fw.api_client.call_api(
            resource_path,
            "GET",
            auth_settings=["ApiKey"],
            _return_http_data_only=True,
            _preload_content=False,
        )
        resp.raise_for_status()
        result = resp.json()

        self._emptiness_cache[(cont_id, c.level)] = len(result) == 0

        return self._emptiness_cache[(cont_id, c.level)]

    def _check_container_permission(self, c_level, path):
        """
        Verify that the current user has enough permissions to create/upload into the
        given group/project
        """
        if c_level == T.ContainerLevel.group and self.ingest_config.copy_duplicates:
            try:
                self.fw.can_create_project_in_group(path[0])
            except global_errors.NotEnoughPermissions as exc:
                self.permission_errors.add(
                    "User does not have enough permissions to create sidecar project "
                    f"which is required for copy-duplicates. Reason: {exc}"
                )
        if c_level == T.ContainerLevel.project:
            try:
                self.fw.can_import_into(path[0], path[1])
            except global_errors.NotEnoughPermissions as exc:
                # instead of raising for the first error, collect all of them
                # so the user will have a better image about the permission errors
                self.permission_errors.add(str(exc))

    def _check_require_container(self, container):
        """
        If the require_project flag is set (or it is a project migration) and the
        group/project does not exist raise ContainerDoesNotExist exception
        """
        if (
            (
                self.strategy_config.strategy_name == "project"
                or self.ingest_config.require_project
            )
            and not container.existing
            and container.level in [T.ContainerLevel.group, T.ContainerLevel.project]
        ):
            container_label = container.src_context.label or container.src_context.id
            msg = f"{container.level.name} '{container_label}' does not exist"

            reason = ""

            if self.strategy_config.strategy_name == "project":
                reason = "Migration needs group and project created at the destination"
            else:
                reason = "The --require-project flag is set"

            raise ingest_errors.ContainerDoesNotExist(f"{reason} and {msg}")

    def _find_container_in_fw(
        self,
        path: t.List[str],
        c_level: T.ContainerLevel,
        context: T.SourceContainerContext,
    ) -> t.Optional[T.DestinationContainerContext]:
        """Attempt to find the container in FW"""
        try:
            container = None
            if self.ingest_config.strict_uid and c_level in (
                T.ContainerLevel.session,
                T.ContainerLevel.acquisition,
            ):
                if c_level == T.ContainerLevel.session:
                    search_fn = self.fw.get_all_sessions
                else:
                    search_fn = self.fw.get_all_acquisitions

                filter_vals = {
                    "group": path[0],
                    "project": self.project_path_map[path[1]],
                    "uid": context.uid,
                }
                filter_str = ",".join(f"{k}={v}" for k, v in filter_vals.items())
                containers = search_fn(filter=filter_str, sort="created:asc")
                if len(containers) == 0:
                    log.info(
                        f"Could not find any {c_level.name}s with UID {context.uid}"
                    )
                else:
                    if len(containers) > 1:
                        log.warning(
                            f"Multiple ({len(containers)}) {c_level.name}s with UID {context.uid}, using first"
                        )
                    container = containers[0].to_dict()

            if container is None:
                container = self.fw.lookup(path).to_dict()

            files = self._get_files_from_container(container)
            container.pop("files", [])
            log.debug(f"Resolve: {path} - returned: {container['id']}")
            return T.DestinationContainerContext(**container, files=files)
        except flywheel.ApiException:
            log.debug(f"Resolve: {path} - NOT FOUND")
            return None

    @staticmethod
    def _get_files_from_container(container):
        files = container.get("files", [])
        files = list(map(lambda f: f["name"], files))
        return files

    def _get_dd_files(self, path: t.List[str]) -> t.Dict[str, t.List[str]]:
        files = {}
        if len(path) < 2:
            return files
        for prj_path in self.dd_container_paths:
            new_path = prj_path + path[2:]
            try:
                container = self.fw.lookup(new_path).to_dict()
                files["/".join(new_path)] = self._get_files_from_container(container)
                log.debug(f"Resolve DD: {new_path} - returned: {container['id']}")
            except flywheel.ApiException:
                log.debug(f"Resolve DD container: {new_path} - NOT FOUND")
        return files

    def _get_visited_container(self, path: str) -> T.Container:
        """
        Get container that we already resolved either from cache or from database if we
        already wrote changes to the db
        """
        child = self.cache.get(path)
        if not child:
            # if not in cache try to get from insert cache
            child = self.insert_containers.get(path)
        if not child:
            # if not in insert cache, it is already written to the db
            child = self.db.find_one_container(M.Container.path == path)
        self.cache[path] = child
        return child

    def _get_uid_ids_for_item(self, item: T.Item) -> t.Set[UUID]:
        """Get ids of UID rows for the given item"""
        uid_ids: t.Set[UUID] = set()
        for uid in self.db.get_all_uid(M.UID.item_id == item.id):
            uid_ids.add(uid.id)
        return uid_ids

    def _on_success(self):
        if self.ingest_config.detect_duplicates:
            self.db.start_detecting_duplicates()
        else:
            self.db.set_ingest_status(status=T.IngestStatus.in_review)
            if self.ingest_config.assume_yes:
                # ingest was started with assume yes so accept the review
                self.db.review()

    def _on_error(self):
        self.db.fail()


class ContainerBatchWriter(BatchWriter):
    """Batch writer with cache"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = {}

    def get(self, key: str) -> t.Union[None, T.Container]:
        """get item from cachae"""
        return self.cache.get(key)

    def push_container(self, key: str, container: T.Container) -> None:
        """push item"""
        super().push(container.dict())
        self.cache[key] = container

    def flush(self) -> None:
        """flush items"""
        super().flush()
        self.cache = {}
