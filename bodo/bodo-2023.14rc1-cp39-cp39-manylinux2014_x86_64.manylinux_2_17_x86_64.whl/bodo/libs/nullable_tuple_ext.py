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
        avx__wrhq = [('data', fe_type.tuple_typ), ('null_values', fe_type.
            null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, avx__wrhq)


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
        pltqa__raw = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        pltqa__raw.data = data_tuple
        pltqa__raw.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return pltqa__raw._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    uyc__fsok = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.tuple_typ, uyc__fsok.data)
    c.context.nrt.incref(c.builder, typ.null_typ, uyc__fsok.null_values)
    mhowo__wiz = c.pyapi.from_native_value(typ.tuple_typ, uyc__fsok.data, c
        .env_manager)
    fxfej__vhquo = c.pyapi.from_native_value(typ.null_typ, uyc__fsok.
        null_values, c.env_manager)
    dttb__xyj = c.context.get_constant(types.int64, len(typ.tuple_typ))
    qjqbq__xyqd = c.pyapi.list_new(dttb__xyj)
    with cgutils.for_range(c.builder, dttb__xyj) as gjvbz__ybg:
        i = gjvbz__ybg.index
        oqvly__oah = c.pyapi.long_from_longlong(i)
        miao__ewpx = c.pyapi.object_getitem(fxfej__vhquo, oqvly__oah)
        mhhl__ypy = c.pyapi.to_native_value(types.bool_, miao__ewpx).value
        with c.builder.if_else(mhhl__ypy) as (fksh__hzv, eea__ffem):
            with fksh__hzv:
                c.pyapi.list_setitem(qjqbq__xyqd, i, c.pyapi.make_none())
            with eea__ffem:
                btpz__yin = c.pyapi.object_getitem(mhowo__wiz, oqvly__oah)
                c.pyapi.list_setitem(qjqbq__xyqd, i, btpz__yin)
        c.pyapi.decref(oqvly__oah)
        c.pyapi.decref(miao__ewpx)
    lcqoi__hca = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    hltrf__apkf = c.pyapi.call_function_objargs(lcqoi__hca, (qjqbq__xyqd,))
    c.pyapi.decref(mhowo__wiz)
    c.pyapi.decref(fxfej__vhquo)
    c.pyapi.decref(lcqoi__hca)
    c.pyapi.decref(qjqbq__xyqd)
    c.context.nrt.decref(c.builder, typ, val)
    return hltrf__apkf


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
    pltqa__raw = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (pltqa__raw.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    jrt__mbt = 'def impl(val1, val2):\n'
    jrt__mbt += '    data_tup1 = val1._data\n'
    jrt__mbt += '    null_tup1 = val1._null_values\n'
    jrt__mbt += '    data_tup2 = val2._data\n'
    jrt__mbt += '    null_tup2 = val2._null_values\n'
    sfmm__rmg = val1._tuple_typ
    for i in range(len(sfmm__rmg)):
        jrt__mbt += f'    null1_{i} = null_tup1[{i}]\n'
        jrt__mbt += f'    null2_{i} = null_tup2[{i}]\n'
        jrt__mbt += f'    data1_{i} = data_tup1[{i}]\n'
        jrt__mbt += f'    data2_{i} = data_tup2[{i}]\n'
        jrt__mbt += f'    if null1_{i} != null2_{i}:\n'
        jrt__mbt += '        return False\n'
        jrt__mbt += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        jrt__mbt += f'        return False\n'
    jrt__mbt += f'    return True\n'
    hikfz__iowl = {}
    exec(jrt__mbt, {}, hikfz__iowl)
    impl = hikfz__iowl['impl']
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
    jrt__mbt = 'def impl(nullable_tup):\n'
    jrt__mbt += '    data_tup = nullable_tup._data\n'
    jrt__mbt += '    null_tup = nullable_tup._null_values\n'
    jrt__mbt += '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n'
    jrt__mbt += '    acc = _PyHASH_XXPRIME_5\n'
    sfmm__rmg = nullable_tup._tuple_typ
    for i in range(len(sfmm__rmg)):
        jrt__mbt += f'    null_val_{i} = null_tup[{i}]\n'
        jrt__mbt += f'    null_lane_{i} = hash(null_val_{i})\n'
        jrt__mbt += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        jrt__mbt += '        return -1\n'
        jrt__mbt += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        jrt__mbt += '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n'
        jrt__mbt += '    acc *= _PyHASH_XXPRIME_1\n'
        jrt__mbt += f'    if not null_val_{i}:\n'
        jrt__mbt += f'        lane_{i} = hash(data_tup[{i}])\n'
        jrt__mbt += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        jrt__mbt += f'            return -1\n'
        jrt__mbt += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        jrt__mbt += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        jrt__mbt += '        acc *= _PyHASH_XXPRIME_1\n'
    jrt__mbt += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    jrt__mbt += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    jrt__mbt += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    jrt__mbt += '    return numba.cpython.hashing.process_return(acc)\n'
    hikfz__iowl = {}
    exec(jrt__mbt, {'numba': numba, '_PyHASH_XXPRIME_1': _PyHASH_XXPRIME_1,
        '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2, '_PyHASH_XXPRIME_5':
        _PyHASH_XXPRIME_5}, hikfz__iowl)
    impl = hikfz__iowl['impl']
    return impl
