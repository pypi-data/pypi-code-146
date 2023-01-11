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
            zddok__rmzf = 0
            tipj__zoes = []
            for i in range(usecols[-1] + 1):
                if i == usecols[zddok__rmzf]:
                    tipj__zoes.append(arrs[zddok__rmzf])
                    zddok__rmzf += 1
                else:
                    tipj__zoes.append(None)
            for jcu__ayb in range(usecols[-1] + 1, num_arrs):
                tipj__zoes.append(None)
            self.arrays = tipj__zoes
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((pateb__txhgm == pfwwb__uvur).all() for 
            pateb__txhgm, pfwwb__uvur in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        tgto__qgsui = len(self.arrays)
        wkd__hlk = dict(zip(range(tgto__qgsui), self.arrays))
        df = pd.DataFrame(wkd__hlk, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        qvygt__zwb = []
        abu__cxx = []
        dzdw__abo = {}
        pouy__wlo = {}
        djs__ynw = defaultdict(int)
        asoqg__aarc = defaultdict(list)
        if not has_runtime_cols:
            for i, t in enumerate(arr_types):
                if t not in dzdw__abo:
                    zqn__ydbxh = len(dzdw__abo)
                    dzdw__abo[t] = zqn__ydbxh
                    pouy__wlo[zqn__ydbxh] = t
                xpa__jvaj = dzdw__abo[t]
                qvygt__zwb.append(xpa__jvaj)
                abu__cxx.append(djs__ynw[xpa__jvaj])
                djs__ynw[xpa__jvaj] += 1
                asoqg__aarc[xpa__jvaj].append(i)
        self.block_nums = qvygt__zwb
        self.block_offsets = abu__cxx
        self.type_to_blk = dzdw__abo
        self.blk_to_type = pouy__wlo
        self.block_to_arr_ind = asoqg__aarc
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
            enqx__flumv = [(f'block_{i}', types.List(t)) for i, t in
                enumerate(fe_type.arr_types)]
        else:
            enqx__flumv = [(f'block_{xpa__jvaj}', types.List(t)) for t,
                xpa__jvaj in fe_type.type_to_blk.items()]
        enqx__flumv.append(('parent', types.pyobject))
        enqx__flumv.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, enqx__flumv)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    iczis__fof = c.pyapi.object_getattr_string(val, 'arrays')
    table = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    table.parent = cgutils.get_null_value(table.parent.type)
    usi__pnvv = c.pyapi.make_none()
    cgagw__piqch = c.context.get_constant(types.int64, 0)
    btrx__ppd = cgutils.alloca_once_value(c.builder, cgagw__piqch)
    for t, xpa__jvaj in typ.type_to_blk.items():
        yxqly__tesxs = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[xpa__jvaj]))
        jcu__ayb, oyfx__vtas = ListInstance.allocate_ex(c.context, c.
            builder, types.List(t), yxqly__tesxs)
        oyfx__vtas.size = yxqly__tesxs
        guwf__btimd = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[xpa__jvaj],
            dtype=np.int64))
        psy__cprqs = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, guwf__btimd)
        with cgutils.for_range(c.builder, yxqly__tesxs) as znen__gssv:
            i = znen__gssv.index
            ytjsw__xceu = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), psy__cprqs, i)
            tult__koqlc = c.pyapi.long_from_longlong(ytjsw__xceu)
            sqgpx__fzk = c.pyapi.object_getitem(iczis__fof, tult__koqlc)
            rvn__yoc = c.builder.icmp_unsigned('==', sqgpx__fzk, usi__pnvv)
            with c.builder.if_else(rvn__yoc) as (jgk__lwqu, mfhc__ogll):
                with jgk__lwqu:
                    hnv__ksmtj = c.context.get_constant_null(t)
                    oyfx__vtas.inititem(i, hnv__ksmtj, incref=False)
                with mfhc__ogll:
                    xire__wmdk = c.pyapi.call_method(sqgpx__fzk, '__len__', ())
                    vizhi__jyfu = c.pyapi.long_as_longlong(xire__wmdk)
                    c.builder.store(vizhi__jyfu, btrx__ppd)
                    c.pyapi.decref(xire__wmdk)
                    arr = c.pyapi.to_native_value(t, sqgpx__fzk).value
                    oyfx__vtas.inititem(i, arr, incref=False)
            c.pyapi.decref(sqgpx__fzk)
            c.pyapi.decref(tult__koqlc)
        setattr(table, f'block_{xpa__jvaj}', oyfx__vtas.value)
    table.len = c.builder.load(btrx__ppd)
    c.pyapi.decref(iczis__fof)
    c.pyapi.decref(usi__pnvv)
    omq__xwr = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(table._getvalue(), is_error=omq__xwr)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    table = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        pwk__urzh = c.context.get_constant(types.int64, 0)
        for i, t in enumerate(typ.arr_types):
            tipj__zoes = getattr(table, f'block_{i}')
            ocq__njia = ListInstance(c.context, c.builder, types.List(t),
                tipj__zoes)
            pwk__urzh = c.builder.add(pwk__urzh, ocq__njia.size)
        imh__bfvif = c.pyapi.list_new(pwk__urzh)
        vzukj__fulus = c.context.get_constant(types.int64, 0)
        for i, t in enumerate(typ.arr_types):
            tipj__zoes = getattr(table, f'block_{i}')
            ocq__njia = ListInstance(c.context, c.builder, types.List(t),
                tipj__zoes)
            with cgutils.for_range(c.builder, ocq__njia.size) as znen__gssv:
                i = znen__gssv.index
                arr = ocq__njia.getitem(i)
                c.context.nrt.incref(c.builder, t, arr)
                idx = c.builder.add(vzukj__fulus, i)
                c.pyapi.list_setitem(imh__bfvif, idx, c.pyapi.
                    from_native_value(t, arr, c.env_manager))
            vzukj__fulus = c.builder.add(vzukj__fulus, ocq__njia.size)
        mmu__lolqt = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        ojlvv__wzf = c.pyapi.call_function_objargs(mmu__lolqt, (imh__bfvif,))
        c.pyapi.decref(mmu__lolqt)
        c.pyapi.decref(imh__bfvif)
        c.context.nrt.decref(c.builder, typ, val)
        return ojlvv__wzf
    imh__bfvif = c.pyapi.list_new(c.context.get_constant(types.int64, len(
        typ.arr_types)))
    ixcrk__vfuw = cgutils.is_not_null(c.builder, table.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for t, xpa__jvaj in typ.type_to_blk.items():
        tipj__zoes = getattr(table, f'block_{xpa__jvaj}')
        ocq__njia = ListInstance(c.context, c.builder, types.List(t),
            tipj__zoes)
        guwf__btimd = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[xpa__jvaj],
            dtype=np.int64))
        psy__cprqs = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, guwf__btimd)
        with cgutils.for_range(c.builder, ocq__njia.size) as znen__gssv:
            i = znen__gssv.index
            ytjsw__xceu = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), psy__cprqs, i)
            arr = ocq__njia.getitem(i)
            nrdvt__nwz = cgutils.alloca_once_value(c.builder, arr)
            mey__qzv = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(t))
            is_null = is_ll_eq(c.builder, nrdvt__nwz, mey__qzv)
            with c.builder.if_else(c.builder.and_(is_null, c.builder.not_(
                ensure_unboxed))) as (jgk__lwqu, mfhc__ogll):
                with jgk__lwqu:
                    usi__pnvv = c.pyapi.make_none()
                    c.pyapi.list_setitem(imh__bfvif, ytjsw__xceu, usi__pnvv)
                with mfhc__ogll:
                    sqgpx__fzk = cgutils.alloca_once(c.builder, c.context.
                        get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(is_null, ixcrk__vfuw)
                        ) as (yxkq__kur, aaq__wcuo):
                        with yxkq__kur:
                            cnno__ndibs = get_df_obj_column_codegen(c.
                                context, c.builder, c.pyapi, table.parent,
                                ytjsw__xceu, t)
                            c.builder.store(cnno__ndibs, sqgpx__fzk)
                        with aaq__wcuo:
                            c.context.nrt.incref(c.builder, t, arr)
                            c.builder.store(c.pyapi.from_native_value(t,
                                arr, c.env_manager), sqgpx__fzk)
                    c.pyapi.list_setitem(imh__bfvif, ytjsw__xceu, c.builder
                        .load(sqgpx__fzk))
    mmu__lolqt = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    ojlvv__wzf = c.pyapi.call_function_objargs(mmu__lolqt, (imh__bfvif,))
    c.pyapi.decref(mmu__lolqt)
    c.pyapi.decref(imh__bfvif)
    c.context.nrt.decref(c.builder, typ, val)
    return ojlvv__wzf


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
        livjv__vwua = context.get_constant(types.int64, 0)
        for i, t in enumerate(table_type.arr_types):
            tipj__zoes = getattr(table, f'block_{i}')
            ocq__njia = ListInstance(context, builder, types.List(t),
                tipj__zoes)
            livjv__vwua = builder.add(livjv__vwua, ocq__njia.size)
        return livjv__vwua
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    table = cgutils.create_struct_proxy(table_type)(context, builder, table_arg
        )
    xpa__jvaj = table_type.block_nums[col_ind]
    ewsd__yhzkc = table_type.block_offsets[col_ind]
    tipj__zoes = getattr(table, f'block_{xpa__jvaj}')
    grl__rvaiu = types.none(table_type, types.List(arr_type), types.int64,
        types.int64)
    urzs__bxk = context.get_constant(types.int64, col_ind)
    wjvcw__tbwan = context.get_constant(types.int64, ewsd__yhzkc)
    hqazx__rajzv = table_arg, tipj__zoes, wjvcw__tbwan, urzs__bxk
    ensure_column_unboxed_codegen(context, builder, grl__rvaiu, hqazx__rajzv)
    ocq__njia = ListInstance(context, builder, types.List(arr_type), tipj__zoes
        )
    arr = ocq__njia.getitem(ewsd__yhzkc)
    return arr


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, jcu__ayb = args
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
    gvk__syk = list(ind_typ.instance_type.meta)
    jvul__wgyjg = defaultdict(list)
    for ind in gvk__syk:
        jvul__wgyjg[table_type.block_nums[ind]].append(table_type.
            block_offsets[ind])

    def codegen(context, builder, sig, args):
        table_arg, jcu__ayb = args
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        for xpa__jvaj, uqn__qkrs in jvul__wgyjg.items():
            arr_type = table_type.blk_to_type[xpa__jvaj]
            tipj__zoes = getattr(table, f'block_{xpa__jvaj}')
            ocq__njia = ListInstance(context, builder, types.List(arr_type),
                tipj__zoes)
            hnv__ksmtj = context.get_constant_null(arr_type)
            if len(uqn__qkrs) == 1:
                ewsd__yhzkc = uqn__qkrs[0]
                arr = ocq__njia.getitem(ewsd__yhzkc)
                context.nrt.decref(builder, arr_type, arr)
                ocq__njia.inititem(ewsd__yhzkc, hnv__ksmtj, incref=False)
            else:
                yxqly__tesxs = context.get_constant(types.int64, len(uqn__qkrs)
                    )
                yjhn__nolr = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(uqn__qkrs, dtype=
                    np.int64))
                htx__jym = context.make_array(types.Array(types.int64, 1, 'C')
                    )(context, builder, yjhn__nolr)
                with cgutils.for_range(builder, yxqly__tesxs) as znen__gssv:
                    i = znen__gssv.index
                    ewsd__yhzkc = _getitem_array_single_int(context,
                        builder, types.int64, types.Array(types.int64, 1,
                        'C'), htx__jym, i)
                    arr = ocq__njia.getitem(ewsd__yhzkc)
                    context.nrt.decref(builder, arr_type, arr)
                    ocq__njia.inititem(ewsd__yhzkc, hnv__ksmtj, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    cgagw__piqch = context.get_constant(types.int64, 0)
    kso__mime = context.get_constant(types.int64, 1)
    wons__ddor = arr_type not in in_table_type.type_to_blk
    for t, xpa__jvaj in out_table_type.type_to_blk.items():
        if t in in_table_type.type_to_blk:
            lfqe__puvla = in_table_type.type_to_blk[t]
            oyfx__vtas = ListInstance(context, builder, types.List(t),
                getattr(in_table, f'block_{lfqe__puvla}'))
            context.nrt.incref(builder, types.List(t), oyfx__vtas.value)
            setattr(out_table, f'block_{xpa__jvaj}', oyfx__vtas.value)
    if wons__ddor:
        jcu__ayb, oyfx__vtas = ListInstance.allocate_ex(context, builder,
            types.List(arr_type), kso__mime)
        oyfx__vtas.size = kso__mime
        oyfx__vtas.inititem(cgagw__piqch, arr_arg, incref=True)
        xpa__jvaj = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{xpa__jvaj}', oyfx__vtas.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        xpa__jvaj = out_table_type.type_to_blk[arr_type]
        oyfx__vtas = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{xpa__jvaj}'))
        if is_new_col:
            n = oyfx__vtas.size
            gomp__inodf = builder.add(n, kso__mime)
            oyfx__vtas.resize(gomp__inodf)
            oyfx__vtas.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            mjm__odk = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            oyfx__vtas.setitem(mjm__odk, arr_arg, incref=True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            mjm__odk = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            n = oyfx__vtas.size
            gomp__inodf = builder.add(n, kso__mime)
            oyfx__vtas.resize(gomp__inodf)
            context.nrt.incref(builder, arr_type, oyfx__vtas.getitem(mjm__odk))
            oyfx__vtas.move(builder.add(mjm__odk, kso__mime), mjm__odk,
                builder.sub(n, mjm__odk))
            oyfx__vtas.setitem(mjm__odk, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    qrljb__ssk = in_table_type.arr_types[col_ind]
    if qrljb__ssk in out_table_type.type_to_blk:
        xpa__jvaj = out_table_type.type_to_blk[qrljb__ssk]
        swrm__srsde = getattr(out_table, f'block_{xpa__jvaj}')
        rvxx__owjyd = types.List(qrljb__ssk)
        mjm__odk = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        jqkne__blfer = rvxx__owjyd.dtype(rvxx__owjyd, types.intp)
        dvln__xqes = context.compile_internal(builder, lambda lst, i: lst.
            pop(i), jqkne__blfer, (swrm__srsde, mjm__odk))
        context.nrt.decref(builder, qrljb__ssk, dvln__xqes)


def generate_set_table_data_code(table, ind, arr_type, used_cols, is_null=False
    ):
    kubab__pfzqd = list(table.arr_types)
    if ind == len(kubab__pfzqd):
        dkc__zxa = None
        kubab__pfzqd.append(arr_type)
    else:
        dkc__zxa = table.arr_types[ind]
        kubab__pfzqd[ind] = arr_type
    itea__cmpw = TableType(tuple(kubab__pfzqd))
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'set_table_parent': set_table_parent, 'alloc_list_like':
        alloc_list_like, 'out_table_typ': itea__cmpw}
    ahch__wotgy = 'def set_table_data(table, ind, arr, used_cols=None):\n'
    ahch__wotgy += f'  T2 = init_table(out_table_typ, False)\n'
    ahch__wotgy += f'  T2 = set_table_len(T2, len(table))\n'
    ahch__wotgy += f'  T2 = set_table_parent(T2, table)\n'
    for typ, xpa__jvaj in itea__cmpw.type_to_blk.items():
        if typ in table.type_to_blk:
            hotfw__bhl = table.type_to_blk[typ]
            ahch__wotgy += (
                f'  arr_list_{xpa__jvaj} = get_table_block(table, {hotfw__bhl})\n'
                )
            ahch__wotgy += f"""  out_arr_list_{xpa__jvaj} = alloc_list_like(arr_list_{xpa__jvaj}, {len(itea__cmpw.block_to_arr_ind[xpa__jvaj])}, False)
"""
            if used_cols is None or set(table.block_to_arr_ind[hotfw__bhl]
                ) & used_cols:
                ahch__wotgy += (
                    f'  for i in range(len(arr_list_{xpa__jvaj})):\n')
                if typ not in (dkc__zxa, arr_type):
                    ahch__wotgy += (
                        f'    out_arr_list_{xpa__jvaj}[i] = arr_list_{xpa__jvaj}[i]\n'
                        )
                else:
                    rwv__dila = table.block_to_arr_ind[hotfw__bhl]
                    xtmyk__iqu = np.empty(len(rwv__dila), np.int64)
                    jmjx__fty = False
                    for qmq__ireh, ytjsw__xceu in enumerate(rwv__dila):
                        if ytjsw__xceu != ind:
                            oeptv__bkrq = itea__cmpw.block_offsets[ytjsw__xceu]
                        else:
                            oeptv__bkrq = -1
                            jmjx__fty = True
                        xtmyk__iqu[qmq__ireh] = oeptv__bkrq
                    glbls[f'out_idxs_{xpa__jvaj}'] = np.array(xtmyk__iqu,
                        np.int64)
                    ahch__wotgy += f'    out_idx = out_idxs_{xpa__jvaj}[i]\n'
                    if jmjx__fty:
                        ahch__wotgy += f'    if out_idx == -1:\n'
                        ahch__wotgy += f'      continue\n'
                    ahch__wotgy += f"""    out_arr_list_{xpa__jvaj}[out_idx] = arr_list_{xpa__jvaj}[i]
"""
            if typ == arr_type and not is_null:
                ahch__wotgy += f"""  out_arr_list_{xpa__jvaj}[{itea__cmpw.block_offsets[ind]}] = arr
"""
        else:
            glbls[f'arr_list_typ_{xpa__jvaj}'] = types.List(arr_type)
            ahch__wotgy += f"""  out_arr_list_{xpa__jvaj} = alloc_list_like(arr_list_typ_{xpa__jvaj}, 1, False)
"""
            if not is_null:
                ahch__wotgy += f'  out_arr_list_{xpa__jvaj}[0] = arr\n'
        ahch__wotgy += (
            f'  T2 = set_table_block(T2, out_arr_list_{xpa__jvaj}, {xpa__jvaj})\n'
            )
    ahch__wotgy += f'  return T2\n'
    ytbu__xjp = {}
    exec(ahch__wotgy, glbls, ytbu__xjp)
    return ytbu__xjp['set_table_data']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def set_table_data(table, ind, arr, used_cols=None):
    if is_overload_none(used_cols):
        gvhuf__axx = None
    else:
        gvhuf__axx = set(used_cols.instance_type.meta)
    yidld__ilqf = get_overload_const_int(ind)
    return generate_set_table_data_code(table, yidld__ilqf, arr, gvhuf__axx)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def set_table_data_null(table, ind, arr, used_cols=None):
    yidld__ilqf = get_overload_const_int(ind)
    arr_type = arr.instance_type
    if is_overload_none(used_cols):
        gvhuf__axx = None
    else:
        gvhuf__axx = set(used_cols.instance_type.meta)
    return generate_set_table_data_code(table, yidld__ilqf, arr_type,
        gvhuf__axx, is_null=True)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_table_data',
    'bodo.hiframes.table'] = alias_ext_dummy_func


def get_table_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    zmi__lmm = args[0]
    if equiv_set.has_shape(zmi__lmm):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            zmi__lmm)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    khvyf__huopw = []
    for t, xpa__jvaj in table_type.type_to_blk.items():
        pwm__xoghg = len(table_type.block_to_arr_ind[xpa__jvaj])
        hbd__iatgg = []
        for i in range(pwm__xoghg):
            ytjsw__xceu = table_type.block_to_arr_ind[xpa__jvaj][i]
            hbd__iatgg.append(pyval.arrays[ytjsw__xceu])
        khvyf__huopw.append(context.get_constant_generic(builder, types.
            List(t), hbd__iatgg))
    jgcq__odl = context.get_constant_null(types.pyobject)
    rlgs__hvqq = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(khvyf__huopw + [jgcq__odl, rlgs__hvqq])


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
        for t, xpa__jvaj in out_table_type.type_to_blk.items():
            kvtqp__gvk = context.get_constant_null(types.List(t))
            setattr(table, f'block_{xpa__jvaj}', kvtqp__gvk)
        return table._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    qviyp__iir = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        qviyp__iir[typ.dtype] = i
    bxhs__dkace = table_type.instance_type if isinstance(table_type, types.
        TypeRef) else table_type
    assert isinstance(bxhs__dkace, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        jkxgy__ganoy, jcu__ayb = args
        table = cgutils.create_struct_proxy(bxhs__dkace)(context, builder)
        for t, xpa__jvaj in bxhs__dkace.type_to_blk.items():
            idx = qviyp__iir[t]
            bwojh__gzg = signature(types.List(t), tuple_of_lists_type,
                types.literal(idx))
            hexa__ghju = jkxgy__ganoy, idx
            wfooe__nfqs = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, bwojh__gzg, hexa__ghju)
            setattr(table, f'block_{xpa__jvaj}', wfooe__nfqs)
        return table._getvalue()
    sig = bxhs__dkace(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    xpa__jvaj = get_overload_const_int(blk_type)
    arr_type = None
    for t, pfwwb__uvur in table_type.type_to_blk.items():
        if pfwwb__uvur == xpa__jvaj:
            arr_type = t
            break
    assert arr_type is not None, 'invalid table type block'
    xnjo__vlgyj = types.List(arr_type)

    def codegen(context, builder, sig, args):
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            args[0])
        tipj__zoes = getattr(table, f'block_{xpa__jvaj}')
        return impl_ret_borrowed(context, builder, xnjo__vlgyj, tipj__zoes)
    sig = xnjo__vlgyj(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, nhljk__xhh = args
        olm__akov = context.get_python_api(builder)
        tsu__sqy = used_cols_typ == types.none
        if not tsu__sqy:
            ryl__jkndr = numba.cpython.setobj.SetInstance(context, builder,
                types.Set(types.int64), nhljk__xhh)
        table = cgutils.create_struct_proxy(sig.args[0])(context, builder,
            table_arg)
        for t, xpa__jvaj in table_type.type_to_blk.items():
            yxqly__tesxs = context.get_constant(types.int64, len(table_type
                .block_to_arr_ind[xpa__jvaj]))
            guwf__btimd = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind[
                xpa__jvaj], dtype=np.int64))
            psy__cprqs = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, guwf__btimd)
            tipj__zoes = getattr(table, f'block_{xpa__jvaj}')
            with cgutils.for_range(builder, yxqly__tesxs) as znen__gssv:
                i = znen__gssv.index
                ytjsw__xceu = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    psy__cprqs, i)
                grl__rvaiu = types.none(table_type, types.List(t), types.
                    int64, types.int64)
                hqazx__rajzv = table_arg, tipj__zoes, i, ytjsw__xceu
                if tsu__sqy:
                    ensure_column_unboxed_codegen(context, builder,
                        grl__rvaiu, hqazx__rajzv)
                else:
                    vtzfw__aflxa = ryl__jkndr.contains(ytjsw__xceu)
                    with builder.if_then(vtzfw__aflxa):
                        ensure_column_unboxed_codegen(context, builder,
                            grl__rvaiu, hqazx__rajzv)
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
    table_arg, llz__guaud, pozo__irv, vbj__tuzj = args
    olm__akov = context.get_python_api(builder)
    table = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        table_arg)
    ixcrk__vfuw = cgutils.is_not_null(builder, table.parent)
    ocq__njia = ListInstance(context, builder, sig.args[1], llz__guaud)
    ttfk__wosrj = ocq__njia.getitem(pozo__irv)
    nrdvt__nwz = cgutils.alloca_once_value(builder, ttfk__wosrj)
    mey__qzv = cgutils.alloca_once_value(builder, context.get_constant_null
        (sig.args[1].dtype))
    is_null = is_ll_eq(builder, nrdvt__nwz, mey__qzv)
    with builder.if_then(is_null):
        with builder.if_else(ixcrk__vfuw) as (jgk__lwqu, mfhc__ogll):
            with jgk__lwqu:
                sqgpx__fzk = get_df_obj_column_codegen(context, builder,
                    olm__akov, table.parent, vbj__tuzj, sig.args[1].dtype)
                arr = olm__akov.to_native_value(sig.args[1].dtype, sqgpx__fzk
                    ).value
                ocq__njia.inititem(pozo__irv, arr, incref=False)
                olm__akov.decref(sqgpx__fzk)
            with mfhc__ogll:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    xpa__jvaj = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, hbrnu__mhj, jcu__ayb = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{xpa__jvaj}', hbrnu__mhj)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, fnl__uwjdw = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = fnl__uwjdw
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def set_table_parent(typingctx, out_table_type, in_table_type):
    assert isinstance(in_table_type, TableType), 'table type expected'
    assert isinstance(out_table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        gztu__qrao, ubkh__bzke = args
        in_table = cgutils.create_struct_proxy(in_table_type)(context,
            builder, ubkh__bzke)
        out_table = cgutils.create_struct_proxy(out_table_type)(context,
            builder, gztu__qrao)
        out_table.parent = in_table.parent
        context.nrt.incref(builder, types.pyobject, out_table.parent)
        return impl_ret_borrowed(context, builder, out_table_type,
            out_table._getvalue())
    sig = out_table_type(out_table_type, in_table_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, len_type, to_str_if_dict_t):
    xnjo__vlgyj = list_type.instance_type if isinstance(list_type, types.
        TypeRef) else list_type
    assert isinstance(xnjo__vlgyj, types.List), 'list type or typeref expected'
    assert isinstance(len_type, types.Integer), 'integer type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    if is_overload_true(to_str_if_dict_t):
        xnjo__vlgyj = types.List(to_str_arr_if_dict_array(xnjo__vlgyj.dtype))

    def codegen(context, builder, sig, args):
        trxo__oqxcc = args[1]
        jcu__ayb, oyfx__vtas = ListInstance.allocate_ex(context, builder,
            xnjo__vlgyj, trxo__oqxcc)
        oyfx__vtas.size = trxo__oqxcc
        return oyfx__vtas.value
    sig = xnjo__vlgyj(list_type, len_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    rlj__vhsp = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(rlj__vhsp)

    def codegen(context, builder, sig, args):
        trxo__oqxcc, jcu__ayb = args
        jcu__ayb, oyfx__vtas = ListInstance.allocate_ex(context, builder,
            list_type, trxo__oqxcc)
        oyfx__vtas.size = trxo__oqxcc
        return oyfx__vtas.value
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
        ehd__zcx = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(ehd__zcx)
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
        kxkk__grxa = used_cols.instance_type
        xzaq__clyb = np.array(kxkk__grxa.meta, dtype=np.int64)
        glbls['used_cols_vals'] = xzaq__clyb
        vxqd__nsa = set([T.block_nums[i] for i in xzaq__clyb])
    else:
        xzaq__clyb = None
    ahch__wotgy = 'def table_filter_func(T, idx, used_cols=None):\n'
    ahch__wotgy += f'  T2 = init_table(T, False)\n'
    ahch__wotgy += f'  l = 0\n'
    if xzaq__clyb is not None and len(xzaq__clyb) == 0:
        ahch__wotgy += f'  l = _get_idx_length(idx, len(T))\n'
        ahch__wotgy += f'  T2 = set_table_len(T2, l)\n'
        ahch__wotgy += f'  return T2\n'
        ytbu__xjp = {}
        exec(ahch__wotgy, glbls, ytbu__xjp)
        return ytbu__xjp['table_filter_func']
    if xzaq__clyb is not None:
        ahch__wotgy += f'  used_set = set(used_cols_vals)\n'
    for xpa__jvaj in T.type_to_blk.values():
        ahch__wotgy += (
            f'  arr_list_{xpa__jvaj} = get_table_block(T, {xpa__jvaj})\n')
        ahch__wotgy += f"""  out_arr_list_{xpa__jvaj} = alloc_list_like(arr_list_{xpa__jvaj}, len(arr_list_{xpa__jvaj}), False)
"""
        if xzaq__clyb is None or xpa__jvaj in vxqd__nsa:
            glbls[f'arr_inds_{xpa__jvaj}'] = np.array(T.block_to_arr_ind[
                xpa__jvaj], dtype=np.int64)
            ahch__wotgy += f'  for i in range(len(arr_list_{xpa__jvaj})):\n'
            ahch__wotgy += (
                f'    arr_ind_{xpa__jvaj} = arr_inds_{xpa__jvaj}[i]\n')
            if xzaq__clyb is not None:
                ahch__wotgy += (
                    f'    if arr_ind_{xpa__jvaj} not in used_set: continue\n')
            ahch__wotgy += f"""    ensure_column_unboxed(T, arr_list_{xpa__jvaj}, i, arr_ind_{xpa__jvaj})
"""
            ahch__wotgy += f"""    out_arr_{xpa__jvaj} = ensure_contig_if_np(arr_list_{xpa__jvaj}[i][idx])
"""
            ahch__wotgy += f'    l = len(out_arr_{xpa__jvaj})\n'
            ahch__wotgy += (
                f'    out_arr_list_{xpa__jvaj}[i] = out_arr_{xpa__jvaj}\n')
        ahch__wotgy += (
            f'  T2 = set_table_block(T2, out_arr_list_{xpa__jvaj}, {xpa__jvaj})\n'
            )
    ahch__wotgy += f'  T2 = set_table_len(T2, l)\n'
    ahch__wotgy += f'  return T2\n'
    ytbu__xjp = {}
    exec(ahch__wotgy, glbls, ytbu__xjp)
    return ytbu__xjp['table_filter_func']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_subset(T, idx, copy_arrs, used_cols=None):
    izau__aru = list(idx.instance_type.meta)
    kubab__pfzqd = tuple(np.array(T.arr_types, dtype=object)[izau__aru])
    itea__cmpw = TableType(kubab__pfzqd)
    if not is_overload_constant_bool(copy_arrs):
        raise_bodo_error('table_subset(): copy_arrs must be a constant')
    izjsm__huw = is_overload_true(copy_arrs)
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'set_table_block':
        set_table_block, 'set_table_len': set_table_len, 'alloc_list_like':
        alloc_list_like, 'out_table_typ': itea__cmpw}
    if not is_overload_none(used_cols):
        kept_cols = used_cols.instance_type.meta
        jfvh__aktt = set(kept_cols)
        glbls['kept_cols'] = np.array(kept_cols, np.int64)
        aqj__whk = True
    else:
        aqj__whk = False
    mies__laipn = {i: c for i, c in enumerate(izau__aru)}
    ahch__wotgy = 'def table_subset(T, idx, copy_arrs, used_cols=None):\n'
    ahch__wotgy += f'  T2 = init_table(out_table_typ, False)\n'
    ahch__wotgy += f'  T2 = set_table_len(T2, len(T))\n'
    if aqj__whk and len(jfvh__aktt) == 0:
        ahch__wotgy += f'  return T2\n'
        ytbu__xjp = {}
        exec(ahch__wotgy, glbls, ytbu__xjp)
        return ytbu__xjp['table_subset']
    if aqj__whk:
        ahch__wotgy += f'  kept_cols_set = set(kept_cols)\n'
    for typ, xpa__jvaj in itea__cmpw.type_to_blk.items():
        hotfw__bhl = T.type_to_blk[typ]
        ahch__wotgy += (
            f'  arr_list_{xpa__jvaj} = get_table_block(T, {hotfw__bhl})\n')
        ahch__wotgy += f"""  out_arr_list_{xpa__jvaj} = alloc_list_like(arr_list_{xpa__jvaj}, {len(itea__cmpw.block_to_arr_ind[xpa__jvaj])}, False)
"""
        cev__corek = True
        if aqj__whk:
            mrld__egcuy = set(itea__cmpw.block_to_arr_ind[xpa__jvaj])
            scpk__sfm = mrld__egcuy & jfvh__aktt
            cev__corek = len(scpk__sfm) > 0
        if cev__corek:
            glbls[f'out_arr_inds_{xpa__jvaj}'] = np.array(itea__cmpw.
                block_to_arr_ind[xpa__jvaj], dtype=np.int64)
            ahch__wotgy += (
                f'  for i in range(len(out_arr_list_{xpa__jvaj})):\n')
            ahch__wotgy += (
                f'    out_arr_ind_{xpa__jvaj} = out_arr_inds_{xpa__jvaj}[i]\n')
            if aqj__whk:
                ahch__wotgy += (
                    f'    if out_arr_ind_{xpa__jvaj} not in kept_cols_set: continue\n'
                    )
            iziue__izls = []
            fhf__ozhkb = []
            for smlpw__dst in itea__cmpw.block_to_arr_ind[xpa__jvaj]:
                ifu__ybcxl = mies__laipn[smlpw__dst]
                iziue__izls.append(ifu__ybcxl)
                bwqh__ejakb = T.block_offsets[ifu__ybcxl]
                fhf__ozhkb.append(bwqh__ejakb)
            glbls[f'in_logical_idx_{xpa__jvaj}'] = np.array(iziue__izls,
                dtype=np.int64)
            glbls[f'in_physical_idx_{xpa__jvaj}'] = np.array(fhf__ozhkb,
                dtype=np.int64)
            ahch__wotgy += (
                f'    logical_idx_{xpa__jvaj} = in_logical_idx_{xpa__jvaj}[i]\n'
                )
            ahch__wotgy += (
                f'    physical_idx_{xpa__jvaj} = in_physical_idx_{xpa__jvaj}[i]\n'
                )
            ahch__wotgy += f"""    ensure_column_unboxed(T, arr_list_{xpa__jvaj}, physical_idx_{xpa__jvaj}, logical_idx_{xpa__jvaj})
"""
            qmclg__lpfj = '.copy()' if izjsm__huw else ''
            ahch__wotgy += f"""    out_arr_list_{xpa__jvaj}[i] = arr_list_{xpa__jvaj}[physical_idx_{xpa__jvaj}]{qmclg__lpfj}
"""
        ahch__wotgy += (
            f'  T2 = set_table_block(T2, out_arr_list_{xpa__jvaj}, {xpa__jvaj})\n'
            )
    ahch__wotgy += f'  return T2\n'
    ytbu__xjp = {}
    exec(ahch__wotgy, glbls, ytbu__xjp)
    return ytbu__xjp['table_subset']


def table_filter_equiv(self, scope, equiv_set, loc, args, kws):
    zmi__lmm = args[0]
    if equiv_set.has_shape(zmi__lmm):
        if guard(is_whole_slice, self.typemap, self.func_ir, args[1]):
            return ArrayAnalysis.AnalyzeResult(shape=zmi__lmm, pre=[])
        return ArrayAnalysis.AnalyzeResult(shape=(None, equiv_set.get_shape
            (zmi__lmm)[1]), pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_table_filter = (
    table_filter_equiv)


def table_subset_equiv(self, scope, equiv_set, loc, args, kws):
    zmi__lmm = args[0]
    if equiv_set.has_shape(zmi__lmm):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            zmi__lmm)[0], None), pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_table_subset = (
    table_subset_equiv)


