"""
Array of intervals corresponding to IntervalArray of Pandas.
Used for IntervalIndex, which is necessary for Series.value_counts() with 'bins'
argument.
"""
import numba
import pandas as pd
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo


class IntervalType(types.Type):

    def __init__(self):
        super(IntervalType, self).__init__('IntervalType()')


class IntervalArrayType(types.ArrayCompatible):

    def __init__(self, arr_type):
        self.arr_type = arr_type
        self.dtype = IntervalType()
        super(IntervalArrayType, self).__init__(name=
            f'IntervalArrayType({arr_type})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return IntervalArrayType(self.arr_type)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(IntervalArrayType)
class IntervalArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        nqq__ust = [('left', fe_type.arr_type), ('right', fe_type.arr_type)]
        models.StructModel.__init__(self, dmm, fe_type, nqq__ust)


make_attribute_wrapper(IntervalArrayType, 'left', '_left')
make_attribute_wrapper(IntervalArrayType, 'right', '_right')


@typeof_impl.register(pd.arrays.IntervalArray)
def typeof_interval_array(val, c):
    arr_type = bodo.typeof(val._left)
    return IntervalArrayType(arr_type)


@intrinsic
def init_interval_array(typingctx, left, right=None):
    assert left == right, 'Interval left/right array types should be the same'

    def codegen(context, builder, signature, args):
        gwrwe__qyhz, vhhp__hwh = args
        nlcir__fle = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        nlcir__fle.left = gwrwe__qyhz
        nlcir__fle.right = vhhp__hwh
        context.nrt.incref(builder, signature.args[0], gwrwe__qyhz)
        context.nrt.incref(builder, signature.args[1], vhhp__hwh)
        return nlcir__fle._getvalue()
    eyaoi__mim = IntervalArrayType(left)
    lye__qics = eyaoi__mim(left, right)
    return lye__qics, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    xcx__uae = []
    for ndk__ihig in args:
        fpa__owe = equiv_set.get_shape(ndk__ihig)
        if fpa__owe is not None:
            xcx__uae.append(fpa__owe[0])
    if len(xcx__uae) > 1:
        equiv_set.insert_equiv(*xcx__uae)
    left = args[0]
    if equiv_set.has_shape(left):
        return ArrayAnalysis.AnalyzeResult(shape=left, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_libs_interval_arr_ext_init_interval_array
    ) = init_interval_array_equiv


def alias_ext_init_interval_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_interval_array',
    'bodo.libs.int_arr_ext'] = alias_ext_init_interval_array


@box(IntervalArrayType)
def box_interval_arr(typ, val, c):
    nlcir__fle = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, nlcir__fle.left)
    yedvo__nqvpo = c.pyapi.from_native_value(typ.arr_type, nlcir__fle.left,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, nlcir__fle.right)
    ked__womwj = c.pyapi.from_native_value(typ.arr_type, nlcir__fle.right,
        c.env_manager)
    antc__pid = c.context.insert_const_string(c.builder.module, 'pandas')
    wjp__ajk = c.pyapi.import_module_noblock(antc__pid)
    sbri__uqsv = c.pyapi.object_getattr_string(wjp__ajk, 'arrays')
    lziv__hcoh = c.pyapi.object_getattr_string(sbri__uqsv, 'IntervalArray')
    avlj__qcl = c.pyapi.call_method(lziv__hcoh, 'from_arrays', (
        yedvo__nqvpo, ked__womwj))
    c.pyapi.decref(yedvo__nqvpo)
    c.pyapi.decref(ked__womwj)
    c.pyapi.decref(wjp__ajk)
    c.pyapi.decref(sbri__uqsv)
    c.pyapi.decref(lziv__hcoh)
    c.context.nrt.decref(c.builder, typ, val)
    return avlj__qcl


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    yedvo__nqvpo = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, yedvo__nqvpo).value
    c.pyapi.decref(yedvo__nqvpo)
    ked__womwj = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, ked__womwj).value
    c.pyapi.decref(ked__womwj)
    nlcir__fle = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    nlcir__fle.left = left
    nlcir__fle.right = right
    iopb__zqtnj = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(nlcir__fle._getvalue(), is_error=iopb__zqtnj)


@overload(len, no_unliteral=True)
def overload_interval_arr_len(A):
    if isinstance(A, IntervalArrayType):
        return lambda A: len(A._left)


@overload_attribute(IntervalArrayType, 'shape')
def overload_interval_arr_shape(A):
    return lambda A: (len(A._left),)


@overload_attribute(IntervalArrayType, 'ndim')
def overload_interval_arr_ndim(A):
    return lambda A: 1


@overload_attribute(IntervalArrayType, 'nbytes')
def overload_interval_arr_nbytes(A):
    return lambda A: A._left.nbytes + A._right.nbytes


@overload_method(IntervalArrayType, 'copy', no_unliteral=True)
def overload_interval_arr_copy(A):
    return lambda A: bodo.libs.interval_arr_ext.init_interval_array(A._left
        .copy(), A._right.copy())
