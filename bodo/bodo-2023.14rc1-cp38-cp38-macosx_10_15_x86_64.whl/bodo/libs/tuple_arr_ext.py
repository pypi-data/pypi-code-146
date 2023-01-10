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
        return types.BaseTuple.from_types(tuple(xozob__bajy.dtype for
            xozob__bajy in self.data))

    def copy(self):
        return TupleArrayType(self.data)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(TupleArrayType)
class TupleArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        lhlp__gxf = [('data', StructArrayType(fe_type.data))]
        models.StructModel.__init__(self, dmm, fe_type, lhlp__gxf)


make_attribute_wrapper(TupleArrayType, 'data', '_data')


@intrinsic
def init_tuple_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, StructArrayType)
    eorfj__wpv = TupleArrayType(data_typ.data)

    def codegen(context, builder, sig, args):
        nwx__twag, = args
        hwvjn__atak = context.make_helper(builder, eorfj__wpv)
        hwvjn__atak.data = nwx__twag
        context.nrt.incref(builder, data_typ, nwx__twag)
        return hwvjn__atak._getvalue()
    return eorfj__wpv(data_typ), codegen


@unbox(TupleArrayType)
def unbox_tuple_array(typ, val, c):
    data_typ = StructArrayType(typ.data)
    bzc__exgjt = unbox_struct_array(data_typ, val, c, is_tuple_array=True)
    nwx__twag = bzc__exgjt.value
    hwvjn__atak = c.context.make_helper(c.builder, typ)
    hwvjn__atak.data = nwx__twag
    urnr__pqnga = bzc__exgjt.is_error
    return NativeValue(hwvjn__atak._getvalue(), is_error=urnr__pqnga)


@box(TupleArrayType)
def box_tuple_arr(typ, val, c):
    data_typ = StructArrayType(typ.data)
    hwvjn__atak = c.context.make_helper(c.builder, typ, val)
    arr = box_struct_arr(data_typ, hwvjn__atak.data, c, is_tuple_array=True)
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
        pqiq__vrqzj = 'def impl(arr, ind):\n'
        ovmsx__qwu = ','.join(f'get_data(arr._data)[{din__dsctf}][ind]' for
            din__dsctf in range(len(arr.data)))
        pqiq__vrqzj += f'  return ({ovmsx__qwu})\n'
        gxox__fjqyh = {}
        exec(pqiq__vrqzj, {'get_data': bodo.libs.struct_arr_ext.get_data},
            gxox__fjqyh)
        uybvp__ffv = gxox__fjqyh['impl']
        return uybvp__ffv
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
        mcn__oqxz = len(arr.data)
        pqiq__vrqzj = 'def impl(arr, ind, val):\n'
        pqiq__vrqzj += '  data = get_data(arr._data)\n'
        pqiq__vrqzj += '  null_bitmap = get_null_bitmap(arr._data)\n'
        pqiq__vrqzj += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for din__dsctf in range(mcn__oqxz):
            pqiq__vrqzj += f'  data[{din__dsctf}][ind] = val[{din__dsctf}]\n'
        gxox__fjqyh = {}
        exec(pqiq__vrqzj, {'get_data': bodo.libs.struct_arr_ext.get_data,
            'get_null_bitmap': bodo.libs.struct_arr_ext.get_null_bitmap,
            'set_bit_to_arr': bodo.libs.int_arr_ext.set_bit_to_arr},
            gxox__fjqyh)
        uybvp__ffv = gxox__fjqyh['impl']
        return uybvp__ffv

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
