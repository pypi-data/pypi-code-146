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
        yfxe__hbji = [('data', types.Tuple(fe_type.array_types)), ('names',
            types.Tuple(fe_type.names_typ)), ('name', fe_type.name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, yfxe__hbji)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[ytskd__oxtuc].values) for
        ytskd__oxtuc in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (xleb__pihvi) for xleb__pihvi in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    tpbg__xjl = c.context.insert_const_string(c.builder.module, 'pandas')
    cvxbn__mnqa = c.pyapi.import_module_noblock(tpbg__xjl)
    ood__zpuzn = c.pyapi.object_getattr_string(cvxbn__mnqa, 'MultiIndex')
    cdw__fomy = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types), cdw__fomy
        .data)
    unfog__tdwx = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        cdw__fomy.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ), cdw__fomy.names
        )
    rjd__uee = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        cdw__fomy.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, cdw__fomy.name)
    whuxi__haj = c.pyapi.from_native_value(typ.name_typ, cdw__fomy.name, c.
        env_manager)
    mgcli__bmy = c.pyapi.borrow_none()
    agm__lhbjx = c.pyapi.call_method(ood__zpuzn, 'from_arrays', (
        unfog__tdwx, mgcli__bmy, rjd__uee))
    c.pyapi.object_setattr_string(agm__lhbjx, 'name', whuxi__haj)
    c.pyapi.decref(unfog__tdwx)
    c.pyapi.decref(rjd__uee)
    c.pyapi.decref(whuxi__haj)
    c.pyapi.decref(cvxbn__mnqa)
    c.pyapi.decref(ood__zpuzn)
    c.context.nrt.decref(c.builder, typ, val)
    return agm__lhbjx


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    seq__lcry = []
    mena__mzeje = []
    for ytskd__oxtuc in range(typ.nlevels):
        fxeft__pma = c.pyapi.unserialize(c.pyapi.serialize_object(ytskd__oxtuc)
            )
        enpy__jzo = c.pyapi.call_method(val, 'get_level_values', (fxeft__pma,))
        awic__xrpc = c.pyapi.object_getattr_string(enpy__jzo, 'values')
        c.pyapi.decref(enpy__jzo)
        c.pyapi.decref(fxeft__pma)
        oicz__sfxl = c.pyapi.to_native_value(typ.array_types[ytskd__oxtuc],
            awic__xrpc).value
        seq__lcry.append(oicz__sfxl)
        mena__mzeje.append(awic__xrpc)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, seq__lcry)
    else:
        data = cgutils.pack_struct(c.builder, seq__lcry)
    rjd__uee = c.pyapi.object_getattr_string(val, 'names')
    ldsxx__rcti = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    xmyoe__snfj = c.pyapi.call_function_objargs(ldsxx__rcti, (rjd__uee,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), xmyoe__snfj
        ).value
    whuxi__haj = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, whuxi__haj).value
    cdw__fomy = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    cdw__fomy.data = data
    cdw__fomy.names = names
    cdw__fomy.name = name
    for awic__xrpc in mena__mzeje:
        c.pyapi.decref(awic__xrpc)
    c.pyapi.decref(rjd__uee)
    c.pyapi.decref(ldsxx__rcti)
    c.pyapi.decref(xmyoe__snfj)
    c.pyapi.decref(whuxi__haj)
    return NativeValue(cdw__fomy._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    dqvwb__jkh = 'pandas.MultiIndex.from_product'
    gtuk__glcj = dict(sortorder=sortorder)
    vusgm__fcvxz = dict(sortorder=None)
    check_unsupported_args(dqvwb__jkh, gtuk__glcj, vusgm__fcvxz,
        package_name='pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{dqvwb__jkh}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{dqvwb__jkh}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{dqvwb__jkh}: iterables and names must be of the same length.')


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
    deoys__ksp = MultiIndexType(array_types, names_typ)
    psx__vesky = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, psx__vesky, deoys__ksp)
    mpj__drp = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{psx__vesky}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    wpvsd__vej = {}
    exec(mpj__drp, globals(), wpvsd__vej)
    ede__yvsh = wpvsd__vej['impl']
    return ede__yvsh


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        wbzp__pdes, pqk__xqa, homg__qioe = args
        ggcd__pgfee = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        ggcd__pgfee.data = wbzp__pdes
        ggcd__pgfee.names = pqk__xqa
        ggcd__pgfee.name = homg__qioe
        context.nrt.incref(builder, signature.args[0], wbzp__pdes)
        context.nrt.incref(builder, signature.args[1], pqk__xqa)
        context.nrt.incref(builder, signature.args[2], homg__qioe)
        return ggcd__pgfee._getvalue()
    htkwu__euwb = MultiIndexType(data.types, names.types, name)
    return htkwu__euwb(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        syv__lcfl = len(I.array_types)
        mpj__drp = 'def impl(I, ind):\n'
        mpj__drp += '  data = I._data\n'
        mpj__drp += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(
            f'ensure_contig_if_np(data[{ytskd__oxtuc}][ind])' for
            ytskd__oxtuc in range(syv__lcfl))))
        wpvsd__vej = {}
        exec(mpj__drp, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, wpvsd__vej)
        ede__yvsh = wpvsd__vej['impl']
        return ede__yvsh


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    kxpss__aqs, oqw__huj = sig.args
    if kxpss__aqs != oqw__huj:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
