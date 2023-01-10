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
        except OSError as nmxmw__rinec:
            if 'non-file path' in str(nmxmw__rinec):
                raise FileNotFoundError(str(nmxmw__rinec))
            raise


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    qdac__veu = get_overload_const_str(dnf_filter_str)
    rkg__qeam = get_overload_const_str(expr_filter_str)
    rwy__aqi = ', '.join(f'f{vzx__xxem}' for vzx__xxem in range(len(var_tup)))
    mpct__nnilx = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        mpct__nnilx += f'  {rwy__aqi}, = var_tup\n'
    mpct__nnilx += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    mpct__nnilx += f'    dnf_filters_py = {qdac__veu}\n'
    mpct__nnilx += f'    expr_filters_py = {rkg__qeam}\n'
    mpct__nnilx += '  return (dnf_filters_py, expr_filters_py)\n'
    csqxv__bnl = {}
    frmxp__apasf = globals()
    frmxp__apasf['numba'] = numba
    exec(mpct__nnilx, frmxp__apasf, csqxv__bnl)
    return csqxv__bnl['impl']


def unify_schemas(schemas):
    hicw__fvahe = []
    for schema in schemas:
        for vzx__xxem in range(len(schema)):
            hhjo__gnmzt = schema.field(vzx__xxem)
            if hhjo__gnmzt.type == pa.large_string():
                schema = schema.set(vzx__xxem, hhjo__gnmzt.with_type(pa.
                    string()))
            elif hhjo__gnmzt.type == pa.large_binary():
                schema = schema.set(vzx__xxem, hhjo__gnmzt.with_type(pa.
                    binary()))
            elif isinstance(hhjo__gnmzt.type, (pa.ListType, pa.LargeListType)
                ) and hhjo__gnmzt.type.value_type in (pa.string(), pa.
                large_string()):
                schema = schema.set(vzx__xxem, hhjo__gnmzt.with_type(pa.
                    list_(pa.field(hhjo__gnmzt.type.value_field.name, pa.
                    string()))))
            elif isinstance(hhjo__gnmzt.type, pa.LargeListType):
                schema = schema.set(vzx__xxem, hhjo__gnmzt.with_type(pa.
                    list_(pa.field(hhjo__gnmzt.type.value_field.name,
                    hhjo__gnmzt.type.value_type))))
        hicw__fvahe.append(schema)
    return pa.unify_schemas(hicw__fvahe)


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
        for vzx__xxem in range(len(self.schema)):
            hhjo__gnmzt = self.schema.field(vzx__xxem)
            if hhjo__gnmzt.type == pa.large_string():
                self.schema = self.schema.set(vzx__xxem, hhjo__gnmzt.
                    with_type(pa.string()))
        self.pieces = [ParquetPiece(frag, partitioning, self.
            partition_names) for frag in pa_pq_dataset._dataset.
            get_fragments(filter=pa_pq_dataset._filter_expression)]

    def set_fs(self, fs):
        self.filesystem = fs
        for ziqb__bux in self.pieces:
            ziqb__bux.filesystem = fs

    def __setstate__(self, state):
        self.__dict__ = state
        if self.partition_names:
            wwioo__wtjl = {ziqb__bux: self.partitioning_dictionaries[
                vzx__xxem] for vzx__xxem, ziqb__bux in enumerate(self.
                partition_names)}
            self.partitioning = self.partitioning_cls(self.
                partitioning_schema, wwioo__wtjl)


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
            self.partition_keys = [(pyahe__vjpq, partitioning.dictionaries[
                vzx__xxem].index(self.partition_keys[pyahe__vjpq]).as_py()) for
                vzx__xxem, pyahe__vjpq in enumerate(partition_names)]

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
        bgri__goy = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    klgk__tlw = MPI.COMM_WORLD
    if isinstance(fpath, list):
        xniag__vkjdw = urlparse(fpath[0])
        protocol = xniag__vkjdw.scheme
        orogh__dlshv = xniag__vkjdw.netloc
        for vzx__xxem in range(len(fpath)):
            hhjo__gnmzt = fpath[vzx__xxem]
            wqd__cphl = urlparse(hhjo__gnmzt)
            if wqd__cphl.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if wqd__cphl.netloc != orogh__dlshv:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[vzx__xxem] = hhjo__gnmzt.rstrip('/')
    else:
        xniag__vkjdw = urlparse(fpath)
        protocol = xniag__vkjdw.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as cup__uft:
            lppoo__uhp = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(lppoo__uhp)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as cup__uft:
            lppoo__uhp = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
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
            nncdl__mrzp = gcsfs.GCSFileSystem(token=None)
            fs.append(PyFileSystem(FSSpecHandler(nncdl__mrzp)))
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
            thttq__oewcv = fs.glob(path)
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(thttq__oewcv) == 0:
            raise BodoError('No files found matching glob pattern')
        return thttq__oewcv
    zjqru__qwj = False
    if get_row_counts:
        cmvmf__mlfw = getfs(parallel=True)
        zjqru__qwj = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        lry__kqgh = 1
        fzqlj__tyntb = os.cpu_count()
        if fzqlj__tyntb is not None and fzqlj__tyntb > 1:
            lry__kqgh = fzqlj__tyntb // 2
        try:
            if get_row_counts:
                cbn__xqx = tracing.Event('pq.ParquetDataset', is_parallel=False
                    )
                if tracing.is_tracing():
                    cbn__xqx.add_attribute('g_dnf_filter', str(dnf_filters))
            vksb__yqqev = pa.io_thread_count()
            pa.set_io_thread_count(lry__kqgh)
            prefix = ''
            if protocol == 's3':
                prefix = 's3://'
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{xniag__vkjdw.netloc}'
            if prefix:
                if isinstance(fpath, list):
                    agibm__tip = [hhjo__gnmzt[len(prefix):] for hhjo__gnmzt in
                        fpath]
                else:
                    agibm__tip = fpath[len(prefix):]
            else:
                agibm__tip = fpath
            if isinstance(agibm__tip, list):
                qyv__cza = []
                for ziqb__bux in agibm__tip:
                    if has_magic(ziqb__bux):
                        qyv__cza += glob(protocol, getfs(), ziqb__bux)
                    else:
                        qyv__cza.append(ziqb__bux)
                agibm__tip = qyv__cza
            elif has_magic(agibm__tip):
                agibm__tip = glob(protocol, getfs(), agibm__tip)
            miyya__tlkd = pq.ParquetDataset(agibm__tip, filesystem=getfs(),
                filters=None, use_legacy_dataset=False, partitioning=
                partitioning)
            if dnf_filters is not None:
                miyya__tlkd._filters = dnf_filters
                miyya__tlkd._filter_expression = pq._filters_to_expression(
                    dnf_filters)
            zckha__tbfs = len(miyya__tlkd.files)
            miyya__tlkd = ParquetDataset(miyya__tlkd, prefix)
            pa.set_io_thread_count(vksb__yqqev)
            if typing_pa_schema:
                miyya__tlkd.schema = typing_pa_schema
            if get_row_counts:
                if dnf_filters is not None:
                    cbn__xqx.add_attribute('num_pieces_before_filter',
                        zckha__tbfs)
                    cbn__xqx.add_attribute('num_pieces_after_filter', len(
                        miyya__tlkd.pieces))
                cbn__xqx.finalize()
        except Exception as nmxmw__rinec:
            if isinstance(nmxmw__rinec, IsADirectoryError):
                nmxmw__rinec = BodoError(list_of_files_error_msg)
            elif isinstance(fpath, list) and isinstance(nmxmw__rinec, (
                OSError, FileNotFoundError)):
                nmxmw__rinec = BodoError(str(nmxmw__rinec) +
                    list_of_files_error_msg)
            else:
                nmxmw__rinec = BodoError(
                    f"""error from pyarrow: {type(nmxmw__rinec).__name__}: {str(nmxmw__rinec)}
"""
                    )
            klgk__tlw.bcast(nmxmw__rinec)
            raise nmxmw__rinec
        if get_row_counts:
            qvsan__ymbny = tracing.Event('bcast dataset')
        miyya__tlkd = klgk__tlw.bcast(miyya__tlkd)
    else:
        if get_row_counts:
            qvsan__ymbny = tracing.Event('bcast dataset')
        miyya__tlkd = klgk__tlw.bcast(None)
        if isinstance(miyya__tlkd, Exception):
            wiuok__bvqal = miyya__tlkd
            raise wiuok__bvqal
    miyya__tlkd.set_fs(getfs())
    if get_row_counts:
        qvsan__ymbny.finalize()
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = zjqru__qwj = False
    if get_row_counts or zjqru__qwj:
        if get_row_counts and tracing.is_tracing():
            jgej__ilot = tracing.Event('get_row_counts')
            jgej__ilot.add_attribute('g_num_pieces', len(miyya__tlkd.pieces))
            jgej__ilot.add_attribute('g_expr_filters', str(expr_filters))
        gxq__jksdm = 0.0
        num_pieces = len(miyya__tlkd.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        wtkbv__tfq = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        iks__beu = 0
        zafiw__nvj = 0
        jefy__gowl = 0
        vcps__rvbh = True
        if expr_filters is not None:
            import random
            random.seed(37)
            taqjk__yti = random.sample(miyya__tlkd.pieces, k=len(
                miyya__tlkd.pieces))
        else:
            taqjk__yti = miyya__tlkd.pieces
        fpaths = [ziqb__bux.path for ziqb__bux in taqjk__yti[start:wtkbv__tfq]]
        lry__kqgh = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(lry__kqgh)
        pa.set_cpu_count(lry__kqgh)
        wiuok__bvqal = None
        try:
            inz__ywujc = ds.dataset(fpaths, filesystem=miyya__tlkd.
                filesystem, partitioning=miyya__tlkd.partitioning)
            for ujl__vvnp, frag in zip(taqjk__yti[start:wtkbv__tfq],
                inz__ywujc.get_fragments()):
                if zjqru__qwj:
                    maxoq__xej = frag.metadata.schema.to_arrow_schema()
                    kcw__spwl = set(maxoq__xej.names)
                    pkgd__ewete = set(miyya__tlkd.schema.names) - set(
                        miyya__tlkd.partition_names)
                    if pkgd__ewete != kcw__spwl:
                        ehitd__trdra = kcw__spwl - pkgd__ewete
                        cdj__dkol = pkgd__ewete - kcw__spwl
                        nnzwh__qme = f'Schema in {ujl__vvnp} was different.\n'
                        if typing_pa_schema is not None:
                            if ehitd__trdra:
                                nnzwh__qme += f"""File contains column(s) {ehitd__trdra} not found in other files in the dataset.
"""
                                raise BodoError(nnzwh__qme)
                        else:
                            if ehitd__trdra:
                                nnzwh__qme += f"""File contains column(s) {ehitd__trdra} not found in other files in the dataset.
"""
                            if cdj__dkol:
                                nnzwh__qme += f"""File missing column(s) {cdj__dkol} found in other files in the dataset.
"""
                            raise BodoError(nnzwh__qme)
                    try:
                        miyya__tlkd.schema = unify_schemas([miyya__tlkd.
                            schema, maxoq__xej])
                    except Exception as nmxmw__rinec:
                        nnzwh__qme = (
                            f'Schema in {ujl__vvnp} was different.\n' + str
                            (nmxmw__rinec))
                        raise BodoError(nnzwh__qme)
                fncgc__ada = time.time()
                ige__pql = frag.scanner(schema=inz__ywujc.schema, filter=
                    expr_filters, use_threads=True).count_rows()
                gxq__jksdm += time.time() - fncgc__ada
                ujl__vvnp._bodo_num_rows = ige__pql
                iks__beu += ige__pql
                zafiw__nvj += frag.num_row_groups
                jefy__gowl += sum(zpxte__itwaq.total_byte_size for
                    zpxte__itwaq in frag.row_groups)
        except Exception as nmxmw__rinec:
            wiuok__bvqal = nmxmw__rinec
        if klgk__tlw.allreduce(wiuok__bvqal is not None, op=MPI.LOR):
            for wiuok__bvqal in klgk__tlw.allgather(wiuok__bvqal):
                if wiuok__bvqal:
                    if isinstance(fpath, list) and isinstance(wiuok__bvqal,
                        (OSError, FileNotFoundError)):
                        raise BodoError(str(wiuok__bvqal) +
                            list_of_files_error_msg)
                    raise wiuok__bvqal
        if zjqru__qwj:
            vcps__rvbh = klgk__tlw.allreduce(vcps__rvbh, op=MPI.LAND)
            if not vcps__rvbh:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            miyya__tlkd._bodo_total_rows = klgk__tlw.allreduce(iks__beu, op
                =MPI.SUM)
            exshr__wyn = klgk__tlw.allreduce(zafiw__nvj, op=MPI.SUM)
            mph__xojt = klgk__tlw.allreduce(jefy__gowl, op=MPI.SUM)
            pqi__sxn = np.array([ziqb__bux._bodo_num_rows for ziqb__bux in
                miyya__tlkd.pieces])
            pqi__sxn = klgk__tlw.allreduce(pqi__sxn, op=MPI.SUM)
            for ziqb__bux, jvavi__gepc in zip(miyya__tlkd.pieces, pqi__sxn):
                ziqb__bux._bodo_num_rows = jvavi__gepc
            if is_parallel and bodo.get_rank(
                ) == 0 and exshr__wyn < bodo.get_size() and exshr__wyn != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({exshr__wyn}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()}). For more details, refer to
