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
        cowc__qjere = [('data', fe_type.tuple_typ), ('null_values', fe_type
            .null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, cowc__qjere)


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
        zup__bvr = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        zup__bvr.data = data_tuple
        zup__bvr.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return zup__bvr._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    tsn__xce = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    c.context.nrt.incref(c.builder, typ.tuple_typ, tsn__xce.data)
    c.context.nrt.incref(c.builder, typ.null_typ, tsn__xce.null_values)
    iazzq__kkzec = c.pyapi.from_native_value(typ.tuple_typ, tsn__xce.data,
        c.env_manager)
    oxue__jtwxy = c.pyapi.from_native_value(typ.null_typ, tsn__xce.
        null_values, c.env_manager)
    ukz__mdtj = c.context.get_constant(types.int64, len(typ.tuple_typ))
    hufot__lqfk = c.pyapi.list_new(ukz__mdtj)
    with cgutils.for_range(c.builder, ukz__mdtj) as yfjq__oaglm:
        i = yfjq__oaglm.index
        nsu__pgsy = c.pyapi.long_from_longlong(i)
        vpj__tcr = c.pyapi.object_getitem(oxue__jtwxy, nsu__pgsy)
        bxf__quhl = c.pyapi.to_native_value(types.bool_, vpj__tcr).value
        with c.builder.if_else(bxf__quhl) as (jcphr__mxeu, gbms__mbvpv):
            with jcphr__mxeu:
                c.pyapi.list_setitem(hufot__lqfk, i, c.pyapi.make_none())
            with gbms__mbvpv:
                vhbys__uvcf = c.pyapi.object_getitem(iazzq__kkzec, nsu__pgsy)
                c.pyapi.list_setitem(hufot__lqfk, i, vhbys__uvcf)
        c.pyapi.decref(nsu__pgsy)
        c.pyapi.decref(vpj__tcr)
    sejii__cpis = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    aok__urm = c.pyapi.call_function_objargs(sejii__cpis, (hufot__lqfk,))
    c.pyapi.decref(iazzq__kkzec)
    c.pyapi.decref(oxue__jtwxy)
    c.pyapi.decref(sejii__cpis)
    c.pyapi.decref(hufot__lqfk)
    c.context.nrt.decref(c.builder, typ, val)
    return aok__urm


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
    zup__bvr = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (zup__bvr.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    zpel__atcz = 'def impl(val1, val2):\n'
    zpel__atcz += '    data_tup1 = val1._data\n'
    zpel__atcz += '    null_tup1 = val1._null_values\n'
    zpel__atcz += '    data_tup2 = val2._data\n'
    zpel__atcz += '    null_tup2 = val2._null_values\n'
    unt__ixjj = val1._tuple_typ
    for i in range(len(unt__ixjj)):
        zpel__atcz += f'    null1_{i} = null_tup1[{i}]\n'
        zpel__atcz += f'    null2_{i} = null_tup2[{i}]\n'
        zpel__atcz += f'    data1_{i} = data_tup1[{i}]\n'
        zpel__atcz += f'    data2_{i} = data_tup2[{i}]\n'
        zpel__atcz += f'    if null1_{i} != null2_{i}:\n'
        zpel__atcz += '        return False\n'
        zpel__atcz += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        zpel__atcz += f'        return False\n'
    zpel__atcz += f'    return True\n'
    jirn__rdpi = {}
    exec(zpel__atcz, {}, jirn__rdpi)
    impl = jirn__rdpi['impl']
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
    zpel__atcz = 'def impl(nullable_tup):\n'
    zpel__atcz += '    data_tup = nullable_tup._data\n'
    zpel__atcz += '    null_tup = nullable_tup._null_values\n'
    zpel__atcz += '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n'
    zpel__atcz += '    acc = _PyHASH_XXPRIME_5\n'
    unt__ixjj = nullable_tup._tuple_typ
    for i in range(len(unt__ixjj)):
        zpel__atcz += f'    null_val_{i} = null_tup[{i}]\n'
        zpel__atcz += f'    null_lane_{i} = hash(null_val_{i})\n'
        zpel__atcz += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        zpel__atcz += '        return -1\n'
        zpel__atcz += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        zpel__atcz += '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n'
        zpel__atcz += '    acc *= _PyHASH_XXPRIME_1\n'
        zpel__atcz += f'    if not null_val_{i}:\n'
        zpel__atcz += f'        lane_{i} = hash(data_tup[{i}])\n'
        zpel__atcz += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        zpel__atcz += f'            return -1\n'
        zpel__atcz += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        zpel__atcz += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        zpel__atcz += '        acc *= _PyHASH_XXPRIME_1\n'
    zpel__atcz += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    zpel__atcz += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    zpel__atcz += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    zpel__atcz += '    return numba.cpython.hashing.process_return(acc)\n'
    jirn__rdpi = {}
    exec(zpel__atcz, {'numba': numba, '_PyHASH_XXPRIME_1':
        _PyHASH_XXPRIME_1, '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2,
        '_PyHASH_XXPRIME_5': _PyHASH_XXPRIME_5}, jirn__rdpi)
    impl = jirn__rdpi['impl']
    return impl