def gen_str_and_dict_enc_cols_to_one_block_fn_txt(in_table_type,
    out_table_type, glbls, is_gatherv=False):
    assert bodo.string_array_type in in_table_type.type_to_blk and bodo.string_array_type in in_table_type.type_to_blk, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: Table type {in_table_type} does not contain both a string, and encoded string column'
    sjitp__qlafo = in_table_type.type_to_blk[bodo.string_array_type]
    grl__ulevo = in_table_type.type_to_blk[bodo.dict_str_arr_type]
    rquza__cogkx = in_table_type.block_to_arr_ind.get(sjitp__qlafo)
    qquja__nrrn = in_table_type.block_to_arr_ind.get(grl__ulevo)
    dlda__vkxc = []
    cjjva__krruq = []
    yaf__fjdmm = 0
    onbcr__mgbh = 0
    for zrfy__zep in range(len(rquza__cogkx) + len(qquja__nrrn)):
        if yaf__fjdmm == len(rquza__cogkx):
            cjjva__krruq.append(zrfy__zep)
            continue
        elif onbcr__mgbh == len(qquja__nrrn):
            dlda__vkxc.append(zrfy__zep)
            continue
        jlma__xdp = rquza__cogkx[yaf__fjdmm]
        dbm__nhl = qquja__nrrn[onbcr__mgbh]
        if jlma__xdp < dbm__nhl:
            dlda__vkxc.append(zrfy__zep)
            yaf__fjdmm += 1
        else:
            cjjva__krruq.append(zrfy__zep)
            onbcr__mgbh += 1
    assert 'output_table_str_arr_offsets_in_combined_block' not in glbls, "Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: key 'output_table_str_arr_idxs_in_combined_block' already present as a global variable"
    glbls['output_table_str_arr_offsets_in_combined_block'] = np.array(
        dlda__vkxc)
    assert 'output_table_dict_enc_str_arr_offsets_in_combined_block' not in glbls, "Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: key 'output_table_str_arr_idxs_in_combined_block' already present as a global variable"
    glbls['output_table_dict_enc_str_arr_offsets_in_combined_block'
        ] = np.array(cjjva__krruq)
    glbls['decode_if_dict_array'] = decode_if_dict_array
    bnuya__kemnj = out_table_type.type_to_blk[bodo.string_array_type]
    assert f'arr_inds_{sjitp__qlafo}' not in glbls, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: arr_inds_{sjitp__qlafo} already present in global variables'
    glbls[f'arr_inds_{sjitp__qlafo}'] = np.array(in_table_type.
        block_to_arr_ind[sjitp__qlafo], dtype=np.int64)
    assert f'arr_inds_{grl__ulevo}' not in glbls, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: arr_inds_{grl__ulevo} already present in global variables'
    glbls[f'arr_inds_{grl__ulevo}'] = np.array(in_table_type.
        block_to_arr_ind[grl__ulevo], dtype=np.int64)
    ahch__wotgy = (
        f'  input_str_arr_list = get_table_block(T, {sjitp__qlafo})\n')
    ahch__wotgy += (
        f'  input_dict_enc_str_arr_list = get_table_block(T, {grl__ulevo})\n')
    ahch__wotgy += f"""  out_arr_list_{bnuya__kemnj} = alloc_list_like(input_str_arr_list, {len(dlda__vkxc) + len(cjjva__krruq)}, True)
"""
    ahch__wotgy += f"""  for input_str_ary_idx, output_str_arr_offset in enumerate(output_table_str_arr_offsets_in_combined_block):
"""
    ahch__wotgy += (
        f'    arr_ind_str = arr_inds_{sjitp__qlafo}[input_str_ary_idx]\n')
    ahch__wotgy += f"""    ensure_column_unboxed(T, input_str_arr_list, input_str_ary_idx, arr_ind_str)
"""
    ahch__wotgy += f'    out_arr_str = input_str_arr_list[input_str_ary_idx]\n'
    if is_gatherv:
        ahch__wotgy += f"""    out_arr_str = bodo.gatherv(out_arr_str, allgather, warn_if_rep, root)
"""
    ahch__wotgy += (
        f'    out_arr_list_{bnuya__kemnj}[output_str_arr_offset] = out_arr_str\n'
        )
    ahch__wotgy += f"""  for input_dict_enc_str_ary_idx, output_dict_enc_str_arr_offset in enumerate(output_table_dict_enc_str_arr_offsets_in_combined_block):
"""
    ahch__wotgy += (
        f'    arr_ind_dict_enc_str = arr_inds_{grl__ulevo}[input_dict_enc_str_ary_idx]\n'
        )
    ahch__wotgy += f"""    ensure_column_unboxed(T, input_dict_enc_str_arr_list, input_dict_enc_str_ary_idx, arr_ind_dict_enc_str)
"""
    ahch__wotgy += f"""    out_arr_dict_enc_str = decode_if_dict_array(input_dict_enc_str_arr_list[input_dict_enc_str_ary_idx])
"""
    if is_gatherv:
        ahch__wotgy += f"""    out_arr_dict_enc_str = bodo.gatherv(out_arr_dict_enc_str, allgather, warn_if_rep, root)
"""
    ahch__wotgy += f"""    out_arr_list_{bnuya__kemnj}[output_dict_enc_str_arr_offset] = out_arr_dict_enc_str
"""
    ahch__wotgy += (
        f'  T2 = set_table_block(T2, out_arr_list_{bnuya__kemnj}, {bnuya__kemnj})\n'
        )
    return ahch__wotgy


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    ahch__wotgy = 'def impl(T):\n'
    ahch__wotgy += f'  T2 = init_table(T, True)\n'
    ahch__wotgy += f'  l = len(T)\n'
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'set_table_block':
        set_table_block, 'set_table_len': set_table_len, 'alloc_list_like':
        alloc_list_like, 'decode_if_dict_array': decode_if_dict_array}
    out_table_type = bodo.hiframes.table.get_init_table_output_type(T, True)
    dsqbk__ytp = (bodo.string_array_type in T.type_to_blk and bodo.
        dict_str_arr_type in T.type_to_blk)
    if dsqbk__ytp:
        ahch__wotgy += gen_str_and_dict_enc_cols_to_one_block_fn_txt(T,
            out_table_type, glbls)
    for typ, bqlhi__uief in T.type_to_blk.items():
        if dsqbk__ytp and typ in (bodo.string_array_type, bodo.
            dict_str_arr_type):
            continue
        if typ == bodo.dict_str_arr_type:
            assert bodo.string_array_type in out_table_type.type_to_blk, 'Error in decode_if_dict_table: If encoded string type is present in the input, then non-encoded string type should be present in the output'
            cfc__gcx = out_table_type.type_to_blk[bodo.string_array_type]
        else:
            assert typ in out_table_type.type_to_blk, 'Error in decode_if_dict_table: All non-encoded string types present in the input should be present in the output'
            cfc__gcx = out_table_type.type_to_blk[typ]
        glbls[f'arr_inds_{bqlhi__uief}'] = np.array(T.block_to_arr_ind[
            bqlhi__uief], dtype=np.int64)
        ahch__wotgy += (
            f'  arr_list_{bqlhi__uief} = get_table_block(T, {bqlhi__uief})\n')
        ahch__wotgy += f"""  out_arr_list_{bqlhi__uief} = alloc_list_like(arr_list_{bqlhi__uief}, len(arr_list_{bqlhi__uief}), True)
"""
        ahch__wotgy += f'  for i in range(len(arr_list_{bqlhi__uief})):\n'
        ahch__wotgy += (
            f'    arr_ind_{bqlhi__uief} = arr_inds_{bqlhi__uief}[i]\n')
        ahch__wotgy += f"""    ensure_column_unboxed(T, arr_list_{bqlhi__uief}, i, arr_ind_{bqlhi__uief})
"""
        ahch__wotgy += f"""    out_arr_{bqlhi__uief} = decode_if_dict_array(arr_list_{bqlhi__uief}[i])
"""
        ahch__wotgy += (
            f'    out_arr_list_{bqlhi__uief}[i] = out_arr_{bqlhi__uief}\n')
        ahch__wotgy += (
            f'  T2 = set_table_block(T2, out_arr_list_{bqlhi__uief}, {cfc__gcx})\n'
            )
    ahch__wotgy += f'  T2 = set_table_len(T2, l)\n'
    ahch__wotgy += f'  return T2\n'
    ytbu__xjp = {}
    exec(ahch__wotgy, glbls, ytbu__xjp)
    return ytbu__xjp['impl']


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
        fdrg__hcvo = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        fdrg__hcvo = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            fdrg__hcvo.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        ncbkc__fpj, urs__oqa = args
        table = cgutils.create_struct_proxy(table_type)(context, builder)
        table.len = urs__oqa
        khvyf__huopw = cgutils.unpack_tuple(builder, ncbkc__fpj)
        for i, tipj__zoes in enumerate(khvyf__huopw):
            setattr(table, f'block_{i}', tipj__zoes)
            context.nrt.incref(builder, types.List(fdrg__hcvo[i]), tipj__zoes)
        return table._getvalue()
    table_type = TableType(tuple(fdrg__hcvo), True)
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
        aqj__whk = True
    else:
        kept_cols = set(np.arange(len(in_col_inds)))
        aqj__whk = False
    extra_arrs_no_series = ', '.join(f'get_series_data(extra_arrs_t[{i}])' if
        isinstance(extra_arrs_t[i], SeriesType) else f'extra_arrs_t[{i}]' for
        i in range(len(extra_arrs_t)))
    extra_arrs_no_series = (
        f"({extra_arrs_no_series}{',' if len(extra_arrs_t) == 1 else ''})")
    if isinstance(in_table_t, (types.BaseTuple, types.NoneType)):
        return _logical_tuple_table_to_table_codegen(in_table_t,
            extra_arrs_t, in_col_inds, kept_cols, n_table_cols_t,
            out_table_type_t, extra_arrs_no_series)
    amno__sdk = len(in_table_t.arr_types)
    out_table_type = TableType(tuple(in_table_t.arr_types[i] if i <
        amno__sdk else _to_arr_if_series(extra_arrs_t.types[i - amno__sdk]) for
        i in in_col_inds)) if is_overload_none(out_table_type_t
        ) else unwrap_typeref(out_table_type_t)
    glbls.update({'init_table': init_table, 'set_table_len': set_table_len,
        'out_table_type': out_table_type})
    ahch__wotgy = """def impl(in_table_t, extra_arrs_t, in_col_inds_t, n_table_cols_t, out_table_type_t=None, used_cols=None):
"""
    if any(isinstance(t, SeriesType) for t in extra_arrs_t.types):
        ahch__wotgy += f'  extra_arrs_t = {extra_arrs_no_series}\n'
    ahch__wotgy += f'  T1 = in_table_t\n'
    ahch__wotgy += f'  T2 = init_table(out_table_type, False)\n'
    ahch__wotgy += f'  T2 = set_table_len(T2, len(T1))\n'
    if aqj__whk and len(kept_cols) == 0:
        ahch__wotgy += f'  return T2\n'
        ytbu__xjp = {}
        exec(ahch__wotgy, glbls, ytbu__xjp)
        return ytbu__xjp['impl']
    if aqj__whk:
        ahch__wotgy += f'  kept_cols_set = set(kept_cols)\n'
    for typ, xpa__jvaj in out_table_type.type_to_blk.items():
        glbls[f'arr_list_typ_{xpa__jvaj}'] = types.List(typ)
        yxqly__tesxs = len(out_table_type.block_to_arr_ind[xpa__jvaj])
        ahch__wotgy += f"""  out_arr_list_{xpa__jvaj} = alloc_list_like(arr_list_typ_{xpa__jvaj}, {yxqly__tesxs}, False)
"""
        if typ in in_table_t.type_to_blk:
            fexk__cqgv = in_table_t.type_to_blk[typ]
            qug__hef = []
            rwd__tkwtd = []
            for klex__wrfx in out_table_type.block_to_arr_ind[xpa__jvaj]:
                cxpwg__janh = in_col_inds[klex__wrfx]
                if cxpwg__janh < amno__sdk:
                    qug__hef.append(in_table_t.block_offsets[cxpwg__janh])
                    rwd__tkwtd.append(cxpwg__janh)
                else:
                    qug__hef.append(-1)
                    rwd__tkwtd.append(-1)
            glbls[f'in_idxs_{xpa__jvaj}'] = np.array(qug__hef, np.int64)
            glbls[f'in_arr_inds_{xpa__jvaj}'] = np.array(rwd__tkwtd, np.int64)
            if aqj__whk:
                glbls[f'out_arr_inds_{xpa__jvaj}'] = np.array(out_table_type
                    .block_to_arr_ind[xpa__jvaj], dtype=np.int64)
            ahch__wotgy += (
                f'  in_arr_list_{xpa__jvaj} = get_table_block(T1, {fexk__cqgv})\n'
                )
            ahch__wotgy += (
                f'  for i in range(len(out_arr_list_{xpa__jvaj})):\n')
            ahch__wotgy += (
                f'    in_offset_{xpa__jvaj} = in_idxs_{xpa__jvaj}[i]\n')
            ahch__wotgy += f'    if in_offset_{xpa__jvaj} == -1:\n'
            ahch__wotgy += f'      continue\n'
            ahch__wotgy += (
                f'    in_arr_ind_{xpa__jvaj} = in_arr_inds_{xpa__jvaj}[i]\n')
            if aqj__whk:
                ahch__wotgy += f"""    if out_arr_inds_{xpa__jvaj}[i] not in kept_cols_set: continue
"""
            ahch__wotgy += f"""    ensure_column_unboxed(T1, in_arr_list_{xpa__jvaj}, in_offset_{xpa__jvaj}, in_arr_ind_{xpa__jvaj})
"""
            ahch__wotgy += f"""    out_arr_list_{xpa__jvaj}[i] = in_arr_list_{xpa__jvaj}[in_offset_{xpa__jvaj}]
"""
        for i, klex__wrfx in enumerate(out_table_type.block_to_arr_ind[
            xpa__jvaj]):
            if klex__wrfx not in kept_cols:
                continue
            cxpwg__janh = in_col_inds[klex__wrfx]
            if cxpwg__janh >= amno__sdk:
                ahch__wotgy += f"""  out_arr_list_{xpa__jvaj}[{i}] = extra_arrs_t[{cxpwg__janh - amno__sdk}]
"""
        ahch__wotgy += (
            f'  T2 = set_table_block(T2, out_arr_list_{xpa__jvaj}, {xpa__jvaj})\n'
            )
    ahch__wotgy += f'  return T2\n'
    glbls.update({'alloc_list_like': alloc_list_like, 'set_table_block':
        set_table_block, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'get_series_data':
        bodo.hiframes.pd_series_ext.get_series_data})
    ytbu__xjp = {}
    exec(ahch__wotgy, glbls, ytbu__xjp)
    return ytbu__xjp['impl']


