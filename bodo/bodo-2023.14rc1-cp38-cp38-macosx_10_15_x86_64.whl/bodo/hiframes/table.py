"""Table data type for storing dataframe column arrays. Supports storing many columns
(e.g. >10k) efficiently.
"""
import operator
from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.ir_utils import guard
from numba.core.typing.templates import signature
from numba.cpython.listobj import ListInstance
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, lower_getattr, make_attribute_wrapper, models, overload, register_model, typeof_impl, unbox
from numba.np.arrayobj import _getitem_array_single_int
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.typing import BodoError, MetaType, decode_if_dict_array, get_overload_const_int, is_list_like_index_type, is_overload_constant_bool, is_overload_constant_int, is_overload_none, is_overload_true, raise_bodo_error, to_str_arr_if_dict_array, unwrap_typeref
from bodo.utils.utils import is_whole_slice


class Table:

    def __init__(self, arrs, usecols=None, num_arrs=-1):
        if usecols is not None:
            assert num_arrs != -1, 'num_arrs must be provided if usecols is not None'
            nqlqu__ynp = 0
            mfmc__zeib = []
            for i in range(usecols[-1] + 1):
                if i == usecols[nqlqu__ynp]:
                    mfmc__zeib.append(arrs[nqlqu__ynp])
                    nqlqu__ynp += 1
                else:
                    mfmc__zeib.append(None)
            for zexw__fksjk in range(usecols[-1] + 1, num_arrs):
                mfmc__zeib.append(None)
            self.arrays = mfmc__zeib
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((xfgw__ppe == zorac__dhz).all() for xfgw__ppe,
            zorac__dhz in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        iwakz__bhze = len(self.arrays)
        otr__dsld = dict(zip(range(iwakz__bhze), self.arrays))
        df = pd.DataFrame(otr__dsld, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        kgqu__qyzed = []
        qkyg__jfik = []
        hekwy__qnbhc = {}
        nfod__qxza = {}
        qnpwe__ljh = defaultdict(int)
        zln__eqe = defaultdict(list)
        if not has_runtime_cols:
            for i, t in enumerate(arr_types):
                if t not in hekwy__qnbhc:
                    zahsy__mlt = len(hekwy__qnbhc)
                    hekwy__qnbhc[t] = zahsy__mlt
                    nfod__qxza[zahsy__mlt] = t
                exn__piu = hekwy__qnbhc[t]
                kgqu__qyzed.append(exn__piu)
                qkyg__jfik.append(qnpwe__ljh[exn__piu])
                qnpwe__ljh[exn__piu] += 1
                zln__eqe[exn__piu].append(i)
        self.block_nums = kgqu__qyzed
        self.block_offsets = qkyg__jfik
        self.type_to_blk = hekwy__qnbhc
        self.blk_to_type = nfod__qxza
        self.block_to_arr_ind = zln__eqe
        super(TableType, self).__init__(name=
            f'TableType({arr_types}, {has_runtime_cols})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    @property
    def key(self):
        return self.arr_types, self.has_runtime_cols

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(Table)
def typeof_table(val, c):
    return TableType(tuple(numba.typeof(arr) for arr in val.arrays))


@register_model(TableType)
class TableTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        if fe_type.has_runtime_cols:
            qtij__sqnz = [(f'block_{i}', types.List(t)) for i, t in
                enumerate(fe_type.arr_types)]
        else:
            qtij__sqnz = [(f'block_{exn__piu}', types.List(t)) for t,
                exn__piu in fe_type.type_to_blk.items()]
        qtij__sqnz.append(('parent', types.pyobject))
        qtij__sqnz.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, qtij__sqnz)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    dnvrc__wwl = c.pyapi.object_getattr_string(val, 'arrays')
    table = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    table.parent = cgutils.get_null_value(table.parent.type)
    yrmmx__ngv = c.pyapi.make_none()
    wqaiq__acp = c.context.get_constant(types.int64, 0)
    cmti__gjy = cgutils.alloca_once_value(c.builder, wqaiq__acp)
    for t, exn__piu in typ.type_to_blk.items():
        spr__leh = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[exn__piu]))
        zexw__fksjk, evpri__ieba = ListInstance.allocate_ex(c.context, c.
            builder, types.List(t), spr__leh)
        evpri__ieba.size = spr__leh
        dphc__fvgf = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[exn__piu],
            dtype=np.int64))
        qkmn__tngql = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, dphc__fvgf)
        with cgutils.for_range(c.builder, spr__leh) as fxykj__xgod:
            i = fxykj__xgod.index
            hgwu__ztt = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), qkmn__tngql, i)
            vkf__pdc = c.pyapi.long_from_longlong(hgwu__ztt)
            zkkwr__noov = c.pyapi.object_getitem(dnvrc__wwl, vkf__pdc)
            uwiy__gwi = c.builder.icmp_unsigned('==', zkkwr__noov, yrmmx__ngv)
            with c.builder.if_else(uwiy__gwi) as (tth__jwtb, awud__bgu):
                with tth__jwtb:
                    sfamo__ltgho = c.context.get_constant_null(t)
                    evpri__ieba.inititem(i, sfamo__ltgho, incref=False)
                with awud__bgu:
                    cdkwt__crv = c.pyapi.call_method(zkkwr__noov, '__len__', ()
                        )
                    chh__ioik = c.pyapi.long_as_longlong(cdkwt__crv)
                    c.builder.store(chh__ioik, cmti__gjy)
                    c.pyapi.decref(cdkwt__crv)
                    arr = c.pyapi.to_native_value(t, zkkwr__noov).value
                    evpri__ieba.inititem(i, arr, incref=False)
            c.pyapi.decref(zkkwr__noov)
            c.pyapi.decref(vkf__pdc)
        setattr(table, f'block_{exn__piu}', evpri__ieba.value)
    table.len = c.builder.load(cmti__gjy)
    c.pyapi.decref(dnvrc__wwl)
    c.pyapi.decref(yrmmx__ngv)
    sjgqo__jorpb = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(table._getvalue(), is_error=sjgqo__jorpb)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    table = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        bis__kdi = c.context.get_constant(types.int64, 0)
        for i, t in enumerate(typ.arr_types):
            mfmc__zeib = getattr(table, f'block_{i}')
            qes__dsosz = ListInstance(c.context, c.builder, types.List(t),
                mfmc__zeib)
            bis__kdi = c.builder.add(bis__kdi, qes__dsosz.size)
        rxzlz__vvf = c.pyapi.list_new(bis__kdi)
        unkg__uelrq = c.context.get_constant(types.int64, 0)
        for i, t in enumerate(typ.arr_types):
            mfmc__zeib = getattr(table, f'block_{i}')
            qes__dsosz = ListInstance(c.context, c.builder, types.List(t),
                mfmc__zeib)
            with cgutils.for_range(c.builder, qes__dsosz.size) as fxykj__xgod:
                i = fxykj__xgod.index
                arr = qes__dsosz.getitem(i)
                c.context.nrt.incref(c.builder, t, arr)
                idx = c.builder.add(unkg__uelrq, i)
                c.pyapi.list_setitem(rxzlz__vvf, idx, c.pyapi.
                    from_native_value(t, arr, c.env_manager))
            unkg__uelrq = c.builder.add(unkg__uelrq, qes__dsosz.size)
        qzm__fwsfr = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        nrpc__skzqk = c.pyapi.call_function_objargs(qzm__fwsfr, (rxzlz__vvf,))
        c.pyapi.decref(qzm__fwsfr)
        c.pyapi.decref(rxzlz__vvf)
        c.context.nrt.decref(c.builder, typ, val)
        return nrpc__skzqk
    rxzlz__vvf = c.pyapi.list_new(c.context.get_constant(types.int64, len(
        typ.arr_types)))
    tknt__xkmrv = cgutils.is_not_null(c.builder, table.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for t, exn__piu in typ.type_to_blk.items():
        mfmc__zeib = getattr(table, f'block_{exn__piu}')
        qes__dsosz = ListInstance(c.context, c.builder, types.List(t),
            mfmc__zeib)
        dphc__fvgf = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[exn__piu],
            dtype=np.int64))
        qkmn__tngql = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, dphc__fvgf)
        with cgutils.for_range(c.builder, qes__dsosz.size) as fxykj__xgod:
            i = fxykj__xgod.index
            hgwu__ztt = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), qkmn__tngql, i)
            arr = qes__dsosz.getitem(i)
            tzx__lmfm = cgutils.alloca_once_value(c.builder, arr)
            kdy__tbfaf = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(t))
            is_null = is_ll_eq(c.builder, tzx__lmfm, kdy__tbfaf)
            with c.builder.if_else(c.builder.and_(is_null, c.builder.not_(
                ensure_unboxed))) as (tth__jwtb, awud__bgu):
                with tth__jwtb:
                    yrmmx__ngv = c.pyapi.make_none()
                    c.pyapi.list_setitem(rxzlz__vvf, hgwu__ztt, yrmmx__ngv)
                with awud__bgu:
                    zkkwr__noov = cgutils.alloca_once(c.builder, c.context.
                        get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(is_null, tknt__xkmrv)
                        ) as (pjq__dfiey, emmnp__tere):
                        with pjq__dfiey:
                            gci__eyxfz = get_df_obj_column_codegen(c.
                                context, c.builder, c.pyapi, table.parent,
                                hgwu__ztt, t)
                            c.builder.store(gci__eyxfz, zkkwr__noov)
                        with emmnp__tere:
                            c.context.nrt.incref(c.builder, t, arr)
                            c.builder.store(c.pyapi.from_native_value(t,
                                arr, c.env_manager), zkkwr__noov)
                    c.pyapi.list_setitem(rxzlz__vvf, hgwu__ztt, c.builder.
                        load(zkkwr__noov))
    qzm__fwsfr = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    nrpc__skzqk = c.pyapi.call_function_objargs(qzm__fwsfr, (rxzlz__vvf,))
    c.pyapi.decref(qzm__fwsfr)
    c.pyapi.decref(rxzlz__vvf)
    c.context.nrt.decref(c.builder, typ, val)
    return nrpc__skzqk


