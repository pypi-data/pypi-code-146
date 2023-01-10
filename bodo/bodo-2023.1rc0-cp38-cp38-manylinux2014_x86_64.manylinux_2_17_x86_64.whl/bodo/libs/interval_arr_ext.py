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
        yfgwf__bmbz = [('left', fe_type.arr_type), ('right', fe_type.arr_type)]
        models.StructModel.__init__(self, dmm, fe_type, yfgwf__bmbz)


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
        sgc__alsas, hffdb__pgp = args
        fipy__woar = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        fipy__woar.left = sgc__alsas
        fipy__woar.right = hffdb__pgp
        context.nrt.incref(builder, signature.args[0], sgc__alsas)
        context.nrt.incref(builder, signature.args[1], hffdb__pgp)
        return fipy__woar._getvalue()
    klqzk__gwps = IntervalArrayType(left)
    uxx__jknij = klqzk__gwps(left, right)
    return uxx__jknij, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    ngdvs__rhjc = []
    for ceoa__eueb in args:
        ibn__ynr = equiv_set.get_shape(ceoa__eueb)
        if ibn__ynr is not None:
            ngdvs__rhjc.append(ibn__ynr[0])
    if len(ngdvs__rhjc) > 1:
        equiv_set.insert_equiv(*ngdvs__rhjc)
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
    fipy__woar = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, fipy__woar.left)
    gla__gtsk = c.pyapi.from_native_value(typ.arr_type, fipy__woar.left, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, fipy__woar.right)
    goku__nvib = c.pyapi.from_native_value(typ.arr_type, fipy__woar.right,
        c.env_manager)
    hixo__xnq = c.context.insert_const_string(c.builder.module, 'pandas')
    otgi__ien = c.pyapi.import_module_noblock(hixo__xnq)
    smkww__zadgc = c.pyapi.object_getattr_string(otgi__ien, 'arrays')
    zvg__bdv = c.pyapi.object_getattr_string(smkww__zadgc, 'IntervalArray')
    tte__bhe = c.pyapi.call_method(zvg__bdv, 'from_arrays', (gla__gtsk,
        goku__nvib))
    c.pyapi.decref(gla__gtsk)
    c.pyapi.decref(goku__nvib)
    c.pyapi.decref(otgi__ien)
    c.pyapi.decref(smkww__zadgc)
    c.pyapi.decref(zvg__bdv)
    c.context.nrt.decref(c.builder, typ, val)
    return tte__bhe


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    gla__gtsk = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, gla__gtsk).value
    c.pyapi.decref(gla__gtsk)
    goku__nvib = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, goku__nvib).value
    c.pyapi.decref(goku__nvib)
    fipy__woar = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    fipy__woar.left = left
    fipy__woar.right = right
    rookz__ekec = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(fipy__woar._getvalue(), is_error=rookz__ekec)


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
