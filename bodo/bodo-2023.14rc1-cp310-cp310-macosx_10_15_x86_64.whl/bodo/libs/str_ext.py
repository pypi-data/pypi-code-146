import operator
import re
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, bound_function, infer_getattr, infer_global, signature
from numba.extending import intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, register_jitable, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import hstr_ext
from bodo.utils.typing import BodoError, get_overload_const_int, get_overload_const_str, is_overload_constant_int, is_overload_constant_str


def unliteral_all(args):
    return tuple(types.unliteral(a) for a in args)


ll.add_symbol('del_str', hstr_ext.del_str)
ll.add_symbol('unicode_to_utf8', hstr_ext.unicode_to_utf8)
ll.add_symbol('memcmp', hstr_ext.memcmp)
ll.add_symbol('int_to_hex', hstr_ext.int_to_hex)
string_type = types.unicode_type


@numba.njit
def contains_regex(e, in_str):
    with numba.objmode(res='bool_'):
        res = bool(e.search(in_str))
    return res


@numba.generated_jit
def str_findall_count(regex, in_str):

    def _str_findall_count_impl(regex, in_str):
        with numba.objmode(res='int64'):
            res = len(regex.findall(in_str))
        return res
    return _str_findall_count_impl


utf8_str_type = types.ArrayCTypes(types.Array(types.uint8, 1, 'C'))


@intrinsic
def unicode_to_utf8_and_len(typingctx, str_typ):
    assert str_typ in (string_type, types.Optional(string_type)) or isinstance(
        str_typ, types.StringLiteral)
    xenmv__fqddg = types.Tuple([utf8_str_type, types.int64])

    def codegen(context, builder, sig, args):
        hgiu__vvdka, = args
        lbyxn__jdi = cgutils.create_struct_proxy(string_type)(context,
            builder, value=hgiu__vvdka)
        jtf__khsi = cgutils.create_struct_proxy(utf8_str_type)(context, builder
            )
        bswq__dgfkc = cgutils.create_struct_proxy(xenmv__fqddg)(context,
            builder)
        is_ascii = builder.icmp_unsigned('==', lbyxn__jdi.is_ascii, lir.
            Constant(lbyxn__jdi.is_ascii.type, 1))
        with builder.if_else(is_ascii) as (yzvvi__foqv, ole__mlnza):
            with yzvvi__foqv:
                context.nrt.incref(builder, string_type, hgiu__vvdka)
                jtf__khsi.data = lbyxn__jdi.data
                jtf__khsi.meminfo = lbyxn__jdi.meminfo
                bswq__dgfkc.f1 = lbyxn__jdi.length
            with ole__mlnza:
                scc__opz = lir.FunctionType(lir.IntType(64), [lir.IntType(8
                    ).as_pointer(), lir.IntType(8).as_pointer(), lir.
                    IntType(64), lir.IntType(32)])
                xkq__ejil = cgutils.get_or_insert_function(builder.module,
                    scc__opz, name='unicode_to_utf8')
                uslgh__newn = context.get_constant_null(types.voidptr)
                qgog__jov = builder.call(xkq__ejil, [uslgh__newn,
                    lbyxn__jdi.data, lbyxn__jdi.length, lbyxn__jdi.kind])
                bswq__dgfkc.f1 = qgog__jov
                knh__rise = builder.add(qgog__jov, lir.Constant(lir.IntType
                    (64), 1))
                jtf__khsi.meminfo = context.nrt.meminfo_alloc_aligned(builder,
                    size=knh__rise, align=32)
                jtf__khsi.data = context.nrt.meminfo_data(builder,
                    jtf__khsi.meminfo)
                builder.call(xkq__ejil, [jtf__khsi.data, lbyxn__jdi.data,
                    lbyxn__jdi.length, lbyxn__jdi.kind])
                builder.store(lir.Constant(lir.IntType(8), 0), builder.gep(
                    jtf__khsi.data, [qgog__jov]))
        bswq__dgfkc.f0 = jtf__khsi._getvalue()
        return bswq__dgfkc._getvalue()
    return xenmv__fqddg(string_type), codegen


