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
        viind__yoqn = state
        vyk__jlyvx = inspect.getsourcelines(viind__yoqn)[0][0]
        assert vyk__jlyvx.startswith('@bodo.jit') or vyk__jlyvx.startswith(
            '@jit')
        vtzue__rrnxi = eval(vyk__jlyvx[1:])
        self.dispatcher = vtzue__rrnxi(viind__yoqn)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    xyjuk__hhli = MPI.COMM_WORLD
    while True:
        pueoe__afd = xyjuk__hhli.bcast(None, root=MASTER_RANK)
        if pueoe__afd[0] == 'exec':
            viind__yoqn = pickle.loads(pueoe__afd[1])
            for cma__jxo, udt__rms in list(viind__yoqn.__globals__.items()):
                if isinstance(udt__rms, MasterModeDispatcher):
                    viind__yoqn.__globals__[cma__jxo] = udt__rms.dispatcher
            if viind__yoqn.__module__ not in sys.modules:
                sys.modules[viind__yoqn.__module__] = pytypes.ModuleType(
                    viind__yoqn.__module__)
            vyk__jlyvx = inspect.getsourcelines(viind__yoqn)[0][0]
            assert vyk__jlyvx.startswith('@bodo.jit') or vyk__jlyvx.startswith(
                '@jit')
            vtzue__rrnxi = eval(vyk__jlyvx[1:])
            func = vtzue__rrnxi(viind__yoqn)
            pycn__nxzc = pueoe__afd[2]
            jmqs__tgvz = pueoe__afd[3]
            hucbg__bewdf = []
            for xhwmx__opcd in pycn__nxzc:
                if xhwmx__opcd == 'scatter':
                    hucbg__bewdf.append(bodo.scatterv(None))
                elif xhwmx__opcd == 'bcast':
                    hucbg__bewdf.append(xyjuk__hhli.bcast(None, root=
                        MASTER_RANK))
            mtjxu__tqtds = {}
            for argname, xhwmx__opcd in jmqs__tgvz.items():
                if xhwmx__opcd == 'scatter':
                    mtjxu__tqtds[argname] = bodo.scatterv(None)
                elif xhwmx__opcd == 'bcast':
                    mtjxu__tqtds[argname] = xyjuk__hhli.bcast(None, root=
                        MASTER_RANK)
            ldwxf__jeamt = func(*hucbg__bewdf, **mtjxu__tqtds)
            if ldwxf__jeamt is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(ldwxf__jeamt)
            del (pueoe__afd, viind__yoqn, func, vtzue__rrnxi, pycn__nxzc,
                jmqs__tgvz, hucbg__bewdf, mtjxu__tqtds, ldwxf__jeamt)
            gc.collect()
        elif pueoe__afd[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    xyjuk__hhli = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        pycn__nxzc = ['scatter' for xiglh__xtahp in range(len(args))]
        jmqs__tgvz = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        kthf__kkm = func.py_func.__code__.co_varnames
        fvuw__ikr = func.targetoptions

        def get_distribution(argname):
            if argname in fvuw__ikr.get('distributed', []
                ) or argname in fvuw__ikr.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        pycn__nxzc = [get_distribution(argname) for argname in kthf__kkm[:
            len(args)]]
        jmqs__tgvz = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    ebuox__zibow = pickle.dumps(func.py_func)
    xyjuk__hhli.bcast(['exec', ebuox__zibow, pycn__nxzc, jmqs__tgvz])
    hucbg__bewdf = []
    for atsle__ulat, xhwmx__opcd in zip(args, pycn__nxzc):
        if xhwmx__opcd == 'scatter':
            hucbg__bewdf.append(bodo.scatterv(atsle__ulat))
        elif xhwmx__opcd == 'bcast':
            xyjuk__hhli.bcast(atsle__ulat)
            hucbg__bewdf.append(atsle__ulat)
    mtjxu__tqtds = {}
    for argname, atsle__ulat in kwargs.items():
        xhwmx__opcd = jmqs__tgvz[argname]
        if xhwmx__opcd == 'scatter':
            mtjxu__tqtds[argname] = bodo.scatterv(atsle__ulat)
        elif xhwmx__opcd == 'bcast':
            xyjuk__hhli.bcast(atsle__ulat)
            mtjxu__tqtds[argname] = atsle__ulat
    yivms__iznf = []
    for cma__jxo, udt__rms in list(func.py_func.__globals__.items()):
        if isinstance(udt__rms, MasterModeDispatcher):
            yivms__iznf.append((func.py_func.__globals__, cma__jxo, func.
                py_func.__globals__[cma__jxo]))
            func.py_func.__globals__[cma__jxo] = udt__rms.dispatcher
    ldwxf__jeamt = func(*hucbg__bewdf, **mtjxu__tqtds)
    for pqtfi__qks, cma__jxo, udt__rms in yivms__iznf:
        pqtfi__qks[cma__jxo] = udt__rms
    if ldwxf__jeamt is not None and func.overloads[func.signatures[0]
        ].metadata['is_return_distributed']:
        ldwxf__jeamt = bodo.gatherv(ldwxf__jeamt)
    return ldwxf__jeamt


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
