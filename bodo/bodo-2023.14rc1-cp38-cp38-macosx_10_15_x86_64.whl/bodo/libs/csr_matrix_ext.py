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
        zuaz__udpq = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, zuaz__udpq)


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
        mfkuf__ificj, tjug__fmof, lrmuc__hax, vysl__onrd = args
        dpp__hlb = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        dpp__hlb.data = mfkuf__ificj
        dpp__hlb.indices = tjug__fmof
        dpp__hlb.indptr = lrmuc__hax
        dpp__hlb.shape = vysl__onrd
        context.nrt.incref(builder, signature.args[0], mfkuf__ificj)
        context.nrt.incref(builder, signature.args[1], tjug__fmof)
        context.nrt.incref(builder, signature.args[2], lrmuc__hax)
        return dpp__hlb._getvalue()
    uqvkk__jlj = CSRMatrixType(data_t.dtype, indices_t.dtype)
    wqqzu__ukkdw = uqvkk__jlj(data_t, indices_t, indptr_t, types.UniTuple(
        types.int64, 2))
    return wqqzu__ukkdw, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    dpp__hlb = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ulaly__pnr = c.pyapi.object_getattr_string(val, 'data')
    rps__gxj = c.pyapi.object_getattr_string(val, 'indices')
    nbz__nufy = c.pyapi.object_getattr_string(val, 'indptr')
    hqfua__zgwlg = c.pyapi.object_getattr_string(val, 'shape')
    dpp__hlb.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1, 'C'),
        ulaly__pnr).value
    dpp__hlb.indices = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 1,
        'C'), rps__gxj).value
    dpp__hlb.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 1,
        'C'), nbz__nufy).value
    dpp__hlb.shape = c.pyapi.to_native_value(types.UniTuple(types.int64, 2),
        hqfua__zgwlg).value
    c.pyapi.decref(ulaly__pnr)
    c.pyapi.decref(rps__gxj)
    c.pyapi.decref(nbz__nufy)
    c.pyapi.decref(hqfua__zgwlg)
    flh__qqw = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(dpp__hlb._getvalue(), is_error=flh__qqw)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    mpny__wqw = c.context.insert_const_string(c.builder.module, 'scipy.sparse')
    xchkl__zqcu = c.pyapi.import_module_noblock(mpny__wqw)
    dpp__hlb = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        dpp__hlb.data)
    ulaly__pnr = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        dpp__hlb.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        dpp__hlb.indices)
    rps__gxj = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'),
        dpp__hlb.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        dpp__hlb.indptr)
    nbz__nufy = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'
        ), dpp__hlb.indptr, c.env_manager)
    hqfua__zgwlg = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        dpp__hlb.shape, c.env_manager)
    ruyko__vksm = c.pyapi.tuple_pack([ulaly__pnr, rps__gxj, nbz__nufy])
    wmqp__wfsg = c.pyapi.call_method(xchkl__zqcu, 'csr_matrix', (
        ruyko__vksm, hqfua__zgwlg))
    c.pyapi.decref(ruyko__vksm)
    c.pyapi.decref(ulaly__pnr)
    c.pyapi.decref(rps__gxj)
    c.pyapi.decref(nbz__nufy)
    c.pyapi.decref(hqfua__zgwlg)
    c.pyapi.decref(xchkl__zqcu)
    c.context.nrt.decref(c.builder, typ, val)
    return wmqp__wfsg


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
    nkx__nwrn = A.dtype
    cecre__omgqq = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            nucii__ormy, ixe__jkwhi = A.shape
            dutl__olbw = numba.cpython.unicode._normalize_slice(idx[0],
                nucii__ormy)
            rin__kiy = numba.cpython.unicode._normalize_slice(idx[1],
                ixe__jkwhi)
            if dutl__olbw.step != 1 or rin__kiy.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            sbxc__xjh = dutl__olbw.start
            fxxrq__ymr = dutl__olbw.stop
            pzl__etj = rin__kiy.start
            cytke__tbyt = rin__kiy.stop
            vnxz__ifgf = A.indptr
            vrs__ncvm = A.indices
            jbco__olcbf = A.data
            ltyu__fen = fxxrq__ymr - sbxc__xjh
            awig__sid = cytke__tbyt - pzl__etj
            fjnd__cfa = 0
            sajqb__rsf = 0
            for budv__phpx in range(ltyu__fen):
                kdv__rvbt = vnxz__ifgf[sbxc__xjh + budv__phpx]
                yno__nkdx = vnxz__ifgf[sbxc__xjh + budv__phpx + 1]
                for ncka__afvv in range(kdv__rvbt, yno__nkdx):
                    if vrs__ncvm[ncka__afvv] >= pzl__etj and vrs__ncvm[
                        ncka__afvv] < cytke__tbyt:
                        fjnd__cfa += 1
            jbx__cfco = np.empty(ltyu__fen + 1, cecre__omgqq)
            nhll__rmmlo = np.empty(fjnd__cfa, cecre__omgqq)
            malir__ejk = np.empty(fjnd__cfa, nkx__nwrn)
            jbx__cfco[0] = 0
            for budv__phpx in range(ltyu__fen):
                kdv__rvbt = vnxz__ifgf[sbxc__xjh + budv__phpx]
                yno__nkdx = vnxz__ifgf[sbxc__xjh + budv__phpx + 1]
                for ncka__afvv in range(kdv__rvbt, yno__nkdx):
                    if vrs__ncvm[ncka__afvv] >= pzl__etj and vrs__ncvm[
                        ncka__afvv] < cytke__tbyt:
                        nhll__rmmlo[sajqb__rsf] = vrs__ncvm[ncka__afvv
                            ] - pzl__etj
                        malir__ejk[sajqb__rsf] = jbco__olcbf[ncka__afvv]
                        sajqb__rsf += 1
                jbx__cfco[budv__phpx + 1] = sajqb__rsf
            return init_csr_matrix(malir__ejk, nhll__rmmlo, jbx__cfco, (
                ltyu__fen, awig__sid))
        return impl
    elif isinstance(idx, types.Array
        ) and idx.ndim == 1 and idx.dtype == cecre__omgqq:

        def impl(A, idx):
            nucii__ormy, ixe__jkwhi = A.shape
            vnxz__ifgf = A.indptr
            vrs__ncvm = A.indices
            jbco__olcbf = A.data
            ltyu__fen = len(idx)
            fjnd__cfa = 0
            sajqb__rsf = 0
            for budv__phpx in range(ltyu__fen):
                wss__bdcs = idx[budv__phpx]
                kdv__rvbt = vnxz__ifgf[wss__bdcs]
                yno__nkdx = vnxz__ifgf[wss__bdcs + 1]
                fjnd__cfa += yno__nkdx - kdv__rvbt
            jbx__cfco = np.empty(ltyu__fen + 1, cecre__omgqq)
            nhll__rmmlo = np.empty(fjnd__cfa, cecre__omgqq)
            malir__ejk = np.empty(fjnd__cfa, nkx__nwrn)
            jbx__cfco[0] = 0
            for budv__phpx in range(ltyu__fen):
                wss__bdcs = idx[budv__phpx]
                kdv__rvbt = vnxz__ifgf[wss__bdcs]
                yno__nkdx = vnxz__ifgf[wss__bdcs + 1]
                nhll__rmmlo[sajqb__rsf:sajqb__rsf + yno__nkdx - kdv__rvbt
                    ] = vrs__ncvm[kdv__rvbt:yno__nkdx]
                malir__ejk[sajqb__rsf:sajqb__rsf + yno__nkdx - kdv__rvbt
                    ] = jbco__olcbf[kdv__rvbt:yno__nkdx]
                sajqb__rsf += yno__nkdx - kdv__rvbt
                jbx__cfco[budv__phpx + 1] = sajqb__rsf
            bkw__ojuky = init_csr_matrix(malir__ejk, nhll__rmmlo, jbx__cfco,
                (ltyu__fen, ixe__jkwhi))
            return bkw__ojuky
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
