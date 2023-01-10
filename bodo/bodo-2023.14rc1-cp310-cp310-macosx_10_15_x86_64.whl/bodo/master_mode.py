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
        vdg__iuw = state
        eoaks__hwpxc = inspect.getsourcelines(vdg__iuw)[0][0]
        assert eoaks__hwpxc.startswith('@bodo.jit') or eoaks__hwpxc.startswith(
            '@jit')
        jpl__emnl = eval(eoaks__hwpxc[1:])
        self.dispatcher = jpl__emnl(vdg__iuw)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    vlruc__iex = MPI.COMM_WORLD
    while True:
        anq__ywzzi = vlruc__iex.bcast(None, root=MASTER_RANK)
        if anq__ywzzi[0] == 'exec':
            vdg__iuw = pickle.loads(anq__ywzzi[1])
            for mlvp__tksj, hhwa__hvpda in list(vdg__iuw.__globals__.items()):
                if isinstance(hhwa__hvpda, MasterModeDispatcher):
                    vdg__iuw.__globals__[mlvp__tksj] = hhwa__hvpda.dispatcher
            if vdg__iuw.__module__ not in sys.modules:
                sys.modules[vdg__iuw.__module__] = pytypes.ModuleType(vdg__iuw
                    .__module__)
            eoaks__hwpxc = inspect.getsourcelines(vdg__iuw)[0][0]
            assert eoaks__hwpxc.startswith('@bodo.jit'
                ) or eoaks__hwpxc.startswith('@jit')
            jpl__emnl = eval(eoaks__hwpxc[1:])
            func = jpl__emnl(vdg__iuw)
            rsu__roh = anq__ywzzi[2]
            sges__ibhsu = anq__ywzzi[3]
            kaic__uskh = []
            for buidr__kcw in rsu__roh:
                if buidr__kcw == 'scatter':
                    kaic__uskh.append(bodo.scatterv(None))
                elif buidr__kcw == 'bcast':
                    kaic__uskh.append(vlruc__iex.bcast(None, root=MASTER_RANK))
            toqum__pzv = {}
            for argname, buidr__kcw in sges__ibhsu.items():
                if buidr__kcw == 'scatter':
                    toqum__pzv[argname] = bodo.scatterv(None)
                elif buidr__kcw == 'bcast':
                    toqum__pzv[argname] = vlruc__iex.bcast(None, root=
                        MASTER_RANK)
            qqyp__lust = func(*kaic__uskh, **toqum__pzv)
            if qqyp__lust is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(qqyp__lust)
            del (anq__ywzzi, vdg__iuw, func, jpl__emnl, rsu__roh,
                sges__ibhsu, kaic__uskh, toqum__pzv, qqyp__lust)
            gc.collect()
        elif anq__ywzzi[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    vlruc__iex = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        rsu__roh = ['scatter' for zbbux__wnqxx in range(len(args))]
        sges__ibhsu = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        yod__javd = func.py_func.__code__.co_varnames
        nzch__jdbgn = func.targetoptions

        def get_distribution(argname):
            if argname in nzch__jdbgn.get('distributed', []
                ) or argname in nzch__jdbgn.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        rsu__roh = [get_distribution(argname) for argname in yod__javd[:len
            (args)]]
        sges__ibhsu = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    mok__isk = pickle.dumps(func.py_func)
    vlruc__iex.bcast(['exec', mok__isk, rsu__roh, sges__ibhsu])
    kaic__uskh = []
    for rzohi__kjsoe, buidr__kcw in zip(args, rsu__roh):
        if buidr__kcw == 'scatter':
            kaic__uskh.append(bodo.scatterv(rzohi__kjsoe))
        elif buidr__kcw == 'bcast':
            vlruc__iex.bcast(rzohi__kjsoe)
            kaic__uskh.append(rzohi__kjsoe)
    toqum__pzv = {}
    for argname, rzohi__kjsoe in kwargs.items():
        buidr__kcw = sges__ibhsu[argname]
        if buidr__kcw == 'scatter':
            toqum__pzv[argname] = bodo.scatterv(rzohi__kjsoe)
        elif buidr__kcw == 'bcast':
            vlruc__iex.bcast(rzohi__kjsoe)
            toqum__pzv[argname] = rzohi__kjsoe
    umeb__usvn = []
    for mlvp__tksj, hhwa__hvpda in list(func.py_func.__globals__.items()):
        if isinstance(hhwa__hvpda, MasterModeDispatcher):
            umeb__usvn.append((func.py_func.__globals__, mlvp__tksj, func.
                py_func.__globals__[mlvp__tksj]))
            func.py_func.__globals__[mlvp__tksj] = hhwa__hvpda.dispatcher
    qqyp__lust = func(*kaic__uskh, **toqum__pzv)
    for dkxtp__ckl, mlvp__tksj, hhwa__hvpda in umeb__usvn:
        dkxtp__ckl[mlvp__tksj] = hhwa__hvpda
    if qqyp__lust is not None and func.overloads[func.signatures[0]].metadata[
        'is_return_distributed']:
        qqyp__lust = bodo.gatherv(qqyp__lust)
    return qqyp__lust


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
