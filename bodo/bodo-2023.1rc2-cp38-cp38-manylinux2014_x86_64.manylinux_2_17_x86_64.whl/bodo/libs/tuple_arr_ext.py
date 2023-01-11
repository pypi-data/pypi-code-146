"""Array of tuple values, implemented by reusing array of structs implementation.
"""
import operator
import numba
import numpy as np
from numba.core import types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs.struct_arr_ext import StructArrayType, box_struct_arr, unbox_struct_array


class TupleArrayType(types.ArrayCompatible):

    def __init__(self, data):
        self.data = data
        super(TupleArrayType, self).__init__(name='TupleArrayType({})'.
            format(data))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.BaseTuple.from_types(tuple(oeou__hadl.dtype for
            oeou__hadl in self.data))

    def copy(self):
        return TupleArrayType(self.data)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(TupleArrayType)
class TupleArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wulv__agg = [('data', StructArrayType(fe_type.data))]
        models.StructModel.__init__(self, dmm, fe_type, wulv__agg)


make_attribute_wrapper(TupleArrayType, 'data', '_data')


@intrinsic
def init_tuple_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, StructArrayType)
    pro__pvg = TupleArrayType(data_typ.data)

    def codegen(context, builder, sig, args):
        jglu__boae, = args
        jcypi__jkrb = context.make_helper(builder, pro__pvg)
        jcypi__jkrb.data = jglu__boae
        context.nrt.incref(builder, data_typ, jglu__boae)
        return jcypi__jkrb._getvalue()
    return pro__pvg(data_typ), codegen


@unbox(TupleArrayType)
def unbox_tuple_array(typ, val, c):
    data_typ = StructArrayType(typ.data)
    cyd__jwsy = unbox_struct_array(data_typ, val, c, is_tuple_array=True)
    jglu__boae = cyd__jwsy.value
    jcypi__jkrb = c.context.make_helper(c.builder, typ)
    jcypi__jkrb.data = jglu__boae
    lwq__ydass = cyd__jwsy.is_error
    return NativeValue(jcypi__jkrb._getvalue(), is_error=lwq__ydass)


@box(TupleArrayType)
def box_tuple_arr(typ, val, c):
    data_typ = StructArrayType(typ.data)
    jcypi__jkrb = c.context.make_helper(c.builder, typ, val)
    arr = box_struct_arr(data_typ, jcypi__jkrb.data, c, is_tuple_array=True)
    return arr


@numba.njit
def pre_alloc_tuple_array(n, nested_counts, dtypes):
    return init_tuple_arr(bodo.libs.struct_arr_ext.pre_alloc_struct_array(n,
        nested_counts, dtypes, None))


def pre_alloc_tuple_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_tuple_arr_ext_pre_alloc_tuple_array
    ) = pre_alloc_tuple_array_equiv


@overload(operator.getitem, no_unliteral=True)
def tuple_arr_getitem(arr, ind):
    if not isinstance(arr, TupleArrayType):
        return
    if isinstance(ind, types.Integer):
        fqhd__ntca = 'def impl(arr, ind):\n'
        ocyxj__rnwap = ','.join(f'get_data(arr._data)[{uofeo__cww}][ind]' for
            uofeo__cww in range(len(arr.data)))
        fqhd__ntca += f'  return ({ocyxj__rnwap})\n'
        ltcj__rbsm = {}
        exec(fqhd__ntca, {'get_data': bodo.libs.struct_arr_ext.get_data},
            ltcj__rbsm)
        cge__ehm = ltcj__rbsm['impl']
        return cge__ehm
    if ind != bodo.boolean_array:

        def impl_arr(arr, ind):
            return init_tuple_arr(arr._data[ind])
        return impl_arr


@overload(operator.setitem, no_unliteral=True)
def tuple_arr_setitem(arr, ind, val):
    if not isinstance(arr, TupleArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        gpskm__dzfx = len(arr.data)
        fqhd__ntca = 'def impl(arr, ind, val):\n'
        fqhd__ntca += '  data = get_data(arr._data)\n'
        fqhd__ntca += '  null_bitmap = get_null_bitmap(arr._data)\n'
        fqhd__ntca += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for uofeo__cww in range(gpskm__dzfx):
            fqhd__ntca += f'  data[{uofeo__cww}][ind] = val[{uofeo__cww}]\n'
        ltcj__rbsm = {}
        exec(fqhd__ntca, {'get_data': bodo.libs.struct_arr_ext.get_data,
            'get_null_bitmap': bodo.libs.struct_arr_ext.get_null_bitmap,
            'set_bit_to_arr': bodo.libs.int_arr_ext.set_bit_to_arr}, ltcj__rbsm
            )
        cge__ehm = ltcj__rbsm['impl']
        return cge__ehm

    def impl_arr(arr, ind, val):
        val = bodo.utils.conversion.coerce_to_array(val, use_nullable_array
            =True)
        arr._data[ind] = val._data
    return impl_arr


@overload(len, no_unliteral=True)
def overload_tuple_arr_len(A):
    if isinstance(A, TupleArrayType):
        return lambda A: len(A._data)


@overload_attribute(TupleArrayType, 'shape')
def overload_tuple_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(TupleArrayType, 'dtype')
def overload_tuple_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(TupleArrayType, 'ndim')
def overload_tuple_arr_ndim(A):
    return lambda A: 1


@overload_attribute(TupleArrayType, 'nbytes')
def overload_tuple_arr_nbytes(A):
    return lambda A: A._data.nbytes


@overload_method(TupleArrayType, 'copy', no_unliteral=True)
def overload_tuple_arr_copy(A):

    def copy_impl(A):
        return init_tuple_arr(A._data.copy())
    return copy_impl
