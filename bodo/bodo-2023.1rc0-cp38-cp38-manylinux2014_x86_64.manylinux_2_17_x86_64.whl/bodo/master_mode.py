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
        vqpd__stt = state
        vso__pifkw = inspect.getsourcelines(vqpd__stt)[0][0]
        assert vso__pifkw.startswith('@bodo.jit') or vso__pifkw.startswith(
            '@jit')
        vsbfe__cms = eval(vso__pifkw[1:])
        self.dispatcher = vsbfe__cms(vqpd__stt)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    gttt__ugoic = MPI.COMM_WORLD
    while True:
        nok__gklys = gttt__ugoic.bcast(None, root=MASTER_RANK)
        if nok__gklys[0] == 'exec':
            vqpd__stt = pickle.loads(nok__gklys[1])
            for atwed__cobhq, yblkm__tacq in list(vqpd__stt.__globals__.items()
                ):
                if isinstance(yblkm__tacq, MasterModeDispatcher):
                    vqpd__stt.__globals__[atwed__cobhq
                        ] = yblkm__tacq.dispatcher
            if vqpd__stt.__module__ not in sys.modules:
                sys.modules[vqpd__stt.__module__] = pytypes.ModuleType(
                    vqpd__stt.__module__)
            vso__pifkw = inspect.getsourcelines(vqpd__stt)[0][0]
            assert vso__pifkw.startswith('@bodo.jit') or vso__pifkw.startswith(
                '@jit')
            vsbfe__cms = eval(vso__pifkw[1:])
            func = vsbfe__cms(vqpd__stt)
            lpife__zzmof = nok__gklys[2]
            ubrfk__knmvq = nok__gklys[3]
            jcko__aix = []
            for hrn__vhg in lpife__zzmof:
                if hrn__vhg == 'scatter':
                    jcko__aix.append(bodo.scatterv(None))
                elif hrn__vhg == 'bcast':
                    jcko__aix.append(gttt__ugoic.bcast(None, root=MASTER_RANK))
            pkd__elp = {}
            for argname, hrn__vhg in ubrfk__knmvq.items():
                if hrn__vhg == 'scatter':
                    pkd__elp[argname] = bodo.scatterv(None)
                elif hrn__vhg == 'bcast':
                    pkd__elp[argname] = gttt__ugoic.bcast(None, root=
                        MASTER_RANK)
            thcru__ybgae = func(*jcko__aix, **pkd__elp)
            if thcru__ybgae is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(thcru__ybgae)
            del (nok__gklys, vqpd__stt, func, vsbfe__cms, lpife__zzmof,
                ubrfk__knmvq, jcko__aix, pkd__elp, thcru__ybgae)
            gc.collect()
        elif nok__gklys[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    gttt__ugoic = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        lpife__zzmof = ['scatter' for hqy__mgojt in range(len(args))]
        ubrfk__knmvq = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        nhc__qsen = func.py_func.__code__.co_varnames
        bxk__btwe = func.targetoptions

        def get_distribution(argname):
            if argname in bxk__btwe.get('distributed', []
                ) or argname in bxk__btwe.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        lpife__zzmof = [get_distribution(argname) for argname in nhc__qsen[
            :len(args)]]
        ubrfk__knmvq = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    dgbqj__izcd = pickle.dumps(func.py_func)
    gttt__ugoic.bcast(['exec', dgbqj__izcd, lpife__zzmof, ubrfk__knmvq])
    jcko__aix = []
    for iahix__aear, hrn__vhg in zip(args, lpife__zzmof):
        if hrn__vhg == 'scatter':
            jcko__aix.append(bodo.scatterv(iahix__aear))
        elif hrn__vhg == 'bcast':
            gttt__ugoic.bcast(iahix__aear)
            jcko__aix.append(iahix__aear)
    pkd__elp = {}
    for argname, iahix__aear in kwargs.items():
        hrn__vhg = ubrfk__knmvq[argname]
        if hrn__vhg == 'scatter':
            pkd__elp[argname] = bodo.scatterv(iahix__aear)
        elif hrn__vhg == 'bcast':
            gttt__ugoic.bcast(iahix__aear)
            pkd__elp[argname] = iahix__aear
    vwjg__scbe = []
    for atwed__cobhq, yblkm__tacq in list(func.py_func.__globals__.items()):
        if isinstance(yblkm__tacq, MasterModeDispatcher):
            vwjg__scbe.append((func.py_func.__globals__, atwed__cobhq, func
                .py_func.__globals__[atwed__cobhq]))
            func.py_func.__globals__[atwed__cobhq] = yblkm__tacq.dispatcher
    thcru__ybgae = func(*jcko__aix, **pkd__elp)
    for lbvdr__bot, atwed__cobhq, yblkm__tacq in vwjg__scbe:
        lbvdr__bot[atwed__cobhq] = yblkm__tacq
    if thcru__ybgae is not None and func.overloads[func.signatures[0]
        ].metadata['is_return_distributed']:
        thcru__ybgae = bodo.gatherv(thcru__ybgae)
    return thcru__ybgae


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
