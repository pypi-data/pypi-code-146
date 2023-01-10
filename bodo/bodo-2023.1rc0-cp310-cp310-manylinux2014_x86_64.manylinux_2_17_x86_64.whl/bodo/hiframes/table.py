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
            xcjtd__jgzxl = 0
            cegsf__zvbv = []
            for i in range(usecols[-1] + 1):
                if i == usecols[xcjtd__jgzxl]:
                    cegsf__zvbv.append(arrs[xcjtd__jgzxl])
                    xcjtd__jgzxl += 1
                else:
                    cegsf__zvbv.append(None)
            for ktsqr__qnu in range(usecols[-1] + 1, num_arrs):
                cegsf__zvbv.append(None)
            self.arrays = cegsf__zvbv
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((fvn__edo == nttap__iem).all() for fvn__edo,
            nttap__iem in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        thyf__alpn = len(self.arrays)
        cfr__ultn = dict(zip(range(thyf__alpn), self.arrays))
        df = pd.DataFrame(cfr__ultn, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        ijcpa__tyaq = []
        judcg__srt = []
        efty__alqj = {}
        xcxgs__vuf = {}
        ymcg__bvao = defaultdict(int)
        mtp__ddtvp = defaultdict(list)
        if not has_runtime_cols:
            for i, t in enumerate(arr_types):
                if t not in efty__alqj:
                    xeg__oajgv = len(efty__alqj)
                    efty__alqj[t] = xeg__oajgv
                    xcxgs__vuf[xeg__oajgv] = t
                jwvm__nhnri = efty__alqj[t]
                ijcpa__tyaq.append(jwvm__nhnri)
                judcg__srt.append(ymcg__bvao[jwvm__nhnri])
                ymcg__bvao[jwvm__nhnri] += 1
                mtp__ddtvp[jwvm__nhnri].append(i)
        self.block_nums = ijcpa__tyaq
        self.block_offsets = judcg__srt
        self.type_to_blk = efty__alqj
        self.blk_to_type = xcxgs__vuf
        self.block_to_arr_ind = mtp__ddtvp
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
            vjb__hwe = [(f'block_{i}', types.List(t)) for i, t in enumerate
                (fe_type.arr_types)]
        else:
            vjb__hwe = [(f'block_{jwvm__nhnri}', types.List(t)) for t,
                jwvm__nhnri in fe_type.type_to_blk.items()]
        vjb__hwe.append(('parent', types.pyobject))
        vjb__hwe.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, vjb__hwe)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    dou__erqxd = c.pyapi.object_getattr_string(val, 'arrays')
    table = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    table.parent = cgutils.get_null_value(table.parent.type)
    ell__pij = c.pyapi.make_none()
    vucx__rwqfb = c.context.get_constant(types.int64, 0)
    uuxm__kugug = cgutils.alloca_once_value(c.builder, vucx__rwqfb)
    for t, jwvm__nhnri in typ.type_to_blk.items():
        djom__edco = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[jwvm__nhnri]))
        ktsqr__qnu, serm__iwe = ListInstance.allocate_ex(c.context, c.
            builder, types.List(t), djom__edco)
        serm__iwe.size = djom__edco
        ecoo__fgyc = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[jwvm__nhnri
            ], dtype=np.int64))
        pyrsh__qpenp = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, ecoo__fgyc)
        with cgutils.for_range(c.builder, djom__edco) as ahx__crenk:
            i = ahx__crenk.index
            dgcod__wqkb = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), pyrsh__qpenp, i)
            kfx__yyszf = c.pyapi.long_from_longlong(dgcod__wqkb)
            ntlkd__hytbl = c.pyapi.object_getitem(dou__erqxd, kfx__yyszf)
            wyr__kxm = c.builder.icmp_unsigned('==', ntlkd__hytbl, ell__pij)
            with c.builder.if_else(wyr__kxm) as (utt__psdwr, iuj__lqx):
                with utt__psdwr:
                    qhvxl__cborq = c.context.get_constant_null(t)
                    serm__iwe.inititem(i, qhvxl__cborq, incref=False)
                with iuj__lqx:
                    vhte__ikbnt = c.pyapi.call_method(ntlkd__hytbl,
                        '__len__', ())
                    naucw__umm = c.pyapi.long_as_longlong(vhte__ikbnt)
                    c.builder.store(naucw__umm, uuxm__kugug)
                    c.pyapi.decref(vhte__ikbnt)
                    arr = c.pyapi.to_native_value(t, ntlkd__hytbl).value
                    serm__iwe.inititem(i, arr, incref=False)
            c.pyapi.decref(ntlkd__hytbl)
            c.pyapi.decref(kfx__yyszf)
        setattr(table, f'block_{jwvm__nhnri}', serm__iwe.value)
    table.len = c.builder.load(uuxm__kugug)
    c.pyapi.decref(dou__erqxd)
    c.pyapi.decref(ell__pij)
    odvc__vhsd = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(table._getvalue(), is_error=odvc__vhsd)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    table = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        kuc__wrjd = c.context.get_constant(types.int64, 0)
        for i, t in enumerate(typ.arr_types):
            cegsf__zvbv = getattr(table, f'block_{i}')
            cyjk__ecq = ListInstance(c.context, c.builder, types.List(t),
                cegsf__zvbv)
            kuc__wrjd = c.builder.add(kuc__wrjd, cyjk__ecq.size)
        znrc__onc = c.pyapi.list_new(kuc__wrjd)
        qodpl__axglv = c.context.get_constant(types.int64, 0)
        for i, t in enumerate(typ.arr_types):
            cegsf__zvbv = getattr(table, f'block_{i}')
            cyjk__ecq = ListInstance(c.context, c.builder, types.List(t),
                cegsf__zvbv)
            with cgutils.for_range(c.builder, cyjk__ecq.size) as ahx__crenk:
                i = ahx__crenk.index
                arr = cyjk__ecq.getitem(i)
                c.context.nrt.incref(c.builder, t, arr)
                idx = c.builder.add(qodpl__axglv, i)
                c.pyapi.list_setitem(znrc__onc, idx, c.pyapi.
                    from_native_value(t, arr, c.env_manager))
            qodpl__axglv = c.builder.add(qodpl__axglv, cyjk__ecq.size)
        utjkk__hthec = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        wmq__uon = c.pyapi.call_function_objargs(utjkk__hthec, (znrc__onc,))
        c.pyapi.decref(utjkk__hthec)
        c.pyapi.decref(znrc__onc)
        c.context.nrt.decref(c.builder, typ, val)
        return wmq__uon
    znrc__onc = c.pyapi.list_new(c.context.get_constant(types.int64, len(
        typ.arr_types)))
    ttpl__bgqsx = cgutils.is_not_null(c.builder, table.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for t, jwvm__nhnri in typ.type_to_blk.items():
        cegsf__zvbv = getattr(table, f'block_{jwvm__nhnri}')
        cyjk__ecq = ListInstance(c.context, c.builder, types.List(t),
            cegsf__zvbv)
        ecoo__fgyc = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[jwvm__nhnri
            ], dtype=np.int64))
        pyrsh__qpenp = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, ecoo__fgyc)
        with cgutils.for_range(c.builder, cyjk__ecq.size) as ahx__crenk:
            i = ahx__crenk.index
            dgcod__wqkb = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), pyrsh__qpenp, i)
            arr = cyjk__ecq.getitem(i)
            zpbgg__ktjkk = cgutils.alloca_once_value(c.builder, arr)
            ywv__ybx = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(t))
            is_null = is_ll_eq(c.builder, zpbgg__ktjkk, ywv__ybx)
            with c.builder.if_else(c.builder.and_(is_null, c.builder.not_(
                ensure_unboxed))) as (utt__psdwr, iuj__lqx):
                with utt__psdwr:
                    ell__pij = c.pyapi.make_none()
                    c.pyapi.list_setitem(znrc__onc, dgcod__wqkb, ell__pij)
                with iuj__lqx:
                    ntlkd__hytbl = cgutils.alloca_once(c.builder, c.context
                        .get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(is_null, ttpl__bgqsx)
                        ) as (nyt__pfuu, prak__smqg):
                        with nyt__pfuu:
                            uqrqf__ido = get_df_obj_column_codegen(c.
                                context, c.builder, c.pyapi, table.parent,
                                dgcod__wqkb, t)
                            c.builder.store(uqrqf__ido, ntlkd__hytbl)
                        with prak__smqg:
                            c.context.nrt.incref(c.builder, t, arr)
                            c.builder.store(c.pyapi.from_native_value(t,
                                arr, c.env_manager), ntlkd__hytbl)
                    c.pyapi.list_setitem(znrc__onc, dgcod__wqkb, c.builder.
                        load(ntlkd__hytbl))
    utjkk__hthec = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    wmq__uon = c.pyapi.call_function_objargs(utjkk__hthec, (znrc__onc,))
    c.pyapi.decref(utjkk__hthec)
    c.pyapi.decref(znrc__onc)
    c.context.nrt.decref(c.builder, typ, val)
    return wmq__uon


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
        qyht__wicd = context.get_constant(types.int64, 0)
        for i, t in enumerate(table_type.arr_types):
            cegsf__zvbv = getattr(table, f'block_{i}')
            cyjk__ecq = ListInstance(context, builder, types.List(t),
                cegsf__zvbv)
            qyht__wicd = builder.add(qyht__wicd, cyjk__ecq.size)
        return qyht__wicd
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    table = cgutils.create_struct_proxy(table_type)(context, builder, table_arg
        )
    jwvm__nhnri = table_type.block_nums[col_ind]
    kfcxy__jmyt = table_type.block_offsets[col_ind]
    cegsf__zvbv = getattr(table, f'block_{jwvm__nhnri}')
    icnp__how = types.none(table_type, types.List(arr_type), types.int64,
        types.int64)
    vxk__eeen = context.get_constant(types.int64, col_ind)
    weebe__gfu = context.get_constant(types.int64, kfcxy__jmyt)
    kroup__xfa = table_arg, cegsf__zvbv, weebe__gfu, vxk__eeen
    ensure_column_unboxed_codegen(context, builder, icnp__how, kroup__xfa)
    cyjk__ecq = ListInstance(context, builder, types.List(arr_type),
        cegsf__zvbv)
    arr = cyjk__ecq.getitem(kfcxy__jmyt)
    return arr


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, ktsqr__qnu = args
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
    xss__nqy = list(ind_typ.instance_type.meta)
    aggm__hbl = defaultdict(list)
    for ind in xss__nqy:
        aggm__hbl[table_type.block_nums[ind]].append(table_type.
            block_offsets[ind])

    def codegen(context, builder, sig, args):
        table_arg, ktsqr__qnu = args
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        for jwvm__nhnri, fmrq__yibrj in aggm__hbl.items():
            arr_type = table_type.blk_to_type[jwvm__nhnri]
            cegsf__zvbv = getattr(table, f'block_{jwvm__nhnri}')
            cyjk__ecq = ListInstance(context, builder, types.List(arr_type),
                cegsf__zvbv)
            qhvxl__cborq = context.get_constant_null(arr_type)
            if len(fmrq__yibrj) == 1:
                kfcxy__jmyt = fmrq__yibrj[0]
                arr = cyjk__ecq.getitem(kfcxy__jmyt)
                context.nrt.decref(builder, arr_type, arr)
                cyjk__ecq.inititem(kfcxy__jmyt, qhvxl__cborq, incref=False)
            else:
                djom__edco = context.get_constant(types.int64, len(fmrq__yibrj)
                    )
                suvi__ddpat = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(fmrq__yibrj, dtype
                    =np.int64))
                cvhf__rqoe = context.make_array(types.Array(types.int64, 1,
                    'C'))(context, builder, suvi__ddpat)
                with cgutils.for_range(builder, djom__edco) as ahx__crenk:
                    i = ahx__crenk.index
                    kfcxy__jmyt = _getitem_array_single_int(context,
                        builder, types.int64, types.Array(types.int64, 1,
                        'C'), cvhf__rqoe, i)
                    arr = cyjk__ecq.getitem(kfcxy__jmyt)
                    context.nrt.decref(builder, arr_type, arr)
                    cyjk__ecq.inititem(kfcxy__jmyt, qhvxl__cborq, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    vucx__rwqfb = context.get_constant(types.int64, 0)
    kwu__dewqa = context.get_constant(types.int64, 1)
    oun__fxdoz = arr_type not in in_table_type.type_to_blk
    for t, jwvm__nhnri in out_table_type.type_to_blk.items():
        if t in in_table_type.type_to_blk:
            gkkd__dijkf = in_table_type.type_to_blk[t]
            serm__iwe = ListInstance(context, builder, types.List(t),
                getattr(in_table, f'block_{gkkd__dijkf}'))
            context.nrt.incref(builder, types.List(t), serm__iwe.value)
            setattr(out_table, f'block_{jwvm__nhnri}', serm__iwe.value)
    if oun__fxdoz:
        ktsqr__qnu, serm__iwe = ListInstance.allocate_ex(context, builder,
            types.List(arr_type), kwu__dewqa)
        serm__iwe.size = kwu__dewqa
        serm__iwe.inititem(vucx__rwqfb, arr_arg, incref=True)
        jwvm__nhnri = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{jwvm__nhnri}', serm__iwe.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        jwvm__nhnri = out_table_type.type_to_blk[arr_type]
        serm__iwe = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{jwvm__nhnri}'))
        if is_new_col:
            n = serm__iwe.size
            ccbl__uie = builder.add(n, kwu__dewqa)
            serm__iwe.resize(ccbl__uie)
            serm__iwe.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            tvekj__vovj = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            serm__iwe.setitem(tvekj__vovj, arr_arg, incref=True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            tvekj__vovj = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            n = serm__iwe.size
            ccbl__uie = builder.add(n, kwu__dewqa)
            serm__iwe.resize(ccbl__uie)
            context.nrt.incref(builder, arr_type, serm__iwe.getitem(
                tvekj__vovj))
            serm__iwe.move(builder.add(tvekj__vovj, kwu__dewqa),
                tvekj__vovj, builder.sub(n, tvekj__vovj))
            serm__iwe.setitem(tvekj__vovj, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    vwx__plm = in_table_type.arr_types[col_ind]
    if vwx__plm in out_table_type.type_to_blk:
        jwvm__nhnri = out_table_type.type_to_blk[vwx__plm]
        vivv__onq = getattr(out_table, f'block_{jwvm__nhnri}')
        ripnb__nmg = types.List(vwx__plm)
        tvekj__vovj = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        msbxq__fpovy = ripnb__nmg.dtype(ripnb__nmg, types.intp)
        rxjb__ejdin = context.compile_internal(builder, lambda lst, i: lst.
            pop(i), msbxq__fpovy, (vivv__onq, tvekj__vovj))
        context.nrt.decref(builder, vwx__plm, rxjb__ejdin)


def generate_set_table_data_code(table, ind, arr_type, used_cols, is_null=False
    ):
    cfcna__raijm = list(table.arr_types)
    if ind == len(cfcna__raijm):
        widhj__utmea = None
        cfcna__raijm.append(arr_type)
    else:
        widhj__utmea = table.arr_types[ind]
        cfcna__raijm[ind] = arr_type
    pix__vwf = TableType(tuple(cfcna__raijm))
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'set_table_parent': set_table_parent, 'alloc_list_like':
        alloc_list_like, 'out_table_typ': pix__vwf}
    hcd__ghudi = 'def set_table_data(table, ind, arr, used_cols=None):\n'
    hcd__ghudi += f'  T2 = init_table(out_table_typ, False)\n'
    hcd__ghudi += f'  T2 = set_table_len(T2, len(table))\n'
    hcd__ghudi += f'  T2 = set_table_parent(T2, table)\n'
    for typ, jwvm__nhnri in pix__vwf.type_to_blk.items():
        if typ in table.type_to_blk:
            qjs__cfbu = table.type_to_blk[typ]
            hcd__ghudi += (
                f'  arr_list_{jwvm__nhnri} = get_table_block(table, {qjs__cfbu})\n'
                )
            hcd__ghudi += f"""  out_arr_list_{jwvm__nhnri} = alloc_list_like(arr_list_{jwvm__nhnri}, {len(pix__vwf.block_to_arr_ind[jwvm__nhnri])}, False)
"""
            if used_cols is None or set(table.block_to_arr_ind[qjs__cfbu]
                ) & used_cols:
                hcd__ghudi += (
                    f'  for i in range(len(arr_list_{jwvm__nhnri})):\n')
                if typ not in (widhj__utmea, arr_type):
                    hcd__ghudi += (
                        f'    out_arr_list_{jwvm__nhnri}[i] = arr_list_{jwvm__nhnri}[i]\n'
                        )
                else:
                    vaghw__qge = table.block_to_arr_ind[qjs__cfbu]
                    xob__kty = np.empty(len(vaghw__qge), np.int64)
                    fdiyi__nsbg = False
                    for knk__vmd, dgcod__wqkb in enumerate(vaghw__qge):
                        if dgcod__wqkb != ind:
                            koyhh__wsx = pix__vwf.block_offsets[dgcod__wqkb]
                        else:
                            koyhh__wsx = -1
                            fdiyi__nsbg = True
                        xob__kty[knk__vmd] = koyhh__wsx
                    glbls[f'out_idxs_{jwvm__nhnri}'] = np.array(xob__kty,
                        np.int64)
                    hcd__ghudi += f'    out_idx = out_idxs_{jwvm__nhnri}[i]\n'
                    if fdiyi__nsbg:
                        hcd__ghudi += f'    if out_idx == -1:\n'
                        hcd__ghudi += f'      continue\n'
                    hcd__ghudi += f"""    out_arr_list_{jwvm__nhnri}[out_idx] = arr_list_{jwvm__nhnri}[i]
"""
            if typ == arr_type and not is_null:
                hcd__ghudi += (
                    f'  out_arr_list_{jwvm__nhnri}[{pix__vwf.block_offsets[ind]}] = arr\n'
                    )
        else:
            glbls[f'arr_list_typ_{jwvm__nhnri}'] = types.List(arr_type)
            hcd__ghudi += f"""  out_arr_list_{jwvm__nhnri} = alloc_list_like(arr_list_typ_{jwvm__nhnri}, 1, False)
"""
            if not is_null:
                hcd__ghudi += f'  out_arr_list_{jwvm__nhnri}[0] = arr\n'
        hcd__ghudi += (
            f'  T2 = set_table_block(T2, out_arr_list_{jwvm__nhnri}, {jwvm__nhnri})\n'
            )
    hcd__ghudi += f'  return T2\n'
    ybmck__vum = {}
    exec(hcd__ghudi, glbls, ybmck__vum)
    return ybmck__vum['set_table_data']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def set_table_data(table, ind, arr, used_cols=None):
    if is_overload_none(used_cols):
        mib__hrnhd = None
    else:
        mib__hrnhd = set(used_cols.instance_type.meta)
    rdsxz__baon = get_overload_const_int(ind)
    return generate_set_table_data_code(table, rdsxz__baon, arr, mib__hrnhd)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def set_table_data_null(table, ind, arr, used_cols=None):
    rdsxz__baon = get_overload_const_int(ind)
    arr_type = arr.instance_type
    if is_overload_none(used_cols):
        mib__hrnhd = None
    else:
        mib__hrnhd = set(used_cols.instance_type.meta)
    return generate_set_table_data_code(table, rdsxz__baon, arr_type,
        mib__hrnhd, is_null=True)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_table_data',
    'bodo.hiframes.table'] = alias_ext_dummy_func


def get_table_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    ldh__zlqf = args[0]
    if equiv_set.has_shape(ldh__zlqf):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            ldh__zlqf)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    yriyq__aruy = []
    for t, jwvm__nhnri in table_type.type_to_blk.items():
        oazdr__xtz = len(table_type.block_to_arr_ind[jwvm__nhnri])
        hbrun__dhy = []
        for i in range(oazdr__xtz):
            dgcod__wqkb = table_type.block_to_arr_ind[jwvm__nhnri][i]
            hbrun__dhy.append(pyval.arrays[dgcod__wqkb])
        yriyq__aruy.append(context.get_constant_generic(builder, types.List
            (t), hbrun__dhy))
    aqq__ddbf = context.get_constant_null(types.pyobject)
    exri__skpb = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(yriyq__aruy + [aqq__ddbf, exri__skpb])


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
        for t, jwvm__nhnri in out_table_type.type_to_blk.items():
            hbfaa__ktjyz = context.get_constant_null(types.List(t))
            setattr(table, f'block_{jwvm__nhnri}', hbfaa__ktjyz)
        return table._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    cwb__dqf = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        cwb__dqf[typ.dtype] = i
    jeaf__uqg = table_type.instance_type if isinstance(table_type, types.
        TypeRef) else table_type
    assert isinstance(jeaf__uqg, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        tgc__xuw, ktsqr__qnu = args
        table = cgutils.create_struct_proxy(jeaf__uqg)(context, builder)
        for t, jwvm__nhnri in jeaf__uqg.type_to_blk.items():
            idx = cwb__dqf[t]
            zqla__xjf = signature(types.List(t), tuple_of_lists_type, types
                .literal(idx))
            wqks__jbj = tgc__xuw, idx
            wvls__mwpp = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, zqla__xjf, wqks__jbj)
            setattr(table, f'block_{jwvm__nhnri}', wvls__mwpp)
        return table._getvalue()
    sig = jeaf__uqg(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    jwvm__nhnri = get_overload_const_int(blk_type)
    arr_type = None
    for t, nttap__iem in table_type.type_to_blk.items():
        if nttap__iem == jwvm__nhnri:
            arr_type = t
            break
    assert arr_type is not None, 'invalid table type block'
    ojej__srt = types.List(arr_type)

    def codegen(context, builder, sig, args):
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            args[0])
        cegsf__zvbv = getattr(table, f'block_{jwvm__nhnri}')
        return impl_ret_borrowed(context, builder, ojej__srt, cegsf__zvbv)
    sig = ojej__srt(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, pzo__pycga = args
        ggt__yttz = context.get_python_api(builder)
        zvis__sqkh = used_cols_typ == types.none
        if not zvis__sqkh:
            zzkqp__ndbe = numba.cpython.setobj.SetInstance(context, builder,
                types.Set(types.int64), pzo__pycga)
        table = cgutils.create_struct_proxy(sig.args[0])(context, builder,
            table_arg)
        for t, jwvm__nhnri in table_type.type_to_blk.items():
            djom__edco = context.get_constant(types.int64, len(table_type.
                block_to_arr_ind[jwvm__nhnri]))
            ecoo__fgyc = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind[
                jwvm__nhnri], dtype=np.int64))
            pyrsh__qpenp = context.make_array(types.Array(types.int64, 1, 'C')
                )(context, builder, ecoo__fgyc)
            cegsf__zvbv = getattr(table, f'block_{jwvm__nhnri}')
            with cgutils.for_range(builder, djom__edco) as ahx__crenk:
                i = ahx__crenk.index
                dgcod__wqkb = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    pyrsh__qpenp, i)
                icnp__how = types.none(table_type, types.List(t), types.
                    int64, types.int64)
                kroup__xfa = table_arg, cegsf__zvbv, i, dgcod__wqkb
                if zvis__sqkh:
                    ensure_column_unboxed_codegen(context, builder,
                        icnp__how, kroup__xfa)
                else:
                    zfelb__onhv = zzkqp__ndbe.contains(dgcod__wqkb)
                    with builder.if_then(zfelb__onhv):
                        ensure_column_unboxed_codegen(context, builder,
                            icnp__how, kroup__xfa)
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
    table_arg, wpq__ggzl, ftb__wpz, lmfg__gww = args
    ggt__yttz = context.get_python_api(builder)
    table = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        table_arg)
    ttpl__bgqsx = cgutils.is_not_null(builder, table.parent)
    cyjk__ecq = ListInstance(context, builder, sig.args[1], wpq__ggzl)
    yukid__mswn = cyjk__ecq.getitem(ftb__wpz)
    zpbgg__ktjkk = cgutils.alloca_once_value(builder, yukid__mswn)
    ywv__ybx = cgutils.alloca_once_value(builder, context.get_constant_null
        (sig.args[1].dtype))
    is_null = is_ll_eq(builder, zpbgg__ktjkk, ywv__ybx)
    with builder.if_then(is_null):
        with builder.if_else(ttpl__bgqsx) as (utt__psdwr, iuj__lqx):
            with utt__psdwr:
                ntlkd__hytbl = get_df_obj_column_codegen(context, builder,
                    ggt__yttz, table.parent, lmfg__gww, sig.args[1].dtype)
                arr = ggt__yttz.to_native_value(sig.args[1].dtype, ntlkd__hytbl
                    ).value
                cyjk__ecq.inititem(ftb__wpz, arr, incref=False)
                ggt__yttz.decref(ntlkd__hytbl)
            with iuj__lqx:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    jwvm__nhnri = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, aiv__qudzr, ktsqr__qnu = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{jwvm__nhnri}', aiv__qudzr)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, qin__dsxwb = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = qin__dsxwb
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def set_table_parent(typingctx, out_table_type, in_table_type):
    assert isinstance(in_table_type, TableType), 'table type expected'
    assert isinstance(out_table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        wgbtr__fde, jipca__gyy = args
        in_table = cgutils.create_struct_proxy(in_table_type)(context,
            builder, jipca__gyy)
        out_table = cgutils.create_struct_proxy(out_table_type)(context,
            builder, wgbtr__fde)
        out_table.parent = in_table.parent
        context.nrt.incref(builder, types.pyobject, out_table.parent)
        return impl_ret_borrowed(context, builder, out_table_type,
            out_table._getvalue())
    sig = out_table_type(out_table_type, in_table_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, len_type, to_str_if_dict_t):
    ojej__srt = list_type.instance_type if isinstance(list_type, types.TypeRef
        ) else list_type
    assert isinstance(ojej__srt, types.List), 'list type or typeref expected'
    assert isinstance(len_type, types.Integer), 'integer type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    if is_overload_true(to_str_if_dict_t):
        ojej__srt = types.List(to_str_arr_if_dict_array(ojej__srt.dtype))

    def codegen(context, builder, sig, args):
        hyr__dbg = args[1]
        ktsqr__qnu, serm__iwe = ListInstance.allocate_ex(context, builder,
            ojej__srt, hyr__dbg)
        serm__iwe.size = hyr__dbg
        return serm__iwe.value
    sig = ojej__srt(list_type, len_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    jgf__ieut = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(jgf__ieut)

    def codegen(context, builder, sig, args):
        hyr__dbg, ktsqr__qnu = args
        ktsqr__qnu, serm__iwe = ListInstance.allocate_ex(context, builder,
            list_type, hyr__dbg)
        serm__iwe.size = hyr__dbg
        return serm__iwe.value
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
        snhqa__zikpv = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(snhqa__zikpv)
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
        szndh__otkl = used_cols.instance_type
        tbq__zwec = np.array(szndh__otkl.meta, dtype=np.int64)
        glbls['used_cols_vals'] = tbq__zwec
        urlyo__shw = set([T.block_nums[i] for i in tbq__zwec])
    else:
        tbq__zwec = None
    hcd__ghudi = 'def table_filter_func(T, idx, used_cols=None):\n'
    hcd__ghudi += f'  T2 = init_table(T, False)\n'
    hcd__ghudi += f'  l = 0\n'
    if tbq__zwec is not None and len(tbq__zwec) == 0:
        hcd__ghudi += f'  l = _get_idx_length(idx, len(T))\n'
        hcd__ghudi += f'  T2 = set_table_len(T2, l)\n'
        hcd__ghudi += f'  return T2\n'
        ybmck__vum = {}
        exec(hcd__ghudi, glbls, ybmck__vum)
        return ybmck__vum['table_filter_func']
    if tbq__zwec is not None:
        hcd__ghudi += f'  used_set = set(used_cols_vals)\n'
    for jwvm__nhnri in T.type_to_blk.values():
        hcd__ghudi += (
            f'  arr_list_{jwvm__nhnri} = get_table_block(T, {jwvm__nhnri})\n')
        hcd__ghudi += f"""  out_arr_list_{jwvm__nhnri} = alloc_list_like(arr_list_{jwvm__nhnri}, len(arr_list_{jwvm__nhnri}), False)
"""
        if tbq__zwec is None or jwvm__nhnri in urlyo__shw:
            glbls[f'arr_inds_{jwvm__nhnri}'] = np.array(T.block_to_arr_ind[
                jwvm__nhnri], dtype=np.int64)
            hcd__ghudi += f'  for i in range(len(arr_list_{jwvm__nhnri})):\n'
            hcd__ghudi += (
                f'    arr_ind_{jwvm__nhnri} = arr_inds_{jwvm__nhnri}[i]\n')
            if tbq__zwec is not None:
                hcd__ghudi += (
                    f'    if arr_ind_{jwvm__nhnri} not in used_set: continue\n'
                    )
            hcd__ghudi += f"""    ensure_column_unboxed(T, arr_list_{jwvm__nhnri}, i, arr_ind_{jwvm__nhnri})
"""
            hcd__ghudi += f"""    out_arr_{jwvm__nhnri} = ensure_contig_if_np(arr_list_{jwvm__nhnri}[i][idx])
"""
            hcd__ghudi += f'    l = len(out_arr_{jwvm__nhnri})\n'
            hcd__ghudi += (
                f'    out_arr_list_{jwvm__nhnri}[i] = out_arr_{jwvm__nhnri}\n')
        hcd__ghudi += (
            f'  T2 = set_table_block(T2, out_arr_list_{jwvm__nhnri}, {jwvm__nhnri})\n'
            )
    hcd__ghudi += f'  T2 = set_table_len(T2, l)\n'
    hcd__ghudi += f'  return T2\n'
    ybmck__vum = {}
    exec(hcd__ghudi, glbls, ybmck__vum)
    return ybmck__vum['table_filter_func']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_subset(T, idx, copy_arrs, used_cols=None):
    prqj__pqscm = list(idx.instance_type.meta)
    cfcna__raijm = tuple(np.array(T.arr_types, dtype=object)[prqj__pqscm])
    pix__vwf = TableType(cfcna__raijm)
    if not is_overload_constant_bool(copy_arrs):
        raise_bodo_error('table_subset(): copy_arrs must be a constant')
    kbq__kseun = is_overload_true(copy_arrs)
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'set_table_block':
        set_table_block, 'set_table_len': set_table_len, 'alloc_list_like':
        alloc_list_like, 'out_table_typ': pix__vwf}
    if not is_overload_none(used_cols):
        kept_cols = used_cols.instance_type.meta
        wmh__ymkd = set(kept_cols)
        glbls['kept_cols'] = np.array(kept_cols, np.int64)
        syjg__juq = True
    else:
        syjg__juq = False
    irpud__yiqpl = {i: c for i, c in enumerate(prqj__pqscm)}
    hcd__ghudi = 'def table_subset(T, idx, copy_arrs, used_cols=None):\n'
    hcd__ghudi += f'  T2 = init_table(out_table_typ, False)\n'
    hcd__ghudi += f'  T2 = set_table_len(T2, len(T))\n'
    if syjg__juq and len(wmh__ymkd) == 0:
        hcd__ghudi += f'  return T2\n'
        ybmck__vum = {}
        exec(hcd__ghudi, glbls, ybmck__vum)
        return ybmck__vum['table_subset']
    if syjg__juq:
        hcd__ghudi += f'  kept_cols_set = set(kept_cols)\n'
    for typ, jwvm__nhnri in pix__vwf.type_to_blk.items():
        qjs__cfbu = T.type_to_blk[typ]
        hcd__ghudi += (
            f'  arr_list_{jwvm__nhnri} = get_table_block(T, {qjs__cfbu})\n')
        hcd__ghudi += f"""  out_arr_list_{jwvm__nhnri} = alloc_list_like(arr_list_{jwvm__nhnri}, {len(pix__vwf.block_to_arr_ind[jwvm__nhnri])}, False)
"""
        qknwz__ykpjg = True
        if syjg__juq:
            dciw__yaufs = set(pix__vwf.block_to_arr_ind[jwvm__nhnri])
            xqir__xql = dciw__yaufs & wmh__ymkd
            qknwz__ykpjg = len(xqir__xql) > 0
        if qknwz__ykpjg:
            glbls[f'out_arr_inds_{jwvm__nhnri}'] = np.array(pix__vwf.
                block_to_arr_ind[jwvm__nhnri], dtype=np.int64)
            hcd__ghudi += (
                f'  for i in range(len(out_arr_list_{jwvm__nhnri})):\n')
            hcd__ghudi += (
                f'    out_arr_ind_{jwvm__nhnri} = out_arr_inds_{jwvm__nhnri}[i]\n'
                )
            if syjg__juq:
                hcd__ghudi += (
                    f'    if out_arr_ind_{jwvm__nhnri} not in kept_cols_set: continue\n'
                    )
            tya__cusei = []
            caa__qho = []
            for ubxf__ter in pix__vwf.block_to_arr_ind[jwvm__nhnri]:
                kizf__uatv = irpud__yiqpl[ubxf__ter]
                tya__cusei.append(kizf__uatv)
                zkx__fvdzp = T.block_offsets[kizf__uatv]
                caa__qho.append(zkx__fvdzp)
            glbls[f'in_logical_idx_{jwvm__nhnri}'] = np.array(tya__cusei,
                dtype=np.int64)
            glbls[f'in_physical_idx_{jwvm__nhnri}'] = np.array(caa__qho,
                dtype=np.int64)
            hcd__ghudi += (
                f'    logical_idx_{jwvm__nhnri} = in_logical_idx_{jwvm__nhnri}[i]\n'
                )
            hcd__ghudi += (
                f'    physical_idx_{jwvm__nhnri} = in_physical_idx_{jwvm__nhnri}[i]\n'
                )
            hcd__ghudi += f"""    ensure_column_unboxed(T, arr_list_{jwvm__nhnri}, physical_idx_{jwvm__nhnri}, logical_idx_{jwvm__nhnri})
"""
            wroq__xxqr = '.copy()' if kbq__kseun else ''
            hcd__ghudi += f"""    out_arr_list_{jwvm__nhnri}[i] = arr_list_{jwvm__nhnri}[physical_idx_{jwvm__nhnri}]{wroq__xxqr}
"""
        hcd__ghudi += (
            f'  T2 = set_table_block(T2, out_arr_list_{jwvm__nhnri}, {jwvm__nhnri})\n'
            )
    hcd__ghudi += f'  return T2\n'
    ybmck__vum = {}
    exec(hcd__ghudi, glbls, ybmck__vum)
    return ybmck__vum['table_subset']


def table_filter_equiv(self, scope, equiv_set, loc, args, kws):
    ldh__zlqf = args[0]
    if equiv_set.has_shape(ldh__zlqf):
        if guard(is_whole_slice, self.typemap, self.func_ir, args[1]):
            return ArrayAnalysis.AnalyzeResult(shape=ldh__zlqf, pre=[])
        return ArrayAnalysis.AnalyzeResult(shape=(None, equiv_set.get_shape
            (ldh__zlqf)[1]), pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_table_filter = (
    table_filter_equiv)


def table_subset_equiv(self, scope, equiv_set, loc, args, kws):
    ldh__zlqf = args[0]
    if equiv_set.has_shape(ldh__zlqf):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            ldh__zlqf)[0], None), pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_table_subset = (
    table_subset_equiv)


