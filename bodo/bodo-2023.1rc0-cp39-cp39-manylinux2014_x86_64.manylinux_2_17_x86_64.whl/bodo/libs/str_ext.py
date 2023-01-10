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
    pdf__tcxy = types.Tuple([utf8_str_type, types.int64])

    def codegen(context, builder, sig, args):
        eiepy__rzi, = args
        stv__rpvdt = cgutils.create_struct_proxy(string_type)(context,
            builder, value=eiepy__rzi)
        urgw__hokfr = cgutils.create_struct_proxy(utf8_str_type)(context,
            builder)
        llfty__hcir = cgutils.create_struct_proxy(pdf__tcxy)(context, builder)
        is_ascii = builder.icmp_unsigned('==', stv__rpvdt.is_ascii, lir.
            Constant(stv__rpvdt.is_ascii.type, 1))
        with builder.if_else(is_ascii) as (fdpj__xlz, tzzlo__oes):
            with fdpj__xlz:
                context.nrt.incref(builder, string_type, eiepy__rzi)
                urgw__hokfr.data = stv__rpvdt.data
                urgw__hokfr.meminfo = stv__rpvdt.meminfo
                llfty__hcir.f1 = stv__rpvdt.length
            with tzzlo__oes:
                nzn__fda = lir.FunctionType(lir.IntType(64), [lir.IntType(8
                    ).as_pointer(), lir.IntType(8).as_pointer(), lir.
                    IntType(64), lir.IntType(32)])
                irzya__axr = cgutils.get_or_insert_function(builder.module,
                    nzn__fda, name='unicode_to_utf8')
                izltd__mgdwo = context.get_constant_null(types.voidptr)
                qvoh__ctlk = builder.call(irzya__axr, [izltd__mgdwo,
                    stv__rpvdt.data, stv__rpvdt.length, stv__rpvdt.kind])
                llfty__hcir.f1 = qvoh__ctlk
                igmc__jtatr = builder.add(qvoh__ctlk, lir.Constant(lir.
                    IntType(64), 1))
                urgw__hokfr.meminfo = context.nrt.meminfo_alloc_aligned(builder
                    , size=igmc__jtatr, align=32)
                urgw__hokfr.data = context.nrt.meminfo_data(builder,
                    urgw__hokfr.meminfo)
                builder.call(irzya__axr, [urgw__hokfr.data, stv__rpvdt.data,
                    stv__rpvdt.length, stv__rpvdt.kind])
                builder.store(lir.Constant(lir.IntType(8), 0), builder.gep(
                    urgw__hokfr.data, [qvoh__ctlk]))
        llfty__hcir.f0 = urgw__hokfr._getvalue()
        return llfty__hcir._getvalue()
    return pdf__tcxy(string_type), codegen


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
        nzn__fda = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
        ejl__xtck = cgutils.get_or_insert_function(builder.module, nzn__fda,
            name='memcmp')
        return builder.call(ejl__xtck, args)
    return types.int32(types.voidptr, types.voidptr, types.intp), codegen


def int_to_str_len(n):
    return len(str(n))


@overload(int_to_str_len)
def overload_int_to_str_len(n):
    tmhu__vtgs = n(10)

    def impl(n):
        if n == 0:
            return 1
        ultv__bpsdv = 0
        if n < 0:
            n = -n
            ultv__bpsdv += 1
        while n > 0:
            n = n // tmhu__vtgs
            ultv__bpsdv += 1
        return ultv__bpsdv
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
        [xkv__amkq] = args
        if isinstance(xkv__amkq, StdStringType):
            return signature(types.float64, xkv__amkq)
        if xkv__amkq == string_type:
            return signature(types.float64, xkv__amkq)


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
    stv__rpvdt = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    nzn__fda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(8
        ).as_pointer(), lir.IntType(64)])
    sycap__pflea = cgutils.get_or_insert_function(builder.module, nzn__fda,
        name='init_string_const')
    return builder.call(sycap__pflea, [stv__rpvdt.data, stv__rpvdt.length])


def gen_std_str_to_unicode(context, builder, std_str_val, del_str=False):
    kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def _std_str_to_unicode(std_str):
        length = bodo.libs.str_ext.get_std_str_len(std_str)
        wked__jtt = numba.cpython.unicode._empty_string(kind, length, 1)
        bodo.libs.str_arr_ext._memcpy(wked__jtt._data, bodo.libs.str_ext.
            get_c_str(std_str), length, 1)
        if del_str:
            bodo.libs.str_ext.del_str(std_str)
        return wked__jtt
    val = context.compile_internal(builder, _std_str_to_unicode,
        string_type(bodo.libs.str_ext.std_str_type), [std_str_val])
    return val


