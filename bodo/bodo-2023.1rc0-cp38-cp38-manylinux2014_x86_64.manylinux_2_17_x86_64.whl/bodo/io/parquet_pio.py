import os
import warnings
from collections import defaultdict
from glob import has_magic
from typing import Optional
from urllib.parse import urlparse
import llvmlite.binding as ll
import numba
import numpy as np
import pyarrow
import pyarrow as pa
import pyarrow.dataset as ds
from numba.core import types
from numba.extending import NativeValue, box, intrinsic, models, overload, register_model, unbox
from pyarrow._fs import PyFileSystem
from pyarrow.fs import FSSpecHandler
import bodo
import bodo.utils.tracing as tracing
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.io.fs_io import get_hdfs_fs, get_s3_fs_from_path
from bodo.io.helpers import _get_numba_typ_from_pa_typ
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.distributed_api import get_end, get_start
from bodo.utils.typing import BodoError, BodoWarning, FileInfo, FileSchema, get_overload_const_str
REMOTE_FILESYSTEMS = {'s3', 'gcs', 'gs', 'http', 'hdfs', 'abfs', 'abfss'}
READ_STR_AS_DICT_THRESHOLD = 1.0
list_of_files_error_msg = (
    '. Make sure the list/glob passed to read_parquet() only contains paths to files (no directories)'
    )


class ParquetPredicateType(types.Type):

    def __init__(self):
        super(ParquetPredicateType, self).__init__(name=
            'ParquetPredicateType()')


parquet_predicate_type = ParquetPredicateType()
types.parquet_predicate_type = parquet_predicate_type
register_model(ParquetPredicateType)(models.OpaqueModel)


@unbox(ParquetPredicateType)
def unbox_parquet_predicate_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@box(ParquetPredicateType)
def box_parquet_predicate_type(typ, val, c):
    c.pyapi.incref(val)
    return val


class ParquetFileInfo(FileInfo):

    def __init__(self, columns, storage_options=None, input_file_name_col=
        None, read_as_dict_cols=None, use_hive=True):
        self.columns = columns
        self.storage_options = storage_options
        self.input_file_name_col = input_file_name_col
        self.read_as_dict_cols = read_as_dict_cols
        self.use_hive = use_hive
        super().__init__()

    def _get_schema(self, fname):
        try:
            return parquet_file_schema(fname, selected_columns=self.columns,
                storage_options=self.storage_options, input_file_name_col=
                self.input_file_name_col, read_as_dict_cols=self.
                read_as_dict_cols, use_hive=self.use_hive)
        except OSError as jvo__epw:
            if 'non-file path' in str(jvo__epw):
                raise FileNotFoundError(str(jvo__epw))
            raise


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    olj__tlid = get_overload_const_str(dnf_filter_str)
    yrs__xfpx = get_overload_const_str(expr_filter_str)
    nxhic__vmsc = ', '.join(f'f{dyydf__chr}' for dyydf__chr in range(len(
        var_tup)))
    cds__neiqi = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        cds__neiqi += f'  {nxhic__vmsc}, = var_tup\n'
    cds__neiqi += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    cds__neiqi += f'    dnf_filters_py = {olj__tlid}\n'
    cds__neiqi += f'    expr_filters_py = {yrs__xfpx}\n'
    cds__neiqi += '  return (dnf_filters_py, expr_filters_py)\n'
    hhadu__lab = {}
    cuyd__vmsx = globals()
    cuyd__vmsx['numba'] = numba
    exec(cds__neiqi, cuyd__vmsx, hhadu__lab)
    return hhadu__lab['impl']


def unify_schemas(schemas):
    igp__iyja = []
    for schema in schemas:
        for dyydf__chr in range(len(schema)):
            vxkml__fuk = schema.field(dyydf__chr)
            if vxkml__fuk.type == pa.large_string():
                schema = schema.set(dyydf__chr, vxkml__fuk.with_type(pa.
                    string()))
            elif vxkml__fuk.type == pa.large_binary():
                schema = schema.set(dyydf__chr, vxkml__fuk.with_type(pa.
                    binary()))
            elif isinstance(vxkml__fuk.type, (pa.ListType, pa.LargeListType)
                ) and vxkml__fuk.type.value_type in (pa.string(), pa.
                large_string()):
                schema = schema.set(dyydf__chr, vxkml__fuk.with_type(pa.
                    list_(pa.field(vxkml__fuk.type.value_field.name, pa.
                    string()))))
            elif isinstance(vxkml__fuk.type, pa.LargeListType):
                schema = schema.set(dyydf__chr, vxkml__fuk.with_type(pa.
                    list_(pa.field(vxkml__fuk.type.value_field.name,
                    vxkml__fuk.type.value_type))))
        igp__iyja.append(schema)
    return pa.unify_schemas(igp__iyja)