@lower_builtin(len, TableType)
def table_len_lower(context, builder, sig, args):
    impl = table_len_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def table_len_overload(T):
    if not isinstance(T, TableType):
        return

    def impl(T):
        return T._len
    return impl


@lower_getattr(TableType, 'shape')
def lower_table_shape(context, builder, typ, val):
    impl = table_shape_overload(typ)
    return context.compile_internal(builder, impl, types.Tuple([types.int64,
        types.int64])(typ), (val,))


def table_shape_overload(T):
    if T.has_runtime_cols:

        def impl(T):
            return T._len, compute_num_runtime_columns(T)
        return impl
    ncols = len(T.arr_types)
    return lambda T: (T._len, types.int64(ncols))


@intrinsic
def compute_num_runtime_columns(typingctx, table_type):
    assert isinstance(table_type, TableType)

    def codegen(context, builder, sig, args):
        table_arg, = args
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        nwihu__trz = context.get_constant(types.int64, 0)
        for i, t in enumerate(table_type.arr_types):
            mfmc__zeib = getattr(table, f'block_{i}')
            qes__dsosz = ListInstance(context, builder, types.List(t),
                mfmc__zeib)
            nwihu__trz = builder.add(nwihu__trz, qes__dsosz.size)
        return nwihu__trz
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    table = cgutils.create_struct_proxy(table_type)(context, builder, table_arg
        )
    exn__piu = table_type.block_nums[col_ind]
    iawqy__che = table_type.block_offsets[col_ind]
    mfmc__zeib = getattr(table, f'block_{exn__piu}')
    tnvm__lhtot = types.none(table_type, types.List(arr_type), types.int64,
        types.int64)
    ibhsw__bfx = context.get_constant(types.int64, col_ind)
    koa__oypg = context.get_constant(types.int64, iawqy__che)
    bnww__usl = table_arg, mfmc__zeib, koa__oypg, ibhsw__bfx
    ensure_column_unboxed_codegen(context, builder, tnvm__lhtot, bnww__usl)
    qes__dsosz = ListInstance(context, builder, types.List(arr_type),
        mfmc__zeib)
    arr = qes__dsosz.getitem(iawqy__che)
    return arr


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, zexw__fksjk = args
        arr = get_table_data_codegen(context, builder, table_arg, col_ind,
            table_type)
        return impl_ret_borrowed(context, builder, arr_type, arr)
    sig = arr_type(table_type, ind_typ)
    return sig, codegen


