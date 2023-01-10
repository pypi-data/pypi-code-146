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
    nla__isc = types.Tuple([utf8_str_type, types.int64])

    def codegen(context, builder, sig, args):
        kot__huid, = args
        qqyfl__ftq = cgutils.create_struct_proxy(string_type)(context,
            builder, value=kot__huid)
        nxoe__izps = cgutils.create_struct_proxy(utf8_str_type)(context,
            builder)
        sdymk__ylgqv = cgutils.create_struct_proxy(nla__isc)(context, builder)
        is_ascii = builder.icmp_unsigned('==', qqyfl__ftq.is_ascii, lir.
            Constant(qqyfl__ftq.is_ascii.type, 1))
        with builder.if_else(is_ascii) as (tuoje__vxbzt, vvd__grhjb):
            with tuoje__vxbzt:
                context.nrt.incref(builder, string_type, kot__huid)
                nxoe__izps.data = qqyfl__ftq.data
                nxoe__izps.meminfo = qqyfl__ftq.meminfo
                sdymk__ylgqv.f1 = qqyfl__ftq.length
            with vvd__grhjb:
                ybd__pyx = lir.FunctionType(lir.IntType(64), [lir.IntType(8
                    ).as_pointer(), lir.IntType(8).as_pointer(), lir.
                    IntType(64), lir.IntType(32)])
                xzdr__aent = cgutils.get_or_insert_function(builder.module,
                    ybd__pyx, name='unicode_to_utf8')
                bveye__wltdk = context.get_constant_null(types.voidptr)
                hunhh__zdvpg = builder.call(xzdr__aent, [bveye__wltdk,
                    qqyfl__ftq.data, qqyfl__ftq.length, qqyfl__ftq.kind])
                sdymk__ylgqv.f1 = hunhh__zdvpg
                jjey__lwe = builder.add(hunhh__zdvpg, lir.Constant(lir.
                    IntType(64), 1))
                nxoe__izps.meminfo = context.nrt.meminfo_alloc_aligned(builder,
                    size=jjey__lwe, align=32)
                nxoe__izps.data = context.nrt.meminfo_data(builder,
                    nxoe__izps.meminfo)
                builder.call(xzdr__aent, [nxoe__izps.data, qqyfl__ftq.data,
                    qqyfl__ftq.length, qqyfl__ftq.kind])
                builder.store(lir.Constant(lir.IntType(8), 0), builder.gep(
                    nxoe__izps.data, [hunhh__zdvpg]))
        sdymk__ylgqv.f0 = nxoe__izps._getvalue()
        return sdymk__ylgqv._getvalue()
    return nla__isc(string_type), codegen


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
        ybd__pyx = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
        ejq__jdph = cgutils.get_or_insert_function(builder.module, ybd__pyx,
            name='memcmp')
        return builder.call(ejq__jdph, args)
    return types.int32(types.voidptr, types.voidptr, types.intp), codegen


def int_to_str_len(n):
    return len(str(n))


@overload(int_to_str_len)
def overload_int_to_str_len(n):
    yyarw__tihlb = n(10)

    def impl(n):
        if n == 0:
            return 1
        sjyei__rlb = 0
        if n < 0:
            n = -n
            sjyei__rlb += 1
        while n > 0:
            n = n // yyarw__tihlb
            sjyei__rlb += 1
        return sjyei__rlb
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
        [nse__oxrq] = args
        if isinstance(nse__oxrq, StdStringType):
            return signature(types.float64, nse__oxrq)
        if nse__oxrq == string_type:
            return signature(types.float64, nse__oxrq)


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
    qqyfl__ftq = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    ybd__pyx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(8
        ).as_pointer(), lir.IntType(64)])
    ciu__fifrf = cgutils.get_or_insert_function(builder.module, ybd__pyx,
        name='init_string_const')
    return builder.call(ciu__fifrf, [qqyfl__ftq.data, qqyfl__ftq.length])


def gen_std_str_to_unicode(context, builder, std_str_val, del_str=False):
    kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def _std_str_to_unicode(std_str):
        length = bodo.libs.str_ext.get_std_str_len(std_str)
        gtv__swfkp = numba.cpython.unicode._empty_string(kind, length, 1)
        bodo.libs.str_arr_ext._memcpy(gtv__swfkp._data, bodo.libs.str_ext.
            get_c_str(std_str), length, 1)
        if del_str:
            bodo.libs.str_ext.del_str(std_str)
        return gtv__swfkp
    val = context.compile_internal(builder, _std_str_to_unicode,
        string_type(bodo.libs.str_ext.std_str_type), [std_str_val])
    return val


