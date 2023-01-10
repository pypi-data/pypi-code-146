"""
Wrapper class for Tuples that supports tracking null entries.
This is primarily used for maintaining null information for
Series values used in df.apply
"""
import operator
import numba
from numba.core import cgutils, types
from numba.extending import box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_method, register_model


class NullableTupleType(types.IterableType):

    def __init__(self, tuple_typ, null_typ):
        self._tuple_typ = tuple_typ
        self._null_typ = null_typ
        super(NullableTupleType, self).__init__(name=
            f'NullableTupleType({tuple_typ}, {null_typ})')

    @property
    def tuple_typ(self):
        return self._tuple_typ

    @property
    def null_typ(self):
        return self._null_typ

    def __getitem__(self, i):
        return self._tuple_typ[i]

    @property
    def key(self):
        return self._tuple_typ

    @property
    def dtype(self):
        return self.tuple_typ.dtype

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def iterator_type(self):
        return self.tuple_typ.iterator_type

    def __len__(self):
        return len(self.tuple_typ)


@register_model(NullableTupleType)
class NullableTupleModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bssh__yln = [('data', fe_type.tuple_typ), ('null_values', fe_type.
            null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, bssh__yln)


make_attribute_wrapper(NullableTupleType, 'data', '_data')
make_attribute_wrapper(NullableTupleType, 'null_values', '_null_values')


@intrinsic
def build_nullable_tuple(typingctx, data_tuple, null_values):
    assert isinstance(data_tuple, types.BaseTuple
        ), "build_nullable_tuple 'data_tuple' argument must be a tuple"
    assert isinstance(null_values, types.BaseTuple
        ), "build_nullable_tuple 'null_values' argument must be a tuple"
    data_tuple = types.unliteral(data_tuple)
    null_values = types.unliteral(null_values)

    def codegen(context, builder, signature, args):
        data_tuple, null_values = args
        lxtlz__gzhvi = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        lxtlz__gzhvi.data = data_tuple
        lxtlz__gzhvi.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return lxtlz__gzhvi._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    rqwox__pds = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.tuple_typ, rqwox__pds.data)
    c.context.nrt.incref(c.builder, typ.null_typ, rqwox__pds.null_values)
    kxzau__jlb = c.pyapi.from_native_value(typ.tuple_typ, rqwox__pds.data,
        c.env_manager)
    cwqd__vvoy = c.pyapi.from_native_value(typ.null_typ, rqwox__pds.
        null_values, c.env_manager)
    urga__ypgt = c.context.get_constant(types.int64, len(typ.tuple_typ))
    xcs__hpi = c.pyapi.list_new(urga__ypgt)
    with cgutils.for_range(c.builder, urga__ypgt) as ogax__hlxm:
        i = ogax__hlxm.index
        mjeak__mbuz = c.pyapi.long_from_longlong(i)
        yyx__rywnc = c.pyapi.object_getitem(cwqd__vvoy, mjeak__mbuz)
        mcrq__prr = c.pyapi.to_native_value(types.bool_, yyx__rywnc).value
        with c.builder.if_else(mcrq__prr) as (uodmo__miap, lwzcu__eum):
            with uodmo__miap:
                c.pyapi.list_setitem(xcs__hpi, i, c.pyapi.make_none())
            with lwzcu__eum:
                wzo__mnyau = c.pyapi.object_getitem(kxzau__jlb, mjeak__mbuz)
                c.pyapi.list_setitem(xcs__hpi, i, wzo__mnyau)
        c.pyapi.decref(mjeak__mbuz)
        c.pyapi.decref(yyx__rywnc)
    ime__xrr = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    sxmt__hvbw = c.pyapi.call_function_objargs(ime__xrr, (xcs__hpi,))
    c.pyapi.decref(kxzau__jlb)
    c.pyapi.decref(cwqd__vvoy)
    c.pyapi.decref(ime__xrr)
    c.pyapi.decref(xcs__hpi)
    c.context.nrt.decref(c.builder, typ, val)
    return sxmt__hvbw


@overload(operator.getitem)
def overload_getitem(A, idx):
    if not isinstance(A, NullableTupleType):
        return
    return lambda A, idx: A._data[idx]