def gen_str_and_dict_enc_cols_to_one_block_fn_txt(in_table_type,
    out_table_type, glbls, is_gatherv=False):
    assert bodo.string_array_type in in_table_type.type_to_blk and bodo.string_array_type in in_table_type.type_to_blk, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: Table type {in_table_type} does not contain both a string, and encoded string column'
    ndie__fvel = in_table_type.type_to_blk[bodo.string_array_type]
    szt__scolz = in_table_type.type_to_blk[bodo.dict_str_arr_type]
    lomjl__ozarn = in_table_type.block_to_arr_ind.get(ndie__fvel)
    jqmq__yvzh = in_table_type.block_to_arr_ind.get(szt__scolz)
    mhc__fuyz = []
    sspk__pkd = []
    nzp__rgidm = 0
    ewpci__anfly = 0
    for mwafu__rozx in range(len(lomjl__ozarn) + len(jqmq__yvzh)):
        if nzp__rgidm == len(lomjl__ozarn):
            sspk__pkd.append(mwafu__rozx)
            continue
        elif ewpci__anfly == len(jqmq__yvzh):
            mhc__fuyz.append(mwafu__rozx)
            continue
        ozofg__vzsu = lomjl__ozarn[nzp__rgidm]
        rdvea__etmw = jqmq__yvzh[ewpci__anfly]
        if ozofg__vzsu < rdvea__etmw:
            mhc__fuyz.append(mwafu__rozx)
            nzp__rgidm += 1
        else:
            sspk__pkd.append(mwafu__rozx)
            ewpci__anfly += 1
    assert 'output_table_str_arr_offsets_in_combined_block' not in glbls, "Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: key 'output_table_str_arr_idxs_in_combined_block' already present as a global variable"
    glbls['output_table_str_arr_offsets_in_combined_block'] = np.array(
        mhc__fuyz)
    assert 'output_table_dict_enc_str_arr_offsets_in_combined_block' not in glbls, "Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: key 'output_table_str_arr_idxs_in_combined_block' already present as a global variable"
    glbls['output_table_dict_enc_str_arr_offsets_in_combined_block'
        ] = np.array(sspk__pkd)
    glbls['decode_if_dict_array'] = decode_if_dict_array
    woe__ducpb = out_table_type.type_to_blk[bodo.string_array_type]
    assert f'arr_inds_{ndie__fvel}' not in glbls, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: arr_inds_{ndie__fvel} already present in global variables'
    glbls[f'arr_inds_{ndie__fvel}'] = np.array(in_table_type.
        block_to_arr_ind[ndie__fvel], dtype=np.int64)
    assert f'arr_inds_{szt__scolz}' not in glbls, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: arr_inds_{szt__scolz} already present in global variables'
    glbls[f'arr_inds_{szt__scolz}'] = np.array(in_table_type.
        block_to_arr_ind[szt__scolz], dtype=np.int64)
    hcd__ghudi = f'  input_str_arr_list = get_table_block(T, {ndie__fvel})\n'
    hcd__ghudi += (
        f'  input_dict_enc_str_arr_list = get_table_block(T, {szt__scolz})\n')
    hcd__ghudi += f"""  out_arr_list_{woe__ducpb} = alloc_list_like(input_str_arr_list, {len(mhc__fuyz) + len(sspk__pkd)}, True)
"""
    hcd__ghudi += f"""  for input_str_ary_idx, output_str_arr_offset in enumerate(output_table_str_arr_offsets_in_combined_block):
"""
    hcd__ghudi += (
        f'    arr_ind_str = arr_inds_{ndie__fvel}[input_str_ary_idx]\n')
    hcd__ghudi += f"""    ensure_column_unboxed(T, input_str_arr_list, input_str_ary_idx, arr_ind_str)
"""
    hcd__ghudi += f'    out_arr_str = input_str_arr_list[input_str_ary_idx]\n'
    if is_gatherv:
        hcd__ghudi += (
            f'    out_arr_str = bodo.gatherv(out_arr_str, allgather, warn_if_rep, root)\n'
            )
    hcd__ghudi += (
        f'    out_arr_list_{woe__ducpb}[output_str_arr_offset] = out_arr_str\n'
        )
    hcd__ghudi += f"""  for input_dict_enc_str_ary_idx, output_dict_enc_str_arr_offset in enumerate(output_table_dict_enc_str_arr_offsets_in_combined_block):
"""
    hcd__ghudi += (
        f'    arr_ind_dict_enc_str = arr_inds_{szt__scolz}[input_dict_enc_str_ary_idx]\n'
        )
    hcd__ghudi += f"""    ensure_column_unboxed(T, input_dict_enc_str_arr_list, input_dict_enc_str_ary_idx, arr_ind_dict_enc_str)
"""
    hcd__ghudi += f"""    out_arr_dict_enc_str = decode_if_dict_array(input_dict_enc_str_arr_list[input_dict_enc_str_ary_idx])
"""
    if is_gatherv:
        hcd__ghudi += f"""    out_arr_dict_enc_str = bodo.gatherv(out_arr_dict_enc_str, allgather, warn_if_rep, root)
"""
    hcd__ghudi += f"""    out_arr_list_{woe__ducpb}[output_dict_enc_str_arr_offset] = out_arr_dict_enc_str
"""
    hcd__ghudi += (
        f'  T2 = set_table_block(T2, out_arr_list_{woe__ducpb}, {woe__ducpb})\n'
        )
    return hcd__ghudi


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    hcd__ghudi = 'def impl(T):\n'
    hcd__ghudi += f'  T2 = init_table(T, True)\n'
    hcd__ghudi += f'  l = len(T)\n'
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'set_table_block':
        set_table_block, 'set_table_len': set_table_len, 'alloc_list_like':
        alloc_list_like, 'decode_if_dict_array': decode_if_dict_array}
    out_table_type = bodo.hiframes.table.get_init_table_output_type(T, True)
    omj__hnsm = (bodo.string_array_type in T.type_to_blk and bodo.
        dict_str_arr_type in T.type_to_blk)
    if omj__hnsm:
        hcd__ghudi += gen_str_and_dict_enc_cols_to_one_block_fn_txt(T,
            out_table_type, glbls)
    for typ, rnr__jtf in T.type_to_blk.items():
        if omj__hnsm and typ in (bodo.string_array_type, bodo.dict_str_arr_type
            ):
            continue
        if typ == bodo.dict_str_arr_type:
            assert bodo.string_array_type in out_table_type.type_to_blk, 'Error in decode_if_dict_table: If encoded string type is present in the input, then non-encoded string type should be present in the output'
            nmlkx__lxiry = out_table_type.type_to_blk[bodo.string_array_type]
        else:
            assert typ in out_table_type.type_to_blk, 'Error in decode_if_dict_table: All non-encoded string types present in the input should be present in the output'
            nmlkx__lxiry = out_table_type.type_to_blk[typ]
        glbls[f'arr_inds_{rnr__jtf}'] = np.array(T.block_to_arr_ind[
            rnr__jtf], dtype=np.int64)
        hcd__ghudi += (
            f'  arr_list_{rnr__jtf} = get_table_block(T, {rnr__jtf})\n')
        hcd__ghudi += f"""  out_arr_list_{rnr__jtf} = alloc_list_like(arr_list_{rnr__jtf}, len(arr_list_{rnr__jtf}), True)
"""
        hcd__ghudi += f'  for i in range(len(arr_list_{rnr__jtf})):\n'
        hcd__ghudi += f'    arr_ind_{rnr__jtf} = arr_inds_{rnr__jtf}[i]\n'
        hcd__ghudi += (
            f'    ensure_column_unboxed(T, arr_list_{rnr__jtf}, i, arr_ind_{rnr__jtf})\n'
            )
        hcd__ghudi += (
            f'    out_arr_{rnr__jtf} = decode_if_dict_array(arr_list_{rnr__jtf}[i])\n'
            )
        hcd__ghudi += f'    out_arr_list_{rnr__jtf}[i] = out_arr_{rnr__jtf}\n'
        hcd__ghudi += (
            f'  T2 = set_table_block(T2, out_arr_list_{rnr__jtf}, {nmlkx__lxiry})\n'
            )
    hcd__ghudi += f'  T2 = set_table_len(T2, l)\n'
    hcd__ghudi += f'  return T2\n'
    ybmck__vum = {}
    exec(hcd__ghudi, glbls, ybmck__vum)
    return ybmck__vum['impl']


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
        rbjka__tkpe = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        rbjka__tkpe = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            rbjka__tkpe.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        ovllw__ihad, cvlr__oucvf = args
        table = cgutils.create_struct_proxy(table_type)(context, builder)
        table.len = cvlr__oucvf
        yriyq__aruy = cgutils.unpack_tuple(builder, ovllw__ihad)
        for i, cegsf__zvbv in enumerate(yriyq__aruy):
            setattr(table, f'block_{i}', cegsf__zvbv)
            context.nrt.incref(builder, types.List(rbjka__tkpe[i]), cegsf__zvbv
                )
        return table._getvalue()
    table_type = TableType(tuple(rbjka__tkpe), True)
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
        syjg__juq = True
    else:
        kept_cols = set(np.arange(len(in_col_inds)))
        syjg__juq = False
    extra_arrs_no_series = ', '.join(f'get_series_data(extra_arrs_t[{i}])' if
        isinstance(extra_arrs_t[i], SeriesType) else f'extra_arrs_t[{i}]' for
        i in range(len(extra_arrs_t)))
    extra_arrs_no_series = (
        f"({extra_arrs_no_series}{',' if len(extra_arrs_t) == 1 else ''})")
    if isinstance(in_table_t, (types.BaseTuple, types.NoneType)):
        return _logical_tuple_table_to_table_codegen(in_table_t,
            extra_arrs_t, in_col_inds, kept_cols, n_table_cols_t,
            out_table_type_t, extra_arrs_no_series)
    qflzq__siewp = len(in_table_t.arr_types)
    out_table_type = TableType(tuple(in_table_t.arr_types[i] if i <
        qflzq__siewp else _to_arr_if_series(extra_arrs_t.types[i -
        qflzq__siewp]) for i in in_col_inds)) if is_overload_none(
        out_table_type_t) else unwrap_typeref(out_table_type_t)
    glbls.update({'init_table': init_table, 'set_table_len': set_table_len,
        'out_table_type': out_table_type})
    hcd__ghudi = """def impl(in_table_t, extra_arrs_t, in_col_inds_t, n_table_cols_t, out_table_type_t=None, used_cols=None):
"""
    if any(isinstance(t, SeriesType) for t in extra_arrs_t.types):
        hcd__ghudi += f'  extra_arrs_t = {extra_arrs_no_series}\n'
    hcd__ghudi += f'  T1 = in_table_t\n'
    hcd__ghudi += f'  T2 = init_table(out_table_type, False)\n'
    hcd__ghudi += f'  T2 = set_table_len(T2, len(T1))\n'
    if syjg__juq and len(kept_cols) == 0:
        hcd__ghudi += f'  return T2\n'
        ybmck__vum = {}
        exec(hcd__ghudi, glbls, ybmck__vum)
        return ybmck__vum['impl']
    if syjg__juq:
        hcd__ghudi += f'  kept_cols_set = set(kept_cols)\n'
    for typ, jwvm__nhnri in out_table_type.type_to_blk.items():
        glbls[f'arr_list_typ_{jwvm__nhnri}'] = types.List(typ)
        djom__edco = len(out_table_type.block_to_arr_ind[jwvm__nhnri])
        hcd__ghudi += f"""  out_arr_list_{jwvm__nhnri} = alloc_list_like(arr_list_typ_{jwvm__nhnri}, {djom__edco}, False)
"""
        if typ in in_table_t.type_to_blk:
            klcka__mrwo = in_table_t.type_to_blk[typ]
            zrhn__fvlp = []
            qhimz__jock = []
            for rezq__buffz in out_table_type.block_to_arr_ind[jwvm__nhnri]:
                iuh__bpuk = in_col_inds[rezq__buffz]
                if iuh__bpuk < qflzq__siewp:
                    zrhn__fvlp.append(in_table_t.block_offsets[iuh__bpuk])
                    qhimz__jock.append(iuh__bpuk)
                else:
                    zrhn__fvlp.append(-1)
                    qhimz__jock.append(-1)
            glbls[f'in_idxs_{jwvm__nhnri}'] = np.array(zrhn__fvlp, np.int64)
            glbls[f'in_arr_inds_{jwvm__nhnri}'] = np.array(qhimz__jock, np.
                int64)
            if syjg__juq:
                glbls[f'out_arr_inds_{jwvm__nhnri}'] = np.array(out_table_type
                    .block_to_arr_ind[jwvm__nhnri], dtype=np.int64)
            hcd__ghudi += (
                f'  in_arr_list_{jwvm__nhnri} = get_table_block(T1, {klcka__mrwo})\n'
                )
            hcd__ghudi += (
                f'  for i in range(len(out_arr_list_{jwvm__nhnri})):\n')
            hcd__ghudi += (
                f'    in_offset_{jwvm__nhnri} = in_idxs_{jwvm__nhnri}[i]\n')
            hcd__ghudi += f'    if in_offset_{jwvm__nhnri} == -1:\n'
            hcd__ghudi += f'      continue\n'
            hcd__ghudi += (
                f'    in_arr_ind_{jwvm__nhnri} = in_arr_inds_{jwvm__nhnri}[i]\n'
                )
            if syjg__juq:
                hcd__ghudi += f"""    if out_arr_inds_{jwvm__nhnri}[i] not in kept_cols_set: continue
"""
            hcd__ghudi += f"""    ensure_column_unboxed(T1, in_arr_list_{jwvm__nhnri}, in_offset_{jwvm__nhnri}, in_arr_ind_{jwvm__nhnri})
"""
            hcd__ghudi += f"""    out_arr_list_{jwvm__nhnri}[i] = in_arr_list_{jwvm__nhnri}[in_offset_{jwvm__nhnri}]
"""
        for i, rezq__buffz in enumerate(out_table_type.block_to_arr_ind[
            jwvm__nhnri]):
            if rezq__buffz not in kept_cols:
                continue
            iuh__bpuk = in_col_inds[rezq__buffz]
            if iuh__bpuk >= qflzq__siewp:
                hcd__ghudi += f"""  out_arr_list_{jwvm__nhnri}[{i}] = extra_arrs_t[{iuh__bpuk - qflzq__siewp}]
"""
        hcd__ghudi += (
            f'  T2 = set_table_block(T2, out_arr_list_{jwvm__nhnri}, {jwvm__nhnri})\n'
            )
    hcd__ghudi += f'  return T2\n'
    glbls.update({'alloc_list_like': alloc_list_like, 'set_table_block':
        set_table_block, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'get_series_data':
        bodo.hiframes.pd_series_ext.get_series_data})
    ybmck__vum = {}
    exec(hcd__ghudi, glbls, ybmck__vum)
    return ybmck__vum['impl']


