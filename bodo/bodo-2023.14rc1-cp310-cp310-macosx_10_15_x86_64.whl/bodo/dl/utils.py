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
    ysofb__slw = MPI.COMM_WORLD
    bvg__xrvy = ysofb__slw.Get_rank()
    etwb__cpd = get_host_ranks()
    ykdsa__xwkil = get_nodes_first_ranks()
    if bvg__xrvy in ykdsa__xwkil:
        try:
            cqkn__mdb = get_num_gpus(framework)
        except Exception as klihk__efw:
            cqkn__mdb = klihk__efw
        mbgop__wyva = create_subcomm_mpi4py(ykdsa__xwkil)
        paz__vqjs = mbgop__wyva.gather(cqkn__mdb)
        if bvg__xrvy == 0:
            gpu_ranks = []
            xjda__qxzi = None
            for zuw__zrld, xfzf__rla in enumerate(etwb__cpd.values()):
                yjxfj__ncxac = paz__vqjs[zuw__zrld]
                if isinstance(yjxfj__ncxac, Exception):
                    xjda__qxzi = yjxfj__ncxac
                    break
                if yjxfj__ncxac == 0:
                    continue
                qdz__motx = len(xfzf__rla) // yjxfj__ncxac
                for vhmx__jhe, ibew__jqe in enumerate(xfzf__rla):
                    if vhmx__jhe % qdz__motx == 0:
                        rebaj__xbk = vhmx__jhe / qdz__motx
                        if rebaj__xbk < yjxfj__ncxac:
                            gpu_ranks.append(ibew__jqe)
            if xjda__qxzi:
                ysofb__slw.bcast(xjda__qxzi)
                raise xjda__qxzi
            else:
                ysofb__slw.bcast(gpu_ranks)
    if bvg__xrvy != 0:
        gpu_ranks = ysofb__slw.bcast(None)
        if isinstance(gpu_ranks, Exception):
            klihk__efw = gpu_ranks
            raise klihk__efw
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
    lqz__lqceu = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        mbgop__wyva = MPI.COMM_WORLD.Split(color=0 if lqz__lqceu in
            gpu_ranks else MPI.UNDEFINED, key=lqz__lqceu)
        if mbgop__wyva != MPI.COMM_NULL:
            hvd.init(comm=mbgop__wyva)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                ryn__epnas = tf.config.experimental.list_physical_devices('GPU'
                    )
                for bbf__trdi in ryn__epnas:
                    tf.config.experimental.set_memory_growth(bbf__trdi, True)
                tf.config.experimental.set_visible_devices(ryn__epnas[hvd.
                    local_rank()], 'GPU')
    else:
        if lqz__lqceu == 0:
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
        gnve__mybwm = 17
        ysofb__slw = MPI.COMM_WORLD
        cqqqc__dwd = MPI.Get_processor_name()
        nzz__pbr = get_host_ranks()[cqqqc__dwd]
        assert_dl_initialized()
        if bodo.get_rank() == nzz__pbr[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for bvg__xrvy in nzz__pbr[1:]:
                ysofb__slw.isend(1, dest=bvg__xrvy, tag=gnve__mybwm)
        else:
            while True:
                mgp__gkt = MPI.Status()
                eforb__vmm = ysofb__slw.Iprobe(MPI.ANY_SOURCE, MPI.ANY_TAG,
                    mgp__gkt)
                if eforb__vmm:
                    assert mgp__gkt.source == nzz__pbr[0]
                    assert mgp__gkt.tag == gnve__mybwm
                    ysofb__slw.recv(source=0, tag=gnve__mybwm)
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
