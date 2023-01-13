import dataclasses
import functools

from fsspec import spec  # type: ignore
from spinsrv import spin
from spinsrv import spinpy


@dataclasses.dataclass
class Config:
    public: str = ""
    private: str = ""
    citizen: spin.CitizenName = ""


# I copied in a sample from the Databricks filesystem implementation
# https://github.com/fsspec/filesystem_spec/blob/master/fsspec/implementations/dbfs.py
class SpinFileSystem(spec.AbstractFileSystem):
    protocol = "spin"
    root_marker = "/"

    def __init__(self, config: Config, *args, **kwargs):
        self.config = config

        self.kc = spinpy.KeyServerHTTPClient()
        self.dc = spinpy.DirServerHTTPClient()
        self.bc = spinpy.BitServerHTTPClient()

        super().__init__(*args, **kwargs)

    def ls(self, path, detail=True):
        """
        List the contents of the given path.

        Parameters
        ----------
        path: str
            Absolute path
        detail: bool
            Return not only the list of filenames,
            but also additional information on file sizes
            and types.
        """
        try:
            out = self._ls_from_cache(path)
        except FileNotFoundError:
            out = None

        if not out:
            resp = self.dc.tree(
                spin.DirTreeRequest(
                    public=self.config.public,
                    private=self.config.private,
                    citizen=self.config.citizen,
                    path=path,
                    level=1,
                )
            )
            if resp.error != "":
                raise OSError(resp.error)  # TODO: better error handling?
            entries = resp.entries
            out = [
                {
                    "name": e.path,
                    "type": "directory" if e.type == spin.EntryDir else "file",
                    "size": sum([b.size for b in e.blocks]),
                }
                for e in entries
            ]
            self.dircache[path] = out

        if detail:
            return out
        return [o["name"] for o in out]

    # helper to get parents of a path, used by makedirs below
    def _parents(self, path):
        x = path.split("/")
        ps = []
        for i in range(1, len(x)):
            ps.append("/".join(x[0 : i + 1]))
        return ps

    def makedirs(self, path, exist_ok=True):
        """
        Create a given absolute path and all of its parents.

        Parameters
        ----------
        path: str
            Absolute path to create
        exist_ok: bool
            If false, checks if the folder
            exists before creating it (and raises an
            Exception if this is the case)
        """
        ops = []
        ps = self._parents(path)
        for p in ps:
            ops.append(
                spin.DirOp(
                    type=spin.PutDirOperation,
                    entry=spin.DirEntry(
                        type=spin.EntryDir,
                        citizen=self.config.citizen,
                        path=p,
                        sequence=spin.SeqIgnore,
                    ),
                )
            )

        seq = spin.SeqIgnore
        if not exist_ok:
            ops[-1].sequence = spin.SeqNotExist

        resp = self.dc.apply(
            spin.DirApplyRequest(
                public=self.config.public,
                private=self.config.private,
                ops=ops,
            )
        )
        if resp.error != "":
            raise OSError(resp.error)  # TODO: better error handling?

        for p in ps:
            self.invalidate_cache(p)

    def mkdir(self, path, create_parents=True, **kwargs):
        """
        Create a given absolute path and all of its parents.

        Parameters
        ----------
        path: str
            Absolute path to create
        create_parents: bool
            Whether to create all parents or not.
            "False" is not implemented so far.
        """
        if not create_parents:
            raise NotImplementedError

        self.mkdirs(path, **kwargs)

    def cp_file(self, frompath, topath, **kwargs):
        e = self._lookup(frompath)
        if e is None:
            raise FileNotFoundError(f"path {frompath}")
        e.path = topath
        e.sequence = spin.SeqIgnore
        resp = self.dc.apply(
            spin.DirApplyRequest(
                public=self.config.public,
                private=self.config.private,
                ops=[
                    spin.DirOp(
                        type=spin.PutDirOperation,
                        entry=e,
                    )
                ],
            )
        )
        if resp.error != "":
            raise OSError(resp.error)
        self.invalidate_cache(self._parent(topath))

    def rm_file(self, path):
        resp = self.dc.apply(
            spin.DirApplyRequest(
                public=self.config.public,
                private=self.config.private,
                ops=[
                    spin.DirOp(
                        type=spin.DelDirOperation,
                        entry=spin.DirEntry(
                            citizen=self.config.citizen,
                            path=path,
                            sequence=spin.SeqIgnore,
                        ),
                    )
                ],
            )
        )
        if resp.error != "":
            raise OSError(resp.error)  # TODO: better error handling?
        # TODO check for error on resp
        self.invalidate_cache(self._parent(path))

    def _open(self, path, mode="rb", block_size="default", **kwargs):
        """
        Overwrite the base class method to make sure to create a SpinFile.
        All arguments are copied from the base method.
        """
        return SpinFile(self, path, mode=mode, block_size=block_size, **kwargs)

    # lookup a dir entry
    def _lookup(self, path: spin.Path) -> spin.DirEntry:
        resp = self.dc.tree(
            spin.DirTreeRequest(
                public=self.config.public,
                private=self.config.private,
                citizen=self.config.citizen,
                path=path,
                level=0,
            )
        )
        if resp.error != "":
            raise OSError(resp.error)  # TODO: better handling?
        return resp.entries[0]

    # get the data from the store
    @functools.lru_cache(maxsize=2000)
    def _get(self, ref: spin.Ref) -> bytes:
        resp = self.bc.apply(
            spin.BitApplyRequest(
                public=self.config.public,
                private=self.config.private,
                ops=[
                    spin.BitOp(
                        type=spin.GetBitOperation,
                        ref=ref,
                    )
                ],
            )
        )
        if resp.error != "":
            print(resp)
            raise OSError(resp.error)  # TODO: better handling
        if len(resp.outcomes) != 1:
            print(resp)
            raise OSError(f"expected 1 outcome, got {len(resp.outcomes)}")

        return resp.outcomes[0].bytes

    def invalidate_cache(self, path=None):
        if path is None:
            self.dircache.clear()
        else:
            self.dircache.pop(path, None)
        super().invalidate_cache(path)


