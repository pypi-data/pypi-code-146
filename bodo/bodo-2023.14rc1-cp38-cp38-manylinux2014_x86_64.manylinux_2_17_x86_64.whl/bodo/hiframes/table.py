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
            zepuf__jujqr = 0
            aiq__wjjof = []
            for i in range(usecols[-1] + 1):
                if i == usecols[zepuf__jujqr]:
                    aiq__wjjof.append(arrs[zepuf__jujqr])
                    zepuf__jujqr += 1
                else:
                    aiq__wjjof.append(None)
            for wpq__dcq in range(usecols[-1] + 1, num_arrs):
                aiq__wjjof.append(None)
            self.arrays = aiq__wjjof
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((vtgxk__zzqq == dwyse__dshr).all() for 
            vtgxk__zzqq, dwyse__dshr in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        acry__dtj = len(self.arrays)
        bunom__rrsp = dict(zip(range(acry__dtj), self.arrays))
        df = pd.DataFrame(bunom__rrsp, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        epadb__jwwqf = []
        dlee__dmabe = []
        axyx__lfup = {}
        udd__hsl = {}
        sgs__ublc = defaultdict(int)
        rhy__qmdom = defaultdict(list)
        if not has_runtime_cols:
            for i, t in enumerate(arr_types):
                if t not in axyx__lfup:
                    dny__cdk = len(axyx__lfup)
                    axyx__lfup[t] = dny__cdk
                    udd__hsl[dny__cdk] = t
                uqxu__oyll = axyx__lfup[t]
                epadb__jwwqf.append(uqxu__oyll)
                dlee__dmabe.append(sgs__ublc[uqxu__oyll])
                sgs__ublc[uqxu__oyll] += 1
                rhy__qmdom[uqxu__oyll].append(i)
        self.block_nums = epadb__jwwqf
        self.block_offsets = dlee__dmabe
        self.type_to_blk = axyx__lfup
        self.blk_to_type = udd__hsl
        self.block_to_arr_ind = rhy__qmdom
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
            uczuh__otda = [(f'block_{i}', types.List(t)) for i, t in
                enumerate(fe_type.arr_types)]
        else:
            uczuh__otda = [(f'block_{uqxu__oyll}', types.List(t)) for t,
                uqxu__oyll in fe_type.type_to_blk.items()]
        uczuh__otda.append(('parent', types.pyobject))
        uczuh__otda.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, uczuh__otda)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    ajc__lem = c.pyapi.object_getattr_string(val, 'arrays')
    table = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    table.parent = cgutils.get_null_value(table.parent.type)
    dtxlh__hkya = c.pyapi.make_none()
    efhdv__jsg = c.context.get_constant(types.int64, 0)
    yat__yfi = cgutils.alloca_once_value(c.builder, efhdv__jsg)
    for t, uqxu__oyll in typ.type_to_blk.items():
        ats__aam = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[uqxu__oyll]))
        wpq__dcq, pnjo__izj = ListInstance.allocate_ex(c.context, c.builder,
            types.List(t), ats__aam)
        pnjo__izj.size = ats__aam
        lxjn__rdhv = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[uqxu__oyll],
            dtype=np.int64))
        upe__uimbe = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, lxjn__rdhv)
        with cgutils.for_range(c.builder, ats__aam) as bike__fobmc:
            i = bike__fobmc.index
            qwt__qrvp = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), upe__uimbe, i)
            ahw__mbpg = c.pyapi.long_from_longlong(qwt__qrvp)
            xua__lbl = c.pyapi.object_getitem(ajc__lem, ahw__mbpg)
            aytco__yoh = c.builder.icmp_unsigned('==', xua__lbl, dtxlh__hkya)
            with c.builder.if_else(aytco__yoh) as (qcsm__shihj, ajnex__agp):
                with qcsm__shihj:
                    qfp__dhi = c.context.get_constant_null(t)
                    pnjo__izj.inititem(i, qfp__dhi, incref=False)
                with ajnex__agp:
                    tdk__ilnk = c.pyapi.call_method(xua__lbl, '__len__', ())
                    aqsyq__ongdv = c.pyapi.long_as_longlong(tdk__ilnk)
                    c.builder.store(aqsyq__ongdv, yat__yfi)
                    c.pyapi.decref(tdk__ilnk)
                    arr = c.pyapi.to_native_value(t, xua__lbl).value
                    pnjo__izj.inititem(i, arr, incref=False)
            c.pyapi.decref(xua__lbl)
            c.pyapi.decref(ahw__mbpg)
        setattr(table, f'block_{uqxu__oyll}', pnjo__izj.value)
    table.len = c.builder.load(yat__yfi)
    c.pyapi.decref(ajc__lem)
    c.pyapi.decref(dtxlh__hkya)
    suuby__kgfd = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(table._getvalue(), is_error=suuby__kgfd)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    table = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        nbqqu__nnlr = c.context.get_constant(types.int64, 0)
        for i, t in enumerate(typ.arr_types):
            aiq__wjjof = getattr(table, f'block_{i}')
            ica__ajrs = ListInstance(c.context, c.builder, types.List(t),
                aiq__wjjof)
            nbqqu__nnlr = c.builder.add(nbqqu__nnlr, ica__ajrs.size)
        npcot__lna = c.pyapi.list_new(nbqqu__nnlr)
        bnzd__gpn = c.context.get_constant(types.int64, 0)
        for i, t in enumerate(typ.arr_types):
            aiq__wjjof = getattr(table, f'block_{i}')
            ica__ajrs = ListInstance(c.context, c.builder, types.List(t),
                aiq__wjjof)
            with cgutils.for_range(c.builder, ica__ajrs.size) as bike__fobmc:
                i = bike__fobmc.index
                arr = ica__ajrs.getitem(i)
                c.context.nrt.incref(c.builder, t, arr)
                idx = c.builder.add(bnzd__gpn, i)
                c.pyapi.list_setitem(npcot__lna, idx, c.pyapi.
                    from_native_value(t, arr, c.env_manager))
            bnzd__gpn = c.builder.add(bnzd__gpn, ica__ajrs.size)
        knfn__qvf = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        ttvu__wovad = c.pyapi.call_function_objargs(knfn__qvf, (npcot__lna,))
        c.pyapi.decref(knfn__qvf)
        c.pyapi.decref(npcot__lna)
        c.context.nrt.decref(c.builder, typ, val)
        return ttvu__wovad
    npcot__lna = c.pyapi.list_new(c.context.get_constant(types.int64, len(
        typ.arr_types)))
    veyzh__vodc = cgutils.is_not_null(c.builder, table.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for t, uqxu__oyll in typ.type_to_blk.items():
        aiq__wjjof = getattr(table, f'block_{uqxu__oyll}')
        ica__ajrs = ListInstance(c.context, c.builder, types.List(t),
            aiq__wjjof)
        lxjn__rdhv = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[uqxu__oyll],
            dtype=np.int64))
        upe__uimbe = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, lxjn__rdhv)
        with cgutils.for_range(c.builder, ica__ajrs.size) as bike__fobmc:
            i = bike__fobmc.index
            qwt__qrvp = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), upe__uimbe, i)
            arr = ica__ajrs.getitem(i)
            sidvc__oie = cgutils.alloca_once_value(c.builder, arr)
            dxrr__owiop = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(t))
            is_null = is_ll_eq(c.builder, sidvc__oie, dxrr__owiop)
            with c.builder.if_else(c.builder.and_(is_null, c.builder.not_(
                ensure_unboxed))) as (qcsm__shihj, ajnex__agp):
                with qcsm__shihj:
                    dtxlh__hkya = c.pyapi.make_none()
                    c.pyapi.list_setitem(npcot__lna, qwt__qrvp, dtxlh__hkya)
                with ajnex__agp:
                    xua__lbl = cgutils.alloca_once(c.builder, c.context.
                        get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(is_null, veyzh__vodc)
                        ) as (xdt__sums, yiy__kme):
                        with xdt__sums:
                            ykt__qos = get_df_obj_column_codegen(c.context,
                                c.builder, c.pyapi, table.parent, qwt__qrvp, t)
                            c.builder.store(ykt__qos, xua__lbl)
                        with yiy__kme:
                            c.context.nrt.incref(c.builder, t, arr)
                            c.builder.store(c.pyapi.from_native_value(t,
                                arr, c.env_manager), xua__lbl)
                    c.pyapi.list_setitem(npcot__lna, qwt__qrvp, c.builder.
                        load(xua__lbl))
    knfn__qvf = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    ttvu__wovad = c.pyapi.call_function_objargs(knfn__qvf, (npcot__lna,))
    c.pyapi.decref(knfn__qvf)
    c.pyapi.decref(npcot__lna)
    c.context.nrt.decref(c.builder, typ, val)
    return ttvu__wovad


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
        vjzp__gqpr = context.get_constant(types.int64, 0)
        for i, t in enumerate(table_type.arr_types):
            aiq__wjjof = getattr(table, f'block_{i}')
            ica__ajrs = ListInstance(context, builder, types.List(t),
                aiq__wjjof)
            vjzp__gqpr = builder.add(vjzp__gqpr, ica__ajrs.size)
        return vjzp__gqpr
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    table = cgutils.create_struct_proxy(table_type)(context, builder, table_arg
        )
    uqxu__oyll = table_type.block_nums[col_ind]
    avfs__tls = table_type.block_offsets[col_ind]
    aiq__wjjof = getattr(table, f'block_{uqxu__oyll}')
    cqu__ikrm = types.none(table_type, types.List(arr_type), types.int64,
        types.int64)
    nvrrq__eyy = context.get_constant(types.int64, col_ind)
    jchg__grpx = context.get_constant(types.int64, avfs__tls)
    pvc__gdgxj = table_arg, aiq__wjjof, jchg__grpx, nvrrq__eyy
    ensure_column_unboxed_codegen(context, builder, cqu__ikrm, pvc__gdgxj)
    ica__ajrs = ListInstance(context, builder, types.List(arr_type), aiq__wjjof
        )
    arr = ica__ajrs.getitem(avfs__tls)
    return arr


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, wpq__dcq = args
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
    ncghx__vbrq = list(ind_typ.instance_type.meta)
    muxbz__xirh = defaultdict(list)
    for ind in ncghx__vbrq:
        muxbz__xirh[table_type.block_nums[ind]].append(table_type.
            block_offsets[ind])

    def codegen(context, builder, sig, args):
        table_arg, wpq__dcq = args
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        for uqxu__oyll, flu__ztp in muxbz__xirh.items():
            arr_type = table_type.blk_to_type[uqxu__oyll]
            aiq__wjjof = getattr(table, f'block_{uqxu__oyll}')
            ica__ajrs = ListInstance(context, builder, types.List(arr_type),
                aiq__wjjof)
            qfp__dhi = context.get_constant_null(arr_type)
            if len(flu__ztp) == 1:
                avfs__tls = flu__ztp[0]
                arr = ica__ajrs.getitem(avfs__tls)
                context.nrt.decref(builder, arr_type, arr)
                ica__ajrs.inititem(avfs__tls, qfp__dhi, incref=False)
            else:
                ats__aam = context.get_constant(types.int64, len(flu__ztp))
                ientd__piwp = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(flu__ztp, dtype=np
                    .int64))
                xtl__pfxi = context.make_array(types.Array(types.int64, 1, 'C')
                    )(context, builder, ientd__piwp)
                with cgutils.for_range(builder, ats__aam) as bike__fobmc:
                    i = bike__fobmc.index
                    avfs__tls = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        xtl__pfxi, i)
                    arr = ica__ajrs.getitem(avfs__tls)
                    context.nrt.decref(builder, arr_type, arr)
                    ica__ajrs.inititem(avfs__tls, qfp__dhi, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    efhdv__jsg = context.get_constant(types.int64, 0)
    maqu__tsttk = context.get_constant(types.int64, 1)
    ojki__tnt = arr_type not in in_table_type.type_to_blk
    for t, uqxu__oyll in out_table_type.type_to_blk.items():
        if t in in_table_type.type_to_blk:
            ulehn__ngln = in_table_type.type_to_blk[t]
            pnjo__izj = ListInstance(context, builder, types.List(t),
                getattr(in_table, f'block_{ulehn__ngln}'))
            context.nrt.incref(builder, types.List(t), pnjo__izj.value)
            setattr(out_table, f'block_{uqxu__oyll}', pnjo__izj.value)
    if ojki__tnt:
        wpq__dcq, pnjo__izj = ListInstance.allocate_ex(context, builder,
            types.List(arr_type), maqu__tsttk)
        pnjo__izj.size = maqu__tsttk
        pnjo__izj.inititem(efhdv__jsg, arr_arg, incref=True)
        uqxu__oyll = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{uqxu__oyll}', pnjo__izj.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        uqxu__oyll = out_table_type.type_to_blk[arr_type]
        pnjo__izj = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{uqxu__oyll}'))
        if is_new_col:
            n = pnjo__izj.size
            jvnv__axmzs = builder.add(n, maqu__tsttk)
            pnjo__izj.resize(jvnv__axmzs)
            pnjo__izj.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            nvjl__ofulu = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            pnjo__izj.setitem(nvjl__ofulu, arr_arg, incref=True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            nvjl__ofulu = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            n = pnjo__izj.size
            jvnv__axmzs = builder.add(n, maqu__tsttk)
            pnjo__izj.resize(jvnv__axmzs)
            context.nrt.incref(builder, arr_type, pnjo__izj.getitem(
                nvjl__ofulu))
            pnjo__izj.move(builder.add(nvjl__ofulu, maqu__tsttk),
                nvjl__ofulu, builder.sub(n, nvjl__ofulu))
            pnjo__izj.setitem(nvjl__ofulu, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    nzow__hbgx = in_table_type.arr_types[col_ind]
    if nzow__hbgx in out_table_type.type_to_blk:
        uqxu__oyll = out_table_type.type_to_blk[nzow__hbgx]
        bcvrk__dlfj = getattr(out_table, f'block_{uqxu__oyll}')
        gvzna__lljkp = types.List(nzow__hbgx)
        nvjl__ofulu = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        ckwe__fjle = gvzna__lljkp.dtype(gvzna__lljkp, types.intp)
        tgeiq__ohgr = context.compile_internal(builder, lambda lst, i: lst.
            pop(i), ckwe__fjle, (bcvrk__dlfj, nvjl__ofulu))
        context.nrt.decref(builder, nzow__hbgx, tgeiq__ohgr)


def generate_set_table_data_code(table, ind, arr_type, used_cols, is_null=False
    ):
    xlru__rrc = list(table.arr_types)
    if ind == len(xlru__rrc):
        puhyp__rnd = None
        xlru__rrc.append(arr_type)
    else:
        puhyp__rnd = table.arr_types[ind]
        xlru__rrc[ind] = arr_type
    cyqvd__gvm = TableType(tuple(xlru__rrc))
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'set_table_parent': set_table_parent, 'alloc_list_like':
        alloc_list_like, 'out_table_typ': cyqvd__gvm}
    lps__albmq = 'def set_table_data(table, ind, arr, used_cols=None):\n'
    lps__albmq += f'  T2 = init_table(out_table_typ, False)\n'
    lps__albmq += f'  T2 = set_table_len(T2, len(table))\n'
    lps__albmq += f'  T2 = set_table_parent(T2, table)\n'
    for typ, uqxu__oyll in cyqvd__gvm.type_to_blk.items():
        if typ in table.type_to_blk:
            ntdjl__znzgy = table.type_to_blk[typ]
            lps__albmq += (
                f'  arr_list_{uqxu__oyll} = get_table_block(table, {ntdjl__znzgy})\n'
                )
            lps__albmq += f"""  out_arr_list_{uqxu__oyll} = alloc_list_like(arr_list_{uqxu__oyll}, {len(cyqvd__gvm.block_to_arr_ind[uqxu__oyll])}, False)
"""
            if used_cols is None or set(table.block_to_arr_ind[ntdjl__znzgy]
                ) & used_cols:
                lps__albmq += (
                    f'  for i in range(len(arr_list_{uqxu__oyll})):\n')
                if typ not in (puhyp__rnd, arr_type):
                    lps__albmq += (
                        f'    out_arr_list_{uqxu__oyll}[i] = arr_list_{uqxu__oyll}[i]\n'
                        )
                else:
                    vujx__khjjk = table.block_to_arr_ind[ntdjl__znzgy]
                    wtym__zqz = np.empty(len(vujx__khjjk), np.int64)
                    eiys__oam = False
                    for dgd__ixp, qwt__qrvp in enumerate(vujx__khjjk):
                        if qwt__qrvp != ind:
                            isy__iiazy = cyqvd__gvm.block_offsets[qwt__qrvp]
                        else:
                            isy__iiazy = -1
                            eiys__oam = True
                        wtym__zqz[dgd__ixp] = isy__iiazy
                    glbls[f'out_idxs_{uqxu__oyll}'] = np.array(wtym__zqz,
                        np.int64)
                    lps__albmq += f'    out_idx = out_idxs_{uqxu__oyll}[i]\n'
                    if eiys__oam:
                        lps__albmq += f'    if out_idx == -1:\n'
                        lps__albmq += f'      continue\n'
                    lps__albmq += f"""    out_arr_list_{uqxu__oyll}[out_idx] = arr_list_{uqxu__oyll}[i]
"""
            if typ == arr_type and not is_null:
                lps__albmq += f"""  out_arr_list_{uqxu__oyll}[{cyqvd__gvm.block_offsets[ind]}] = arr
"""
        else:
            glbls[f'arr_list_typ_{uqxu__oyll}'] = types.List(arr_type)
            lps__albmq += f"""  out_arr_list_{uqxu__oyll} = alloc_list_like(arr_list_typ_{uqxu__oyll}, 1, False)
"""
            if not is_null:
                lps__albmq += f'  out_arr_list_{uqxu__oyll}[0] = arr\n'
        lps__albmq += (
            f'  T2 = set_table_block(T2, out_arr_list_{uqxu__oyll}, {uqxu__oyll})\n'
            )
    lps__albmq += f'  return T2\n'
    fki__sep = {}
    exec(lps__albmq, glbls, fki__sep)
    return fki__sep['set_table_data']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def set_table_data(table, ind, arr, used_cols=None):
    if is_overload_none(used_cols):
        uzz__gwwg = None
    else:
        uzz__gwwg = set(used_cols.instance_type.meta)
    dna__yhlm = get_overload_const_int(ind)
    return generate_set_table_data_code(table, dna__yhlm, arr, uzz__gwwg)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def set_table_data_null(table, ind, arr, used_cols=None):
    dna__yhlm = get_overload_const_int(ind)
    arr_type = arr.instance_type
    if is_overload_none(used_cols):
        uzz__gwwg = None
    else:
        uzz__gwwg = set(used_cols.instance_type.meta)
    return generate_set_table_data_code(table, dna__yhlm, arr_type,
        uzz__gwwg, is_null=True)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_table_data',
    'bodo.hiframes.table'] = alias_ext_dummy_func


def get_table_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    mofi__etpf = args[0]
    if equiv_set.has_shape(mofi__etpf):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            mofi__etpf)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    osnij__uzo = []
    for t, uqxu__oyll in table_type.type_to_blk.items():
        vhs__vqhbh = len(table_type.block_to_arr_ind[uqxu__oyll])
        luzv__czkij = []
        for i in range(vhs__vqhbh):
            qwt__qrvp = table_type.block_to_arr_ind[uqxu__oyll][i]
            luzv__czkij.append(pyval.arrays[qwt__qrvp])
        osnij__uzo.append(context.get_constant_generic(builder, types.List(
            t), luzv__czkij))
    ggrxn__blbcy = context.get_constant_null(types.pyobject)
    mmdj__qpuj = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(osnij__uzo + [ggrxn__blbcy, mmdj__qpuj])


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
        for t, uqxu__oyll in out_table_type.type_to_blk.items():
            cfe__cti = context.get_constant_null(types.List(t))
            setattr(table, f'block_{uqxu__oyll}', cfe__cti)
        return table._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    sbdke__afi = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        sbdke__afi[typ.dtype] = i
    wusob__fuxhx = table_type.instance_type if isinstance(table_type, types
        .TypeRef) else table_type
    assert isinstance(wusob__fuxhx, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        daj__berz, wpq__dcq = args
        table = cgutils.create_struct_proxy(wusob__fuxhx)(context, builder)
        for t, uqxu__oyll in wusob__fuxhx.type_to_blk.items():
            idx = sbdke__afi[t]
            psfk__ani = signature(types.List(t), tuple_of_lists_type, types
                .literal(idx))
            qho__qvw = daj__berz, idx
            bsfo__yfrr = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, psfk__ani, qho__qvw)
            setattr(table, f'block_{uqxu__oyll}', bsfo__yfrr)
        return table._getvalue()
    sig = wusob__fuxhx(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    uqxu__oyll = get_overload_const_int(blk_type)
    arr_type = None
    for t, dwyse__dshr in table_type.type_to_blk.items():
        if dwyse__dshr == uqxu__oyll:
            arr_type = t
            break
    assert arr_type is not None, 'invalid table type block'
    qapkl__ynks = types.List(arr_type)

    def codegen(context, builder, sig, args):
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            args[0])
        aiq__wjjof = getattr(table, f'block_{uqxu__oyll}')
        return impl_ret_borrowed(context, builder, qapkl__ynks, aiq__wjjof)
    sig = qapkl__ynks(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, xwre__yys = args
        qxhnj__rzyie = context.get_python_api(builder)
        mhidv__keblm = used_cols_typ == types.none
        if not mhidv__keblm:
            wiar__ysyec = numba.cpython.setobj.SetInstance(context, builder,
                types.Set(types.int64), xwre__yys)
        table = cgutils.create_struct_proxy(sig.args[0])(context, builder,
            table_arg)
        for t, uqxu__oyll in table_type.type_to_blk.items():
            ats__aam = context.get_constant(types.int64, len(table_type.
                block_to_arr_ind[uqxu__oyll]))
            lxjn__rdhv = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind[
                uqxu__oyll], dtype=np.int64))
            upe__uimbe = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, lxjn__rdhv)
            aiq__wjjof = getattr(table, f'block_{uqxu__oyll}')
            with cgutils.for_range(builder, ats__aam) as bike__fobmc:
                i = bike__fobmc.index
                qwt__qrvp = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    upe__uimbe, i)
                cqu__ikrm = types.none(table_type, types.List(t), types.
                    int64, types.int64)
                pvc__gdgxj = table_arg, aiq__wjjof, i, qwt__qrvp
                if mhidv__keblm:
                    ensure_column_unboxed_codegen(context, builder,
                        cqu__ikrm, pvc__gdgxj)
                else:
                    ohgf__mgfnm = wiar__ysyec.contains(qwt__qrvp)
                    with builder.if_then(ohgf__mgfnm):
                        ensure_column_unboxed_codegen(context, builder,
                            cqu__ikrm, pvc__gdgxj)
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
    table_arg, wcg__vii, mneqq__zrdv, cwjuk__eyhzp = args
    qxhnj__rzyie = context.get_python_api(builder)
    table = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        table_arg)
    veyzh__vodc = cgutils.is_not_null(builder, table.parent)
    ica__ajrs = ListInstance(context, builder, sig.args[1], wcg__vii)
    ydziu__jkid = ica__ajrs.getitem(mneqq__zrdv)
    sidvc__oie = cgutils.alloca_once_value(builder, ydziu__jkid)
    dxrr__owiop = cgutils.alloca_once_value(builder, context.
        get_constant_null(sig.args[1].dtype))
    is_null = is_ll_eq(builder, sidvc__oie, dxrr__owiop)
    with builder.if_then(is_null):
        with builder.if_else(veyzh__vodc) as (qcsm__shihj, ajnex__agp):
            with qcsm__shihj:
                xua__lbl = get_df_obj_column_codegen(context, builder,
                    qxhnj__rzyie, table.parent, cwjuk__eyhzp, sig.args[1].dtype
                    )
                arr = qxhnj__rzyie.to_native_value(sig.args[1].dtype, xua__lbl
                    ).value
                ica__ajrs.inititem(mneqq__zrdv, arr, incref=False)
                qxhnj__rzyie.decref(xua__lbl)
            with ajnex__agp:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    uqxu__oyll = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, hhv__gky, wpq__dcq = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{uqxu__oyll}', hhv__gky)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, qbt__rfbum = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = qbt__rfbum
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def set_table_parent(typingctx, out_table_type, in_table_type):
    assert isinstance(in_table_type, TableType), 'table type expected'
    assert isinstance(out_table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        yaydh__xmvl, nntf__bgrwq = args
        in_table = cgutils.create_struct_proxy(in_table_type)(context,
            builder, nntf__bgrwq)
        out_table = cgutils.create_struct_proxy(out_table_type)(context,
            builder, yaydh__xmvl)
        out_table.parent = in_table.parent
        context.nrt.incref(builder, types.pyobject, out_table.parent)
        return impl_ret_borrowed(context, builder, out_table_type,
            out_table._getvalue())
    sig = out_table_type(out_table_type, in_table_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, len_type, to_str_if_dict_t):
    qapkl__ynks = list_type.instance_type if isinstance(list_type, types.
        TypeRef) else list_type
    assert isinstance(qapkl__ynks, types.List), 'list type or typeref expected'
    assert isinstance(len_type, types.Integer), 'integer type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    if is_overload_true(to_str_if_dict_t):
        qapkl__ynks = types.List(to_str_arr_if_dict_array(qapkl__ynks.dtype))

    def codegen(context, builder, sig, args):
        hyni__pxqbb = args[1]
        wpq__dcq, pnjo__izj = ListInstance.allocate_ex(context, builder,
            qapkl__ynks, hyni__pxqbb)
        pnjo__izj.size = hyni__pxqbb
        return pnjo__izj.value
    sig = qapkl__ynks(list_type, len_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    qfy__zukto = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(qfy__zukto)

    def codegen(context, builder, sig, args):
        hyni__pxqbb, wpq__dcq = args
        wpq__dcq, pnjo__izj = ListInstance.allocate_ex(context, builder,
            list_type, hyni__pxqbb)
        pnjo__izj.size = hyni__pxqbb
        return pnjo__izj.value
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
        isdm__clcsa = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(isdm__clcsa)
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
        gwf__ldur = used_cols.instance_type
        ntv__qyo = np.array(gwf__ldur.meta, dtype=np.int64)
        glbls['used_cols_vals'] = ntv__qyo
        dzn__aid = set([T.block_nums[i] for i in ntv__qyo])
    else:
        ntv__qyo = None
    lps__albmq = 'def table_filter_func(T, idx, used_cols=None):\n'
    lps__albmq += f'  T2 = init_table(T, False)\n'
    lps__albmq += f'  l = 0\n'
    if ntv__qyo is not None and len(ntv__qyo) == 0:
        lps__albmq += f'  l = _get_idx_length(idx, len(T))\n'
        lps__albmq += f'  T2 = set_table_len(T2, l)\n'
        lps__albmq += f'  return T2\n'
        fki__sep = {}
        exec(lps__albmq, glbls, fki__sep)
        return fki__sep['table_filter_func']
    if ntv__qyo is not None:
        lps__albmq += f'  used_set = set(used_cols_vals)\n'
    for uqxu__oyll in T.type_to_blk.values():
        lps__albmq += (
            f'  arr_list_{uqxu__oyll} = get_table_block(T, {uqxu__oyll})\n')
        lps__albmq += f"""  out_arr_list_{uqxu__oyll} = alloc_list_like(arr_list_{uqxu__oyll}, len(arr_list_{uqxu__oyll}), False)
"""
        if ntv__qyo is None or uqxu__oyll in dzn__aid:
            glbls[f'arr_inds_{uqxu__oyll}'] = np.array(T.block_to_arr_ind[
                uqxu__oyll], dtype=np.int64)
            lps__albmq += f'  for i in range(len(arr_list_{uqxu__oyll})):\n'
            lps__albmq += (
                f'    arr_ind_{uqxu__oyll} = arr_inds_{uqxu__oyll}[i]\n')
            if ntv__qyo is not None:
                lps__albmq += (
                    f'    if arr_ind_{uqxu__oyll} not in used_set: continue\n')
            lps__albmq += f"""    ensure_column_unboxed(T, arr_list_{uqxu__oyll}, i, arr_ind_{uqxu__oyll})
"""
            lps__albmq += f"""    out_arr_{uqxu__oyll} = ensure_contig_if_np(arr_list_{uqxu__oyll}[i][idx])
"""
            lps__albmq += f'    l = len(out_arr_{uqxu__oyll})\n'
            lps__albmq += (
                f'    out_arr_list_{uqxu__oyll}[i] = out_arr_{uqxu__oyll}\n')
        lps__albmq += (
            f'  T2 = set_table_block(T2, out_arr_list_{uqxu__oyll}, {uqxu__oyll})\n'
            )
    lps__albmq += f'  T2 = set_table_len(T2, l)\n'
    lps__albmq += f'  return T2\n'
    fki__sep = {}
    exec(lps__albmq, glbls, fki__sep)
    return fki__sep['table_filter_func']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_subset(T, idx, copy_arrs, used_cols=None):
    iyfiw__dfgz = list(idx.instance_type.meta)
    xlru__rrc = tuple(np.array(T.arr_types, dtype=object)[iyfiw__dfgz])
    cyqvd__gvm = TableType(xlru__rrc)
    if not is_overload_constant_bool(copy_arrs):
        raise_bodo_error('table_subset(): copy_arrs must be a constant')
    uwhv__gzns = is_overload_true(copy_arrs)
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'set_table_block':
        set_table_block, 'set_table_len': set_table_len, 'alloc_list_like':
        alloc_list_like, 'out_table_typ': cyqvd__gvm}
    if not is_overload_none(used_cols):
        kept_cols = used_cols.instance_type.meta
        exmq__gzjlx = set(kept_cols)
        glbls['kept_cols'] = np.array(kept_cols, np.int64)
        aivuu__idwy = True
    else:
        aivuu__idwy = False
    fcta__akwia = {i: c for i, c in enumerate(iyfiw__dfgz)}
    lps__albmq = 'def table_subset(T, idx, copy_arrs, used_cols=None):\n'
    lps__albmq += f'  T2 = init_table(out_table_typ, False)\n'
    lps__albmq += f'  T2 = set_table_len(T2, len(T))\n'
    if aivuu__idwy and len(exmq__gzjlx) == 0:
        lps__albmq += f'  return T2\n'
        fki__sep = {}
        exec(lps__albmq, glbls, fki__sep)
        return fki__sep['table_subset']
    if aivuu__idwy:
        lps__albmq += f'  kept_cols_set = set(kept_cols)\n'
    for typ, uqxu__oyll in cyqvd__gvm.type_to_blk.items():
        ntdjl__znzgy = T.type_to_blk[typ]
        lps__albmq += (
            f'  arr_list_{uqxu__oyll} = get_table_block(T, {ntdjl__znzgy})\n')
        lps__albmq += f"""  out_arr_list_{uqxu__oyll} = alloc_list_like(arr_list_{uqxu__oyll}, {len(cyqvd__gvm.block_to_arr_ind[uqxu__oyll])}, False)
"""
        vew__arc = True
        if aivuu__idwy:
            ftkoe__nlu = set(cyqvd__gvm.block_to_arr_ind[uqxu__oyll])
            icrgo__wqz = ftkoe__nlu & exmq__gzjlx
            vew__arc = len(icrgo__wqz) > 0
        if vew__arc:
            glbls[f'out_arr_inds_{uqxu__oyll}'] = np.array(cyqvd__gvm.
                block_to_arr_ind[uqxu__oyll], dtype=np.int64)
            lps__albmq += (
                f'  for i in range(len(out_arr_list_{uqxu__oyll})):\n')
            lps__albmq += (
                f'    out_arr_ind_{uqxu__oyll} = out_arr_inds_{uqxu__oyll}[i]\n'
                )
            if aivuu__idwy:
                lps__albmq += (
                    f'    if out_arr_ind_{uqxu__oyll} not in kept_cols_set: continue\n'
                    )
            aall__eyvlt = []
            myu__buoa = []
            for hepb__znd in cyqvd__gvm.block_to_arr_ind[uqxu__oyll]:
                sjx__swyg = fcta__akwia[hepb__znd]
                aall__eyvlt.append(sjx__swyg)
                kjlqq__klp = T.block_offsets[sjx__swyg]
                myu__buoa.append(kjlqq__klp)
            glbls[f'in_logical_idx_{uqxu__oyll}'] = np.array(aall__eyvlt,
                dtype=np.int64)
            glbls[f'in_physical_idx_{uqxu__oyll}'] = np.array(myu__buoa,
                dtype=np.int64)
            lps__albmq += (
                f'    logical_idx_{uqxu__oyll} = in_logical_idx_{uqxu__oyll}[i]\n'
                )
            lps__albmq += (
                f'    physical_idx_{uqxu__oyll} = in_physical_idx_{uqxu__oyll}[i]\n'
                )
            lps__albmq += f"""    ensure_column_unboxed(T, arr_list_{uqxu__oyll}, physical_idx_{uqxu__oyll}, logical_idx_{uqxu__oyll})
"""
            cfd__zagz = '.copy()' if uwhv__gzns else ''
            lps__albmq += f"""    out_arr_list_{uqxu__oyll}[i] = arr_list_{uqxu__oyll}[physical_idx_{uqxu__oyll}]{cfd__zagz}
"""
        lps__albmq += (
            f'  T2 = set_table_block(T2, out_arr_list_{uqxu__oyll}, {uqxu__oyll})\n'
            )
    lps__albmq += f'  return T2\n'
    fki__sep = {}
    exec(lps__albmq, glbls, fki__sep)
    return fki__sep['table_subset']


def table_filter_equiv(self, scope, equiv_set, loc, args, kws):
    mofi__etpf = args[0]
    if equiv_set.has_shape(mofi__etpf):
        if guard(is_whole_slice, self.typemap, self.func_ir, args[1]):
            return ArrayAnalysis.AnalyzeResult(shape=mofi__etpf, pre=[])
        return ArrayAnalysis.AnalyzeResult(shape=(None, equiv_set.get_shape
            (mofi__etpf)[1]), pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_table_filter = (
    table_filter_equiv)


def table_subset_equiv(self, scope, equiv_set, loc, args, kws):
    mofi__etpf = args[0]
    if equiv_set.has_shape(mofi__etpf):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            mofi__etpf)[0], None), pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_table_subset = (
    table_subset_equiv)


