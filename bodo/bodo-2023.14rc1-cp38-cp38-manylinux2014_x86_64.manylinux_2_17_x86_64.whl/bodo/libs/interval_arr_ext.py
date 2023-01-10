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
        rxp__jcgvq = [('left', fe_type.arr_type), ('right', fe_type.arr_type)]
        models.StructModel.__init__(self, dmm, fe_type, rxp__jcgvq)


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
        alcn__dyw, sksxx__rrm = args
        oavpk__lwfx = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        oavpk__lwfx.left = alcn__dyw
        oavpk__lwfx.right = sksxx__rrm
        context.nrt.incref(builder, signature.args[0], alcn__dyw)
        context.nrt.incref(builder, signature.args[1], sksxx__rrm)
        return oavpk__lwfx._getvalue()
    sgf__dflrh = IntervalArrayType(left)
    sepsx__heczh = sgf__dflrh(left, right)
    return sepsx__heczh, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    ctedg__znoe = []
    for vcpvd__bpd in args:
        xleb__msv = equiv_set.get_shape(vcpvd__bpd)
        if xleb__msv is not None:
            ctedg__znoe.append(xleb__msv[0])
    if len(ctedg__znoe) > 1:
        equiv_set.insert_equiv(*ctedg__znoe)
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
    oavpk__lwfx = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, oavpk__lwfx.left)
    waz__fgcj = c.pyapi.from_native_value(typ.arr_type, oavpk__lwfx.left, c
        .env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, oavpk__lwfx.right)
    knzl__fjz = c.pyapi.from_native_value(typ.arr_type, oavpk__lwfx.right,
        c.env_manager)
    mkudf__dljvb = c.context.insert_const_string(c.builder.module, 'pandas')
    ctn__coesv = c.pyapi.import_module_noblock(mkudf__dljvb)
    dkzpf__ufnor = c.pyapi.object_getattr_string(ctn__coesv, 'arrays')
    lnj__csi = c.pyapi.object_getattr_string(dkzpf__ufnor, 'IntervalArray')
    hhylz__zozku = c.pyapi.call_method(lnj__csi, 'from_arrays', (waz__fgcj,
        knzl__fjz))
    c.pyapi.decref(waz__fgcj)
    c.pyapi.decref(knzl__fjz)
    c.pyapi.decref(ctn__coesv)
    c.pyapi.decref(dkzpf__ufnor)
    c.pyapi.decref(lnj__csi)
    c.context.nrt.decref(c.builder, typ, val)
    return hhylz__zozku


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    waz__fgcj = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, waz__fgcj).value
    c.pyapi.decref(waz__fgcj)
    knzl__fjz = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, knzl__fjz).value
    c.pyapi.decref(knzl__fjz)
    oavpk__lwfx = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    oavpk__lwfx.left = left
    oavpk__lwfx.right = right
    ecwtx__cgus = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(oavpk__lwfx._getvalue(), is_error=ecwtx__cgus)


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