class ParquetDataset:

    def __init__(self, pa_pq_dataset, prefix=''):
        self.schema: pa.Schema = pa_pq_dataset.schema
        self.filesystem = None
        self._bodo_total_rows = 0
        self._prefix = prefix
        self.partitioning = None
        partitioning = pa_pq_dataset.partitioning
        self.partition_names = ([] if partitioning is None or partitioning.
            schema == pa_pq_dataset.schema else list(partitioning.schema.names)
            )
        if self.partition_names:
            self.partitioning_dictionaries = partitioning.dictionaries
            self.partitioning_cls = partitioning.__class__
            self.partitioning_schema = partitioning.schema
        else:
            self.partitioning_dictionaries = {}
        for dyydf__chr in range(len(self.schema)):
            vxkml__fuk = self.schema.field(dyydf__chr)
            if vxkml__fuk.type == pa.large_string():
                self.schema = self.schema.set(dyydf__chr, vxkml__fuk.
                    with_type(pa.string()))
        self.pieces = [ParquetPiece(frag, partitioning, self.
            partition_names) for frag in pa_pq_dataset._dataset.
            get_fragments(filter=pa_pq_dataset._filter_expression)]

    def set_fs(self, fs):
        self.filesystem = fs
        for xxi__eepc in self.pieces:
            xxi__eepc.filesystem = fs

    def __setstate__(self, state):
        self.__dict__ = state
        if self.partition_names:
            sudr__iaae = {xxi__eepc: self.partitioning_dictionaries[
                dyydf__chr] for dyydf__chr, xxi__eepc in enumerate(self.
                partition_names)}
            self.partitioning = self.partitioning_cls(self.
                partitioning_schema, sudr__iaae)


class ParquetPiece(object):

    def __init__(self, frag, partitioning, partition_names):
        self._frag = None
        self.format = frag.format
        self.path = frag.path
        self._bodo_num_rows = 0
        self.partition_keys = []
        if partitioning is not None:
            self.partition_keys = ds._get_partition_keys(frag.
                partition_expression)
            self.partition_keys = [(wee__yksk, partitioning.dictionaries[
                dyydf__chr].index(self.partition_keys[wee__yksk]).as_py()) for
                dyydf__chr, wee__yksk in enumerate(partition_names)]

    @property
    def frag(self):
        if self._frag is None:
            self._frag = self.format.make_fragment(self.path, self.filesystem)
            del self.format
        return self._frag

    @property
    def metadata(self):
        return self.frag.metadata

    @property
    def num_row_groups(self):
        return self.frag.num_row_groups


def get_parquet_dataset(fpath, get_row_counts: bool=True, dnf_filters=None,
    expr_filters=None, storage_options=None, read_categories: bool=False,
    is_parallel=False, tot_rows_to_read: Optional[int]=None,
    typing_pa_schema: Optional[pa.Schema]=None, use_hive: bool=True,
    partitioning='hive') ->ParquetDataset:
    if not use_hive:
        partitioning = None
    if get_row_counts:
        cet__ktiz = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    kse__ric = MPI.COMM_WORLD
    if isinstance(fpath, list):
        joxr__sod = urlparse(fpath[0])
        protocol = joxr__sod.scheme
        dwobk__edklc = joxr__sod.netloc
        for dyydf__chr in range(len(fpath)):
            vxkml__fuk = fpath[dyydf__chr]
            qfoly__qbui = urlparse(vxkml__fuk)
            if qfoly__qbui.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if qfoly__qbui.netloc != dwobk__edklc:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[dyydf__chr] = vxkml__fuk.rstrip('/')
    else:
        joxr__sod = urlparse(fpath)
        protocol = joxr__sod.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as qjxe__mpc:
            amiag__ajsxh = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(amiag__ajsxh)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as qjxe__mpc:
            amiag__ajsxh = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
