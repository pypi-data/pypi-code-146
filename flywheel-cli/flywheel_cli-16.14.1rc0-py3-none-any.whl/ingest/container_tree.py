"""Provides interface for container creation"""
import logging
import sys
import typing as t
from uuid import UUID

import crayons

from ..util import hrsize
from . import schemas as s

log = logging.getLogger(__name__)


class ContainerNode:
    """Represents a container node in the hierarchy"""

    # pylint: disable=too-few-public-methods, too-many-arguments
    def __init__(
        self,
        label,
        files_cnt=0,
        bytes_sum=0,
        existing=False,
        parent: t.Optional["ContainerNode"] = None,
    ):
        """Initialize ContainerNode"""
        self.label = label
        self.files_cnt = files_cnt
        self.existing = existing
        # holds bytes sum of the sub tree
        # it is continuously updated when building the tree
        self.bytes_sum = bytes_sum

        self.parent = parent
        self.children: t.List["ContainerNode"] = []

    def __str__(self) -> str:
        filesize = hrsize(self.bytes_sum)
        plural = "s" if self.files_cnt > 1 else ""
        status = "using" if self.existing else "creating"
        parts = [f"{crayons.blue(self.label)}"]
        if self.bytes_sum and self.files_cnt:  # container w/ files
            parts.append(f"({filesize} / {self.files_cnt} file{plural})")
        elif self.bytes_sum:  # container w/o files, sub tree size
            parts.append(f"({filesize})")
        parts.append(f"({status})")
        return " ".join(parts)


class ContainerTree:
    """Container tree class"""

    def __init__(self):
        """Build a container tree which can be printed"""
        self.total_bytes_sum = 0
        self.total_files_cnt = 0
        self.root_nodes = []
        self.nodes: t.Dict[UUID, ContainerNode] = {}

    def add_node(self, container: s.Container) -> None:
        """
        Rebuild the hierarchy by adding nodes one by one
        This method assumes that the containers come in order, like parent first then children
        """
        if container.id in self.nodes:
            # container already added
            return
        parent_node = None
        if container.parent_id:
            parent_node = self.nodes.get(container.parent_id)
            if not parent_node:
                log.warning(
                    f"Couldn't find parent node for container: {container.path}. "
                    "Probably trying to build container tree "
                    "not in order (parent first then children). Skipping ..."
                )
                return
        context = container.dst_context or container.src_context
        label = context.label or context.id
        if container.level.name == "group":
            label = context.id
        node = ContainerNode(
            label,
            files_cnt=container.files_cnt or 0,
            bytes_sum=container.bytes_sum or 0,
            existing=bool(container.dst_context),
            parent=parent_node,
        )
        self.nodes[container.id] = node

        if not parent_node:
            self.root_nodes.append(node)
        else:
            parent_node.children.append(node)

        # populate size to parents because the container holds bytes_sum and files_cnt only
        # of files that are in that particular container
        current = parent_node
        while current:
            current.bytes_sum += node.bytes_sum or 0
            current = current.parent

        # track total bytes sum and files count
        self.total_bytes_sum += container.bytes_sum or 0
        self.total_files_cnt += container.files_cnt or 0

    def print_tree(self, fh=sys.stdout):
        """Print hierarchy"""
        utf8 = fh.encoding == "UTF-8"
        none_str = "│  " if utf8 else "|  "
        node_str = "├─ " if utf8 else "|- "
        last_str = "└─ " if utf8 else "`- "

        def pprint_tree(node, prefix="", last=True):
            print(prefix, last_str if last else node_str, node, file=fh, sep="")
            prefix += "   " if last else none_str
            child_count = len(node.children)
            children = node.children
            for i, child in enumerate(children):
                last = i == (child_count - 1)
                pprint_tree(child, prefix, last)

        for node in self.root_nodes:
            pprint_tree(node)
