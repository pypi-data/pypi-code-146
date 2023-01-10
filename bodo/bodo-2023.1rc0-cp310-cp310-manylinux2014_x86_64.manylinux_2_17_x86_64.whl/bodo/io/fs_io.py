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
            zcjvq__ymxfm = self.fs.open_input_file(path)
        except:
            zcjvq__ymxfm = self.fs.open_input_stream(path)
    elif mode == 'wb':
        zcjvq__ymxfm = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, zcjvq__ymxfm, path, mode, block_size, **kwargs)


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
    xszwq__nwo = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    tcq__rlxb = False
    afz__kjrhc = get_proxy_uri_from_env_vars()
    if storage_options:
        tcq__rlxb = storage_options.get('anon', False)
    return S3FileSystem(anonymous=tcq__rlxb, region=region,
        endpoint_override=xszwq__nwo, proxy_options=afz__kjrhc)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    xszwq__nwo = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    tcq__rlxb = False
    afz__kjrhc = get_proxy_uri_from_env_vars()
    if storage_options:
        tcq__rlxb = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=xszwq__nwo,
        anonymous=tcq__rlxb, proxy_options=afz__kjrhc)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    wrjfd__ztlpe = urlparse(path)
    if wrjfd__ztlpe.scheme in ('abfs', 'abfss'):
        wviz__ciz = path
        if wrjfd__ztlpe.port is None:
            gyvn__dqtg = 0
        else:
            gyvn__dqtg = wrjfd__ztlpe.port
        uor__maqe = None
    else:
        wviz__ciz = wrjfd__ztlpe.hostname
        gyvn__dqtg = wrjfd__ztlpe.port
        uor__maqe = wrjfd__ztlpe.username
    try:
        fs = HdFS(host=wviz__ciz, port=gyvn__dqtg, user=uor__maqe)
    except Exception as xfob__hfnkt:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            xfob__hfnkt))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        ccjh__xcp = fs.isdir(path)
    except gcsfs.utils.HttpError as xfob__hfnkt:
        raise BodoError(
            f'{xfob__hfnkt}. Make sure your google cloud credentials are set!')
    return ccjh__xcp


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [nstfs__fqper.split('/')[-1] for nstfs__fqper in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        wrjfd__ztlpe = urlparse(path)
        znsw__kct = (wrjfd__ztlpe.netloc + wrjfd__ztlpe.path).rstrip('/')
        hxmnn__vtjbj = fs.get_file_info(znsw__kct)
        if hxmnn__vtjbj.type in (pa_fs.FileType.NotFound, pa_fs.FileType.
            Unknown):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if (not hxmnn__vtjbj.size and hxmnn__vtjbj.type == pa_fs.FileType.
            Directory):
            return True
        return False
    except (FileNotFoundError, OSError) as xfob__hfnkt:
        raise
    except BodoError as fcbj__prd:
        raise
    except Exception as xfob__hfnkt:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(xfob__hfnkt).__name__}: {str(xfob__hfnkt)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    geol__xvqex = None
    try:
        if s3_is_directory(fs, path):
            wrjfd__ztlpe = urlparse(path)
            znsw__kct = (wrjfd__ztlpe.netloc + wrjfd__ztlpe.path).rstrip('/')
            etoj__tfnzu = pa_fs.FileSelector(znsw__kct, recursive=False)
            tbjxq__jusi = fs.get_file_info(etoj__tfnzu)
            if tbjxq__jusi and tbjxq__jusi[0].path in [znsw__kct,
                f'{znsw__kct}/'] and int(tbjxq__jusi[0].size or 0) == 0:
                tbjxq__jusi = tbjxq__jusi[1:]
            geol__xvqex = [njvvy__tzqk.base_name for njvvy__tzqk in tbjxq__jusi
                ]
    except BodoError as fcbj__prd:
        raise
    except Exception as xfob__hfnkt:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(xfob__hfnkt).__name__}: {str(xfob__hfnkt)}
{bodo_error_msg}"""
            )
    return geol__xvqex


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    wrjfd__ztlpe = urlparse(path)
    ijo__hhbs = wrjfd__ztlpe.path
    try:
        opu__leqt = HadoopFileSystem.from_uri(path)
    except Exception as xfob__hfnkt:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            xfob__hfnkt))
    tfd__yoeo = opu__leqt.get_file_info([ijo__hhbs])
    if tfd__yoeo[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not tfd__yoeo[0].size and tfd__yoeo[0].type == FileType.Directory:
        return opu__leqt, True
    return opu__leqt, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    geol__xvqex = None
    opu__leqt, ccjh__xcp = hdfs_is_directory(path)
    if ccjh__xcp:
        wrjfd__ztlpe = urlparse(path)
        ijo__hhbs = wrjfd__ztlpe.path
        etoj__tfnzu = FileSelector(ijo__hhbs, recursive=True)
        try:
            tbjxq__jusi = opu__leqt.get_file_info(etoj__tfnzu)
        except Exception as xfob__hfnkt:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(ijo__hhbs, xfob__hfnkt))
        geol__xvqex = [njvvy__tzqk.base_name for njvvy__tzqk in tbjxq__jusi]
    return opu__leqt, geol__xvqex


def abfs_is_directory(path):
    opu__leqt = get_hdfs_fs(path)
    try:
        tfd__yoeo = opu__leqt.info(path)
    except OSError as fcbj__prd:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if tfd__yoeo['size'] == 0 and tfd__yoeo['kind'].lower() == 'directory':
        return opu__leqt, True
    return opu__leqt, False


def abfs_list_dir_fnames(path):
    geol__xvqex = None
    opu__leqt, ccjh__xcp = abfs_is_directory(path)
    if ccjh__xcp:
        wrjfd__ztlpe = urlparse(path)
        ijo__hhbs = wrjfd__ztlpe.path
        try:
            irkbf__fvaru = opu__leqt.ls(ijo__hhbs)
        except Exception as xfob__hfnkt:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(ijo__hhbs, xfob__hfnkt))
        geol__xvqex = [fname[fname.rindex('/') + 1:] for fname in irkbf__fvaru]
    return opu__leqt, geol__xvqex


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    cegu__xrtf = urlparse(path)
    fname = path
    fs = None
    fdgr__pjmru = 'read_json' if ftype == 'json' else 'read_csv'
    ztyh__eunv = (
        f'pd.{fdgr__pjmru}(): there is no {ftype} file in directory: {fname}')
    hkry__uawxb = directory_of_files_common_filter
    if cegu__xrtf.scheme == 's3':
        djbhd__qzo = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        ojj__woa = s3_list_dir_fnames(fs, path)
        znsw__kct = (cegu__xrtf.netloc + cegu__xrtf.path).rstrip('/')
        fname = znsw__kct
        if ojj__woa:
            ojj__woa = [(znsw__kct + '/' + nstfs__fqper) for nstfs__fqper in
                sorted(filter(hkry__uawxb, ojj__woa))]
            dytks__noo = [nstfs__fqper for nstfs__fqper in ojj__woa if int(
                fs.get_file_info(nstfs__fqper).size or 0) > 0]
            if len(dytks__noo) == 0:
                raise BodoError(ztyh__eunv)
            fname = dytks__noo[0]
        bof__limew = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        uywv__gorku = fs._open(fname)
    elif cegu__xrtf.scheme == 'hdfs':
        djbhd__qzo = True
        fs, ojj__woa = hdfs_list_dir_fnames(path)
        bof__limew = fs.get_file_info([cegu__xrtf.path])[0].size
        if ojj__woa:
            path = path.rstrip('/')
            ojj__woa = [(path + '/' + nstfs__fqper) for nstfs__fqper in
                sorted(filter(hkry__uawxb, ojj__woa))]
            dytks__noo = [nstfs__fqper for nstfs__fqper in ojj__woa if fs.
                get_file_info([urlparse(nstfs__fqper).path])[0].size > 0]
            if len(dytks__noo) == 0:
                raise BodoError(ztyh__eunv)
            fname = dytks__noo[0]
            fname = urlparse(fname).path
            bof__limew = fs.get_file_info([fname])[0].size
        uywv__gorku = fs.open_input_file(fname)
    elif cegu__xrtf.scheme in ('abfs', 'abfss'):
        djbhd__qzo = True
        fs, ojj__woa = abfs_list_dir_fnames(path)
        bof__limew = fs.info(fname)['size']
        if ojj__woa:
            path = path.rstrip('/')
            ojj__woa = [(path + '/' + nstfs__fqper) for nstfs__fqper in
                sorted(filter(hkry__uawxb, ojj__woa))]
            dytks__noo = [nstfs__fqper for nstfs__fqper in ojj__woa if fs.
                info(nstfs__fqper)['size'] > 0]
            if len(dytks__noo) == 0:
                raise BodoError(ztyh__eunv)
            fname = dytks__noo[0]
            bof__limew = fs.info(fname)['size']
            fname = urlparse(fname).path
        uywv__gorku = fs.open(fname, 'rb')
    else:
        if cegu__xrtf.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {cegu__xrtf.scheme}. Please refer to https://docs.bodo.ai/latest/file_io/.'
                )
        djbhd__qzo = False
        if os.path.isdir(path):
            irkbf__fvaru = filter(hkry__uawxb, glob.glob(os.path.join(os.
                path.abspath(path), '*')))
            dytks__noo = [nstfs__fqper for nstfs__fqper in sorted(
                irkbf__fvaru) if os.path.getsize(nstfs__fqper) > 0]
            if len(dytks__noo) == 0:
                raise BodoError(ztyh__eunv)
            fname = dytks__noo[0]
        bof__limew = os.path.getsize(fname)
        uywv__gorku = fname
    return djbhd__qzo, uywv__gorku, bof__limew, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    eszk__gfjs = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            zgm__gjgk, vnm__qcm = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = zgm__gjgk.region
        except Exception as xfob__hfnkt:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{xfob__hfnkt}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = eszk__gfjs.bcast(bucket_loc)
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
        wwhnh__ihqyl = get_s3_bucket_region_njit(path_or_buf, parallel=
            is_parallel)
        joeiy__inua, zepu__phml = unicode_to_utf8_and_len(D)
        snd__roibv = 0
        if is_parallel:
            snd__roibv = bodo.libs.distributed_api.dist_exscan(zepu__phml,
                np.int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), joeiy__inua, snd__roibv,
            zepu__phml, is_parallel, unicode_to_utf8(wwhnh__ihqyl),
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
    gmhkb__xiawr = get_overload_constant_dict(storage_options)
    ctut__wrny = 'def impl(storage_options):\n'
    ctut__wrny += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    ctut__wrny += f'    storage_options_py = {str(gmhkb__xiawr)}\n'
    ctut__wrny += '  return storage_options_py\n'
    edqj__ifs = {}
    exec(ctut__wrny, globals(), edqj__ifs)
    return edqj__ifs['impl']