def gen_str_and_dict_enc_cols_to_one_block_fn_txt(in_table_type,
    out_table_type, glbls, is_gatherv=False):
    assert bodo.string_array_type in in_table_type.type_to_blk and bodo.string_array_type in in_table_type.type_to_blk, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: Table type {in_table_type} does not contain both a string, and encoded string column'
    uljk__xxwez = in_table_type.type_to_blk[bodo.string_array_type]
    hmmkb__xzj = in_table_type.type_to_blk[bodo.dict_str_arr_type]
    iyxu__lvr = in_table_type.block_to_arr_ind.get(uljk__xxwez)
    rbpiw__hqwj = in_table_type.block_to_arr_ind.get(hmmkb__xzj)
    nkfq__ccrmk = []
    jftpb__zyljx = []
    kkixs__kgbfh = 0
    zcf__ggtsq = 0
    for foryy__snmsi in range(len(iyxu__lvr) + len(rbpiw__hqwj)):
        if kkixs__kgbfh == len(iyxu__lvr):
            jftpb__zyljx.append(foryy__snmsi)
            continue
        elif zcf__ggtsq == len(rbpiw__hqwj):
            nkfq__ccrmk.append(foryy__snmsi)
            continue
        maugi__khar = iyxu__lvr[kkixs__kgbfh]
        pec__stib = rbpiw__hqwj[zcf__ggtsq]
        if maugi__khar < pec__stib:
            nkfq__ccrmk.append(foryy__snmsi)
            kkixs__kgbfh += 1
        else:
            jftpb__zyljx.append(foryy__snmsi)
            zcf__ggtsq += 1
    assert 'output_table_str_arr_offsets_in_combined_block' not in glbls, "Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: key 'output_table_str_arr_idxs_in_combined_block' already present as a global variable"
    glbls['output_table_str_arr_offsets_in_combined_block'] = np.array(
        nkfq__ccrmk)
    assert 'output_table_dict_enc_str_arr_offsets_in_combined_block' not in glbls, "Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: key 'output_table_str_arr_idxs_in_combined_block' already present as a global variable"
    glbls['output_table_dict_enc_str_arr_offsets_in_combined_block'
        ] = np.array(jftpb__zyljx)
    glbls['decode_if_dict_array'] = decode_if_dict_array
    ytcmb__twpf = out_table_type.type_to_blk[bodo.string_array_type]
    assert f'arr_inds_{uljk__xxwez}' not in glbls, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: arr_inds_{uljk__xxwez} already present in global variables'
    glbls[f'arr_inds_{uljk__xxwez}'] = np.array(in_table_type.
        block_to_arr_ind[uljk__xxwez], dtype=np.int64)
    assert f'arr_inds_{hmmkb__xzj}' not in glbls, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: arr_inds_{hmmkb__xzj} already present in global variables'
    glbls[f'arr_inds_{hmmkb__xzj}'] = np.array(in_table_type.
        block_to_arr_ind[hmmkb__xzj], dtype=np.int64)
    lps__albmq = f'  input_str_arr_list = get_table_block(T, {uljk__xxwez})\n'
    lps__albmq += (
        f'  input_dict_enc_str_arr_list = get_table_block(T, {hmmkb__xzj})\n')
    lps__albmq += f"""  out_arr_list_{ytcmb__twpf} = alloc_list_like(input_str_arr_list, {len(nkfq__ccrmk) + len(jftpb__zyljx)}, True)
"""
    lps__albmq += f"""  for input_str_ary_idx, output_str_arr_offset in enumerate(output_table_str_arr_offsets_in_combined_block):
"""
    lps__albmq += (
        f'    arr_ind_str = arr_inds_{uljk__xxwez}[input_str_ary_idx]\n')
    lps__albmq += f"""    ensure_column_unboxed(T, input_str_arr_list, input_str_ary_idx, arr_ind_str)
"""
    lps__albmq += f'    out_arr_str = input_str_arr_list[input_str_ary_idx]\n'
    if is_gatherv:
        lps__albmq += (
            f'    out_arr_str = bodo.gatherv(out_arr_str, allgather, warn_if_rep, root)\n'
            )
    lps__albmq += (
        f'    out_arr_list_{ytcmb__twpf}[output_str_arr_offset] = out_arr_str\n'
        )
    lps__albmq += f"""  for input_dict_enc_str_ary_idx, output_dict_enc_str_arr_offset in enumerate(output_table_dict_enc_str_arr_offsets_in_combined_block):
"""
    lps__albmq += (
        f'    arr_ind_dict_enc_str = arr_inds_{hmmkb__xzj}[input_dict_enc_str_ary_idx]\n'
        )
    lps__albmq += f"""    ensure_column_unboxed(T, input_dict_enc_str_arr_list, input_dict_enc_str_ary_idx, arr_ind_dict_enc_str)
"""
    lps__albmq += f"""    out_arr_dict_enc_str = decode_if_dict_array(input_dict_enc_str_arr_list[input_dict_enc_str_ary_idx])
"""
    if is_gatherv:
        lps__albmq += f"""    out_arr_dict_enc_str = bodo.gatherv(out_arr_dict_enc_str, allgather, warn_if_rep, root)
"""
    lps__albmq += f"""    out_arr_list_{ytcmb__twpf}[output_dict_enc_str_arr_offset] = out_arr_dict_enc_str
"""
    lps__albmq += (
        f'  T2 = set_table_block(T2, out_arr_list_{ytcmb__twpf}, {ytcmb__twpf})\n'
        )
    return lps__albmq


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    lps__albmq = 'def impl(T):\n'
    lps__albmq += f'  T2 = init_table(T, True)\n'
    lps__albmq += f'  l = len(T)\n'
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'set_table_block':
        set_table_block, 'set_table_len': set_table_len, 'alloc_list_like':
        alloc_list_like, 'decode_if_dict_array': decode_if_dict_array}
    out_table_type = bodo.hiframes.table.get_init_table_output_type(T, True)
    dln__dhe = (bodo.string_array_type in T.type_to_blk and bodo.
        dict_str_arr_type in T.type_to_blk)
    if dln__dhe:
        lps__albmq += gen_str_and_dict_enc_cols_to_one_block_fn_txt(T,
            out_table_type, glbls)
    for typ, lcoln__qbef in T.type_to_blk.items():
        if dln__dhe and typ in (bodo.string_array_type, bodo.dict_str_arr_type
            ):
            continue
        if typ == bodo.dict_str_arr_type:
            assert bodo.string_array_type in out_table_type.type_to_blk, 'Error in decode_if_dict_table: If encoded string type is present in the input, then non-encoded string type should be present in the output'
            etoz__utskz = out_table_type.type_to_blk[bodo.string_array_type]
        else:
            assert typ in out_table_type.type_to_blk, 'Error in decode_if_dict_table: All non-encoded string types present in the input should be present in the output'
            etoz__utskz = out_table_type.type_to_blk[typ]
        glbls[f'arr_inds_{lcoln__qbef}'] = np.array(T.block_to_arr_ind[
            lcoln__qbef], dtype=np.int64)
        lps__albmq += (
            f'  arr_list_{lcoln__qbef} = get_table_block(T, {lcoln__qbef})\n')
        lps__albmq += f"""  out_arr_list_{lcoln__qbef} = alloc_list_like(arr_list_{lcoln__qbef}, len(arr_list_{lcoln__qbef}), True)
"""
        lps__albmq += f'  for i in range(len(arr_list_{lcoln__qbef})):\n'
        lps__albmq += (
            f'    arr_ind_{lcoln__qbef} = arr_inds_{lcoln__qbef}[i]\n')
        lps__albmq += f"""    ensure_column_unboxed(T, arr_list_{lcoln__qbef}, i, arr_ind_{lcoln__qbef})
"""
        lps__albmq += f"""    out_arr_{lcoln__qbef} = decode_if_dict_array(arr_list_{lcoln__qbef}[i])
"""
        lps__albmq += (
            f'    out_arr_list_{lcoln__qbef}[i] = out_arr_{lcoln__qbef}\n')
        lps__albmq += (
            f'  T2 = set_table_block(T2, out_arr_list_{lcoln__qbef}, {etoz__utskz})\n'
            )
    lps__albmq += f'  T2 = set_table_len(T2, l)\n'
    lps__albmq += f'  return T2\n'
    fki__sep = {}
    exec(lps__albmq, glbls, fki__sep)
    return fki__sep['impl']


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
        vvte__hyztw = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        vvte__hyztw = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            vvte__hyztw.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        bln__pqjc, xip__nei = args
        table = cgutils.create_struct_proxy(table_type)(context, builder)
        table.len = xip__nei
        osnij__uzo = cgutils.unpack_tuple(builder, bln__pqjc)
        for i, aiq__wjjof in enumerate(osnij__uzo):
            setattr(table, f'block_{i}', aiq__wjjof)
            context.nrt.incref(builder, types.List(vvte__hyztw[i]), aiq__wjjof)
        return table._getvalue()
    table_type = TableType(tuple(vvte__hyztw), True)
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
        aivuu__idwy = True
    else:
        kept_cols = set(np.arange(len(in_col_inds)))
        aivuu__idwy = False
    extra_arrs_no_series = ', '.join(f'get_series_data(extra_arrs_t[{i}])' if
        isinstance(extra_arrs_t[i], SeriesType) else f'extra_arrs_t[{i}]' for
        i in range(len(extra_arrs_t)))
    extra_arrs_no_series = (
        f"({extra_arrs_no_series}{',' if len(extra_arrs_t) == 1 else ''})")
    if isinstance(in_table_t, (types.BaseTuple, types.NoneType)):
        return _logical_tuple_table_to_table_codegen(in_table_t,
            extra_arrs_t, in_col_inds, kept_cols, n_table_cols_t,
            out_table_type_t, extra_arrs_no_series)
    boyn__htt = len(in_table_t.arr_types)
    out_table_type = TableType(tuple(in_table_t.arr_types[i] if i <
        boyn__htt else _to_arr_if_series(extra_arrs_t.types[i - boyn__htt]) for
        i in in_col_inds)) if is_overload_none(out_table_type_t
        ) else unwrap_typeref(out_table_type_t)
    glbls.update({'init_table': init_table, 'set_table_len': set_table_len,
        'out_table_type': out_table_type})
    lps__albmq = """def impl(in_table_t, extra_arrs_t, in_col_inds_t, n_table_cols_t, out_table_type_t=None, used_cols=None):
"""
    if any(isinstance(t, SeriesType) for t in extra_arrs_t.types):
        lps__albmq += f'  extra_arrs_t = {extra_arrs_no_series}\n'
    lps__albmq += f'  T1 = in_table_t\n'
    lps__albmq += f'  T2 = init_table(out_table_type, False)\n'
    lps__albmq += f'  T2 = set_table_len(T2, len(T1))\n'
    if aivuu__idwy and len(kept_cols) == 0:
        lps__albmq += f'  return T2\n'
        fki__sep = {}
        exec(lps__albmq, glbls, fki__sep)
        return fki__sep['impl']
    if aivuu__idwy:
        lps__albmq += f'  kept_cols_set = set(kept_cols)\n'
    for typ, uqxu__oyll in out_table_type.type_to_blk.items():
        glbls[f'arr_list_typ_{uqxu__oyll}'] = types.List(typ)
        ats__aam = len(out_table_type.block_to_arr_ind[uqxu__oyll])
        lps__albmq += f"""  out_arr_list_{uqxu__oyll} = alloc_list_like(arr_list_typ_{uqxu__oyll}, {ats__aam}, False)
"""
        if typ in in_table_t.type_to_blk:
            ntwhb__ckj = in_table_t.type_to_blk[typ]
            iprd__suqcp = []
            rqh__mvie = []
            for nps__umfvp in out_table_type.block_to_arr_ind[uqxu__oyll]:
                tzkx__zeu = in_col_inds[nps__umfvp]
                if tzkx__zeu < boyn__htt:
                    iprd__suqcp.append(in_table_t.block_offsets[tzkx__zeu])
                    rqh__mvie.append(tzkx__zeu)
                else:
                    iprd__suqcp.append(-1)
                    rqh__mvie.append(-1)
            glbls[f'in_idxs_{uqxu__oyll}'] = np.array(iprd__suqcp, np.int64)
            glbls[f'in_arr_inds_{uqxu__oyll}'] = np.array(rqh__mvie, np.int64)
            if aivuu__idwy:
                glbls[f'out_arr_inds_{uqxu__oyll}'] = np.array(out_table_type
                    .block_to_arr_ind[uqxu__oyll], dtype=np.int64)
            lps__albmq += (
                f'  in_arr_list_{uqxu__oyll} = get_table_block(T1, {ntwhb__ckj})\n'
                )
            lps__albmq += (
                f'  for i in range(len(out_arr_list_{uqxu__oyll})):\n')
            lps__albmq += (
                f'    in_offset_{uqxu__oyll} = in_idxs_{uqxu__oyll}[i]\n')
            lps__albmq += f'    if in_offset_{uqxu__oyll} == -1:\n'
            lps__albmq += f'      continue\n'
            lps__albmq += (
                f'    in_arr_ind_{uqxu__oyll} = in_arr_inds_{uqxu__oyll}[i]\n')
            if aivuu__idwy:
                lps__albmq += f"""    if out_arr_inds_{uqxu__oyll}[i] not in kept_cols_set: continue
"""
            lps__albmq += f"""    ensure_column_unboxed(T1, in_arr_list_{uqxu__oyll}, in_offset_{uqxu__oyll}, in_arr_ind_{uqxu__oyll})
"""
            lps__albmq += f"""    out_arr_list_{uqxu__oyll}[i] = in_arr_list_{uqxu__oyll}[in_offset_{uqxu__oyll}]
"""
        for i, nps__umfvp in enumerate(out_table_type.block_to_arr_ind[
            uqxu__oyll]):
            if nps__umfvp not in kept_cols:
                continue
            tzkx__zeu = in_col_inds[nps__umfvp]
            if tzkx__zeu >= boyn__htt:
                lps__albmq += f"""  out_arr_list_{uqxu__oyll}[{i}] = extra_arrs_t[{tzkx__zeu - boyn__htt}]
"""
        lps__albmq += (
            f'  T2 = set_table_block(T2, out_arr_list_{uqxu__oyll}, {uqxu__oyll})\n'
            )
    lps__albmq += f'  return T2\n'
    glbls.update({'alloc_list_like': alloc_list_like, 'set_table_block':
        set_table_block, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'get_series_data':
        bodo.hiframes.pd_series_ext.get_series_data})
    fki__sep = {}
    exec(lps__albmq, glbls, fki__sep)
    return fki__sep['impl']


