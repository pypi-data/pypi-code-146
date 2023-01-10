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
        except OSError as wxau__hse:
            if 'non-file path' in str(wxau__hse):
                raise FileNotFoundError(str(wxau__hse))
            raise


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    nliu__tslqc = get_overload_const_str(dnf_filter_str)
    bzx__yojda = get_overload_const_str(expr_filter_str)
    ihqfu__lpa = ', '.join(f'f{qmd__jmn}' for qmd__jmn in range(len(var_tup)))
    vgist__fbtp = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        vgist__fbtp += f'  {ihqfu__lpa}, = var_tup\n'
    vgist__fbtp += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    vgist__fbtp += f'    dnf_filters_py = {nliu__tslqc}\n'
    vgist__fbtp += f'    expr_filters_py = {bzx__yojda}\n'
    vgist__fbtp += '  return (dnf_filters_py, expr_filters_py)\n'
    ojfu__ctuk = {}
    ysqd__lyx = globals()
    ysqd__lyx['numba'] = numba
    exec(vgist__fbtp, ysqd__lyx, ojfu__ctuk)
    return ojfu__ctuk['impl']


def unify_schemas(schemas):
    gjgj__zlss = []
    for schema in schemas:
        for qmd__jmn in range(len(schema)):
            lhqzs__iaqv = schema.field(qmd__jmn)
            if lhqzs__iaqv.type == pa.large_string():
                schema = schema.set(qmd__jmn, lhqzs__iaqv.with_type(pa.
                    string()))
            elif lhqzs__iaqv.type == pa.large_binary():
                schema = schema.set(qmd__jmn, lhqzs__iaqv.with_type(pa.
                    binary()))
            elif isinstance(lhqzs__iaqv.type, (pa.ListType, pa.LargeListType)
                ) and lhqzs__iaqv.type.value_type in (pa.string(), pa.
                large_string()):
                schema = schema.set(qmd__jmn, lhqzs__iaqv.with_type(pa.
                    list_(pa.field(lhqzs__iaqv.type.value_field.name, pa.
                    string()))))
            elif isinstance(lhqzs__iaqv.type, pa.LargeListType):
                schema = schema.set(qmd__jmn, lhqzs__iaqv.with_type(pa.
                    list_(pa.field(lhqzs__iaqv.type.value_field.name,
                    lhqzs__iaqv.type.value_type))))
        gjgj__zlss.append(schema)
    return pa.unify_schemas(gjgj__zlss)


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
        for qmd__jmn in range(len(self.schema)):
            lhqzs__iaqv = self.schema.field(qmd__jmn)
            if lhqzs__iaqv.type == pa.large_string():
                self.schema = self.schema.set(qmd__jmn, lhqzs__iaqv.
                    with_type(pa.string()))
        self.pieces = [ParquetPiece(frag, partitioning, self.
            partition_names) for frag in pa_pq_dataset._dataset.
            get_fragments(filter=pa_pq_dataset._filter_expression)]

    def set_fs(self, fs):
        self.filesystem = fs
        for byhi__qjg in self.pieces:
            byhi__qjg.filesystem = fs

    def __setstate__(self, state):
        self.__dict__ = state
        if self.partition_names:
            tmvx__sujd = {byhi__qjg: self.partitioning_dictionaries[
                qmd__jmn] for qmd__jmn, byhi__qjg in enumerate(self.
                partition_names)}
            self.partitioning = self.partitioning_cls(self.
                partitioning_schema, tmvx__sujd)


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
            self.partition_keys = [(zyhx__iqny, partitioning.dictionaries[
                qmd__jmn].index(self.partition_keys[zyhx__iqny]).as_py()) for
                qmd__jmn, zyhx__iqny in enumerate(partition_names)]

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
        yezz__syu = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    ijgul__pusgd = MPI.COMM_WORLD
    if isinstance(fpath, list):
        fxbtn__utarj = urlparse(fpath[0])
        protocol = fxbtn__utarj.scheme
        ckj__prd = fxbtn__utarj.netloc
        for qmd__jmn in range(len(fpath)):
            lhqzs__iaqv = fpath[qmd__jmn]
            bvmtq__qblhn = urlparse(lhqzs__iaqv)
            if bvmtq__qblhn.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if bvmtq__qblhn.netloc != ckj__prd:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[qmd__jmn] = lhqzs__iaqv.rstrip('/')
    else:
        fxbtn__utarj = urlparse(fpath)
        protocol = fxbtn__utarj.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as ndbu__exba:
            uksf__zjm = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(uksf__zjm)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as ndbu__exba:
            uksf__zjm = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
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
            vjyj__ocqxi = gcsfs.GCSFileSystem(token=None)
            fs.append(PyFileSystem(FSSpecHandler(vjyj__ocqxi)))
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
            ljyo__xeb = fs.glob(path)
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(ljyo__xeb) == 0:
            raise BodoError('No files found matching glob pattern')
        return ljyo__xeb
    orrfb__gyea = False
    if get_row_counts:
        uovf__gplv = getfs(parallel=True)
        orrfb__gyea = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        srej__skipq = 1
        fau__lnd = os.cpu_count()
        if fau__lnd is not None and fau__lnd > 1:
            srej__skipq = fau__lnd // 2
        try:
            if get_row_counts:
                tzdqf__yitc = tracing.Event('pq.ParquetDataset',
                    is_parallel=False)
                if tracing.is_tracing():
                    tzdqf__yitc.add_attribute('g_dnf_filter', str(dnf_filters))
            evjjo__dic = pa.io_thread_count()
            pa.set_io_thread_count(srej__skipq)
            prefix = ''
            if protocol == 's3':
                prefix = 's3://'
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{fxbtn__utarj.netloc}'
            if prefix:
                if isinstance(fpath, list):
                    pyqtb__obu = [lhqzs__iaqv[len(prefix):] for lhqzs__iaqv in
                        fpath]
                else:
                    pyqtb__obu = fpath[len(prefix):]
            else:
                pyqtb__obu = fpath
            if isinstance(pyqtb__obu, list):
                afi__xwuf = []
                for byhi__qjg in pyqtb__obu:
                    if has_magic(byhi__qjg):
                        afi__xwuf += glob(protocol, getfs(), byhi__qjg)
                    else:
                        afi__xwuf.append(byhi__qjg)
                pyqtb__obu = afi__xwuf
            elif has_magic(pyqtb__obu):
                pyqtb__obu = glob(protocol, getfs(), pyqtb__obu)
            inwmi__jei = pq.ParquetDataset(pyqtb__obu, filesystem=getfs(),
                filters=None, use_legacy_dataset=False, partitioning=
                partitioning)
            if dnf_filters is not None:
                inwmi__jei._filters = dnf_filters
                inwmi__jei._filter_expression = pq._filters_to_expression(
                    dnf_filters)
            bxubc__bvcf = len(inwmi__jei.files)
            inwmi__jei = ParquetDataset(inwmi__jei, prefix)
            pa.set_io_thread_count(evjjo__dic)
            if typing_pa_schema:
                inwmi__jei.schema = typing_pa_schema
            if get_row_counts:
                if dnf_filters is not None:
                    tzdqf__yitc.add_attribute('num_pieces_before_filter',
                        bxubc__bvcf)
                    tzdqf__yitc.add_attribute('num_pieces_after_filter',
                        len(inwmi__jei.pieces))
                tzdqf__yitc.finalize()
        except Exception as wxau__hse:
            if isinstance(wxau__hse, IsADirectoryError):
                wxau__hse = BodoError(list_of_files_error_msg)
            elif isinstance(fpath, list) and isinstance(wxau__hse, (OSError,
                FileNotFoundError)):
                wxau__hse = BodoError(str(wxau__hse) + list_of_files_error_msg)
            else:
                wxau__hse = BodoError(
                    f"""error from pyarrow: {type(wxau__hse).__name__}: {str(wxau__hse)}
"""
                    )
            ijgul__pusgd.bcast(wxau__hse)
            raise wxau__hse
        if get_row_counts:
            qma__nqws = tracing.Event('bcast dataset')
        inwmi__jei = ijgul__pusgd.bcast(inwmi__jei)
    else:
        if get_row_counts:
            qma__nqws = tracing.Event('bcast dataset')
        inwmi__jei = ijgul__pusgd.bcast(None)
        if isinstance(inwmi__jei, Exception):
            dtnd__offs = inwmi__jei
            raise dtnd__offs
    inwmi__jei.set_fs(getfs())
    if get_row_counts:
        qma__nqws.finalize()
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = orrfb__gyea = False
    if get_row_counts or orrfb__gyea:
        if get_row_counts and tracing.is_tracing():
            yemn__wnzfh = tracing.Event('get_row_counts')
            yemn__wnzfh.add_attribute('g_num_pieces', len(inwmi__jei.pieces))
            yemn__wnzfh.add_attribute('g_expr_filters', str(expr_filters))
        bvf__urv = 0.0
        num_pieces = len(inwmi__jei.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        hvamr__rvelz = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        cgh__dhn = 0
        acg__kmsw = 0
        cka__qjt = 0
        bzvuo__mflp = True
        if expr_filters is not None:
            import random
            random.seed(37)
            offu__vhv = random.sample(inwmi__jei.pieces, k=len(inwmi__jei.
                pieces))
        else:
            offu__vhv = inwmi__jei.pieces
        fpaths = [byhi__qjg.path for byhi__qjg in offu__vhv[start:hvamr__rvelz]
            ]
        srej__skipq = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(srej__skipq)
        pa.set_cpu_count(srej__skipq)
        dtnd__offs = None
        try:
            ufr__tgagy = ds.dataset(fpaths, filesystem=inwmi__jei.
                filesystem, partitioning=inwmi__jei.partitioning)
            for zcm__tsd, frag in zip(offu__vhv[start:hvamr__rvelz],
                ufr__tgagy.get_fragments()):
                if orrfb__gyea:
                    wfd__iuu = frag.metadata.schema.to_arrow_schema()
                    tfff__wyq = set(wfd__iuu.names)
                    mlqly__btnp = set(inwmi__jei.schema.names) - set(inwmi__jei
                        .partition_names)
                    if mlqly__btnp != tfff__wyq:
                        wvn__kvn = tfff__wyq - mlqly__btnp
                        yvlnb__icfyp = mlqly__btnp - tfff__wyq
                        akizy__cbp = f'Schema in {zcm__tsd} was different.\n'
                        if typing_pa_schema is not None:
                            if wvn__kvn:
                                akizy__cbp += f"""File contains column(s) {wvn__kvn} not found in other files in the dataset.
"""
                                raise BodoError(akizy__cbp)
                        else:
                            if wvn__kvn:
                                akizy__cbp += f"""File contains column(s) {wvn__kvn} not found in other files in the dataset.
"""
                            if yvlnb__icfyp:
                                akizy__cbp += f"""File missing column(s) {yvlnb__icfyp} found in other files in the dataset.
"""
                            raise BodoError(akizy__cbp)
                    try:
                        inwmi__jei.schema = unify_schemas([inwmi__jei.
                            schema, wfd__iuu])
                    except Exception as wxau__hse:
                        akizy__cbp = (
                            f'Schema in {zcm__tsd} was different.\n' + str(
                            wxau__hse))
                        raise BodoError(akizy__cbp)
                pdrk__cfgl = time.time()
                fzm__avx = frag.scanner(schema=ufr__tgagy.schema, filter=
                    expr_filters, use_threads=True).count_rows()
                bvf__urv += time.time() - pdrk__cfgl
                zcm__tsd._bodo_num_rows = fzm__avx
                cgh__dhn += fzm__avx
                acg__kmsw += frag.num_row_groups
                cka__qjt += sum(jlu__yawb.total_byte_size for jlu__yawb in
                    frag.row_groups)
        except Exception as wxau__hse:
            dtnd__offs = wxau__hse
        if ijgul__pusgd.allreduce(dtnd__offs is not None, op=MPI.LOR):
            for dtnd__offs in ijgul__pusgd.allgather(dtnd__offs):
                if dtnd__offs:
                    if isinstance(fpath, list) and isinstance(dtnd__offs, (
                        OSError, FileNotFoundError)):
                        raise BodoError(str(dtnd__offs) +
                            list_of_files_error_msg)
                    raise dtnd__offs
        if orrfb__gyea:
            bzvuo__mflp = ijgul__pusgd.allreduce(bzvuo__mflp, op=MPI.LAND)
            if not bzvuo__mflp:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            inwmi__jei._bodo_total_rows = ijgul__pusgd.allreduce(cgh__dhn,
                op=MPI.SUM)
            gjb__jzxq = ijgul__pusgd.allreduce(acg__kmsw, op=MPI.SUM)
            dclb__oes = ijgul__pusgd.allreduce(cka__qjt, op=MPI.SUM)
            ufvq__viq = np.array([byhi__qjg._bodo_num_rows for byhi__qjg in
                inwmi__jei.pieces])
            ufvq__viq = ijgul__pusgd.allreduce(ufvq__viq, op=MPI.SUM)
            for byhi__qjg, mfloq__varf in zip(inwmi__jei.pieces, ufvq__viq):
                byhi__qjg._bodo_num_rows = mfloq__varf
            if is_parallel and bodo.get_rank(
                ) == 0 and gjb__jzxq < bodo.get_size() and gjb__jzxq != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({gjb__jzxq}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()}). For more details, refer to
