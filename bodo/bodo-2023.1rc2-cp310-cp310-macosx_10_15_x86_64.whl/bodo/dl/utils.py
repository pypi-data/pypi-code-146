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
    qec__aes = MPI.COMM_WORLD
    rgwn__cfi = qec__aes.Get_rank()
    uwz__wzogc = get_host_ranks()
    oiw__njb = get_nodes_first_ranks()
    if rgwn__cfi in oiw__njb:
        try:
            fret__fcrkt = get_num_gpus(framework)
        except Exception as hpvs__zrkb:
            fret__fcrkt = hpvs__zrkb
        ejqq__xhove = create_subcomm_mpi4py(oiw__njb)
        wuks__uwa = ejqq__xhove.gather(fret__fcrkt)
        if rgwn__cfi == 0:
            gpu_ranks = []
            rhdyc__raq = None
            for bczzv__kbwbv, ezxt__iipj in enumerate(uwz__wzogc.values()):
                lvq__pgg = wuks__uwa[bczzv__kbwbv]
                if isinstance(lvq__pgg, Exception):
                    rhdyc__raq = lvq__pgg
                    break
                if lvq__pgg == 0:
                    continue
                jweq__etv = len(ezxt__iipj) // lvq__pgg
                for rukej__gouas, myvw__ahvhf in enumerate(ezxt__iipj):
                    if rukej__gouas % jweq__etv == 0:
                        ggbw__wms = rukej__gouas / jweq__etv
                        if ggbw__wms < lvq__pgg:
                            gpu_ranks.append(myvw__ahvhf)
            if rhdyc__raq:
                qec__aes.bcast(rhdyc__raq)
                raise rhdyc__raq
            else:
                qec__aes.bcast(gpu_ranks)
    if rgwn__cfi != 0:
        gpu_ranks = qec__aes.bcast(None)
        if isinstance(gpu_ranks, Exception):
            hpvs__zrkb = gpu_ranks
            raise hpvs__zrkb
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
    ymx__nozuo = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        ejqq__xhove = MPI.COMM_WORLD.Split(color=0 if ymx__nozuo in
            gpu_ranks else MPI.UNDEFINED, key=ymx__nozuo)
        if ejqq__xhove != MPI.COMM_NULL:
            hvd.init(comm=ejqq__xhove)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                ndu__luvy = tf.config.experimental.list_physical_devices('GPU')
                for cfv__bza in ndu__luvy:
                    tf.config.experimental.set_memory_growth(cfv__bza, True)
                tf.config.experimental.set_visible_devices(ndu__luvy[hvd.
                    local_rank()], 'GPU')
    else:
        if ymx__nozuo == 0:
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
        bgjxz__wrct = 17
        qec__aes = MPI.COMM_WORLD
        mcez__zuqjp = MPI.Get_processor_name()
        xisg__rnlcv = get_host_ranks()[mcez__zuqjp]
        assert_dl_initialized()
        if bodo.get_rank() == xisg__rnlcv[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for rgwn__cfi in xisg__rnlcv[1:]:
                qec__aes.isend(1, dest=rgwn__cfi, tag=bgjxz__wrct)
        else:
            while True:
                yfvn__rhtl = MPI.Status()
                qna__igw = qec__aes.Iprobe(MPI.ANY_SOURCE, MPI.ANY_TAG,
                    yfvn__rhtl)
                if qna__igw:
                    assert yfvn__rhtl.source == xisg__rnlcv[0]
                    assert yfvn__rhtl.tag == bgjxz__wrct
                    qec__aes.recv(source=0, tag=bgjxz__wrct)
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
