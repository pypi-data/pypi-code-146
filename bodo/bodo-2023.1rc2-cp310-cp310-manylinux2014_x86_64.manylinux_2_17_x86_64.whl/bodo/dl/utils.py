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
    sip__dqcz = MPI.COMM_WORLD
    stegp__jtq = sip__dqcz.Get_rank()
    axou__pcexk = get_host_ranks()
    jeb__yqcz = get_nodes_first_ranks()
    if stegp__jtq in jeb__yqcz:
        try:
            lpd__rms = get_num_gpus(framework)
        except Exception as cogz__cwcw:
            lpd__rms = cogz__cwcw
        atcu__bhhr = create_subcomm_mpi4py(jeb__yqcz)
        hnlw__wode = atcu__bhhr.gather(lpd__rms)
        if stegp__jtq == 0:
            gpu_ranks = []
            sdjk__sxj = None
            for toy__skr, eei__ato in enumerate(axou__pcexk.values()):
                vgg__fxdi = hnlw__wode[toy__skr]
                if isinstance(vgg__fxdi, Exception):
                    sdjk__sxj = vgg__fxdi
                    break
                if vgg__fxdi == 0:
                    continue
                zfxq__rbtey = len(eei__ato) // vgg__fxdi
                for fxhhg__jooao, uuae__vbyu in enumerate(eei__ato):
                    if fxhhg__jooao % zfxq__rbtey == 0:
                        czxfs__bdh = fxhhg__jooao / zfxq__rbtey
                        if czxfs__bdh < vgg__fxdi:
                            gpu_ranks.append(uuae__vbyu)
            if sdjk__sxj:
                sip__dqcz.bcast(sdjk__sxj)
                raise sdjk__sxj
            else:
                sip__dqcz.bcast(gpu_ranks)
    if stegp__jtq != 0:
        gpu_ranks = sip__dqcz.bcast(None)
        if isinstance(gpu_ranks, Exception):
            cogz__cwcw = gpu_ranks
            raise cogz__cwcw
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
    zhlr__zzuzn = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        atcu__bhhr = MPI.COMM_WORLD.Split(color=0 if zhlr__zzuzn in
            gpu_ranks else MPI.UNDEFINED, key=zhlr__zzuzn)
        if atcu__bhhr != MPI.COMM_NULL:
            hvd.init(comm=atcu__bhhr)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                ebvhi__emdw = tf.config.experimental.list_physical_devices(
                    'GPU')
                for epjih__mkgl in ebvhi__emdw:
                    tf.config.experimental.set_memory_growth(epjih__mkgl, True)
                tf.config.experimental.set_visible_devices(ebvhi__emdw[hvd.
                    local_rank()], 'GPU')
    else:
        if zhlr__zzuzn == 0:
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
        pskw__sef = 17
        sip__dqcz = MPI.COMM_WORLD
        bgvj__zepko = MPI.Get_processor_name()
        kmin__sgpm = get_host_ranks()[bgvj__zepko]
        assert_dl_initialized()
        if bodo.get_rank() == kmin__sgpm[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for stegp__jtq in kmin__sgpm[1:]:
                sip__dqcz.isend(1, dest=stegp__jtq, tag=pskw__sef)
        else:
            while True:
                hpzl__yvboa = MPI.Status()
                nhgg__zerr = sip__dqcz.Iprobe(MPI.ANY_SOURCE, MPI.ANY_TAG,
                    hpzl__yvboa)
                if nhgg__zerr:
                    assert hpzl__yvboa.source == kmin__sgpm[0]
                    assert hpzl__yvboa.tag == pskw__sef
                    sip__dqcz.recv(source=0, tag=pskw__sef)
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