@intrinsic
def del_column(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType
        ), 'Can only delete columns from a table'
    assert isinstance(ind_typ, types.TypeRef) and isinstance(ind_typ.
        instance_type, MetaType), 'ind_typ must be a typeref for a meta type'
    jwhte__vzm = list(ind_typ.instance_type.meta)
    ydeu__cbyzn = defaultdict(list)
    for ind in jwhte__vzm:
        ydeu__cbyzn[table_type.block_nums[ind]].append(table_type.
            block_offsets[ind])

    def codegen(context, builder, sig, args):
        table_arg, zexw__fksjk = args
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        for exn__piu, webil__niw in ydeu__cbyzn.items():
            arr_type = table_type.blk_to_type[exn__piu]
            mfmc__zeib = getattr(table, f'block_{exn__piu}')
            qes__dsosz = ListInstance(context, builder, types.List(arr_type
                ), mfmc__zeib)
            sfamo__ltgho = context.get_constant_null(arr_type)
            if len(webil__niw) == 1:
                iawqy__che = webil__niw[0]
                arr = qes__dsosz.getitem(iawqy__che)
                context.nrt.decref(builder, arr_type, arr)
                qes__dsosz.inititem(iawqy__che, sfamo__ltgho, incref=False)
            else:
                spr__leh = context.get_constant(types.int64, len(webil__niw))
                ppqtd__rzn = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(webil__niw, dtype=
                    np.int64))
                rayc__acwj = context.make_array(types.Array(types.int64, 1,
                    'C'))(context, builder, ppqtd__rzn)
                with cgutils.for_range(builder, spr__leh) as fxykj__xgod:
                    i = fxykj__xgod.index
                    iawqy__che = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        rayc__acwj, i)
                    arr = qes__dsosz.getitem(iawqy__che)
                    context.nrt.decref(builder, arr_type, arr)
                    qes__dsosz.inititem(iawqy__che, sfamo__ltgho, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    wqaiq__acp = context.get_constant(types.int64, 0)
    ttqgy__xkhf = context.get_constant(types.int64, 1)
    iufxw__genn = arr_type not in in_table_type.type_to_blk
    for t, exn__piu in out_table_type.type_to_blk.items():
        if t in in_table_type.type_to_blk:
            mdvjy__uuka = in_table_type.type_to_blk[t]
            evpri__ieba = ListInstance(context, builder, types.List(t),
                getattr(in_table, f'block_{mdvjy__uuka}'))
            context.nrt.incref(builder, types.List(t), evpri__ieba.value)
            setattr(out_table, f'block_{exn__piu}', evpri__ieba.value)
    if iufxw__genn:
        zexw__fksjk, evpri__ieba = ListInstance.allocate_ex(context,
            builder, types.List(arr_type), ttqgy__xkhf)
        evpri__ieba.size = ttqgy__xkhf
        evpri__ieba.inititem(wqaiq__acp, arr_arg, incref=True)
        exn__piu = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{exn__piu}', evpri__ieba.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        exn__piu = out_table_type.type_to_blk[arr_type]
        evpri__ieba = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{exn__piu}'))
        if is_new_col:
            n = evpri__ieba.size
            dupot__ytlij = builder.add(n, ttqgy__xkhf)
            evpri__ieba.resize(dupot__ytlij)
            evpri__ieba.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            qtkm__uqt = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            evpri__ieba.setitem(qtkm__uqt, arr_arg, incref=True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            qtkm__uqt = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            n = evpri__ieba.size
            dupot__ytlij = builder.add(n, ttqgy__xkhf)
            evpri__ieba.resize(dupot__ytlij)
            context.nrt.incref(builder, arr_type, evpri__ieba.getitem(
                qtkm__uqt))
            evpri__ieba.move(builder.add(qtkm__uqt, ttqgy__xkhf), qtkm__uqt,
                builder.sub(n, qtkm__uqt))
            evpri__ieba.setitem(qtkm__uqt, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    xdig__cnz = in_table_type.arr_types[col_ind]
    if xdig__cnz in out_table_type.type_to_blk:
        exn__piu = out_table_type.type_to_blk[xdig__cnz]
        vyqld__nnbd = getattr(out_table, f'block_{exn__piu}')
        cunol__oru = types.List(xdig__cnz)
        qtkm__uqt = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        bfaja__ntalm = cunol__oru.dtype(cunol__oru, types.intp)
        lgzex__ufiel = context.compile_internal(builder, lambda lst, i: lst
            .pop(i), bfaja__ntalm, (vyqld__nnbd, qtkm__uqt))
        context.nrt.decref(builder, xdig__cnz, lgzex__ufiel)


def generate_set_table_data_code(table, ind, arr_type, used_cols, is_null=False
    ):
    ppwq__frpj = list(table.arr_types)
    if ind == len(ppwq__frpj):
        mfr__rraem = None
        ppwq__frpj.append(arr_type)
    else:
        mfr__rraem = table.arr_types[ind]
        ppwq__frpj[ind] = arr_type
    woc__tudpz = TableType(tuple(ppwq__frpj))
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'set_table_parent': set_table_parent, 'alloc_list_like':
        alloc_list_like, 'out_table_typ': woc__tudpz}
    tlbm__tqte = 'def set_table_data(table, ind, arr, used_cols=None):\n'
    tlbm__tqte += f'  T2 = init_table(out_table_typ, False)\n'
    tlbm__tqte += f'  T2 = set_table_len(T2, len(table))\n'
    tlbm__tqte += f'  T2 = set_table_parent(T2, table)\n'
    for typ, exn__piu in woc__tudpz.type_to_blk.items():
        if typ in table.type_to_blk:
            sbp__huje = table.type_to_blk[typ]
            tlbm__tqte += (
                f'  arr_list_{exn__piu} = get_table_block(table, {sbp__huje})\n'
                )
            tlbm__tqte += f"""  out_arr_list_{exn__piu} = alloc_list_like(arr_list_{exn__piu}, {len(woc__tudpz.block_to_arr_ind[exn__piu])}, False)
"""
            if used_cols is None or set(table.block_to_arr_ind[sbp__huje]
                ) & used_cols:
                tlbm__tqte += f'  for i in range(len(arr_list_{exn__piu})):\n'
                if typ not in (mfr__rraem, arr_type):
                    tlbm__tqte += (
                        f'    out_arr_list_{exn__piu}[i] = arr_list_{exn__piu}[i]\n'
                        )
                else:
                    pyz__gdrew = table.block_to_arr_ind[sbp__huje]
                    cyo__lgw = np.empty(len(pyz__gdrew), np.int64)
                    zhccl__ibs = False
                    for ywclv__ovq, hgwu__ztt in enumerate(pyz__gdrew):
                        if hgwu__ztt != ind:
                            btbzu__cno = woc__tudpz.block_offsets[hgwu__ztt]
                        else:
                            btbzu__cno = -1
                            zhccl__ibs = True
                        cyo__lgw[ywclv__ovq] = btbzu__cno
                    glbls[f'out_idxs_{exn__piu}'] = np.array(cyo__lgw, np.int64
                        )
                    tlbm__tqte += f'    out_idx = out_idxs_{exn__piu}[i]\n'
                    if zhccl__ibs:
                        tlbm__tqte += f'    if out_idx == -1:\n'
                        tlbm__tqte += f'      continue\n'
                    tlbm__tqte += (
                        f'    out_arr_list_{exn__piu}[out_idx] = arr_list_{exn__piu}[i]\n'
                        )
            if typ == arr_type and not is_null:
                tlbm__tqte += (
                    f'  out_arr_list_{exn__piu}[{woc__tudpz.block_offsets[ind]}] = arr\n'
                    )
        else:
            glbls[f'arr_list_typ_{exn__piu}'] = types.List(arr_type)
            tlbm__tqte += f"""  out_arr_list_{exn__piu} = alloc_list_like(arr_list_typ_{exn__piu}, 1, False)
"""
            if not is_null:
                tlbm__tqte += f'  out_arr_list_{exn__piu}[0] = arr\n'
        tlbm__tqte += (
            f'  T2 = set_table_block(T2, out_arr_list_{exn__piu}, {exn__piu})\n'
            )
    tlbm__tqte += f'  return T2\n'
    aczi__xef = {}
    exec(tlbm__tqte, glbls, aczi__xef)
    return aczi__xef['set_table_data']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def set_table_data(table, ind, arr, used_cols=None):
    if is_overload_none(used_cols):
        stag__ulj = None
    else:
        stag__ulj = set(used_cols.instance_type.meta)
    ums__yrbb = get_overload_const_int(ind)
    return generate_set_table_data_code(table, ums__yrbb, arr, stag__ulj)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def set_table_data_null(table, ind, arr, used_cols=None):
    ums__yrbb = get_overload_const_int(ind)
    arr_type = arr.instance_type
    if is_overload_none(used_cols):
        stag__ulj = None
    else:
        stag__ulj = set(used_cols.instance_type.meta)
    return generate_set_table_data_code(table, ums__yrbb, arr_type,
        stag__ulj, is_null=True)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_table_data',
    'bodo.hiframes.table'] = alias_ext_dummy_func


def get_table_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    fxr__cnunv = args[0]
    if equiv_set.has_shape(fxr__cnunv):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            fxr__cnunv)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    cmq__kdj = []
    for t, exn__piu in table_type.type_to_blk.items():
        oomg__tzlma = len(table_type.block_to_arr_ind[exn__piu])
        dkkay__jgo = []
        for i in range(oomg__tzlma):
            hgwu__ztt = table_type.block_to_arr_ind[exn__piu][i]
            dkkay__jgo.append(pyval.arrays[hgwu__ztt])
        cmq__kdj.append(context.get_constant_generic(builder, types.List(t),
            dkkay__jgo))
    dfk__pjs = context.get_constant_null(types.pyobject)
    cms__eldl = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(cmq__kdj + [dfk__pjs, cms__eldl])


