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
        lntz__rkl = [('data', fe_type.tuple_typ), ('null_values', fe_type.
            null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, lntz__rkl)


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
        emej__fqaut = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        emej__fqaut.data = data_tuple
        emej__fqaut.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return emej__fqaut._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    trr__kpd = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    c.context.nrt.incref(c.builder, typ.tuple_typ, trr__kpd.data)
    c.context.nrt.incref(c.builder, typ.null_typ, trr__kpd.null_values)
    moelh__ujb = c.pyapi.from_native_value(typ.tuple_typ, trr__kpd.data, c.
        env_manager)
    cpn__hbfy = c.pyapi.from_native_value(typ.null_typ, trr__kpd.
        null_values, c.env_manager)
    mtmpc__slq = c.context.get_constant(types.int64, len(typ.tuple_typ))
    qpyip__cqf = c.pyapi.list_new(mtmpc__slq)
    with cgutils.for_range(c.builder, mtmpc__slq) as czdk__zsxlt:
        i = czdk__zsxlt.index
        kscl__ovid = c.pyapi.long_from_longlong(i)
        jjy__rltta = c.pyapi.object_getitem(cpn__hbfy, kscl__ovid)
        gzyrq__juirb = c.pyapi.to_native_value(types.bool_, jjy__rltta).value
        with c.builder.if_else(gzyrq__juirb) as (isma__laq, dztwo__oyle):
            with isma__laq:
                c.pyapi.list_setitem(qpyip__cqf, i, c.pyapi.make_none())
            with dztwo__oyle:
                cizl__gjf = c.pyapi.object_getitem(moelh__ujb, kscl__ovid)
                c.pyapi.list_setitem(qpyip__cqf, i, cizl__gjf)
        c.pyapi.decref(kscl__ovid)
        c.pyapi.decref(jjy__rltta)
    ollze__dty = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    pfqtr__rnnc = c.pyapi.call_function_objargs(ollze__dty, (qpyip__cqf,))
    c.pyapi.decref(moelh__ujb)
    c.pyapi.decref(cpn__hbfy)
    c.pyapi.decref(ollze__dty)
    c.pyapi.decref(qpyip__cqf)
    c.context.nrt.decref(c.builder, typ, val)
    return pfqtr__rnnc


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
    emej__fqaut = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (emej__fqaut.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    kan__sexw = 'def impl(val1, val2):\n'
    kan__sexw += '    data_tup1 = val1._data\n'
    kan__sexw += '    null_tup1 = val1._null_values\n'
    kan__sexw += '    data_tup2 = val2._data\n'
    kan__sexw += '    null_tup2 = val2._null_values\n'
    arwx__qaxmk = val1._tuple_typ
    for i in range(len(arwx__qaxmk)):
        kan__sexw += f'    null1_{i} = null_tup1[{i}]\n'
        kan__sexw += f'    null2_{i} = null_tup2[{i}]\n'
        kan__sexw += f'    data1_{i} = data_tup1[{i}]\n'
        kan__sexw += f'    data2_{i} = data_tup2[{i}]\n'
        kan__sexw += f'    if null1_{i} != null2_{i}:\n'
        kan__sexw += '        return False\n'
        kan__sexw += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        kan__sexw += f'        return False\n'
    kan__sexw += f'    return True\n'
    kcsyk__kcnqy = {}
    exec(kan__sexw, {}, kcsyk__kcnqy)
    impl = kcsyk__kcnqy['impl']
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
    kan__sexw = 'def impl(nullable_tup):\n'
    kan__sexw += '    data_tup = nullable_tup._data\n'
    kan__sexw += '    null_tup = nullable_tup._null_values\n'
    kan__sexw += '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n'
    kan__sexw += '    acc = _PyHASH_XXPRIME_5\n'
    arwx__qaxmk = nullable_tup._tuple_typ
    for i in range(len(arwx__qaxmk)):
        kan__sexw += f'    null_val_{i} = null_tup[{i}]\n'
        kan__sexw += f'    null_lane_{i} = hash(null_val_{i})\n'
        kan__sexw += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        kan__sexw += '        return -1\n'
        kan__sexw += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        kan__sexw += '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n'
        kan__sexw += '    acc *= _PyHASH_XXPRIME_1\n'
        kan__sexw += f'    if not null_val_{i}:\n'
        kan__sexw += f'        lane_{i} = hash(data_tup[{i}])\n'
        kan__sexw += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        kan__sexw += f'            return -1\n'
        kan__sexw += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        kan__sexw += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        kan__sexw += '        acc *= _PyHASH_XXPRIME_1\n'
    kan__sexw += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    kan__sexw += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    kan__sexw += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    kan__sexw += '    return numba.cpython.hashing.process_return(acc)\n'
    kcsyk__kcnqy = {}
    exec(kan__sexw, {'numba': numba, '_PyHASH_XXPRIME_1': _PyHASH_XXPRIME_1,
        '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2, '_PyHASH_XXPRIME_5':
        _PyHASH_XXPRIME_5}, kcsyk__kcnqy)
    impl = kcsyk__kcnqy['impl']
    return impl