"""
    fs = []

    def getfs(parallel=False):
        if len(fs) == 1:
            return fs[0]
        if protocol == 's3':
            fs.append(get_s3_fs_from_path(fpath, parallel=parallel,
                storage_options=storage_options) if not isinstance(fpath,
                list) else get_s3_fs_from_path(fpath[0], parallel=parallel,
                storage_options=storage_options))
        elif protocol in {'gcs', 'gs'}:
            kry__qpd = gcsfs.GCSFileSystem(token=None)
            fs.append(PyFileSystem(FSSpecHandler(kry__qpd)))
        elif protocol == 'http':
            fs.append(PyFileSystem(FSSpecHandler(fsspec.filesystem('http'))))
        elif protocol in {'hdfs', 'abfs', 'abfss'}:
            fs.append(get_hdfs_fs(fpath) if not isinstance(fpath, list) else
                get_hdfs_fs(fpath[0]))
        else:
            fs.append(pa.fs.LocalFileSystem())
        return fs[0]

    def glob(protocol, fs, path):
        if not protocol and fs is None:
            from fsspec.implementations.local import LocalFileSystem
            fs = LocalFileSystem()
        if isinstance(fs, pa.fs.FileSystem):
            from fsspec.implementations.arrow import ArrowFSWrapper
            fs = ArrowFSWrapper(fs)
        try:
            psk__xxd = fs.glob(path)
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(psk__xxd) == 0:
            raise BodoError('No files found matching glob pattern')
        return psk__xxd
    rxn__caz = False
    if get_row_counts:
        ssd__llk = getfs(parallel=True)
        rxn__caz = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        rrcph__xupzv = 1
        rejz__kwc = os.cpu_count()
        if rejz__kwc is not None and rejz__kwc > 1:
            rrcph__xupzv = rejz__kwc // 2
        try:
            if get_row_counts:
                zcfxg__facc = tracing.Event('pq.ParquetDataset',
                    is_parallel=False)
                if tracing.is_tracing():
                    zcfxg__facc.add_attribute('g_dnf_filter', str(dnf_filters))
            trsu__tyz = pa.io_thread_count()
            pa.set_io_thread_count(rrcph__xupzv)
            prefix = ''
            if protocol == 's3':
                prefix = 's3://'
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{joxr__sod.netloc}'
            if prefix:
                if isinstance(fpath, list):
                    ikfev__xjhbk = [vxkml__fuk[len(prefix):] for vxkml__fuk in
                        fpath]
                else:
                    ikfev__xjhbk = fpath[len(prefix):]
            else:
                ikfev__xjhbk = fpath
            if isinstance(ikfev__xjhbk, list):
                lzf__hczl = []
                for xxi__eepc in ikfev__xjhbk:
                    if has_magic(xxi__eepc):
                        lzf__hczl += glob(protocol, getfs(), xxi__eepc)
                    else:
                        lzf__hczl.append(xxi__eepc)
                ikfev__xjhbk = lzf__hczl
            elif has_magic(ikfev__xjhbk):
                ikfev__xjhbk = glob(protocol, getfs(), ikfev__xjhbk)
            xhhct__epjz = pq.ParquetDataset(ikfev__xjhbk, filesystem=getfs(
                ), filters=None, use_legacy_dataset=False, partitioning=
                partitioning)
            if dnf_filters is not None:
                xhhct__epjz._filters = dnf_filters
                xhhct__epjz._filter_expression = pq._filters_to_expression(
                    dnf_filters)
            srv__hytti = len(xhhct__epjz.files)
            xhhct__epjz = ParquetDataset(xhhct__epjz, prefix)
            pa.set_io_thread_count(trsu__tyz)
            if typing_pa_schema:
                xhhct__epjz.schema = typing_pa_schema
            if get_row_counts:
                if dnf_filters is not None:
                    zcfxg__facc.add_attribute('num_pieces_before_filter',
                        srv__hytti)
                    zcfxg__facc.add_attribute('num_pieces_after_filter',
                        len(xhhct__epjz.pieces))
                zcfxg__facc.finalize()
        except Exception as jvo__epw:
            if isinstance(jvo__epw, IsADirectoryError):
                jvo__epw = BodoError(list_of_files_error_msg)
            elif isinstance(fpath, list) and isinstance(jvo__epw, (OSError,
                FileNotFoundError)):
                jvo__epw = BodoError(str(jvo__epw) + list_of_files_error_msg)
            else:
                jvo__epw = BodoError(
                    f"""error from pyarrow: {type(jvo__epw).__name__}: {str(jvo__epw)}
