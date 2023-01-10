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
    hgbgg__muru = MPI.COMM_WORLD
    yeh__olxem = hgbgg__muru.Get_rank()
    sycio__nnyi = get_host_ranks()
    lxsq__nmqf = get_nodes_first_ranks()
    if yeh__olxem in lxsq__nmqf:
        try:
            jqnk__bdiud = get_num_gpus(framework)
        except Exception as vpnzh__zybgr:
            jqnk__bdiud = vpnzh__zybgr
        ppjlq__ndbb = create_subcomm_mpi4py(lxsq__nmqf)
        szmr__ygcr = ppjlq__ndbb.gather(jqnk__bdiud)
        if yeh__olxem == 0:
            gpu_ranks = []
            ptemi__xfm = None
            for nybm__lbfsr, ddxsg__gua in enumerate(sycio__nnyi.values()):
                ngf__szqhi = szmr__ygcr[nybm__lbfsr]
                if isinstance(ngf__szqhi, Exception):
                    ptemi__xfm = ngf__szqhi
                    break
                if ngf__szqhi == 0:
                    continue
                mxqr__vnbfu = len(ddxsg__gua) // ngf__szqhi
                for ytpy__ljw, fts__irnt in enumerate(ddxsg__gua):
                    if ytpy__ljw % mxqr__vnbfu == 0:
                        xbgtl__zrhgl = ytpy__ljw / mxqr__vnbfu
                        if xbgtl__zrhgl < ngf__szqhi:
                            gpu_ranks.append(fts__irnt)
            if ptemi__xfm:
                hgbgg__muru.bcast(ptemi__xfm)
                raise ptemi__xfm
            else:
                hgbgg__muru.bcast(gpu_ranks)
    if yeh__olxem != 0:
        gpu_ranks = hgbgg__muru.bcast(None)
        if isinstance(gpu_ranks, Exception):
            vpnzh__zybgr = gpu_ranks
            raise vpnzh__zybgr
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
    oeffv__fhpc = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        ppjlq__ndbb = MPI.COMM_WORLD.Split(color=0 if oeffv__fhpc in
            gpu_ranks else MPI.UNDEFINED, key=oeffv__fhpc)
        if ppjlq__ndbb != MPI.COMM_NULL:
            hvd.init(comm=ppjlq__ndbb)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                avdb__ttfwr = tf.config.experimental.list_physical_devices(
                    'GPU')
                for trf__xzeg in avdb__ttfwr:
                    tf.config.experimental.set_memory_growth(trf__xzeg, True)
                tf.config.experimental.set_visible_devices(avdb__ttfwr[hvd.
                    local_rank()], 'GPU')
    else:
        if oeffv__fhpc == 0:
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
        owheh__veo = 17
        hgbgg__muru = MPI.COMM_WORLD
        gsm__zgv = MPI.Get_processor_name()
        pbe__bvgiw = get_host_ranks()[gsm__zgv]
        assert_dl_initialized()
        if bodo.get_rank() == pbe__bvgiw[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for yeh__olxem in pbe__bvgiw[1:]:
                hgbgg__muru.isend(1, dest=yeh__olxem, tag=owheh__veo)
        else:
            while True:
                dzv__xmyp = MPI.Status()
                nwx__dhnmc = hgbgg__muru.Iprobe(MPI.ANY_SOURCE, MPI.ANY_TAG,
                    dzv__xmyp)
                if nwx__dhnmc:
                    assert dzv__xmyp.source == pbe__bvgiw[0]
                    assert dzv__xmyp.tag == owheh__veo
                    hgbgg__muru.recv(source=0, tag=owheh__veo)
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