def gen_get_unicode_chars(context, builder, unicode_val):
    qqyfl__ftq = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    return qqyfl__ftq.data


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
        etcnq__meill = [('data', types.List(string_type))]
        models.StructModel.__init__(self, dmm, fe_type, etcnq__meill)


make_attribute_wrapper(RandomAccessStringArrayType, 'data', '_data')


@intrinsic
def alloc_random_access_string_array(typingctx, n_t=None):

    def codegen(context, builder, sig, args):
        oxuwp__vrakt, = args
        sgk__rogg = types.List(string_type)
        eyz__utfl = numba.cpython.listobj.ListInstance.allocate(context,
            builder, sgk__rogg, oxuwp__vrakt)
        eyz__utfl.size = oxuwp__vrakt
        yily__blav = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        yily__blav.data = eyz__utfl.value
        return yily__blav._getvalue()
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
            iwn__wxo = 0
            ujgd__dduqg = v
            if ujgd__dduqg < 0:
                iwn__wxo = 1
                ujgd__dduqg = -ujgd__dduqg
            if ujgd__dduqg < 1:
                ldpzk__exyu = 1
            else:
                ldpzk__exyu = 1 + int(np.floor(np.log10(ujgd__dduqg)))
            length = iwn__wxo + ldpzk__exyu + 1 + 6
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
    ybd__pyx = lir.FunctionType(lir.DoubleType(), [lir.IntType(8).as_pointer()]
        )
    ciu__fifrf = cgutils.get_or_insert_function(builder.module, ybd__pyx,
        name='str_to_float64')
    res = builder.call(ciu__fifrf, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(StdStringType, types.float32)
def cast_str_to_float32(context, builder, fromty, toty, val):
    ybd__pyx = lir.FunctionType(lir.FloatType(), [lir.IntType(8).as_pointer()])
    ciu__fifrf = cgutils.get_or_insert_function(builder.module, ybd__pyx,
        name='str_to_float32')
    res = builder.call(ciu__fifrf, (val,))
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
    qqyfl__ftq = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    ybd__pyx = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(8)
        .as_pointer(), lir.IntType(64)])
    ciu__fifrf = cgutils.get_or_insert_function(builder.module, ybd__pyx,
        name='str_to_int64')
    res = builder.call(ciu__fifrf, (qqyfl__ftq.data, qqyfl__ftq.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.uint64)
@lower_cast(string_type, types.uint32)
@lower_cast(string_type, types.uint16)
@lower_cast(string_type, types.uint8)
def cast_unicode_str_to_uint64(context, builder, fromty, toty, val):
    qqyfl__ftq = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    ybd__pyx = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(8)
        .as_pointer(), lir.IntType(64)])
    ciu__fifrf = cgutils.get_or_insert_function(builder.module, ybd__pyx,
        name='str_to_uint64')
    res = builder.call(ciu__fifrf, (qqyfl__ftq.data, qqyfl__ftq.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@infer_getattr
class StringAttribute(AttributeTemplate):
    key = types.UnicodeType

    @bound_function('str.format', no_unliteral=True)
    def resolve_format(self, string_typ, args, kws):
        kws = dict(kws)
        gkj__ztap = ', '.join('e{}'.format(upc__fmj) for upc__fmj in range(
            len(args)))
        if gkj__ztap:
            gkj__ztap += ', '
        jnh__goa = ', '.join("{} = ''".format(a) for a in kws.keys())
        xjigv__vstm = f'def format_stub(string, {gkj__ztap} {jnh__goa}):\n'
        xjigv__vstm += '    pass\n'
        yewxr__upq = {}
        exec(xjigv__vstm, {}, yewxr__upq)
        uuism__fqtwf = yewxr__upq['format_stub']
        zwu__oskql = numba.core.utils.pysignature(uuism__fqtwf)
        hxo__waog = (string_typ,) + args + tuple(kws.values())
        return signature(string_typ, hxo__waog).replace(pysig=zwu__oskql)


@numba.njit(cache=True)
def str_split(arr, pat, n):
    vhj__yanw = pat is not None and len(pat) > 1
    if vhj__yanw:
        lpfl__ismmb = re.compile(pat)
        if n == -1:
            n = 0
    elif n == 0:
        n = -1
    eyz__utfl = len(arr)
    fup__relfm = 0
    fzn__hoah = 0
    for upc__fmj in numba.parfors.parfor.internal_prange(eyz__utfl):
        if bodo.libs.array_kernels.isna(arr, upc__fmj):
            continue
        if vhj__yanw:
            dzrj__cmnqz = lpfl__ismmb.split(arr[upc__fmj], maxsplit=n)
        elif pat == '':
            dzrj__cmnqz = [''] + list(arr[upc__fmj]) + ['']
        else:
            dzrj__cmnqz = arr[upc__fmj].split(pat, n)
        fup__relfm += len(dzrj__cmnqz)
        for s in dzrj__cmnqz:
            fzn__hoah += bodo.libs.str_arr_ext.get_utf8_size(s)
    nunic__pra = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        eyz__utfl, (fup__relfm, fzn__hoah), bodo.libs.str_arr_ext.
        string_array_type)
    ofzbj__ykg = bodo.libs.array_item_arr_ext.get_offsets(nunic__pra)
    jvzlt__vwwmj = bodo.libs.array_item_arr_ext.get_null_bitmap(nunic__pra)
    gyyz__pmx = bodo.libs.array_item_arr_ext.get_data(nunic__pra)
    yfeek__luie = 0
    for tywbr__htm in numba.parfors.parfor.internal_prange(eyz__utfl):
        ofzbj__ykg[tywbr__htm] = yfeek__luie
        if bodo.libs.array_kernels.isna(arr, tywbr__htm):
            bodo.libs.int_arr_ext.set_bit_to_arr(jvzlt__vwwmj, tywbr__htm, 0)
            continue
        bodo.libs.int_arr_ext.set_bit_to_arr(jvzlt__vwwmj, tywbr__htm, 1)
        if vhj__yanw:
            dzrj__cmnqz = lpfl__ismmb.split(arr[tywbr__htm], maxsplit=n)
        elif pat == '':
            dzrj__cmnqz = [''] + list(arr[tywbr__htm]) + ['']
        else:
            dzrj__cmnqz = arr[tywbr__htm].split(pat, n)
        ypn__pub = len(dzrj__cmnqz)
        for lpor__unthq in range(ypn__pub):
            s = dzrj__cmnqz[lpor__unthq]
            gyyz__pmx[yfeek__luie] = s
            yfeek__luie += 1
    ofzbj__ykg[eyz__utfl] = yfeek__luie
    return nunic__pra


@overload(hex)
def overload_hex(x):
    if isinstance(x, types.Integer):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(x):
            x = np.int64(x)
            if x < 0:
                blmqt__xbei = '-0x'
                x = x * -1
            else:
                blmqt__xbei = '0x'
            x = np.uint64(x)
            if x == 0:
                pwnxg__nfk = 1
            else:
                pwnxg__nfk = fast_ceil_log2(x + 1)
                pwnxg__nfk = (pwnxg__nfk + 3) // 4
            length = len(blmqt__xbei) + pwnxg__nfk
            output = numba.cpython.unicode._empty_string(kind, length, 1)
            bodo.libs.str_arr_ext._memcpy(output._data, blmqt__xbei._data,
                len(blmqt__xbei), 1)
            int_to_hex(output, pwnxg__nfk, len(blmqt__xbei), x)
            return output
        return impl


@register_jitable
def fast_ceil_log2(x):
    knjy__kcxvd = 0 if x & x - 1 == 0 else 1
    tcqxp__xdmt = [np.uint64(18446744069414584320), np.uint64(4294901760),
        np.uint64(65280), np.uint64(240), np.uint64(12), np.uint64(2)]
    xvy__pno = 32
    for upc__fmj in range(len(tcqxp__xdmt)):
        clcpx__njssr = 0 if x & tcqxp__xdmt[upc__fmj] == 0 else xvy__pno
        knjy__kcxvd = knjy__kcxvd + clcpx__njssr
        x = x >> clcpx__njssr
        xvy__pno = xvy__pno >> 1
    return knjy__kcxvd


@intrinsic
def int_to_hex(typingctx, output, out_len, header_len, int_val):

    def codegen(context, builder, sig, args):
        output, out_len, header_len, int_val = args
        pqxfh__pxui = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=output)
        ybd__pyx = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(64)])
        mcybp__kitv = cgutils.get_or_insert_function(builder.module,
            ybd__pyx, name='int_to_hex')
        bjnz__lsnz = builder.inttoptr(builder.add(builder.ptrtoint(
            pqxfh__pxui.data, lir.IntType(64)), header_len), lir.IntType(8)
            .as_pointer())
        builder.call(mcybp__kitv, (bjnz__lsnz, out_len, int_val))
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
