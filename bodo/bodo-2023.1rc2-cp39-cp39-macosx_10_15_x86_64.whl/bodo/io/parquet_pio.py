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
        except OSError as lcs__uyk:
            if 'non-file path' in str(lcs__uyk):
                raise FileNotFoundError(str(lcs__uyk))
            raise


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    zeg__mior = get_overload_const_str(dnf_filter_str)
    yzj__sjut = get_overload_const_str(expr_filter_str)
    hjb__wtsh = ', '.join(f'f{ftza__umd}' for ftza__umd in range(len(var_tup)))
    kjcy__vemqv = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        kjcy__vemqv += f'  {hjb__wtsh}, = var_tup\n'
    kjcy__vemqv += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    kjcy__vemqv += f'    dnf_filters_py = {zeg__mior}\n'
    kjcy__vemqv += f'    expr_filters_py = {yzj__sjut}\n'
    kjcy__vemqv += '  return (dnf_filters_py, expr_filters_py)\n'
    xvnl__dcfrp = {}
    hntcj__tlkag = globals()
    hntcj__tlkag['numba'] = numba
    exec(kjcy__vemqv, hntcj__tlkag, xvnl__dcfrp)
    return xvnl__dcfrp['impl']


def unify_schemas(schemas):
    uhm__yvnj = []
    for schema in schemas:
        for ftza__umd in range(len(schema)):
            wddj__tzxv = schema.field(ftza__umd)
            if wddj__tzxv.type == pa.large_string():
                schema = schema.set(ftza__umd, wddj__tzxv.with_type(pa.
                    string()))
            elif wddj__tzxv.type == pa.large_binary():
                schema = schema.set(ftza__umd, wddj__tzxv.with_type(pa.
                    binary()))
            elif isinstance(wddj__tzxv.type, (pa.ListType, pa.LargeListType)
                ) and wddj__tzxv.type.value_type in (pa.string(), pa.
                large_string()):
                schema = schema.set(ftza__umd, wddj__tzxv.with_type(pa.
                    list_(pa.field(wddj__tzxv.type.value_field.name, pa.
                    string()))))
            elif isinstance(wddj__tzxv.type, pa.LargeListType):
                schema = schema.set(ftza__umd, wddj__tzxv.with_type(pa.
                    list_(pa.field(wddj__tzxv.type.value_field.name,
                    wddj__tzxv.type.value_type))))
        uhm__yvnj.append(schema)
    return pa.unify_schemas(uhm__yvnj)


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
        for ftza__umd in range(len(self.schema)):
            wddj__tzxv = self.schema.field(ftza__umd)
            if wddj__tzxv.type == pa.large_string():
                self.schema = self.schema.set(ftza__umd, wddj__tzxv.
                    with_type(pa.string()))
        self.pieces = [ParquetPiece(frag, partitioning, self.
            partition_names) for frag in pa_pq_dataset._dataset.
            get_fragments(filter=pa_pq_dataset._filter_expression)]

    def set_fs(self, fs):
        self.filesystem = fs
        for omi__wso in self.pieces:
            omi__wso.filesystem = fs

    def __setstate__(self, state):
        self.__dict__ = state
        if self.partition_names:
            wnz__joe = {omi__wso: self.partitioning_dictionaries[ftza__umd] for
                ftza__umd, omi__wso in enumerate(self.partition_names)}
            self.partitioning = self.partitioning_cls(self.
                partitioning_schema, wnz__joe)


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
            self.partition_keys = [(yygn__awaj, partitioning.dictionaries[
                ftza__umd].index(self.partition_keys[yygn__awaj]).as_py()) for
                ftza__umd, yygn__awaj in enumerate(partition_names)]

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
        ehe__ywg = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    byagk__krorr = MPI.COMM_WORLD
    if isinstance(fpath, list):
        rlo__txil = urlparse(fpath[0])
        protocol = rlo__txil.scheme
        alw__mgl = rlo__txil.netloc
        for ftza__umd in range(len(fpath)):
            wddj__tzxv = fpath[ftza__umd]
            kwhbu__bvov = urlparse(wddj__tzxv)
            if kwhbu__bvov.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if kwhbu__bvov.netloc != alw__mgl:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[ftza__umd] = wddj__tzxv.rstrip('/')
    else:
        rlo__txil = urlparse(fpath)
        protocol = rlo__txil.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as mmrz__wqmd:
            yknru__raxe = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(yknru__raxe)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as mmrz__wqmd:
            yknru__raxe = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
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
            sat__fbd = gcsfs.GCSFileSystem(token=None)
            fs.append(PyFileSystem(FSSpecHandler(sat__fbd)))
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
            jdgzi__auiz = fs.glob(path)
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(jdgzi__auiz) == 0:
            raise BodoError('No files found matching glob pattern')
        return jdgzi__auiz
    zjazf__ozsbc = False
    if get_row_counts:
        tqyhk__vneat = getfs(parallel=True)
        zjazf__ozsbc = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        sgmz__hty = 1
        rbis__nho = os.cpu_count()
        if rbis__nho is not None and rbis__nho > 1:
            sgmz__hty = rbis__nho // 2
        try:
            if get_row_counts:
                awoca__nrme = tracing.Event('pq.ParquetDataset',
                    is_parallel=False)
                if tracing.is_tracing():
                    awoca__nrme.add_attribute('g_dnf_filter', str(dnf_filters))
            uain__saa = pa.io_thread_count()
            pa.set_io_thread_count(sgmz__hty)
            prefix = ''
            if protocol == 's3':
                prefix = 's3://'
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{rlo__txil.netloc}'
            if prefix:
                if isinstance(fpath, list):
                    xsdd__whd = [wddj__tzxv[len(prefix):] for wddj__tzxv in
                        fpath]
                else:
                    xsdd__whd = fpath[len(prefix):]
            else:
                xsdd__whd = fpath
            if isinstance(xsdd__whd, list):
                uoam__shcyy = []
                for omi__wso in xsdd__whd:
                    if has_magic(omi__wso):
                        uoam__shcyy += glob(protocol, getfs(), omi__wso)
                    else:
                        uoam__shcyy.append(omi__wso)
                xsdd__whd = uoam__shcyy
            elif has_magic(xsdd__whd):
                xsdd__whd = glob(protocol, getfs(), xsdd__whd)
            szafg__egxl = pq.ParquetDataset(xsdd__whd, filesystem=getfs(),
                filters=None, use_legacy_dataset=False, partitioning=
                partitioning)
            if dnf_filters is not None:
                szafg__egxl._filters = dnf_filters
                szafg__egxl._filter_expression = pq._filters_to_expression(
                    dnf_filters)
            yzbtm__detw = len(szafg__egxl.files)
            szafg__egxl = ParquetDataset(szafg__egxl, prefix)
            pa.set_io_thread_count(uain__saa)
            if typing_pa_schema:
                szafg__egxl.schema = typing_pa_schema
            if get_row_counts:
                if dnf_filters is not None:
                    awoca__nrme.add_attribute('num_pieces_before_filter',
                        yzbtm__detw)
                    awoca__nrme.add_attribute('num_pieces_after_filter',
                        len(szafg__egxl.pieces))
                awoca__nrme.finalize()
        except Exception as lcs__uyk:
            if isinstance(lcs__uyk, IsADirectoryError):
                lcs__uyk = BodoError(list_of_files_error_msg)
            elif isinstance(fpath, list) and isinstance(lcs__uyk, (OSError,
                FileNotFoundError)):
                lcs__uyk = BodoError(str(lcs__uyk) + list_of_files_error_msg)
            else:
                lcs__uyk = BodoError(
                    f"""error from pyarrow: {type(lcs__uyk).__name__}: {str(lcs__uyk)}
"""
                    )
            byagk__krorr.bcast(lcs__uyk)
            raise lcs__uyk
        if get_row_counts:
            nirt__dtvom = tracing.Event('bcast dataset')
        szafg__egxl = byagk__krorr.bcast(szafg__egxl)
    else:
        if get_row_counts:
            nirt__dtvom = tracing.Event('bcast dataset')
        szafg__egxl = byagk__krorr.bcast(None)
        if isinstance(szafg__egxl, Exception):
            xtvnc__whc = szafg__egxl
            raise xtvnc__whc
    szafg__egxl.set_fs(getfs())
    if get_row_counts:
        nirt__dtvom.finalize()
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = zjazf__ozsbc = False
    if get_row_counts or zjazf__ozsbc:
        if get_row_counts and tracing.is_tracing():
            btpl__bpo = tracing.Event('get_row_counts')
            btpl__bpo.add_attribute('g_num_pieces', len(szafg__egxl.pieces))
            btpl__bpo.add_attribute('g_expr_filters', str(expr_filters))
        yexwz__ootct = 0.0
        num_pieces = len(szafg__egxl.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        ayoa__yjaw = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        erhtv__dget = 0
        utpoa__utghg = 0
        aak__sah = 0
        psgrf__oyj = True
        if expr_filters is not None:
            import random
            random.seed(37)
            cogim__qavyh = random.sample(szafg__egxl.pieces, k=len(
                szafg__egxl.pieces))
        else:
            cogim__qavyh = szafg__egxl.pieces
        fpaths = [omi__wso.path for omi__wso in cogim__qavyh[start:ayoa__yjaw]]
        sgmz__hty = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(sgmz__hty)
        pa.set_cpu_count(sgmz__hty)
        xtvnc__whc = None
        try:
            gwo__ybgd = ds.dataset(fpaths, filesystem=szafg__egxl.
                filesystem, partitioning=szafg__egxl.partitioning)
            for pht__qayeh, frag in zip(cogim__qavyh[start:ayoa__yjaw],
                gwo__ybgd.get_fragments()):
                if zjazf__ozsbc:
                    kkai__xvqb = frag.metadata.schema.to_arrow_schema()
                    xbb__eje = set(kkai__xvqb.names)
                    xvfc__mwwog = set(szafg__egxl.schema.names) - set(
                        szafg__egxl.partition_names)
                    if xvfc__mwwog != xbb__eje:
                        nthyg__tmxtf = xbb__eje - xvfc__mwwog
                        mlf__sbd = xvfc__mwwog - xbb__eje
                        ixcxi__yko = f'Schema in {pht__qayeh} was different.\n'
                        if typing_pa_schema is not None:
                            if nthyg__tmxtf:
                                ixcxi__yko += f"""File contains column(s) {nthyg__tmxtf} not found in other files in the dataset.
"""
                                raise BodoError(ixcxi__yko)
                        else:
                            if nthyg__tmxtf:
                                ixcxi__yko += f"""File contains column(s) {nthyg__tmxtf} not found in other files in the dataset.
"""
                            if mlf__sbd:
                                ixcxi__yko += f"""File missing column(s) {mlf__sbd} found in other files in the dataset.
"""
                            raise BodoError(ixcxi__yko)
                    try:
                        szafg__egxl.schema = unify_schemas([szafg__egxl.
                            schema, kkai__xvqb])
                    except Exception as lcs__uyk:
                        ixcxi__yko = (
                            f'Schema in {pht__qayeh} was different.\n' +
                            str(lcs__uyk))
                        raise BodoError(ixcxi__yko)
                eqm__bzlvs = time.time()
                aedah__wai = frag.scanner(schema=gwo__ybgd.schema, filter=
                    expr_filters, use_threads=True).count_rows()
                yexwz__ootct += time.time() - eqm__bzlvs
                pht__qayeh._bodo_num_rows = aedah__wai
                erhtv__dget += aedah__wai
                utpoa__utghg += frag.num_row_groups
                aak__sah += sum(extuj__hjt.total_byte_size for extuj__hjt in
                    frag.row_groups)
        except Exception as lcs__uyk:
            xtvnc__whc = lcs__uyk
        if byagk__krorr.allreduce(xtvnc__whc is not None, op=MPI.LOR):
            for xtvnc__whc in byagk__krorr.allgather(xtvnc__whc):
                if xtvnc__whc:
                    if isinstance(fpath, list) and isinstance(xtvnc__whc, (
                        OSError, FileNotFoundError)):
                        raise BodoError(str(xtvnc__whc) +
                            list_of_files_error_msg)
                    raise xtvnc__whc
        if zjazf__ozsbc:
            psgrf__oyj = byagk__krorr.allreduce(psgrf__oyj, op=MPI.LAND)
            if not psgrf__oyj:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            szafg__egxl._bodo_total_rows = byagk__krorr.allreduce(erhtv__dget,
                op=MPI.SUM)
            zqd__mqiwu = byagk__krorr.allreduce(utpoa__utghg, op=MPI.SUM)
            hjpd__ssz = byagk__krorr.allreduce(aak__sah, op=MPI.SUM)
            kbrh__ftcb = np.array([omi__wso._bodo_num_rows for omi__wso in
                szafg__egxl.pieces])
            kbrh__ftcb = byagk__krorr.allreduce(kbrh__ftcb, op=MPI.SUM)
            for omi__wso, ijrrk__qms in zip(szafg__egxl.pieces, kbrh__ftcb):
                omi__wso._bodo_num_rows = ijrrk__qms
            if is_parallel and bodo.get_rank(
                ) == 0 and zqd__mqiwu < bodo.get_size() and zqd__mqiwu != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({zqd__mqiwu}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()}). For more details, refer to
