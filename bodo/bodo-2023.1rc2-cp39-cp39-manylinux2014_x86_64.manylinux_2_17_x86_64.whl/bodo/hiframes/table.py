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
            psd__yet = 0
            zqu__jju = []
            for i in range(usecols[-1] + 1):
                if i == usecols[psd__yet]:
                    zqu__jju.append(arrs[psd__yet])
                    psd__yet += 1
                else:
                    zqu__jju.append(None)
            for mqu__yzoq in range(usecols[-1] + 1, num_arrs):
                zqu__jju.append(None)
            self.arrays = zqu__jju
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((ssyn__slhm == pfzi__hfao).all() for ssyn__slhm,
            pfzi__hfao in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        xag__semzl = len(self.arrays)
        gjrv__oin = dict(zip(range(xag__semzl), self.arrays))
        df = pd.DataFrame(gjrv__oin, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        divnr__srqy = []
        jod__uztx = []
        wwjlm__blbl = {}
        sjhi__xdh = {}
        sreai__fxb = defaultdict(int)
        brqpv__cekr = defaultdict(list)
        if not has_runtime_cols:
            for i, t in enumerate(arr_types):
                if t not in wwjlm__blbl:
                    wwzo__rtdy = len(wwjlm__blbl)
                    wwjlm__blbl[t] = wwzo__rtdy
                    sjhi__xdh[wwzo__rtdy] = t
                hbl__dpumu = wwjlm__blbl[t]
                divnr__srqy.append(hbl__dpumu)
                jod__uztx.append(sreai__fxb[hbl__dpumu])
                sreai__fxb[hbl__dpumu] += 1
                brqpv__cekr[hbl__dpumu].append(i)
        self.block_nums = divnr__srqy
        self.block_offsets = jod__uztx
        self.type_to_blk = wwjlm__blbl
        self.blk_to_type = sjhi__xdh
        self.block_to_arr_ind = brqpv__cekr
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
            elzfg__luol = [(f'block_{i}', types.List(t)) for i, t in
                enumerate(fe_type.arr_types)]
        else:
            elzfg__luol = [(f'block_{hbl__dpumu}', types.List(t)) for t,
                hbl__dpumu in fe_type.type_to_blk.items()]
        elzfg__luol.append(('parent', types.pyobject))
        elzfg__luol.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, elzfg__luol)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    rsnn__ggr = c.pyapi.object_getattr_string(val, 'arrays')
    table = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    table.parent = cgutils.get_null_value(table.parent.type)
    lznn__enr = c.pyapi.make_none()
    tbx__dxyd = c.context.get_constant(types.int64, 0)
    psuwd__nxk = cgutils.alloca_once_value(c.builder, tbx__dxyd)
    for t, hbl__dpumu in typ.type_to_blk.items():
        jpwg__ldavs = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[hbl__dpumu]))
        mqu__yzoq, pyw__hsw = ListInstance.allocate_ex(c.context, c.builder,
            types.List(t), jpwg__ldavs)
        pyw__hsw.size = jpwg__ldavs
        syli__kro = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[hbl__dpumu],
            dtype=np.int64))
        jhi__oktk = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, syli__kro)
        with cgutils.for_range(c.builder, jpwg__ldavs) as csfrr__fch:
            i = csfrr__fch.index
            qxga__dqr = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), jhi__oktk, i)
            geol__ihly = c.pyapi.long_from_longlong(qxga__dqr)
            qga__yxif = c.pyapi.object_getitem(rsnn__ggr, geol__ihly)
            bthmp__jkvq = c.builder.icmp_unsigned('==', qga__yxif, lznn__enr)
            with c.builder.if_else(bthmp__jkvq) as (picgf__zoo, fmco__lzfd):
                with picgf__zoo:
                    mktn__xip = c.context.get_constant_null(t)
                    pyw__hsw.inititem(i, mktn__xip, incref=False)
                with fmco__lzfd:
                    mrhg__sfq = c.pyapi.call_method(qga__yxif, '__len__', ())
                    jeoc__zgx = c.pyapi.long_as_longlong(mrhg__sfq)
                    c.builder.store(jeoc__zgx, psuwd__nxk)
                    c.pyapi.decref(mrhg__sfq)
                    arr = c.pyapi.to_native_value(t, qga__yxif).value
                    pyw__hsw.inititem(i, arr, incref=False)
            c.pyapi.decref(qga__yxif)
            c.pyapi.decref(geol__ihly)
        setattr(table, f'block_{hbl__dpumu}', pyw__hsw.value)
    table.len = c.builder.load(psuwd__nxk)
    c.pyapi.decref(rsnn__ggr)
    c.pyapi.decref(lznn__enr)
    xpnbh__jrco = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(table._getvalue(), is_error=xpnbh__jrco)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    table = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        vziad__uhy = c.context.get_constant(types.int64, 0)
        for i, t in enumerate(typ.arr_types):
            zqu__jju = getattr(table, f'block_{i}')
            rrrp__ubq = ListInstance(c.context, c.builder, types.List(t),
                zqu__jju)
            vziad__uhy = c.builder.add(vziad__uhy, rrrp__ubq.size)
        zvs__gvtle = c.pyapi.list_new(vziad__uhy)
        dvolb__rse = c.context.get_constant(types.int64, 0)
        for i, t in enumerate(typ.arr_types):
            zqu__jju = getattr(table, f'block_{i}')
            rrrp__ubq = ListInstance(c.context, c.builder, types.List(t),
                zqu__jju)
            with cgutils.for_range(c.builder, rrrp__ubq.size) as csfrr__fch:
                i = csfrr__fch.index
                arr = rrrp__ubq.getitem(i)
                c.context.nrt.incref(c.builder, t, arr)
                idx = c.builder.add(dvolb__rse, i)
                c.pyapi.list_setitem(zvs__gvtle, idx, c.pyapi.
                    from_native_value(t, arr, c.env_manager))
            dvolb__rse = c.builder.add(dvolb__rse, rrrp__ubq.size)
        ejro__atwrc = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        skonu__tmdv = c.pyapi.call_function_objargs(ejro__atwrc, (zvs__gvtle,))
        c.pyapi.decref(ejro__atwrc)
        c.pyapi.decref(zvs__gvtle)
        c.context.nrt.decref(c.builder, typ, val)
        return skonu__tmdv
    zvs__gvtle = c.pyapi.list_new(c.context.get_constant(types.int64, len(
        typ.arr_types)))
    vjum__erku = cgutils.is_not_null(c.builder, table.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for t, hbl__dpumu in typ.type_to_blk.items():
        zqu__jju = getattr(table, f'block_{hbl__dpumu}')
        rrrp__ubq = ListInstance(c.context, c.builder, types.List(t), zqu__jju)
        syli__kro = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[hbl__dpumu],
            dtype=np.int64))
        jhi__oktk = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, syli__kro)
        with cgutils.for_range(c.builder, rrrp__ubq.size) as csfrr__fch:
            i = csfrr__fch.index
            qxga__dqr = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), jhi__oktk, i)
            arr = rrrp__ubq.getitem(i)
            fqect__vsxq = cgutils.alloca_once_value(c.builder, arr)
            tjfmw__trkey = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(t))
            is_null = is_ll_eq(c.builder, fqect__vsxq, tjfmw__trkey)
            with c.builder.if_else(c.builder.and_(is_null, c.builder.not_(
                ensure_unboxed))) as (picgf__zoo, fmco__lzfd):
                with picgf__zoo:
                    lznn__enr = c.pyapi.make_none()
                    c.pyapi.list_setitem(zvs__gvtle, qxga__dqr, lznn__enr)
                with fmco__lzfd:
                    qga__yxif = cgutils.alloca_once(c.builder, c.context.
                        get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(is_null, vjum__erku)
                        ) as (ltqnu__yrjfx, mom__oyj):
                        with ltqnu__yrjfx:
                            lyynp__rnugq = get_df_obj_column_codegen(c.
                                context, c.builder, c.pyapi, table.parent,
                                qxga__dqr, t)
                            c.builder.store(lyynp__rnugq, qga__yxif)
                        with mom__oyj:
                            c.context.nrt.incref(c.builder, t, arr)
                            c.builder.store(c.pyapi.from_native_value(t,
                                arr, c.env_manager), qga__yxif)
                    c.pyapi.list_setitem(zvs__gvtle, qxga__dqr, c.builder.
                        load(qga__yxif))
    ejro__atwrc = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    skonu__tmdv = c.pyapi.call_function_objargs(ejro__atwrc, (zvs__gvtle,))
    c.pyapi.decref(ejro__atwrc)
    c.pyapi.decref(zvs__gvtle)
    c.context.nrt.decref(c.builder, typ, val)
    return skonu__tmdv


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
        agywz__cjdd = context.get_constant(types.int64, 0)
        for i, t in enumerate(table_type.arr_types):
            zqu__jju = getattr(table, f'block_{i}')
            rrrp__ubq = ListInstance(context, builder, types.List(t), zqu__jju)
            agywz__cjdd = builder.add(agywz__cjdd, rrrp__ubq.size)
        return agywz__cjdd
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    table = cgutils.create_struct_proxy(table_type)(context, builder, table_arg
        )
    hbl__dpumu = table_type.block_nums[col_ind]
    vkv__wjgs = table_type.block_offsets[col_ind]
    zqu__jju = getattr(table, f'block_{hbl__dpumu}')
    tsjf__bhy = types.none(table_type, types.List(arr_type), types.int64,
        types.int64)
    uwed__lsgal = context.get_constant(types.int64, col_ind)
    fin__iejl = context.get_constant(types.int64, vkv__wjgs)
    bhqs__lfe = table_arg, zqu__jju, fin__iejl, uwed__lsgal
    ensure_column_unboxed_codegen(context, builder, tsjf__bhy, bhqs__lfe)
    rrrp__ubq = ListInstance(context, builder, types.List(arr_type), zqu__jju)
    arr = rrrp__ubq.getitem(vkv__wjgs)
    return arr


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, mqu__yzoq = args
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
    coxox__qlrrd = list(ind_typ.instance_type.meta)
    nfchk__skm = defaultdict(list)
    for ind in coxox__qlrrd:
        nfchk__skm[table_type.block_nums[ind]].append(table_type.
            block_offsets[ind])

    def codegen(context, builder, sig, args):
        table_arg, mqu__yzoq = args
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        for hbl__dpumu, wsdn__jpd in nfchk__skm.items():
            arr_type = table_type.blk_to_type[hbl__dpumu]
            zqu__jju = getattr(table, f'block_{hbl__dpumu}')
            rrrp__ubq = ListInstance(context, builder, types.List(arr_type),
                zqu__jju)
            mktn__xip = context.get_constant_null(arr_type)
            if len(wsdn__jpd) == 1:
                vkv__wjgs = wsdn__jpd[0]
                arr = rrrp__ubq.getitem(vkv__wjgs)
                context.nrt.decref(builder, arr_type, arr)
                rrrp__ubq.inititem(vkv__wjgs, mktn__xip, incref=False)
            else:
                jpwg__ldavs = context.get_constant(types.int64, len(wsdn__jpd))
                wqot__lexhu = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(wsdn__jpd, dtype=
                    np.int64))
                jad__nvm = context.make_array(types.Array(types.int64, 1, 'C')
                    )(context, builder, wqot__lexhu)
                with cgutils.for_range(builder, jpwg__ldavs) as csfrr__fch:
                    i = csfrr__fch.index
                    vkv__wjgs = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        jad__nvm, i)
                    arr = rrrp__ubq.getitem(vkv__wjgs)
                    context.nrt.decref(builder, arr_type, arr)
                    rrrp__ubq.inititem(vkv__wjgs, mktn__xip, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    tbx__dxyd = context.get_constant(types.int64, 0)
    jnk__erly = context.get_constant(types.int64, 1)
    efvaa__firxg = arr_type not in in_table_type.type_to_blk
    for t, hbl__dpumu in out_table_type.type_to_blk.items():
        if t in in_table_type.type_to_blk:
            eqbdf__tzk = in_table_type.type_to_blk[t]
            pyw__hsw = ListInstance(context, builder, types.List(t),
                getattr(in_table, f'block_{eqbdf__tzk}'))
            context.nrt.incref(builder, types.List(t), pyw__hsw.value)
            setattr(out_table, f'block_{hbl__dpumu}', pyw__hsw.value)
    if efvaa__firxg:
        mqu__yzoq, pyw__hsw = ListInstance.allocate_ex(context, builder,
            types.List(arr_type), jnk__erly)
        pyw__hsw.size = jnk__erly
        pyw__hsw.inititem(tbx__dxyd, arr_arg, incref=True)
        hbl__dpumu = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{hbl__dpumu}', pyw__hsw.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        hbl__dpumu = out_table_type.type_to_blk[arr_type]
        pyw__hsw = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{hbl__dpumu}'))
        if is_new_col:
            n = pyw__hsw.size
            upsy__quhb = builder.add(n, jnk__erly)
            pyw__hsw.resize(upsy__quhb)
            pyw__hsw.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            lzs__qpemo = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            pyw__hsw.setitem(lzs__qpemo, arr_arg, incref=True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            lzs__qpemo = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            n = pyw__hsw.size
            upsy__quhb = builder.add(n, jnk__erly)
            pyw__hsw.resize(upsy__quhb)
            context.nrt.incref(builder, arr_type, pyw__hsw.getitem(lzs__qpemo))
            pyw__hsw.move(builder.add(lzs__qpemo, jnk__erly), lzs__qpemo,
                builder.sub(n, lzs__qpemo))
            pyw__hsw.setitem(lzs__qpemo, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    eviob__wceo = in_table_type.arr_types[col_ind]
    if eviob__wceo in out_table_type.type_to_blk:
        hbl__dpumu = out_table_type.type_to_blk[eviob__wceo]
        khu__scif = getattr(out_table, f'block_{hbl__dpumu}')
        accs__npk = types.List(eviob__wceo)
        lzs__qpemo = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        jnvgr__vhzv = accs__npk.dtype(accs__npk, types.intp)
        qdj__bzzi = context.compile_internal(builder, lambda lst, i: lst.
            pop(i), jnvgr__vhzv, (khu__scif, lzs__qpemo))
        context.nrt.decref(builder, eviob__wceo, qdj__bzzi)


def generate_set_table_data_code(table, ind, arr_type, used_cols, is_null=False
    ):
    hcq__kjku = list(table.arr_types)
    if ind == len(hcq__kjku):
        pdxvh__rhsm = None
        hcq__kjku.append(arr_type)
    else:
        pdxvh__rhsm = table.arr_types[ind]
        hcq__kjku[ind] = arr_type
    bqbt__zky = TableType(tuple(hcq__kjku))
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'set_table_parent': set_table_parent, 'alloc_list_like':
        alloc_list_like, 'out_table_typ': bqbt__zky}
    qrjte__diipc = 'def set_table_data(table, ind, arr, used_cols=None):\n'
    qrjte__diipc += f'  T2 = init_table(out_table_typ, False)\n'
    qrjte__diipc += f'  T2 = set_table_len(T2, len(table))\n'
    qrjte__diipc += f'  T2 = set_table_parent(T2, table)\n'
    for typ, hbl__dpumu in bqbt__zky.type_to_blk.items():
        if typ in table.type_to_blk:
            oqcr__jtg = table.type_to_blk[typ]
            qrjte__diipc += (
                f'  arr_list_{hbl__dpumu} = get_table_block(table, {oqcr__jtg})\n'
                )
            qrjte__diipc += f"""  out_arr_list_{hbl__dpumu} = alloc_list_like(arr_list_{hbl__dpumu}, {len(bqbt__zky.block_to_arr_ind[hbl__dpumu])}, False)
"""
            if used_cols is None or set(table.block_to_arr_ind[oqcr__jtg]
                ) & used_cols:
                qrjte__diipc += (
                    f'  for i in range(len(arr_list_{hbl__dpumu})):\n')
                if typ not in (pdxvh__rhsm, arr_type):
                    qrjte__diipc += (
                        f'    out_arr_list_{hbl__dpumu}[i] = arr_list_{hbl__dpumu}[i]\n'
                        )
                else:
                    uiq__ydph = table.block_to_arr_ind[oqcr__jtg]
                    obmy__rbu = np.empty(len(uiq__ydph), np.int64)
                    gwbnt__pul = False
                    for djz__qqo, qxga__dqr in enumerate(uiq__ydph):
                        if qxga__dqr != ind:
                            hmtee__oldq = bqbt__zky.block_offsets[qxga__dqr]
                        else:
                            hmtee__oldq = -1
                            gwbnt__pul = True
                        obmy__rbu[djz__qqo] = hmtee__oldq
                    glbls[f'out_idxs_{hbl__dpumu}'] = np.array(obmy__rbu,
                        np.int64)
                    qrjte__diipc += f'    out_idx = out_idxs_{hbl__dpumu}[i]\n'
                    if gwbnt__pul:
                        qrjte__diipc += f'    if out_idx == -1:\n'
                        qrjte__diipc += f'      continue\n'
                    qrjte__diipc += f"""    out_arr_list_{hbl__dpumu}[out_idx] = arr_list_{hbl__dpumu}[i]
"""
            if typ == arr_type and not is_null:
                qrjte__diipc += f"""  out_arr_list_{hbl__dpumu}[{bqbt__zky.block_offsets[ind]}] = arr
"""
        else:
            glbls[f'arr_list_typ_{hbl__dpumu}'] = types.List(arr_type)
            qrjte__diipc += f"""  out_arr_list_{hbl__dpumu} = alloc_list_like(arr_list_typ_{hbl__dpumu}, 1, False)
"""
            if not is_null:
                qrjte__diipc += f'  out_arr_list_{hbl__dpumu}[0] = arr\n'
        qrjte__diipc += (
            f'  T2 = set_table_block(T2, out_arr_list_{hbl__dpumu}, {hbl__dpumu})\n'
            )
    qrjte__diipc += f'  return T2\n'
    ljw__ghk = {}
    exec(qrjte__diipc, glbls, ljw__ghk)
    return ljw__ghk['set_table_data']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def set_table_data(table, ind, arr, used_cols=None):
    if is_overload_none(used_cols):
        soen__mtjt = None
    else:
        soen__mtjt = set(used_cols.instance_type.meta)
    wms__jbbr = get_overload_const_int(ind)
    return generate_set_table_data_code(table, wms__jbbr, arr, soen__mtjt)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def set_table_data_null(table, ind, arr, used_cols=None):
    wms__jbbr = get_overload_const_int(ind)
    arr_type = arr.instance_type
    if is_overload_none(used_cols):
        soen__mtjt = None
    else:
        soen__mtjt = set(used_cols.instance_type.meta)
    return generate_set_table_data_code(table, wms__jbbr, arr_type,
        soen__mtjt, is_null=True)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_table_data',
    'bodo.hiframes.table'] = alias_ext_dummy_func


def get_table_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    alpvr__jscu = args[0]
    if equiv_set.has_shape(alpvr__jscu):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            alpvr__jscu)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    bslb__scx = []
    for t, hbl__dpumu in table_type.type_to_blk.items():
        jcf__yrbv = len(table_type.block_to_arr_ind[hbl__dpumu])
        gdyso__epj = []
        for i in range(jcf__yrbv):
            qxga__dqr = table_type.block_to_arr_ind[hbl__dpumu][i]
            gdyso__epj.append(pyval.arrays[qxga__dqr])
        bslb__scx.append(context.get_constant_generic(builder, types.List(t
            ), gdyso__epj))
    wca__osc = context.get_constant_null(types.pyobject)
    dfnru__brd = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(bslb__scx + [wca__osc, dfnru__brd])


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
        for t, hbl__dpumu in out_table_type.type_to_blk.items():
            ssovr__mbzw = context.get_constant_null(types.List(t))
            setattr(table, f'block_{hbl__dpumu}', ssovr__mbzw)
        return table._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    hnhxd__dyoat = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        hnhxd__dyoat[typ.dtype] = i
    gkokm__ijusm = table_type.instance_type if isinstance(table_type, types
        .TypeRef) else table_type
    assert isinstance(gkokm__ijusm, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        hjt__sko, mqu__yzoq = args
        table = cgutils.create_struct_proxy(gkokm__ijusm)(context, builder)
        for t, hbl__dpumu in gkokm__ijusm.type_to_blk.items():
            idx = hnhxd__dyoat[t]
            weldb__eok = signature(types.List(t), tuple_of_lists_type,
                types.literal(idx))
            nntu__xxom = hjt__sko, idx
            ila__qlvn = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, weldb__eok, nntu__xxom)
            setattr(table, f'block_{hbl__dpumu}', ila__qlvn)
        return table._getvalue()
    sig = gkokm__ijusm(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    hbl__dpumu = get_overload_const_int(blk_type)
    arr_type = None
    for t, pfzi__hfao in table_type.type_to_blk.items():
        if pfzi__hfao == hbl__dpumu:
            arr_type = t
            break
    assert arr_type is not None, 'invalid table type block'
    xnr__dhayu = types.List(arr_type)

    def codegen(context, builder, sig, args):
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            args[0])
        zqu__jju = getattr(table, f'block_{hbl__dpumu}')
        return impl_ret_borrowed(context, builder, xnr__dhayu, zqu__jju)
    sig = xnr__dhayu(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, iyu__pig = args
        qaiqt__hvq = context.get_python_api(builder)
        tdvfj__vdx = used_cols_typ == types.none
        if not tdvfj__vdx:
            ith__zfkk = numba.cpython.setobj.SetInstance(context, builder,
                types.Set(types.int64), iyu__pig)
        table = cgutils.create_struct_proxy(sig.args[0])(context, builder,
            table_arg)
        for t, hbl__dpumu in table_type.type_to_blk.items():
            jpwg__ldavs = context.get_constant(types.int64, len(table_type.
                block_to_arr_ind[hbl__dpumu]))
            syli__kro = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind[
                hbl__dpumu], dtype=np.int64))
            jhi__oktk = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, syli__kro)
            zqu__jju = getattr(table, f'block_{hbl__dpumu}')
            with cgutils.for_range(builder, jpwg__ldavs) as csfrr__fch:
                i = csfrr__fch.index
                qxga__dqr = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'), jhi__oktk, i
                    )
                tsjf__bhy = types.none(table_type, types.List(t), types.
                    int64, types.int64)
                bhqs__lfe = table_arg, zqu__jju, i, qxga__dqr
                if tdvfj__vdx:
                    ensure_column_unboxed_codegen(context, builder,
                        tsjf__bhy, bhqs__lfe)
                else:
                    zpagz__bgo = ith__zfkk.contains(qxga__dqr)
                    with builder.if_then(zpagz__bgo):
                        ensure_column_unboxed_codegen(context, builder,
                            tsjf__bhy, bhqs__lfe)
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
    table_arg, qumf__ogbjd, gfqbz__aamut, xcm__ceqou = args
    qaiqt__hvq = context.get_python_api(builder)
    table = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        table_arg)
    vjum__erku = cgutils.is_not_null(builder, table.parent)
    rrrp__ubq = ListInstance(context, builder, sig.args[1], qumf__ogbjd)
    rozsv__zsve = rrrp__ubq.getitem(gfqbz__aamut)
    fqect__vsxq = cgutils.alloca_once_value(builder, rozsv__zsve)
    tjfmw__trkey = cgutils.alloca_once_value(builder, context.
        get_constant_null(sig.args[1].dtype))
    is_null = is_ll_eq(builder, fqect__vsxq, tjfmw__trkey)
    with builder.if_then(is_null):
        with builder.if_else(vjum__erku) as (picgf__zoo, fmco__lzfd):
            with picgf__zoo:
                qga__yxif = get_df_obj_column_codegen(context, builder,
                    qaiqt__hvq, table.parent, xcm__ceqou, sig.args[1].dtype)
                arr = qaiqt__hvq.to_native_value(sig.args[1].dtype, qga__yxif
                    ).value
                rrrp__ubq.inititem(gfqbz__aamut, arr, incref=False)
                qaiqt__hvq.decref(qga__yxif)
            with fmco__lzfd:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    hbl__dpumu = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, lhbto__aqy, mqu__yzoq = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{hbl__dpumu}', lhbto__aqy)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, nsaw__fopg = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = nsaw__fopg
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def set_table_parent(typingctx, out_table_type, in_table_type):
    assert isinstance(in_table_type, TableType), 'table type expected'
    assert isinstance(out_table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        zdcke__csse, vst__vlyn = args
        in_table = cgutils.create_struct_proxy(in_table_type)(context,
            builder, vst__vlyn)
        out_table = cgutils.create_struct_proxy(out_table_type)(context,
            builder, zdcke__csse)
        out_table.parent = in_table.parent
        context.nrt.incref(builder, types.pyobject, out_table.parent)
        return impl_ret_borrowed(context, builder, out_table_type,
            out_table._getvalue())
    sig = out_table_type(out_table_type, in_table_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, len_type, to_str_if_dict_t):
    xnr__dhayu = list_type.instance_type if isinstance(list_type, types.TypeRef
        ) else list_type
    assert isinstance(xnr__dhayu, types.List), 'list type or typeref expected'
    assert isinstance(len_type, types.Integer), 'integer type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    if is_overload_true(to_str_if_dict_t):
        xnr__dhayu = types.List(to_str_arr_if_dict_array(xnr__dhayu.dtype))

    def codegen(context, builder, sig, args):
        dqegy__rytmh = args[1]
        mqu__yzoq, pyw__hsw = ListInstance.allocate_ex(context, builder,
            xnr__dhayu, dqegy__rytmh)
        pyw__hsw.size = dqegy__rytmh
        return pyw__hsw.value
    sig = xnr__dhayu(list_type, len_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    mna__xoys = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(mna__xoys)

    def codegen(context, builder, sig, args):
        dqegy__rytmh, mqu__yzoq = args
        mqu__yzoq, pyw__hsw = ListInstance.allocate_ex(context, builder,
            list_type, dqegy__rytmh)
        pyw__hsw.size = dqegy__rytmh
        return pyw__hsw.value
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
        apt__etdn = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(apt__etdn)
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
        rzxsm__yfsit = used_cols.instance_type
        lqyu__sigy = np.array(rzxsm__yfsit.meta, dtype=np.int64)
        glbls['used_cols_vals'] = lqyu__sigy
        ffvfi__gmti = set([T.block_nums[i] for i in lqyu__sigy])
    else:
        lqyu__sigy = None
    qrjte__diipc = 'def table_filter_func(T, idx, used_cols=None):\n'
    qrjte__diipc += f'  T2 = init_table(T, False)\n'
    qrjte__diipc += f'  l = 0\n'
    if lqyu__sigy is not None and len(lqyu__sigy) == 0:
        qrjte__diipc += f'  l = _get_idx_length(idx, len(T))\n'
        qrjte__diipc += f'  T2 = set_table_len(T2, l)\n'
        qrjte__diipc += f'  return T2\n'
        ljw__ghk = {}
        exec(qrjte__diipc, glbls, ljw__ghk)
        return ljw__ghk['table_filter_func']
    if lqyu__sigy is not None:
        qrjte__diipc += f'  used_set = set(used_cols_vals)\n'
    for hbl__dpumu in T.type_to_blk.values():
        qrjte__diipc += (
            f'  arr_list_{hbl__dpumu} = get_table_block(T, {hbl__dpumu})\n')
        qrjte__diipc += f"""  out_arr_list_{hbl__dpumu} = alloc_list_like(arr_list_{hbl__dpumu}, len(arr_list_{hbl__dpumu}), False)
"""
        if lqyu__sigy is None or hbl__dpumu in ffvfi__gmti:
            glbls[f'arr_inds_{hbl__dpumu}'] = np.array(T.block_to_arr_ind[
                hbl__dpumu], dtype=np.int64)
            qrjte__diipc += f'  for i in range(len(arr_list_{hbl__dpumu})):\n'
            qrjte__diipc += (
                f'    arr_ind_{hbl__dpumu} = arr_inds_{hbl__dpumu}[i]\n')
            if lqyu__sigy is not None:
                qrjte__diipc += (
                    f'    if arr_ind_{hbl__dpumu} not in used_set: continue\n')
            qrjte__diipc += f"""    ensure_column_unboxed(T, arr_list_{hbl__dpumu}, i, arr_ind_{hbl__dpumu})
"""
            qrjte__diipc += f"""    out_arr_{hbl__dpumu} = ensure_contig_if_np(arr_list_{hbl__dpumu}[i][idx])
"""
            qrjte__diipc += f'    l = len(out_arr_{hbl__dpumu})\n'
            qrjte__diipc += (
                f'    out_arr_list_{hbl__dpumu}[i] = out_arr_{hbl__dpumu}\n')
        qrjte__diipc += (
            f'  T2 = set_table_block(T2, out_arr_list_{hbl__dpumu}, {hbl__dpumu})\n'
            )
    qrjte__diipc += f'  T2 = set_table_len(T2, l)\n'
    qrjte__diipc += f'  return T2\n'
    ljw__ghk = {}
    exec(qrjte__diipc, glbls, ljw__ghk)
    return ljw__ghk['table_filter_func']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_subset(T, idx, copy_arrs, used_cols=None):
    bcx__ruz = list(idx.instance_type.meta)
    hcq__kjku = tuple(np.array(T.arr_types, dtype=object)[bcx__ruz])
    bqbt__zky = TableType(hcq__kjku)
    if not is_overload_constant_bool(copy_arrs):
        raise_bodo_error('table_subset(): copy_arrs must be a constant')
    ahpe__iqo = is_overload_true(copy_arrs)
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'set_table_block':
        set_table_block, 'set_table_len': set_table_len, 'alloc_list_like':
        alloc_list_like, 'out_table_typ': bqbt__zky}
    if not is_overload_none(used_cols):
        kept_cols = used_cols.instance_type.meta
        ctmgr__fbk = set(kept_cols)
        glbls['kept_cols'] = np.array(kept_cols, np.int64)
        govu__ejp = True
    else:
        govu__ejp = False
    dkhys__eyurr = {i: c for i, c in enumerate(bcx__ruz)}
    qrjte__diipc = 'def table_subset(T, idx, copy_arrs, used_cols=None):\n'
    qrjte__diipc += f'  T2 = init_table(out_table_typ, False)\n'
    qrjte__diipc += f'  T2 = set_table_len(T2, len(T))\n'
    if govu__ejp and len(ctmgr__fbk) == 0:
        qrjte__diipc += f'  return T2\n'
        ljw__ghk = {}
        exec(qrjte__diipc, glbls, ljw__ghk)
        return ljw__ghk['table_subset']
    if govu__ejp:
        qrjte__diipc += f'  kept_cols_set = set(kept_cols)\n'
    for typ, hbl__dpumu in bqbt__zky.type_to_blk.items():
        oqcr__jtg = T.type_to_blk[typ]
        qrjte__diipc += (
            f'  arr_list_{hbl__dpumu} = get_table_block(T, {oqcr__jtg})\n')
        qrjte__diipc += f"""  out_arr_list_{hbl__dpumu} = alloc_list_like(arr_list_{hbl__dpumu}, {len(bqbt__zky.block_to_arr_ind[hbl__dpumu])}, False)
"""
        vlrx__suue = True
        if govu__ejp:
            looxq__dci = set(bqbt__zky.block_to_arr_ind[hbl__dpumu])
            nyj__xmxz = looxq__dci & ctmgr__fbk
            vlrx__suue = len(nyj__xmxz) > 0
        if vlrx__suue:
            glbls[f'out_arr_inds_{hbl__dpumu}'] = np.array(bqbt__zky.
                block_to_arr_ind[hbl__dpumu], dtype=np.int64)
            qrjte__diipc += (
                f'  for i in range(len(out_arr_list_{hbl__dpumu})):\n')
            qrjte__diipc += (
                f'    out_arr_ind_{hbl__dpumu} = out_arr_inds_{hbl__dpumu}[i]\n'
                )
            if govu__ejp:
                qrjte__diipc += (
                    f'    if out_arr_ind_{hbl__dpumu} not in kept_cols_set: continue\n'
                    )
            cmrh__gwkb = []
            uocwh__bkagq = []
            for pki__dvuqc in bqbt__zky.block_to_arr_ind[hbl__dpumu]:
                vqtii__jmxr = dkhys__eyurr[pki__dvuqc]
                cmrh__gwkb.append(vqtii__jmxr)
                smzv__gatoz = T.block_offsets[vqtii__jmxr]
                uocwh__bkagq.append(smzv__gatoz)
            glbls[f'in_logical_idx_{hbl__dpumu}'] = np.array(cmrh__gwkb,
                dtype=np.int64)
            glbls[f'in_physical_idx_{hbl__dpumu}'] = np.array(uocwh__bkagq,
                dtype=np.int64)
            qrjte__diipc += (
                f'    logical_idx_{hbl__dpumu} = in_logical_idx_{hbl__dpumu}[i]\n'
                )
            qrjte__diipc += (
                f'    physical_idx_{hbl__dpumu} = in_physical_idx_{hbl__dpumu}[i]\n'
                )
            qrjte__diipc += f"""    ensure_column_unboxed(T, arr_list_{hbl__dpumu}, physical_idx_{hbl__dpumu}, logical_idx_{hbl__dpumu})
"""
            nuse__rhp = '.copy()' if ahpe__iqo else ''
            qrjte__diipc += f"""    out_arr_list_{hbl__dpumu}[i] = arr_list_{hbl__dpumu}[physical_idx_{hbl__dpumu}]{nuse__rhp}
"""
        qrjte__diipc += (
            f'  T2 = set_table_block(T2, out_arr_list_{hbl__dpumu}, {hbl__dpumu})\n'
            )
    qrjte__diipc += f'  return T2\n'
    ljw__ghk = {}
    exec(qrjte__diipc, glbls, ljw__ghk)
    return ljw__ghk['table_subset']


def table_filter_equiv(self, scope, equiv_set, loc, args, kws):
    alpvr__jscu = args[0]
    if equiv_set.has_shape(alpvr__jscu):
        if guard(is_whole_slice, self.typemap, self.func_ir, args[1]):
            return ArrayAnalysis.AnalyzeResult(shape=alpvr__jscu, pre=[])
        return ArrayAnalysis.AnalyzeResult(shape=(None, equiv_set.get_shape
            (alpvr__jscu)[1]), pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_table_filter = (
    table_filter_equiv)


def table_subset_equiv(self, scope, equiv_set, loc, args, kws):
    alpvr__jscu = args[0]
    if equiv_set.has_shape(alpvr__jscu):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            alpvr__jscu)[0], None), pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_table_subset = (
    table_subset_equiv)