def _logical_tuple_table_to_table_codegen(in_table_t, extra_arrs_t,
    in_col_inds, kept_cols, n_table_cols_t, out_table_type_t,
    extra_arrs_no_series):
    amno__sdk = get_overload_const_int(n_table_cols_t
        ) if is_overload_constant_int(n_table_cols_t) else len(in_table_t.types
        )
    out_table_type = TableType(tuple(in_table_t.types[i] if i < amno__sdk else
        _to_arr_if_series(extra_arrs_t.types[i - amno__sdk]) for i in
        in_col_inds)) if is_overload_none(out_table_type_t
        ) else unwrap_typeref(out_table_type_t)
    duqo__ysbh = None
    if not is_overload_none(in_table_t):
        for i, t in enumerate(in_table_t.types):
            if t != types.none:
                duqo__ysbh = f'in_table_t[{i}]'
                break
    if duqo__ysbh is None:
        for i, t in enumerate(extra_arrs_t.types):
            if t != types.none:
                duqo__ysbh = f'extra_arrs_t[{i}]'
                break
    assert duqo__ysbh is not None, 'no array found in input data'
    ahch__wotgy = """def impl(in_table_t, extra_arrs_t, in_col_inds_t, n_table_cols_t, out_table_type_t=None, used_cols=None):
"""
    if any(isinstance(t, SeriesType) for t in extra_arrs_t.types):
        ahch__wotgy += f'  extra_arrs_t = {extra_arrs_no_series}\n'
    ahch__wotgy += f'  T1 = in_table_t\n'
    ahch__wotgy += f'  T2 = init_table(out_table_type, False)\n'
    ahch__wotgy += f'  T2 = set_table_len(T2, len({duqo__ysbh}))\n'
    glbls = {}
    for typ, xpa__jvaj in out_table_type.type_to_blk.items():
        glbls[f'arr_list_typ_{xpa__jvaj}'] = types.List(typ)
        yxqly__tesxs = len(out_table_type.block_to_arr_ind[xpa__jvaj])
        ahch__wotgy += f"""  out_arr_list_{xpa__jvaj} = alloc_list_like(arr_list_typ_{xpa__jvaj}, {yxqly__tesxs}, False)
"""
        for i, klex__wrfx in enumerate(out_table_type.block_to_arr_ind[
            xpa__jvaj]):
            if klex__wrfx not in kept_cols:
                continue
            cxpwg__janh = in_col_inds[klex__wrfx]
            if cxpwg__janh < amno__sdk:
                ahch__wotgy += (
                    f'  out_arr_list_{xpa__jvaj}[{i}] = T1[{cxpwg__janh}]\n')
            else:
                ahch__wotgy += f"""  out_arr_list_{xpa__jvaj}[{i}] = extra_arrs_t[{cxpwg__janh - amno__sdk}]
"""
        ahch__wotgy += (
            f'  T2 = set_table_block(T2, out_arr_list_{xpa__jvaj}, {xpa__jvaj})\n'
            )
    ahch__wotgy += f'  return T2\n'
    glbls.update({'init_table': init_table, 'alloc_list_like':
        alloc_list_like, 'set_table_block': set_table_block,
        'set_table_len': set_table_len, 'out_table_type': out_table_type,
        'get_series_data': bodo.hiframes.pd_series_ext.get_series_data})
    ytbu__xjp = {}
    exec(ahch__wotgy, glbls, ytbu__xjp)
    return ytbu__xjp['impl']


def logical_table_to_table_equiv(self, scope, equiv_set, loc, args, kws):
    ksqy__jdje = args[0]
    oxpj__qrx = args[1]
    if equiv_set.has_shape(ksqy__jdje):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            ksqy__jdje)[0], None), pre=[])
    if equiv_set.has_shape(oxpj__qrx):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            oxpj__qrx)[0], None), pre=[])


(ArrayAnalysis._analyze_op_call_bodo_hiframes_table_logical_table_to_table
    ) = logical_table_to_table_equiv


def alias_ext_logical_table_to_table(lhs_name, args, alias_map, arg_aliases):
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['logical_table_to_table',
    'bodo.hiframes.table'] = alias_ext_logical_table_to_table
