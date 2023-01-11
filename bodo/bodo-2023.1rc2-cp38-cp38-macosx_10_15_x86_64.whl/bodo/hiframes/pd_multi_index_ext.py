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
        hvrqs__kdg = [('data', types.Tuple(fe_type.array_types)), ('names',
            types.Tuple(fe_type.names_typ)), ('name', fe_type.name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, hvrqs__kdg)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[kqy__xueju].values) for
        kqy__xueju in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (imuwa__wce) for imuwa__wce in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    wtmu__kmg = c.context.insert_const_string(c.builder.module, 'pandas')
    jpc__aeay = c.pyapi.import_module_noblock(wtmu__kmg)
    ycxb__abdbt = c.pyapi.object_getattr_string(jpc__aeay, 'MultiIndex')
    ovah__gcekb = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types),
        ovah__gcekb.data)
    pkm__zqon = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        ovah__gcekb.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ), ovah__gcekb
        .names)
    ovmt__aqvh = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        ovah__gcekb.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, ovah__gcekb.name)
    atmxr__zxd = c.pyapi.from_native_value(typ.name_typ, ovah__gcekb.name,
        c.env_manager)
    radlk__rlug = c.pyapi.borrow_none()
    kwgf__cqhny = c.pyapi.call_method(ycxb__abdbt, 'from_arrays', (
        pkm__zqon, radlk__rlug, ovmt__aqvh))
    c.pyapi.object_setattr_string(kwgf__cqhny, 'name', atmxr__zxd)
    c.pyapi.decref(pkm__zqon)
    c.pyapi.decref(ovmt__aqvh)
    c.pyapi.decref(atmxr__zxd)
    c.pyapi.decref(jpc__aeay)
    c.pyapi.decref(ycxb__abdbt)
    c.context.nrt.decref(c.builder, typ, val)
    return kwgf__cqhny


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    sdrg__lntu = []
    zfny__smgnw = []
    for kqy__xueju in range(typ.nlevels):
        fywy__khv = c.pyapi.unserialize(c.pyapi.serialize_object(kqy__xueju))
        tllkq__gzfgv = c.pyapi.call_method(val, 'get_level_values', (
            fywy__khv,))
        tzl__ggt = c.pyapi.object_getattr_string(tllkq__gzfgv, 'values')
        c.pyapi.decref(tllkq__gzfgv)
        c.pyapi.decref(fywy__khv)
        uxrm__kyw = c.pyapi.to_native_value(typ.array_types[kqy__xueju],
            tzl__ggt).value
        sdrg__lntu.append(uxrm__kyw)
        zfny__smgnw.append(tzl__ggt)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, sdrg__lntu)
    else:
        data = cgutils.pack_struct(c.builder, sdrg__lntu)
    ovmt__aqvh = c.pyapi.object_getattr_string(val, 'names')
    ddsoj__mdl = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    lppwg__ckm = c.pyapi.call_function_objargs(ddsoj__mdl, (ovmt__aqvh,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), lppwg__ckm
        ).value
    atmxr__zxd = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, atmxr__zxd).value
    ovah__gcekb = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ovah__gcekb.data = data
    ovah__gcekb.names = names
    ovah__gcekb.name = name
    for tzl__ggt in zfny__smgnw:
        c.pyapi.decref(tzl__ggt)
    c.pyapi.decref(ovmt__aqvh)
    c.pyapi.decref(ddsoj__mdl)
    c.pyapi.decref(lppwg__ckm)
    c.pyapi.decref(atmxr__zxd)
    return NativeValue(ovah__gcekb._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    hzx__anyz = 'pandas.MultiIndex.from_product'
    iywvq__qdm = dict(sortorder=sortorder)
    dxub__hfzds = dict(sortorder=None)
    check_unsupported_args(hzx__anyz, iywvq__qdm, dxub__hfzds, package_name
        ='pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{hzx__anyz}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{hzx__anyz}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{hzx__anyz}: iterables and names must be of the same length.')


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
    xad__dpkfw = MultiIndexType(array_types, names_typ)
    oipn__sskdz = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, oipn__sskdz, xad__dpkfw)
    twtkq__jza = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{oipn__sskdz}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    ijlj__volg = {}
    exec(twtkq__jza, globals(), ijlj__volg)
    etffp__gwwo = ijlj__volg['impl']
    return etffp__gwwo


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        fejzo__tver, izmr__gmnp, xdnpw__kpwpz = args
        iyx__uyar = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        iyx__uyar.data = fejzo__tver
        iyx__uyar.names = izmr__gmnp
        iyx__uyar.name = xdnpw__kpwpz
        context.nrt.incref(builder, signature.args[0], fejzo__tver)
        context.nrt.incref(builder, signature.args[1], izmr__gmnp)
        context.nrt.incref(builder, signature.args[2], xdnpw__kpwpz)
        return iyx__uyar._getvalue()
    ojxlw__nrst = MultiIndexType(data.types, names.types, name)
    return ojxlw__nrst(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        cxrv__lzs = len(I.array_types)
        twtkq__jza = 'def impl(I, ind):\n'
        twtkq__jza += '  data = I._data\n'
        twtkq__jza += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(
            f'ensure_contig_if_np(data[{kqy__xueju}][ind])' for kqy__xueju in
            range(cxrv__lzs))))
        ijlj__volg = {}
        exec(twtkq__jza, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, ijlj__volg)
        etffp__gwwo = ijlj__volg['impl']
        return etffp__gwwo


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    rale__chd, rtcol__sworm = sig.args
    if rale__chd != rtcol__sworm:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