def unicode_to_utf8(s):
    return s


@overload(unicode_to_utf8)
def overload_unicode_to_utf8(s):
    return lambda s: unicode_to_utf8_and_len(s)[0]


def unicode_to_utf8_len(s):
    return s


@overload(unicode_to_utf8_len)
def overload_unicode_to_utf8_len(s):
    return lambda s: unicode_to_utf8_and_len(s)[1]


@overload(max)
def overload_builtin_max(lhs, rhs):
    if lhs == types.unicode_type and rhs == types.unicode_type:

        def impl(lhs, rhs):
            return lhs if lhs > rhs else rhs
        return impl


@overload(min)
def overload_builtin_min(lhs, rhs):
    if lhs == types.unicode_type and rhs == types.unicode_type:

        def impl(lhs, rhs):
            return lhs if lhs < rhs else rhs
        return impl


@intrinsic
def memcmp(typingctx, dest_t, src_t, count_t=None):

    def codegen(context, builder, sig, args):
        scc__opz = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
        lamkv__ydkpb = cgutils.get_or_insert_function(builder.module,
            scc__opz, name='memcmp')
        return builder.call(lamkv__ydkpb, args)
    return types.int32(types.voidptr, types.voidptr, types.intp), codegen


def int_to_str_len(n):
    return len(str(n))


@overload(int_to_str_len)
def overload_int_to_str_len(n):
    ggp__sgtsq = n(10)

    def impl(n):
        if n == 0:
            return 1
        ccnlo__wberc = 0
        if n < 0:
            n = -n
            ccnlo__wberc += 1
        while n > 0:
            n = n // ggp__sgtsq
            ccnlo__wberc += 1
        return ccnlo__wberc
    return impl


class StdStringType(types.Opaque):

    def __init__(self):
        super(StdStringType, self).__init__(name='StdStringType')


std_str_type = StdStringType()
register_model(StdStringType)(models.OpaqueModel)
del_str = types.ExternalFunction('del_str', types.void(std_str_type))
get_c_str = types.ExternalFunction('get_c_str', types.voidptr(std_str_type))
dummy_use = numba.njit(lambda a: None)


@overload(int)
def int_str_overload(in_str, base=10):
    if in_str == string_type:
        if is_overload_constant_int(base) and get_overload_const_int(base
            ) == 10:

            def _str_to_int_impl(in_str, base=10):
                val = _str_to_int64(in_str._data, in_str._length)
                dummy_use(in_str)
                return val
            return _str_to_int_impl

        def _str_to_int_base_impl(in_str, base=10):
            val = _str_to_int64_base(in_str._data, in_str._length, base)
            dummy_use(in_str)
            return val
        return _str_to_int_base_impl


