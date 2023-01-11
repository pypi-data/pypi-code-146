import os
import re
import subprocess
import sys


from drb.core import DrbNode
from argparse import ArgumentParser
import stat
import logging
import errno
import pyfuse3
import trio


# If we are running from the pyfuse3 source directory, try
# to load the module from there first.
basedir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '../..'))
if (os.path.exists(os.path.join(basedir, 'setup.py')) and
        os.path.exists(os.path.join(basedir, 'src', 'pyfuse3.pyx'))):
    sys.path.insert(0, os.path.join(basedir, 'src'))


try:
    import faulthandler
except ImportError:
    pass
else:
    faulthandler.enable()

log = logging.getLogger(__name__)


class DrbFs(pyfuse3.Operations):
    def __init__(self, node: DrbNode):
        super(DrbFs, self).__init__()

        self.list_node = []

        self.node_id = pyfuse3.ROOT_INODE + 1

        self.list_node.append(node)

        self.list_node_child = {(pyfuse3.ROOT_INODE, node): self.node_id}

        self.hello_data = b"hello world\n"
        self.node = node

    def getattr_node(self, node, entry, value=False):
        if node.has_child() and not value:
            entry.st_mode = (stat.S_IFDIR | 0o755)
            entry.st_size = 0
        else:
            entry.st_mode = (stat.S_IFREG | 0o644)
            if node.value is not None:
                if isinstance(node.value, bytes):
                    value = node.value.decode()
                else:
                    value = str(node.value)
                entry.st_size = len(value)
            # elif node.has_impl(io.BufferedIOBase):
            #     entry.st_size = ????
            # TODO manage stream
            else:
                entry.st_size = 0

    def getattr_node_sync(self, inode, ctx=None, value=False):
        entry = pyfuse3.EntryAttributes()
        if inode == pyfuse3.ROOT_INODE:
            entry.st_mode = (stat.S_IFDIR | 0o755)
            entry.st_size = 0
        elif (inode - self.node_id) < len(self.list_node):
            node = self.list_node[inode - self.node_id]
            self.getattr_node(node, entry, value)
        else:
            raise pyfuse3.FUSEError(errno.ENOENT)

        stamp = int(1438467123.985654 * 1e9)
        entry.st_atime_ns = stamp
        entry.st_ctime_ns = stamp
        entry.st_mtime_ns = stamp
        entry.st_gid = os.getgid()
        entry.st_uid = os.getuid()
        entry.st_ino = inode
        if value:
            entry.st_ino = inode+1000

        return entry

    async def getattr(self, inode, ctx=None):
        return self.getattr_node_sync(inode, ctx)

    def get_inode_from_parent_node(self, inode):
        if (inode - self.node_id) > len(self.list_node):
            raise pyfuse3.FUSEError(errno.ENOENT)
        parent_node = self.list_node[inode - self.node_id]
        node = parent_node.parent
        inode_parent = None
        if node is not None:
            for index in range(len(self.list_node)):
                if self.list_node[index] == node.path:
                    return index+self.node_id
                if self.list_node[index].path == node.path:
                    inode_parent = index+self.node_id
        return inode_parent

    async def lookup(self, parent_inode, name, ctx=None):
        if parent_inode == pyfuse3.ROOT_INODE:
            if name == self.node.name.encode():
                return self.getattr_node_sync(self.node_id)
            raise pyfuse3.FUSEError(errno.ENOENT)

        name_child = name.decode()
        if name_child == '.value':
            return self.getattr_node_sync(parent_inode, value=True)
        if name == '.':
            return self.getattr_node_sync(parent_inode)
        elif name == '..':
            inode_parent = self.get_inode_from_parent_node(parent_inode)
            if inode_parent is not None:
                return self.getattr_node_sync(inode_parent)
            else:
                raise pyfuse3.FUSEError(errno.ENOENT)

        if (parent_inode - self.node_id) > len(self.list_node):
            raise pyfuse3.FUSEError(errno.ENOENT)
        parent_node = self.list_node[parent_inode - self.node_id]
        index = 0

        if re.match(r'.*\[\d+\]$', name_child)\
                and not parent_node.has_child(name_child):
            index_str = re.findall(r'\[(\d+)\]$', name_child)

            index = int(index_str[0])
            name_child = re.sub(r'.*\[\d+\]$', '', name_child)

        if parent_node.has_child(name_child):
            try:
                child = parent_node[name_child, index]
            except Exception as error:
                raise pyfuse3.FUSEError(errno.ENOENT)

            inode_child = self.insert_child_if(parent_inode,
                                               name_child,
                                               child)
            return await self.getattr(inode_child)

        raise pyfuse3.FUSEError(errno.ENOENT)

    async def opendir(self, inode, ctx):
        if inode == pyfuse3.ROOT_INODE:
            return inode
        if (inode - self.node_id) > len(self.list_node):
            raise pyfuse3.FUSEError(errno.ENOENT)
        return inode

    def insert_child_if(self, dir_inode, name_child, node_child):
        if (dir_inode, name_child) in self.list_node_child.keys():
            inode_child = self.list_node_child[(dir_inode, name_child)]
        else:
            inode_child = len(self.list_node) + self.node_id
            self.list_node_child[(dir_inode, name_child)] = inode_child
            self.list_node.append(node_child)
        return inode_child

    def insert_child(self, token, dir_inode, name_child, node_child,
                     value_child=False):
        inode_child = self.insert_child_if(dir_inode,
                                           name_child,
                                           node_child)
        pyfuse3.readdir_reply(
            token, name_child.encode(),
            self.getattr_node_sync(inode_child, value=value_child), 1)

    async def readdir(self, inode, start_id, token):
        if inode == pyfuse3.ROOT_INODE:
            if start_id == 0:
                pyfuse3.readdir_reply(
                    token, self.node.name.encode(),
                    await self.getattr(self.node_id),
                    1)
            return

        dir_inode = inode
        if (dir_inode - self.node_id) > len(self.list_node):
            raise pyfuse3.FUSEError(errno.ENOENT)
        dir_node = self.list_node[dir_inode - self.node_id]

        # only one entry
        if start_id == 0:
            pyfuse3.readdir_reply(
                token, '.'.encode(), await self.getattr(dir_inode),
                dir_inode)
            inode_parent = self.get_inode_from_parent_node(dir_inode)
            if inode_parent is not None:
                pyfuse3.readdir_reply(
                    token, '..'.encode(), await self.getattr(inode_parent),
                    inode_parent)
            # if dir_node.value is not None or \
            #         dir_node.has_impl(io.BufferedIOBase):
            # TODO manage streamio
            if dir_node.value is not None:
                self.insert_child(token,
                                  dir_inode=dir_inode,
                                  name_child='.value',
                                  node_child=dir_node,
                                  value_child=True)

            list_name_child = []
            for child in dir_node.children:
                if child.name not in list_name_child:
                    list_name_child.append(child.name)

            for name_child in list_name_child:
                list_child_named = dir_node[name_child, :]
                if len(list_child_named) > 1:
                    index = 0
                    for child in list_child_named:
                        index = index + 1
                        self.insert_child(token,
                                          dir_inode=dir_inode,
                                          name_child=name_child + f'[{index}]',
                                          node_child=child)

                else:
                    self.insert_child(token,
                                      dir_inode=dir_inode,
                                      name_child=name_child,
                                      node_child=list_child_named[0])

        return

    async def open(self, inode, flags, ctx):
        if (inode - self.node_id) > len(self.list_node):
            raise pyfuse3.FUSEError(errno.ENOENT)
        if flags & os.O_RDWR or flags & os.O_WRONLY:
            raise pyfuse3.FUSEError(errno.EACCES)
        return pyfuse3.FileInfo(fh=inode)

    async def read(self, fh, off, size):
        if (fh - self.node_id) > len(self.list_node):
            raise pyfuse3.FUSEError(errno.ENOENT)
        node = self.list_node[fh - self.node_id]
        if node.value is not None:
            value = node.value
            if isinstance(value, bytes):
                value = node.value.encode()
            else:
                value = str(value)
            return value.encode()[off:off + size]
        else:
            return ''


