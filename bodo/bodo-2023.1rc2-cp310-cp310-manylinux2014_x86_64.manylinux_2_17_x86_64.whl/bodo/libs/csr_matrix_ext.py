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
        wvz__hcndu = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, wvz__hcndu)


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
        gjqhe__ilrme, zumy__kps, xjl__qlrvw, jfz__rltry = args
        hmz__asuli = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        hmz__asuli.data = gjqhe__ilrme
        hmz__asuli.indices = zumy__kps
        hmz__asuli.indptr = xjl__qlrvw
        hmz__asuli.shape = jfz__rltry
        context.nrt.incref(builder, signature.args[0], gjqhe__ilrme)
        context.nrt.incref(builder, signature.args[1], zumy__kps)
        context.nrt.incref(builder, signature.args[2], xjl__qlrvw)
        return hmz__asuli._getvalue()
    tao__vbtw = CSRMatrixType(data_t.dtype, indices_t.dtype)
    pfqti__fvtka = tao__vbtw(data_t, indices_t, indptr_t, types.UniTuple(
        types.int64, 2))
    return pfqti__fvtka, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    hmz__asuli = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ilzb__okbgj = c.pyapi.object_getattr_string(val, 'data')
    nhkf__hne = c.pyapi.object_getattr_string(val, 'indices')
    tfov__klz = c.pyapi.object_getattr_string(val, 'indptr')
    eli__ceycr = c.pyapi.object_getattr_string(val, 'shape')
    hmz__asuli.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1, 'C'
        ), ilzb__okbgj).value
    hmz__asuli.indices = c.pyapi.to_native_value(types.Array(typ.idx_dtype,
        1, 'C'), nhkf__hne).value
    hmz__asuli.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 
        1, 'C'), tfov__klz).value
    hmz__asuli.shape = c.pyapi.to_native_value(types.UniTuple(types.int64, 
        2), eli__ceycr).value
    c.pyapi.decref(ilzb__okbgj)
    c.pyapi.decref(nhkf__hne)
    c.pyapi.decref(tfov__klz)
    c.pyapi.decref(eli__ceycr)
    jzk__dld = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(hmz__asuli._getvalue(), is_error=jzk__dld)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    ludnf__wvrp = c.context.insert_const_string(c.builder.module,
        'scipy.sparse')
    haf__sndjo = c.pyapi.import_module_noblock(ludnf__wvrp)
    hmz__asuli = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        hmz__asuli.data)
    ilzb__okbgj = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        hmz__asuli.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        hmz__asuli.indices)
    nhkf__hne = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'
        ), hmz__asuli.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        hmz__asuli.indptr)
    tfov__klz = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'
        ), hmz__asuli.indptr, c.env_manager)
    eli__ceycr = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        hmz__asuli.shape, c.env_manager)
    hlsb__kpsc = c.pyapi.tuple_pack([ilzb__okbgj, nhkf__hne, tfov__klz])
    aspao__tkp = c.pyapi.call_method(haf__sndjo, 'csr_matrix', (hlsb__kpsc,
        eli__ceycr))
    c.pyapi.decref(hlsb__kpsc)
    c.pyapi.decref(ilzb__okbgj)
    c.pyapi.decref(nhkf__hne)
    c.pyapi.decref(tfov__klz)
    c.pyapi.decref(eli__ceycr)
    c.pyapi.decref(haf__sndjo)
    c.context.nrt.decref(c.builder, typ, val)
    return aspao__tkp


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
    ogk__zku = A.dtype
    evoig__jci = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            nahnp__qmp, npmn__ufq = A.shape
            kobc__hdmr = numba.cpython.unicode._normalize_slice(idx[0],
                nahnp__qmp)
            vpeoi__crd = numba.cpython.unicode._normalize_slice(idx[1],
                npmn__ufq)
            if kobc__hdmr.step != 1 or vpeoi__crd.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            zhd__wjw = kobc__hdmr.start
            xldz__umzpj = kobc__hdmr.stop
            ufvj__fsbj = vpeoi__crd.start
            oqfe__hjb = vpeoi__crd.stop
            neqz__jmnzo = A.indptr
            aqfss__phjz = A.indices
            piup__jdip = A.data
            wrtig__visa = xldz__umzpj - zhd__wjw
            hepf__ptg = oqfe__hjb - ufvj__fsbj
            msrh__cqr = 0
            isoh__lvy = 0
            for ybqh__jos in range(wrtig__visa):
                nkq__ebfo = neqz__jmnzo[zhd__wjw + ybqh__jos]
                flpcv__zazb = neqz__jmnzo[zhd__wjw + ybqh__jos + 1]
                for ppc__qsmt in range(nkq__ebfo, flpcv__zazb):
                    if aqfss__phjz[ppc__qsmt] >= ufvj__fsbj and aqfss__phjz[
                        ppc__qsmt] < oqfe__hjb:
                        msrh__cqr += 1
            mrsbk__spdj = np.empty(wrtig__visa + 1, evoig__jci)
            fku__rhms = np.empty(msrh__cqr, evoig__jci)
            kim__tgmid = np.empty(msrh__cqr, ogk__zku)
            mrsbk__spdj[0] = 0
            for ybqh__jos in range(wrtig__visa):
                nkq__ebfo = neqz__jmnzo[zhd__wjw + ybqh__jos]
                flpcv__zazb = neqz__jmnzo[zhd__wjw + ybqh__jos + 1]
                for ppc__qsmt in range(nkq__ebfo, flpcv__zazb):
                    if aqfss__phjz[ppc__qsmt] >= ufvj__fsbj and aqfss__phjz[
                        ppc__qsmt] < oqfe__hjb:
                        fku__rhms[isoh__lvy] = aqfss__phjz[ppc__qsmt
                            ] - ufvj__fsbj
                        kim__tgmid[isoh__lvy] = piup__jdip[ppc__qsmt]
                        isoh__lvy += 1
                mrsbk__spdj[ybqh__jos + 1] = isoh__lvy
            return init_csr_matrix(kim__tgmid, fku__rhms, mrsbk__spdj, (
                wrtig__visa, hepf__ptg))
        return impl
    elif isinstance(idx, types.Array
        ) and idx.ndim == 1 and idx.dtype == evoig__jci:

        def impl(A, idx):
            nahnp__qmp, npmn__ufq = A.shape
            neqz__jmnzo = A.indptr
            aqfss__phjz = A.indices
            piup__jdip = A.data
            wrtig__visa = len(idx)
            msrh__cqr = 0
            isoh__lvy = 0
            for ybqh__jos in range(wrtig__visa):
                yowou__zhkd = idx[ybqh__jos]
                nkq__ebfo = neqz__jmnzo[yowou__zhkd]
                flpcv__zazb = neqz__jmnzo[yowou__zhkd + 1]
                msrh__cqr += flpcv__zazb - nkq__ebfo
            mrsbk__spdj = np.empty(wrtig__visa + 1, evoig__jci)
            fku__rhms = np.empty(msrh__cqr, evoig__jci)
            kim__tgmid = np.empty(msrh__cqr, ogk__zku)
            mrsbk__spdj[0] = 0
            for ybqh__jos in range(wrtig__visa):
                yowou__zhkd = idx[ybqh__jos]
                nkq__ebfo = neqz__jmnzo[yowou__zhkd]
                flpcv__zazb = neqz__jmnzo[yowou__zhkd + 1]
                fku__rhms[isoh__lvy:isoh__lvy + flpcv__zazb - nkq__ebfo
                    ] = aqfss__phjz[nkq__ebfo:flpcv__zazb]
                kim__tgmid[isoh__lvy:isoh__lvy + flpcv__zazb - nkq__ebfo
                    ] = piup__jdip[nkq__ebfo:flpcv__zazb]
                isoh__lvy += flpcv__zazb - nkq__ebfo
                mrsbk__spdj[ybqh__jos + 1] = isoh__lvy
            jnnv__jcxrn = init_csr_matrix(kim__tgmid, fku__rhms,
                mrsbk__spdj, (wrtig__visa, npmn__ufq))
            return jnnv__jcxrn
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
