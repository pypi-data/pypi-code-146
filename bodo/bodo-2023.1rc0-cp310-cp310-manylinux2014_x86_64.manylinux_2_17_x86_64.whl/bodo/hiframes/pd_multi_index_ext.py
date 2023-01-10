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
        dwy__gaeqd = [('data', types.Tuple(fe_type.array_types)), ('names',
            types.Tuple(fe_type.names_typ)), ('name', fe_type.name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, dwy__gaeqd)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[tlm__fyr].values) for
        tlm__fyr in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (bqb__jjjk) for bqb__jjjk in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    kvfdb__nhh = c.context.insert_const_string(c.builder.module, 'pandas')
    bnzzy__ofzd = c.pyapi.import_module_noblock(kvfdb__nhh)
    enf__rah = c.pyapi.object_getattr_string(bnzzy__ofzd, 'MultiIndex')
    vtpcu__mbmmf = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types),
        vtpcu__mbmmf.data)
    rnh__lffa = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        vtpcu__mbmmf.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ),
        vtpcu__mbmmf.names)
    coa__vpijj = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        vtpcu__mbmmf.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, vtpcu__mbmmf.name)
    mjg__yks = c.pyapi.from_native_value(typ.name_typ, vtpcu__mbmmf.name, c
        .env_manager)
    twj__hbwj = c.pyapi.borrow_none()
    qvbak__ghwb = c.pyapi.call_method(enf__rah, 'from_arrays', (rnh__lffa,
        twj__hbwj, coa__vpijj))
    c.pyapi.object_setattr_string(qvbak__ghwb, 'name', mjg__yks)
    c.pyapi.decref(rnh__lffa)
    c.pyapi.decref(coa__vpijj)
    c.pyapi.decref(mjg__yks)
    c.pyapi.decref(bnzzy__ofzd)
    c.pyapi.decref(enf__rah)
    c.context.nrt.decref(c.builder, typ, val)
    return qvbak__ghwb


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    qgsvo__ysw = []
    wypk__dkb = []
    for tlm__fyr in range(typ.nlevels):
        jkgtg__gqb = c.pyapi.unserialize(c.pyapi.serialize_object(tlm__fyr))
        tnir__auab = c.pyapi.call_method(val, 'get_level_values', (jkgtg__gqb,)
            )
        muumv__lbjc = c.pyapi.object_getattr_string(tnir__auab, 'values')
        c.pyapi.decref(tnir__auab)
        c.pyapi.decref(jkgtg__gqb)
        sti__hlqd = c.pyapi.to_native_value(typ.array_types[tlm__fyr],
            muumv__lbjc).value
        qgsvo__ysw.append(sti__hlqd)
        wypk__dkb.append(muumv__lbjc)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, qgsvo__ysw)
    else:
        data = cgutils.pack_struct(c.builder, qgsvo__ysw)
    coa__vpijj = c.pyapi.object_getattr_string(val, 'names')
    utl__nlpoh = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    bdg__mvaut = c.pyapi.call_function_objargs(utl__nlpoh, (coa__vpijj,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), bdg__mvaut
        ).value
    mjg__yks = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, mjg__yks).value
    vtpcu__mbmmf = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    vtpcu__mbmmf.data = data
    vtpcu__mbmmf.names = names
    vtpcu__mbmmf.name = name
    for muumv__lbjc in wypk__dkb:
        c.pyapi.decref(muumv__lbjc)
    c.pyapi.decref(coa__vpijj)
    c.pyapi.decref(utl__nlpoh)
    c.pyapi.decref(bdg__mvaut)
    c.pyapi.decref(mjg__yks)
    return NativeValue(vtpcu__mbmmf._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    mui__oue = 'pandas.MultiIndex.from_product'
    lvcig__sxx = dict(sortorder=sortorder)
    hkguo__cao = dict(sortorder=None)
    check_unsupported_args(mui__oue, lvcig__sxx, hkguo__cao, package_name=
        'pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{mui__oue}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{mui__oue}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{mui__oue}: iterables and names must be of the same length.')


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
    wgs__lpr = MultiIndexType(array_types, names_typ)
    jdzau__wzps = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, jdzau__wzps, wgs__lpr)
    mwx__mzmzo = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{jdzau__wzps}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    eyq__cdmar = {}
    exec(mwx__mzmzo, globals(), eyq__cdmar)
    oke__mlngr = eyq__cdmar['impl']
    return oke__mlngr


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        wdfae__mrda, grpw__eaj, xpjbl__nsun = args
        rdtep__psxp = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        rdtep__psxp.data = wdfae__mrda
        rdtep__psxp.names = grpw__eaj
        rdtep__psxp.name = xpjbl__nsun
        context.nrt.incref(builder, signature.args[0], wdfae__mrda)
        context.nrt.incref(builder, signature.args[1], grpw__eaj)
        context.nrt.incref(builder, signature.args[2], xpjbl__nsun)
        return rdtep__psxp._getvalue()
    irjmq__zfdo = MultiIndexType(data.types, names.types, name)
    return irjmq__zfdo(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        qzeg__eohs = len(I.array_types)
        mwx__mzmzo = 'def impl(I, ind):\n'
        mwx__mzmzo += '  data = I._data\n'
        mwx__mzmzo += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(f'ensure_contig_if_np(data[{tlm__fyr}][ind])' for
            tlm__fyr in range(qzeg__eohs))))
        eyq__cdmar = {}
        exec(mwx__mzmzo, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, eyq__cdmar)
        oke__mlngr = eyq__cdmar['impl']
        return oke__mlngr


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    jzve__rjfwg, awn__jjiz = sig.args
    if jzve__rjfwg != awn__jjiz:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
