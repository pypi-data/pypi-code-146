from psu_upload.models.uploaded_file import UploadedFile
from psu_upload.models.database_file import DatabaseFile
from psu_base.services import utility_service, auth_service
from psu_upload.services import upload_service
from psu_base.classes.Log import Log

log = Log()

# Base queries that can have further filtering applied to them by the calling app


def get_file_query():
    if upload_service.using_s3():
        return UploadedFile.objects
    else:
        return DatabaseFile.objects


def get_all_files():
    app_code = utility_service.get_app_code()
    if upload_service.using_s3():
        return get_file_query().filter(app_code=app_code).exclude(status="D")
    else:
        return get_file_query().filter(app_code=app_code).exclude(status="D")


def get_user_files(username=None):
    if auth_service.is_logged_in() and not username:
        username = auth_service.get_user().username

    return get_all_files().filter(owner=username)
