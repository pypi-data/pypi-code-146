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
        pkl__lag = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, pkl__lag)


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
        ojs__jbcl, rvq__atkl, ckka__lzxmm, lbfhs__nypz = args
        xuzfk__bnjz = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        xuzfk__bnjz.data = ojs__jbcl
        xuzfk__bnjz.indices = rvq__atkl
        xuzfk__bnjz.indptr = ckka__lzxmm
        xuzfk__bnjz.shape = lbfhs__nypz
        context.nrt.incref(builder, signature.args[0], ojs__jbcl)
        context.nrt.incref(builder, signature.args[1], rvq__atkl)
        context.nrt.incref(builder, signature.args[2], ckka__lzxmm)
        return xuzfk__bnjz._getvalue()
    tdkl__tstmq = CSRMatrixType(data_t.dtype, indices_t.dtype)
    uoc__qkudg = tdkl__tstmq(data_t, indices_t, indptr_t, types.UniTuple(
        types.int64, 2))
    return uoc__qkudg, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    xuzfk__bnjz = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    ooptx__onwnb = c.pyapi.object_getattr_string(val, 'data')
    xsflc__ocw = c.pyapi.object_getattr_string(val, 'indices')
    fzvn__yijqs = c.pyapi.object_getattr_string(val, 'indptr')
    zmnst__ciqma = c.pyapi.object_getattr_string(val, 'shape')
    xuzfk__bnjz.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1,
        'C'), ooptx__onwnb).value
    xuzfk__bnjz.indices = c.pyapi.to_native_value(types.Array(typ.idx_dtype,
        1, 'C'), xsflc__ocw).value
    xuzfk__bnjz.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype,
        1, 'C'), fzvn__yijqs).value
    xuzfk__bnjz.shape = c.pyapi.to_native_value(types.UniTuple(types.int64,
        2), zmnst__ciqma).value
    c.pyapi.decref(ooptx__onwnb)
    c.pyapi.decref(xsflc__ocw)
    c.pyapi.decref(fzvn__yijqs)
    c.pyapi.decref(zmnst__ciqma)
    hkip__rdv = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(xuzfk__bnjz._getvalue(), is_error=hkip__rdv)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    thz__itru = c.context.insert_const_string(c.builder.module, 'scipy.sparse')
    cwh__yomju = c.pyapi.import_module_noblock(thz__itru)
    xuzfk__bnjz = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        xuzfk__bnjz.data)
    ooptx__onwnb = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        xuzfk__bnjz.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        xuzfk__bnjz.indices)
    xsflc__ocw = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), xuzfk__bnjz.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        xuzfk__bnjz.indptr)
    fzvn__yijqs = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), xuzfk__bnjz.indptr, c.env_manager)
    zmnst__ciqma = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        xuzfk__bnjz.shape, c.env_manager)
    jmeln__dhpby = c.pyapi.tuple_pack([ooptx__onwnb, xsflc__ocw, fzvn__yijqs])
    ibuv__dqkf = c.pyapi.call_method(cwh__yomju, 'csr_matrix', (
        jmeln__dhpby, zmnst__ciqma))
    c.pyapi.decref(jmeln__dhpby)
    c.pyapi.decref(ooptx__onwnb)
    c.pyapi.decref(xsflc__ocw)
    c.pyapi.decref(fzvn__yijqs)
    c.pyapi.decref(zmnst__ciqma)
    c.pyapi.decref(cwh__yomju)
    c.context.nrt.decref(c.builder, typ, val)
    return ibuv__dqkf


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
    fvcu__gvznk = A.dtype
    tlzf__txhy = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            fqdg__lqrh, ngdu__xyyl = A.shape
            thvk__wtcns = numba.cpython.unicode._normalize_slice(idx[0],
                fqdg__lqrh)
            qsgjr__elya = numba.cpython.unicode._normalize_slice(idx[1],
                ngdu__xyyl)
            if thvk__wtcns.step != 1 or qsgjr__elya.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            bql__migt = thvk__wtcns.start
            xpcw__sihs = thvk__wtcns.stop
            kmyve__tfeie = qsgjr__elya.start
            jtpon__ducgb = qsgjr__elya.stop
            zxqd__izyq = A.indptr
            qhwi__awin = A.indices
            mrw__zmrb = A.data
            wtke__vnve = xpcw__sihs - bql__migt
            cysq__vtaae = jtpon__ducgb - kmyve__tfeie
            tkh__fhxb = 0
            izxh__fihn = 0
            for puxdq__lkdj in range(wtke__vnve):
                ygyxh__uax = zxqd__izyq[bql__migt + puxdq__lkdj]
                iyekb__bxz = zxqd__izyq[bql__migt + puxdq__lkdj + 1]
                for uoyml__swmo in range(ygyxh__uax, iyekb__bxz):
                    if qhwi__awin[uoyml__swmo] >= kmyve__tfeie and qhwi__awin[
                        uoyml__swmo] < jtpon__ducgb:
                        tkh__fhxb += 1
            ngbss__eqa = np.empty(wtke__vnve + 1, tlzf__txhy)
            gwsog__wtokz = np.empty(tkh__fhxb, tlzf__txhy)
            cac__dehlf = np.empty(tkh__fhxb, fvcu__gvznk)
            ngbss__eqa[0] = 0
            for puxdq__lkdj in range(wtke__vnve):
                ygyxh__uax = zxqd__izyq[bql__migt + puxdq__lkdj]
                iyekb__bxz = zxqd__izyq[bql__migt + puxdq__lkdj + 1]
                for uoyml__swmo in range(ygyxh__uax, iyekb__bxz):
                    if qhwi__awin[uoyml__swmo] >= kmyve__tfeie and qhwi__awin[
                        uoyml__swmo] < jtpon__ducgb:
                        gwsog__wtokz[izxh__fihn] = qhwi__awin[uoyml__swmo
                            ] - kmyve__tfeie
                        cac__dehlf[izxh__fihn] = mrw__zmrb[uoyml__swmo]
                        izxh__fihn += 1
                ngbss__eqa[puxdq__lkdj + 1] = izxh__fihn
            return init_csr_matrix(cac__dehlf, gwsog__wtokz, ngbss__eqa, (
                wtke__vnve, cysq__vtaae))
        return impl
    elif isinstance(idx, types.Array
        ) and idx.ndim == 1 and idx.dtype == tlzf__txhy:

        def impl(A, idx):
            fqdg__lqrh, ngdu__xyyl = A.shape
            zxqd__izyq = A.indptr
            qhwi__awin = A.indices
            mrw__zmrb = A.data
            wtke__vnve = len(idx)
            tkh__fhxb = 0
            izxh__fihn = 0
            for puxdq__lkdj in range(wtke__vnve):
                xwhs__cqhaq = idx[puxdq__lkdj]
                ygyxh__uax = zxqd__izyq[xwhs__cqhaq]
                iyekb__bxz = zxqd__izyq[xwhs__cqhaq + 1]
                tkh__fhxb += iyekb__bxz - ygyxh__uax
            ngbss__eqa = np.empty(wtke__vnve + 1, tlzf__txhy)
            gwsog__wtokz = np.empty(tkh__fhxb, tlzf__txhy)
            cac__dehlf = np.empty(tkh__fhxb, fvcu__gvznk)
            ngbss__eqa[0] = 0
            for puxdq__lkdj in range(wtke__vnve):
                xwhs__cqhaq = idx[puxdq__lkdj]
                ygyxh__uax = zxqd__izyq[xwhs__cqhaq]
                iyekb__bxz = zxqd__izyq[xwhs__cqhaq + 1]
                gwsog__wtokz[izxh__fihn:izxh__fihn + iyekb__bxz - ygyxh__uax
                    ] = qhwi__awin[ygyxh__uax:iyekb__bxz]
                cac__dehlf[izxh__fihn:izxh__fihn + iyekb__bxz - ygyxh__uax
                    ] = mrw__zmrb[ygyxh__uax:iyekb__bxz]
                izxh__fihn += iyekb__bxz - ygyxh__uax
                ngbss__eqa[puxdq__lkdj + 1] = izxh__fihn
            wit__mxd = init_csr_matrix(cac__dehlf, gwsog__wtokz, ngbss__eqa,
                (wtke__vnve, ngdu__xyyl))
            return wit__mxd
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