def get_init_table_output_type(table_type, to_str_if_dict_t):
    out_table_type = table_type.instance_type if isinstance(table_type,
        types.TypeRef) else table_type
    assert isinstance(out_table_type, TableType
        ), 'table type or typeref expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    if is_overload_true(to_str_if_dict_t):
        out_table_type = to_str_arr_if_dict_array(out_table_type)
    return out_table_type


@intrinsic
def init_table(typingctx, table_type, to_str_if_dict_t):
    out_table_type = get_init_table_output_type(table_type, to_str_if_dict_t)

    def codegen(context, builder, sig, args):
        table = cgutils.create_struct_proxy(out_table_type)(context, builder)
        for t, exn__piu in out_table_type.type_to_blk.items():
            jvrpy__xkor = context.get_constant_null(types.List(t))
            setattr(table, f'block_{exn__piu}', jvrpy__xkor)
        return table._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    tflj__dbfrb = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        tflj__dbfrb[typ.dtype] = i
    xfqfo__nin = table_type.instance_type if isinstance(table_type, types.
        TypeRef) else table_type
    assert isinstance(xfqfo__nin, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        qxlt__msrz, zexw__fksjk = args
        table = cgutils.create_struct_proxy(xfqfo__nin)(context, builder)
        for t, exn__piu in xfqfo__nin.type_to_blk.items():
            idx = tflj__dbfrb[t]
            ruu__sccc = signature(types.List(t), tuple_of_lists_type, types
                .literal(idx))
            tnzp__affi = qxlt__msrz, idx
            ceos__ltb = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, ruu__sccc, tnzp__affi)
            setattr(table, f'block_{exn__piu}', ceos__ltb)
        return table._getvalue()
    sig = xfqfo__nin(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    exn__piu = get_overload_const_int(blk_type)
    arr_type = None
    for t, zorac__dhz in table_type.type_to_blk.items():
        if zorac__dhz == exn__piu:
            arr_type = t
            break
    assert arr_type is not None, 'invalid table type block'
    zsi__obsa = types.List(arr_type)

    def codegen(context, builder, sig, args):
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            args[0])
        mfmc__zeib = getattr(table, f'block_{exn__piu}')
        return impl_ret_borrowed(context, builder, zsi__obsa, mfmc__zeib)
    sig = zsi__obsa(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, wafa__blyvn = args
        hkpd__fsrtx = context.get_python_api(builder)
        hvheg__jkrh = used_cols_typ == types.none
        if not hvheg__jkrh:
            pwvbr__knl = numba.cpython.setobj.SetInstance(context, builder,
                types.Set(types.int64), wafa__blyvn)
        table = cgutils.create_struct_proxy(sig.args[0])(context, builder,
            table_arg)
        for t, exn__piu in table_type.type_to_blk.items():
            spr__leh = context.get_constant(types.int64, len(table_type.
                block_to_arr_ind[exn__piu]))
            dphc__fvgf = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind[
                exn__piu], dtype=np.int64))
            qkmn__tngql = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, dphc__fvgf)
            mfmc__zeib = getattr(table, f'block_{exn__piu}')
            with cgutils.for_range(builder, spr__leh) as fxykj__xgod:
                i = fxykj__xgod.index
                hgwu__ztt = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    qkmn__tngql, i)
                tnvm__lhtot = types.none(table_type, types.List(t), types.
                    int64, types.int64)
                bnww__usl = table_arg, mfmc__zeib, i, hgwu__ztt
                if hvheg__jkrh:
                    ensure_column_unboxed_codegen(context, builder,
                        tnvm__lhtot, bnww__usl)
                else:
                    tjua__tspzs = pwvbr__knl.contains(hgwu__ztt)
                    with builder.if_then(tjua__tspzs):
                        ensure_column_unboxed_codegen(context, builder,
                            tnvm__lhtot, bnww__usl)
    assert isinstance(table_type, TableType), 'table type expected'
    sig = types.none(table_type, used_cols_typ)
    return sig, codegen


@intrinsic
def ensure_column_unboxed(typingctx, table_type, arr_list_t, ind_t, arr_ind_t):
    assert isinstance(table_type, TableType), 'table type expected'
    sig = types.none(table_type, arr_list_t, ind_t, arr_ind_t)
    return sig, ensure_column_unboxed_codegen