# I copied in a sample from the Databricks filesystem implementation
# https://github.com/fsspec/filesystem_spec/blob/master/fsspec/implementations/dbfs.py
class SpinFile(spec.AbstractBufferedFile):
    """
    Helper class for files referenced in the SpinFileSystem.
    """

    DEFAULT_BLOCK_SIZE = 10 * 2**20

    def __init__(
        self,
        fs,
        path,
        mode="rb",
        block_size="default",
        autocommit=True,
        cache_type="readahead",
        cache_options=None,
        **kwargs,
    ):
        """
        Create a new instance of the SpinFile.

        """
        if block_size is None or block_size == "default":
            block_size = self.DEFAULT_BLOCK_SIZE

        self.dir_entry = None

        super().__init__(
            fs,
            path,
            mode=mode,
            block_size=block_size,
            autocommit=autocommit,
            cache_type=cache_type,
            cache_options=cache_options or {},
            **kwargs,
        )

    def _initiate_upload(self):
        """Internal function to start a file upload"""
        self.dir_entry = spin.DirEntry(
            type=spin.EntryFile,
            citizen=self.fs.config.citizen,
            path=self.path,
            sequence=spin.SeqIgnore,
        )

    def _upload_chunk(self, final=False):
        """Internal function to add a chunk of data to a started upload"""
        self.buffer.seek(0)
        data = self.buffer.getvalue()

        data_chunks = [
            data[start:end] for start, end in self._to_sized_blocks(len(data))
        ]

        for (i, data_chunk) in enumerate(data_chunks):
            resp = self.fs.bc.apply(
                spin.BitApplyRequest(
                    public=self.fs.config.public,
                    private=self.fs.config.private,
                    ops=[spin.BitOp(type=spin.PutBitOperation, bytes=data_chunk)],
                )
            )

            if resp.error != "":
                print(resp)
                raise OSError(resp.error)  # TODO: better handling?

            if len(resp.outcomes) != 1:
                print(resp)
                raise OSError(f"expected 1 outcome, got {len(resp.outcomes)}")

            self.dir_entry.blocks.append(
                spin.DirBlock(
                    ref=resp.outcomes[0].ref_data.ref,
                    offset=self.offset + i * self.blocksize,
                    size=len(data_chunk),
                )
            )

        if final:
            resp = self.fs.dc.apply(
                spin.DirApplyRequest(
                    public=self.fs.config.public,
                    private=self.fs.config.private,
                    ops=[spin.DirOp(type=spin.PutDirOperation, entry=self.dir_entry)],
                )
            )
            if resp.error != "":
                print(resp)
                raise OSError(resp.error)  # TODO: better handling
            self.dir_entry = resp.entries[0]
            self.fs.invalidate_cache(self.fs._parent(self.dir_entry.path))
            return True

    # warn: this code is not seriously tested
    def _intersection(self, a, b, c, d):
        # compute [a, b] ∩ [c,d]
        if b < c or a > d:
            return (0, 0)
        return (max(a, c), min(b, d))

    # warn: this code is not seriously tested
    def _blocks_in_range(self, start, end):
        # find the blocks for the file for the bit range start to end
        out = []
        for b in self.dir_entry.blocks:
            bstart, bend = b.offset, b.offset + b.size
            istart, iend = self._intersection(start, end, bstart, bend)
            if iend - istart == 0:  # skip if empty intersection
                continue
            out.append((b, (istart, iend)))
        return out

    def _fetch_range(self, start, end):
        """Internal function to download a block of data"""
        if self.dir_entry is None:
            self.dir_entry = self.fs._lookup(self.path)

        return_buffer = b""
        for (b, (s, e)) in self._blocks_in_range(start, end):
            data = self.fs._get(b.ref)
            return_buffer += data[start - b.offset : end]
        return return_buffer

    def _to_sized_blocks(self, total_length):
        """Helper function to split a range from 0 to total_length into blocksizes"""
        for data_chunk in range(0, total_length, self.blocksize):
            data_start = data_chunk
            data_end = min(total_length, data_chunk + self.blocksize)
            yield data_start, data_end