def gen_get_unicode_chars(context, builder, unicode_val):
    stv__rpvdt = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    return stv__rpvdt.data


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
        ydv__khxdw = [('data', types.List(string_type))]
        models.StructModel.__init__(self, dmm, fe_type, ydv__khxdw)


make_attribute_wrapper(RandomAccessStringArrayType, 'data', '_data')


@intrinsic
def alloc_random_access_string_array(typingctx, n_t=None):

    def codegen(context, builder, sig, args):
        bvt__xicu, = args
        eenl__svqv = types.List(string_type)
        psqgg__creij = numba.cpython.listobj.ListInstance.allocate(context,
            builder, eenl__svqv, bvt__xicu)
        psqgg__creij.size = bvt__xicu
        wnn__janw = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        wnn__janw.data = psqgg__creij.value
        return wnn__janw._getvalue()
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
            humh__bxa = 0
            lnah__tvjsf = v
            if lnah__tvjsf < 0:
                humh__bxa = 1
                lnah__tvjsf = -lnah__tvjsf
            if lnah__tvjsf < 1:
                nkkt__rmp = 1
            else:
                nkkt__rmp = 1 + int(np.floor(np.log10(lnah__tvjsf)))
            length = humh__bxa + nkkt__rmp + 1 + 6
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
    nzn__fda = lir.FunctionType(lir.DoubleType(), [lir.IntType(8).as_pointer()]
        )
    sycap__pflea = cgutils.get_or_insert_function(builder.module, nzn__fda,
        name='str_to_float64')
    res = builder.call(sycap__pflea, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(StdStringType, types.float32)
def cast_str_to_float32(context, builder, fromty, toty, val):
    nzn__fda = lir.FunctionType(lir.FloatType(), [lir.IntType(8).as_pointer()])
    sycap__pflea = cgutils.get_or_insert_function(builder.module, nzn__fda,
        name='str_to_float32')
    res = builder.call(sycap__pflea, (val,))
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
    stv__rpvdt = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    nzn__fda = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(8)
        .as_pointer(), lir.IntType(64)])
    sycap__pflea = cgutils.get_or_insert_function(builder.module, nzn__fda,
        name='str_to_int64')
    res = builder.call(sycap__pflea, (stv__rpvdt.data, stv__rpvdt.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.uint64)
@lower_cast(string_type, types.uint32)
@lower_cast(string_type, types.uint16)
@lower_cast(string_type, types.uint8)
def cast_unicode_str_to_uint64(context, builder, fromty, toty, val):
    stv__rpvdt = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    nzn__fda = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(8)
        .as_pointer(), lir.IntType(64)])
    sycap__pflea = cgutils.get_or_insert_function(builder.module, nzn__fda,
        name='str_to_uint64')
    res = builder.call(sycap__pflea, (stv__rpvdt.data, stv__rpvdt.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@infer_getattr
class StringAttribute(AttributeTemplate):
    key = types.UnicodeType

    @bound_function('str.format', no_unliteral=True)
    def resolve_format(self, string_typ, args, kws):
        kws = dict(kws)
        clkx__sgbr = ', '.join('e{}'.format(yhyzz__zuv) for yhyzz__zuv in
            range(len(args)))
        if clkx__sgbr:
            clkx__sgbr += ', '
        zcxj__ibag = ', '.join("{} = ''".format(a) for a in kws.keys())
        tzy__ztm = f'def format_stub(string, {clkx__sgbr} {zcxj__ibag}):\n'
        tzy__ztm += '    pass\n'
        sdj__xax = {}
        exec(tzy__ztm, {}, sdj__xax)
        qbfa__hxwgd = sdj__xax['format_stub']
        hnj__gdsjz = numba.core.utils.pysignature(qbfa__hxwgd)
        jqvvk__tbk = (string_typ,) + args + tuple(kws.values())
        return signature(string_typ, jqvvk__tbk).replace(pysig=hnj__gdsjz)


@numba.njit(cache=True)
def str_split(arr, pat, n):
    abqee__kys = pat is not None and len(pat) > 1
    if abqee__kys:
        rzoig__otpbt = re.compile(pat)
        if n == -1:
            n = 0
    elif n == 0:
        n = -1
    psqgg__creij = len(arr)
    xseqi__tiacw = 0
    yifh__xjnr = 0
    for yhyzz__zuv in numba.parfors.parfor.internal_prange(psqgg__creij):
        if bodo.libs.array_kernels.isna(arr, yhyzz__zuv):
            continue
        if abqee__kys:
            avo__rfdlr = rzoig__otpbt.split(arr[yhyzz__zuv], maxsplit=n)
        elif pat == '':
            avo__rfdlr = [''] + list(arr[yhyzz__zuv]) + ['']
        else:
            avo__rfdlr = arr[yhyzz__zuv].split(pat, n)
        xseqi__tiacw += len(avo__rfdlr)
        for s in avo__rfdlr:
            yifh__xjnr += bodo.libs.str_arr_ext.get_utf8_size(s)
    tzf__pkd = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        psqgg__creij, (xseqi__tiacw, yifh__xjnr), bodo.libs.str_arr_ext.
        string_array_type)
    bugsr__zbd = bodo.libs.array_item_arr_ext.get_offsets(tzf__pkd)
    iit__tcnlk = bodo.libs.array_item_arr_ext.get_null_bitmap(tzf__pkd)
    jrop__ofccv = bodo.libs.array_item_arr_ext.get_data(tzf__pkd)
    ocfn__ebni = 0
    for pwaiv__wys in numba.parfors.parfor.internal_prange(psqgg__creij):
        bugsr__zbd[pwaiv__wys] = ocfn__ebni
        if bodo.libs.array_kernels.isna(arr, pwaiv__wys):
            bodo.libs.int_arr_ext.set_bit_to_arr(iit__tcnlk, pwaiv__wys, 0)
            continue
        bodo.libs.int_arr_ext.set_bit_to_arr(iit__tcnlk, pwaiv__wys, 1)
        if abqee__kys:
            avo__rfdlr = rzoig__otpbt.split(arr[pwaiv__wys], maxsplit=n)
        elif pat == '':
            avo__rfdlr = [''] + list(arr[pwaiv__wys]) + ['']
        else:
            avo__rfdlr = arr[pwaiv__wys].split(pat, n)
        shij__obqgf = len(avo__rfdlr)
        for tcf__bpo in range(shij__obqgf):
            s = avo__rfdlr[tcf__bpo]
            jrop__ofccv[ocfn__ebni] = s
            ocfn__ebni += 1
    bugsr__zbd[psqgg__creij] = ocfn__ebni
    return tzf__pkd


@overload(hex)
def overload_hex(x):
    if isinstance(x, types.Integer):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(x):
            x = np.int64(x)
            if x < 0:
                jmli__vmqf = '-0x'
                x = x * -1
            else:
                jmli__vmqf = '0x'
            x = np.uint64(x)
            if x == 0:
                gjez__legv = 1
            else:
                gjez__legv = fast_ceil_log2(x + 1)
                gjez__legv = (gjez__legv + 3) // 4
            length = len(jmli__vmqf) + gjez__legv
            output = numba.cpython.unicode._empty_string(kind, length, 1)
            bodo.libs.str_arr_ext._memcpy(output._data, jmli__vmqf._data,
                len(jmli__vmqf), 1)
            int_to_hex(output, gjez__legv, len(jmli__vmqf), x)
            return output
        return impl


@register_jitable
def fast_ceil_log2(x):
    rheg__bywnr = 0 if x & x - 1 == 0 else 1
    zpw__nhi = [np.uint64(18446744069414584320), np.uint64(4294901760), np.
        uint64(65280), np.uint64(240), np.uint64(12), np.uint64(2)]
    uzh__jclot = 32
    for yhyzz__zuv in range(len(zpw__nhi)):
        qepnd__fns = 0 if x & zpw__nhi[yhyzz__zuv] == 0 else uzh__jclot
        rheg__bywnr = rheg__bywnr + qepnd__fns
        x = x >> qepnd__fns
        uzh__jclot = uzh__jclot >> 1
    return rheg__bywnr


@intrinsic
def int_to_hex(typingctx, output, out_len, header_len, int_val):

    def codegen(context, builder, sig, args):
        output, out_len, header_len, int_val = args
        xtxn__vld = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=output)
        nzn__fda = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(64)])
        qcce__fwgd = cgutils.get_or_insert_function(builder.module,
            nzn__fda, name='int_to_hex')
        has__hqutx = builder.inttoptr(builder.add(builder.ptrtoint(
            xtxn__vld.data, lir.IntType(64)), header_len), lir.IntType(8).
            as_pointer())
        builder.call(qcce__fwgd, (has__hqutx, out_len, int_val))
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
