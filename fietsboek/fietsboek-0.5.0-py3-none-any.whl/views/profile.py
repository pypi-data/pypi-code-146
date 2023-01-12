"""Views corresponding to the user profile."""
import datetime

from pyramid.httpexceptions import HTTPForbidden, HTTPFound, HTTPNotFound
from pyramid.i18n import TranslationString as _
from pyramid.view import view_config
from sqlalchemy import select

from .. import models, util


@view_config(
    route_name="profile",
    renderer="fietsboek:templates/profile.jinja2",
    permission="user",
    request_method="GET",
)
def profile(request):
    """Provides the profile overview.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """

    coming_requests = request.dbsession.execute(
        select(models.FriendRequest).filter_by(recipient_id=request.identity.id)
    ).scalars()
    going_requests = request.dbsession.execute(
        select(models.FriendRequest).filter_by(sender_id=request.identity.id)
    ).scalars()
    return {
        "user": request.identity,
        "outgoing_friend_requests": going_requests,
        "incoming_friend_requests": coming_requests,
    }


@view_config(route_name="change-profile", permission="user", request_method="POST")
def do_change_profile(request):
    """Endpoint to change the personal data.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    password = request.params["password"]
    if password:
        try:
            util.check_password_constraints(password, request.params["repeat-password"])
        except ValueError as exc:
            request.session.flash(request.localizer.translate(exc.args[0]))
            return HTTPFound(request.route_url("profile"))
        request.identity.set_password(request.params["password"])
    name = request.params["name"]
    if request.identity.name != name:
        request.identity.name = name
    request.session.flash(request.localizer.translate(_("flash.personal_data_updated")))
    return HTTPFound(request.route_url("profile"))


@view_config(route_name="add-friend", permission="user", request_method="POST")
def do_add_friend(request):
    """Sends a friend request.

    This is the endpoint of a form on the profile overview.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    email = request.params["friend-email"]
    candidate = request.dbsession.execute(models.User.query_by_email(email)).scalar_one_or_none()
    if candidate is None:
        request.session.flash(request.localizer.translate(_("flash.friend_not_found")))
        return HTTPFound(request.route_url("profile"))

    if candidate in request.identity.get_friends() or candidate in [
        x.recipient for x in request.identity.outgoing_requests
    ]:
        request.session.flash(request.localizer.translate(_("flash.friend_already_exists")))
        return HTTPFound(request.route_url("profile"))

    for incoming in request.identity.incoming_requests:
        if incoming.sender == candidate:
            # We have an incoming request from that person, so we just accept that
            request.identity.add_friend(candidate)
            request.dbsession.delete(incoming)
            request.session.flash(request.localizer.translate(_("flash.friend_added")))
            return HTTPFound(request.route_url("profile"))

    # Nothing helped, so we send the friend request
    friend_req = models.FriendRequest(
        sender=request.identity,
        recipient=candidate,
        date=datetime.datetime.utcnow(),
    )
    request.dbsession.add(friend_req)
    request.session.flash(request.localizer.translate(_("flash.friend_request_sent")))
    return HTTPFound(request.route_url("profile"))


@view_config(route_name="delete-friend", permission="user", request_method="POST")
def do_delete_friend(request):
    """Deletes a friend.

    This is the endpoint of a form on the profile overview.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    friend = request.dbsession.execute(
        select(models.User).filter_by(id=request.params["friend-id"])
    ).scalar_one_or_none()
    if friend:
        request.identity.remove_friend(friend)
    return HTTPFound(request.route_url("profile"))


@view_config(route_name="accept-friend", permission="user", request_method="POST")
def do_accept_friend(request):
    """Accepts a friend request.

    This is the endpoint of a form on the profile overview.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    friend_request = request.dbsession.execute(
        select(models.FriendRequest).filter_by(id=request.params["request-id"])
    ).scalar_one_or_none()
    if friend_request is None:
        return HTTPNotFound()
    if friend_request.recipient != request.identity:
        return HTTPForbidden()

    friend_request.sender.add_friend(friend_request.recipient)
    request.dbsession.delete(friend_request)
    return HTTPFound(request.route_url("profile"))


@view_config(route_name="json-friends", renderer="json", permission="user")
def json_friends(request):
    """Returns a JSON-ified list of the user's friends.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    friends = [{"name": friend.name, "id": friend.id} for friend in request.identity.get_friends()]
    return friends