@infer_global(float)
class StrToFloat(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        [khdjo__inhb] = args
        if isinstance(khdjo__inhb, StdStringType):
            return signature(types.float64, khdjo__inhb)
        if khdjo__inhb == string_type:
            return signature(types.float64, khdjo__inhb)


ll.add_symbol('init_string_const', hstr_ext.init_string_const)
ll.add_symbol('get_c_str', hstr_ext.get_c_str)
ll.add_symbol('str_to_int64', hstr_ext.str_to_int64)
ll.add_symbol('str_to_uint64', hstr_ext.str_to_uint64)
ll.add_symbol('str_to_int64_base', hstr_ext.str_to_int64_base)
ll.add_symbol('str_to_float64', hstr_ext.str_to_float64)
ll.add_symbol('str_to_float32', hstr_ext.str_to_float32)
ll.add_symbol('get_str_len', hstr_ext.get_str_len)
ll.add_symbol('str_from_float32', hstr_ext.str_from_float32)
ll.add_symbol('str_from_float64', hstr_ext.str_from_float64)
get_std_str_len = types.ExternalFunction('get_str_len', signature(types.
    intp, std_str_type))
init_string_from_chars = types.ExternalFunction('init_string_const',
    std_str_type(types.voidptr, types.intp))
_str_to_int64 = types.ExternalFunction('str_to_int64', signature(types.
    int64, types.voidptr, types.int64))
_str_to_uint64 = types.ExternalFunction('str_to_uint64', signature(types.
    uint64, types.voidptr, types.int64))
_str_to_int64_base = types.ExternalFunction('str_to_int64_base', signature(
    types.int64, types.voidptr, types.int64, types.int64))


def gen_unicode_to_std_str(context, builder, unicode_val):
    lbyxn__jdi = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    scc__opz = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(8
        ).as_pointer(), lir.IntType(64)])
    yfqhk__guf = cgutils.get_or_insert_function(builder.module, scc__opz,
        name='init_string_const')
    return builder.call(yfqhk__guf, [lbyxn__jdi.data, lbyxn__jdi.length])


def gen_std_str_to_unicode(context, builder, std_str_val, del_str=False):
    kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def _std_str_to_unicode(std_str):
        length = bodo.libs.str_ext.get_std_str_len(std_str)
        mrko__pujh = numba.cpython.unicode._empty_string(kind, length, 1)
        bodo.libs.str_arr_ext._memcpy(mrko__pujh._data, bodo.libs.str_ext.
            get_c_str(std_str), length, 1)
        if del_str:
            bodo.libs.str_ext.del_str(std_str)
        return mrko__pujh
    val = context.compile_internal(builder, _std_str_to_unicode,
        string_type(bodo.libs.str_ext.std_str_type), [std_str_val])
    return val


def gen_get_unicode_chars(context, builder, unicode_val):
    lbyxn__jdi = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    return lbyxn__jdi.data


@intrinsic
def unicode_to_std_str(typingctx, unicode_t=None):

    def codegen(context, builder, sig, args):
        return gen_unicode_to_std_str(context, builder, args[0])
    return std_str_type(string_type), codegen


@intrinsic
def std_str_to_unicode(typingctx, unicode_t=None):

    def codegen(context, builder, sig, args):
        return gen_std_str_to_unicode(context, builder, args[0], True)
    return string_type(std_str_type), codegen


class RandomAccessStringArrayType(types.ArrayCompatible):

    def __init__(self):
        super(RandomAccessStringArrayType, self).__init__(name=
            'RandomAccessStringArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_type

    def copy(self):
        RandomAccessStringArrayType()


random_access_string_array = RandomAccessStringArrayType()


@register_model(RandomAccessStringArrayType)
class RandomAccessStringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ntspj__rxm = [('data', types.List(string_type))]
        models.StructModel.__init__(self, dmm, fe_type, ntspj__rxm)


make_attribute_wrapper(RandomAccessStringArrayType, 'data', '_data')


@intrinsic
def alloc_random_access_string_array(typingctx, n_t=None):

    def codegen(context, builder, sig, args):
        evgjt__ntr, = args
        yxtz__vbg = types.List(string_type)
        nexjl__vvicw = numba.cpython.listobj.ListInstance.allocate(context,
            builder, yxtz__vbg, evgjt__ntr)
        nexjl__vvicw.size = evgjt__ntr
        nonwv__byvki = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        nonwv__byvki.data = nexjl__vvicw.value
        return nonwv__byvki._getvalue()
    return random_access_string_array(types.intp), codegen


@overload(operator.getitem, no_unliteral=True)
def random_access_str_arr_getitem(A, ind):
    if A != random_access_string_array:
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]


