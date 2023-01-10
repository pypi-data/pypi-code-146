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
        fmofg__btc = [('left', fe_type.arr_type), ('right', fe_type.arr_type)]
        models.StructModel.__init__(self, dmm, fe_type, fmofg__btc)


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
        yryey__dfu, eos__bwl = args
        mty__nekey = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        mty__nekey.left = yryey__dfu
        mty__nekey.right = eos__bwl
        context.nrt.incref(builder, signature.args[0], yryey__dfu)
        context.nrt.incref(builder, signature.args[1], eos__bwl)
        return mty__nekey._getvalue()
    juf__img = IntervalArrayType(left)
    khjb__jfinj = juf__img(left, right)
    return khjb__jfinj, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    ukbke__bqqj = []
    for xks__wrf in args:
        cyth__zghl = equiv_set.get_shape(xks__wrf)
        if cyth__zghl is not None:
            ukbke__bqqj.append(cyth__zghl[0])
    if len(ukbke__bqqj) > 1:
        equiv_set.insert_equiv(*ukbke__bqqj)
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
    mty__nekey = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, mty__nekey.left)
    itldt__olmiv = c.pyapi.from_native_value(typ.arr_type, mty__nekey.left,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, mty__nekey.right)
    wlgq__lcq = c.pyapi.from_native_value(typ.arr_type, mty__nekey.right, c
        .env_manager)
    qtl__zlefp = c.context.insert_const_string(c.builder.module, 'pandas')
    uhug__vdypa = c.pyapi.import_module_noblock(qtl__zlefp)
    aji__nbf = c.pyapi.object_getattr_string(uhug__vdypa, 'arrays')
    msvxw__izzjv = c.pyapi.object_getattr_string(aji__nbf, 'IntervalArray')
    gysej__girg = c.pyapi.call_method(msvxw__izzjv, 'from_arrays', (
        itldt__olmiv, wlgq__lcq))
    c.pyapi.decref(itldt__olmiv)
    c.pyapi.decref(wlgq__lcq)
    c.pyapi.decref(uhug__vdypa)
    c.pyapi.decref(aji__nbf)
    c.pyapi.decref(msvxw__izzjv)
    c.context.nrt.decref(c.builder, typ, val)
    return gysej__girg


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    itldt__olmiv = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, itldt__olmiv).value
    c.pyapi.decref(itldt__olmiv)
    wlgq__lcq = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, wlgq__lcq).value
    c.pyapi.decref(wlgq__lcq)
    mty__nekey = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    mty__nekey.left = left
    mty__nekey.right = right
    spk__houc = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(mty__nekey._getvalue(), is_error=spk__houc)


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
