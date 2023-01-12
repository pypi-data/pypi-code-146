"""Upload functionality."""
import datetime
import logging

import gpxpy
from pyramid.httpexceptions import HTTPBadRequest, HTTPFound
from pyramid.i18n import TranslationString as _
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy import select

from .. import actions, models, util
from ..models.track import TrackType, Visibility

LOGGER = logging.getLogger(__name__)


@view_config(
    route_name="upload",
    renderer="fietsboek:templates/upload.jinja2",
    request_method="GET",
    permission="upload",
)
def show_upload(request):
    """Renders the main upload form.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    # pylint: disable=unused-argument
    return {}


@view_config(route_name="upload", request_method="POST", permission="upload")
def do_upload(request):
    """Endpoint to store the uploaded file.

    This does not yet create a track, it simply stores the track as a
    :class:`~fietsboek.models.track.Upload` and redirects the user to "finish"
    the upload by providing the missing metadata.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    try:
        gpx = request.POST["gpx"].file.read()
    except AttributeError:
        request.session.flash(request.localizer.translate(_("flash.no_file_selected")))
        return HTTPFound(request.route_url("upload"))

    # Before we do anything, we check if we can parse the file.
    # gpxpy might throw different exceptions, so we simply catch `Exception`
    # here - if we can't parse it, we don't care too much why at this point.
    # pylint: disable=broad-except
    try:
        gpxpy.parse(gpx)
    except Exception as exc:
        request.session.flash(request.localizer.translate(_("flash.invalid_file")))
        LOGGER.info("Could not parse gpx: %s", exc)
        return HTTPFound(request.route_url("upload"))

    now = datetime.datetime.utcnow()

    upload = models.Upload(
        owner=request.identity,
        uploaded_at=now,
    )
    upload.gpx_data = gpx
    request.dbsession.add(upload)
    request.dbsession.flush()

    return HTTPFound(request.route_url("finish-upload", upload_id=upload.id))


@view_config(route_name="preview", permission="upload.finish")
def preview(request):
    """Allows a preview of the uploaded track by returning the GPX data of a
    :class:`~fietsboek.models.track.Upload`

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    upload = request.context
    return Response(upload.gpx_data, content_type="application/gpx+xml")


@view_config(
    route_name="finish-upload",
    renderer="fietsboek:templates/finish_upload.jinja2",
    request_method="GET",
    permission="upload.finish",
)
def finish_upload(request):
    """Renders the form that allows the user to finish the upload.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    upload = request.context
    badges = request.dbsession.execute(select(models.Badge)).scalars()
    badges = [(False, badge) for badge in badges]
    gpx = gpxpy.parse(upload.gpx_data)
    timezone = util.guess_gpx_timezone(gpx)
    date = gpx.time or gpx.get_time_bounds().start_time or datetime.datetime.now()
    date = date.astimezone(timezone)
    tz_offset = timezone.utcoffset(date)
    tz_offset = 0 if tz_offset is None else tz_offset.total_seconds()
    track_name = ""
    track_desc = ""
    for track in gpx.tracks:
        if not track_name and track.name:
            track_name = track.name
        if not track_desc and track.description:
            track_desc = track.description

    return {
        "preview_id": upload.id,
        "upload_title": gpx.name or track_name,
        "upload_date": date,
        "upload_date_tz": int(tz_offset // 60),
        "upload_visibility": Visibility.PRIVATE,
        "upload_type": TrackType.ORGANIC,
        "upload_description": gpx.description or track_desc,
        "upload_tags": set(),
        "upload_tagged_people": [],
        "badges": badges,
    }


@view_config(route_name="finish-upload", request_method="POST", permission="upload.finish")
def do_finish_upload(request):
    """Endpoint for the "finishing upload" form.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    upload = request.context
    user_friends = request.identity.get_friends()
    badges = util.retrieve_multiple(request.dbsession, models.Badge, request.params, "badge[]")
    tagged_people = util.retrieve_multiple(
        request.dbsession, models.User, request.params, "tagged-friend[]"
    )

    if any(user not in user_friends for user in tagged_people):
        return HTTPBadRequest()

    tz_offset = datetime.timedelta(minutes=int(request.params["date-tz"]))
    date = datetime.datetime.fromisoformat(request.params["date"])
    date = date.replace(tzinfo=datetime.timezone(tz_offset))

    track = actions.add_track(
        request.dbsession,
        request.data_manager,
        owner=request.identity,
        title=request.params["title"],
        visibility=Visibility[request.params["visibility"]],
        track_type=TrackType[request.params["type"]],
        description=request.params["description"],
        badges=badges,
        tagged_people=tagged_people,
        date=date,
        tags=request.params.getall("tag[]"),
        gpx_data=upload.gpx_data,
    )
    request.dbsession.delete(upload)

    # Don't forget to add the images
    LOGGER.debug("Starting to edit images for the upload")
    actions.edit_images(request, track)

    request.session.flash(request.localizer.translate(_("flash.upload_success")))

    return HTTPFound(request.route_url("details", track_id=track.id))


@view_config(route_name="cancel-upload", permission="upload.finish", request_method="POST")
def cancel_upload(request):
    """Cancels the upload and clears the temporary data.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    upload = request.context
    request.dbsession.delete(upload)
    request.session.flash(request.localizer.translate(_("flash.upload_cancelled")))
    return HTTPFound(request.route_url("upload"))
