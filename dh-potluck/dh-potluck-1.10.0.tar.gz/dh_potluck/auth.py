import hashlib
import logging
import re
from functools import wraps
from http import HTTPStatus
from pickle import dumps, loads

import requests
from flask import current_app, g, jsonify, request
from flask_redis import FlaskRedis
from redis.exceptions import ResponseError, TimeoutError

logger = logging.getLogger(__name__)


token_missing = {
    'description': 'Authentication token missing or incorrectly formatted.',
    'status': HTTPStatus.UNAUTHORIZED,
}
token_invalid = {
    'description': 'Authentication token invalid or expired.',
    'status': HTTPStatus.UNAUTHORIZED,
}
user_disabled = {
    'description': 'User account disabled.',
    'status': HTTPStatus.FORBIDDEN,
}
permission_denied = {
    'description': 'You do not have access to this resource.',
    'status': HTTPStatus.FORBIDDEN,
}
auth_error = {
    'description': 'An error occurred trying to authenticate.',
    'status': HTTPStatus.INTERNAL_SERVER_ERROR,
}


def error_response(error):
    return jsonify({'description': error['description']}), error['status']


class UnauthenticatedUser:
    role = None
    is_active = True


class AuthenticatedUser:
    id = None
    email = None
    first_name = None
    last_name = None
    default_time_zone = None
    time_zone_name = None
    password_reset_expires = None
    password_reset_url = None
    has_device = None
    status = None
    brandpanel_id = None
    is_superadmin = None
    is_pending = None
    job_title = None
    avatar_url = None
    organization = None
    brands = None
    accessible_brands = None
    permissions = None
    updated_at = None
    created_at = None

    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    @property
    def role(self):
        if self.is_superadmin:
            return 'superadmin'
        return 'user'

    @property
    def is_active(self):
        return self.status == 0


class ApplicationUser:
    role = 'app'
    is_active = True


def get_user(app_token, validate_token_func):
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        g.user = UnauthenticatedUser()
        return

    match = re.match(r'^(Application|Token|Bearer):? (\S+)$', auth_header)
    if not match:
        return error_response(token_missing)
    method = match.group(1)
    token = match.group(2)

    # Application token
    # Note: 'Token' is deprecated - all applications should be updated to use 'Application'
    if method == 'Application' or method == 'Token':
        if token == app_token:
            g.user = ApplicationUser()
        else:
            return error_response(token_invalid)

    # Bearer token
    elif method == 'Bearer':
        user = validate_token_func(match.group(2))
        if not user:
            return error_response(token_invalid)
        g.user = user

    if not g.user.is_active:
        return error_response(user_disabled)


roles = {
    'user': 0,
    'brand_admin': 1,
    'superadmin': 2,
    'app': 3,
}


def role_required(role):
    """
    Currently, the supported roles are:

    1. user
    2. brand_admin
    3. superadmin
    4. app

    Roles are ordered from least to most privilege. Each role receives the permissions of the roles
    before it. Example:

    If role='user', users with 'user', 'superadmin', or 'app' roles will be granted access.
    If role='superadmin', only users with 'superadmin' or 'app' roles will be granted access.
    """

    def decorator(func):
        # finds the role within a brand of the current user
        def get_brand_role():
            # extract the brand_id from the path
            brand_id = request.view_args.get('brand_id')
            if not brand_id:
                return None

            # use the brand_id to find the specific brand_role from the list of brand_roles
            brs = g.user.permissions.get('brand_roles', [])
            br = next((br.get('role') for br in brs if br.get('brand_id') == brand_id), None)

            # br.value will exist if g.user is assigned a user model (called from auth)
            # otherwise, br alone is the value we want
            return getattr(br, 'value', br)

        @wraps(func)
        def wrapper(*args, **kwargs):
            if isinstance(g.user, UnauthenticatedUser):
                return error_response(token_missing)

            if roles[g.user.role] >= roles[role]:
                return func(*args, **kwargs)

            # a check for the brand_admin role is needed as it isn't stored in the user instance
            if role == 'brand_admin' and g.user.brands and get_brand_role() == 'admin':
                return func(*args, **kwargs)

            return error_response(permission_denied)

        return wrapper

    return decorator


class AuthCache(object):
    cache = None

    @classmethod
    def get_cache(cls):
        if not current_app.config.get('DH_POTLUCK_AUTH_REDIS_URL'):
            logger.debug('Identity cache url (DH_POTLUCK_AUTH_REDIS_URL) not configured')
            return None
        if not cls.cache:
            cls.cache = FlaskRedis(
                app=current_app, config_prefix='DH_POTLUCK_AUTH_REDIS', socket_timeout=0.4
            )
        return cls.cache


def _get_from_cache(token):
    logger.debug('Get identity from cache')
    cache = AuthCache.get_cache()
    if not cache:
        return None
    try:
        cached_identity = cache.get(get_auth_cache_key(token))
        if cached_identity:
            logger.debug('Identity found!')
            return loads(cached_identity)
    except TimeoutError as err:
        logger.error(err)
        return None


def _set_to_cache(token, identity):
    logger.debug('Set identity to cache')
    ex = current_app.config.get('DH_POTLUCK_IDENTITY_EXPIRY_IN_SECONDS') or (5 * 60)
    cache = AuthCache.get_cache()
    if not cache:
        return
    try:
        cache.set(get_auth_cache_key(token), dumps(identity), ex=ex)
    except (ResponseError, TimeoutError) as err:
        logger.error(err)


def get_auth_cache_key(token):
    hash_object = hashlib.sha1(token.encode('utf-8'))
    token_hash = hash_object.hexdigest()
    return f'auth:token#{token_hash}'


def validate_token_using_api(token):
    if current_app.config.get('DH_POTLUCK_ENABLE_AUTH_CACHE'):
        identity = _get_from_cache(token)
        if identity:
            return AuthenticatedUser(identity)

    logger.debug('Get identity from auth service')
    auth_api_url = current_app.config['DH_POTLUCK_AUTH_API_URL']
    res = requests.get(
        auth_api_url + 'self',
        headers={'Authorization': f'Bearer {token}', 'content-type': 'application/json'},
    )
    if res.status_code == HTTPStatus.OK:
        identity = res.json()
        if current_app.config.get('DH_POTLUCK_ENABLE_AUTH_CACHE'):
            # TODO: Remove this once auth is upgraded to use the new cache key
            _set_to_cache(token, identity)
        return AuthenticatedUser(identity)

    return None