def init_logging(debug=False):
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(threadName)s: '
                                  '[%(name)s] %(message)s',
                                  datefmt="%Y-%m-%d %H:%M:%S")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    if debug:
        handler.setLevel(logging.DEBUG)
        root_logger.setLevel(logging.DEBUG)
    else:
        handler.setLevel(logging.INFO)
        root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)


def parse_args():
    '''Parse command line'''

    parser = ArgumentParser()

    parser.add_argument('mountpoint', type=str,
                        help='Where to mount the file system')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='Enable debugging output')
    parser.add_argument('--debug-fuse', action='store_true', default=False,
                        help='Enable FUSE debugging output')
    return parser.parse_args()


class FsNode:
    def __init__(self, node: DrbNode, mount_point, debug=False):
        self.node = node
        self.mount_point = mount_point
        self.debug = debug
        self.debug_fuse = debug

    def close(self):
        print(subprocess.Popen('umount ' + self.mount_point,
                               shell=True,
                               stdout=subprocess.PIPE).stdout.read())

    def run_fs(self):
        # options = parse_args()
        init_logging(self.debug)

        node = self.node
        testfs = DrbFs(node)
        fuse_options = set(pyfuse3.default_options)
        fuse_options.add(f'fsname={node.name}')
        if self.debug:
            fuse_options.add('debug')
        pyfuse3.init(testfs, self.mount_point, fuse_options)

        try:
            trio.run(pyfuse3.main)
        finally:
            print('close')
            pyfuse3.close()


def init_fs(**kwargs):
    node = kwargs['node']
    mount_point = kwargs['mountpoint']

    if not os.path.isdir(mount_point):
        try:
            os.mkdir(mount_point)
        except Exception as error:
            print(str(error))

    fsnode = FsNode(node, mount_point)
    return fsnode


def start_fs(**kwargs):
    fsnode = init_fs(**kwargs)
    fsnode.run_fs()