def ensure_column_unboxed_codegen(context, builder, sig, args):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    table_arg, rom__mrfpy, qyatw__nfgxu, ypjaw__gci = args
    hkpd__fsrtx = context.get_python_api(builder)
    table = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        table_arg)
    tknt__xkmrv = cgutils.is_not_null(builder, table.parent)
    qes__dsosz = ListInstance(context, builder, sig.args[1], rom__mrfpy)
    pem__uhjel = qes__dsosz.getitem(qyatw__nfgxu)
    tzx__lmfm = cgutils.alloca_once_value(builder, pem__uhjel)
    kdy__tbfaf = cgutils.alloca_once_value(builder, context.
        get_constant_null(sig.args[1].dtype))
    is_null = is_ll_eq(builder, tzx__lmfm, kdy__tbfaf)
    with builder.if_then(is_null):
        with builder.if_else(tknt__xkmrv) as (tth__jwtb, awud__bgu):
            with tth__jwtb:
                zkkwr__noov = get_df_obj_column_codegen(context, builder,
                    hkpd__fsrtx, table.parent, ypjaw__gci, sig.args[1].dtype)
                arr = hkpd__fsrtx.to_native_value(sig.args[1].dtype,
                    zkkwr__noov).value
                qes__dsosz.inititem(qyatw__nfgxu, arr, incref=False)
                hkpd__fsrtx.decref(zkkwr__noov)
            with awud__bgu:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    exn__piu = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, nxy__ndquo, zexw__fksjk = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{exn__piu}', nxy__ndquo)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, agyrm__igo = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = agyrm__igo
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def set_table_parent(typingctx, out_table_type, in_table_type):
    assert isinstance(in_table_type, TableType), 'table type expected'
    assert isinstance(out_table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        lofj__ujv, tdy__irbz = args
        in_table = cgutils.create_struct_proxy(in_table_type)(context,
            builder, tdy__irbz)
        out_table = cgutils.create_struct_proxy(out_table_type)(context,
            builder, lofj__ujv)
        out_table.parent = in_table.parent
        context.nrt.incref(builder, types.pyobject, out_table.parent)
        return impl_ret_borrowed(context, builder, out_table_type,
            out_table._getvalue())
    sig = out_table_type(out_table_type, in_table_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, len_type, to_str_if_dict_t):
    zsi__obsa = list_type.instance_type if isinstance(list_type, types.TypeRef
        ) else list_type
    assert isinstance(zsi__obsa, types.List), 'list type or typeref expected'
    assert isinstance(len_type, types.Integer), 'integer type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    if is_overload_true(to_str_if_dict_t):
        zsi__obsa = types.List(to_str_arr_if_dict_array(zsi__obsa.dtype))

    def codegen(context, builder, sig, args):
        nhj__evxlt = args[1]
        zexw__fksjk, evpri__ieba = ListInstance.allocate_ex(context,
            builder, zsi__obsa, nhj__evxlt)
        evpri__ieba.size = nhj__evxlt
        return evpri__ieba.value
    sig = zsi__obsa(list_type, len_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    ixgk__bpiix = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(ixgk__bpiix)

    def codegen(context, builder, sig, args):
        nhj__evxlt, zexw__fksjk = args
        zexw__fksjk, evpri__ieba = ListInstance.allocate_ex(context,
            builder, list_type, nhj__evxlt)
        evpri__ieba.size = nhj__evxlt
        return evpri__ieba.value
    sig = list_type(size_typ, data_typ)
    return sig, codegen


def _get_idx_length(idx):
    pass


@overload(_get_idx_length)
def overload_get_idx_length(idx, n):
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        return lambda idx, n: idx.sum()
    assert isinstance(idx, types.SliceType), 'slice index expected'

    def impl(idx, n):
        jtff__qpw = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(jtff__qpw)
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_filter(T, idx, used_cols=None):
    from bodo.utils.conversion import ensure_contig_if_np
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'set_table_block':
        set_table_block, 'set_table_len': set_table_len, 'alloc_list_like':
        alloc_list_like, '_get_idx_length': _get_idx_length,
        'ensure_contig_if_np': ensure_contig_if_np}
    if not is_overload_none(used_cols):
        rrc__ntu = used_cols.instance_type
        golq__ozibt = np.array(rrc__ntu.meta, dtype=np.int64)
        glbls['used_cols_vals'] = golq__ozibt
        ubpt__qtj = set([T.block_nums[i] for i in golq__ozibt])
    else:
        golq__ozibt = None
    tlbm__tqte = 'def table_filter_func(T, idx, used_cols=None):\n'
    tlbm__tqte += f'  T2 = init_table(T, False)\n'
    tlbm__tqte += f'  l = 0\n'
    if golq__ozibt is not None and len(golq__ozibt) == 0:
        tlbm__tqte += f'  l = _get_idx_length(idx, len(T))\n'
        tlbm__tqte += f'  T2 = set_table_len(T2, l)\n'
        tlbm__tqte += f'  return T2\n'
        aczi__xef = {}
        exec(tlbm__tqte, glbls, aczi__xef)
        return aczi__xef['table_filter_func']
    if golq__ozibt is not None:
        tlbm__tqte += f'  used_set = set(used_cols_vals)\n'
    for exn__piu in T.type_to_blk.values():
        tlbm__tqte += (
            f'  arr_list_{exn__piu} = get_table_block(T, {exn__piu})\n')
        tlbm__tqte += f"""  out_arr_list_{exn__piu} = alloc_list_like(arr_list_{exn__piu}, len(arr_list_{exn__piu}), False)
"""
        if golq__ozibt is None or exn__piu in ubpt__qtj:
            glbls[f'arr_inds_{exn__piu}'] = np.array(T.block_to_arr_ind[
                exn__piu], dtype=np.int64)
            tlbm__tqte += f'  for i in range(len(arr_list_{exn__piu})):\n'
            tlbm__tqte += f'    arr_ind_{exn__piu} = arr_inds_{exn__piu}[i]\n'
            if golq__ozibt is not None:
                tlbm__tqte += (
                    f'    if arr_ind_{exn__piu} not in used_set: continue\n')
            tlbm__tqte += f"""    ensure_column_unboxed(T, arr_list_{exn__piu}, i, arr_ind_{exn__piu})
"""
            tlbm__tqte += f"""    out_arr_{exn__piu} = ensure_contig_if_np(arr_list_{exn__piu}[i][idx])
"""
            tlbm__tqte += f'    l = len(out_arr_{exn__piu})\n'
            tlbm__tqte += (
                f'    out_arr_list_{exn__piu}[i] = out_arr_{exn__piu}\n')
        tlbm__tqte += (
            f'  T2 = set_table_block(T2, out_arr_list_{exn__piu}, {exn__piu})\n'
            )
    tlbm__tqte += f'  T2 = set_table_len(T2, l)\n'
    tlbm__tqte += f'  return T2\n'
    aczi__xef = {}
    exec(tlbm__tqte, glbls, aczi__xef)
    return aczi__xef['table_filter_func']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_subset(T, idx, copy_arrs, used_cols=None):
    rgag__yjs = list(idx.instance_type.meta)
    ppwq__frpj = tuple(np.array(T.arr_types, dtype=object)[rgag__yjs])
    woc__tudpz = TableType(ppwq__frpj)
    if not is_overload_constant_bool(copy_arrs):
        raise_bodo_error('table_subset(): copy_arrs must be a constant')
    axm__fyqot = is_overload_true(copy_arrs)
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'set_table_block':
        set_table_block, 'set_table_len': set_table_len, 'alloc_list_like':
        alloc_list_like, 'out_table_typ': woc__tudpz}
    if not is_overload_none(used_cols):
        kept_cols = used_cols.instance_type.meta
        zfw__bkj = set(kept_cols)
        glbls['kept_cols'] = np.array(kept_cols, np.int64)
        oirq__tdpez = True
    else:
        oirq__tdpez = False
    hrpri__ockd = {i: c for i, c in enumerate(rgag__yjs)}
    tlbm__tqte = 'def table_subset(T, idx, copy_arrs, used_cols=None):\n'
    tlbm__tqte += f'  T2 = init_table(out_table_typ, False)\n'
    tlbm__tqte += f'  T2 = set_table_len(T2, len(T))\n'
    if oirq__tdpez and len(zfw__bkj) == 0:
        tlbm__tqte += f'  return T2\n'
        aczi__xef = {}
        exec(tlbm__tqte, glbls, aczi__xef)
        return aczi__xef['table_subset']
    if oirq__tdpez:
        tlbm__tqte += f'  kept_cols_set = set(kept_cols)\n'
    for typ, exn__piu in woc__tudpz.type_to_blk.items():
        sbp__huje = T.type_to_blk[typ]
        tlbm__tqte += (
            f'  arr_list_{exn__piu} = get_table_block(T, {sbp__huje})\n')
        tlbm__tqte += f"""  out_arr_list_{exn__piu} = alloc_list_like(arr_list_{exn__piu}, {len(woc__tudpz.block_to_arr_ind[exn__piu])}, False)
"""
        piuve__gckm = True
        if oirq__tdpez:
            maau__zbcbs = set(woc__tudpz.block_to_arr_ind[exn__piu])
            bzf__hzhdr = maau__zbcbs & zfw__bkj
            piuve__gckm = len(bzf__hzhdr) > 0
        if piuve__gckm:
            glbls[f'out_arr_inds_{exn__piu}'] = np.array(woc__tudpz.
                block_to_arr_ind[exn__piu], dtype=np.int64)
            tlbm__tqte += f'  for i in range(len(out_arr_list_{exn__piu})):\n'
            tlbm__tqte += (
                f'    out_arr_ind_{exn__piu} = out_arr_inds_{exn__piu}[i]\n')
            if oirq__tdpez:
                tlbm__tqte += (
                    f'    if out_arr_ind_{exn__piu} not in kept_cols_set: continue\n'
                    )
            koe__vylh = []
            yuuso__sft = []
            for lis__yma in woc__tudpz.block_to_arr_ind[exn__piu]:
                xhb__mxe = hrpri__ockd[lis__yma]
                koe__vylh.append(xhb__mxe)
                weekt__jbym = T.block_offsets[xhb__mxe]
                yuuso__sft.append(weekt__jbym)
            glbls[f'in_logical_idx_{exn__piu}'] = np.array(koe__vylh, dtype
                =np.int64)
            glbls[f'in_physical_idx_{exn__piu}'] = np.array(yuuso__sft,
                dtype=np.int64)
            tlbm__tqte += (
                f'    logical_idx_{exn__piu} = in_logical_idx_{exn__piu}[i]\n')
            tlbm__tqte += (
                f'    physical_idx_{exn__piu} = in_physical_idx_{exn__piu}[i]\n'
                )
            tlbm__tqte += f"""    ensure_column_unboxed(T, arr_list_{exn__piu}, physical_idx_{exn__piu}, logical_idx_{exn__piu})
"""
            sqi__uvri = '.copy()' if axm__fyqot else ''
            tlbm__tqte += f"""    out_arr_list_{exn__piu}[i] = arr_list_{exn__piu}[physical_idx_{exn__piu}]{sqi__uvri}
"""
        tlbm__tqte += (
            f'  T2 = set_table_block(T2, out_arr_list_{exn__piu}, {exn__piu})\n'
            )
    tlbm__tqte += f'  return T2\n'
    aczi__xef = {}
    exec(tlbm__tqte, glbls, aczi__xef)
    return aczi__xef['table_subset']