def _logical_tuple_table_to_table_codegen(in_table_t, extra_arrs_t,
    in_col_inds, kept_cols, n_table_cols_t, out_table_type_t,
    extra_arrs_no_series):
    qflzq__siewp = get_overload_const_int(n_table_cols_t
        ) if is_overload_constant_int(n_table_cols_t) else len(in_table_t.types
        )
    out_table_type = TableType(tuple(in_table_t.types[i] if i <
        qflzq__siewp else _to_arr_if_series(extra_arrs_t.types[i -
        qflzq__siewp]) for i in in_col_inds)) if is_overload_none(
        out_table_type_t) else unwrap_typeref(out_table_type_t)
    aoxg__ohqdt = None
    if not is_overload_none(in_table_t):
        for i, t in enumerate(in_table_t.types):
            if t != types.none:
                aoxg__ohqdt = f'in_table_t[{i}]'
                break
    if aoxg__ohqdt is None:
        for i, t in enumerate(extra_arrs_t.types):
            if t != types.none:
                aoxg__ohqdt = f'extra_arrs_t[{i}]'
                break
    assert aoxg__ohqdt is not None, 'no array found in input data'
    hcd__ghudi = """def impl(in_table_t, extra_arrs_t, in_col_inds_t, n_table_cols_t, out_table_type_t=None, used_cols=None):
"""
    if any(isinstance(t, SeriesType) for t in extra_arrs_t.types):
        hcd__ghudi += f'  extra_arrs_t = {extra_arrs_no_series}\n'
    hcd__ghudi += f'  T1 = in_table_t\n'
    hcd__ghudi += f'  T2 = init_table(out_table_type, False)\n'
    hcd__ghudi += f'  T2 = set_table_len(T2, len({aoxg__ohqdt}))\n'
    glbls = {}
    for typ, jwvm__nhnri in out_table_type.type_to_blk.items():
        glbls[f'arr_list_typ_{jwvm__nhnri}'] = types.List(typ)
        djom__edco = len(out_table_type.block_to_arr_ind[jwvm__nhnri])
        hcd__ghudi += f"""  out_arr_list_{jwvm__nhnri} = alloc_list_like(arr_list_typ_{jwvm__nhnri}, {djom__edco}, False)
"""
        for i, rezq__buffz in enumerate(out_table_type.block_to_arr_ind[
            jwvm__nhnri]):
            if rezq__buffz not in kept_cols:
                continue
            iuh__bpuk = in_col_inds[rezq__buffz]
            if iuh__bpuk < qflzq__siewp:
                hcd__ghudi += (
                    f'  out_arr_list_{jwvm__nhnri}[{i}] = T1[{iuh__bpuk}]\n')
            else:
                hcd__ghudi += f"""  out_arr_list_{jwvm__nhnri}[{i}] = extra_arrs_t[{iuh__bpuk - qflzq__siewp}]
"""
        hcd__ghudi += (
            f'  T2 = set_table_block(T2, out_arr_list_{jwvm__nhnri}, {jwvm__nhnri})\n'
            )
    hcd__ghudi += f'  return T2\n'
    glbls.update({'init_table': init_table, 'alloc_list_like':
        alloc_list_like, 'set_table_block': set_table_block,
        'set_table_len': set_table_len, 'out_table_type': out_table_type,
        'get_series_data': bodo.hiframes.pd_series_ext.get_series_data})
    ybmck__vum = {}
    exec(hcd__ghudi, glbls, ybmck__vum)
    return ybmck__vum['impl']


def logical_table_to_table_equiv(self, scope, equiv_set, loc, args, kws):
    npg__yzk = args[0]
    vcawr__wgyow = args[1]
    if equiv_set.has_shape(npg__yzk):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            npg__yzk)[0], None), pre=[])
    if equiv_set.has_shape(vcawr__wgyow):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            vcawr__wgyow)[0], None), pre=[])


(ArrayAnalysis._analyze_op_call_bodo_hiframes_table_logical_table_to_table
    ) = logical_table_to_table_equiv


def alias_ext_logical_table_to_table(lhs_name, args, alias_map, arg_aliases):
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['logical_table_to_table',
    'bodo.hiframes.table'] = alias_ext_logical_table_to_table
