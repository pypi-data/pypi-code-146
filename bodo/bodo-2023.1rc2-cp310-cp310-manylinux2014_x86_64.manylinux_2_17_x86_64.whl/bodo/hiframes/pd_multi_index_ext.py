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
        csvd__giusa = [('data', types.Tuple(fe_type.array_types)), ('names',
            types.Tuple(fe_type.names_typ)), ('name', fe_type.name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, csvd__giusa)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[tdbau__ywrse].values) for
        tdbau__ywrse in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (ywyct__mpraf) for ywyct__mpraf in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    sir__vcm = c.context.insert_const_string(c.builder.module, 'pandas')
    zixg__kpka = c.pyapi.import_module_noblock(sir__vcm)
    ufo__sdcvs = c.pyapi.object_getattr_string(zixg__kpka, 'MultiIndex')
    ipv__gpp = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types), ipv__gpp.data
        )
    guiqr__pwns = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        ipv__gpp.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ), ipv__gpp.names)
    pzpo__xgs = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        ipv__gpp.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, ipv__gpp.name)
    fqsj__lixr = c.pyapi.from_native_value(typ.name_typ, ipv__gpp.name, c.
        env_manager)
    gpvqv__xslaf = c.pyapi.borrow_none()
    kxw__xdw = c.pyapi.call_method(ufo__sdcvs, 'from_arrays', (guiqr__pwns,
        gpvqv__xslaf, pzpo__xgs))
    c.pyapi.object_setattr_string(kxw__xdw, 'name', fqsj__lixr)
    c.pyapi.decref(guiqr__pwns)
    c.pyapi.decref(pzpo__xgs)
    c.pyapi.decref(fqsj__lixr)
    c.pyapi.decref(zixg__kpka)
    c.pyapi.decref(ufo__sdcvs)
    c.context.nrt.decref(c.builder, typ, val)
    return kxw__xdw


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    lell__ojyad = []
    zvh__spi = []
    for tdbau__ywrse in range(typ.nlevels):
        wcny__qmc = c.pyapi.unserialize(c.pyapi.serialize_object(tdbau__ywrse))
        and__mkswz = c.pyapi.call_method(val, 'get_level_values', (wcny__qmc,))
        pmq__xqb = c.pyapi.object_getattr_string(and__mkswz, 'values')
        c.pyapi.decref(and__mkswz)
        c.pyapi.decref(wcny__qmc)
        ikcr__dzyp = c.pyapi.to_native_value(typ.array_types[tdbau__ywrse],
            pmq__xqb).value
        lell__ojyad.append(ikcr__dzyp)
        zvh__spi.append(pmq__xqb)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, lell__ojyad)
    else:
        data = cgutils.pack_struct(c.builder, lell__ojyad)
    pzpo__xgs = c.pyapi.object_getattr_string(val, 'names')
    wxd__urdd = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    wtgje__pimy = c.pyapi.call_function_objargs(wxd__urdd, (pzpo__xgs,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), wtgje__pimy
        ).value
    fqsj__lixr = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, fqsj__lixr).value
    ipv__gpp = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ipv__gpp.data = data
    ipv__gpp.names = names
    ipv__gpp.name = name
    for pmq__xqb in zvh__spi:
        c.pyapi.decref(pmq__xqb)
    c.pyapi.decref(pzpo__xgs)
    c.pyapi.decref(wxd__urdd)
    c.pyapi.decref(wtgje__pimy)
    c.pyapi.decref(fqsj__lixr)
    return NativeValue(ipv__gpp._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    yoo__ptoj = 'pandas.MultiIndex.from_product'
    hxocx__xicur = dict(sortorder=sortorder)
    lhtul__kimnj = dict(sortorder=None)
    check_unsupported_args(yoo__ptoj, hxocx__xicur, lhtul__kimnj,
        package_name='pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{yoo__ptoj}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{yoo__ptoj}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{yoo__ptoj}: iterables and names must be of the same length.')


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
    pxgdw__qdvjs = MultiIndexType(array_types, names_typ)
    hlzx__sjxta = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, hlzx__sjxta, pxgdw__qdvjs)
    rislq__khy = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{hlzx__sjxta}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    zzqx__fkc = {}
    exec(rislq__khy, globals(), zzqx__fkc)
    zlkxa__aoxl = zzqx__fkc['impl']
    return zlkxa__aoxl


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        lrajp__gpkgy, cfkvw__qhyta, wdvd__nql = args
        swinb__ztm = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        swinb__ztm.data = lrajp__gpkgy
        swinb__ztm.names = cfkvw__qhyta
        swinb__ztm.name = wdvd__nql
        context.nrt.incref(builder, signature.args[0], lrajp__gpkgy)
        context.nrt.incref(builder, signature.args[1], cfkvw__qhyta)
        context.nrt.incref(builder, signature.args[2], wdvd__nql)
        return swinb__ztm._getvalue()
    agevj__cpw = MultiIndexType(data.types, names.types, name)
    return agevj__cpw(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        lyvjz__vwwct = len(I.array_types)
        rislq__khy = 'def impl(I, ind):\n'
        rislq__khy += '  data = I._data\n'
        rislq__khy += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(
            f'ensure_contig_if_np(data[{tdbau__ywrse}][ind])' for
            tdbau__ywrse in range(lyvjz__vwwct))))
        zzqx__fkc = {}
        exec(rislq__khy, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, zzqx__fkc)
        zlkxa__aoxl = zzqx__fkc['impl']
        return zlkxa__aoxl


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    nnx__mjz, yzec__doal = sig.args
    if nnx__mjz != yzec__doal:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