"""
                    )
            kse__ric.bcast(jvo__epw)
            raise jvo__epw
        if get_row_counts:
            lov__fuz = tracing.Event('bcast dataset')
        xhhct__epjz = kse__ric.bcast(xhhct__epjz)
    else:
        if get_row_counts:
            lov__fuz = tracing.Event('bcast dataset')
        xhhct__epjz = kse__ric.bcast(None)
        if isinstance(xhhct__epjz, Exception):
            xcn__jwe = xhhct__epjz
            raise xcn__jwe
    xhhct__epjz.set_fs(getfs())
    if get_row_counts:
        lov__fuz.finalize()
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = rxn__caz = False
    if get_row_counts or rxn__caz:
        if get_row_counts and tracing.is_tracing():
            vkj__osmp = tracing.Event('get_row_counts')
            vkj__osmp.add_attribute('g_num_pieces', len(xhhct__epjz.pieces))
            vkj__osmp.add_attribute('g_expr_filters', str(expr_filters))
        vyuhs__bry = 0.0
        num_pieces = len(xhhct__epjz.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        pxbda__meqf = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        sykgt__bylh = 0
        kvdz__vzv = 0
        cyub__csww = 0
        mdv__ucq = True
        if expr_filters is not None:
            import random
            random.seed(37)
            jmqk__nhpwf = random.sample(xhhct__epjz.pieces, k=len(
                xhhct__epjz.pieces))
        else:
            jmqk__nhpwf = xhhct__epjz.pieces
        fpaths = [xxi__eepc.path for xxi__eepc in jmqk__nhpwf[start:
            pxbda__meqf]]
        rrcph__xupzv = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(rrcph__xupzv)
        pa.set_cpu_count(rrcph__xupzv)
        xcn__jwe = None
        try:
            jzbtj__rwaty = ds.dataset(fpaths, filesystem=xhhct__epjz.
                filesystem, partitioning=xhhct__epjz.partitioning)
            for jgrda__zpqil, frag in zip(jmqk__nhpwf[start:pxbda__meqf],
                jzbtj__rwaty.get_fragments()):
                if rxn__caz:
                    ckv__gms = frag.metadata.schema.to_arrow_schema()
                    dhek__eyc = set(ckv__gms.names)
                    mndo__ihhok = set(xhhct__epjz.schema.names) - set(
                        xhhct__epjz.partition_names)
                    if mndo__ihhok != dhek__eyc:
                        ndxm__uscb = dhek__eyc - mndo__ihhok
                        mcir__nbv = mndo__ihhok - dhek__eyc
                        qoad__pfxkj = (
                            f'Schema in {jgrda__zpqil} was different.\n')
                        if typing_pa_schema is not None:
                            if ndxm__uscb:
                                qoad__pfxkj += f"""File contains column(s) {ndxm__uscb} not found in other files in the dataset.
"""
                                raise BodoError(qoad__pfxkj)
                        else:
                            if ndxm__uscb:
                                qoad__pfxkj += f"""File contains column(s) {ndxm__uscb} not found in other files in the dataset.
"""
                            if mcir__nbv:
                                qoad__pfxkj += f"""File missing column(s) {mcir__nbv} found in other files in the dataset.
