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
            hny__coo = self.fs.open_input_file(path)
        except:
            hny__coo = self.fs.open_input_stream(path)
    elif mode == 'wb':
        hny__coo = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, hny__coo, path, mode, block_size, **kwargs)


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
    ffle__nbq = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    jfjay__jgtl = False
    jiw__zulua = get_proxy_uri_from_env_vars()
    if storage_options:
        jfjay__jgtl = storage_options.get('anon', False)
    return S3FileSystem(anonymous=jfjay__jgtl, region=region,
        endpoint_override=ffle__nbq, proxy_options=jiw__zulua)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    ffle__nbq = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    jfjay__jgtl = False
    jiw__zulua = get_proxy_uri_from_env_vars()
    if storage_options:
        jfjay__jgtl = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=ffle__nbq, anonymous
        =jfjay__jgtl, proxy_options=jiw__zulua)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    qenv__znu = urlparse(path)
    if qenv__znu.scheme in ('abfs', 'abfss'):
        tcea__vhb = path
        if qenv__znu.port is None:
            hjp__mvpfx = 0
        else:
            hjp__mvpfx = qenv__znu.port
        uky__syds = None
    else:
        tcea__vhb = qenv__znu.hostname
        hjp__mvpfx = qenv__znu.port
        uky__syds = qenv__znu.username
    try:
        fs = HdFS(host=tcea__vhb, port=hjp__mvpfx, user=uky__syds)
    except Exception as qdad__faonr:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            qdad__faonr))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        npu__avoe = fs.isdir(path)
    except gcsfs.utils.HttpError as qdad__faonr:
        raise BodoError(
            f'{qdad__faonr}. Make sure your google cloud credentials are set!')
    return npu__avoe


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [yumgm__juiog.split('/')[-1] for yumgm__juiog in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        qenv__znu = urlparse(path)
        qkj__ojja = (qenv__znu.netloc + qenv__znu.path).rstrip('/')
        fiyx__kwag = fs.get_file_info(qkj__ojja)
        if fiyx__kwag.type in (pa_fs.FileType.NotFound, pa_fs.FileType.Unknown
            ):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if not fiyx__kwag.size and fiyx__kwag.type == pa_fs.FileType.Directory:
            return True
        return False
    except (FileNotFoundError, OSError) as qdad__faonr:
        raise
    except BodoError as cygk__hsgx:
        raise
    except Exception as qdad__faonr:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(qdad__faonr).__name__}: {str(qdad__faonr)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    fxsb__psgx = None
    try:
        if s3_is_directory(fs, path):
            qenv__znu = urlparse(path)
            qkj__ojja = (qenv__znu.netloc + qenv__znu.path).rstrip('/')
            vfgtr__npq = pa_fs.FileSelector(qkj__ojja, recursive=False)
            tud__uyim = fs.get_file_info(vfgtr__npq)
            if tud__uyim and tud__uyim[0].path in [qkj__ojja, f'{qkj__ojja}/'
                ] and int(tud__uyim[0].size or 0) == 0:
                tud__uyim = tud__uyim[1:]
            fxsb__psgx = [xso__tjcld.base_name for xso__tjcld in tud__uyim]
    except BodoError as cygk__hsgx:
        raise
    except Exception as qdad__faonr:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(qdad__faonr).__name__}: {str(qdad__faonr)}
{bodo_error_msg}"""
            )
    return fxsb__psgx


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    qenv__znu = urlparse(path)
    yqg__oma = qenv__znu.path
    try:
        pki__ftjq = HadoopFileSystem.from_uri(path)
    except Exception as qdad__faonr:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            qdad__faonr))
    bpu__kuucq = pki__ftjq.get_file_info([yqg__oma])
    if bpu__kuucq[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not bpu__kuucq[0].size and bpu__kuucq[0].type == FileType.Directory:
        return pki__ftjq, True
    return pki__ftjq, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    fxsb__psgx = None
    pki__ftjq, npu__avoe = hdfs_is_directory(path)
    if npu__avoe:
        qenv__znu = urlparse(path)
        yqg__oma = qenv__znu.path
        vfgtr__npq = FileSelector(yqg__oma, recursive=True)
        try:
            tud__uyim = pki__ftjq.get_file_info(vfgtr__npq)
        except Exception as qdad__faonr:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(yqg__oma, qdad__faonr))
        fxsb__psgx = [xso__tjcld.base_name for xso__tjcld in tud__uyim]
    return pki__ftjq, fxsb__psgx


def abfs_is_directory(path):
    pki__ftjq = get_hdfs_fs(path)
    try:
        bpu__kuucq = pki__ftjq.info(path)
    except OSError as cygk__hsgx:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if bpu__kuucq['size'] == 0 and bpu__kuucq['kind'].lower() == 'directory':
        return pki__ftjq, True
    return pki__ftjq, False


def abfs_list_dir_fnames(path):
    fxsb__psgx = None
    pki__ftjq, npu__avoe = abfs_is_directory(path)
    if npu__avoe:
        qenv__znu = urlparse(path)
        yqg__oma = qenv__znu.path
        try:
            zoeiw__jcv = pki__ftjq.ls(yqg__oma)
        except Exception as qdad__faonr:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(yqg__oma, qdad__faonr))
        fxsb__psgx = [fname[fname.rindex('/') + 1:] for fname in zoeiw__jcv]
    return pki__ftjq, fxsb__psgx


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    bex__ljmy = urlparse(path)
    fname = path
    fs = None
    xzgjh__icj = 'read_json' if ftype == 'json' else 'read_csv'
    yznhs__vxe = (
        f'pd.{xzgjh__icj}(): there is no {ftype} file in directory: {fname}')
    zrp__lvv = directory_of_files_common_filter
    if bex__ljmy.scheme == 's3':
        ihu__nmag = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        xno__msut = s3_list_dir_fnames(fs, path)
        qkj__ojja = (bex__ljmy.netloc + bex__ljmy.path).rstrip('/')
        fname = qkj__ojja
        if xno__msut:
            xno__msut = [(qkj__ojja + '/' + yumgm__juiog) for yumgm__juiog in
                sorted(filter(zrp__lvv, xno__msut))]
            wpzj__vnr = [yumgm__juiog for yumgm__juiog in xno__msut if int(
                fs.get_file_info(yumgm__juiog).size or 0) > 0]
            if len(wpzj__vnr) == 0:
                raise BodoError(yznhs__vxe)
            fname = wpzj__vnr[0]
        lum__hyy = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        kqci__vzyo = fs._open(fname)
    elif bex__ljmy.scheme == 'hdfs':
        ihu__nmag = True
        fs, xno__msut = hdfs_list_dir_fnames(path)
        lum__hyy = fs.get_file_info([bex__ljmy.path])[0].size
        if xno__msut:
            path = path.rstrip('/')
            xno__msut = [(path + '/' + yumgm__juiog) for yumgm__juiog in
                sorted(filter(zrp__lvv, xno__msut))]
            wpzj__vnr = [yumgm__juiog for yumgm__juiog in xno__msut if fs.
                get_file_info([urlparse(yumgm__juiog).path])[0].size > 0]
            if len(wpzj__vnr) == 0:
                raise BodoError(yznhs__vxe)
            fname = wpzj__vnr[0]
            fname = urlparse(fname).path
            lum__hyy = fs.get_file_info([fname])[0].size
        kqci__vzyo = fs.open_input_file(fname)
    elif bex__ljmy.scheme in ('abfs', 'abfss'):
        ihu__nmag = True
        fs, xno__msut = abfs_list_dir_fnames(path)
        lum__hyy = fs.info(fname)['size']
        if xno__msut:
            path = path.rstrip('/')
            xno__msut = [(path + '/' + yumgm__juiog) for yumgm__juiog in
                sorted(filter(zrp__lvv, xno__msut))]
            wpzj__vnr = [yumgm__juiog for yumgm__juiog in xno__msut if fs.
                info(yumgm__juiog)['size'] > 0]
            if len(wpzj__vnr) == 0:
                raise BodoError(yznhs__vxe)
            fname = wpzj__vnr[0]
            lum__hyy = fs.info(fname)['size']
            fname = urlparse(fname).path
        kqci__vzyo = fs.open(fname, 'rb')
    else:
        if bex__ljmy.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {bex__ljmy.scheme}. Please refer to https://docs.bodo.ai/latest/file_io/.'
                )
        ihu__nmag = False
        if os.path.isdir(path):
            zoeiw__jcv = filter(zrp__lvv, glob.glob(os.path.join(os.path.
                abspath(path), '*')))
            wpzj__vnr = [yumgm__juiog for yumgm__juiog in sorted(zoeiw__jcv
                ) if os.path.getsize(yumgm__juiog) > 0]
            if len(wpzj__vnr) == 0:
                raise BodoError(yznhs__vxe)
            fname = wpzj__vnr[0]
        lum__hyy = os.path.getsize(fname)
        kqci__vzyo = fname
    return ihu__nmag, kqci__vzyo, lum__hyy, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    utlrl__exldp = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            kqo__gaz, twmg__vfwgy = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = kqo__gaz.region
        except Exception as qdad__faonr:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{qdad__faonr}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = utlrl__exldp.bcast(bucket_loc)
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
        ymf__sgcx = get_s3_bucket_region_njit(path_or_buf, parallel=is_parallel
            )
        myi__caux, fevc__gbst = unicode_to_utf8_and_len(D)
        zelp__zrphs = 0
        if is_parallel:
            zelp__zrphs = bodo.libs.distributed_api.dist_exscan(fevc__gbst,
                np.int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), myi__caux, zelp__zrphs,
            fevc__gbst, is_parallel, unicode_to_utf8(ymf__sgcx),
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
    idi__trgi = get_overload_constant_dict(storage_options)
    aygm__gsjj = 'def impl(storage_options):\n'
    aygm__gsjj += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    aygm__gsjj += f'    storage_options_py = {str(idi__trgi)}\n'
    aygm__gsjj += '  return storage_options_py\n'
    lkwb__yegp = {}
    exec(aygm__gsjj, globals(), lkwb__yegp)
    return lkwb__yegp['impl']