@overload(len)
def overload_len(A):
    if not isinstance(A, NullableTupleType):
        return
    return lambda A: len(A._data)


@lower_builtin('getiter', NullableTupleType)
def nullable_tuple_getiter(context, builder, sig, args):
    lxtlz__gzhvi = cgutils.create_struct_proxy(sig.args[0])(context,
        builder, value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (lxtlz__gzhvi.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    dggpl__wvmco = 'def impl(val1, val2):\n'
    dggpl__wvmco += '    data_tup1 = val1._data\n'
    dggpl__wvmco += '    null_tup1 = val1._null_values\n'
    dggpl__wvmco += '    data_tup2 = val2._data\n'
    dggpl__wvmco += '    null_tup2 = val2._null_values\n'
    xjvp__vtg = val1._tuple_typ
    for i in range(len(xjvp__vtg)):
        dggpl__wvmco += f'    null1_{i} = null_tup1[{i}]\n'
        dggpl__wvmco += f'    null2_{i} = null_tup2[{i}]\n'
        dggpl__wvmco += f'    data1_{i} = data_tup1[{i}]\n'
        dggpl__wvmco += f'    data2_{i} = data_tup2[{i}]\n'
        dggpl__wvmco += f'    if null1_{i} != null2_{i}:\n'
        dggpl__wvmco += '        return False\n'
        dggpl__wvmco += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        dggpl__wvmco += f'        return False\n'
    dggpl__wvmco += f'    return True\n'
    xabw__hiqy = {}
    exec(dggpl__wvmco, {}, xabw__hiqy)
    impl = xabw__hiqy['impl']
    return impl


@overload_method(NullableTupleType, '__hash__')
def nullable_tuple_hash(val):

    def impl(val):
        return _nullable_tuple_hash(val)
    return impl


_PyHASH_XXPRIME_1 = numba.cpython.hashing._PyHASH_XXPRIME_1
_PyHASH_XXPRIME_2 = numba.cpython.hashing._PyHASH_XXPRIME_1
_PyHASH_XXPRIME_5 = numba.cpython.hashing._PyHASH_XXPRIME_1


@numba.generated_jit(nopython=True)
def _nullable_tuple_hash(nullable_tup):
    dggpl__wvmco = 'def impl(nullable_tup):\n'
    dggpl__wvmco += '    data_tup = nullable_tup._data\n'
    dggpl__wvmco += '    null_tup = nullable_tup._null_values\n'
    dggpl__wvmco += (
        '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n')
    dggpl__wvmco += '    acc = _PyHASH_XXPRIME_5\n'
    xjvp__vtg = nullable_tup._tuple_typ
    for i in range(len(xjvp__vtg)):
        dggpl__wvmco += f'    null_val_{i} = null_tup[{i}]\n'
        dggpl__wvmco += f'    null_lane_{i} = hash(null_val_{i})\n'
        dggpl__wvmco += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        dggpl__wvmco += '        return -1\n'
        dggpl__wvmco += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        dggpl__wvmco += (
            '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        dggpl__wvmco += '    acc *= _PyHASH_XXPRIME_1\n'
        dggpl__wvmco += f'    if not null_val_{i}:\n'
        dggpl__wvmco += f'        lane_{i} = hash(data_tup[{i}])\n'
        dggpl__wvmco += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        dggpl__wvmco += f'            return -1\n'
        dggpl__wvmco += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        dggpl__wvmco += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        dggpl__wvmco += '        acc *= _PyHASH_XXPRIME_1\n'
    dggpl__wvmco += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    dggpl__wvmco += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    dggpl__wvmco += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    dggpl__wvmco += '    return numba.cpython.hashing.process_return(acc)\n'
    xabw__hiqy = {}
    exec(dggpl__wvmco, {'numba': numba, '_PyHASH_XXPRIME_1':
        _PyHASH_XXPRIME_1, '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2,
        '_PyHASH_XXPRIME_5': _PyHASH_XXPRIME_5}, xabw__hiqy)
    impl = xabw__hiqy['impl']
    return impl
