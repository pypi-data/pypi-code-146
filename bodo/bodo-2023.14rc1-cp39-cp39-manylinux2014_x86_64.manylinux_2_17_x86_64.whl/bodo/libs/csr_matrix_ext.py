"""CSR Matrix data type implementation for scipy.sparse.csr_matrix
"""
import operator
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
import bodo
from bodo.utils.typing import BodoError


class CSRMatrixType(types.ArrayCompatible):
    ndim = 2

    def __init__(self, dtype, idx_dtype):
        self.dtype = dtype
        self.idx_dtype = idx_dtype
        super(CSRMatrixType, self).__init__(name=
            f'CSRMatrixType({dtype}, {idx_dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    def copy(self):
        return CSRMatrixType(self.dtype, self.idx_dtype)


@register_model(CSRMatrixType)
class CSRMatrixModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ifqth__wsqki = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, ifqth__wsqki)


make_attribute_wrapper(CSRMatrixType, 'data', 'data')
make_attribute_wrapper(CSRMatrixType, 'indices', 'indices')
make_attribute_wrapper(CSRMatrixType, 'indptr', 'indptr')
make_attribute_wrapper(CSRMatrixType, 'shape', 'shape')


@intrinsic
def init_csr_matrix(typingctx, data_t, indices_t, indptr_t, shape_t=None):
    assert isinstance(data_t, types.Array)
    assert isinstance(indices_t, types.Array) and isinstance(indices_t.
        dtype, types.Integer)
    assert indices_t == indptr_t

    def codegen(context, builder, signature, args):
        egpsp__xzna, eou__qck, bipm__ehf, xbtn__rjfjb = args
        fyz__nczc = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        fyz__nczc.data = egpsp__xzna
        fyz__nczc.indices = eou__qck
        fyz__nczc.indptr = bipm__ehf
        fyz__nczc.shape = xbtn__rjfjb
        context.nrt.incref(builder, signature.args[0], egpsp__xzna)
        context.nrt.incref(builder, signature.args[1], eou__qck)
        context.nrt.incref(builder, signature.args[2], bipm__ehf)
        return fyz__nczc._getvalue()
    bjb__poy = CSRMatrixType(data_t.dtype, indices_t.dtype)
    zca__lgfoj = bjb__poy(data_t, indices_t, indptr_t, types.UniTuple(types
        .int64, 2))
    return zca__lgfoj, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    fyz__nczc = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    wzhbm__kacl = c.pyapi.object_getattr_string(val, 'data')
    ymq__ejdo = c.pyapi.object_getattr_string(val, 'indices')
    zqr__yjtz = c.pyapi.object_getattr_string(val, 'indptr')
    jduh__vbp = c.pyapi.object_getattr_string(val, 'shape')
    fyz__nczc.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1, 'C'),
        wzhbm__kacl).value
    fyz__nczc.indices = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 
        1, 'C'), ymq__ejdo).value
    fyz__nczc.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 1,
        'C'), zqr__yjtz).value
    fyz__nczc.shape = c.pyapi.to_native_value(types.UniTuple(types.int64, 2
        ), jduh__vbp).value
    c.pyapi.decref(wzhbm__kacl)
    c.pyapi.decref(ymq__ejdo)
    c.pyapi.decref(zqr__yjtz)
    c.pyapi.decref(jduh__vbp)
    mbjs__dbsow = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(fyz__nczc._getvalue(), is_error=mbjs__dbsow)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    rhx__uqv = c.context.insert_const_string(c.builder.module, 'scipy.sparse')
    dsoqf__xwk = c.pyapi.import_module_noblock(rhx__uqv)
    fyz__nczc = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        fyz__nczc.data)
    wzhbm__kacl = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        fyz__nczc.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        fyz__nczc.indices)
    ymq__ejdo = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'
        ), fyz__nczc.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        fyz__nczc.indptr)
    zqr__yjtz = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'
        ), fyz__nczc.indptr, c.env_manager)
    jduh__vbp = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        fyz__nczc.shape, c.env_manager)
    cuhl__dqrq = c.pyapi.tuple_pack([wzhbm__kacl, ymq__ejdo, zqr__yjtz])
    awcbr__ymah = c.pyapi.call_method(dsoqf__xwk, 'csr_matrix', (cuhl__dqrq,
        jduh__vbp))
    c.pyapi.decref(cuhl__dqrq)
    c.pyapi.decref(wzhbm__kacl)
    c.pyapi.decref(ymq__ejdo)
    c.pyapi.decref(zqr__yjtz)
    c.pyapi.decref(jduh__vbp)
    c.pyapi.decref(dsoqf__xwk)
    c.context.nrt.decref(c.builder, typ, val)
    return awcbr__ymah


@overload(len, no_unliteral=True)
def overload_csr_matrix_len(A):
    if isinstance(A, CSRMatrixType):
        return lambda A: A.shape[0]


@overload_attribute(CSRMatrixType, 'ndim')
def overload_csr_matrix_ndim(A):
    return lambda A: 2


@overload_method(CSRMatrixType, 'copy', no_unliteral=True)
def overload_csr_matrix_copy(A):

    def copy_impl(A):
        return init_csr_matrix(A.data.copy(), A.indices.copy(), A.indptr.
            copy(), A.shape)
    return copy_impl


