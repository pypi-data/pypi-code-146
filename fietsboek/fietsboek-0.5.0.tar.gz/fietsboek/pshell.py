"""Shell for interactive access to the Pyramid application."""
from . import models


def setup(env):
    """Sets the shell environment up.

    :param env: The environment to set up.
    :type env: pyramid.scripting.AppEnvironment
    """
    request = env["request"]

    # start a transaction
    request.tm.begin()

    # inject some vars into the shell builtins
    env["tm"] = request.tm
    env["dbsession"] = request.dbsession
    env["models"] = models