https://docs.bodo.ai/latest/file_io/#parquet-section.
"""
                    ))
            if zqd__mqiwu == 0:
                vnok__eer = 0
            else:
                vnok__eer = hjpd__ssz // zqd__mqiwu
            if (bodo.get_rank() == 0 and hjpd__ssz >= 20 * 1048576 and 
                vnok__eer < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({vnok__eer} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                btpl__bpo.add_attribute('g_total_num_row_groups', zqd__mqiwu)
                btpl__bpo.add_attribute('total_scan_time', yexwz__ootct)
                achpb__bot = np.array([omi__wso._bodo_num_rows for omi__wso in
                    szafg__egxl.pieces])
                gry__zbqx = np.percentile(achpb__bot, [25, 50, 75])
                btpl__bpo.add_attribute('g_row_counts_min', achpb__bot.min())
                btpl__bpo.add_attribute('g_row_counts_Q1', gry__zbqx[0])
                btpl__bpo.add_attribute('g_row_counts_median', gry__zbqx[1])
                btpl__bpo.add_attribute('g_row_counts_Q3', gry__zbqx[2])
                btpl__bpo.add_attribute('g_row_counts_max', achpb__bot.max())
                btpl__bpo.add_attribute('g_row_counts_mean', achpb__bot.mean())
                btpl__bpo.add_attribute('g_row_counts_std', achpb__bot.std())
                btpl__bpo.add_attribute('g_row_counts_sum', achpb__bot.sum())
                btpl__bpo.finalize()
    if read_categories:
        _add_categories_to_pq_dataset(szafg__egxl)
    if get_row_counts:
        ehe__ywg.finalize()
    if zjazf__ozsbc:
        if tracing.is_tracing():
            bjux__tjgp = tracing.Event('unify_schemas_across_ranks')
        xtvnc__whc = None
        try:
            szafg__egxl.schema = byagk__krorr.allreduce(szafg__egxl.schema,
                bodo.io.helpers.pa_schema_unify_mpi_op)
        except Exception as lcs__uyk:
            xtvnc__whc = lcs__uyk
        if tracing.is_tracing():
            bjux__tjgp.finalize()
        if byagk__krorr.allreduce(xtvnc__whc is not None, op=MPI.LOR):
            for xtvnc__whc in byagk__krorr.allgather(xtvnc__whc):
                if xtvnc__whc:
                    ixcxi__yko = (f'Schema in some files were different.\n' +
                        str(xtvnc__whc))
                    raise BodoError(ixcxi__yko)
    return szafg__egxl


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, filesystem, str_as_dict_cols, start_offset,
    rows_to_read, partitioning, schema):
    import pyarrow as pa
    rbis__nho = os.cpu_count()
    if rbis__nho is None or rbis__nho == 0:
        rbis__nho = 2
    eqih__hlqc = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), rbis__nho)
    rihci__eqmrv = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)),
        rbis__nho)
    if is_parallel and len(fpaths) > rihci__eqmrv and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(rihci__eqmrv)
        pa.set_cpu_count(rihci__eqmrv)
    else:
        pa.set_io_thread_count(eqih__hlqc)
        pa.set_cpu_count(eqih__hlqc)
    zmtc__fedjd = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    nhkc__dkksg = set(str_as_dict_cols)
    for ftza__umd, name in enumerate(schema.names):
        if name in nhkc__dkksg:
            amf__zlwl = schema.field(ftza__umd)
            vhf__oyg = pa.field(name, pa.dictionary(pa.int32(), amf__zlwl.
                type), amf__zlwl.nullable)
            schema = schema.remove(ftza__umd).insert(ftza__umd, vhf__oyg)
    szafg__egxl = ds.dataset(fpaths, filesystem=filesystem, partitioning=
        partitioning, schema=schema, format=zmtc__fedjd)
    dpiqt__axky = szafg__egxl.schema.names
    afxrm__rtjia = [dpiqt__axky[xcjwu__ciksd] for xcjwu__ciksd in
        selected_fields]
    uvksl__nqrq = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if uvksl__nqrq and expr_filters is None:
        xykmp__btt = []
        fvdpk__lgi = 0
        oniwb__dwsy = 0
        for frag in szafg__egxl.get_fragments():
            bgf__mye = []
            for extuj__hjt in frag.row_groups:
                cpkyr__xzqy = extuj__hjt.num_rows
                if start_offset < fvdpk__lgi + cpkyr__xzqy:
                    if oniwb__dwsy == 0:
                        dmv__whsx = start_offset - fvdpk__lgi
                        gyus__qbdwj = min(cpkyr__xzqy - dmv__whsx, rows_to_read
                            )
                    else:
                        gyus__qbdwj = min(cpkyr__xzqy, rows_to_read -
                            oniwb__dwsy)
                    oniwb__dwsy += gyus__qbdwj
                    bgf__mye.append(extuj__hjt.id)
                fvdpk__lgi += cpkyr__xzqy
                if oniwb__dwsy == rows_to_read:
                    break
            xykmp__btt.append(frag.subset(row_group_ids=bgf__mye))
            if oniwb__dwsy == rows_to_read:
                break
        szafg__egxl = ds.FileSystemDataset(xykmp__btt, szafg__egxl.schema,
            zmtc__fedjd, filesystem=szafg__egxl.filesystem)
        start_offset = dmv__whsx
    xhg__lazka = szafg__egxl.scanner(columns=afxrm__rtjia, filter=
        expr_filters, use_threads=True).to_reader()
    return szafg__egxl, xhg__lazka, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema
    ojnc__ajix = [c for c in pa_schema.names if isinstance(pa_schema.field(
        c).type, pa.DictionaryType) and c not in pq_dataset.partition_names]
    if len(ojnc__ajix) == 0:
        pq_dataset._category_info = {}
        return
    byagk__krorr = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            zjsy__ycbb = pq_dataset.pieces[0].frag.head(100, columns=ojnc__ajix
                )
            jsvpj__sqryv = {c: tuple(zjsy__ycbb.column(c).chunk(0).
                dictionary.to_pylist()) for c in ojnc__ajix}
            del zjsy__ycbb
        except Exception as lcs__uyk:
            byagk__krorr.bcast(lcs__uyk)
            raise lcs__uyk
        byagk__krorr.bcast(jsvpj__sqryv)
    else:
        jsvpj__sqryv = byagk__krorr.bcast(None)
        if isinstance(jsvpj__sqryv, Exception):
            xtvnc__whc = jsvpj__sqryv
            raise xtvnc__whc
    pq_dataset._category_info = jsvpj__sqryv


def get_pandas_metadata(schema, num_pieces):
    xpaqa__qsnz = None
    ysj__bzode = defaultdict(lambda : None)
    dys__tnqk = b'pandas'
    if schema.metadata is not None and dys__tnqk in schema.metadata:
        import json
        uao__rdxy = json.loads(schema.metadata[dys__tnqk].decode('utf8'))
        sta__umaiu = len(uao__rdxy['index_columns'])
        if sta__umaiu > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        xpaqa__qsnz = uao__rdxy['index_columns'][0] if sta__umaiu else None
        if not isinstance(xpaqa__qsnz, str) and not isinstance(xpaqa__qsnz,
            dict):
            xpaqa__qsnz = None
        for oddck__vmrl in uao__rdxy['columns']:
            tui__vqq = oddck__vmrl['name']
            lcs__sptgh = oddck__vmrl['pandas_type']
            if (lcs__sptgh.startswith('int') or lcs__sptgh.startswith('float')
                ) and tui__vqq is not None:
                jfq__rkta = oddck__vmrl['numpy_type']
                if jfq__rkta.startswith('Int') or jfq__rkta.startswith('Float'
                    ):
                    ysj__bzode[tui__vqq] = True
                else:
                    ysj__bzode[tui__vqq] = False
    return xpaqa__qsnz, ysj__bzode


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for tui__vqq in pa_schema.names:
        cmlp__pwkyq = pa_schema.field(tui__vqq)
        if cmlp__pwkyq.type in (pa.string(), pa.large_string()):
            str_columns.append(tui__vqq)
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
    cogim__qavyh = pq_dataset.pieces
    if len(cogim__qavyh) > bodo.get_size():
        import random
        random.seed(37)
        cogim__qavyh = random.sample(cogim__qavyh, bodo.get_size())
    else:
        cogim__qavyh = cogim__qavyh
    if is_iceberg:
        cogim__qavyh = [omi__wso for omi__wso in cogim__qavyh if
            _pa_schemas_match(omi__wso.metadata.schema.to_arrow_schema(),
            pa_schema)]
    return cogim__qavyh


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns: list,
    is_iceberg: bool=False) ->set:
    from mpi4py import MPI
    byagk__krorr = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    cogim__qavyh = _get_sample_pq_pieces(pq_dataset, pa_schema, is_iceberg)
    str_columns = sorted(str_columns)
    imo__idleo = np.zeros(len(str_columns), dtype=np.int64)
    jqx__wpi = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(cogim__qavyh):
        pht__qayeh = cogim__qavyh[bodo.get_rank()]
        try:
            metadata = pht__qayeh.metadata
            for ftza__umd in range(pht__qayeh.num_row_groups):
                for asuw__udzd, tui__vqq in enumerate(str_columns):
                    jaa__tgs = pa_schema.get_field_index(tui__vqq)
                    imo__idleo[asuw__udzd] += metadata.row_group(ftza__umd
                        ).column(jaa__tgs).total_uncompressed_size
            mmy__hcpye = metadata.num_rows
        except Exception as lcs__uyk:
            if isinstance(lcs__uyk, (OSError, FileNotFoundError)):
                mmy__hcpye = 0
            else:
                raise
    else:
        mmy__hcpye = 0
    ntbs__rtltx = byagk__krorr.allreduce(mmy__hcpye, op=MPI.SUM)
    if ntbs__rtltx == 0:
        return set()
    byagk__krorr.Allreduce(imo__idleo, jqx__wpi, op=MPI.SUM)
    ggjr__lugbf = jqx__wpi / ntbs__rtltx
    ltf__ipll = set()
    for ftza__umd, bfo__mrn in enumerate(ggjr__lugbf):
        if bfo__mrn < READ_STR_AS_DICT_THRESHOLD:
            tui__vqq = str_columns[ftza__umd]
            ltf__ipll.add(tui__vqq)
    return ltf__ipll


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None, use_hive=True
    ) ->FileSchema:
    dpiqt__axky = []
    api__sxt = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True, use_hive=
        use_hive)
    partition_names = pq_dataset.partition_names
    pa_schema = pq_dataset.schema
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    sqzvo__nqr = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    cmmcq__weq = read_as_dict_cols - sqzvo__nqr
    if len(cmmcq__weq) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {cmmcq__weq}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(sqzvo__nqr)
    sqzvo__nqr = sqzvo__nqr - read_as_dict_cols
    str_columns = [cxb__qcyb for cxb__qcyb in str_columns if cxb__qcyb in
        sqzvo__nqr]
    ltf__ipll = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    ltf__ipll.update(read_as_dict_cols)
    dpiqt__axky = pa_schema.names
    xpaqa__qsnz, ysj__bzode = get_pandas_metadata(pa_schema, num_pieces)
    xnia__zsgxw = []
    xcau__nrbe = []
    xznm__hufiw = []
    for ftza__umd, c in enumerate(dpiqt__axky):
        if c in partition_names:
            continue
        cmlp__pwkyq = pa_schema.field(c)
        rbusy__xynh, fmf__brzvb = _get_numba_typ_from_pa_typ(cmlp__pwkyq, c ==
            xpaqa__qsnz, ysj__bzode[c], pq_dataset._category_info,
            str_as_dict=c in ltf__ipll)
        xnia__zsgxw.append(rbusy__xynh)
        xcau__nrbe.append(fmf__brzvb)
        xznm__hufiw.append(cmlp__pwkyq.type)
    if partition_names:
        xnia__zsgxw += [_get_partition_cat_dtype(pq_dataset.
            partitioning_dictionaries[ftza__umd]) for ftza__umd in range(
            len(partition_names))]
        xcau__nrbe.extend([True] * len(partition_names))
        xznm__hufiw.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        dpiqt__axky += [input_file_name_col]
        xnia__zsgxw += [dict_str_arr_type]
        xcau__nrbe.append(True)
        xznm__hufiw.append(None)
    stqyi__rzv = {c: ftza__umd for ftza__umd, c in enumerate(dpiqt__axky)}
    if selected_columns is None:
        selected_columns = dpiqt__axky
    for c in selected_columns:
        if c not in stqyi__rzv:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if xpaqa__qsnz and not isinstance(xpaqa__qsnz, dict
        ) and xpaqa__qsnz not in selected_columns:
        selected_columns.append(xpaqa__qsnz)
    dpiqt__axky = selected_columns
    mrle__lkl = []
    api__sxt = []
    yjb__uvy = []
    klo__bfhzb = []
    for ftza__umd, c in enumerate(dpiqt__axky):
        wuhq__vkrps = stqyi__rzv[c]
        mrle__lkl.append(wuhq__vkrps)
        api__sxt.append(xnia__zsgxw[wuhq__vkrps])
        if not xcau__nrbe[wuhq__vkrps]:
            yjb__uvy.append(ftza__umd)
            klo__bfhzb.append(xznm__hufiw[wuhq__vkrps])
    return (dpiqt__axky, api__sxt, xpaqa__qsnz, mrle__lkl, partition_names,
        yjb__uvy, klo__bfhzb, pa_schema)


def _get_partition_cat_dtype(dictionary):
    assert dictionary is not None
    oefo__yfq = dictionary.to_pandas()
    hiz__hycn = bodo.typeof(oefo__yfq).dtype
    if isinstance(hiz__hycn, types.Integer):
        wxvwo__pzbw = PDCategoricalDtype(tuple(oefo__yfq), hiz__hycn, False,
            int_type=hiz__hycn)
    else:
        wxvwo__pzbw = PDCategoricalDtype(tuple(oefo__yfq), hiz__hycn, False)
    return CategoricalArrayType(wxvwo__pzbw)


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
        ywgx__hggu = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(1), lir.IntType(8).as_pointer(), lir.IntType(1)])
        ucnc__vmya = cgutils.get_or_insert_function(builder.module,
            ywgx__hggu, name='pq_write')
        zbz__nthrr = builder.call(ucnc__vmya, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return zbz__nthrr
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
        ywgx__hggu = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        ucnc__vmya = cgutils.get_or_insert_function(builder.module,
            ywgx__hggu, name='pq_write_partitioned')
        builder.call(ucnc__vmya, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64, types.
        voidptr, types.voidptr), codegen
