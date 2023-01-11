"""Provides TemplateScanner class"""

import copy
import logging
import re
from collections import deque

import fs
from pydantic import ValidationError

from ... import util
from ...walker.fw_walker import FWFileInfo, FWMetaFileInfo
from .. import errors
from .. import schemas as s
from ..strategies.factory import create_strategy
from ..template import TERMINAL_NODE
from .abstract import AbstractScanner

log = logging.getLogger(__name__)

_FW_CONTAINER_PATH_PATTERN = re.compile(
    r"SUBJECTS/|SESSIONS/|ACQUISITIONS/|\.flywheel\.json"
)


class TemplateScanner(AbstractScanner):
    """Template scanner"""

    def _scan(self, subdir):
        import_strategy = create_strategy(self.strategy_config)
        import_strategy.initialize()
        initial_context = import_strategy.initial_context()
        root_node = import_strategy.root_node

        if root_node.node_type == "scanner":
            yield from self.create_task_or_item(subdir, root_node, initial_context, {})
            # stop when the root node is a scanner, like in case of dicom strategy
            return

        if self.strategy_config.strategy_name == "project":
            yield from self._scan_for_project_strategy(
                subdir, initial_context, root_node
            )
        else:
            yield from self._regular_scan(subdir, initial_context, root_node)

    def _regular_scan(self, subdir, initial_context, root_node):
        """
        It goes through the files and creates Items that will only be yielded if a whole
        directory is done or at the and of the function.
        """
        prev_dir = None
        prev_node = root_node
        prev_context = copy.deepcopy(initial_context)
        files = {}

        # TODO: determine according to the hierarcy how walk the input folder
        for fileinfo in self.iter_files(subdir):
            context = copy.deepcopy(initial_context)
            path_parts = deque(fileinfo.name.split("/"))
            node = root_node
            parent_dirpath = "/"
            while len(path_parts) > 1:
                dirname = path_parts.popleft()
                parent_dirpath = fs.path.combine(parent_dirpath, dirname)
                node = node.extract_metadata(
                    dirname, context, self.walker, path=parent_dirpath
                )
                if node in (None, TERMINAL_NODE):
                    break

            if prev_dir and prev_dir != parent_dirpath:
                yield from self.create_task_or_item(
                    prev_dir, prev_node, prev_context, files
                )
                files = {}

            rel_filepath = fs.path.join(*path_parts)
            files[rel_filepath] = fileinfo
            prev_dir = parent_dirpath
            prev_node = node
            prev_context = context

        yield from self.create_task_or_item(prev_dir, prev_node, prev_context, files)

    def create_task_or_item(
        self, dirpath, node, context, files
    ):  # pylint: disable=too-many-branches
        """Create ingest item or scan task according to the node type"""
        if context.get("ignore"):
            return

        # Merge subject and session if one of them is missing
        if getattr(self.strategy_config, "no_subjects", False) or getattr(
            self.strategy_config, "no_sessions", False
        ):
            self.context_merge_subject_and_session(context)

        if getattr(self.strategy_config, "group_override", False):
            util.set_nested_attr(
                context, "group._id", self.strategy_config.group_override
            )

        if getattr(self.strategy_config, "project_override", False):
            util.set_nested_attr(
                context, "project.label", self.strategy_config.project_override
            )

        if node not in (None, TERMINAL_NODE) and node.node_type == "scanner":
            scan_context = copy.deepcopy(context)
            scan_context["scanner"] = {
                "type": node.scanner_type,
                "dir": dirpath,
                "opts": node.opts,
            }
            yield s.TaskIn(
                type=s.TaskType.scan,
                context=scan_context,
            )
            return

        try:
            # parse and validate item context
            item_context = s.ItemContext(**context)
        except ValidationError as exc:
            msg = f"Context is invalid for file. Details:\n{exc}"
            log.debug(msg)
            # add errors
            for filepath, fileinfo in files.items():
                self.file_errors.append(
                    s.Error(
                        code=errors.InvalidFileContext.code,
                        message=msg,
                        filepath=fileinfo.name,
                    )
                )
            return

        if item_context.packfile:
            packfile_size = sum(f.size for f in files.values())
            filename = item_context.packfile.name
            if not filename:
                parent_ctx = self._get_parent_context(item_context)
                cname = parent_ctx.label or parent_ctx.id
                packfile_type = item_context.packfile.type

                is_single_file = (
                    packfile_type != "zip"
                    and len(files) == 1
                    and not self.ingest_config.zip_single_dicom
                )

                item_context.packfile.zip = not is_single_file

                if not packfile_type or packfile_type == "zip":
                    if is_single_file:
                        filename = cname
                    else:
                        filename = f"{cname}.zip"
                else:
                    if is_single_file:
                        filename = f"{cname}.{packfile_type}"
                    else:
                        filename = f"{cname}.{packfile_type}.zip"

            yield s.Item(
                type="packfile",
                dir=dirpath,
                filename=filename,
                files=list(files.keys()),
                files_cnt=len(files),
                bytes_sum=packfile_size,
                context=item_context,
            )
        else:
            for filepath, fileinfo in files.items():
                if isinstance(fileinfo, FWFileInfo):
                    # Upload task gives the item.dir/item.files[0] to the Walker::open.
                    # FWFile needs a container_id and a filename for downloading the
                    # content of a file.
                    yield s.Item(
                        type="file",
                        dir=fileinfo.container_id,  # dir is container_id
                        filename=fs.path.basename(filepath),
                        files=[fileinfo.filename],  # files[0] is filename
                        files_cnt=1,
                        bytes_sum=fileinfo.size,
                        context=item_context,
                    )
                else:
                    yield s.Item(
                        type="file",
                        dir=dirpath,
                        filename=fs.path.basename(filepath),
                        files=[filepath],
                        files_cnt=1,
                        bytes_sum=fileinfo.size,
                        context=item_context,
                    )

    @staticmethod
    def _get_parent_context(context: s.ItemContext) -> s.SourceContainerContext:
        """
        Get parent container context from item context, like if group, project in the context
        this method will return the project context
        """
        for cont_level in ("acquisition", "session", "subject", "project", "group"):
            cont_ctx = getattr(context, cont_level, None)
            if cont_ctx:
                break
        return cont_ctx

    @staticmethod
    def _create_path_for_container_metadata_filepath(full_filepath):
        """
        From FW container metadata filepath (e.g.:
        sth/SUBJECTS/subj/SESSIONS/sesh/ACQUISITIONS/acq/somefile.flywheel.json) creates
        path to the actual container without the delimiters and the projectname (e.g.:
        subj/sesh/acq).
        """
        path_parts = _FW_CONTAINER_PATH_PATTERN.sub("", full_filepath).split("/")[1:-1]
        return "/".join([util.sanitize_filename(part) for part in path_parts])

    @staticmethod
    def _trim_container_meta(metadata):
        for k in [
            "created",
            "id",
            "label",
            "modified",
            "notes",
            "permissions",
            "revision",
        ]:
            metadata.pop(k, None)

        return metadata

    @staticmethod
    def _trim_file_meta(metadata):
        for k in [
            "created",
            "hash",
            "modified",
            "origin",
            "path",
            "provider_id",
            "replaced",
            "size",
        ]:
            metadata.pop(k, None)

        return metadata

    def _scan_for_project_strategy(self, subdir, initial_context, root_node):
        """
        It goes through the files and
            - if it's a regular file, the file Item will be created and saved into prev,
              because there's a chance that it's metadata will come in the next file
            - if it's a file metadata (which ALWAYS comes right after the target reqular
              file), its content will be attached to the target regular file which will
              be yielded in the begininng of the next iteration, or at the end of the
              function.
            - immediately yields container metadata (which goes into
              FWContainerMetadata DB table)
        """
        prev = None
        enable_project_files = getattr(
            self.ingest_config, "enable_project_files", False
        )
        for fileinfo in self.iter_files(subdir):
            if len(fileinfo.name.split("/")) <= 3 and (
                "FILES" not in fileinfo.name or not enable_project_files
            ):
                # skipping project level such as
                # - project-name/project-name.flywheel.json
                # - project-name/FILES/some-file.dcm if no --enable-project-files
                continue

            if isinstance(fileinfo, FWMetaFileInfo):
                metadata = fileinfo.content

                if metadata:
                    if metadata.get("mimetype") or "FILES" in fileinfo.name:
                        # file
                        if prev:
                            prev.fw_metadata = (
                                {}
                                if self.strategy_config.no_metadata
                                else self._trim_file_meta(metadata)
                            )
                    else:
                        # container
                        path = self._create_path_for_container_metadata_filepath(
                            fileinfo.name
                        )

                        if path:
                            yield s.FWContainerMetadata(
                                path=path,
                                content={}
                                if self.strategy_config.no_metadata
                                else self._trim_container_meta(metadata),
                            )

                continue

            if prev:
                yield prev
                prev = None

            context = copy.deepcopy(initial_context)
            path_parts = deque(fileinfo.name.split("/"))
            node = root_node
            parent_dirpath = "/"
            while len(path_parts) > 1:
                dirname = path_parts.popleft()
                parent_dirpath = fs.path.combine(parent_dirpath, dirname)
                node = node.extract_metadata(
                    dirname, context, self.walker, path=parent_dirpath
                )
                if node in (None, TERMINAL_NODE):
                    break

            rel_filepath = fs.path.join(*path_parts)
            item_generator = self.create_task_or_item(
                parent_dirpath,
                node,
                context,
                {rel_filepath: fileinfo},
            )
            prev = next(item_generator)  # pylint: disable=stop-iteration-return

        if prev:
            yield prev
