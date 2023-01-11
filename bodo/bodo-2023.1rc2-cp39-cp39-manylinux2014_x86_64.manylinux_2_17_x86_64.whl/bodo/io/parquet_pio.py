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
        except OSError as rinda__jlsbn:
            if 'non-file path' in str(rinda__jlsbn):
                raise FileNotFoundError(str(rinda__jlsbn))
            raise


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    bjy__zgu = get_overload_const_str(dnf_filter_str)
    oamu__vnm = get_overload_const_str(expr_filter_str)
    gju__kfn = ', '.join(f'f{fvxln__nolc}' for fvxln__nolc in range(len(
        var_tup)))
    hjv__jcew = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        hjv__jcew += f'  {gju__kfn}, = var_tup\n'
    hjv__jcew += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    hjv__jcew += f'    dnf_filters_py = {bjy__zgu}\n'
    hjv__jcew += f'    expr_filters_py = {oamu__vnm}\n'
    hjv__jcew += '  return (dnf_filters_py, expr_filters_py)\n'
    jifwu__kfbt = {}
    hnof__idba = globals()
    hnof__idba['numba'] = numba
    exec(hjv__jcew, hnof__idba, jifwu__kfbt)
    return jifwu__kfbt['impl']


def unify_schemas(schemas):
    weal__klq = []
    for schema in schemas:
        for fvxln__nolc in range(len(schema)):
            wemjd__ersef = schema.field(fvxln__nolc)
            if wemjd__ersef.type == pa.large_string():
                schema = schema.set(fvxln__nolc, wemjd__ersef.with_type(pa.
                    string()))
            elif wemjd__ersef.type == pa.large_binary():
                schema = schema.set(fvxln__nolc, wemjd__ersef.with_type(pa.
                    binary()))
            elif isinstance(wemjd__ersef.type, (pa.ListType, pa.LargeListType)
                ) and wemjd__ersef.type.value_type in (pa.string(), pa.
                large_string()):
                schema = schema.set(fvxln__nolc, wemjd__ersef.with_type(pa.
                    list_(pa.field(wemjd__ersef.type.value_field.name, pa.
                    string()))))
            elif isinstance(wemjd__ersef.type, pa.LargeListType):
                schema = schema.set(fvxln__nolc, wemjd__ersef.with_type(pa.
                    list_(pa.field(wemjd__ersef.type.value_field.name,
                    wemjd__ersef.type.value_type))))
        weal__klq.append(schema)
    return pa.unify_schemas(weal__klq)


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
        for fvxln__nolc in range(len(self.schema)):
            wemjd__ersef = self.schema.field(fvxln__nolc)
            if wemjd__ersef.type == pa.large_string():
                self.schema = self.schema.set(fvxln__nolc, wemjd__ersef.
                    with_type(pa.string()))
        self.pieces = [ParquetPiece(frag, partitioning, self.
            partition_names) for frag in pa_pq_dataset._dataset.
            get_fragments(filter=pa_pq_dataset._filter_expression)]

    def set_fs(self, fs):
        self.filesystem = fs
        for amj__zwtg in self.pieces:
            amj__zwtg.filesystem = fs

    def __setstate__(self, state):
        self.__dict__ = state
        if self.partition_names:
            lhj__amue = {amj__zwtg: self.partitioning_dictionaries[
                fvxln__nolc] for fvxln__nolc, amj__zwtg in enumerate(self.
                partition_names)}
            self.partitioning = self.partitioning_cls(self.
                partitioning_schema, lhj__amue)


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
            self.partition_keys = [(rinx__othj, partitioning.dictionaries[
                fvxln__nolc].index(self.partition_keys[rinx__othj]).as_py()
                ) for fvxln__nolc, rinx__othj in enumerate(partition_names)]

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
        nehz__qdq = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    gchf__lys = MPI.COMM_WORLD
    if isinstance(fpath, list):
        gzo__sykvj = urlparse(fpath[0])
        protocol = gzo__sykvj.scheme
        xehr__limq = gzo__sykvj.netloc
        for fvxln__nolc in range(len(fpath)):
            wemjd__ersef = fpath[fvxln__nolc]
            jmsdj__vzch = urlparse(wemjd__ersef)
            if jmsdj__vzch.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if jmsdj__vzch.netloc != xehr__limq:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[fvxln__nolc] = wemjd__ersef.rstrip('/')
    else:
        gzo__sykvj = urlparse(fpath)
        protocol = gzo__sykvj.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as epkwv__ptcj:
            izz__dlgtz = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(izz__dlgtz)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as epkwv__ptcj:
            izz__dlgtz = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
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
            kww__rhcha = gcsfs.GCSFileSystem(token=None)
            fs.append(PyFileSystem(FSSpecHandler(kww__rhcha)))
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
            rkq__akges = fs.glob(path)
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(rkq__akges) == 0:
            raise BodoError('No files found matching glob pattern')
        return rkq__akges
    pfyo__kxsu = False
    if get_row_counts:
        rabsa__ovu = getfs(parallel=True)
        pfyo__kxsu = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        sln__tzfet = 1
        anx__uzh = os.cpu_count()
        if anx__uzh is not None and anx__uzh > 1:
            sln__tzfet = anx__uzh // 2
        try:
            if get_row_counts:
                evx__antz = tracing.Event('pq.ParquetDataset', is_parallel=
                    False)
                if tracing.is_tracing():
                    evx__antz.add_attribute('g_dnf_filter', str(dnf_filters))
            rps__toazi = pa.io_thread_count()
            pa.set_io_thread_count(sln__tzfet)
            prefix = ''
            if protocol == 's3':
                prefix = 's3://'
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{gzo__sykvj.netloc}'
            if prefix:
                if isinstance(fpath, list):
                    qqtr__iph = [wemjd__ersef[len(prefix):] for
                        wemjd__ersef in fpath]
                else:
                    qqtr__iph = fpath[len(prefix):]
            else:
                qqtr__iph = fpath
            if isinstance(qqtr__iph, list):
                jvtiw__tko = []
                for amj__zwtg in qqtr__iph:
                    if has_magic(amj__zwtg):
                        jvtiw__tko += glob(protocol, getfs(), amj__zwtg)
                    else:
                        jvtiw__tko.append(amj__zwtg)
                qqtr__iph = jvtiw__tko
            elif has_magic(qqtr__iph):
                qqtr__iph = glob(protocol, getfs(), qqtr__iph)
            kpj__lmy = pq.ParquetDataset(qqtr__iph, filesystem=getfs(),
                filters=None, use_legacy_dataset=False, partitioning=
                partitioning)
            if dnf_filters is not None:
                kpj__lmy._filters = dnf_filters
                kpj__lmy._filter_expression = pq._filters_to_expression(
                    dnf_filters)
            kynlw__yifg = len(kpj__lmy.files)
            kpj__lmy = ParquetDataset(kpj__lmy, prefix)
            pa.set_io_thread_count(rps__toazi)
            if typing_pa_schema:
                kpj__lmy.schema = typing_pa_schema
            if get_row_counts:
                if dnf_filters is not None:
                    evx__antz.add_attribute('num_pieces_before_filter',
                        kynlw__yifg)
                    evx__antz.add_attribute('num_pieces_after_filter', len(
                        kpj__lmy.pieces))
                evx__antz.finalize()
        except Exception as rinda__jlsbn:
            if isinstance(rinda__jlsbn, IsADirectoryError):
                rinda__jlsbn = BodoError(list_of_files_error_msg)
            elif isinstance(fpath, list) and isinstance(rinda__jlsbn, (
                OSError, FileNotFoundError)):
                rinda__jlsbn = BodoError(str(rinda__jlsbn) +
                    list_of_files_error_msg)
            else:
                rinda__jlsbn = BodoError(
                    f"""error from pyarrow: {type(rinda__jlsbn).__name__}: {str(rinda__jlsbn)}
"""
                    )
            gchf__lys.bcast(rinda__jlsbn)
            raise rinda__jlsbn
        if get_row_counts:
            iopgb__nhqo = tracing.Event('bcast dataset')
        kpj__lmy = gchf__lys.bcast(kpj__lmy)
    else:
        if get_row_counts:
            iopgb__nhqo = tracing.Event('bcast dataset')
        kpj__lmy = gchf__lys.bcast(None)
        if isinstance(kpj__lmy, Exception):
            xld__shiv = kpj__lmy
            raise xld__shiv
    kpj__lmy.set_fs(getfs())
    if get_row_counts:
        iopgb__nhqo.finalize()
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = pfyo__kxsu = False
    if get_row_counts or pfyo__kxsu:
        if get_row_counts and tracing.is_tracing():
            epox__isx = tracing.Event('get_row_counts')
            epox__isx.add_attribute('g_num_pieces', len(kpj__lmy.pieces))
            epox__isx.add_attribute('g_expr_filters', str(expr_filters))
        hgbj__bgqav = 0.0
        num_pieces = len(kpj__lmy.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        wqjwi__grv = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        dzm__ydls = 0
        tvam__ifon = 0
        qgvxr__jhlq = 0
        kojq__nknow = True
        if expr_filters is not None:
            import random
            random.seed(37)
            oxuoj__epgyr = random.sample(kpj__lmy.pieces, k=len(kpj__lmy.
                pieces))
        else:
            oxuoj__epgyr = kpj__lmy.pieces
        fpaths = [amj__zwtg.path for amj__zwtg in oxuoj__epgyr[start:
            wqjwi__grv]]
        sln__tzfet = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(sln__tzfet)
        pa.set_cpu_count(sln__tzfet)
        xld__shiv = None
        try:
            blqx__ateqp = ds.dataset(fpaths, filesystem=kpj__lmy.filesystem,
                partitioning=kpj__lmy.partitioning)
            for ezjpl__eksm, frag in zip(oxuoj__epgyr[start:wqjwi__grv],
                blqx__ateqp.get_fragments()):
                if pfyo__kxsu:
                    hlb__apjbg = frag.metadata.schema.to_arrow_schema()
                    oyli__oavu = set(hlb__apjbg.names)
                    wnr__ebkab = set(kpj__lmy.schema.names) - set(kpj__lmy.
                        partition_names)
                    if wnr__ebkab != oyli__oavu:
                        rnar__wpa = oyli__oavu - wnr__ebkab
                        xawfb__esfi = wnr__ebkab - oyli__oavu
                        mqp__vaisq = (
                            f'Schema in {ezjpl__eksm} was different.\n')
                        if typing_pa_schema is not None:
                            if rnar__wpa:
                                mqp__vaisq += f"""File contains column(s) {rnar__wpa} not found in other files in the dataset.
"""
                                raise BodoError(mqp__vaisq)
                        else:
                            if rnar__wpa:
                                mqp__vaisq += f"""File contains column(s) {rnar__wpa} not found in other files in the dataset.
"""
                            if xawfb__esfi:
                                mqp__vaisq += f"""File missing column(s) {xawfb__esfi} found in other files in the dataset.
"""
                            raise BodoError(mqp__vaisq)
                    try:
                        kpj__lmy.schema = unify_schemas([kpj__lmy.schema,
                            hlb__apjbg])
                    except Exception as rinda__jlsbn:
                        mqp__vaisq = (
                            f'Schema in {ezjpl__eksm} was different.\n' +
                            str(rinda__jlsbn))
                        raise BodoError(mqp__vaisq)
                ame__swgw = time.time()
                nqsd__rqdo = frag.scanner(schema=blqx__ateqp.schema, filter
                    =expr_filters, use_threads=True).count_rows()
                hgbj__bgqav += time.time() - ame__swgw
                ezjpl__eksm._bodo_num_rows = nqsd__rqdo
                dzm__ydls += nqsd__rqdo
                tvam__ifon += frag.num_row_groups
                qgvxr__jhlq += sum(xan__onm.total_byte_size for xan__onm in
                    frag.row_groups)
        except Exception as rinda__jlsbn:
            xld__shiv = rinda__jlsbn
        if gchf__lys.allreduce(xld__shiv is not None, op=MPI.LOR):
            for xld__shiv in gchf__lys.allgather(xld__shiv):
                if xld__shiv:
                    if isinstance(fpath, list) and isinstance(xld__shiv, (
                        OSError, FileNotFoundError)):
                        raise BodoError(str(xld__shiv) +
                            list_of_files_error_msg)
                    raise xld__shiv
        if pfyo__kxsu:
            kojq__nknow = gchf__lys.allreduce(kojq__nknow, op=MPI.LAND)
            if not kojq__nknow:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            kpj__lmy._bodo_total_rows = gchf__lys.allreduce(dzm__ydls, op=
                MPI.SUM)
            mxdap__iye = gchf__lys.allreduce(tvam__ifon, op=MPI.SUM)
            nsnq__ikxb = gchf__lys.allreduce(qgvxr__jhlq, op=MPI.SUM)
            toye__tbfq = np.array([amj__zwtg._bodo_num_rows for amj__zwtg in
                kpj__lmy.pieces])
            toye__tbfq = gchf__lys.allreduce(toye__tbfq, op=MPI.SUM)
            for amj__zwtg, axkri__qgv in zip(kpj__lmy.pieces, toye__tbfq):
                amj__zwtg._bodo_num_rows = axkri__qgv
            if is_parallel and bodo.get_rank(
                ) == 0 and mxdap__iye < bodo.get_size() and mxdap__iye != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({mxdap__iye}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()}). For more details, refer to
