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
            pqq__cmqic = MPI.COMM_WORLD
            tcek__ogvt = None
            if pqq__cmqic.Get_rank() == 0:
                tcek__ogvt = str(uuid4())
            tcek__ogvt = pqq__cmqic.bcast(tcek__ogvt)
        else:
            tcek__ogvt = str(uuid4())
        self.name = os.path.join(gettempdir(), tcek__ogvt)

    def initialize(self):
        if not self.initialized:
            if self.is_parallel:
                import bodo
                self.active_rank = bodo.get_rank(
                    ) in bodo.get_nodes_first_ranks()
            else:
                self.active_rank = True
            jka__exu = None
            if self.active_rank:
                try:
                    os.mkdir(self.name, 448)
                except Exception as msjd__pdwoj:
                    jka__exu = msjd__pdwoj
            if self.is_parallel:
                pqq__cmqic = MPI.COMM_WORLD
                jts__lfzl = isinstance(jka__exu, Exception)
                lwmd__rra = pqq__cmqic.allreduce(jts__lfzl, op=MPI.LOR)
                if lwmd__rra:
                    if jts__lfzl:
                        raise jka__exu
                    else:
                        raise Exception(
                            'Error during temporary directory creation. See exception on other ranks.'
                            )
            elif isinstance(jka__exu, Exception):
                raise jka__exu
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
                    except AttributeError as ayd__fsgg:
                        pass
                    os.chmod(path, 448)
                try:
                    if path != name:
                        resetperms(os.path.dirname(path))
                    resetperms(path)
                    try:
                        os.unlink(path)
                    except (IsADirectoryError, PermissionError) as ayd__fsgg:
                        cls._rmtree(path, ignore_errors=ignore_errors)
                except FileNotFoundError as ayd__fsgg:
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
