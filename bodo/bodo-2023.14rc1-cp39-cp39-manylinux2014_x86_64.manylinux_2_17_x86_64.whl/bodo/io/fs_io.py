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
            heg__adz = self.fs.open_input_file(path)
        except:
            heg__adz = self.fs.open_input_stream(path)
    elif mode == 'wb':
        heg__adz = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, heg__adz, path, mode, block_size, **kwargs)


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
    yaxpc__bnv = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    ybp__opzg = False
    dic__sygp = get_proxy_uri_from_env_vars()
    if storage_options:
        ybp__opzg = storage_options.get('anon', False)
    return S3FileSystem(anonymous=ybp__opzg, region=region,
        endpoint_override=yaxpc__bnv, proxy_options=dic__sygp)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    yaxpc__bnv = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    ybp__opzg = False
    dic__sygp = get_proxy_uri_from_env_vars()
    if storage_options:
        ybp__opzg = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=yaxpc__bnv,
        anonymous=ybp__opzg, proxy_options=dic__sygp)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    rayb__zbcih = urlparse(path)
    if rayb__zbcih.scheme in ('abfs', 'abfss'):
        ifiea__kwo = path
        if rayb__zbcih.port is None:
            hxmu__goal = 0
        else:
            hxmu__goal = rayb__zbcih.port
        vyoq__vbez = None
    else:
        ifiea__kwo = rayb__zbcih.hostname
        hxmu__goal = rayb__zbcih.port
        vyoq__vbez = rayb__zbcih.username
    try:
        fs = HdFS(host=ifiea__kwo, port=hxmu__goal, user=vyoq__vbez)
    except Exception as qya__dsxlm:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            qya__dsxlm))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        paavz__bgmht = fs.isdir(path)
    except gcsfs.utils.HttpError as qya__dsxlm:
        raise BodoError(
            f'{qya__dsxlm}. Make sure your google cloud credentials are set!')
    return paavz__bgmht


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [bpvy__eopo.split('/')[-1] for bpvy__eopo in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        rayb__zbcih = urlparse(path)
        dfm__bcd = (rayb__zbcih.netloc + rayb__zbcih.path).rstrip('/')
        gfl__rda = fs.get_file_info(dfm__bcd)
        if gfl__rda.type in (pa_fs.FileType.NotFound, pa_fs.FileType.Unknown):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if not gfl__rda.size and gfl__rda.type == pa_fs.FileType.Directory:
            return True
        return False
    except (FileNotFoundError, OSError) as qya__dsxlm:
        raise
    except BodoError as cyto__vxvu:
        raise
    except Exception as qya__dsxlm:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(qya__dsxlm).__name__}: {str(qya__dsxlm)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    uobg__rdjf = None
    try:
        if s3_is_directory(fs, path):
            rayb__zbcih = urlparse(path)
            dfm__bcd = (rayb__zbcih.netloc + rayb__zbcih.path).rstrip('/')
            bercs__joma = pa_fs.FileSelector(dfm__bcd, recursive=False)
            uchzq__tolqs = fs.get_file_info(bercs__joma)
            if uchzq__tolqs and uchzq__tolqs[0].path in [dfm__bcd,
                f'{dfm__bcd}/'] and int(uchzq__tolqs[0].size or 0) == 0:
                uchzq__tolqs = uchzq__tolqs[1:]
            uobg__rdjf = [afwdz__fdhu.base_name for afwdz__fdhu in uchzq__tolqs
                ]
    except BodoError as cyto__vxvu:
        raise
    except Exception as qya__dsxlm:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(qya__dsxlm).__name__}: {str(qya__dsxlm)}
{bodo_error_msg}"""
            )
    return uobg__rdjf


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    rayb__zbcih = urlparse(path)
    msem__iiun = rayb__zbcih.path
    try:
        aljmk__bbnq = HadoopFileSystem.from_uri(path)
    except Exception as qya__dsxlm:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            qya__dsxlm))
    vvyxf__uggbl = aljmk__bbnq.get_file_info([msem__iiun])
    if vvyxf__uggbl[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not vvyxf__uggbl[0].size and vvyxf__uggbl[0].type == FileType.Directory:
        return aljmk__bbnq, True
    return aljmk__bbnq, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    uobg__rdjf = None
    aljmk__bbnq, paavz__bgmht = hdfs_is_directory(path)
    if paavz__bgmht:
        rayb__zbcih = urlparse(path)
        msem__iiun = rayb__zbcih.path
        bercs__joma = FileSelector(msem__iiun, recursive=True)
        try:
            uchzq__tolqs = aljmk__bbnq.get_file_info(bercs__joma)
        except Exception as qya__dsxlm:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(msem__iiun, qya__dsxlm))
        uobg__rdjf = [afwdz__fdhu.base_name for afwdz__fdhu in uchzq__tolqs]
    return aljmk__bbnq, uobg__rdjf


def abfs_is_directory(path):
    aljmk__bbnq = get_hdfs_fs(path)
    try:
        vvyxf__uggbl = aljmk__bbnq.info(path)
    except OSError as cyto__vxvu:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if vvyxf__uggbl['size'] == 0 and vvyxf__uggbl['kind'].lower(
        ) == 'directory':
        return aljmk__bbnq, True
    return aljmk__bbnq, False


def abfs_list_dir_fnames(path):
    uobg__rdjf = None
    aljmk__bbnq, paavz__bgmht = abfs_is_directory(path)
    if paavz__bgmht:
        rayb__zbcih = urlparse(path)
        msem__iiun = rayb__zbcih.path
        try:
            gjbth__xrq = aljmk__bbnq.ls(msem__iiun)
        except Exception as qya__dsxlm:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(msem__iiun, qya__dsxlm))
        uobg__rdjf = [fname[fname.rindex('/') + 1:] for fname in gjbth__xrq]
    return aljmk__bbnq, uobg__rdjf


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    rujc__qoie = urlparse(path)
    fname = path
    fs = None
    ychr__higrd = 'read_json' if ftype == 'json' else 'read_csv'
    sdi__lgupu = (
        f'pd.{ychr__higrd}(): there is no {ftype} file in directory: {fname}')
    xajh__bhgn = directory_of_files_common_filter
    if rujc__qoie.scheme == 's3':
        bzbo__kcv = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        sumxi__xnopa = s3_list_dir_fnames(fs, path)
        dfm__bcd = (rujc__qoie.netloc + rujc__qoie.path).rstrip('/')
        fname = dfm__bcd
        if sumxi__xnopa:
            sumxi__xnopa = [(dfm__bcd + '/' + bpvy__eopo) for bpvy__eopo in
                sorted(filter(xajh__bhgn, sumxi__xnopa))]
            imxjz__xryh = [bpvy__eopo for bpvy__eopo in sumxi__xnopa if int
                (fs.get_file_info(bpvy__eopo).size or 0) > 0]
            if len(imxjz__xryh) == 0:
                raise BodoError(sdi__lgupu)
            fname = imxjz__xryh[0]
        bnqio__ixx = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        eaj__rzcqk = fs._open(fname)
    elif rujc__qoie.scheme == 'hdfs':
        bzbo__kcv = True
        fs, sumxi__xnopa = hdfs_list_dir_fnames(path)
        bnqio__ixx = fs.get_file_info([rujc__qoie.path])[0].size
        if sumxi__xnopa:
            path = path.rstrip('/')
            sumxi__xnopa = [(path + '/' + bpvy__eopo) for bpvy__eopo in
                sorted(filter(xajh__bhgn, sumxi__xnopa))]
            imxjz__xryh = [bpvy__eopo for bpvy__eopo in sumxi__xnopa if fs.
                get_file_info([urlparse(bpvy__eopo).path])[0].size > 0]
            if len(imxjz__xryh) == 0:
                raise BodoError(sdi__lgupu)
            fname = imxjz__xryh[0]
            fname = urlparse(fname).path
            bnqio__ixx = fs.get_file_info([fname])[0].size
        eaj__rzcqk = fs.open_input_file(fname)
    elif rujc__qoie.scheme in ('abfs', 'abfss'):
        bzbo__kcv = True
        fs, sumxi__xnopa = abfs_list_dir_fnames(path)
        bnqio__ixx = fs.info(fname)['size']
        if sumxi__xnopa:
            path = path.rstrip('/')
            sumxi__xnopa = [(path + '/' + bpvy__eopo) for bpvy__eopo in
                sorted(filter(xajh__bhgn, sumxi__xnopa))]
            imxjz__xryh = [bpvy__eopo for bpvy__eopo in sumxi__xnopa if fs.
                info(bpvy__eopo)['size'] > 0]
            if len(imxjz__xryh) == 0:
                raise BodoError(sdi__lgupu)
            fname = imxjz__xryh[0]
            bnqio__ixx = fs.info(fname)['size']
            fname = urlparse(fname).path
        eaj__rzcqk = fs.open(fname, 'rb')
    else:
        if rujc__qoie.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {rujc__qoie.scheme}. Please refer to https://docs.bodo.ai/latest/file_io/.'
                )
        bzbo__kcv = False
        if os.path.isdir(path):
            gjbth__xrq = filter(xajh__bhgn, glob.glob(os.path.join(os.path.
                abspath(path), '*')))
            imxjz__xryh = [bpvy__eopo for bpvy__eopo in sorted(gjbth__xrq) if
                os.path.getsize(bpvy__eopo) > 0]
            if len(imxjz__xryh) == 0:
                raise BodoError(sdi__lgupu)
            fname = imxjz__xryh[0]
        bnqio__ixx = os.path.getsize(fname)
        eaj__rzcqk = fname
    return bzbo__kcv, eaj__rzcqk, bnqio__ixx, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    xqeuw__ldmu = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            raqzt__gbc, xdazd__edu = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = raqzt__gbc.region
        except Exception as qya__dsxlm:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{qya__dsxlm}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = xqeuw__ldmu.bcast(bucket_loc)
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
        vuvl__wmqr = get_s3_bucket_region_njit(path_or_buf, parallel=
            is_parallel)
        guc__jodmm, yzhn__kgib = unicode_to_utf8_and_len(D)
        rqdf__rxj = 0
        if is_parallel:
            rqdf__rxj = bodo.libs.distributed_api.dist_exscan(yzhn__kgib,
                np.int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), guc__jodmm, rqdf__rxj,
            yzhn__kgib, is_parallel, unicode_to_utf8(vuvl__wmqr),
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
    pqqfx__yrrg = get_overload_constant_dict(storage_options)
    mmbl__lkuv = 'def impl(storage_options):\n'
    mmbl__lkuv += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    mmbl__lkuv += f'    storage_options_py = {str(pqqfx__yrrg)}\n'
    mmbl__lkuv += '  return storage_options_py\n'
    rlkxn__genq = {}
    exec(mmbl__lkuv, globals(), rlkxn__genq)
    return rlkxn__genq['impl']
