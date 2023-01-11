from enum import Enum
import math
import os
import pickle
import sys

from sumtypes import constructor
from sumtypes import match
from sumtypes import sumtype

from truera.rnn.general.service.container import Locator
from truera.rnn.general.service.local_sync_service import LocalSyncService
from truera.rnn.general.service.s3_sync_service import S3SyncService
from truera.rnn.general.service.sync_client import SyncClient
from truera.rnn.general.service.sync_service import SyncService


class ExportBackend(Enum):
    LOCAL = 1
    S3 = 2


@sumtype
class ExportInfo(object):
    S3 = constructor("filename", "bucket", "prefix")
    Local = constructor("filename")


def get_export_info(filename, ext, export_options):
    '''
    Helper function for dash frontend exports page. See app_export.py for usage and data type of export_options
    returns ExportInfo given dash options
    '''
    if not filename:
        return 'Fill out filename'
    if (not filename.endswith(ext)):
        filename = filename + ext
    if (export_options.backend == ExportBackend.LOCAL.name):
        export_info = ExportInfo.Local(filename)
    elif (export_options.backend == ExportBackend.S3.name):
        if (not export_options.bucket or not export_options.prefix):
            return 'Fill out all export options for s3'
        export_info = ExportInfo.S3(
            filename, export_options.bucket, export_options.prefix
        )
    return export_info


def export_pkl(config, obj, export_info: ExportInfo, locator: Locator):

    if (type(export_info) == ExportInfo.Local):
        sync_service = LocalSyncService(config)
    elif (type(export_info) == ExportInfo.S3):
        sync_service = S3SyncService(
            config, bucket=export_info.bucket, s3_prefix=export_info.prefix
        )

    cache_path = sync_service.get_cache_path(locator)
    os.makedirs(cache_path, exist_ok=True)
    if isinstance(obj, list):
        num_items = len(obj)
        batch_fill = math.ceil(math.log(num_items, 10))
        suffix = ''
        for i in list(range(num_items)):
            if num_items > 1:
                suffix = '-' + str(i).zfill(batch_fill)
            response = export_pkl_single_file(
                sync_service,
                cache_path,
                obj[i],
                export_info,
                locator,
                batch_suffix=suffix
            )
            if 'Successful' not in response:
                return response

        return response

    else:
        return export_pkl_single_file(
            sync_service, cache_path, obj, export_info, locator
        )


def export_pkl_single_file(
    sync_service,
    cache_path,
    obj,
    export_info: ExportInfo,
    locator: Locator,
    batch_suffix=''
):
    local_cached_file = os.path.join(
        cache_path, locator.filename + batch_suffix
    )
    print('Creating File: ' + local_cached_file)

    if (type(export_info) == ExportInfo.Local):
        final_loc = local_cached_file
    elif (type(export_info) == ExportInfo.S3):
        final_loc = os.path.join(
            's3://', export_info.bucket, export_info.prefix,
            export_info.filename + batch_suffix
        )
    try:
        with open(local_cached_file, "wb+") as f:
            pickle.dump(obj, f)
        tmp_locator = Locator.Export(
            locator.project, locator.model, locator.data_collection,
            locator.split, locator.filename + batch_suffix
        )
        sync_service.push(tmp_locator)
        return 'Successful upload to: ' + final_loc
    except:
        print(sys.exc_info())
        return "{0}, {1}, local_file:{2}, upload_location:{3}".format(
            str(sys.exc_info()[0]), str(export_info), local_cached_file,
            final_loc
        )
