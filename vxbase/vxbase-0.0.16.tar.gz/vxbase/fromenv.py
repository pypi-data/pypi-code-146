import logging
from os import environ

_logger = logging.getLogger(__name__)


def is_ci():
    """
    is_ci will try to get the CI env var which is set to true in gitlab and github actions

    :return: boolean indicating if we are in a CI environment
    """
    v = environ.get('CI', False)
    if v is bool:
        return v
    return v == 'true'


def _is(var):
    v = environ.get(var, False)
    _logger.debug('% = %s', var, v)
    return type(v) is not bool and v is not False


def is_github():
    return _is('GITHUB_ACTION')


def is_gitlab():
    return _is('GITLAB_CI')


def which_ci():
    if is_github():
        return 'github_action'
    if is_gitlab():
        return 'gitlab_ci'
    return ''
