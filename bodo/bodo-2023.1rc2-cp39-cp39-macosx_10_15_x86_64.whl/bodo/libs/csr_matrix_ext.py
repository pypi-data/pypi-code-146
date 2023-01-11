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
        gqshd__fbafn = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, gqshd__fbafn)


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
        vmqy__clz, cyq__bfu, xxfw__gcn, kdb__mgjw = args
        jjyu__bslho = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        jjyu__bslho.data = vmqy__clz
        jjyu__bslho.indices = cyq__bfu
        jjyu__bslho.indptr = xxfw__gcn
        jjyu__bslho.shape = kdb__mgjw
        context.nrt.incref(builder, signature.args[0], vmqy__clz)
        context.nrt.incref(builder, signature.args[1], cyq__bfu)
        context.nrt.incref(builder, signature.args[2], xxfw__gcn)
        return jjyu__bslho._getvalue()
    qoz__udh = CSRMatrixType(data_t.dtype, indices_t.dtype)
    ucx__plz = qoz__udh(data_t, indices_t, indptr_t, types.UniTuple(types.
        int64, 2))
    return ucx__plz, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    jjyu__bslho = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    tft__txgmj = c.pyapi.object_getattr_string(val, 'data')
    ukcoi__sykn = c.pyapi.object_getattr_string(val, 'indices')
    cfyf__jkbv = c.pyapi.object_getattr_string(val, 'indptr')
    mig__yekt = c.pyapi.object_getattr_string(val, 'shape')
    jjyu__bslho.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1,
        'C'), tft__txgmj).value
    jjyu__bslho.indices = c.pyapi.to_native_value(types.Array(typ.idx_dtype,
        1, 'C'), ukcoi__sykn).value
    jjyu__bslho.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype,
        1, 'C'), cfyf__jkbv).value
    jjyu__bslho.shape = c.pyapi.to_native_value(types.UniTuple(types.int64,
        2), mig__yekt).value
    c.pyapi.decref(tft__txgmj)
    c.pyapi.decref(ukcoi__sykn)
    c.pyapi.decref(cfyf__jkbv)
    c.pyapi.decref(mig__yekt)
    ulxd__fxyo = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(jjyu__bslho._getvalue(), is_error=ulxd__fxyo)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    xyphy__rkvf = c.context.insert_const_string(c.builder.module,
        'scipy.sparse')
    gos__ohoe = c.pyapi.import_module_noblock(xyphy__rkvf)
    jjyu__bslho = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        jjyu__bslho.data)
    tft__txgmj = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        jjyu__bslho.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        jjyu__bslho.indices)
    ukcoi__sykn = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), jjyu__bslho.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        jjyu__bslho.indptr)
    cfyf__jkbv = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), jjyu__bslho.indptr, c.env_manager)
    mig__yekt = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        jjyu__bslho.shape, c.env_manager)
    hjd__frr = c.pyapi.tuple_pack([tft__txgmj, ukcoi__sykn, cfyf__jkbv])
    ckapu__wffn = c.pyapi.call_method(gos__ohoe, 'csr_matrix', (hjd__frr,
        mig__yekt))
    c.pyapi.decref(hjd__frr)
    c.pyapi.decref(tft__txgmj)
    c.pyapi.decref(ukcoi__sykn)
    c.pyapi.decref(cfyf__jkbv)
    c.pyapi.decref(mig__yekt)
    c.pyapi.decref(gos__ohoe)
    c.context.nrt.decref(c.builder, typ, val)
    return ckapu__wffn


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
    tkfd__cepd = A.dtype
    yip__beig = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            ozj__tmxy, lkbpq__qcwe = A.shape
            ugqhj__ensvi = numba.cpython.unicode._normalize_slice(idx[0],
                ozj__tmxy)
            chdx__vsd = numba.cpython.unicode._normalize_slice(idx[1],
                lkbpq__qcwe)
            if ugqhj__ensvi.step != 1 or chdx__vsd.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            koq__jqxf = ugqhj__ensvi.start
            gpk__yghxc = ugqhj__ensvi.stop
            nsnq__yrh = chdx__vsd.start
            gga__dprh = chdx__vsd.stop
            hhgp__kbe = A.indptr
            ncif__yyt = A.indices
            lrtfs__xgxtd = A.data
            bab__tcf = gpk__yghxc - koq__jqxf
            vysw__dco = gga__dprh - nsnq__yrh
            njn__bik = 0
            gwovc__gewj = 0
            for agk__lrzw in range(bab__tcf):
                vwzya__xgz = hhgp__kbe[koq__jqxf + agk__lrzw]
                rht__rlre = hhgp__kbe[koq__jqxf + agk__lrzw + 1]
                for cyp__tnepd in range(vwzya__xgz, rht__rlre):
                    if ncif__yyt[cyp__tnepd] >= nsnq__yrh and ncif__yyt[
                        cyp__tnepd] < gga__dprh:
                        njn__bik += 1
            sfksw__lbj = np.empty(bab__tcf + 1, yip__beig)
            tuwhw__xze = np.empty(njn__bik, yip__beig)
            dqiq__tfb = np.empty(njn__bik, tkfd__cepd)
            sfksw__lbj[0] = 0
            for agk__lrzw in range(bab__tcf):
                vwzya__xgz = hhgp__kbe[koq__jqxf + agk__lrzw]
                rht__rlre = hhgp__kbe[koq__jqxf + agk__lrzw + 1]
                for cyp__tnepd in range(vwzya__xgz, rht__rlre):
                    if ncif__yyt[cyp__tnepd] >= nsnq__yrh and ncif__yyt[
                        cyp__tnepd] < gga__dprh:
                        tuwhw__xze[gwovc__gewj] = ncif__yyt[cyp__tnepd
                            ] - nsnq__yrh
                        dqiq__tfb[gwovc__gewj] = lrtfs__xgxtd[cyp__tnepd]
                        gwovc__gewj += 1
                sfksw__lbj[agk__lrzw + 1] = gwovc__gewj
            return init_csr_matrix(dqiq__tfb, tuwhw__xze, sfksw__lbj, (
                bab__tcf, vysw__dco))
        return impl
    elif isinstance(idx, types.Array
        ) and idx.ndim == 1 and idx.dtype == yip__beig:

        def impl(A, idx):
            ozj__tmxy, lkbpq__qcwe = A.shape
            hhgp__kbe = A.indptr
            ncif__yyt = A.indices
            lrtfs__xgxtd = A.data
            bab__tcf = len(idx)
            njn__bik = 0
            gwovc__gewj = 0
            for agk__lrzw in range(bab__tcf):
                ujdcr__avgd = idx[agk__lrzw]
                vwzya__xgz = hhgp__kbe[ujdcr__avgd]
                rht__rlre = hhgp__kbe[ujdcr__avgd + 1]
                njn__bik += rht__rlre - vwzya__xgz
            sfksw__lbj = np.empty(bab__tcf + 1, yip__beig)
            tuwhw__xze = np.empty(njn__bik, yip__beig)
            dqiq__tfb = np.empty(njn__bik, tkfd__cepd)
            sfksw__lbj[0] = 0
            for agk__lrzw in range(bab__tcf):
                ujdcr__avgd = idx[agk__lrzw]
                vwzya__xgz = hhgp__kbe[ujdcr__avgd]
                rht__rlre = hhgp__kbe[ujdcr__avgd + 1]
                tuwhw__xze[gwovc__gewj:gwovc__gewj + rht__rlre - vwzya__xgz
                    ] = ncif__yyt[vwzya__xgz:rht__rlre]
                dqiq__tfb[gwovc__gewj:gwovc__gewj + rht__rlre - vwzya__xgz
                    ] = lrtfs__xgxtd[vwzya__xgz:rht__rlre]
                gwovc__gewj += rht__rlre - vwzya__xgz
                sfksw__lbj[agk__lrzw + 1] = gwovc__gewj
            xfl__oykbe = init_csr_matrix(dqiq__tfb, tuwhw__xze, sfksw__lbj,
                (bab__tcf, lkbpq__qcwe))
            return xfl__oykbe
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
