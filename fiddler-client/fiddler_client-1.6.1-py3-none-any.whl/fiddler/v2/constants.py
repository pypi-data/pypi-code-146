import enum

# Headers
CONTENT_TYPE_HEADER_KEY = 'Content-Type'
CONTENT_TYPE_OCTET_STREAM = 'application/octet-stream'
CONTENT_TYPE_OCTET_STREAM_HEADER = {CONTENT_TYPE_HEADER_KEY: CONTENT_TYPE_OCTET_STREAM}

# Multi-part upload
MULTI_PART_UPLOAD_SIZE_THRESHOLD = 5 * 1024 * 1024  # 5MB in bytes
MULTI_PART_CHUNK_SIZE = 100 * 1024 * 1024  # 100MB in bytes


@enum.unique
class FiddlerTimestamp(str, enum.Enum):
    """Supported timestamp formats for events published to Fiddler"""

    EPOCH_MILLISECONDS = 'epoch milliseconds'
    EPOCH_SECONDS = 'epoch seconds'
    ISO_8601 = '%Y-%m-%d %H:%M:%S.%f'
    TIMEZONE = ISO_8601 + '%Z %z'
    INFER = 'infer'


@enum.unique
class FileType(str, enum.Enum):
    """Supported file types for ingestion"""

    CSV = '.csv'


@enum.unique
class ServerDeploymentMode(str, enum.Enum):
    F1 = 'f1'
    F2 = 'f2'


@enum.unique
class UploadType(str, enum.Enum):
    """To distinguish between dataset ingestion and event ingestion.
    Supposed to be only internally used.
    """

    DATASET = 'dataset'
    EVENT = 'event'


FIDDLER_CLIENT_VERSION_HEADER = 'X-Fiddler-Client-Version'
