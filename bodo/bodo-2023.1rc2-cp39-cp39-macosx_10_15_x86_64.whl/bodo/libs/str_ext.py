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
    fniuq__yufc = types.Tuple([utf8_str_type, types.int64])

    def codegen(context, builder, sig, args):
        etsn__bkqrk, = args
        ikjhh__sfq = cgutils.create_struct_proxy(string_type)(context,
            builder, value=etsn__bkqrk)
        cxu__wiaol = cgutils.create_struct_proxy(utf8_str_type)(context,
            builder)
        iqhi__nbj = cgutils.create_struct_proxy(fniuq__yufc)(context, builder)
        is_ascii = builder.icmp_unsigned('==', ikjhh__sfq.is_ascii, lir.
            Constant(ikjhh__sfq.is_ascii.type, 1))
        with builder.if_else(is_ascii) as (vdvbr__uhzb, hbhz__tlqbe):
            with vdvbr__uhzb:
                context.nrt.incref(builder, string_type, etsn__bkqrk)
                cxu__wiaol.data = ikjhh__sfq.data
                cxu__wiaol.meminfo = ikjhh__sfq.meminfo
                iqhi__nbj.f1 = ikjhh__sfq.length
            with hbhz__tlqbe:
                qehbm__rpzf = lir.FunctionType(lir.IntType(64), [lir.
                    IntType(8).as_pointer(), lir.IntType(8).as_pointer(),
                    lir.IntType(64), lir.IntType(32)])
                qpm__vklpp = cgutils.get_or_insert_function(builder.module,
                    qehbm__rpzf, name='unicode_to_utf8')
                zmf__nbsjh = context.get_constant_null(types.voidptr)
                bvikg__gsb = builder.call(qpm__vklpp, [zmf__nbsjh,
                    ikjhh__sfq.data, ikjhh__sfq.length, ikjhh__sfq.kind])
                iqhi__nbj.f1 = bvikg__gsb
                mul__vvm = builder.add(bvikg__gsb, lir.Constant(lir.IntType
                    (64), 1))
                cxu__wiaol.meminfo = context.nrt.meminfo_alloc_aligned(builder,
                    size=mul__vvm, align=32)
                cxu__wiaol.data = context.nrt.meminfo_data(builder,
                    cxu__wiaol.meminfo)
                builder.call(qpm__vklpp, [cxu__wiaol.data, ikjhh__sfq.data,
                    ikjhh__sfq.length, ikjhh__sfq.kind])
                builder.store(lir.Constant(lir.IntType(8), 0), builder.gep(
                    cxu__wiaol.data, [bvikg__gsb]))
        iqhi__nbj.f0 = cxu__wiaol._getvalue()
        return iqhi__nbj._getvalue()
    return fniuq__yufc(string_type), codegen


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
        qehbm__rpzf = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
        apl__tjgmb = cgutils.get_or_insert_function(builder.module,
            qehbm__rpzf, name='memcmp')
        return builder.call(apl__tjgmb, args)
    return types.int32(types.voidptr, types.voidptr, types.intp), codegen


def int_to_str_len(n):
    return len(str(n))


@overload(int_to_str_len)
def overload_int_to_str_len(n):
    pgr__dvxy = n(10)

    def impl(n):
        if n == 0:
            return 1
        sfs__lkz = 0
        if n < 0:
            n = -n
            sfs__lkz += 1
        while n > 0:
            n = n // pgr__dvxy
            sfs__lkz += 1
        return sfs__lkz
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
        [tgl__wkz] = args
        if isinstance(tgl__wkz, StdStringType):
            return signature(types.float64, tgl__wkz)
        if tgl__wkz == string_type:
            return signature(types.float64, tgl__wkz)


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
    ikjhh__sfq = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    qehbm__rpzf = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer(), lir.IntType(64)])
    yvred__ghd = cgutils.get_or_insert_function(builder.module, qehbm__rpzf,
        name='init_string_const')
    return builder.call(yvred__ghd, [ikjhh__sfq.data, ikjhh__sfq.length])


def gen_std_str_to_unicode(context, builder, std_str_val, del_str=False):
    kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def _std_str_to_unicode(std_str):
        length = bodo.libs.str_ext.get_std_str_len(std_str)
        xmdv__smb = numba.cpython.unicode._empty_string(kind, length, 1)
        bodo.libs.str_arr_ext._memcpy(xmdv__smb._data, bodo.libs.str_ext.
            get_c_str(std_str), length, 1)
        if del_str:
            bodo.libs.str_ext.del_str(std_str)
        return xmdv__smb
    val = context.compile_internal(builder, _std_str_to_unicode,
        string_type(bodo.libs.str_ext.std_str_type), [std_str_val])
    return val