"""
                            raise BodoError(qoad__pfxkj)
                    try:
                        xhhct__epjz.schema = unify_schemas([xhhct__epjz.
                            schema, ckv__gms])
                    except Exception as jvo__epw:
                        qoad__pfxkj = (
                            f'Schema in {jgrda__zpqil} was different.\n' +
                            str(jvo__epw))
                        raise BodoError(qoad__pfxkj)
                abjl__ggbx = time.time()
                fvnih__xwy = frag.scanner(schema=jzbtj__rwaty.schema,
                    filter=expr_filters, use_threads=True).count_rows()
                vyuhs__bry += time.time() - abjl__ggbx
                jgrda__zpqil._bodo_num_rows = fvnih__xwy
                sykgt__bylh += fvnih__xwy
                kvdz__vzv += frag.num_row_groups
                cyub__csww += sum(qfzl__kqiwi.total_byte_size for
                    qfzl__kqiwi in frag.row_groups)
        except Exception as jvo__epw:
            xcn__jwe = jvo__epw
        if kse__ric.allreduce(xcn__jwe is not None, op=MPI.LOR):
            for xcn__jwe in kse__ric.allgather(xcn__jwe):
                if xcn__jwe:
                    if isinstance(fpath, list) and isinstance(xcn__jwe, (
                        OSError, FileNotFoundError)):
                        raise BodoError(str(xcn__jwe) + list_of_files_error_msg
                            )
                    raise xcn__jwe
        if rxn__caz:
            mdv__ucq = kse__ric.allreduce(mdv__ucq, op=MPI.LAND)
            if not mdv__ucq:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            xhhct__epjz._bodo_total_rows = kse__ric.allreduce(sykgt__bylh,
                op=MPI.SUM)
            hor__frvc = kse__ric.allreduce(kvdz__vzv, op=MPI.SUM)
            omybw__tsqvn = kse__ric.allreduce(cyub__csww, op=MPI.SUM)
            cva__vkwzq = np.array([xxi__eepc._bodo_num_rows for xxi__eepc in
                xhhct__epjz.pieces])
            cva__vkwzq = kse__ric.allreduce(cva__vkwzq, op=MPI.SUM)
            for xxi__eepc, ntsa__bxnx in zip(xhhct__epjz.pieces, cva__vkwzq):
                xxi__eepc._bodo_num_rows = ntsa__bxnx
            if is_parallel and bodo.get_rank(
                ) == 0 and hor__frvc < bodo.get_size() and hor__frvc != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({hor__frvc}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()}). For more details, refer to
https://docs.bodo.ai/latest/file_io/#parquet-section.
"""
                    ))
            if hor__frvc == 0:
                kvow__wegmq = 0
            else:
                kvow__wegmq = omybw__tsqvn // hor__frvc
            if (bodo.get_rank() == 0 and omybw__tsqvn >= 20 * 1048576 and 
                kvow__wegmq < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({kvow__wegmq} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                vkj__osmp.add_attribute('g_total_num_row_groups', hor__frvc)
                vkj__osmp.add_attribute('total_scan_time', vyuhs__bry)
                kavvh__haxfv = np.array([xxi__eepc._bodo_num_rows for
                    xxi__eepc in xhhct__epjz.pieces])
                daz__iru = np.percentile(kavvh__haxfv, [25, 50, 75])
                vkj__osmp.add_attribute('g_row_counts_min', kavvh__haxfv.min())
                vkj__osmp.add_attribute('g_row_counts_Q1', daz__iru[0])
                vkj__osmp.add_attribute('g_row_counts_median', daz__iru[1])
                vkj__osmp.add_attribute('g_row_counts_Q3', daz__iru[2])
                vkj__osmp.add_attribute('g_row_counts_max', kavvh__haxfv.max())
                vkj__osmp.add_attribute('g_row_counts_mean', kavvh__haxfv.
                    mean())
                vkj__osmp.add_attribute('g_row_counts_std', kavvh__haxfv.std())
                vkj__osmp.add_attribute('g_row_counts_sum', kavvh__haxfv.sum())
                vkj__osmp.finalize()
    if read_categories:
        _add_categories_to_pq_dataset(xhhct__epjz)
    if get_row_counts:
        cet__ktiz.finalize()
    if rxn__caz:
        if tracing.is_tracing():
            dhmtp__llwfl = tracing.Event('unify_schemas_across_ranks')
        xcn__jwe = None
        try:
            xhhct__epjz.schema = kse__ric.allreduce(xhhct__epjz.schema,
                bodo.io.helpers.pa_schema_unify_mpi_op)
        except Exception as jvo__epw:
            xcn__jwe = jvo__epw
        if tracing.is_tracing():
            dhmtp__llwfl.finalize()
        if kse__ric.allreduce(xcn__jwe is not None, op=MPI.LOR):
            for xcn__jwe in kse__ric.allgather(xcn__jwe):
                if xcn__jwe:
                    qoad__pfxkj = (
                        f'Schema in some files were different.\n' + str(
                        xcn__jwe))
                    raise BodoError(qoad__pfxkj)
    return xhhct__epjz


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, filesystem, str_as_dict_cols, start_offset,
    rows_to_read, partitioning, schema):
    import pyarrow as pa
    rejz__kwc = os.cpu_count()
    if rejz__kwc is None or rejz__kwc == 0:
        rejz__kwc = 2
    ljjpq__yqje = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), rejz__kwc)
    qgp__wqpf = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)), rejz__kwc)
    if is_parallel and len(fpaths) > qgp__wqpf and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(qgp__wqpf)
        pa.set_cpu_count(qgp__wqpf)
    else:
        pa.set_io_thread_count(ljjpq__yqje)
        pa.set_cpu_count(ljjpq__yqje)
    vxalg__yns = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    ezs__tbqj = set(str_as_dict_cols)
    for dyydf__chr, name in enumerate(schema.names):
        if name in ezs__tbqj:
            rjjiz__ebjj = schema.field(dyydf__chr)
            gxcc__jzev = pa.field(name, pa.dictionary(pa.int32(),
                rjjiz__ebjj.type), rjjiz__ebjj.nullable)
            schema = schema.remove(dyydf__chr).insert(dyydf__chr, gxcc__jzev)
    xhhct__epjz = ds.dataset(fpaths, filesystem=filesystem, partitioning=
        partitioning, schema=schema, format=vxalg__yns)
    xhu__mifdd = xhhct__epjz.schema.names
    nbw__piu = [xhu__mifdd[aeg__dddje] for aeg__dddje in selected_fields]
    yupb__yhnc = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if yupb__yhnc and expr_filters is None:
        llsi__mapna = []
        npcq__jjhx = 0
        szktk__gtth = 0
        for frag in xhhct__epjz.get_fragments():
            rqzkg__wvm = []
            for qfzl__kqiwi in frag.row_groups:
                ajon__ejdq = qfzl__kqiwi.num_rows
                if start_offset < npcq__jjhx + ajon__ejdq:
                    if szktk__gtth == 0:
                        jbja__hwmu = start_offset - npcq__jjhx
                        luvnt__wuaxy = min(ajon__ejdq - jbja__hwmu,
                            rows_to_read)
                    else:
                        luvnt__wuaxy = min(ajon__ejdq, rows_to_read -
                            szktk__gtth)
                    szktk__gtth += luvnt__wuaxy
                    rqzkg__wvm.append(qfzl__kqiwi.id)
                npcq__jjhx += ajon__ejdq
                if szktk__gtth == rows_to_read:
                    break
            llsi__mapna.append(frag.subset(row_group_ids=rqzkg__wvm))
            if szktk__gtth == rows_to_read:
                break
        xhhct__epjz = ds.FileSystemDataset(llsi__mapna, xhhct__epjz.schema,
            vxalg__yns, filesystem=xhhct__epjz.filesystem)
        start_offset = jbja__hwmu
    cmxs__frlfj = xhhct__epjz.scanner(columns=nbw__piu, filter=expr_filters,
        use_threads=True).to_reader()
    return xhhct__epjz, cmxs__frlfj, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema
    tul__sczd = [c for c in pa_schema.names if isinstance(pa_schema.field(c
        ).type, pa.DictionaryType) and c not in pq_dataset.partition_names]
    if len(tul__sczd) == 0:
        pq_dataset._category_info = {}
        return
    kse__ric = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            tqs__imecp = pq_dataset.pieces[0].frag.head(100, columns=tul__sczd)
            myv__vajgu = {c: tuple(tqs__imecp.column(c).chunk(0).dictionary
                .to_pylist()) for c in tul__sczd}
            del tqs__imecp
        except Exception as jvo__epw:
            kse__ric.bcast(jvo__epw)
            raise jvo__epw
        kse__ric.bcast(myv__vajgu)
    else:
        myv__vajgu = kse__ric.bcast(None)
        if isinstance(myv__vajgu, Exception):
            xcn__jwe = myv__vajgu
            raise xcn__jwe
    pq_dataset._category_info = myv__vajgu