def _logical_tuple_table_to_table_codegen(in_table_t, extra_arrs_t,
    in_col_inds, kept_cols, n_table_cols_t, out_table_type_t,
    extra_arrs_no_series):
    boyn__htt = get_overload_const_int(n_table_cols_t
        ) if is_overload_constant_int(n_table_cols_t) else len(in_table_t.types
        )
    out_table_type = TableType(tuple(in_table_t.types[i] if i < boyn__htt else
        _to_arr_if_series(extra_arrs_t.types[i - boyn__htt]) for i in
        in_col_inds)) if is_overload_none(out_table_type_t
        ) else unwrap_typeref(out_table_type_t)
    yndnd__cve = None
    if not is_overload_none(in_table_t):
        for i, t in enumerate(in_table_t.types):
            if t != types.none:
                yndnd__cve = f'in_table_t[{i}]'
                break
    if yndnd__cve is None:
        for i, t in enumerate(extra_arrs_t.types):
            if t != types.none:
                yndnd__cve = f'extra_arrs_t[{i}]'
                break
    assert yndnd__cve is not None, 'no array found in input data'
    lps__albmq = """def impl(in_table_t, extra_arrs_t, in_col_inds_t, n_table_cols_t, out_table_type_t=None, used_cols=None):
"""
    if any(isinstance(t, SeriesType) for t in extra_arrs_t.types):
        lps__albmq += f'  extra_arrs_t = {extra_arrs_no_series}\n'
    lps__albmq += f'  T1 = in_table_t\n'
    lps__albmq += f'  T2 = init_table(out_table_type, False)\n'
    lps__albmq += f'  T2 = set_table_len(T2, len({yndnd__cve}))\n'
    glbls = {}
    for typ, uqxu__oyll in out_table_type.type_to_blk.items():
        glbls[f'arr_list_typ_{uqxu__oyll}'] = types.List(typ)
        ats__aam = len(out_table_type.block_to_arr_ind[uqxu__oyll])
        lps__albmq += f"""  out_arr_list_{uqxu__oyll} = alloc_list_like(arr_list_typ_{uqxu__oyll}, {ats__aam}, False)
"""
        for i, nps__umfvp in enumerate(out_table_type.block_to_arr_ind[
            uqxu__oyll]):
            if nps__umfvp not in kept_cols:
                continue
            tzkx__zeu = in_col_inds[nps__umfvp]
            if tzkx__zeu < boyn__htt:
                lps__albmq += (
                    f'  out_arr_list_{uqxu__oyll}[{i}] = T1[{tzkx__zeu}]\n')
            else:
                lps__albmq += f"""  out_arr_list_{uqxu__oyll}[{i}] = extra_arrs_t[{tzkx__zeu - boyn__htt}]
"""
        lps__albmq += (
            f'  T2 = set_table_block(T2, out_arr_list_{uqxu__oyll}, {uqxu__oyll})\n'
            )
    lps__albmq += f'  return T2\n'
    glbls.update({'init_table': init_table, 'alloc_list_like':
        alloc_list_like, 'set_table_block': set_table_block,
        'set_table_len': set_table_len, 'out_table_type': out_table_type,
        'get_series_data': bodo.hiframes.pd_series_ext.get_series_data})
    fki__sep = {}
    exec(lps__albmq, glbls, fki__sep)
    return fki__sep['impl']


def logical_table_to_table_equiv(self, scope, equiv_set, loc, args, kws):
    fob__xak = args[0]
    stvt__zobb = args[1]
    if equiv_set.has_shape(fob__xak):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            fob__xak)[0], None), pre=[])
    if equiv_set.has_shape(stvt__zobb):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            stvt__zobb)[0], None), pre=[])


(ArrayAnalysis._analyze_op_call_bodo_hiframes_table_logical_table_to_table
    ) = logical_table_to_table_equiv


def alias_ext_logical_table_to_table(lhs_name, args, alias_map, arg_aliases):
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['logical_table_to_table',
    'bodo.hiframes.table'] = alias_ext_logical_table_to_table
