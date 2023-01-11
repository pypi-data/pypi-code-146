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
        flyg__omh = state
        mcjnn__ftr = inspect.getsourcelines(flyg__omh)[0][0]
        assert mcjnn__ftr.startswith('@bodo.jit') or mcjnn__ftr.startswith(
            '@jit')
        ycmk__ibq = eval(mcjnn__ftr[1:])
        self.dispatcher = ycmk__ibq(flyg__omh)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    hxj__ikm = MPI.COMM_WORLD
    while True:
        qqqq__twzom = hxj__ikm.bcast(None, root=MASTER_RANK)
        if qqqq__twzom[0] == 'exec':
            flyg__omh = pickle.loads(qqqq__twzom[1])
            for iyin__zdmo, chunl__rovk in list(flyg__omh.__globals__.items()):
                if isinstance(chunl__rovk, MasterModeDispatcher):
                    flyg__omh.__globals__[iyin__zdmo] = chunl__rovk.dispatcher
            if flyg__omh.__module__ not in sys.modules:
                sys.modules[flyg__omh.__module__] = pytypes.ModuleType(
                    flyg__omh.__module__)
            mcjnn__ftr = inspect.getsourcelines(flyg__omh)[0][0]
            assert mcjnn__ftr.startswith('@bodo.jit') or mcjnn__ftr.startswith(
                '@jit')
            ycmk__ibq = eval(mcjnn__ftr[1:])
            func = ycmk__ibq(flyg__omh)
            jtl__qlvd = qqqq__twzom[2]
            tav__megb = qqqq__twzom[3]
            jeha__pjos = []
            for ntkus__eos in jtl__qlvd:
                if ntkus__eos == 'scatter':
                    jeha__pjos.append(bodo.scatterv(None))
                elif ntkus__eos == 'bcast':
                    jeha__pjos.append(hxj__ikm.bcast(None, root=MASTER_RANK))
            aauu__hanrz = {}
            for argname, ntkus__eos in tav__megb.items():
                if ntkus__eos == 'scatter':
                    aauu__hanrz[argname] = bodo.scatterv(None)
                elif ntkus__eos == 'bcast':
                    aauu__hanrz[argname] = hxj__ikm.bcast(None, root=
                        MASTER_RANK)
            ldqjx__gyt = func(*jeha__pjos, **aauu__hanrz)
            if ldqjx__gyt is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(ldqjx__gyt)
            del (qqqq__twzom, flyg__omh, func, ycmk__ibq, jtl__qlvd,
                tav__megb, jeha__pjos, aauu__hanrz, ldqjx__gyt)
            gc.collect()
        elif qqqq__twzom[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    hxj__ikm = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        jtl__qlvd = ['scatter' for vurt__bgd in range(len(args))]
        tav__megb = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        xlxut__tdd = func.py_func.__code__.co_varnames
        jvvz__uezu = func.targetoptions

        def get_distribution(argname):
            if argname in jvvz__uezu.get('distributed', []
                ) or argname in jvvz__uezu.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        jtl__qlvd = [get_distribution(argname) for argname in xlxut__tdd[:
            len(args)]]
        tav__megb = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    dmfpb__tzucm = pickle.dumps(func.py_func)
    hxj__ikm.bcast(['exec', dmfpb__tzucm, jtl__qlvd, tav__megb])
    jeha__pjos = []
    for xdx__zmb, ntkus__eos in zip(args, jtl__qlvd):
        if ntkus__eos == 'scatter':
            jeha__pjos.append(bodo.scatterv(xdx__zmb))
        elif ntkus__eos == 'bcast':
            hxj__ikm.bcast(xdx__zmb)
            jeha__pjos.append(xdx__zmb)
    aauu__hanrz = {}
    for argname, xdx__zmb in kwargs.items():
        ntkus__eos = tav__megb[argname]
        if ntkus__eos == 'scatter':
            aauu__hanrz[argname] = bodo.scatterv(xdx__zmb)
        elif ntkus__eos == 'bcast':
            hxj__ikm.bcast(xdx__zmb)
            aauu__hanrz[argname] = xdx__zmb
    dvvrn__eer = []
    for iyin__zdmo, chunl__rovk in list(func.py_func.__globals__.items()):
        if isinstance(chunl__rovk, MasterModeDispatcher):
            dvvrn__eer.append((func.py_func.__globals__, iyin__zdmo, func.
                py_func.__globals__[iyin__zdmo]))
            func.py_func.__globals__[iyin__zdmo] = chunl__rovk.dispatcher
    ldqjx__gyt = func(*jeha__pjos, **aauu__hanrz)
    for hjtqg__novho, iyin__zdmo, chunl__rovk in dvvrn__eer:
        hjtqg__novho[iyin__zdmo] = chunl__rovk
    if ldqjx__gyt is not None and func.overloads[func.signatures[0]].metadata[
        'is_return_distributed']:
        ldqjx__gyt = bodo.gatherv(ldqjx__gyt)
    return ldqjx__gyt


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
