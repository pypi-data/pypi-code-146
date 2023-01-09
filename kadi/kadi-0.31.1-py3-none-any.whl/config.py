# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import socket

from celery.schedules import crontab

import kadi.lib.constants as const


class BaseConfig:
    """Base configuration."""

    ##########
    # Celery #
    ##########

    CELERY_BEAT_SCHEDULE = {
        "clean-resources-periodically": {
            "task": const.TASK_CLEAN_RESOURCES,
            "schedule": crontab(minute="*/60"),
        },
    }

    # So we don't retry forever if the broker is not reachable.
    CELERY_BROKER_TRANSPORT_OPTIONS = {
        "max_retries": 3,
        "interval_start": 0,
        "interval_step": 0.2,
        "interval_max": 0.5,
    }

    CELERY_BROKER_URL = "redis://localhost:6379/0"

    # Will default to "True" in a future release.
    CELERY_WORKER_CANCEL_LONG_RUNNING_TASKS_ON_CONNECTION_LOSS = True

    CELERY_WORKER_REDIRECT_STDOUTS = False

    #########
    # Flask #
    #########

    # Per default, only static files in production environments are "strongly" cached,
    # via headers set by the web server.
    SEND_FILE_MAX_AGE_DEFAULT = 0

    SESSION_COOKIE_DOMAIN = False

    SESSION_COOKIE_NAME = "kadi_session"

    #################
    # Flask-Limiter #
    #################

    RATELIMIT_HEADERS_ENABLED = True

    RATELIMIT_STORAGE_URI = "redis://localhost:6379/0"

    ###############
    # Flask-Login #
    ###############

    # Makes a stolen cookie much harder to use by using a session identifier.
    SESSION_PROTECTION = "strong"

    ####################
    # Flask-SQLAlchemy #
    ####################

    SQLALCHEMY_DATABASE_URI = None

    # To enable pessimistic disconnect handling.
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    ##################
    # Flask-Talisman #
    ##################

    # The options "force_https" and "session_cookie_secure" are only turned off since
    # they are handled separately already.
    FLASK_TALISMAN_OPTIONS = {
        "content_security_policy": {
            "default-src": "'self'",
            "object-src": "'none'",
            "img-src": ["'self'", "data:"],
            "script-src": ["'self'", "'unsafe-eval'"],
            "style-src": ["'self'", "'unsafe-inline'", "data:"],
        },
        "content_security_policy_nonce_in": "script-src",
        "force_https": False,
        "session_cookie_secure": False,
    }

    #################
    # Flask-WTForms #
    #################

    WTF_CSRF_TIME_LIMIT = None

    ########
    # Kadi #
    ########

    AUTH_PROVIDERS = [{"type": const.AUTH_PROVIDER_TYPE_LOCAL}]

    BACKEND_TRANSLATIONS_PATH = os.path.join("{root_path}", "translations")

    BROADCAST_MESSAGE = ""

    CAPABILITIES = []

    # Maximum time in seconds after which deleted resources are cleaned up.
    DELETED_RESOURCES_MAX_AGE = const.ONE_WEEK

    ENFORCE_LEGALS = False

    EXPERIMENTAL_FEATURES = False

    # Maximum time in seconds after which finished tasks are cleaned up.
    FINISHED_TASKS_MAX_AGE = const.ONE_WEEK

    # Path for fonts used outside the web browser context.
    FONTS_PATH = os.path.join("{root_path}", "assets", "fonts")

    # Maximum size in bytes for user and group images.
    IMAGES_MAX_SIZE = 10 * const.ONE_MB

    # Maximum time in seconds after which inactive files are cleaned up.
    INACTIVE_FILES_MAX_AGE = const.ONE_DAY

    INDEX_IMAGE = None

    INDEX_TEXT = ""

    LEGAL_NOTICE = ""

    LOCALE_COOKIE_NAME = "locale"

    LOCALE_COOKIE_SECURE = False

    MAIL_ERROR_LOGS = []

    MAIL_NO_REPLY = f"no-reply@{socket.getfqdn()}"

    MAIL_SUBJECT_HEADER = "Kadi4Mat"

    MANIFEST_PATH = os.path.join("{static_path}", "manifest.json")

    MIGRATIONS_PATH = os.path.join("{root_path}", "migrations")

    MISC_UPLOADS_PATH = None

    NAV_FOOTER_ITEMS = []

    PLUGIN_CONFIG = {}

    PLUGIN_ENTRYPOINT = "kadi_plugins"

    PLUGINS = []

    # Maximum size for file previews which are sent directly to the browser.
    PREVIEW_MAX_SIZE = 25 * const.ONE_MB

    PRIVACY_POLICY = ""

    PROXY_FIX_ENABLE = False

    PROXY_FIX_HEADERS = {
        "x_for": 1,
        "x_proto": 1,
        "x_host": 1,
        "x_port": 0,
        "x_prefix": 0,
    }

    # Global rate limit for anonymous users.
    RATELIMIT_ANONYMOUS_USER = "100/minute;5/second"

    # Global rate limit for authenticated users.
    RATELIMIT_AUTHENTICATED_USER = "500/minute;25/second"

    RATELIMIT_IP_WHITELIST = ["127.0.0.1"]

    # Path for miscellaneous resources used outside the web browser context.
    RESOURCES_PATH = os.path.join("{root_path}", "assets", "resources")

    ROBOTS_NOINDEX = False

    SENTRY_DSN = None

    SMTP_HOST = "localhost"

    SMTP_PASSWORD = ""

    SMTP_PORT = 25

    SMTP_TIMEOUT = 60

    SMTP_USE_TLS = False

    SMTP_USERNAME = ""

    STORAGE_PATH = None

    # Maximum time in seconds after which temporary files are cleaned up.
    TEMPORARY_FILES_MAX_AGE = const.ONE_HOUR

    TERMS_OF_USE = ""

    UPLOAD_CHUNK_SIZE = 10 * const.ONE_MB

    UPLOAD_CHUNKED_BOUNDARY = 50 * const.ONE_MB

    UPLOAD_USER_QUOTA = 10 * const.ONE_GB

    # Maximum time in seconds after which uploads are cleaned up.
    UPLOADS_MAX_AGE = const.ONE_DAY

    WORKFLOW_FEATURES = False