def gen_str_and_dict_enc_cols_to_one_block_fn_txt(in_table_type,
    out_table_type, glbls, is_gatherv=False):
    assert bodo.string_array_type in in_table_type.type_to_blk and bodo.string_array_type in in_table_type.type_to_blk, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: Table type {in_table_type} does not contain both a string, and encoded string column'
    vivv__cumqc = in_table_type.type_to_blk[bodo.string_array_type]
    padv__svj = in_table_type.type_to_blk[bodo.dict_str_arr_type]
    norgn__glrz = in_table_type.block_to_arr_ind.get(vivv__cumqc)
    anuy__khip = in_table_type.block_to_arr_ind.get(padv__svj)
    iauj__hbqzo = []
    awk__jxlp = []
    gkwez__nvp = 0
    fzc__rbk = 0
    for utgi__fkom in range(len(norgn__glrz) + len(anuy__khip)):
        if gkwez__nvp == len(norgn__glrz):
            awk__jxlp.append(utgi__fkom)
            continue
        elif fzc__rbk == len(anuy__khip):
            iauj__hbqzo.append(utgi__fkom)
            continue
        ywcis__ulbsh = norgn__glrz[gkwez__nvp]
        govn__czo = anuy__khip[fzc__rbk]
        if ywcis__ulbsh < govn__czo:
            iauj__hbqzo.append(utgi__fkom)
            gkwez__nvp += 1
        else:
            awk__jxlp.append(utgi__fkom)
            fzc__rbk += 1
    assert 'output_table_str_arr_offsets_in_combined_block' not in glbls, "Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: key 'output_table_str_arr_idxs_in_combined_block' already present as a global variable"
    glbls['output_table_str_arr_offsets_in_combined_block'] = np.array(
        iauj__hbqzo)
    assert 'output_table_dict_enc_str_arr_offsets_in_combined_block' not in glbls, "Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: key 'output_table_str_arr_idxs_in_combined_block' already present as a global variable"
    glbls['output_table_dict_enc_str_arr_offsets_in_combined_block'
        ] = np.array(awk__jxlp)
    glbls['decode_if_dict_array'] = decode_if_dict_array
    liod__ayj = out_table_type.type_to_blk[bodo.string_array_type]
    assert f'arr_inds_{vivv__cumqc}' not in glbls, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: arr_inds_{vivv__cumqc} already present in global variables'
    glbls[f'arr_inds_{vivv__cumqc}'] = np.array(in_table_type.
        block_to_arr_ind[vivv__cumqc], dtype=np.int64)
    assert f'arr_inds_{padv__svj}' not in glbls, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: arr_inds_{padv__svj} already present in global variables'
    glbls[f'arr_inds_{padv__svj}'] = np.array(in_table_type.
        block_to_arr_ind[padv__svj], dtype=np.int64)
    qrjte__diipc = (
        f'  input_str_arr_list = get_table_block(T, {vivv__cumqc})\n')
    qrjte__diipc += (
        f'  input_dict_enc_str_arr_list = get_table_block(T, {padv__svj})\n')
    qrjte__diipc += f"""  out_arr_list_{liod__ayj} = alloc_list_like(input_str_arr_list, {len(iauj__hbqzo) + len(awk__jxlp)}, True)
"""
    qrjte__diipc += f"""  for input_str_ary_idx, output_str_arr_offset in enumerate(output_table_str_arr_offsets_in_combined_block):
"""
    qrjte__diipc += (
        f'    arr_ind_str = arr_inds_{vivv__cumqc}[input_str_ary_idx]\n')
    qrjte__diipc += f"""    ensure_column_unboxed(T, input_str_arr_list, input_str_ary_idx, arr_ind_str)
"""
    qrjte__diipc += (
        f'    out_arr_str = input_str_arr_list[input_str_ary_idx]\n')
    if is_gatherv:
        qrjte__diipc += f"""    out_arr_str = bodo.gatherv(out_arr_str, allgather, warn_if_rep, root)
"""
    qrjte__diipc += (
        f'    out_arr_list_{liod__ayj}[output_str_arr_offset] = out_arr_str\n')
    qrjte__diipc += f"""  for input_dict_enc_str_ary_idx, output_dict_enc_str_arr_offset in enumerate(output_table_dict_enc_str_arr_offsets_in_combined_block):
"""
    qrjte__diipc += (
        f'    arr_ind_dict_enc_str = arr_inds_{padv__svj}[input_dict_enc_str_ary_idx]\n'
        )
    qrjte__diipc += f"""    ensure_column_unboxed(T, input_dict_enc_str_arr_list, input_dict_enc_str_ary_idx, arr_ind_dict_enc_str)
"""
    qrjte__diipc += f"""    out_arr_dict_enc_str = decode_if_dict_array(input_dict_enc_str_arr_list[input_dict_enc_str_ary_idx])
"""
    if is_gatherv:
        qrjte__diipc += f"""    out_arr_dict_enc_str = bodo.gatherv(out_arr_dict_enc_str, allgather, warn_if_rep, root)
"""
    qrjte__diipc += f"""    out_arr_list_{liod__ayj}[output_dict_enc_str_arr_offset] = out_arr_dict_enc_str
"""
    qrjte__diipc += (
        f'  T2 = set_table_block(T2, out_arr_list_{liod__ayj}, {liod__ayj})\n')
    return qrjte__diipc


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    qrjte__diipc = 'def impl(T):\n'
    qrjte__diipc += f'  T2 = init_table(T, True)\n'
    qrjte__diipc += f'  l = len(T)\n'
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'set_table_block':
        set_table_block, 'set_table_len': set_table_len, 'alloc_list_like':
        alloc_list_like, 'decode_if_dict_array': decode_if_dict_array}
    out_table_type = bodo.hiframes.table.get_init_table_output_type(T, True)
    marw__aiuph = (bodo.string_array_type in T.type_to_blk and bodo.
        dict_str_arr_type in T.type_to_blk)
    if marw__aiuph:
        qrjte__diipc += gen_str_and_dict_enc_cols_to_one_block_fn_txt(T,
            out_table_type, glbls)
    for typ, xixhk__ssxl in T.type_to_blk.items():
        if marw__aiuph and typ in (bodo.string_array_type, bodo.
            dict_str_arr_type):
            continue
        if typ == bodo.dict_str_arr_type:
            assert bodo.string_array_type in out_table_type.type_to_blk, 'Error in decode_if_dict_table: If encoded string type is present in the input, then non-encoded string type should be present in the output'
            zezvj__nmz = out_table_type.type_to_blk[bodo.string_array_type]
        else:
            assert typ in out_table_type.type_to_blk, 'Error in decode_if_dict_table: All non-encoded string types present in the input should be present in the output'
            zezvj__nmz = out_table_type.type_to_blk[typ]
        glbls[f'arr_inds_{xixhk__ssxl}'] = np.array(T.block_to_arr_ind[
            xixhk__ssxl], dtype=np.int64)
        qrjte__diipc += (
            f'  arr_list_{xixhk__ssxl} = get_table_block(T, {xixhk__ssxl})\n')
        qrjte__diipc += f"""  out_arr_list_{xixhk__ssxl} = alloc_list_like(arr_list_{xixhk__ssxl}, len(arr_list_{xixhk__ssxl}), True)
"""
        qrjte__diipc += f'  for i in range(len(arr_list_{xixhk__ssxl})):\n'
        qrjte__diipc += (
            f'    arr_ind_{xixhk__ssxl} = arr_inds_{xixhk__ssxl}[i]\n')
        qrjte__diipc += f"""    ensure_column_unboxed(T, arr_list_{xixhk__ssxl}, i, arr_ind_{xixhk__ssxl})
"""
        qrjte__diipc += f"""    out_arr_{xixhk__ssxl} = decode_if_dict_array(arr_list_{xixhk__ssxl}[i])
"""
        qrjte__diipc += (
            f'    out_arr_list_{xixhk__ssxl}[i] = out_arr_{xixhk__ssxl}\n')
        qrjte__diipc += (
            f'  T2 = set_table_block(T2, out_arr_list_{xixhk__ssxl}, {zezvj__nmz})\n'
            )
    qrjte__diipc += f'  T2 = set_table_len(T2, l)\n'
    qrjte__diipc += f'  return T2\n'
    ljw__ghk = {}
    exec(qrjte__diipc, glbls, ljw__ghk)
    return ljw__ghk['impl']


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
        kloev__jway = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        kloev__jway = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            kloev__jway.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        dzw__lekh, kwkv__vtark = args
        table = cgutils.create_struct_proxy(table_type)(context, builder)
        table.len = kwkv__vtark
        bslb__scx = cgutils.unpack_tuple(builder, dzw__lekh)
        for i, zqu__jju in enumerate(bslb__scx):
            setattr(table, f'block_{i}', zqu__jju)
            context.nrt.incref(builder, types.List(kloev__jway[i]), zqu__jju)
        return table._getvalue()
    table_type = TableType(tuple(kloev__jway), True)
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
        govu__ejp = True
    else:
        kept_cols = set(np.arange(len(in_col_inds)))
        govu__ejp = False
    extra_arrs_no_series = ', '.join(f'get_series_data(extra_arrs_t[{i}])' if
        isinstance(extra_arrs_t[i], SeriesType) else f'extra_arrs_t[{i}]' for
        i in range(len(extra_arrs_t)))
    extra_arrs_no_series = (
        f"({extra_arrs_no_series}{',' if len(extra_arrs_t) == 1 else ''})")
    if isinstance(in_table_t, (types.BaseTuple, types.NoneType)):
        return _logical_tuple_table_to_table_codegen(in_table_t,
            extra_arrs_t, in_col_inds, kept_cols, n_table_cols_t,
            out_table_type_t, extra_arrs_no_series)
    bytiz__axg = len(in_table_t.arr_types)
    out_table_type = TableType(tuple(in_table_t.arr_types[i] if i <
        bytiz__axg else _to_arr_if_series(extra_arrs_t.types[i - bytiz__axg
        ]) for i in in_col_inds)) if is_overload_none(out_table_type_t
        ) else unwrap_typeref(out_table_type_t)
    glbls.update({'init_table': init_table, 'set_table_len': set_table_len,
        'out_table_type': out_table_type})
    qrjte__diipc = """def impl(in_table_t, extra_arrs_t, in_col_inds_t, n_table_cols_t, out_table_type_t=None, used_cols=None):
"""
    if any(isinstance(t, SeriesType) for t in extra_arrs_t.types):
        qrjte__diipc += f'  extra_arrs_t = {extra_arrs_no_series}\n'
    qrjte__diipc += f'  T1 = in_table_t\n'
    qrjte__diipc += f'  T2 = init_table(out_table_type, False)\n'
    qrjte__diipc += f'  T2 = set_table_len(T2, len(T1))\n'
    if govu__ejp and len(kept_cols) == 0:
        qrjte__diipc += f'  return T2\n'
        ljw__ghk = {}
        exec(qrjte__diipc, glbls, ljw__ghk)
        return ljw__ghk['impl']
    if govu__ejp:
        qrjte__diipc += f'  kept_cols_set = set(kept_cols)\n'
    for typ, hbl__dpumu in out_table_type.type_to_blk.items():
        glbls[f'arr_list_typ_{hbl__dpumu}'] = types.List(typ)
        jpwg__ldavs = len(out_table_type.block_to_arr_ind[hbl__dpumu])
        qrjte__diipc += f"""  out_arr_list_{hbl__dpumu} = alloc_list_like(arr_list_typ_{hbl__dpumu}, {jpwg__ldavs}, False)
"""
        if typ in in_table_t.type_to_blk:
            zslff__rbirm = in_table_t.type_to_blk[typ]
            gixg__jdp = []
            hyn__bkqxb = []
            for zcr__cuyv in out_table_type.block_to_arr_ind[hbl__dpumu]:
                bpje__wrnm = in_col_inds[zcr__cuyv]
                if bpje__wrnm < bytiz__axg:
                    gixg__jdp.append(in_table_t.block_offsets[bpje__wrnm])
                    hyn__bkqxb.append(bpje__wrnm)
                else:
                    gixg__jdp.append(-1)
                    hyn__bkqxb.append(-1)
            glbls[f'in_idxs_{hbl__dpumu}'] = np.array(gixg__jdp, np.int64)
            glbls[f'in_arr_inds_{hbl__dpumu}'] = np.array(hyn__bkqxb, np.int64)
            if govu__ejp:
                glbls[f'out_arr_inds_{hbl__dpumu}'] = np.array(out_table_type
                    .block_to_arr_ind[hbl__dpumu], dtype=np.int64)
            qrjte__diipc += (
                f'  in_arr_list_{hbl__dpumu} = get_table_block(T1, {zslff__rbirm})\n'
                )
            qrjte__diipc += (
                f'  for i in range(len(out_arr_list_{hbl__dpumu})):\n')
            qrjte__diipc += (
                f'    in_offset_{hbl__dpumu} = in_idxs_{hbl__dpumu}[i]\n')
            qrjte__diipc += f'    if in_offset_{hbl__dpumu} == -1:\n'
            qrjte__diipc += f'      continue\n'
            qrjte__diipc += (
                f'    in_arr_ind_{hbl__dpumu} = in_arr_inds_{hbl__dpumu}[i]\n')
            if govu__ejp:
                qrjte__diipc += f"""    if out_arr_inds_{hbl__dpumu}[i] not in kept_cols_set: continue
"""
            qrjte__diipc += f"""    ensure_column_unboxed(T1, in_arr_list_{hbl__dpumu}, in_offset_{hbl__dpumu}, in_arr_ind_{hbl__dpumu})
"""
            qrjte__diipc += f"""    out_arr_list_{hbl__dpumu}[i] = in_arr_list_{hbl__dpumu}[in_offset_{hbl__dpumu}]
"""
        for i, zcr__cuyv in enumerate(out_table_type.block_to_arr_ind[
            hbl__dpumu]):
            if zcr__cuyv not in kept_cols:
                continue
            bpje__wrnm = in_col_inds[zcr__cuyv]
            if bpje__wrnm >= bytiz__axg:
                qrjte__diipc += f"""  out_arr_list_{hbl__dpumu}[{i}] = extra_arrs_t[{bpje__wrnm - bytiz__axg}]
"""
        qrjte__diipc += (
            f'  T2 = set_table_block(T2, out_arr_list_{hbl__dpumu}, {hbl__dpumu})\n'
            )
    qrjte__diipc += f'  return T2\n'
    glbls.update({'alloc_list_like': alloc_list_like, 'set_table_block':
        set_table_block, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'get_series_data':
        bodo.hiframes.pd_series_ext.get_series_data})
    ljw__ghk = {}
    exec(qrjte__diipc, glbls, ljw__ghk)
    return ljw__ghk['impl']


