import gc
import inspect
import sys
import types as pytypes
import bodo
master_mode_on = False
MASTER_RANK = 0


class MasterModeDispatcher(object):

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def __call__(self, *args, **kwargs):
        assert bodo.get_rank() == MASTER_RANK
        return master_wrapper(self.dispatcher, *args, **kwargs)

    def __getstate__(self):
        assert bodo.get_rank() == MASTER_RANK
        return self.dispatcher.py_func

    def __setstate__(self, state):
        assert bodo.get_rank() != MASTER_RANK
        dwu__meg = state
        tyu__rfyna = inspect.getsourcelines(dwu__meg)[0][0]
        assert tyu__rfyna.startswith('@bodo.jit') or tyu__rfyna.startswith(
            '@jit')
        uvnni__bifr = eval(tyu__rfyna[1:])
        self.dispatcher = uvnni__bifr(dwu__meg)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    lmuyj__mjzeg = MPI.COMM_WORLD
    while True:
        anh__hvk = lmuyj__mjzeg.bcast(None, root=MASTER_RANK)
        if anh__hvk[0] == 'exec':
            dwu__meg = pickle.loads(anh__hvk[1])
            for xyzs__hcv, dddof__ytzex in list(dwu__meg.__globals__.items()):
                if isinstance(dddof__ytzex, MasterModeDispatcher):
                    dwu__meg.__globals__[xyzs__hcv] = dddof__ytzex.dispatcher
            if dwu__meg.__module__ not in sys.modules:
                sys.modules[dwu__meg.__module__] = pytypes.ModuleType(dwu__meg
                    .__module__)
            tyu__rfyna = inspect.getsourcelines(dwu__meg)[0][0]
            assert tyu__rfyna.startswith('@bodo.jit') or tyu__rfyna.startswith(
                '@jit')
            uvnni__bifr = eval(tyu__rfyna[1:])
            func = uvnni__bifr(dwu__meg)
            stsu__cyttx = anh__hvk[2]
            ohkkd__lqj = anh__hvk[3]
            teo__mto = []
            for ypvya__zijg in stsu__cyttx:
                if ypvya__zijg == 'scatter':
                    teo__mto.append(bodo.scatterv(None))
                elif ypvya__zijg == 'bcast':
                    teo__mto.append(lmuyj__mjzeg.bcast(None, root=MASTER_RANK))
            hidim__ysfz = {}
            for argname, ypvya__zijg in ohkkd__lqj.items():
                if ypvya__zijg == 'scatter':
                    hidim__ysfz[argname] = bodo.scatterv(None)
                elif ypvya__zijg == 'bcast':
                    hidim__ysfz[argname] = lmuyj__mjzeg.bcast(None, root=
                        MASTER_RANK)
            buyb__jowf = func(*teo__mto, **hidim__ysfz)
            if buyb__jowf is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(buyb__jowf)
            del (anh__hvk, dwu__meg, func, uvnni__bifr, stsu__cyttx,
                ohkkd__lqj, teo__mto, hidim__ysfz, buyb__jowf)
            gc.collect()
        elif anh__hvk[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    lmuyj__mjzeg = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        stsu__cyttx = ['scatter' for jdvyl__qdbwo in range(len(args))]
        ohkkd__lqj = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        tku__moehd = func.py_func.__code__.co_varnames
        vnj__qjc = func.targetoptions

        def get_distribution(argname):
            if argname in vnj__qjc.get('distributed', []
                ) or argname in vnj__qjc.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        stsu__cyttx = [get_distribution(argname) for argname in tku__moehd[
            :len(args)]]
        ohkkd__lqj = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    bijgq__fsmh = pickle.dumps(func.py_func)
    lmuyj__mjzeg.bcast(['exec', bijgq__fsmh, stsu__cyttx, ohkkd__lqj])
    teo__mto = []
    for poki__vcc, ypvya__zijg in zip(args, stsu__cyttx):
        if ypvya__zijg == 'scatter':
            teo__mto.append(bodo.scatterv(poki__vcc))
        elif ypvya__zijg == 'bcast':
            lmuyj__mjzeg.bcast(poki__vcc)
            teo__mto.append(poki__vcc)
    hidim__ysfz = {}
    for argname, poki__vcc in kwargs.items():
        ypvya__zijg = ohkkd__lqj[argname]
        if ypvya__zijg == 'scatter':
            hidim__ysfz[argname] = bodo.scatterv(poki__vcc)
        elif ypvya__zijg == 'bcast':
            lmuyj__mjzeg.bcast(poki__vcc)
            hidim__ysfz[argname] = poki__vcc
    nzml__eevjp = []
    for xyzs__hcv, dddof__ytzex in list(func.py_func.__globals__.items()):
        if isinstance(dddof__ytzex, MasterModeDispatcher):
            nzml__eevjp.append((func.py_func.__globals__, xyzs__hcv, func.
                py_func.__globals__[xyzs__hcv]))
            func.py_func.__globals__[xyzs__hcv] = dddof__ytzex.dispatcher
    buyb__jowf = func(*teo__mto, **hidim__ysfz)
    for qmvzc__tlj, xyzs__hcv, dddof__ytzex in nzml__eevjp:
        qmvzc__tlj[xyzs__hcv] = dddof__ytzex
    if buyb__jowf is not None and func.overloads[func.signatures[0]].metadata[
        'is_return_distributed']:
        buyb__jowf = bodo.gatherv(buyb__jowf)
    return buyb__jowf


def init_master_mode():
    if bodo.get_size() == 1:
        return
    global master_mode_on
    assert master_mode_on is False, 'init_master_mode can only be called once on each process'
    master_mode_on = True
    assert sys.version_info[:2] >= (3, 8
        ), 'Python 3.8+ required for master mode'
    from bodo import jit
    globals()['jit'] = jit
    import cloudpickle
    from mpi4py import MPI
    globals()['pickle'] = cloudpickle
    globals()['MPI'] = MPI

    def master_exit():
        MPI.COMM_WORLD.bcast(['exit'])
    if bodo.get_rank() == MASTER_RANK:
        import atexit
        atexit.register(master_exit)
    else:
        worker_loop()
