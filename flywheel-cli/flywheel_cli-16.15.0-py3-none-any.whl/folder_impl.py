"""File system operations"""
import os

import fs.osfs
import fs.path

from . import util
from .importers import ContainerResolver, Uploader


class FSWrapper(Uploader, ContainerResolver):
    """File controller"""

    verb = "Copying"

    def __init__(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)

        self.dst_fs = fs.osfs.OSFS(path)

    def upload(self, container, name, fileobj, metadata=None):
        # Save to disk
        path = fs.path.join(container.id, name)
        if hasattr(fileobj, "read"):
            self.dst_fs.writefile(path, fileobj)
        else:
            self.dst_fs.writebytes(path, fileobj)

    def file_exists(self, container, name):
        path = fs.path.join(container.id, name)
        return self.dst_fs.exists(path)

    def path_el(self, container):
        if container.container_type == "group":
            return util.sanitize_filename(container.id)
        return util.sanitize_filename(container.label)

    def resolve_path(self, container_type, path):
        # Resolve folder
        path = os.path.join(*[util.sanitize_filename(part) for part in path])
        if self.dst_fs.exists(path):
            return path, None
        return None, None

    def create_container(self, parent, container):
        # Create folder, if it doesn't exist
        if parent:
            parent_path = parent.id  # id is a path here
            path = fs.path.join(parent_path, util.sanitize_filename(container.label))
        else:
            path = util.sanitize_filename(container.id)  # Group id

        if not self.dst_fs.exists(path):
            self.dst_fs.makedir(path)

        return path

    def check_unique_uids(self, request):
        raise NotImplementedError("Unique UID check is not supported for output-folder")