def table_filter_equiv(self, scope, equiv_set, loc, args, kws):
    fxr__cnunv = args[0]
    if equiv_set.has_shape(fxr__cnunv):
        if guard(is_whole_slice, self.typemap, self.func_ir, args[1]):
            return ArrayAnalysis.AnalyzeResult(shape=fxr__cnunv, pre=[])
        return ArrayAnalysis.AnalyzeResult(shape=(None, equiv_set.get_shape
            (fxr__cnunv)[1]), pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_table_filter = (
    table_filter_equiv)


def table_subset_equiv(self, scope, equiv_set, loc, args, kws):
    fxr__cnunv = args[0]
    if equiv_set.has_shape(fxr__cnunv):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            fxr__cnunv)[0], None), pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_table_subset = (
    table_subset_equiv)


def gen_str_and_dict_enc_cols_to_one_block_fn_txt(in_table_type,
    out_table_type, glbls, is_gatherv=False):
    assert bodo.string_array_type in in_table_type.type_to_blk and bodo.string_array_type in in_table_type.type_to_blk, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: Table type {in_table_type} does not contain both a string, and encoded string column'
    qnvd__qcz = in_table_type.type_to_blk[bodo.string_array_type]
    kxg__dujv = in_table_type.type_to_blk[bodo.dict_str_arr_type]
    hrgtq__ekvlh = in_table_type.block_to_arr_ind.get(qnvd__qcz)
    veah__knrlm = in_table_type.block_to_arr_ind.get(kxg__dujv)
    qqi__fcq = []
    pcx__rzfm = []
    ldwln__pqr = 0
    przw__cao = 0
    for tyby__kjf in range(len(hrgtq__ekvlh) + len(veah__knrlm)):
        if ldwln__pqr == len(hrgtq__ekvlh):
            pcx__rzfm.append(tyby__kjf)
            continue
        elif przw__cao == len(veah__knrlm):
            qqi__fcq.append(tyby__kjf)
            continue
        ezwup__wllg = hrgtq__ekvlh[ldwln__pqr]
        zxy__lixa = veah__knrlm[przw__cao]
        if ezwup__wllg < zxy__lixa:
            qqi__fcq.append(tyby__kjf)
            ldwln__pqr += 1
        else:
            pcx__rzfm.append(tyby__kjf)
            przw__cao += 1
    assert 'output_table_str_arr_offsets_in_combined_block' not in glbls, "Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: key 'output_table_str_arr_idxs_in_combined_block' already present as a global variable"
    glbls['output_table_str_arr_offsets_in_combined_block'] = np.array(qqi__fcq
        )
    assert 'output_table_dict_enc_str_arr_offsets_in_combined_block' not in glbls, "Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: key 'output_table_str_arr_idxs_in_combined_block' already present as a global variable"
    glbls['output_table_dict_enc_str_arr_offsets_in_combined_block'
        ] = np.array(pcx__rzfm)
    glbls['decode_if_dict_array'] = decode_if_dict_array
    jdm__cbdvj = out_table_type.type_to_blk[bodo.string_array_type]
    assert f'arr_inds_{qnvd__qcz}' not in glbls, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: arr_inds_{qnvd__qcz} already present in global variables'
    glbls[f'arr_inds_{qnvd__qcz}'] = np.array(in_table_type.
        block_to_arr_ind[qnvd__qcz], dtype=np.int64)
    assert f'arr_inds_{kxg__dujv}' not in glbls, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: arr_inds_{kxg__dujv} already present in global variables'
    glbls[f'arr_inds_{kxg__dujv}'] = np.array(in_table_type.
        block_to_arr_ind[kxg__dujv], dtype=np.int64)
    tlbm__tqte = f'  input_str_arr_list = get_table_block(T, {qnvd__qcz})\n'
    tlbm__tqte += (
        f'  input_dict_enc_str_arr_list = get_table_block(T, {kxg__dujv})\n')
    tlbm__tqte += f"""  out_arr_list_{jdm__cbdvj} = alloc_list_like(input_str_arr_list, {len(qqi__fcq) + len(pcx__rzfm)}, True)
"""
    tlbm__tqte += f"""  for input_str_ary_idx, output_str_arr_offset in enumerate(output_table_str_arr_offsets_in_combined_block):
"""
    tlbm__tqte += (
        f'    arr_ind_str = arr_inds_{qnvd__qcz}[input_str_ary_idx]\n')
    tlbm__tqte += f"""    ensure_column_unboxed(T, input_str_arr_list, input_str_ary_idx, arr_ind_str)
"""
    tlbm__tqte += f'    out_arr_str = input_str_arr_list[input_str_ary_idx]\n'
    if is_gatherv:
        tlbm__tqte += (
            f'    out_arr_str = bodo.gatherv(out_arr_str, allgather, warn_if_rep, root)\n'
            )
    tlbm__tqte += (
        f'    out_arr_list_{jdm__cbdvj}[output_str_arr_offset] = out_arr_str\n'
        )
    tlbm__tqte += f"""  for input_dict_enc_str_ary_idx, output_dict_enc_str_arr_offset in enumerate(output_table_dict_enc_str_arr_offsets_in_combined_block):
"""
    tlbm__tqte += (
        f'    arr_ind_dict_enc_str = arr_inds_{kxg__dujv}[input_dict_enc_str_ary_idx]\n'
        )
    tlbm__tqte += f"""    ensure_column_unboxed(T, input_dict_enc_str_arr_list, input_dict_enc_str_ary_idx, arr_ind_dict_enc_str)
"""
    tlbm__tqte += f"""    out_arr_dict_enc_str = decode_if_dict_array(input_dict_enc_str_arr_list[input_dict_enc_str_ary_idx])
"""
    if is_gatherv:
        tlbm__tqte += f"""    out_arr_dict_enc_str = bodo.gatherv(out_arr_dict_enc_str, allgather, warn_if_rep, root)
"""
    tlbm__tqte += f"""    out_arr_list_{jdm__cbdvj}[output_dict_enc_str_arr_offset] = out_arr_dict_enc_str
"""
    tlbm__tqte += (
        f'  T2 = set_table_block(T2, out_arr_list_{jdm__cbdvj}, {jdm__cbdvj})\n'
        )
    return tlbm__tqte


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    tlbm__tqte = 'def impl(T):\n'
    tlbm__tqte += f'  T2 = init_table(T, True)\n'
    tlbm__tqte += f'  l = len(T)\n'
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'set_table_block':
        set_table_block, 'set_table_len': set_table_len, 'alloc_list_like':
        alloc_list_like, 'decode_if_dict_array': decode_if_dict_array}
    out_table_type = bodo.hiframes.table.get_init_table_output_type(T, True)
    oom__vfei = (bodo.string_array_type in T.type_to_blk and bodo.
        dict_str_arr_type in T.type_to_blk)
    if oom__vfei:
        tlbm__tqte += gen_str_and_dict_enc_cols_to_one_block_fn_txt(T,
            out_table_type, glbls)
    for typ, nkcm__wgw in T.type_to_blk.items():
        if oom__vfei and typ in (bodo.string_array_type, bodo.dict_str_arr_type
            ):
            continue
        if typ == bodo.dict_str_arr_type:
            assert bodo.string_array_type in out_table_type.type_to_blk, 'Error in decode_if_dict_table: If encoded string type is present in the input, then non-encoded string type should be present in the output'
            tgue__hya = out_table_type.type_to_blk[bodo.string_array_type]
        else:
            assert typ in out_table_type.type_to_blk, 'Error in decode_if_dict_table: All non-encoded string types present in the input should be present in the output'
            tgue__hya = out_table_type.type_to_blk[typ]
        glbls[f'arr_inds_{nkcm__wgw}'] = np.array(T.block_to_arr_ind[
            nkcm__wgw], dtype=np.int64)
        tlbm__tqte += (
            f'  arr_list_{nkcm__wgw} = get_table_block(T, {nkcm__wgw})\n')
        tlbm__tqte += f"""  out_arr_list_{nkcm__wgw} = alloc_list_like(arr_list_{nkcm__wgw}, len(arr_list_{nkcm__wgw}), True)
"""
        tlbm__tqte += f'  for i in range(len(arr_list_{nkcm__wgw})):\n'
        tlbm__tqte += f'    arr_ind_{nkcm__wgw} = arr_inds_{nkcm__wgw}[i]\n'
        tlbm__tqte += f"""    ensure_column_unboxed(T, arr_list_{nkcm__wgw}, i, arr_ind_{nkcm__wgw})
"""
        tlbm__tqte += (
            f'    out_arr_{nkcm__wgw} = decode_if_dict_array(arr_list_{nkcm__wgw}[i])\n'
            )
        tlbm__tqte += (
            f'    out_arr_list_{nkcm__wgw}[i] = out_arr_{nkcm__wgw}\n')
        tlbm__tqte += (
            f'  T2 = set_table_block(T2, out_arr_list_{nkcm__wgw}, {tgue__hya})\n'
            )
    tlbm__tqte += f'  T2 = set_table_len(T2, l)\n'
    tlbm__tqte += f'  return T2\n'
    aczi__xef = {}
    exec(tlbm__tqte, glbls, aczi__xef)
    return aczi__xef['impl']


