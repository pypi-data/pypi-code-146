from django.http import HttpResponse, Http404, HttpResponseForbidden
from psu_base.classes.Log import Log
from psu_base.services import auth_service, utility_service
from psu_upload.services import upload_service, retrieval_service


log = Log()

# ToDo: Error Handling/Messages


def linked_file(request, file_id):
    """
    Retrieve a specified file and display as attachment.

    Security:
    This will only display files belonging to the authenticated owner, or files
    whose ID is saved in the session.  This prevents a user from changing the
    URL to display any file in the database.

    File IDs are automatically added to the session by the {%file_preview%} tag.
    Each app must verify permissions prior to displaying a file preview to a user.

    Authenticated users can always use this to view their own files
    """
    log.trace()

    # Retrieve the file
    file_instance = retrieval_service.get_file_query().get(pk=file_id)
    if not file_instance:
        return Http404()

    # Verify access to view the file
    allowed = False
    if auth_service.is_logged_in():
        if auth_service.get_user().username == file_instance.owner:
            allowed = True
        elif auth_service.has_authority("file_admin"):
            allowed = True

    # If not allowed via authentication, check session for specified file allowances
    if not allowed:
        allowed_files = utility_service.get_session_var("allowed_file_ids", [])
        if allowed_files and file_id in allowed_files:
            allowed = True

    if not allowed:
        return HttpResponseForbidden()

    else:

        # If specifically requested to download rather than open in browser
        download = request.GET.get("download")

        # If content type should not be opened in browser
        if "document" in file_instance.content_type:
            download = True
        elif "ms-" in file_instance.content_type:
            download = True

        filename = file_instance.basename
        response = HttpResponse(content_type=file_instance.content_type)
        if download:
            # Force browser to download file
            response["Content-Disposition"] = "attachment; filename=%s" % filename

    response.write(file_instance.file)
    return response