def gen_get_unicode_chars(context, builder, unicode_val):
    ikjhh__sfq = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    return ikjhh__sfq.data


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
        kleaj__rvar = [('data', types.List(string_type))]
        models.StructModel.__init__(self, dmm, fe_type, kleaj__rvar)


make_attribute_wrapper(RandomAccessStringArrayType, 'data', '_data')


@intrinsic
def alloc_random_access_string_array(typingctx, n_t=None):

    def codegen(context, builder, sig, args):
        yfsm__hmum, = args
        sjay__diyq = types.List(string_type)
        oes__preh = numba.cpython.listobj.ListInstance.allocate(context,
            builder, sjay__diyq, yfsm__hmum)
        oes__preh.size = yfsm__hmum
        twss__fhi = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        twss__fhi.data = oes__preh.value
        return twss__fhi._getvalue()
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
            psrv__zrpfl = 0
            cqq__rlc = v
            if cqq__rlc < 0:
                psrv__zrpfl = 1
                cqq__rlc = -cqq__rlc
            if cqq__rlc < 1:
                ldp__phb = 1
            else:
                ldp__phb = 1 + int(np.floor(np.log10(cqq__rlc)))
            length = psrv__zrpfl + ldp__phb + 1 + 6
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
    qehbm__rpzf = lir.FunctionType(lir.DoubleType(), [lir.IntType(8).
        as_pointer()])
    yvred__ghd = cgutils.get_or_insert_function(builder.module, qehbm__rpzf,
        name='str_to_float64')
    res = builder.call(yvred__ghd, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(StdStringType, types.float32)
def cast_str_to_float32(context, builder, fromty, toty, val):
    qehbm__rpzf = lir.FunctionType(lir.FloatType(), [lir.IntType(8).
        as_pointer()])
    yvred__ghd = cgutils.get_or_insert_function(builder.module, qehbm__rpzf,
        name='str_to_float32')
    res = builder.call(yvred__ghd, (val,))
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
    ikjhh__sfq = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    qehbm__rpzf = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType
        (8).as_pointer(), lir.IntType(64)])
    yvred__ghd = cgutils.get_or_insert_function(builder.module, qehbm__rpzf,
        name='str_to_int64')
    res = builder.call(yvred__ghd, (ikjhh__sfq.data, ikjhh__sfq.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.uint64)
@lower_cast(string_type, types.uint32)
@lower_cast(string_type, types.uint16)
@lower_cast(string_type, types.uint8)
def cast_unicode_str_to_uint64(context, builder, fromty, toty, val):
    ikjhh__sfq = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    qehbm__rpzf = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType
        (8).as_pointer(), lir.IntType(64)])
    yvred__ghd = cgutils.get_or_insert_function(builder.module, qehbm__rpzf,
        name='str_to_uint64')
    res = builder.call(yvred__ghd, (ikjhh__sfq.data, ikjhh__sfq.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@infer_getattr
class StringAttribute(AttributeTemplate):
    key = types.UnicodeType

    @bound_function('str.format', no_unliteral=True)
    def resolve_format(self, string_typ, args, kws):
        kws = dict(kws)
        nqq__uyhv = ', '.join('e{}'.format(qmaa__tigw) for qmaa__tigw in
            range(len(args)))
        if nqq__uyhv:
            nqq__uyhv += ', '
        envxc__pxn = ', '.join("{} = ''".format(a) for a in kws.keys())
        epok__rqg = f'def format_stub(string, {nqq__uyhv} {envxc__pxn}):\n'
        epok__rqg += '    pass\n'
        taf__tkkpw = {}
        exec(epok__rqg, {}, taf__tkkpw)
        igmp__udneg = taf__tkkpw['format_stub']
        jomi__kjo = numba.core.utils.pysignature(igmp__udneg)
        xgnrx__lir = (string_typ,) + args + tuple(kws.values())
        return signature(string_typ, xgnrx__lir).replace(pysig=jomi__kjo)


@numba.njit(cache=True)
def str_split(arr, pat, n):
    nzobu__zvpfl = pat is not None and len(pat) > 1
    if nzobu__zvpfl:
        rzr__uvsp = re.compile(pat)
        if n == -1:
            n = 0
    elif n == 0:
        n = -1
    oes__preh = len(arr)
    pagl__hzk = 0
    bquut__sogt = 0
    for qmaa__tigw in numba.parfors.parfor.internal_prange(oes__preh):
        if bodo.libs.array_kernels.isna(arr, qmaa__tigw):
            continue
        if nzobu__zvpfl:
            kxoj__qni = rzr__uvsp.split(arr[qmaa__tigw], maxsplit=n)
        elif pat == '':
            kxoj__qni = [''] + list(arr[qmaa__tigw]) + ['']
        else:
            kxoj__qni = arr[qmaa__tigw].split(pat, n)
        pagl__hzk += len(kxoj__qni)
        for s in kxoj__qni:
            bquut__sogt += bodo.libs.str_arr_ext.get_utf8_size(s)
    yeij__zpoe = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        oes__preh, (pagl__hzk, bquut__sogt), bodo.libs.str_arr_ext.
        string_array_type)
    imb__awlav = bodo.libs.array_item_arr_ext.get_offsets(yeij__zpoe)
    xmu__shemw = bodo.libs.array_item_arr_ext.get_null_bitmap(yeij__zpoe)
    ckw__ibnm = bodo.libs.array_item_arr_ext.get_data(yeij__zpoe)
    zmzju__gddd = 0
    for oit__qbbhc in numba.parfors.parfor.internal_prange(oes__preh):
        imb__awlav[oit__qbbhc] = zmzju__gddd
        if bodo.libs.array_kernels.isna(arr, oit__qbbhc):
            bodo.libs.int_arr_ext.set_bit_to_arr(xmu__shemw, oit__qbbhc, 0)
            continue
        bodo.libs.int_arr_ext.set_bit_to_arr(xmu__shemw, oit__qbbhc, 1)
        if nzobu__zvpfl:
            kxoj__qni = rzr__uvsp.split(arr[oit__qbbhc], maxsplit=n)
        elif pat == '':
            kxoj__qni = [''] + list(arr[oit__qbbhc]) + ['']
        else:
            kxoj__qni = arr[oit__qbbhc].split(pat, n)
        jxxq__emxlp = len(kxoj__qni)
        for lapx__uph in range(jxxq__emxlp):
            s = kxoj__qni[lapx__uph]
            ckw__ibnm[zmzju__gddd] = s
            zmzju__gddd += 1
    imb__awlav[oes__preh] = zmzju__gddd
    return yeij__zpoe


@overload(hex)
def overload_hex(x):
    if isinstance(x, types.Integer):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(x):
            x = np.int64(x)
            if x < 0:
                ujxl__jzbfh = '-0x'
                x = x * -1
            else:
                ujxl__jzbfh = '0x'
            x = np.uint64(x)
            if x == 0:
                ewgio__pxf = 1
            else:
                ewgio__pxf = fast_ceil_log2(x + 1)
                ewgio__pxf = (ewgio__pxf + 3) // 4
            length = len(ujxl__jzbfh) + ewgio__pxf
            output = numba.cpython.unicode._empty_string(kind, length, 1)
            bodo.libs.str_arr_ext._memcpy(output._data, ujxl__jzbfh._data,
                len(ujxl__jzbfh), 1)
            int_to_hex(output, ewgio__pxf, len(ujxl__jzbfh), x)
            return output
        return impl


@register_jitable
def fast_ceil_log2(x):
    lvhgu__rgvls = 0 if x & x - 1 == 0 else 1
    wrmwi__eipu = [np.uint64(18446744069414584320), np.uint64(4294901760),
        np.uint64(65280), np.uint64(240), np.uint64(12), np.uint64(2)]
    otwf__pfnc = 32
    for qmaa__tigw in range(len(wrmwi__eipu)):
        oyrkx__lhum = 0 if x & wrmwi__eipu[qmaa__tigw] == 0 else otwf__pfnc
        lvhgu__rgvls = lvhgu__rgvls + oyrkx__lhum
        x = x >> oyrkx__lhum
        otwf__pfnc = otwf__pfnc >> 1
    return lvhgu__rgvls


@intrinsic
def int_to_hex(typingctx, output, out_len, header_len, int_val):

    def codegen(context, builder, sig, args):
        output, out_len, header_len, int_val = args
        ylxax__wdegv = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=output)
        qehbm__rpzf = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(64)])
        hmyf__zllqs = cgutils.get_or_insert_function(builder.module,
            qehbm__rpzf, name='int_to_hex')
        alc__ppyy = builder.inttoptr(builder.add(builder.ptrtoint(
            ylxax__wdegv.data, lir.IntType(64)), header_len), lir.IntType(8
            ).as_pointer())
        builder.call(hmyf__zllqs, (alc__ppyy, out_len, int_val))
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