@overload(operator.setitem)
def random_access_str_arr_setitem(A, idx, val):
    if A != random_access_string_array:
        return
    if isinstance(idx, types.Integer):
        assert val == string_type

        def impl_scalar(A, idx, val):
            A._data[idx] = val
        return impl_scalar


@overload(len, no_unliteral=True)
def overload_str_arr_len(A):
    if A == random_access_string_array:
        return lambda A: len(A._data)


@overload_attribute(RandomAccessStringArrayType, 'shape')
def overload_str_arr_shape(A):
    return lambda A: (len(A._data),)


def alloc_random_access_str_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_libs_str_ext_alloc_random_access_string_array
    ) = alloc_random_access_str_arr_equiv
str_from_float32 = types.ExternalFunction('str_from_float32', types.void(
    types.voidptr, types.float32))
str_from_float64 = types.ExternalFunction('str_from_float64', types.void(
    types.voidptr, types.float64))


def float_to_str(s, v):
    pass


@overload(float_to_str)
def float_to_str_overload(s, v):
    assert isinstance(v, types.Float)
    if v == types.float32:
        return lambda s, v: str_from_float32(s._data, v)
    return lambda s, v: str_from_float64(s._data, v)


@overload(str)
def float_str_overload(v):
    if isinstance(v, types.Float):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(v):
            if v == 0:
                return '0.0'
            mjv__etu = 0
            znb__zdp = v
            if znb__zdp < 0:
                mjv__etu = 1
                znb__zdp = -znb__zdp
            if znb__zdp < 1:
                lgskr__ies = 1
            else:
                lgskr__ies = 1 + int(np.floor(np.log10(znb__zdp)))
            length = mjv__etu + lgskr__ies + 1 + 6
            s = numba.cpython.unicode._malloc_string(kind, 1, length, True)
            float_to_str(s, v)
            return s
        return impl


@overload(format, no_unliteral=True)
def overload_format(value, format_spec=''):
    if is_overload_constant_str(format_spec) and get_overload_const_str(
        format_spec) == '':

        def impl_fast(value, format_spec=''):
            return str(value)
        return impl_fast

    def impl(value, format_spec=''):
        with numba.objmode(res='string'):
            res = format(value, format_spec)
        return res
    return impl