class ProductionConfig(BaseConfig):
    """Production configuration."""

    #########
    # Flask #
    #########

    PREFERRED_URL_SCHEME = "https"

    SESSION_COOKIE_SECURE = True

    USE_X_SENDFILE = True

    ########
    # Kadi #
    ########

    LOCALE_COOKIE_SECURE = True


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    #################
    # Elasticsearch #
    #################

    # Ignore Elasticsearch not running and use a basic search fallback.
    ELASTICSEARCH_ENABLE_FALLBACK = True

    #########
    # Flask #
    #########

    SECRET_KEY = "s3cr3t"

    SERVER_NAME = "localhost:5000"

    ####################
    # Flask-SQLAlchemy #
    ####################

    SQLALCHEMY_DATABASE_URI = "postgresql://kadi:kadi@localhost/kadi"

    ########
    # Kadi #
    ########

    AUTH_PROVIDERS = [
        {"type": const.AUTH_PROVIDER_TYPE_LOCAL, "allow_registration": True}
    ]

    EXPERIMENTAL_FEATURES = True

    MISC_UPLOADS_PATH = os.path.join("{instance_path}", "uploads")

    SMTP_PORT = 8_025

    STORAGE_PATH = os.path.join("{instance_path}", "storage")


class TestingConfig(BaseConfig):
    """Testing configuration."""

    ##########
    # Celery #
    ##########

    # Ensure Celery is never used.
    CELERY_BROKER_URL = None

    #################
    # Elasticsearch #
    #################

    # Ensure Elasticsearch is never used.
    ELASTICSEARCH_HOSTS = None

    #########
    # Flask #
    #########

    SECRET_KEY = "s3cr3t"

    SERVER_NAME = "localhost"

    TESTING = True

    #################
    # Flask-Limiter #
    #################

    RATELIMIT_STORAGE_URI = "memory://"

    ####################
    # Flask-SQLAlchemy #
    ####################

    SQLALCHEMY_DATABASE_URI = "postgresql://kadi_test:kadi_test@localhost/kadi_test"

    #################
    # Flask-WTForms #
    #################

    WTF_CSRF_ENABLED = False

    ########
    # Kadi #
    ########

    AUTH_PROVIDERS = [
        {"type": const.AUTH_PROVIDER_TYPE_LOCAL, "allow_registration": True},
        {"type": const.AUTH_PROVIDER_TYPE_LDAP},
        {
            "type": const.AUTH_PROVIDER_TYPE_SHIB,
            "idps": [{"name": "Test", "entity_id": "https://idp.example.com"}],
        },
    ]

    EXPERIMENTAL_FEATURES = True


CONFIG_CLASSES = {
    const.ENV_PRODUCTION: ProductionConfig,
    const.ENV_DEVELOPMENT: DevelopmentConfig,
    const.ENV_TESTING: TestingConfig,
}
