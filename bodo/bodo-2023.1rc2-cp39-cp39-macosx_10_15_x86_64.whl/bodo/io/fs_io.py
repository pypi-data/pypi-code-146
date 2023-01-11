"""
S3 & Hadoop file system supports, and file system dependent calls
"""
import glob
import os
import warnings
from urllib.parse import urlparse
import llvmlite.binding as ll
import numba
import numpy as np
from fsspec.implementations.arrow import ArrowFile, ArrowFSWrapper, wrap_exceptions
from numba.core import types
from numba.extending import NativeValue, models, overload, register_model, unbox
import bodo
from bodo.io import csv_cpp
from bodo.libs.distributed_api import Reduce_Type
from bodo.libs.str_ext import unicode_to_utf8, unicode_to_utf8_and_len
from bodo.utils.typing import BodoError, BodoWarning, get_overload_constant_dict
from bodo.utils.utils import check_java_installation


def fsspec_arrowfswrapper__open(self, path, mode='rb', block_size=None, **
    kwargs):
    if mode == 'rb':
        try:
            lcu__irq = self.fs.open_input_file(path)
        except:
            lcu__irq = self.fs.open_input_stream(path)
    elif mode == 'wb':
        lcu__irq = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, lcu__irq, path, mode, block_size, **kwargs)


ArrowFSWrapper._open = wrap_exceptions(fsspec_arrowfswrapper__open)
_csv_write = types.ExternalFunction('csv_write', types.void(types.voidptr,
    types.voidptr, types.int64, types.int64, types.bool_, types.voidptr,
    types.voidptr))
ll.add_symbol('csv_write', csv_cpp.csv_write)
bodo_error_msg = """
    Some possible causes:
        (1) Incorrect path: Specified file/directory doesn't exist or is unreachable.
        (2) Missing credentials: You haven't provided S3 credentials, neither through 
            environment variables, nor through a local AWS setup 
            that makes the credentials available at ~/.aws/credentials.
        (3) Incorrect credentials: Your S3 credentials are incorrect or do not have
            the correct permissions.
        (4) Wrong bucket region is used. Set AWS_DEFAULT_REGION variable with correct bucket region.
    """


def get_proxy_uri_from_env_vars():
    return os.environ.get('http_proxy', None) or os.environ.get('https_proxy',
        None) or os.environ.get('HTTP_PROXY', None) or os.environ.get(
        'HTTPS_PROXY', None)


