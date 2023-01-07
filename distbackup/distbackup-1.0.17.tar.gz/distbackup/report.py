import time
import logging

from typing import Optional
from dataclasses import dataclass, field
from ktpanda.textcolor import Colorizer

from .utils import addcomma, disk_in_nexus, round_blocks, prettysize, prettysize_clr, size_color, Progress
from .nexus import NexusLevelDict
from .database import BackupDB

log = logging.getLogger(__name__)

@dataclass
class FileNode:
    '''Track the size of a file or folder for `ncdu` and `tree` commands'''

    name: str
    parent: object
    size: int = 0
    hash: Optional[str] = None
    lastmod: Optional[float] = None
    iscanon: bool = True
    refs: Optional[int] = None
    copies: Optional[int] = None
    nexus: Optional[str] = None
    priority: int = 1
    obj_priority: int = 1
    maxcopies: Optional[int] = None
    obj_maxcopies: Optional[int] = None
    inode: Optional[int]  = None
    children: dict[str, object] = field(default_factory=dict)

    total_files: int = 0
    total_size: int = 0
    copy_files: Optional[list] = None
    copy_size: Optional[list] = None

class Reporter:
    def __init__(self, db:BackupDB, ignore_lock=False):
        self.db:BackupDB = db

    def report(self, nexus_levels:NexusLevelDict=None, exclude_saturated:bool=False):

        if nexus_levels is None:
            nexus_levels = NexusLevelDict(self.db.load_nexus())

        copy_data = nexus_levels.get_copy_data()
        if not copy_data or copy_data == [0]:
            yield Colorizer().t('No files in database.')
            return

        yield Colorizer().t('Usage:')

        for i, (size, saturated_size) in enumerate(copy_data):
            c = Colorizer().t(f'{i:3d}: ')
            if saturated_size:
                c.t(prettysize_clr(size - saturated_size), rpad=7)
                c.t(' + ').t(prettysize_clr(saturated_size)).t(' saturated')
            else:
                c.t(prettysize_clr(size - saturated_size))
            yield c

        clridx = 0
        yield Colorizer().t('  %-12s  %-20s %-7s %s' % ('name', 'total', 'free',' '.join('%-7d' % j for j in range(1, len(copy_data)))))
        with self.db.execute('SELECT name, nexus_index, size FROM disk WHERE name NOTNULL ORDER BY name') as curs:
            for name, index, dsize in curs:
                data = nexus_levels.get_copy_data(index)[1:]
                total = sum(lvl[0] for lvl in data)
                free = dsize - total

                fg_clr = '!ccc' if (clridx & 1) else '!fff'
                bg_clr = '222' if (clridx & 1) else '333'
                clridx += 1

                txt = Colorizer(fg=fg_clr, bg=bg_clr)
                if self.db.current_disk and name == self.db.current_disk.name:
                    txt.set(fg='!c0f').t('> ')
                else:
                    txt.t('  ')

                txt.t(name, rpad=12).t(' ')
                txt.t(addcomma(total), lpad=20, fg=size_color(total)).t(' ')
                txt.t(prettysize_clr(free), lpad=7)
                if not data:
                    txt.t(' no files')
                else:
                    for size, saturated_size in data:
                        txt.t(' ').t(prettysize_clr(size - saturated_size if exclude_saturated else size), lpad=7)

                yield txt

    def print_report(self, *a, indent='', **kw):
        for line in self.report(*a, **kw):
            log.info(indent + line.get())

    def list_files(self, pat):
        destid = self.db.current_disk.nexus_index if self.db.current_disk else None
        for path, size, lastmod, hash, nexus in self.db.filter_files(
                pat, sql='SELECT ft.virtual_path, ft.size, ft.last_modified, ft.hash, ob.nexus FROM file_tree ft LEFT JOIN object ob ON ft.hash = ob.hash'):
            if destid is not None:
                if nexus is None:
                    continue
                if not disk_in_nexus(nexus, destid):
                    continue

            disks = ','.join(self.db.nexus_disks(nexus)) if nexus else ''
            print('%-7s (%s) %s' % (prettysize(size), disks, path))

    def get_tree(self, mincopies=None, maxcopies=None):
        root = FileNode('', None, inode=1)
        nodebypath = {}

        max_copies = self.db.query_scalar('SELECT max(copies) + 1 FROM object')
        root.copy_files = [0] * max_copies
        root.copy_size = [0] * max_copies
        cnt = self.db.query_scalar('SELECT count(virtual_path) FROM file_tree')
        i = 0
        lprogress = ''

        vinode = 1
        hash_to_inode = {}

        where = []
        if mincopies is not None:
            where.append(f'ob.copies >= {int(mincopies)}')
        if maxcopies is not None:
            where.append(f'ob.copies <= {int(maxcopies)}')
        where = 'WHERE ' + ' AND '.join(where) if where else ''

        sql = f'''
        SELECT ft.last_modified, ft.hash, ft.size, ft.virtual_path, ft.priority, ft.maxcopies,
               ob.blocksize, ob.refs, ob.copies, ob.nexus, ob.last_path, ob.priority, ob.maxcopies
        FROM file_tree ft
        INNER JOIN object ob ON ft.hash = ob.hash
        ''' + where

        progress = Progress.get_global()
        progress.set_status('loading db...')
        with self.db.execute(sql) as curs:
            for lastmod, hash, size, path, prio, maxcopies, blocksize, refs, copies, nexus, lpath, obprio, obmaxcopies in curs:
                cnode = root
                p = [root]
                for comp in path.split('/')[1:]:
                    nnode = cnode.children.get(comp)
                    if nnode is None:
                        vinode += 1
                        cnode.children[comp] = nnode = FileNode(comp, cnode, inode=vinode)
                        nnode.copy_size = [0] * max_copies
                        nnode.copy_files = [0] * max_copies
                    cnode = nnode
                    p.append(cnode)

                cnode.size = size
                cnode.lastmod = lastmod
                cnode.hash = hash
                cnode.priority = prio
                cnode.obj_priority = obprio
                cnode.maxcopies = maxcopies
                cnode.obj_maxcopies = obmaxcopies

                cnode.iscanon = path == lpath
                cnode.refs = refs
                cnode.copies = copies
                cnode.nexus = nexus
                inode = hash_to_inode.get(hash)
                if inode is None:
                    hash_to_inode[hash] = cnode.inode
                else:
                    cnode.inode = inode

                ref_blocksize = blocksize // refs
                if path == lpath:
                    ref_blocksize += blocksize % refs

                for node in p:
                    node.total_size += ref_blocksize
                    node.total_files += 1
                    node.copy_size[copies] += ref_blocksize
                    node.copy_files[copies] += 1

                i += 1
                progress.progress((i + 1) * 100 / cnt)

        progress.reset()
        return root

    def make_ncdu(self, mincopies=None, maxcopies=None):
        root = self.get_tree(mincopies, maxcopies)
        def visit_node(node):
            name = node.name.strip('/') or '/distbackup'
            if node.nexus:
                name += ' (' + ','.join(self.db.nexus_disks(node.nexus)) + ')'
            if node.priority != 1:
                name += f' (P{node.priority})'

            if node.maxcopies:
                name += f' (M{node.maxcopies})'

            data = {
                "name": name,
                "asize": node.size,
                "dsize": round_blocks(node.size),
            }

            if node.children:
                data['asize'] = 4096
                data['dsize'] = 4096
                data['dev'] = 1
                data['ino'] = node.inode
                rval = [data]
                for cnode in sorted(list(node.children.values()), key=lambda c:-c.total_size):
                    rval.append(visit_node(cnode))
            else:
                if node.refs > 1:
                    data['hlnkc'] = True
                data['ino'] = node.inode
                rval = data

            return rval
        data = [1, 1,
            {
                "progname": "ncdu",
                "progver": "1.15.1",
                "timestamp": int(time.time())
            },
            visit_node(root)
        ]
        return data
