"""Support for MultiIndex type of Pandas
"""
import operator
import numba
import pandas as pd
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, register_model, typeof_impl, unbox
from bodo.utils.conversion import ensure_contig_if_np
from bodo.utils.typing import BodoError, check_unsupported_args, dtype_to_array_type, get_val_type_maybe_str_literal, is_overload_none


class MultiIndexType(types.ArrayCompatible):

    def __init__(self, array_types, names_typ=None, name_typ=None):
        names_typ = (types.none,) * len(array_types
            ) if names_typ is None else names_typ
        name_typ = types.none if name_typ is None else name_typ
        self.array_types = array_types
        self.names_typ = names_typ
        self.name_typ = name_typ
        super(MultiIndexType, self).__init__(name=
            'MultiIndexType({}, {}, {})'.format(array_types, names_typ,
            name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return MultiIndexType(self.array_types, self.names_typ, self.name_typ)

    @property
    def nlevels(self):
        return len(self.array_types)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(MultiIndexType)
class MultiIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        mnp__xzsw = [('data', types.Tuple(fe_type.array_types)), ('names',
            types.Tuple(fe_type.names_typ)), ('name', fe_type.name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, mnp__xzsw)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[yapo__mwdn].values) for
        yapo__mwdn in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (ptv__siqjc) for ptv__siqjc in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    bvoe__wgvtu = c.context.insert_const_string(c.builder.module, 'pandas')
    vvu__eehrj = c.pyapi.import_module_noblock(bvoe__wgvtu)
    xcmra__rij = c.pyapi.object_getattr_string(vvu__eehrj, 'MultiIndex')
    jiwet__fjf = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types),
        jiwet__fjf.data)
    ctg__jtez = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        jiwet__fjf.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ), jiwet__fjf.
        names)
    nskw__wwo = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        jiwet__fjf.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, jiwet__fjf.name)
    svkd__cceb = c.pyapi.from_native_value(typ.name_typ, jiwet__fjf.name, c
        .env_manager)
    kcymv__goyxj = c.pyapi.borrow_none()
    clm__dqpe = c.pyapi.call_method(xcmra__rij, 'from_arrays', (ctg__jtez,
        kcymv__goyxj, nskw__wwo))
    c.pyapi.object_setattr_string(clm__dqpe, 'name', svkd__cceb)
    c.pyapi.decref(ctg__jtez)
    c.pyapi.decref(nskw__wwo)
    c.pyapi.decref(svkd__cceb)
    c.pyapi.decref(vvu__eehrj)
    c.pyapi.decref(xcmra__rij)
    c.context.nrt.decref(c.builder, typ, val)
    return clm__dqpe


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    qbh__sekn = []
    fft__mkhi = []
    for yapo__mwdn in range(typ.nlevels):
        rhqia__ppfio = c.pyapi.unserialize(c.pyapi.serialize_object(yapo__mwdn)
            )
        egje__dez = c.pyapi.call_method(val, 'get_level_values', (
            rhqia__ppfio,))
        tfizy__tfvq = c.pyapi.object_getattr_string(egje__dez, 'values')
        c.pyapi.decref(egje__dez)
        c.pyapi.decref(rhqia__ppfio)
        yoiem__sxysa = c.pyapi.to_native_value(typ.array_types[yapo__mwdn],
            tfizy__tfvq).value
        qbh__sekn.append(yoiem__sxysa)
        fft__mkhi.append(tfizy__tfvq)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, qbh__sekn)
    else:
        data = cgutils.pack_struct(c.builder, qbh__sekn)
    nskw__wwo = c.pyapi.object_getattr_string(val, 'names')
    hzds__xbdm = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    djmcz__hblwj = c.pyapi.call_function_objargs(hzds__xbdm, (nskw__wwo,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), djmcz__hblwj
        ).value
    svkd__cceb = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, svkd__cceb).value
    jiwet__fjf = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    jiwet__fjf.data = data
    jiwet__fjf.names = names
    jiwet__fjf.name = name
    for tfizy__tfvq in fft__mkhi:
        c.pyapi.decref(tfizy__tfvq)
    c.pyapi.decref(nskw__wwo)
    c.pyapi.decref(hzds__xbdm)
    c.pyapi.decref(djmcz__hblwj)
    c.pyapi.decref(svkd__cceb)
    return NativeValue(jiwet__fjf._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    hszs__nfxl = 'pandas.MultiIndex.from_product'
    ada__dwjz = dict(sortorder=sortorder)
    yyosq__wql = dict(sortorder=None)
    check_unsupported_args(hszs__nfxl, ada__dwjz, yyosq__wql, package_name=
        'pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{hszs__nfxl}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{hszs__nfxl}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{hszs__nfxl}: iterables and names must be of the same length.')


def from_product(iterable, sortorder=None, names=None):
    pass


@overload(from_product)
def from_product_overload(iterables, sortorder=None, names=None):
    from_product_error_checking(iterables, sortorder, names)
    array_types = tuple(dtype_to_array_type(iterable.dtype) for iterable in
        iterables)
    if is_overload_none(names):
        names_typ = tuple([types.none] * len(iterables))
    else:
        names_typ = names.types
    nkm__ptdix = MultiIndexType(array_types, names_typ)
    ytzes__ivqt = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, ytzes__ivqt, nkm__ptdix)
    wmctu__lyby = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{ytzes__ivqt}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    hrj__qaep = {}
    exec(wmctu__lyby, globals(), hrj__qaep)
    rbd__wfif = hrj__qaep['impl']
    return rbd__wfif


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        fur__iyw, nxwr__eazlu, xlrjd__zan = args
        tqkp__ziqn = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        tqkp__ziqn.data = fur__iyw
        tqkp__ziqn.names = nxwr__eazlu
        tqkp__ziqn.name = xlrjd__zan
        context.nrt.incref(builder, signature.args[0], fur__iyw)
        context.nrt.incref(builder, signature.args[1], nxwr__eazlu)
        context.nrt.incref(builder, signature.args[2], xlrjd__zan)
        return tqkp__ziqn._getvalue()
    gzxrt__rhy = MultiIndexType(data.types, names.types, name)
    return gzxrt__rhy(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        uru__asl = len(I.array_types)
        wmctu__lyby = 'def impl(I, ind):\n'
        wmctu__lyby += '  data = I._data\n'
        wmctu__lyby += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(
            f'ensure_contig_if_np(data[{yapo__mwdn}][ind])' for yapo__mwdn in
            range(uru__asl))))
        hrj__qaep = {}
        exec(wmctu__lyby, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, hrj__qaep)
        rbd__wfif = hrj__qaep['impl']
        return rbd__wfif


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    evk__qvzrz, gbuy__blty = sig.args
    if evk__qvzrz != gbuy__blty:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
