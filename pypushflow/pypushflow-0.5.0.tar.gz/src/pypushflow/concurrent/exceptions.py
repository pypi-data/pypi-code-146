from multiprocessing.pool import RemoteTraceback as MpRemoteTraceback

try:
    from .billiard import RemoteTraceback as BRemoteTraceback
except ImportError:
    BRemoteTraceback = None


def extract_remote_exception(exception: BaseException) -> BaseException:
    if isinstance(exception.__cause__, MpRemoteTraceback):
        return exception.__cause__
    if BRemoteTraceback is not None and isinstance(
        exception.__cause__, BRemoteTraceback
    ):
        return exception.__cause__
    return exception