def get_pandas_metadata(schema, num_pieces):
    wtc__zjeek = None
    ugri__qsltx = defaultdict(lambda : None)
    qkq__iepcr = b'pandas'
    if schema.metadata is not None and qkq__iepcr in schema.metadata:
        import json
        efx__pry = json.loads(schema.metadata[qkq__iepcr].decode('utf8'))
        qzr__wux = len(efx__pry['index_columns'])
        if qzr__wux > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        wtc__zjeek = efx__pry['index_columns'][0] if qzr__wux else None
        if not isinstance(wtc__zjeek, str) and not isinstance(wtc__zjeek, dict
            ):
            wtc__zjeek = None
        for dia__odlo in efx__pry['columns']:
            csn__anlw = dia__odlo['name']
            teqr__nio = dia__odlo['pandas_type']
            if (teqr__nio.startswith('int') or teqr__nio.startswith('float')
                ) and csn__anlw is not None:
                fhcl__xvjsl = dia__odlo['numpy_type']
                if fhcl__xvjsl.startswith('Int') or fhcl__xvjsl.startswith(
                    'Float'):
                    ugri__qsltx[csn__anlw] = True
                else:
                    ugri__qsltx[csn__anlw] = False
    return wtc__zjeek, ugri__qsltx


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for csn__anlw in pa_schema.names:
        icpw__szn = pa_schema.field(csn__anlw)
        if icpw__szn.type in (pa.string(), pa.large_string()):
            str_columns.append(csn__anlw)
    return str_columns


