import os
import shutil
import warnings
import weakref
from tempfile import gettempdir
from uuid import uuid4
from mpi4py import MPI


class LazyTemporaryDirectory:

    def __init__(self, ignore_cleanup_errors=False, is_parallel=True):
        self._ignore_cleanup_errors = ignore_cleanup_errors
        self.initialized = False
        self.is_parallel = is_parallel
        self.active_rank = False
        if self.is_parallel:
            hvsol__pyrc = MPI.COMM_WORLD
            fcb__lubln = None
            if hvsol__pyrc.Get_rank() == 0:
                fcb__lubln = str(uuid4())
            fcb__lubln = hvsol__pyrc.bcast(fcb__lubln)
        else:
            fcb__lubln = str(uuid4())
        self.name = os.path.join(gettempdir(), fcb__lubln)

    def initialize(self):
        if not self.initialized:
            if self.is_parallel:
                import bodo
                self.active_rank = bodo.get_rank(
                    ) in bodo.get_nodes_first_ranks()
            else:
                self.active_rank = True
            shk__uqex = None
            if self.active_rank:
                try:
                    os.mkdir(self.name, 448)
                except Exception as arip__pij:
                    shk__uqex = arip__pij
            if self.is_parallel:
                hvsol__pyrc = MPI.COMM_WORLD
                dpb__bgtp = isinstance(shk__uqex, Exception)
                bcze__tnxgs = hvsol__pyrc.allreduce(dpb__bgtp, op=MPI.LOR)
                if bcze__tnxgs:
                    if dpb__bgtp:
                        raise shk__uqex
                    else:
                        raise Exception(
                            'Error during temporary directory creation. See exception on other ranks.'
                            )
            elif isinstance(shk__uqex, Exception):
                raise shk__uqex
            if self.active_rank:
                self._finalizer = weakref.finalize(self, self._cleanup,
                    self.name, warn_message='Implicitly cleaning up {!r}'.
                    format(self), ignore_errors=self._ignore_cleanup_errors)
            else:
                self._finalizer = weakref.finalize(self, lambda : None)
            self.initialized = True

    @classmethod
    def _rmtree(cls, name, ignore_errors=False):

        def onerror(func, path, exc_info):
            if issubclass(exc_info[0], PermissionError):

                def resetperms(path):
                    try:
                        os.chflags(path, 0)
                    except AttributeError as lsxbd__nbmqx:
                        pass
                    os.chmod(path, 448)
                try:
                    if path != name:
                        resetperms(os.path.dirname(path))
                    resetperms(path)
                    try:
                        os.unlink(path)
                    except (IsADirectoryError, PermissionError
                        ) as lsxbd__nbmqx:
                        cls._rmtree(path, ignore_errors=ignore_errors)
                except FileNotFoundError as lsxbd__nbmqx:
                    pass
            elif issubclass(exc_info[0], FileNotFoundError):
                pass
            elif not ignore_errors:
                raise
        shutil.rmtree(name, onerror=onerror)

    @classmethod
    def _cleanup(cls, name, warn_message, ignore_errors=False):
        cls._rmtree(name, ignore_errors=ignore_errors)
        warnings.warn(warn_message, ResourceWarning)

    def __repr__(self):
        return '<{} {!r}>'.format(self.__class__.__name__, self.name)

    def __enter__(self):
        self.initialize()
        return self.name

    def __exit__(self, exc, value, tb):
        self.cleanup()

    def cleanup(self):
        if self.initialized and self.active_rank and (self._finalizer.
            detach() or os.path.exists(self.name)):
            self._rmtree(self.name, ignore_errors=self._ignore_cleanup_errors)