@lower_cast(StdStringType, types.float64)
def cast_str_to_float64(context, builder, fromty, toty, val):
    scc__opz = lir.FunctionType(lir.DoubleType(), [lir.IntType(8).as_pointer()]
        )
    yfqhk__guf = cgutils.get_or_insert_function(builder.module, scc__opz,
        name='str_to_float64')
    res = builder.call(yfqhk__guf, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(StdStringType, types.float32)
def cast_str_to_float32(context, builder, fromty, toty, val):
    scc__opz = lir.FunctionType(lir.FloatType(), [lir.IntType(8).as_pointer()])
    yfqhk__guf = cgutils.get_or_insert_function(builder.module, scc__opz,
        name='str_to_float32')
    res = builder.call(yfqhk__guf, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.float64)
def cast_unicode_str_to_float64(context, builder, fromty, toty, val):
    std_str = gen_unicode_to_std_str(context, builder, val)
    return cast_str_to_float64(context, builder, std_str_type, toty, std_str)


@lower_cast(string_type, types.float32)
def cast_unicode_str_to_float32(context, builder, fromty, toty, val):
    std_str = gen_unicode_to_std_str(context, builder, val)
    return cast_str_to_float32(context, builder, std_str_type, toty, std_str)


@lower_cast(string_type, types.int64)
@lower_cast(string_type, types.int32)
@lower_cast(string_type, types.int16)
@lower_cast(string_type, types.int8)
def cast_unicode_str_to_int64(context, builder, fromty, toty, val):
    lbyxn__jdi = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    scc__opz = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(8)
        .as_pointer(), lir.IntType(64)])
    yfqhk__guf = cgutils.get_or_insert_function(builder.module, scc__opz,
        name='str_to_int64')
    res = builder.call(yfqhk__guf, (lbyxn__jdi.data, lbyxn__jdi.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.uint64)
@lower_cast(string_type, types.uint32)
@lower_cast(string_type, types.uint16)
@lower_cast(string_type, types.uint8)
def cast_unicode_str_to_uint64(context, builder, fromty, toty, val):
    lbyxn__jdi = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    scc__opz = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(8)
        .as_pointer(), lir.IntType(64)])
    yfqhk__guf = cgutils.get_or_insert_function(builder.module, scc__opz,
        name='str_to_uint64')
    res = builder.call(yfqhk__guf, (lbyxn__jdi.data, lbyxn__jdi.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@infer_getattr
class StringAttribute(AttributeTemplate):
    key = types.UnicodeType

    @bound_function('str.format', no_unliteral=True)
    def resolve_format(self, string_typ, args, kws):
        kws = dict(kws)
        sido__sbt = ', '.join('e{}'.format(ohou__byac) for ohou__byac in
            range(len(args)))
        if sido__sbt:
            sido__sbt += ', '
        lkhby__bvmz = ', '.join("{} = ''".format(a) for a in kws.keys())
        xwvl__gfjoj = f'def format_stub(string, {sido__sbt} {lkhby__bvmz}):\n'
        xwvl__gfjoj += '    pass\n'
        hir__yec = {}
        exec(xwvl__gfjoj, {}, hir__yec)
        bbv__nxeum = hir__yec['format_stub']
        hwgb__juobu = numba.core.utils.pysignature(bbv__nxeum)
        talm__ddr = (string_typ,) + args + tuple(kws.values())
        return signature(string_typ, talm__ddr).replace(pysig=hwgb__juobu)


@numba.njit(cache=True)
def str_split(arr, pat, n):
    mjlwc__dihay = pat is not None and len(pat) > 1
    if mjlwc__dihay:
        hjqn__jqp = re.compile(pat)
        if n == -1:
            n = 0
    elif n == 0:
        n = -1
    nexjl__vvicw = len(arr)
    yegj__ijyqn = 0
    kkbyv__crq = 0
    for ohou__byac in numba.parfors.parfor.internal_prange(nexjl__vvicw):
        if bodo.libs.array_kernels.isna(arr, ohou__byac):
            continue
        if mjlwc__dihay:
            khj__loihz = hjqn__jqp.split(arr[ohou__byac], maxsplit=n)
        elif pat == '':
            khj__loihz = [''] + list(arr[ohou__byac]) + ['']
        else:
            khj__loihz = arr[ohou__byac].split(pat, n)
        yegj__ijyqn += len(khj__loihz)
        for s in khj__loihz:
            kkbyv__crq += bodo.libs.str_arr_ext.get_utf8_size(s)
    ouob__idzr = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        nexjl__vvicw, (yegj__ijyqn, kkbyv__crq), bodo.libs.str_arr_ext.
        string_array_type)
    vyzw__tajg = bodo.libs.array_item_arr_ext.get_offsets(ouob__idzr)
    ckcu__mxig = bodo.libs.array_item_arr_ext.get_null_bitmap(ouob__idzr)
    wdj__tlh = bodo.libs.array_item_arr_ext.get_data(ouob__idzr)
    ngn__difkx = 0
    for ppci__tjk in numba.parfors.parfor.internal_prange(nexjl__vvicw):
        vyzw__tajg[ppci__tjk] = ngn__difkx
        if bodo.libs.array_kernels.isna(arr, ppci__tjk):
            bodo.libs.int_arr_ext.set_bit_to_arr(ckcu__mxig, ppci__tjk, 0)
            continue
        bodo.libs.int_arr_ext.set_bit_to_arr(ckcu__mxig, ppci__tjk, 1)
        if mjlwc__dihay:
            khj__loihz = hjqn__jqp.split(arr[ppci__tjk], maxsplit=n)
        elif pat == '':
            khj__loihz = [''] + list(arr[ppci__tjk]) + ['']
        else:
            khj__loihz = arr[ppci__tjk].split(pat, n)
        jpxl__qrltt = len(khj__loihz)
        for vcag__ril in range(jpxl__qrltt):
            s = khj__loihz[vcag__ril]
            wdj__tlh[ngn__difkx] = s
            ngn__difkx += 1
    vyzw__tajg[nexjl__vvicw] = ngn__difkx
    return ouob__idzr


@overload(hex)
def overload_hex(x):
    if isinstance(x, types.Integer):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(x):
            x = np.int64(x)
            if x < 0:
                fmgm__nifgg = '-0x'
                x = x * -1
            else:
                fmgm__nifgg = '0x'
            x = np.uint64(x)
            if x == 0:
                kydct__wngsk = 1
            else:
                kydct__wngsk = fast_ceil_log2(x + 1)
                kydct__wngsk = (kydct__wngsk + 3) // 4
            length = len(fmgm__nifgg) + kydct__wngsk
            output = numba.cpython.unicode._empty_string(kind, length, 1)
            bodo.libs.str_arr_ext._memcpy(output._data, fmgm__nifgg._data,
                len(fmgm__nifgg), 1)
            int_to_hex(output, kydct__wngsk, len(fmgm__nifgg), x)
            return output
        return impl


@register_jitable
def fast_ceil_log2(x):
    ycmpe__als = 0 if x & x - 1 == 0 else 1
    vejaw__gisj = [np.uint64(18446744069414584320), np.uint64(4294901760),
        np.uint64(65280), np.uint64(240), np.uint64(12), np.uint64(2)]
    fvmw__qptwc = 32
    for ohou__byac in range(len(vejaw__gisj)):
        bpz__masx = 0 if x & vejaw__gisj[ohou__byac] == 0 else fvmw__qptwc
        ycmpe__als = ycmpe__als + bpz__masx
        x = x >> bpz__masx
        fvmw__qptwc = fvmw__qptwc >> 1
    return ycmpe__als


@intrinsic
def int_to_hex(typingctx, output, out_len, header_len, int_val):

    def codegen(context, builder, sig, args):
        output, out_len, header_len, int_val = args
        ctsf__jjd = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=output)
        scc__opz = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(64)])
        sdwmt__lkkk = cgutils.get_or_insert_function(builder.module,
            scc__opz, name='int_to_hex')
        lmpor__qzgo = builder.inttoptr(builder.add(builder.ptrtoint(
            ctsf__jjd.data, lir.IntType(64)), header_len), lir.IntType(8).
            as_pointer())
        builder.call(sdwmt__lkkk, (lmpor__qzgo, out_len, int_val))
    return types.void(output, out_len, header_len, int_val), codegen


def alloc_empty_bytes_or_string_data(typ, kind, length, is_ascii=0):
    pass


@overload(alloc_empty_bytes_or_string_data)
def overload_alloc_empty_bytes_or_string_data(typ, kind, length, is_ascii=0):
    typ = typ.instance_type if isinstance(typ, types.TypeRef) else typ
    if typ == bodo.bytes_type:
        return lambda typ, kind, length, is_ascii=0: np.empty(length, np.uint8)
    if typ == string_type:
        return (lambda typ, kind, length, is_ascii=0: numba.cpython.unicode
            ._empty_string(kind, length, is_ascii))
    raise BodoError(
        f'Internal Error: Expected Bytes or String type, found {typ}')


def get_unicode_or_numpy_data(val):
    pass


@overload(get_unicode_or_numpy_data)
def overload_get_unicode_or_numpy_data(val):
    if val == string_type:
        return lambda val: val._data
    if isinstance(val, types.Array):
        return lambda val: val.ctypes
    raise BodoError(
        f'Internal Error: Expected String or Numpy Array, found {val}')
