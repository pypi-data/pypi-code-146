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
        ockbc__rwuq = [('left', fe_type.arr_type), ('right', fe_type.arr_type)]
        models.StructModel.__init__(self, dmm, fe_type, ockbc__rwuq)


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
        gevhp__vzehk, cyeyw__izzh = args
        myoep__bdj = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        myoep__bdj.left = gevhp__vzehk
        myoep__bdj.right = cyeyw__izzh
        context.nrt.incref(builder, signature.args[0], gevhp__vzehk)
        context.nrt.incref(builder, signature.args[1], cyeyw__izzh)
        return myoep__bdj._getvalue()
    grpy__uzjbp = IntervalArrayType(left)
    tgzf__jqr = grpy__uzjbp(left, right)
    return tgzf__jqr, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    xzph__ojw = []
    for ooc__yuoi in args:
        ejx__gihi = equiv_set.get_shape(ooc__yuoi)
        if ejx__gihi is not None:
            xzph__ojw.append(ejx__gihi[0])
    if len(xzph__ojw) > 1:
        equiv_set.insert_equiv(*xzph__ojw)
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
    myoep__bdj = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, myoep__bdj.left)
    xyac__oqra = c.pyapi.from_native_value(typ.arr_type, myoep__bdj.left, c
        .env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, myoep__bdj.right)
    cgg__kps = c.pyapi.from_native_value(typ.arr_type, myoep__bdj.right, c.
        env_manager)
    ggjpf__foz = c.context.insert_const_string(c.builder.module, 'pandas')
    nnu__pmf = c.pyapi.import_module_noblock(ggjpf__foz)
    gfq__iqkqs = c.pyapi.object_getattr_string(nnu__pmf, 'arrays')
    ztoe__rwopz = c.pyapi.object_getattr_string(gfq__iqkqs, 'IntervalArray')
    kzgh__haz = c.pyapi.call_method(ztoe__rwopz, 'from_arrays', (xyac__oqra,
        cgg__kps))
    c.pyapi.decref(xyac__oqra)
    c.pyapi.decref(cgg__kps)
    c.pyapi.decref(nnu__pmf)
    c.pyapi.decref(gfq__iqkqs)
    c.pyapi.decref(ztoe__rwopz)
    c.context.nrt.decref(c.builder, typ, val)
    return kzgh__haz


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    xyac__oqra = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, xyac__oqra).value
    c.pyapi.decref(xyac__oqra)
    cgg__kps = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, cgg__kps).value
    c.pyapi.decref(cgg__kps)
    myoep__bdj = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    myoep__bdj.left = left
    myoep__bdj.right = right
    kmgg__vhhh = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(myoep__bdj._getvalue(), is_error=kmgg__vhhh)


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
