"""Admin views."""
from pyramid.httpexceptions import HTTPFound
from pyramid.i18n import TranslationString as _
from pyramid.view import view_config
from sqlalchemy import select

from .. import models


@view_config(
    route_name="admin",
    renderer="fietsboek:templates/admin.jinja2",
    request_method="GET",
    permission="admin",
)
def admin(request):
    """Renders the main admin overview.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    badges = request.dbsession.execute(select(models.Badge)).scalars()
    return {
        "badges": badges,
    }


@view_config(route_name="admin-badge-add", permission="admin", request_method="POST")
def do_badge_add(request):
    """Adds a badge.

    This is the endpoint of a form on the admin overview.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """

    image = request.params["badge-image"].file.read()
    title = request.params["badge-title"]

    badge = models.Badge(title=title, image=image)
    request.dbsession.add(badge)

    request.session.flash(request.localizer.translate(_("flash.badge_added")))
    return HTTPFound(request.route_url("admin"))


@view_config(route_name="admin-badge-edit", permission="admin", request_method="POST")
def do_badge_edit(request):
    """Modifies an already existing badge.

    This is the endpoint of a form on the admin overview.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    badge = request.dbsession.execute(
        select(models.Badge).filter_by(id=request.params["badge-edit-id"])
    ).scalar_one()
    try:
        badge.image = request.params["badge-image"].file.read()
    except AttributeError:
        pass
    badge.title = request.params["badge-title"]

    request.session.flash(request.localizer.translate(_("flash.badge_modified")))
    return HTTPFound(request.route_url("admin"))


@view_config(route_name="admin-badge-delete", permission="admin", request_method="POST")
def do_badge_delete(request):
    """Removes a badge.

    This is the endpoint of a form on the admin overview.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    badge = request.dbsession.execute(
        select(models.Badge).filter_by(id=request.params["badge-delete-id"])
    ).scalar_one()
    request.dbsession.delete(badge)

    request.session.flash(request.localizer.translate(_("flash.badge_deleted")))
    return HTTPFound(request.route_url("admin"))