@overload(operator.getitem, no_unliteral=True, inline='always')
def overload_table_getitem(T, idx):
    if not isinstance(T, TableType):
        return
    return lambda T, idx: table_filter(T, idx)


@intrinsic
def init_runtime_table_from_lists(typingctx, arr_list_tup_typ, nrows_typ=None):
    assert isinstance(arr_list_tup_typ, types.BaseTuple
        ), 'init_runtime_table_from_lists requires a tuple of list of arrays'
    if isinstance(arr_list_tup_typ, types.UniTuple):
        if arr_list_tup_typ.dtype.dtype == types.undefined:
            return
        jwwb__lxzfe = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        jwwb__lxzfe = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            jwwb__lxzfe.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        ebjin__kky, oiii__uzj = args
        table = cgutils.create_struct_proxy(table_type)(context, builder)
        table.len = oiii__uzj
        cmq__kdj = cgutils.unpack_tuple(builder, ebjin__kky)
        for i, mfmc__zeib in enumerate(cmq__kdj):
            setattr(table, f'block_{i}', mfmc__zeib)
            context.nrt.incref(builder, types.List(jwwb__lxzfe[i]), mfmc__zeib)
        return table._getvalue()
    table_type = TableType(tuple(jwwb__lxzfe), True)
    sig = table_type(arr_list_tup_typ, nrows_typ)
    return sig, codegen


