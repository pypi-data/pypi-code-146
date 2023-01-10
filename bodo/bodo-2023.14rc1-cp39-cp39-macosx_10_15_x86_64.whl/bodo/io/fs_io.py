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
            kuygn__zhw = self.fs.open_input_file(path)
        except:
            kuygn__zhw = self.fs.open_input_stream(path)
    elif mode == 'wb':
        kuygn__zhw = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, kuygn__zhw, path, mode, block_size, **kwargs)


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
    cbb__log = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    rcwnq__tpjhr = False
    jqw__kcowh = get_proxy_uri_from_env_vars()
    if storage_options:
        rcwnq__tpjhr = storage_options.get('anon', False)
    return S3FileSystem(anonymous=rcwnq__tpjhr, region=region,
        endpoint_override=cbb__log, proxy_options=jqw__kcowh)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    cbb__log = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    rcwnq__tpjhr = False
    jqw__kcowh = get_proxy_uri_from_env_vars()
    if storage_options:
        rcwnq__tpjhr = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=cbb__log, anonymous=
        rcwnq__tpjhr, proxy_options=jqw__kcowh)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    fzct__rug = urlparse(path)
    if fzct__rug.scheme in ('abfs', 'abfss'):
        nnq__hsgas = path
        if fzct__rug.port is None:
            lhsoy__rfq = 0
        else:
            lhsoy__rfq = fzct__rug.port
        scxlp__lerg = None
    else:
        nnq__hsgas = fzct__rug.hostname
        lhsoy__rfq = fzct__rug.port
        scxlp__lerg = fzct__rug.username
    try:
        fs = HdFS(host=nnq__hsgas, port=lhsoy__rfq, user=scxlp__lerg)
    except Exception as upn__kypj:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            upn__kypj))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        emvww__jtvsl = fs.isdir(path)
    except gcsfs.utils.HttpError as upn__kypj:
        raise BodoError(
            f'{upn__kypj}. Make sure your google cloud credentials are set!')
    return emvww__jtvsl


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [ymix__jiksi.split('/')[-1] for ymix__jiksi in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        fzct__rug = urlparse(path)
        lbk__qmry = (fzct__rug.netloc + fzct__rug.path).rstrip('/')
        gle__icj = fs.get_file_info(lbk__qmry)
        if gle__icj.type in (pa_fs.FileType.NotFound, pa_fs.FileType.Unknown):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if not gle__icj.size and gle__icj.type == pa_fs.FileType.Directory:
            return True
        return False
    except (FileNotFoundError, OSError) as upn__kypj:
        raise
    except BodoError as ifu__sjpp:
        raise
    except Exception as upn__kypj:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(upn__kypj).__name__}: {str(upn__kypj)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    hbr__mkl = None
    try:
        if s3_is_directory(fs, path):
            fzct__rug = urlparse(path)
            lbk__qmry = (fzct__rug.netloc + fzct__rug.path).rstrip('/')
            mrifu__sktz = pa_fs.FileSelector(lbk__qmry, recursive=False)
            xrfzp__dkou = fs.get_file_info(mrifu__sktz)
            if xrfzp__dkou and xrfzp__dkou[0].path in [lbk__qmry,
                f'{lbk__qmry}/'] and int(xrfzp__dkou[0].size or 0) == 0:
                xrfzp__dkou = xrfzp__dkou[1:]
            hbr__mkl = [ynyb__dogj.base_name for ynyb__dogj in xrfzp__dkou]
    except BodoError as ifu__sjpp:
        raise
    except Exception as upn__kypj:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(upn__kypj).__name__}: {str(upn__kypj)}
{bodo_error_msg}"""
            )
    return hbr__mkl


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    fzct__rug = urlparse(path)
    jaxb__cvm = fzct__rug.path
    try:
        lmkt__pzcb = HadoopFileSystem.from_uri(path)
    except Exception as upn__kypj:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            upn__kypj))
    gms__ytdbr = lmkt__pzcb.get_file_info([jaxb__cvm])
    if gms__ytdbr[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not gms__ytdbr[0].size and gms__ytdbr[0].type == FileType.Directory:
        return lmkt__pzcb, True
    return lmkt__pzcb, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    hbr__mkl = None
    lmkt__pzcb, emvww__jtvsl = hdfs_is_directory(path)
    if emvww__jtvsl:
        fzct__rug = urlparse(path)
        jaxb__cvm = fzct__rug.path
        mrifu__sktz = FileSelector(jaxb__cvm, recursive=True)
        try:
            xrfzp__dkou = lmkt__pzcb.get_file_info(mrifu__sktz)
        except Exception as upn__kypj:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(jaxb__cvm, upn__kypj))
        hbr__mkl = [ynyb__dogj.base_name for ynyb__dogj in xrfzp__dkou]
    return lmkt__pzcb, hbr__mkl


def abfs_is_directory(path):
    lmkt__pzcb = get_hdfs_fs(path)
    try:
        gms__ytdbr = lmkt__pzcb.info(path)
    except OSError as ifu__sjpp:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if gms__ytdbr['size'] == 0 and gms__ytdbr['kind'].lower() == 'directory':
        return lmkt__pzcb, True
    return lmkt__pzcb, False


def abfs_list_dir_fnames(path):
    hbr__mkl = None
    lmkt__pzcb, emvww__jtvsl = abfs_is_directory(path)
    if emvww__jtvsl:
        fzct__rug = urlparse(path)
        jaxb__cvm = fzct__rug.path
        try:
            hlycf__ump = lmkt__pzcb.ls(jaxb__cvm)
        except Exception as upn__kypj:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(jaxb__cvm, upn__kypj))
        hbr__mkl = [fname[fname.rindex('/') + 1:] for fname in hlycf__ump]
    return lmkt__pzcb, hbr__mkl


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    wzsj__dyqgw = urlparse(path)
    fname = path
    fs = None
    qxw__eym = 'read_json' if ftype == 'json' else 'read_csv'
    jcamd__vle = (
        f'pd.{qxw__eym}(): there is no {ftype} file in directory: {fname}')
    ljljf__kbp = directory_of_files_common_filter
    if wzsj__dyqgw.scheme == 's3':
        wpm__osvwc = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        pwcim__frk = s3_list_dir_fnames(fs, path)
        lbk__qmry = (wzsj__dyqgw.netloc + wzsj__dyqgw.path).rstrip('/')
        fname = lbk__qmry
        if pwcim__frk:
            pwcim__frk = [(lbk__qmry + '/' + ymix__jiksi) for ymix__jiksi in
                sorted(filter(ljljf__kbp, pwcim__frk))]
            ykc__tqyky = [ymix__jiksi for ymix__jiksi in pwcim__frk if int(
                fs.get_file_info(ymix__jiksi).size or 0) > 0]
            if len(ykc__tqyky) == 0:
                raise BodoError(jcamd__vle)
            fname = ykc__tqyky[0]
        xhbic__kwwh = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        hsd__hkau = fs._open(fname)
    elif wzsj__dyqgw.scheme == 'hdfs':
        wpm__osvwc = True
        fs, pwcim__frk = hdfs_list_dir_fnames(path)
        xhbic__kwwh = fs.get_file_info([wzsj__dyqgw.path])[0].size
        if pwcim__frk:
            path = path.rstrip('/')
            pwcim__frk = [(path + '/' + ymix__jiksi) for ymix__jiksi in
                sorted(filter(ljljf__kbp, pwcim__frk))]
            ykc__tqyky = [ymix__jiksi for ymix__jiksi in pwcim__frk if fs.
                get_file_info([urlparse(ymix__jiksi).path])[0].size > 0]
            if len(ykc__tqyky) == 0:
                raise BodoError(jcamd__vle)
            fname = ykc__tqyky[0]
            fname = urlparse(fname).path
            xhbic__kwwh = fs.get_file_info([fname])[0].size
        hsd__hkau = fs.open_input_file(fname)
    elif wzsj__dyqgw.scheme in ('abfs', 'abfss'):
        wpm__osvwc = True
        fs, pwcim__frk = abfs_list_dir_fnames(path)
        xhbic__kwwh = fs.info(fname)['size']
        if pwcim__frk:
            path = path.rstrip('/')
            pwcim__frk = [(path + '/' + ymix__jiksi) for ymix__jiksi in
                sorted(filter(ljljf__kbp, pwcim__frk))]
            ykc__tqyky = [ymix__jiksi for ymix__jiksi in pwcim__frk if fs.
                info(ymix__jiksi)['size'] > 0]
            if len(ykc__tqyky) == 0:
                raise BodoError(jcamd__vle)
            fname = ykc__tqyky[0]
            xhbic__kwwh = fs.info(fname)['size']
            fname = urlparse(fname).path
        hsd__hkau = fs.open(fname, 'rb')
    else:
        if wzsj__dyqgw.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {wzsj__dyqgw.scheme}. Please refer to https://docs.bodo.ai/latest/file_io/.'
                )
        wpm__osvwc = False
        if os.path.isdir(path):
            hlycf__ump = filter(ljljf__kbp, glob.glob(os.path.join(os.path.
                abspath(path), '*')))
            ykc__tqyky = [ymix__jiksi for ymix__jiksi in sorted(hlycf__ump) if
                os.path.getsize(ymix__jiksi) > 0]
            if len(ykc__tqyky) == 0:
                raise BodoError(jcamd__vle)
            fname = ykc__tqyky[0]
        xhbic__kwwh = os.path.getsize(fname)
        hsd__hkau = fname
    return wpm__osvwc, hsd__hkau, xhbic__kwwh, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    cwgn__wavq = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            wdchr__wfn, npu__bqwg = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = wdchr__wfn.region
        except Exception as upn__kypj:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{upn__kypj}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = cwgn__wavq.bcast(bucket_loc)
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
        apt__uml = get_s3_bucket_region_njit(path_or_buf, parallel=is_parallel)
        emsv__sqk, ldlr__oter = unicode_to_utf8_and_len(D)
        rtqw__xijd = 0
        if is_parallel:
            rtqw__xijd = bodo.libs.distributed_api.dist_exscan(ldlr__oter,
                np.int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), emsv__sqk, rtqw__xijd,
            ldlr__oter, is_parallel, unicode_to_utf8(apt__uml),
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
    hatqz__lmfxh = get_overload_constant_dict(storage_options)
    htmh__okoj = 'def impl(storage_options):\n'
    htmh__okoj += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    htmh__okoj += f'    storage_options_py = {str(hatqz__lmfxh)}\n'
    htmh__okoj += '  return storage_options_py\n'
    yxw__dyq = {}
    exec(htmh__okoj, globals(), yxw__dyq)
    return yxw__dyq['impl']