def get_s3_fs(region=None, storage_options=None):
    from pyarrow.fs import S3FileSystem
    pioy__hkkev = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    sehx__lovug = False
    uzijy__dyar = get_proxy_uri_from_env_vars()
    if storage_options:
        sehx__lovug = storage_options.get('anon', False)
    return S3FileSystem(anonymous=sehx__lovug, region=region,
        endpoint_override=pioy__hkkev, proxy_options=uzijy__dyar)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    pioy__hkkev = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    sehx__lovug = False
    uzijy__dyar = get_proxy_uri_from_env_vars()
    if storage_options:
        sehx__lovug = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=pioy__hkkev,
        anonymous=sehx__lovug, proxy_options=uzijy__dyar)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    ecx__hxd = urlparse(path)
    if ecx__hxd.scheme in ('abfs', 'abfss'):
        cip__wuh = path
        if ecx__hxd.port is None:
            wzj__glkcy = 0
        else:
            wzj__glkcy = ecx__hxd.port
        ubtgq__yjdlm = None
    else:
        cip__wuh = ecx__hxd.hostname
        wzj__glkcy = ecx__hxd.port
        ubtgq__yjdlm = ecx__hxd.username
    try:
        fs = HdFS(host=cip__wuh, port=wzj__glkcy, user=ubtgq__yjdlm)
    except Exception as cfvyv__qjtds:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            cfvyv__qjtds))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        vwvby__vqiig = fs.isdir(path)
    except gcsfs.utils.HttpError as cfvyv__qjtds:
        raise BodoError(
            f'{cfvyv__qjtds}. Make sure your google cloud credentials are set!'
            )
    return vwvby__vqiig


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [znm__iea.split('/')[-1] for znm__iea in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        ecx__hxd = urlparse(path)
        ykq__lpzqq = (ecx__hxd.netloc + ecx__hxd.path).rstrip('/')
        qsdq__gvurr = fs.get_file_info(ykq__lpzqq)
        if qsdq__gvurr.type in (pa_fs.FileType.NotFound, pa_fs.FileType.Unknown
            ):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if (not qsdq__gvurr.size and qsdq__gvurr.type == pa_fs.FileType.
            Directory):
            return True
        return False
    except (FileNotFoundError, OSError) as cfvyv__qjtds:
        raise
    except BodoError as tuabu__uoxls:
        raise
    except Exception as cfvyv__qjtds:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(cfvyv__qjtds).__name__}: {str(cfvyv__qjtds)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    pvr__fpq = None
    try:
        if s3_is_directory(fs, path):
            ecx__hxd = urlparse(path)
            ykq__lpzqq = (ecx__hxd.netloc + ecx__hxd.path).rstrip('/')
            erimw__zlmp = pa_fs.FileSelector(ykq__lpzqq, recursive=False)
            bzkuv__ryzr = fs.get_file_info(erimw__zlmp)
            if bzkuv__ryzr and bzkuv__ryzr[0].path in [ykq__lpzqq,
                f'{ykq__lpzqq}/'] and int(bzkuv__ryzr[0].size or 0) == 0:
                bzkuv__ryzr = bzkuv__ryzr[1:]
            pvr__fpq = [brjsk__ohd.base_name for brjsk__ohd in bzkuv__ryzr]
    except BodoError as tuabu__uoxls:
        raise
    except Exception as cfvyv__qjtds:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(cfvyv__qjtds).__name__}: {str(cfvyv__qjtds)}
{bodo_error_msg}"""
            )
    return pvr__fpq


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    ecx__hxd = urlparse(path)
    mvbx__jkziq = ecx__hxd.path
    try:
        sprm__peb = HadoopFileSystem.from_uri(path)
    except Exception as cfvyv__qjtds:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            cfvyv__qjtds))
    xemk__qeem = sprm__peb.get_file_info([mvbx__jkziq])
    if xemk__qeem[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not xemk__qeem[0].size and xemk__qeem[0].type == FileType.Directory:
        return sprm__peb, True
    return sprm__peb, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    pvr__fpq = None
    sprm__peb, vwvby__vqiig = hdfs_is_directory(path)
    if vwvby__vqiig:
        ecx__hxd = urlparse(path)
        mvbx__jkziq = ecx__hxd.path
        erimw__zlmp = FileSelector(mvbx__jkziq, recursive=True)
        try:
            bzkuv__ryzr = sprm__peb.get_file_info(erimw__zlmp)
        except Exception as cfvyv__qjtds:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(mvbx__jkziq, cfvyv__qjtds))
        pvr__fpq = [brjsk__ohd.base_name for brjsk__ohd in bzkuv__ryzr]
    return sprm__peb, pvr__fpq


def abfs_is_directory(path):
    sprm__peb = get_hdfs_fs(path)
    try:
        xemk__qeem = sprm__peb.info(path)
    except OSError as tuabu__uoxls:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if xemk__qeem['size'] == 0 and xemk__qeem['kind'].lower() == 'directory':
        return sprm__peb, True
    return sprm__peb, False


def abfs_list_dir_fnames(path):
    pvr__fpq = None
    sprm__peb, vwvby__vqiig = abfs_is_directory(path)
    if vwvby__vqiig:
        ecx__hxd = urlparse(path)
        mvbx__jkziq = ecx__hxd.path
        try:
            mez__ipg = sprm__peb.ls(mvbx__jkziq)
        except Exception as cfvyv__qjtds:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(mvbx__jkziq, cfvyv__qjtds))
        pvr__fpq = [fname[fname.rindex('/') + 1:] for fname in mez__ipg]
    return sprm__peb, pvr__fpq


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    mot__bxhi = urlparse(path)
    fname = path
    fs = None
    mnv__cmbr = 'read_json' if ftype == 'json' else 'read_csv'
    nks__wrpcl = (
        f'pd.{mnv__cmbr}(): there is no {ftype} file in directory: {fname}')
    vazwn__ecog = directory_of_files_common_filter
    if mot__bxhi.scheme == 's3':
        qjtxh__kay = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        uwhdq__bnib = s3_list_dir_fnames(fs, path)
        ykq__lpzqq = (mot__bxhi.netloc + mot__bxhi.path).rstrip('/')
        fname = ykq__lpzqq
        if uwhdq__bnib:
            uwhdq__bnib = [(ykq__lpzqq + '/' + znm__iea) for znm__iea in
                sorted(filter(vazwn__ecog, uwhdq__bnib))]
            chinq__sxxx = [znm__iea for znm__iea in uwhdq__bnib if int(fs.
                get_file_info(znm__iea).size or 0) > 0]
            if len(chinq__sxxx) == 0:
                raise BodoError(nks__wrpcl)
            fname = chinq__sxxx[0]
        acaz__klk = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        fdcov__wgf = fs._open(fname)
    elif mot__bxhi.scheme == 'hdfs':
        qjtxh__kay = True
        fs, uwhdq__bnib = hdfs_list_dir_fnames(path)
        acaz__klk = fs.get_file_info([mot__bxhi.path])[0].size
        if uwhdq__bnib:
            path = path.rstrip('/')
            uwhdq__bnib = [(path + '/' + znm__iea) for znm__iea in sorted(
                filter(vazwn__ecog, uwhdq__bnib))]
            chinq__sxxx = [znm__iea for znm__iea in uwhdq__bnib if fs.
                get_file_info([urlparse(znm__iea).path])[0].size > 0]
            if len(chinq__sxxx) == 0:
                raise BodoError(nks__wrpcl)
            fname = chinq__sxxx[0]
            fname = urlparse(fname).path
            acaz__klk = fs.get_file_info([fname])[0].size
        fdcov__wgf = fs.open_input_file(fname)
    elif mot__bxhi.scheme in ('abfs', 'abfss'):
        qjtxh__kay = True
        fs, uwhdq__bnib = abfs_list_dir_fnames(path)
        acaz__klk = fs.info(fname)['size']
        if uwhdq__bnib:
            path = path.rstrip('/')
            uwhdq__bnib = [(path + '/' + znm__iea) for znm__iea in sorted(
                filter(vazwn__ecog, uwhdq__bnib))]
            chinq__sxxx = [znm__iea for znm__iea in uwhdq__bnib if fs.info(
                znm__iea)['size'] > 0]
            if len(chinq__sxxx) == 0:
                raise BodoError(nks__wrpcl)
            fname = chinq__sxxx[0]
            acaz__klk = fs.info(fname)['size']
            fname = urlparse(fname).path
        fdcov__wgf = fs.open(fname, 'rb')
    else:
        if mot__bxhi.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {mot__bxhi.scheme}. Please refer to https://docs.bodo.ai/latest/file_io/.'
                )
        qjtxh__kay = False
        if os.path.isdir(path):
            mez__ipg = filter(vazwn__ecog, glob.glob(os.path.join(os.path.
                abspath(path), '*')))
            chinq__sxxx = [znm__iea for znm__iea in sorted(mez__ipg) if os.
                path.getsize(znm__iea) > 0]
            if len(chinq__sxxx) == 0:
                raise BodoError(nks__wrpcl)
            fname = chinq__sxxx[0]
        acaz__klk = os.path.getsize(fname)
        fdcov__wgf = fname
    return qjtxh__kay, fdcov__wgf, acaz__klk, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    bor__xyv = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            natco__sjle, osix__bwnmx = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = natco__sjle.region
        except Exception as cfvyv__qjtds:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{cfvyv__qjtds}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = bor__xyv.bcast(bucket_loc)
    return bucket_loc


@numba.njit()
def get_s3_bucket_region_njit(s3_filepath, parallel):
    with numba.objmode(bucket_loc='unicode_type'):
        bucket_loc = ''
        if isinstance(s3_filepath, list):
            s3_filepath = s3_filepath[0]
        if s3_filepath.startswith('s3://'):
            bucket_loc = get_s3_bucket_region(s3_filepath, parallel)
    return bucket_loc


def csv_write(path_or_buf, D, filename_prefix, is_parallel=False):
    return None


@overload(csv_write, no_unliteral=True)
def csv_write_overload(path_or_buf, D, filename_prefix, is_parallel=False):

    def impl(path_or_buf, D, filename_prefix, is_parallel=False):
        byieg__geild = get_s3_bucket_region_njit(path_or_buf, parallel=
            is_parallel)
        koik__jtzgw, evk__roc = unicode_to_utf8_and_len(D)
        kyyg__jwex = 0
        if is_parallel:
            kyyg__jwex = bodo.libs.distributed_api.dist_exscan(evk__roc, np
                .int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), koik__jtzgw, kyyg__jwex,
            evk__roc, is_parallel, unicode_to_utf8(byieg__geild),
            unicode_to_utf8(filename_prefix))
        bodo.utils.utils.check_and_propagate_cpp_exception()
    return impl


class StorageOptionsDictType(types.Opaque):

    def __init__(self):
        super(StorageOptionsDictType, self).__init__(name=
            'StorageOptionsDictType')


storage_options_dict_type = StorageOptionsDictType()
types.storage_options_dict_type = storage_options_dict_type
register_model(StorageOptionsDictType)(models.OpaqueModel)


@unbox(StorageOptionsDictType)
def unbox_storage_options_dict_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


def get_storage_options_pyobject(storage_options):
    pass


@overload(get_storage_options_pyobject, no_unliteral=True)
def overload_get_storage_options_pyobject(storage_options):
    kobn__efwf = get_overload_constant_dict(storage_options)
    hal__ywu = 'def impl(storage_options):\n'
    hal__ywu += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    hal__ywu += f'    storage_options_py = {str(kobn__efwf)}\n'
    hal__ywu += '  return storage_options_py\n'
    mxx__upy = {}
    exec(hal__ywu, globals(), mxx__upy)
    return mxx__upy['impl']