@overload(operator.getitem, no_unliteral=True)
def csr_matrix_getitem(A, idx):
    if not isinstance(A, CSRMatrixType):
        return
    zpe__dvwfv = A.dtype
    ysxi__yyg = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            aqt__qykw, dqdak__tenoe = A.shape
            ujyis__bxhy = numba.cpython.unicode._normalize_slice(idx[0],
                aqt__qykw)
            hjcj__engr = numba.cpython.unicode._normalize_slice(idx[1],
                dqdak__tenoe)
            if ujyis__bxhy.step != 1 or hjcj__engr.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            jaonn__paaq = ujyis__bxhy.start
            ngd__alhkz = ujyis__bxhy.stop
            tugx__isiq = hjcj__engr.start
            dvq__vqp = hjcj__engr.stop
            lui__bagx = A.indptr
            plh__phzkr = A.indices
            ymyn__olzrz = A.data
            xqkz__afev = ngd__alhkz - jaonn__paaq
            fkuy__ykg = dvq__vqp - tugx__isiq
            aak__ijp = 0
            yjb__ydvxt = 0
            for oyal__fjriv in range(xqkz__afev):
                ono__efbcf = lui__bagx[jaonn__paaq + oyal__fjriv]
                sxbms__qcjjx = lui__bagx[jaonn__paaq + oyal__fjriv + 1]
                for wfa__mkleu in range(ono__efbcf, sxbms__qcjjx):
                    if plh__phzkr[wfa__mkleu] >= tugx__isiq and plh__phzkr[
                        wfa__mkleu] < dvq__vqp:
                        aak__ijp += 1
            wqpa__bykfn = np.empty(xqkz__afev + 1, ysxi__yyg)
            fpmk__jbfpv = np.empty(aak__ijp, ysxi__yyg)
            fzxb__srcoa = np.empty(aak__ijp, zpe__dvwfv)
            wqpa__bykfn[0] = 0
            for oyal__fjriv in range(xqkz__afev):
                ono__efbcf = lui__bagx[jaonn__paaq + oyal__fjriv]
                sxbms__qcjjx = lui__bagx[jaonn__paaq + oyal__fjriv + 1]
                for wfa__mkleu in range(ono__efbcf, sxbms__qcjjx):
                    if plh__phzkr[wfa__mkleu] >= tugx__isiq and plh__phzkr[
                        wfa__mkleu] < dvq__vqp:
                        fpmk__jbfpv[yjb__ydvxt] = plh__phzkr[wfa__mkleu
                            ] - tugx__isiq
                        fzxb__srcoa[yjb__ydvxt] = ymyn__olzrz[wfa__mkleu]
                        yjb__ydvxt += 1
                wqpa__bykfn[oyal__fjriv + 1] = yjb__ydvxt
            return init_csr_matrix(fzxb__srcoa, fpmk__jbfpv, wqpa__bykfn, (
                xqkz__afev, fkuy__ykg))
        return impl
    elif isinstance(idx, types.Array
        ) and idx.ndim == 1 and idx.dtype == ysxi__yyg:

        def impl(A, idx):
            aqt__qykw, dqdak__tenoe = A.shape
            lui__bagx = A.indptr
            plh__phzkr = A.indices
            ymyn__olzrz = A.data
            xqkz__afev = len(idx)
            aak__ijp = 0
            yjb__ydvxt = 0
            for oyal__fjriv in range(xqkz__afev):
                yml__xjoi = idx[oyal__fjriv]
                ono__efbcf = lui__bagx[yml__xjoi]
                sxbms__qcjjx = lui__bagx[yml__xjoi + 1]
                aak__ijp += sxbms__qcjjx - ono__efbcf
            wqpa__bykfn = np.empty(xqkz__afev + 1, ysxi__yyg)
            fpmk__jbfpv = np.empty(aak__ijp, ysxi__yyg)
            fzxb__srcoa = np.empty(aak__ijp, zpe__dvwfv)
            wqpa__bykfn[0] = 0
            for oyal__fjriv in range(xqkz__afev):
                yml__xjoi = idx[oyal__fjriv]
                ono__efbcf = lui__bagx[yml__xjoi]
                sxbms__qcjjx = lui__bagx[yml__xjoi + 1]
                fpmk__jbfpv[yjb__ydvxt:yjb__ydvxt + sxbms__qcjjx - ono__efbcf
                    ] = plh__phzkr[ono__efbcf:sxbms__qcjjx]
                fzxb__srcoa[yjb__ydvxt:yjb__ydvxt + sxbms__qcjjx - ono__efbcf
                    ] = ymyn__olzrz[ono__efbcf:sxbms__qcjjx]
                yjb__ydvxt += sxbms__qcjjx - ono__efbcf
                wqpa__bykfn[oyal__fjriv + 1] = yjb__ydvxt
            tdkq__piq = init_csr_matrix(fzxb__srcoa, fpmk__jbfpv,
                wqpa__bykfn, (xqkz__afev, dqdak__tenoe))
            return tdkq__piq
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