def _logical_tuple_table_to_table_codegen(in_table_t, extra_arrs_t,
    in_col_inds, kept_cols, n_table_cols_t, out_table_type_t,
    extra_arrs_no_series):
    bytiz__axg = get_overload_const_int(n_table_cols_t
        ) if is_overload_constant_int(n_table_cols_t) else len(in_table_t.types
        )
    out_table_type = TableType(tuple(in_table_t.types[i] if i < bytiz__axg else
        _to_arr_if_series(extra_arrs_t.types[i - bytiz__axg]) for i in
        in_col_inds)) if is_overload_none(out_table_type_t
        ) else unwrap_typeref(out_table_type_t)
    omdfi__izrcs = None
    if not is_overload_none(in_table_t):
        for i, t in enumerate(in_table_t.types):
            if t != types.none:
                omdfi__izrcs = f'in_table_t[{i}]'
                break
    if omdfi__izrcs is None:
        for i, t in enumerate(extra_arrs_t.types):
            if t != types.none:
                omdfi__izrcs = f'extra_arrs_t[{i}]'
                break
    assert omdfi__izrcs is not None, 'no array found in input data'
    qrjte__diipc = """def impl(in_table_t, extra_arrs_t, in_col_inds_t, n_table_cols_t, out_table_type_t=None, used_cols=None):
"""
    if any(isinstance(t, SeriesType) for t in extra_arrs_t.types):
        qrjte__diipc += f'  extra_arrs_t = {extra_arrs_no_series}\n'
    qrjte__diipc += f'  T1 = in_table_t\n'
    qrjte__diipc += f'  T2 = init_table(out_table_type, False)\n'
    qrjte__diipc += f'  T2 = set_table_len(T2, len({omdfi__izrcs}))\n'
    glbls = {}
    for typ, hbl__dpumu in out_table_type.type_to_blk.items():
        glbls[f'arr_list_typ_{hbl__dpumu}'] = types.List(typ)
        jpwg__ldavs = len(out_table_type.block_to_arr_ind[hbl__dpumu])
        qrjte__diipc += f"""  out_arr_list_{hbl__dpumu} = alloc_list_like(arr_list_typ_{hbl__dpumu}, {jpwg__ldavs}, False)
"""
        for i, zcr__cuyv in enumerate(out_table_type.block_to_arr_ind[
            hbl__dpumu]):
            if zcr__cuyv not in kept_cols:
                continue
            bpje__wrnm = in_col_inds[zcr__cuyv]
            if bpje__wrnm < bytiz__axg:
                qrjte__diipc += (
                    f'  out_arr_list_{hbl__dpumu}[{i}] = T1[{bpje__wrnm}]\n')
            else:
                qrjte__diipc += f"""  out_arr_list_{hbl__dpumu}[{i}] = extra_arrs_t[{bpje__wrnm - bytiz__axg}]
"""
        qrjte__diipc += (
            f'  T2 = set_table_block(T2, out_arr_list_{hbl__dpumu}, {hbl__dpumu})\n'
            )
    qrjte__diipc += f'  return T2\n'
    glbls.update({'init_table': init_table, 'alloc_list_like':
        alloc_list_like, 'set_table_block': set_table_block,
        'set_table_len': set_table_len, 'out_table_type': out_table_type,
        'get_series_data': bodo.hiframes.pd_series_ext.get_series_data})
    ljw__ghk = {}
    exec(qrjte__diipc, glbls, ljw__ghk)
    return ljw__ghk['impl']


def logical_table_to_table_equiv(self, scope, equiv_set, loc, args, kws):
    unfv__vpor = args[0]
    vkdjs__ifq = args[1]
    if equiv_set.has_shape(unfv__vpor):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            unfv__vpor)[0], None), pre=[])
    if equiv_set.has_shape(vkdjs__ifq):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            vkdjs__ifq)[0], None), pre=[])


(ArrayAnalysis._analyze_op_call_bodo_hiframes_table_logical_table_to_table
    ) = logical_table_to_table_equiv


def alias_ext_logical_table_to_table(lhs_name, args, alias_map, arg_aliases):
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['logical_table_to_table',
    'bodo.hiframes.table'] = alias_ext_logical_table_to_table