def _pa_schemas_match(pa_schema1, pa_schema2):
    if pa_schema1.names != pa_schema2.names:
        return False
    try:
        unify_schemas([pa_schema1, pa_schema2])
    except:
        return False
    return True


def _get_sample_pq_pieces(pq_dataset, pa_schema, is_iceberg):
    jmqk__nhpwf = pq_dataset.pieces
    if len(jmqk__nhpwf) > bodo.get_size():
        import random
        random.seed(37)
        jmqk__nhpwf = random.sample(jmqk__nhpwf, bodo.get_size())
    else:
        jmqk__nhpwf = jmqk__nhpwf
    if is_iceberg:
        jmqk__nhpwf = [xxi__eepc for xxi__eepc in jmqk__nhpwf if
            _pa_schemas_match(xxi__eepc.metadata.schema.to_arrow_schema(),
            pa_schema)]
    return jmqk__nhpwf


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns: list,
    is_iceberg: bool=False) ->set:
    from mpi4py import MPI
    kse__ric = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    jmqk__nhpwf = _get_sample_pq_pieces(pq_dataset, pa_schema, is_iceberg)
    str_columns = sorted(str_columns)
    thqc__bqh = np.zeros(len(str_columns), dtype=np.int64)
    hqeln__xzpvd = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(jmqk__nhpwf):
        jgrda__zpqil = jmqk__nhpwf[bodo.get_rank()]
        try:
            metadata = jgrda__zpqil.metadata
            for dyydf__chr in range(jgrda__zpqil.num_row_groups):
                for mvlze__yxcl, csn__anlw in enumerate(str_columns):
                    ocnei__orvf = pa_schema.get_field_index(csn__anlw)
                    thqc__bqh[mvlze__yxcl] += metadata.row_group(dyydf__chr
                        ).column(ocnei__orvf).total_uncompressed_size
            rvjx__jbu = metadata.num_rows
        except Exception as jvo__epw:
            if isinstance(jvo__epw, (OSError, FileNotFoundError)):
                rvjx__jbu = 0
            else:
                raise
    else:
        rvjx__jbu = 0
    hzvpe__pmetx = kse__ric.allreduce(rvjx__jbu, op=MPI.SUM)
    if hzvpe__pmetx == 0:
        return set()
    kse__ric.Allreduce(thqc__bqh, hqeln__xzpvd, op=MPI.SUM)
    xndz__yktwl = hqeln__xzpvd / hzvpe__pmetx
    ayogc__hagvg = set()
    for dyydf__chr, zcoz__mbrsy in enumerate(xndz__yktwl):
        if zcoz__mbrsy < READ_STR_AS_DICT_THRESHOLD:
            csn__anlw = str_columns[dyydf__chr]
            ayogc__hagvg.add(csn__anlw)
    return ayogc__hagvg


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None, use_hive=True
    ) ->FileSchema:
    xhu__mifdd = []
    gpe__eoo = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True, use_hive=
        use_hive)
    partition_names = pq_dataset.partition_names
    pa_schema = pq_dataset.schema
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    vpos__cody = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    pzs__lmc = read_as_dict_cols - vpos__cody
    if len(pzs__lmc) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {pzs__lmc}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(vpos__cody)
    vpos__cody = vpos__cody - read_as_dict_cols
    str_columns = [pace__fgesr for pace__fgesr in str_columns if 
        pace__fgesr in vpos__cody]
    ayogc__hagvg = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    ayogc__hagvg.update(read_as_dict_cols)
    xhu__mifdd = pa_schema.names
    wtc__zjeek, ugri__qsltx = get_pandas_metadata(pa_schema, num_pieces)
    hxyw__qkpob = []
    jbtb__jsmpq = []
    gkl__fvt = []
    for dyydf__chr, c in enumerate(xhu__mifdd):
        if c in partition_names:
            continue
        icpw__szn = pa_schema.field(c)
        ylo__leox, suf__pzrtd = _get_numba_typ_from_pa_typ(icpw__szn, c ==
            wtc__zjeek, ugri__qsltx[c], pq_dataset._category_info,
            str_as_dict=c in ayogc__hagvg)
        hxyw__qkpob.append(ylo__leox)
        jbtb__jsmpq.append(suf__pzrtd)
        gkl__fvt.append(icpw__szn.type)
    if partition_names:
        hxyw__qkpob += [_get_partition_cat_dtype(pq_dataset.
            partitioning_dictionaries[dyydf__chr]) for dyydf__chr in range(
            len(partition_names))]
        jbtb__jsmpq.extend([True] * len(partition_names))
        gkl__fvt.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        xhu__mifdd += [input_file_name_col]
        hxyw__qkpob += [dict_str_arr_type]
        jbtb__jsmpq.append(True)
        gkl__fvt.append(None)
    yjs__suyzp = {c: dyydf__chr for dyydf__chr, c in enumerate(xhu__mifdd)}
    if selected_columns is None:
        selected_columns = xhu__mifdd
    for c in selected_columns:
        if c not in yjs__suyzp:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if wtc__zjeek and not isinstance(wtc__zjeek, dict
        ) and wtc__zjeek not in selected_columns:
        selected_columns.append(wtc__zjeek)
    xhu__mifdd = selected_columns
    wfuw__qsbap = []
    gpe__eoo = []
    smr__mqwtx = []
    npj__sog = []
    for dyydf__chr, c in enumerate(xhu__mifdd):
        weqty__yjmzc = yjs__suyzp[c]
        wfuw__qsbap.append(weqty__yjmzc)
        gpe__eoo.append(hxyw__qkpob[weqty__yjmzc])
        if not jbtb__jsmpq[weqty__yjmzc]:
            smr__mqwtx.append(dyydf__chr)
            npj__sog.append(gkl__fvt[weqty__yjmzc])
    return (xhu__mifdd, gpe__eoo, wtc__zjeek, wfuw__qsbap, partition_names,
        smr__mqwtx, npj__sog, pa_schema)