https://docs.bodo.ai/latest/file_io/#parquet-section.
"""
                    ))
            if mxdap__iye == 0:
                vtops__gxja = 0
            else:
                vtops__gxja = nsnq__ikxb // mxdap__iye
            if (bodo.get_rank() == 0 and nsnq__ikxb >= 20 * 1048576 and 
                vtops__gxja < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({vtops__gxja} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                epox__isx.add_attribute('g_total_num_row_groups', mxdap__iye)
                epox__isx.add_attribute('total_scan_time', hgbj__bgqav)
                zioa__jiqud = np.array([amj__zwtg._bodo_num_rows for
                    amj__zwtg in kpj__lmy.pieces])
                tioer__sgcp = np.percentile(zioa__jiqud, [25, 50, 75])
                epox__isx.add_attribute('g_row_counts_min', zioa__jiqud.min())
                epox__isx.add_attribute('g_row_counts_Q1', tioer__sgcp[0])
                epox__isx.add_attribute('g_row_counts_median', tioer__sgcp[1])
                epox__isx.add_attribute('g_row_counts_Q3', tioer__sgcp[2])
                epox__isx.add_attribute('g_row_counts_max', zioa__jiqud.max())
                epox__isx.add_attribute('g_row_counts_mean', zioa__jiqud.mean()
                    )
                epox__isx.add_attribute('g_row_counts_std', zioa__jiqud.std())
                epox__isx.add_attribute('g_row_counts_sum', zioa__jiqud.sum())
                epox__isx.finalize()
    if read_categories:
        _add_categories_to_pq_dataset(kpj__lmy)
    if get_row_counts:
        nehz__qdq.finalize()
    if pfyo__kxsu:
        if tracing.is_tracing():
            puhe__jjzgk = tracing.Event('unify_schemas_across_ranks')
        xld__shiv = None
        try:
            kpj__lmy.schema = gchf__lys.allreduce(kpj__lmy.schema, bodo.io.
                helpers.pa_schema_unify_mpi_op)
        except Exception as rinda__jlsbn:
            xld__shiv = rinda__jlsbn
        if tracing.is_tracing():
            puhe__jjzgk.finalize()
        if gchf__lys.allreduce(xld__shiv is not None, op=MPI.LOR):
            for xld__shiv in gchf__lys.allgather(xld__shiv):
                if xld__shiv:
                    mqp__vaisq = (f'Schema in some files were different.\n' +
                        str(xld__shiv))
                    raise BodoError(mqp__vaisq)
    return kpj__lmy


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, filesystem, str_as_dict_cols, start_offset,
    rows_to_read, partitioning, schema):
    import pyarrow as pa
    anx__uzh = os.cpu_count()
    if anx__uzh is None or anx__uzh == 0:
        anx__uzh = 2
    yucy__pnkjk = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), anx__uzh)
    llw__yac = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)), anx__uzh)
    if is_parallel and len(fpaths) > llw__yac and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(llw__yac)
        pa.set_cpu_count(llw__yac)
    else:
        pa.set_io_thread_count(yucy__pnkjk)
        pa.set_cpu_count(yucy__pnkjk)
    cgbm__nuqp = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    oiq__lkelu = set(str_as_dict_cols)
    for fvxln__nolc, name in enumerate(schema.names):
        if name in oiq__lkelu:
            huxqf__dojl = schema.field(fvxln__nolc)
            uqk__gjtvd = pa.field(name, pa.dictionary(pa.int32(),
                huxqf__dojl.type), huxqf__dojl.nullable)
            schema = schema.remove(fvxln__nolc).insert(fvxln__nolc, uqk__gjtvd)
    kpj__lmy = ds.dataset(fpaths, filesystem=filesystem, partitioning=
        partitioning, schema=schema, format=cgbm__nuqp)
    vcxm__vkoml = kpj__lmy.schema.names
    yaic__mmor = [vcxm__vkoml[luuds__dud] for luuds__dud in selected_fields]
    seoi__oyb = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if seoi__oyb and expr_filters is None:
        iman__mixan = []
        ancvw__dvjb = 0
        mwdb__yuuh = 0
        for frag in kpj__lmy.get_fragments():
            wvn__alpes = []
            for xan__onm in frag.row_groups:
                jkq__fko = xan__onm.num_rows
                if start_offset < ancvw__dvjb + jkq__fko:
                    if mwdb__yuuh == 0:
                        lde__fjnp = start_offset - ancvw__dvjb
                        ibzo__csnno = min(jkq__fko - lde__fjnp, rows_to_read)
                    else:
                        ibzo__csnno = min(jkq__fko, rows_to_read - mwdb__yuuh)
                    mwdb__yuuh += ibzo__csnno
                    wvn__alpes.append(xan__onm.id)
                ancvw__dvjb += jkq__fko
                if mwdb__yuuh == rows_to_read:
                    break
            iman__mixan.append(frag.subset(row_group_ids=wvn__alpes))
            if mwdb__yuuh == rows_to_read:
                break
        kpj__lmy = ds.FileSystemDataset(iman__mixan, kpj__lmy.schema,
            cgbm__nuqp, filesystem=kpj__lmy.filesystem)
        start_offset = lde__fjnp
    uhhae__vprs = kpj__lmy.scanner(columns=yaic__mmor, filter=expr_filters,
        use_threads=True).to_reader()
    return kpj__lmy, uhhae__vprs, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema
    cbpos__zik = [c for c in pa_schema.names if isinstance(pa_schema.field(
        c).type, pa.DictionaryType) and c not in pq_dataset.partition_names]
    if len(cbpos__zik) == 0:
        pq_dataset._category_info = {}
        return
    gchf__lys = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            zztvn__rjolz = pq_dataset.pieces[0].frag.head(100, columns=
                cbpos__zik)
            nxeqo__nme = {c: tuple(zztvn__rjolz.column(c).chunk(0).
                dictionary.to_pylist()) for c in cbpos__zik}
            del zztvn__rjolz
        except Exception as rinda__jlsbn:
            gchf__lys.bcast(rinda__jlsbn)
            raise rinda__jlsbn
        gchf__lys.bcast(nxeqo__nme)
    else:
        nxeqo__nme = gchf__lys.bcast(None)
        if isinstance(nxeqo__nme, Exception):
            xld__shiv = nxeqo__nme
            raise xld__shiv
    pq_dataset._category_info = nxeqo__nme


def get_pandas_metadata(schema, num_pieces):
    utzvj__ohom = None
    oci__tefcf = defaultdict(lambda : None)
    tlz__cckey = b'pandas'
    if schema.metadata is not None and tlz__cckey in schema.metadata:
        import json
        gnlvp__lhzy = json.loads(schema.metadata[tlz__cckey].decode('utf8'))
        njaam__jhuqe = len(gnlvp__lhzy['index_columns'])
        if njaam__jhuqe > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        utzvj__ohom = gnlvp__lhzy['index_columns'][0] if njaam__jhuqe else None
        if not isinstance(utzvj__ohom, str) and not isinstance(utzvj__ohom,
            dict):
            utzvj__ohom = None
        for cnmw__ntkh in gnlvp__lhzy['columns']:
            nyxzo__msyfj = cnmw__ntkh['name']
            qfrx__dkyat = cnmw__ntkh['pandas_type']
            if (qfrx__dkyat.startswith('int') or qfrx__dkyat.startswith(
                'float')) and nyxzo__msyfj is not None:
                xoyps__edc = cnmw__ntkh['numpy_type']
                if xoyps__edc.startswith('Int') or xoyps__edc.startswith(
                    'Float'):
                    oci__tefcf[nyxzo__msyfj] = True
                else:
                    oci__tefcf[nyxzo__msyfj] = False
    return utzvj__ohom, oci__tefcf


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for nyxzo__msyfj in pa_schema.names:
        yeib__kcre = pa_schema.field(nyxzo__msyfj)
        if yeib__kcre.type in (pa.string(), pa.large_string()):
            str_columns.append(nyxzo__msyfj)
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
    oxuoj__epgyr = pq_dataset.pieces
    if len(oxuoj__epgyr) > bodo.get_size():
        import random
        random.seed(37)
        oxuoj__epgyr = random.sample(oxuoj__epgyr, bodo.get_size())
    else:
        oxuoj__epgyr = oxuoj__epgyr
    if is_iceberg:
        oxuoj__epgyr = [amj__zwtg for amj__zwtg in oxuoj__epgyr if
            _pa_schemas_match(amj__zwtg.metadata.schema.to_arrow_schema(),
            pa_schema)]
    return oxuoj__epgyr


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns: list,
    is_iceberg: bool=False) ->set:
    from mpi4py import MPI
    gchf__lys = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    oxuoj__epgyr = _get_sample_pq_pieces(pq_dataset, pa_schema, is_iceberg)
    str_columns = sorted(str_columns)
    ytzjj__wwls = np.zeros(len(str_columns), dtype=np.int64)
    cht__uhi = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(oxuoj__epgyr):
        ezjpl__eksm = oxuoj__epgyr[bodo.get_rank()]
        try:
            metadata = ezjpl__eksm.metadata
            for fvxln__nolc in range(ezjpl__eksm.num_row_groups):
                for cbqhw__dssfv, nyxzo__msyfj in enumerate(str_columns):
                    alo__rhi = pa_schema.get_field_index(nyxzo__msyfj)
                    ytzjj__wwls[cbqhw__dssfv] += metadata.row_group(fvxln__nolc
                        ).column(alo__rhi).total_uncompressed_size
            bicgc__dyelp = metadata.num_rows
        except Exception as rinda__jlsbn:
            if isinstance(rinda__jlsbn, (OSError, FileNotFoundError)):
                bicgc__dyelp = 0
            else:
                raise
    else:
        bicgc__dyelp = 0
    bhth__mccti = gchf__lys.allreduce(bicgc__dyelp, op=MPI.SUM)
    if bhth__mccti == 0:
        return set()
    gchf__lys.Allreduce(ytzjj__wwls, cht__uhi, op=MPI.SUM)
    fka__ubm = cht__uhi / bhth__mccti
    dxm__fdgq = set()
    for fvxln__nolc, dkjbl__tmtq in enumerate(fka__ubm):
        if dkjbl__tmtq < READ_STR_AS_DICT_THRESHOLD:
            nyxzo__msyfj = str_columns[fvxln__nolc]
            dxm__fdgq.add(nyxzo__msyfj)
    return dxm__fdgq


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None, use_hive=True
    ) ->FileSchema:
    vcxm__vkoml = []
    xkzf__suo = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True, use_hive=
        use_hive)
    partition_names = pq_dataset.partition_names
    pa_schema = pq_dataset.schema
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    pljhe__stxpz = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    ltd__abiqe = read_as_dict_cols - pljhe__stxpz
    if len(ltd__abiqe) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {ltd__abiqe}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(pljhe__stxpz)
    pljhe__stxpz = pljhe__stxpz - read_as_dict_cols
    str_columns = [lfhn__hyfyf for lfhn__hyfyf in str_columns if 
        lfhn__hyfyf in pljhe__stxpz]
    dxm__fdgq = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    dxm__fdgq.update(read_as_dict_cols)
    vcxm__vkoml = pa_schema.names
    utzvj__ohom, oci__tefcf = get_pandas_metadata(pa_schema, num_pieces)
    xpo__wucy = []
    rifgv__peg = []
    hahk__ucs = []
    for fvxln__nolc, c in enumerate(vcxm__vkoml):
        if c in partition_names:
            continue
        yeib__kcre = pa_schema.field(c)
        dmru__ral, qumv__ozqv = _get_numba_typ_from_pa_typ(yeib__kcre, c ==
            utzvj__ohom, oci__tefcf[c], pq_dataset._category_info,
            str_as_dict=c in dxm__fdgq)
        xpo__wucy.append(dmru__ral)
        rifgv__peg.append(qumv__ozqv)
        hahk__ucs.append(yeib__kcre.type)
    if partition_names:
        xpo__wucy += [_get_partition_cat_dtype(pq_dataset.
            partitioning_dictionaries[fvxln__nolc]) for fvxln__nolc in
            range(len(partition_names))]
        rifgv__peg.extend([True] * len(partition_names))
        hahk__ucs.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        vcxm__vkoml += [input_file_name_col]
        xpo__wucy += [dict_str_arr_type]
        rifgv__peg.append(True)
        hahk__ucs.append(None)
    aar__uhlwl = {c: fvxln__nolc for fvxln__nolc, c in enumerate(vcxm__vkoml)}
    if selected_columns is None:
        selected_columns = vcxm__vkoml
    for c in selected_columns:
        if c not in aar__uhlwl:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if utzvj__ohom and not isinstance(utzvj__ohom, dict
        ) and utzvj__ohom not in selected_columns:
        selected_columns.append(utzvj__ohom)
    vcxm__vkoml = selected_columns
    zkx__bew = []
    xkzf__suo = []
    bvqu__pqtxr = []
    gqf__owrk = []
    for fvxln__nolc, c in enumerate(vcxm__vkoml):
        pfkia__yggi = aar__uhlwl[c]
        zkx__bew.append(pfkia__yggi)
        xkzf__suo.append(xpo__wucy[pfkia__yggi])
        if not rifgv__peg[pfkia__yggi]:
            bvqu__pqtxr.append(fvxln__nolc)
            gqf__owrk.append(hahk__ucs[pfkia__yggi])
    return (vcxm__vkoml, xkzf__suo, utzvj__ohom, zkx__bew, partition_names,
        bvqu__pqtxr, gqf__owrk, pa_schema)


def _get_partition_cat_dtype(dictionary):
    assert dictionary is not None
    fhxcm__layys = dictionary.to_pandas()
    czgm__gcy = bodo.typeof(fhxcm__layys).dtype
    if isinstance(czgm__gcy, types.Integer):
        hwvo__nyv = PDCategoricalDtype(tuple(fhxcm__layys), czgm__gcy, 
            False, int_type=czgm__gcy)
    else:
        hwvo__nyv = PDCategoricalDtype(tuple(fhxcm__layys), czgm__gcy, False)
    return CategoricalArrayType(hwvo__nyv)


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
        jtca__moxn = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(1), lir.IntType(8).as_pointer(), lir.IntType(1)])
        hqw__llsg = cgutils.get_or_insert_function(builder.module,
            jtca__moxn, name='pq_write')
        xphhe__mqfut = builder.call(hqw__llsg, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return xphhe__mqfut
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
        jtca__moxn = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        hqw__llsg = cgutils.get_or_insert_function(builder.module,
            jtca__moxn, name='pq_write_partitioned')
        builder.call(hqw__llsg, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64, types.
        voidptr, types.voidptr), codegen
