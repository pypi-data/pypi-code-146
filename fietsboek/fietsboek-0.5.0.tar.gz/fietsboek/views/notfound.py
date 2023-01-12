"""Error views."""
from pyramid.view import notfound_view_config


@notfound_view_config(renderer="fietsboek:templates/404.jinja2")
def notfound_view(request):
    """Renders the 404 response.

    :param request: The Pyramid request.
    :type request: pyramid.request.Request
    :return: The HTTP response.
    :rtype: pyramid.response.Response
    """
    request.response.status = 404
    return {}