https://docs.bodo.ai/latest/file_io/#parquet-section.
"""
                    ))
            if gjb__jzxq == 0:
                ivtw__mcids = 0
            else:
                ivtw__mcids = dclb__oes // gjb__jzxq
            if (bodo.get_rank() == 0 and dclb__oes >= 20 * 1048576 and 
                ivtw__mcids < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({ivtw__mcids} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                yemn__wnzfh.add_attribute('g_total_num_row_groups', gjb__jzxq)
                yemn__wnzfh.add_attribute('total_scan_time', bvf__urv)
                ggyer__ypn = np.array([byhi__qjg._bodo_num_rows for
                    byhi__qjg in inwmi__jei.pieces])
                vogr__cai = np.percentile(ggyer__ypn, [25, 50, 75])
                yemn__wnzfh.add_attribute('g_row_counts_min', ggyer__ypn.min())
                yemn__wnzfh.add_attribute('g_row_counts_Q1', vogr__cai[0])
                yemn__wnzfh.add_attribute('g_row_counts_median', vogr__cai[1])
                yemn__wnzfh.add_attribute('g_row_counts_Q3', vogr__cai[2])
                yemn__wnzfh.add_attribute('g_row_counts_max', ggyer__ypn.max())
                yemn__wnzfh.add_attribute('g_row_counts_mean', ggyer__ypn.
                    mean())
                yemn__wnzfh.add_attribute('g_row_counts_std', ggyer__ypn.std())
                yemn__wnzfh.add_attribute('g_row_counts_sum', ggyer__ypn.sum())
                yemn__wnzfh.finalize()
    if read_categories:
        _add_categories_to_pq_dataset(inwmi__jei)
    if get_row_counts:
        yezz__syu.finalize()
    if orrfb__gyea:
        if tracing.is_tracing():
            jct__flq = tracing.Event('unify_schemas_across_ranks')
        dtnd__offs = None
        try:
            inwmi__jei.schema = ijgul__pusgd.allreduce(inwmi__jei.schema,
                bodo.io.helpers.pa_schema_unify_mpi_op)
        except Exception as wxau__hse:
            dtnd__offs = wxau__hse
        if tracing.is_tracing():
            jct__flq.finalize()
        if ijgul__pusgd.allreduce(dtnd__offs is not None, op=MPI.LOR):
            for dtnd__offs in ijgul__pusgd.allgather(dtnd__offs):
                if dtnd__offs:
                    akizy__cbp = (f'Schema in some files were different.\n' +
                        str(dtnd__offs))
                    raise BodoError(akizy__cbp)
    return inwmi__jei


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, filesystem, str_as_dict_cols, start_offset,
    rows_to_read, partitioning, schema):
    import pyarrow as pa
    fau__lnd = os.cpu_count()
    if fau__lnd is None or fau__lnd == 0:
        fau__lnd = 2
    ama__bwix = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), fau__lnd)
    zozxt__jbmz = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)), fau__lnd)
    if is_parallel and len(fpaths) > zozxt__jbmz and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(zozxt__jbmz)
        pa.set_cpu_count(zozxt__jbmz)
    else:
        pa.set_io_thread_count(ama__bwix)
        pa.set_cpu_count(ama__bwix)
    jtpjy__pkv = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    ysctf__opc = set(str_as_dict_cols)
    for qmd__jmn, name in enumerate(schema.names):
        if name in ysctf__opc:
            vkvm__euxe = schema.field(qmd__jmn)
            jxzhy__tcx = pa.field(name, pa.dictionary(pa.int32(),
                vkvm__euxe.type), vkvm__euxe.nullable)
            schema = schema.remove(qmd__jmn).insert(qmd__jmn, jxzhy__tcx)
    inwmi__jei = ds.dataset(fpaths, filesystem=filesystem, partitioning=
        partitioning, schema=schema, format=jtpjy__pkv)
    lsm__xqej = inwmi__jei.schema.names
    urt__vrra = [lsm__xqej[otxi__wipue] for otxi__wipue in selected_fields]
    dekh__pwx = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if dekh__pwx and expr_filters is None:
        adb__xasxq = []
        kfk__gto = 0
        ksgc__xjame = 0
        for frag in inwmi__jei.get_fragments():
            ypc__wnjw = []
            for jlu__yawb in frag.row_groups:
                zzqg__oik = jlu__yawb.num_rows
                if start_offset < kfk__gto + zzqg__oik:
                    if ksgc__xjame == 0:
                        vtc__fpqj = start_offset - kfk__gto
                        mwaqs__iewai = min(zzqg__oik - vtc__fpqj, rows_to_read)
                    else:
                        mwaqs__iewai = min(zzqg__oik, rows_to_read -
                            ksgc__xjame)
                    ksgc__xjame += mwaqs__iewai
                    ypc__wnjw.append(jlu__yawb.id)
                kfk__gto += zzqg__oik
                if ksgc__xjame == rows_to_read:
                    break
            adb__xasxq.append(frag.subset(row_group_ids=ypc__wnjw))
            if ksgc__xjame == rows_to_read:
                break
        inwmi__jei = ds.FileSystemDataset(adb__xasxq, inwmi__jei.schema,
            jtpjy__pkv, filesystem=inwmi__jei.filesystem)
        start_offset = vtc__fpqj
    ofo__adb = inwmi__jei.scanner(columns=urt__vrra, filter=expr_filters,
        use_threads=True).to_reader()
    return inwmi__jei, ofo__adb, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema
    jsqng__xmgcc = [c for c in pa_schema.names if isinstance(pa_schema.
        field(c).type, pa.DictionaryType) and c not in pq_dataset.
        partition_names]
    if len(jsqng__xmgcc) == 0:
        pq_dataset._category_info = {}
        return
    ijgul__pusgd = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            ykzbs__krba = pq_dataset.pieces[0].frag.head(100, columns=
                jsqng__xmgcc)
            porlg__xumyn = {c: tuple(ykzbs__krba.column(c).chunk(0).
                dictionary.to_pylist()) for c in jsqng__xmgcc}
            del ykzbs__krba
        except Exception as wxau__hse:
            ijgul__pusgd.bcast(wxau__hse)
            raise wxau__hse
        ijgul__pusgd.bcast(porlg__xumyn)
    else:
        porlg__xumyn = ijgul__pusgd.bcast(None)
        if isinstance(porlg__xumyn, Exception):
            dtnd__offs = porlg__xumyn
            raise dtnd__offs
    pq_dataset._category_info = porlg__xumyn


def get_pandas_metadata(schema, num_pieces):
    rmmv__oaf = None
    mke__pvdx = defaultdict(lambda : None)
    uqfhi__owr = b'pandas'
    if schema.metadata is not None and uqfhi__owr in schema.metadata:
        import json
        siuew__csv = json.loads(schema.metadata[uqfhi__owr].decode('utf8'))
        bwk__yzags = len(siuew__csv['index_columns'])
        if bwk__yzags > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        rmmv__oaf = siuew__csv['index_columns'][0] if bwk__yzags else None
        if not isinstance(rmmv__oaf, str) and not isinstance(rmmv__oaf, dict):
            rmmv__oaf = None
        for uxmn__kdzaf in siuew__csv['columns']:
            rcaa__tmkjp = uxmn__kdzaf['name']
            bgtt__ydo = uxmn__kdzaf['pandas_type']
            if (bgtt__ydo.startswith('int') or bgtt__ydo.startswith('float')
                ) and rcaa__tmkjp is not None:
                jce__kovlf = uxmn__kdzaf['numpy_type']
                if jce__kovlf.startswith('Int') or jce__kovlf.startswith(
                    'Float'):
                    mke__pvdx[rcaa__tmkjp] = True
                else:
                    mke__pvdx[rcaa__tmkjp] = False
    return rmmv__oaf, mke__pvdx


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for rcaa__tmkjp in pa_schema.names:
        jxb__lejoz = pa_schema.field(rcaa__tmkjp)
        if jxb__lejoz.type in (pa.string(), pa.large_string()):
            str_columns.append(rcaa__tmkjp)
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
    offu__vhv = pq_dataset.pieces
    if len(offu__vhv) > bodo.get_size():
        import random
        random.seed(37)
        offu__vhv = random.sample(offu__vhv, bodo.get_size())
    else:
        offu__vhv = offu__vhv
    if is_iceberg:
        offu__vhv = [byhi__qjg for byhi__qjg in offu__vhv if
            _pa_schemas_match(byhi__qjg.metadata.schema.to_arrow_schema(),
            pa_schema)]
    return offu__vhv


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns: list,
    is_iceberg: bool=False) ->set:
    from mpi4py import MPI
    ijgul__pusgd = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    offu__vhv = _get_sample_pq_pieces(pq_dataset, pa_schema, is_iceberg)
    str_columns = sorted(str_columns)
    xuja__siosh = np.zeros(len(str_columns), dtype=np.int64)
    cbjkd__tdyq = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(offu__vhv):
        zcm__tsd = offu__vhv[bodo.get_rank()]
        try:
            metadata = zcm__tsd.metadata
            for qmd__jmn in range(zcm__tsd.num_row_groups):
                for hjpb__lmviu, rcaa__tmkjp in enumerate(str_columns):
                    phr__krvoo = pa_schema.get_field_index(rcaa__tmkjp)
                    xuja__siosh[hjpb__lmviu] += metadata.row_group(qmd__jmn
                        ).column(phr__krvoo).total_uncompressed_size
            izp__stsir = metadata.num_rows
        except Exception as wxau__hse:
            if isinstance(wxau__hse, (OSError, FileNotFoundError)):
                izp__stsir = 0
            else:
                raise
    else:
        izp__stsir = 0
    eepi__qqgt = ijgul__pusgd.allreduce(izp__stsir, op=MPI.SUM)
    if eepi__qqgt == 0:
        return set()
    ijgul__pusgd.Allreduce(xuja__siosh, cbjkd__tdyq, op=MPI.SUM)
    diz__wqq = cbjkd__tdyq / eepi__qqgt
    aeir__plhlw = set()
    for qmd__jmn, yrz__vqbvn in enumerate(diz__wqq):
        if yrz__vqbvn < READ_STR_AS_DICT_THRESHOLD:
            rcaa__tmkjp = str_columns[qmd__jmn]
            aeir__plhlw.add(rcaa__tmkjp)
    return aeir__plhlw


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None, use_hive=True
    ) ->FileSchema:
    lsm__xqej = []
    glf__hta = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True, use_hive=
        use_hive)
    partition_names = pq_dataset.partition_names
    pa_schema = pq_dataset.schema
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    dndit__yjo = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    izr__yzftf = read_as_dict_cols - dndit__yjo
    if len(izr__yzftf) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {izr__yzftf}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(dndit__yjo)
    dndit__yjo = dndit__yjo - read_as_dict_cols
    str_columns = [rbfuv__zoxq for rbfuv__zoxq in str_columns if 
        rbfuv__zoxq in dndit__yjo]
    aeir__plhlw = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    aeir__plhlw.update(read_as_dict_cols)
    lsm__xqej = pa_schema.names
    rmmv__oaf, mke__pvdx = get_pandas_metadata(pa_schema, num_pieces)
    qvhjz__wehn = []
    vkt__ptz = []
    uie__gplpo = []
    for qmd__jmn, c in enumerate(lsm__xqej):
        if c in partition_names:
            continue
        jxb__lejoz = pa_schema.field(c)
        rjlui__elds, cqg__czile = _get_numba_typ_from_pa_typ(jxb__lejoz, c ==
            rmmv__oaf, mke__pvdx[c], pq_dataset._category_info, str_as_dict
            =c in aeir__plhlw)
        qvhjz__wehn.append(rjlui__elds)
        vkt__ptz.append(cqg__czile)
        uie__gplpo.append(jxb__lejoz.type)
    if partition_names:
        qvhjz__wehn += [_get_partition_cat_dtype(pq_dataset.
            partitioning_dictionaries[qmd__jmn]) for qmd__jmn in range(len(
            partition_names))]
        vkt__ptz.extend([True] * len(partition_names))
        uie__gplpo.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        lsm__xqej += [input_file_name_col]
        qvhjz__wehn += [dict_str_arr_type]
        vkt__ptz.append(True)
        uie__gplpo.append(None)
    wbcfb__mdom = {c: qmd__jmn for qmd__jmn, c in enumerate(lsm__xqej)}
    if selected_columns is None:
        selected_columns = lsm__xqej
    for c in selected_columns:
        if c not in wbcfb__mdom:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if rmmv__oaf and not isinstance(rmmv__oaf, dict
        ) and rmmv__oaf not in selected_columns:
        selected_columns.append(rmmv__oaf)
    lsm__xqej = selected_columns
    ich__zfbc = []
    glf__hta = []
    dvqck__usm = []
    vysr__iejg = []
    for qmd__jmn, c in enumerate(lsm__xqej):
        sfmll__tad = wbcfb__mdom[c]
        ich__zfbc.append(sfmll__tad)
        glf__hta.append(qvhjz__wehn[sfmll__tad])
        if not vkt__ptz[sfmll__tad]:
            dvqck__usm.append(qmd__jmn)
            vysr__iejg.append(uie__gplpo[sfmll__tad])
    return (lsm__xqej, glf__hta, rmmv__oaf, ich__zfbc, partition_names,
        dvqck__usm, vysr__iejg, pa_schema)


def _get_partition_cat_dtype(dictionary):
    assert dictionary is not None
    zrvj__xycrq = dictionary.to_pandas()
    lihvk__lvrgl = bodo.typeof(zrvj__xycrq).dtype
    if isinstance(lihvk__lvrgl, types.Integer):
        hwldf__pkx = PDCategoricalDtype(tuple(zrvj__xycrq), lihvk__lvrgl, 
            False, int_type=lihvk__lvrgl)
    else:
        hwldf__pkx = PDCategoricalDtype(tuple(zrvj__xycrq), lihvk__lvrgl, False
            )
    return CategoricalArrayType(hwldf__pkx)


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
        fvc__hkjw = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(1), lir.IntType(8).as_pointer(), lir.IntType(1)])
        odl__kayu = cgutils.get_or_insert_function(builder.module,
            fvc__hkjw, name='pq_write')
        lnfk__myor = builder.call(odl__kayu, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return lnfk__myor
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
        fvc__hkjw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        odl__kayu = cgutils.get_or_insert_function(builder.module,
            fvc__hkjw, name='pq_write_partitioned')
        builder.call(odl__kayu, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64, types.
        voidptr, types.voidptr), codegen
