"""Support distributed deep learning with Horovod
"""
import time
import numba
import numpy as np
from mpi4py import MPI
import bodo
from bodo.libs.distributed_api import create_subcomm_mpi4py, get_host_ranks, get_nodes_first_ranks
dl_status = None


def assert_dl_initialized():
    assert dl_status is not None, 'Horovod has not been initialized. Call bodo.dl.start() first'


class DLStatus(object):

    def __init__(self, framework, gpu_ranks):
        self.framework = framework
        self.gpu_ranks = gpu_ranks


def get_num_gpus(framework):
    if framework == 'torch':
        import torch
        return torch.cuda.device_count()
    elif framework == 'tensorflow':
        import tensorflow as tf
        return len(tf.config.experimental.list_physical_devices('GPU'))
    else:
        raise RuntimeError('Framework {} not recognized'.format(framework))


def get_gpu_ranks(framework):
    ainq__utg = MPI.COMM_WORLD
    etwbk__gymjx = ainq__utg.Get_rank()
    znpef__sqz = get_host_ranks()
    adz__csmxp = get_nodes_first_ranks()
    if etwbk__gymjx in adz__csmxp:
        try:
            cunf__ntjc = get_num_gpus(framework)
        except Exception as rhi__ras:
            cunf__ntjc = rhi__ras
        bux__vlglb = create_subcomm_mpi4py(adz__csmxp)
        vmebg__yvic = bux__vlglb.gather(cunf__ntjc)
        if etwbk__gymjx == 0:
            gpu_ranks = []
            viscs__qdvc = None
            for kluf__kchd, fwbtv__nej in enumerate(znpef__sqz.values()):
                pjy__zjk = vmebg__yvic[kluf__kchd]
                if isinstance(pjy__zjk, Exception):
                    viscs__qdvc = pjy__zjk
                    break
                if pjy__zjk == 0:
                    continue
                kgx__aoyh = len(fwbtv__nej) // pjy__zjk
                for hql__kyuwh, qqm__mqtt in enumerate(fwbtv__nej):
                    if hql__kyuwh % kgx__aoyh == 0:
                        mbm__aax = hql__kyuwh / kgx__aoyh
                        if mbm__aax < pjy__zjk:
                            gpu_ranks.append(qqm__mqtt)
            if viscs__qdvc:
                ainq__utg.bcast(viscs__qdvc)
                raise viscs__qdvc
            else:
                ainq__utg.bcast(gpu_ranks)
    if etwbk__gymjx != 0:
        gpu_ranks = ainq__utg.bcast(None)
        if isinstance(gpu_ranks, Exception):
            rhi__ras = gpu_ranks
            raise rhi__ras
    return gpu_ranks


def is_cuda_available():
    assert_dl_initialized()
    return len(dl_status.gpu_ranks) > 0


def initialize_horovod(framework):
    global dl_status
    if dl_status is not None:
        assert dl_status.framework == framework, 'Attempted to initialize Horovod with different DL frameworks'
        return np.array(dl_status.gpu_ranks, dtype=np.int32)
    gpu_ranks = get_gpu_ranks(framework)
    if framework == 'torch':
        import horovod.torch as hvd
        import torch
        torch.set_num_threads(1)
    elif framework == 'tensorflow':
        import horovod.tensorflow as hvd
        import tensorflow as tf
    else:
        raise RuntimeError('Framework {} not recognized'.format(framework))
    hbe__grdjx = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        bux__vlglb = MPI.COMM_WORLD.Split(color=0 if hbe__grdjx in
            gpu_ranks else MPI.UNDEFINED, key=hbe__grdjx)
        if bux__vlglb != MPI.COMM_NULL:
            hvd.init(comm=bux__vlglb)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                fkn__iet = tf.config.experimental.list_physical_devices('GPU')
                for xgez__xpv in fkn__iet:
                    tf.config.experimental.set_memory_growth(xgez__xpv, True)
                tf.config.experimental.set_visible_devices(fkn__iet[hvd.
                    local_rank()], 'GPU')
    else:
        if hbe__grdjx == 0:
            print('[BODO-DL]: No GPUs found in cluster. Using CPUs')
        hvd.init()
    dl_status = DLStatus(framework, np.array(gpu_ranks, dtype=np.int32))


@numba.njit
def start(framework):
    with numba.objmode:
        initialize_horovod(framework)


@numba.njit
def end():
    with numba.objmode:
        end_py()


def end_py():
    if is_cuda_available():
        wpdmm__xsljp = 17
        ainq__utg = MPI.COMM_WORLD
        bxpi__vlq = MPI.Get_processor_name()
        fenw__msu = get_host_ranks()[bxpi__vlq]
        assert_dl_initialized()
        if bodo.get_rank() == fenw__msu[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for etwbk__gymjx in fenw__msu[1:]:
                ainq__utg.isend(1, dest=etwbk__gymjx, tag=wpdmm__xsljp)
        else:
            while True:
                zvniy__vqte = MPI.Status()
                dxr__pdcz = ainq__utg.Iprobe(MPI.ANY_SOURCE, MPI.ANY_TAG,
                    zvniy__vqte)
                if dxr__pdcz:
                    assert zvniy__vqte.source == fenw__msu[0]
                    assert zvniy__vqte.tag == wpdmm__xsljp
                    ainq__utg.recv(source=0, tag=wpdmm__xsljp)
                    break
                time.sleep(1.0)
    else:
        bodo.barrier()


def _prepare_data_get_gpu_ranks():
    assert_dl_initialized()
    return dl_status.gpu_ranks


@numba.njit
def prepare_data(data):
    with numba.objmode(gpu_ranks='int32[:]'):
        gpu_ranks = _prepare_data_get_gpu_ranks()
    if len(gpu_ranks) > 0:
        data = bodo.rebalance(data, dests=list(gpu_ranks), parallel=True)
    else:
        data = bodo.rebalance(data, parallel=True)
    return data
