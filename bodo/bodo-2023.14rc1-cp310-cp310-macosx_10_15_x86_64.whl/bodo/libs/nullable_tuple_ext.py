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
        vcpo__bkoy = [('data', fe_type.tuple_typ), ('null_values', fe_type.
            null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, vcpo__bkoy)


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
        opls__lro = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        opls__lro.data = data_tuple
        opls__lro.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return opls__lro._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    kmki__kyxnu = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.tuple_typ, kmki__kyxnu.data)
    c.context.nrt.incref(c.builder, typ.null_typ, kmki__kyxnu.null_values)
    ccq__egepw = c.pyapi.from_native_value(typ.tuple_typ, kmki__kyxnu.data,
        c.env_manager)
    mpx__sjs = c.pyapi.from_native_value(typ.null_typ, kmki__kyxnu.
        null_values, c.env_manager)
    erp__lnlna = c.context.get_constant(types.int64, len(typ.tuple_typ))
    tpean__zbq = c.pyapi.list_new(erp__lnlna)
    with cgutils.for_range(c.builder, erp__lnlna) as sdy__medzl:
        i = sdy__medzl.index
        ziy__boikx = c.pyapi.long_from_longlong(i)
        ukcs__xzv = c.pyapi.object_getitem(mpx__sjs, ziy__boikx)
        kvdha__wmyfq = c.pyapi.to_native_value(types.bool_, ukcs__xzv).value
        with c.builder.if_else(kvdha__wmyfq) as (mpfrp__qzg, rkcz__mah):
            with mpfrp__qzg:
                c.pyapi.list_setitem(tpean__zbq, i, c.pyapi.make_none())
            with rkcz__mah:
                ezuj__yihqr = c.pyapi.object_getitem(ccq__egepw, ziy__boikx)
                c.pyapi.list_setitem(tpean__zbq, i, ezuj__yihqr)
        c.pyapi.decref(ziy__boikx)
        c.pyapi.decref(ukcs__xzv)
    roi__bvke = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    rlj__zkjze = c.pyapi.call_function_objargs(roi__bvke, (tpean__zbq,))
    c.pyapi.decref(ccq__egepw)
    c.pyapi.decref(mpx__sjs)
    c.pyapi.decref(roi__bvke)
    c.pyapi.decref(tpean__zbq)
    c.context.nrt.decref(c.builder, typ, val)
    return rlj__zkjze


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
    opls__lro = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (opls__lro.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    ycbw__pgn = 'def impl(val1, val2):\n'
    ycbw__pgn += '    data_tup1 = val1._data\n'
    ycbw__pgn += '    null_tup1 = val1._null_values\n'
    ycbw__pgn += '    data_tup2 = val2._data\n'
    ycbw__pgn += '    null_tup2 = val2._null_values\n'
    yft__fwb = val1._tuple_typ
    for i in range(len(yft__fwb)):
        ycbw__pgn += f'    null1_{i} = null_tup1[{i}]\n'
        ycbw__pgn += f'    null2_{i} = null_tup2[{i}]\n'
        ycbw__pgn += f'    data1_{i} = data_tup1[{i}]\n'
        ycbw__pgn += f'    data2_{i} = data_tup2[{i}]\n'
        ycbw__pgn += f'    if null1_{i} != null2_{i}:\n'
        ycbw__pgn += '        return False\n'
        ycbw__pgn += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        ycbw__pgn += f'        return False\n'
    ycbw__pgn += f'    return True\n'
    pmzhc__nwn = {}
    exec(ycbw__pgn, {}, pmzhc__nwn)
    impl = pmzhc__nwn['impl']
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
    ycbw__pgn = 'def impl(nullable_tup):\n'
    ycbw__pgn += '    data_tup = nullable_tup._data\n'
    ycbw__pgn += '    null_tup = nullable_tup._null_values\n'
    ycbw__pgn += '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n'
    ycbw__pgn += '    acc = _PyHASH_XXPRIME_5\n'
    yft__fwb = nullable_tup._tuple_typ
    for i in range(len(yft__fwb)):
        ycbw__pgn += f'    null_val_{i} = null_tup[{i}]\n'
        ycbw__pgn += f'    null_lane_{i} = hash(null_val_{i})\n'
        ycbw__pgn += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        ycbw__pgn += '        return -1\n'
        ycbw__pgn += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        ycbw__pgn += '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n'
        ycbw__pgn += '    acc *= _PyHASH_XXPRIME_1\n'
        ycbw__pgn += f'    if not null_val_{i}:\n'
        ycbw__pgn += f'        lane_{i} = hash(data_tup[{i}])\n'
        ycbw__pgn += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        ycbw__pgn += f'            return -1\n'
        ycbw__pgn += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        ycbw__pgn += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        ycbw__pgn += '        acc *= _PyHASH_XXPRIME_1\n'
    ycbw__pgn += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    ycbw__pgn += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    ycbw__pgn += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    ycbw__pgn += '    return numba.cpython.hashing.process_return(acc)\n'
    pmzhc__nwn = {}
    exec(ycbw__pgn, {'numba': numba, '_PyHASH_XXPRIME_1': _PyHASH_XXPRIME_1,
        '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2, '_PyHASH_XXPRIME_5':
        _PyHASH_XXPRIME_5}, pmzhc__nwn)
    impl = pmzhc__nwn['impl']
    return impl