https://docs.bodo.ai/latest/file_io/#parquet-section.
"""
                    ))
            if exshr__wyn == 0:
                egif__kgskq = 0
            else:
                egif__kgskq = mph__xojt // exshr__wyn
            if (bodo.get_rank() == 0 and mph__xojt >= 20 * 1048576 and 
                egif__kgskq < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({egif__kgskq} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                jgej__ilot.add_attribute('g_total_num_row_groups', exshr__wyn)
                jgej__ilot.add_attribute('total_scan_time', gxq__jksdm)
                duva__aohbf = np.array([ziqb__bux._bodo_num_rows for
                    ziqb__bux in miyya__tlkd.pieces])
                lwwlj__mfqn = np.percentile(duva__aohbf, [25, 50, 75])
                jgej__ilot.add_attribute('g_row_counts_min', duva__aohbf.min())
                jgej__ilot.add_attribute('g_row_counts_Q1', lwwlj__mfqn[0])
                jgej__ilot.add_attribute('g_row_counts_median', lwwlj__mfqn[1])
                jgej__ilot.add_attribute('g_row_counts_Q3', lwwlj__mfqn[2])
                jgej__ilot.add_attribute('g_row_counts_max', duva__aohbf.max())
                jgej__ilot.add_attribute('g_row_counts_mean', duva__aohbf.
                    mean())
                jgej__ilot.add_attribute('g_row_counts_std', duva__aohbf.std())
                jgej__ilot.add_attribute('g_row_counts_sum', duva__aohbf.sum())
                jgej__ilot.finalize()
    if read_categories:
        _add_categories_to_pq_dataset(miyya__tlkd)
    if get_row_counts:
        bgri__goy.finalize()
    if zjqru__qwj:
        if tracing.is_tracing():
            otgp__kxbt = tracing.Event('unify_schemas_across_ranks')
        wiuok__bvqal = None
        try:
            miyya__tlkd.schema = klgk__tlw.allreduce(miyya__tlkd.schema,
                bodo.io.helpers.pa_schema_unify_mpi_op)
        except Exception as nmxmw__rinec:
            wiuok__bvqal = nmxmw__rinec
        if tracing.is_tracing():
            otgp__kxbt.finalize()
        if klgk__tlw.allreduce(wiuok__bvqal is not None, op=MPI.LOR):
            for wiuok__bvqal in klgk__tlw.allgather(wiuok__bvqal):
                if wiuok__bvqal:
                    nnzwh__qme = (f'Schema in some files were different.\n' +
                        str(wiuok__bvqal))
                    raise BodoError(nnzwh__qme)
    return miyya__tlkd


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, filesystem, str_as_dict_cols, start_offset,
    rows_to_read, partitioning, schema):
    import pyarrow as pa
    fzqlj__tyntb = os.cpu_count()
    if fzqlj__tyntb is None or fzqlj__tyntb == 0:
        fzqlj__tyntb = 2
    gkbya__dyo = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)),
        fzqlj__tyntb)
    gzrkt__ppyvn = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)),
        fzqlj__tyntb)
    if is_parallel and len(fpaths) > gzrkt__ppyvn and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(gzrkt__ppyvn)
        pa.set_cpu_count(gzrkt__ppyvn)
    else:
        pa.set_io_thread_count(gkbya__dyo)
        pa.set_cpu_count(gkbya__dyo)
    sqlb__vbxr = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    lkp__kakvb = set(str_as_dict_cols)
    for vzx__xxem, name in enumerate(schema.names):
        if name in lkp__kakvb:
            gxnv__sjr = schema.field(vzx__xxem)
            mikdo__qqd = pa.field(name, pa.dictionary(pa.int32(), gxnv__sjr
                .type), gxnv__sjr.nullable)
            schema = schema.remove(vzx__xxem).insert(vzx__xxem, mikdo__qqd)
    miyya__tlkd = ds.dataset(fpaths, filesystem=filesystem, partitioning=
        partitioning, schema=schema, format=sqlb__vbxr)
    gfko__qlnkb = miyya__tlkd.schema.names
    iiqg__alu = [gfko__qlnkb[rvm__npj] for rvm__npj in selected_fields]
    ofcc__cbxqs = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if ofcc__cbxqs and expr_filters is None:
        mik__zqoyr = []
        putcc__clvkv = 0
        msbde__qkkef = 0
        for frag in miyya__tlkd.get_fragments():
            cpx__amdva = []
            for zpxte__itwaq in frag.row_groups:
                xjjx__yge = zpxte__itwaq.num_rows
                if start_offset < putcc__clvkv + xjjx__yge:
                    if msbde__qkkef == 0:
                        glvqb__zuzb = start_offset - putcc__clvkv
                        lfqdg__sgud = min(xjjx__yge - glvqb__zuzb, rows_to_read
                            )
                    else:
                        lfqdg__sgud = min(xjjx__yge, rows_to_read -
                            msbde__qkkef)
                    msbde__qkkef += lfqdg__sgud
                    cpx__amdva.append(zpxte__itwaq.id)
                putcc__clvkv += xjjx__yge
                if msbde__qkkef == rows_to_read:
                    break
            mik__zqoyr.append(frag.subset(row_group_ids=cpx__amdva))
            if msbde__qkkef == rows_to_read:
                break
        miyya__tlkd = ds.FileSystemDataset(mik__zqoyr, miyya__tlkd.schema,
            sqlb__vbxr, filesystem=miyya__tlkd.filesystem)
        start_offset = glvqb__zuzb
    dvyod__ccni = miyya__tlkd.scanner(columns=iiqg__alu, filter=
        expr_filters, use_threads=True).to_reader()
    return miyya__tlkd, dvyod__ccni, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema
    wbow__qses = [c for c in pa_schema.names if isinstance(pa_schema.field(
        c).type, pa.DictionaryType) and c not in pq_dataset.partition_names]
    if len(wbow__qses) == 0:
        pq_dataset._category_info = {}
        return
    klgk__tlw = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            kgll__hen = pq_dataset.pieces[0].frag.head(100, columns=wbow__qses)
            mqv__aose = {c: tuple(kgll__hen.column(c).chunk(0).dictionary.
                to_pylist()) for c in wbow__qses}
            del kgll__hen
        except Exception as nmxmw__rinec:
            klgk__tlw.bcast(nmxmw__rinec)
            raise nmxmw__rinec
        klgk__tlw.bcast(mqv__aose)
    else:
        mqv__aose = klgk__tlw.bcast(None)
        if isinstance(mqv__aose, Exception):
            wiuok__bvqal = mqv__aose
            raise wiuok__bvqal
    pq_dataset._category_info = mqv__aose


def get_pandas_metadata(schema, num_pieces):
    xqj__pxlbm = None
    ovec__vxlaa = defaultdict(lambda : None)
    dch__cri = b'pandas'
    if schema.metadata is not None and dch__cri in schema.metadata:
        import json
        vnhqd__nqd = json.loads(schema.metadata[dch__cri].decode('utf8'))
        rocxq__nnh = len(vnhqd__nqd['index_columns'])
        if rocxq__nnh > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        xqj__pxlbm = vnhqd__nqd['index_columns'][0] if rocxq__nnh else None
        if not isinstance(xqj__pxlbm, str) and not isinstance(xqj__pxlbm, dict
            ):
            xqj__pxlbm = None
        for gncb__xon in vnhqd__nqd['columns']:
            cxzz__jozc = gncb__xon['name']
            ynn__ytsxw = gncb__xon['pandas_type']
            if (ynn__ytsxw.startswith('int') or ynn__ytsxw.startswith('float')
                ) and cxzz__jozc is not None:
                hkv__kawi = gncb__xon['numpy_type']
                if hkv__kawi.startswith('Int') or hkv__kawi.startswith('Float'
                    ):
                    ovec__vxlaa[cxzz__jozc] = True
                else:
                    ovec__vxlaa[cxzz__jozc] = False
    return xqj__pxlbm, ovec__vxlaa


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for cxzz__jozc in pa_schema.names:
        brepi__hha = pa_schema.field(cxzz__jozc)
        if brepi__hha.type in (pa.string(), pa.large_string()):
            str_columns.append(cxzz__jozc)
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
    taqjk__yti = pq_dataset.pieces
    if len(taqjk__yti) > bodo.get_size():
        import random
        random.seed(37)
        taqjk__yti = random.sample(taqjk__yti, bodo.get_size())
    else:
        taqjk__yti = taqjk__yti
    if is_iceberg:
        taqjk__yti = [ziqb__bux for ziqb__bux in taqjk__yti if
            _pa_schemas_match(ziqb__bux.metadata.schema.to_arrow_schema(),
            pa_schema)]
    return taqjk__yti


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns: list,
    is_iceberg: bool=False) ->set:
    from mpi4py import MPI
    klgk__tlw = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    taqjk__yti = _get_sample_pq_pieces(pq_dataset, pa_schema, is_iceberg)
    str_columns = sorted(str_columns)
    vjveq__qjkur = np.zeros(len(str_columns), dtype=np.int64)
    dnt__olg = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(taqjk__yti):
        ujl__vvnp = taqjk__yti[bodo.get_rank()]
        try:
            metadata = ujl__vvnp.metadata
            for vzx__xxem in range(ujl__vvnp.num_row_groups):
                for dpmur__pcuef, cxzz__jozc in enumerate(str_columns):
                    zloy__bjq = pa_schema.get_field_index(cxzz__jozc)
                    vjveq__qjkur[dpmur__pcuef] += metadata.row_group(vzx__xxem
                        ).column(zloy__bjq).total_uncompressed_size
            grm__aydxg = metadata.num_rows
        except Exception as nmxmw__rinec:
            if isinstance(nmxmw__rinec, (OSError, FileNotFoundError)):
                grm__aydxg = 0
            else:
                raise
    else:
        grm__aydxg = 0
    epk__mqgp = klgk__tlw.allreduce(grm__aydxg, op=MPI.SUM)
    if epk__mqgp == 0:
        return set()
    klgk__tlw.Allreduce(vjveq__qjkur, dnt__olg, op=MPI.SUM)
    iqmy__iqqss = dnt__olg / epk__mqgp
    fbdx__kewnb = set()
    for vzx__xxem, jlh__jbqo in enumerate(iqmy__iqqss):
        if jlh__jbqo < READ_STR_AS_DICT_THRESHOLD:
            cxzz__jozc = str_columns[vzx__xxem]
            fbdx__kewnb.add(cxzz__jozc)
    return fbdx__kewnb


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None, use_hive=True
    ) ->FileSchema:
    gfko__qlnkb = []
    kdw__zcwdi = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True, use_hive=
        use_hive)
    partition_names = pq_dataset.partition_names
    pa_schema = pq_dataset.schema
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    gywxx__ttoxn = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    wxjcv__xvozp = read_as_dict_cols - gywxx__ttoxn
    if len(wxjcv__xvozp) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {wxjcv__xvozp}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(gywxx__ttoxn)
    gywxx__ttoxn = gywxx__ttoxn - read_as_dict_cols
    str_columns = [dde__tugnh for dde__tugnh in str_columns if dde__tugnh in
        gywxx__ttoxn]
    fbdx__kewnb = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    fbdx__kewnb.update(read_as_dict_cols)
    gfko__qlnkb = pa_schema.names
    xqj__pxlbm, ovec__vxlaa = get_pandas_metadata(pa_schema, num_pieces)
    ihe__roj = []
    xdb__qrhg = []
    fzxpm__twfjk = []
    for vzx__xxem, c in enumerate(gfko__qlnkb):
        if c in partition_names:
            continue
        brepi__hha = pa_schema.field(c)
        xbnt__jkj, qrsgf__ufrn = _get_numba_typ_from_pa_typ(brepi__hha, c ==
            xqj__pxlbm, ovec__vxlaa[c], pq_dataset._category_info,
            str_as_dict=c in fbdx__kewnb)
        ihe__roj.append(xbnt__jkj)
        xdb__qrhg.append(qrsgf__ufrn)
        fzxpm__twfjk.append(brepi__hha.type)
    if partition_names:
        ihe__roj += [_get_partition_cat_dtype(pq_dataset.
            partitioning_dictionaries[vzx__xxem]) for vzx__xxem in range(
            len(partition_names))]
        xdb__qrhg.extend([True] * len(partition_names))
        fzxpm__twfjk.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        gfko__qlnkb += [input_file_name_col]
        ihe__roj += [dict_str_arr_type]
        xdb__qrhg.append(True)
        fzxpm__twfjk.append(None)
    ehgxa__aus = {c: vzx__xxem for vzx__xxem, c in enumerate(gfko__qlnkb)}
    if selected_columns is None:
        selected_columns = gfko__qlnkb
    for c in selected_columns:
        if c not in ehgxa__aus:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if xqj__pxlbm and not isinstance(xqj__pxlbm, dict
        ) and xqj__pxlbm not in selected_columns:
        selected_columns.append(xqj__pxlbm)
    gfko__qlnkb = selected_columns
    wqnfe__pzrmp = []
    kdw__zcwdi = []
    zfwap__iayhw = []
    tkref__gyh = []
    for vzx__xxem, c in enumerate(gfko__qlnkb):
        zxebm__ztfa = ehgxa__aus[c]
        wqnfe__pzrmp.append(zxebm__ztfa)
        kdw__zcwdi.append(ihe__roj[zxebm__ztfa])
        if not xdb__qrhg[zxebm__ztfa]:
            zfwap__iayhw.append(vzx__xxem)
            tkref__gyh.append(fzxpm__twfjk[zxebm__ztfa])
    return (gfko__qlnkb, kdw__zcwdi, xqj__pxlbm, wqnfe__pzrmp,
        partition_names, zfwap__iayhw, tkref__gyh, pa_schema)


def _get_partition_cat_dtype(dictionary):
    assert dictionary is not None
    ljsel__pdlm = dictionary.to_pandas()
    pgt__clqw = bodo.typeof(ljsel__pdlm).dtype
    if isinstance(pgt__clqw, types.Integer):
        ccxr__wog = PDCategoricalDtype(tuple(ljsel__pdlm), pgt__clqw, False,
            int_type=pgt__clqw)
    else:
        ccxr__wog = PDCategoricalDtype(tuple(ljsel__pdlm), pgt__clqw, False)
    return CategoricalArrayType(ccxr__wog)


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
        pdd__vahdo = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(1), lir.IntType(8).as_pointer(), lir.IntType(1)])
        rrpu__nog = cgutils.get_or_insert_function(builder.module,
            pdd__vahdo, name='pq_write')
        mfsyf__lzejz = builder.call(rrpu__nog, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return mfsyf__lzejz
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
        pdd__vahdo = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        rrpu__nog = cgutils.get_or_insert_function(builder.module,
            pdd__vahdo, name='pq_write_partitioned')
        builder.call(rrpu__nog, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64, types.
        voidptr, types.voidptr), codegen