def _get_partition_cat_dtype(dictionary):
    assert dictionary is not None
    fxsxz__xch = dictionary.to_pandas()
    vqeb__iueq = bodo.typeof(fxsxz__xch).dtype
    if isinstance(vqeb__iueq, types.Integer):
        ugbmt__ejqlz = PDCategoricalDtype(tuple(fxsxz__xch), vqeb__iueq, 
            False, int_type=vqeb__iueq)
    else:
        ugbmt__ejqlz = PDCategoricalDtype(tuple(fxsxz__xch), vqeb__iueq, False)
    return CategoricalArrayType(ugbmt__ejqlz)


from llvmlite import ir as lir
from numba.core import cgutils
if bodo.utils.utils.has_pyarrow():
    from bodo.io import arrow_cpp
    ll.add_symbol('pq_write', arrow_cpp.pq_write)
    ll.add_symbol('pq_write_partitioned', arrow_cpp.pq_write_partitioned)


@intrinsic
def parquet_write_table_cpp(typingctx, filename_t, table_t, col_names_t,
    index_t, write_index, metadata_t, compression_t, is_parallel_t,
    write_range_index, start, stop, step, name, bucket_region,
    row_group_size, file_prefix, convert_timedelta_to_int64, timestamp_tz,
    downcast_time_ns_to_us):

    def codegen(context, builder, sig, args):
        vilup__cebhl = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(1), lir.IntType(8).as_pointer(), lir.IntType(1)])
        wrp__lfp = cgutils.get_or_insert_function(builder.module,
            vilup__cebhl, name='pq_write')
        sipn__yauc = builder.call(wrp__lfp, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return sipn__yauc
    return types.int64(types.voidptr, table_t, col_names_t, index_t, types.
        boolean, types.voidptr, types.voidptr, types.boolean, types.boolean,
        types.int32, types.int32, types.int32, types.voidptr, types.voidptr,
        types.int64, types.voidptr, types.boolean, types.voidptr, types.boolean
        ), codegen


@intrinsic
def parquet_write_table_partitioned_cpp(typingctx, filename_t, data_table_t,
    col_names_t, col_names_no_partitions_t, cat_table_t, part_col_idxs_t,
    num_part_col_t, compression_t, is_parallel_t, bucket_region,
    row_group_size, file_prefix, timestamp_tz):

    def codegen(context, builder, sig, args):
        vilup__cebhl = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        wrp__lfp = cgutils.get_or_insert_function(builder.module,
            vilup__cebhl, name='pq_write_partitioned')
        builder.call(wrp__lfp, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64, types.
        voidptr, types.voidptr), codegen