def _to_arr_if_series(t):
    return t.data if isinstance(t, SeriesType) else t


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def logical_table_to_table(in_table_t, extra_arrs_t, in_col_inds_t,
    n_table_cols_t, out_table_type_t=None, used_cols=None):
    in_col_inds = in_col_inds_t.instance_type.meta
    assert isinstance(in_table_t, (TableType, types.BaseTuple, types.NoneType)
        ), 'logical_table_to_table: input table must be a TableType or tuple of arrays or None (for dead table)'
    glbls = {}
    if not is_overload_none(used_cols):
        kept_cols = set(used_cols.instance_type.meta)
        glbls['kept_cols'] = np.array(list(kept_cols), np.int64)
        oirq__tdpez = True
    else:
        kept_cols = set(np.arange(len(in_col_inds)))
        oirq__tdpez = False
    extra_arrs_no_series = ', '.join(f'get_series_data(extra_arrs_t[{i}])' if
        isinstance(extra_arrs_t[i], SeriesType) else f'extra_arrs_t[{i}]' for
        i in range(len(extra_arrs_t)))
    extra_arrs_no_series = (
        f"({extra_arrs_no_series}{',' if len(extra_arrs_t) == 1 else ''})")
    if isinstance(in_table_t, (types.BaseTuple, types.NoneType)):
        return _logical_tuple_table_to_table_codegen(in_table_t,
            extra_arrs_t, in_col_inds, kept_cols, n_table_cols_t,
            out_table_type_t, extra_arrs_no_series)
    lgjsw__pqyv = len(in_table_t.arr_types)
    out_table_type = TableType(tuple(in_table_t.arr_types[i] if i <
        lgjsw__pqyv else _to_arr_if_series(extra_arrs_t.types[i -
        lgjsw__pqyv]) for i in in_col_inds)) if is_overload_none(
        out_table_type_t) else unwrap_typeref(out_table_type_t)
    glbls.update({'init_table': init_table, 'set_table_len': set_table_len,
        'out_table_type': out_table_type})
    tlbm__tqte = """def impl(in_table_t, extra_arrs_t, in_col_inds_t, n_table_cols_t, out_table_type_t=None, used_cols=None):
"""
    if any(isinstance(t, SeriesType) for t in extra_arrs_t.types):
        tlbm__tqte += f'  extra_arrs_t = {extra_arrs_no_series}\n'
    tlbm__tqte += f'  T1 = in_table_t\n'
    tlbm__tqte += f'  T2 = init_table(out_table_type, False)\n'
    tlbm__tqte += f'  T2 = set_table_len(T2, len(T1))\n'
    if oirq__tdpez and len(kept_cols) == 0:
        tlbm__tqte += f'  return T2\n'
        aczi__xef = {}
        exec(tlbm__tqte, glbls, aczi__xef)
        return aczi__xef['impl']
    if oirq__tdpez:
        tlbm__tqte += f'  kept_cols_set = set(kept_cols)\n'
    for typ, exn__piu in out_table_type.type_to_blk.items():
        glbls[f'arr_list_typ_{exn__piu}'] = types.List(typ)
        spr__leh = len(out_table_type.block_to_arr_ind[exn__piu])
        tlbm__tqte += f"""  out_arr_list_{exn__piu} = alloc_list_like(arr_list_typ_{exn__piu}, {spr__leh}, False)
"""
        if typ in in_table_t.type_to_blk:
            rcgno__cnkw = in_table_t.type_to_blk[typ]
            zagzr__ptes = []
            bbm__qhvki = []
            for abtc__zpe in out_table_type.block_to_arr_ind[exn__piu]:
                htct__syb = in_col_inds[abtc__zpe]
                if htct__syb < lgjsw__pqyv:
                    zagzr__ptes.append(in_table_t.block_offsets[htct__syb])
                    bbm__qhvki.append(htct__syb)
                else:
                    zagzr__ptes.append(-1)
                    bbm__qhvki.append(-1)
            glbls[f'in_idxs_{exn__piu}'] = np.array(zagzr__ptes, np.int64)
            glbls[f'in_arr_inds_{exn__piu}'] = np.array(bbm__qhvki, np.int64)
            if oirq__tdpez:
                glbls[f'out_arr_inds_{exn__piu}'] = np.array(out_table_type
                    .block_to_arr_ind[exn__piu], dtype=np.int64)
            tlbm__tqte += (
                f'  in_arr_list_{exn__piu} = get_table_block(T1, {rcgno__cnkw})\n'
                )
            tlbm__tqte += f'  for i in range(len(out_arr_list_{exn__piu})):\n'
            tlbm__tqte += f'    in_offset_{exn__piu} = in_idxs_{exn__piu}[i]\n'
            tlbm__tqte += f'    if in_offset_{exn__piu} == -1:\n'
            tlbm__tqte += f'      continue\n'
            tlbm__tqte += (
                f'    in_arr_ind_{exn__piu} = in_arr_inds_{exn__piu}[i]\n')
            if oirq__tdpez:
                tlbm__tqte += (
                    f'    if out_arr_inds_{exn__piu}[i] not in kept_cols_set: continue\n'
                    )
            tlbm__tqte += f"""    ensure_column_unboxed(T1, in_arr_list_{exn__piu}, in_offset_{exn__piu}, in_arr_ind_{exn__piu})
"""
            tlbm__tqte += f"""    out_arr_list_{exn__piu}[i] = in_arr_list_{exn__piu}[in_offset_{exn__piu}]
"""
        for i, abtc__zpe in enumerate(out_table_type.block_to_arr_ind[exn__piu]
            ):
            if abtc__zpe not in kept_cols:
                continue
            htct__syb = in_col_inds[abtc__zpe]
            if htct__syb >= lgjsw__pqyv:
                tlbm__tqte += f"""  out_arr_list_{exn__piu}[{i}] = extra_arrs_t[{htct__syb - lgjsw__pqyv}]
"""
        tlbm__tqte += (
            f'  T2 = set_table_block(T2, out_arr_list_{exn__piu}, {exn__piu})\n'
            )
    tlbm__tqte += f'  return T2\n'
    glbls.update({'alloc_list_like': alloc_list_like, 'set_table_block':
        set_table_block, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'get_series_data':
        bodo.hiframes.pd_series_ext.get_series_data})
    aczi__xef = {}
    exec(tlbm__tqte, glbls, aczi__xef)
    return aczi__xef['impl']


def _logical_tuple_table_to_table_codegen(in_table_t, extra_arrs_t,
    in_col_inds, kept_cols, n_table_cols_t, out_table_type_t,
    extra_arrs_no_series):
    lgjsw__pqyv = get_overload_const_int(n_table_cols_t
        ) if is_overload_constant_int(n_table_cols_t) else len(in_table_t.types
        )
    out_table_type = TableType(tuple(in_table_t.types[i] if i < lgjsw__pqyv
         else _to_arr_if_series(extra_arrs_t.types[i - lgjsw__pqyv]) for i in
        in_col_inds)) if is_overload_none(out_table_type_t
        ) else unwrap_typeref(out_table_type_t)
    jyob__orfxt = None
    if not is_overload_none(in_table_t):
        for i, t in enumerate(in_table_t.types):
            if t != types.none:
                jyob__orfxt = f'in_table_t[{i}]'
                break
    if jyob__orfxt is None:
        for i, t in enumerate(extra_arrs_t.types):
            if t != types.none:
                jyob__orfxt = f'extra_arrs_t[{i}]'
                break
    assert jyob__orfxt is not None, 'no array found in input data'
    tlbm__tqte = """def impl(in_table_t, extra_arrs_t, in_col_inds_t, n_table_cols_t, out_table_type_t=None, used_cols=None):
"""
    if any(isinstance(t, SeriesType) for t in extra_arrs_t.types):
        tlbm__tqte += f'  extra_arrs_t = {extra_arrs_no_series}\n'
    tlbm__tqte += f'  T1 = in_table_t\n'
    tlbm__tqte += f'  T2 = init_table(out_table_type, False)\n'
    tlbm__tqte += f'  T2 = set_table_len(T2, len({jyob__orfxt}))\n'
    glbls = {}
    for typ, exn__piu in out_table_type.type_to_blk.items():
        glbls[f'arr_list_typ_{exn__piu}'] = types.List(typ)
        spr__leh = len(out_table_type.block_to_arr_ind[exn__piu])
        tlbm__tqte += f"""  out_arr_list_{exn__piu} = alloc_list_like(arr_list_typ_{exn__piu}, {spr__leh}, False)
"""
        for i, abtc__zpe in enumerate(out_table_type.block_to_arr_ind[exn__piu]
            ):
            if abtc__zpe not in kept_cols:
                continue
            htct__syb = in_col_inds[abtc__zpe]
            if htct__syb < lgjsw__pqyv:
                tlbm__tqte += (
                    f'  out_arr_list_{exn__piu}[{i}] = T1[{htct__syb}]\n')
            else:
                tlbm__tqte += f"""  out_arr_list_{exn__piu}[{i}] = extra_arrs_t[{htct__syb - lgjsw__pqyv}]
"""
        tlbm__tqte += (
            f'  T2 = set_table_block(T2, out_arr_list_{exn__piu}, {exn__piu})\n'
            )
    tlbm__tqte += f'  return T2\n'
    glbls.update({'init_table': init_table, 'alloc_list_like':
        alloc_list_like, 'set_table_block': set_table_block,
        'set_table_len': set_table_len, 'out_table_type': out_table_type,
        'get_series_data': bodo.hiframes.pd_series_ext.get_series_data})
    aczi__xef = {}
    exec(tlbm__tqte, glbls, aczi__xef)
    return aczi__xef['impl']


def logical_table_to_table_equiv(self, scope, equiv_set, loc, args, kws):
    kltih__wyhgq = args[0]
    cjn__zkcyh = args[1]
    if equiv_set.has_shape(kltih__wyhgq):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            kltih__wyhgq)[0], None), pre=[])
    if equiv_set.has_shape(cjn__zkcyh):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            cjn__zkcyh)[0], None), pre=[])


(ArrayAnalysis._analyze_op_call_bodo_hiframes_table_logical_table_to_table
    ) = logical_table_to_table_equiv


def alias_ext_logical_table_to_table(lhs_name, args, alias_map, arg_aliases):
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['logical_table_to_table',
    'bodo.hiframes.table'] = alias_ext_logical_table_to_table
