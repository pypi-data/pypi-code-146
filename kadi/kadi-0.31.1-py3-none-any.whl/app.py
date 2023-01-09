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
import logging
import os
import warnings
from collections import OrderedDict
from logging.handlers import SMTPHandler

import sentry_sdk
from flask import Flask
from flask import json
from flask.logging import default_handler
from pluggy import PluginManager
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.middleware.proxy_fix import ProxyFix

import kadi.lib.constants as const
from .config import CONFIG_CLASSES
from kadi.ext.babel import babel
from kadi.ext.celery import celery
from kadi.ext.csrf import csrf
from kadi.ext.db import db
from kadi.ext.limiter import limiter
from kadi.ext.login import login
from kadi.ext.migrate import migrate
from kadi.ext.oauth import oauth
from kadi.ext.talisman import talisman
from kadi.lib.config.core import get_sys_config
from kadi.lib.conversion import truncate
from kadi.lib.db import has_pending_revisions
from kadi.lib.db import SimpleTimestampMixin
from kadi.lib.db import StateTimestampMixin
from kadi.lib.exceptions import KadiConfigurationError
from kadi.lib.format import duration
from kadi.lib.format import filesize
from kadi.lib.oauth.utils import has_oauth2_providers
from kadi.lib.permissions.core import has_permission
from kadi.lib.permissions.tasks import _apply_role_rules_task
from kadi.lib.permissions.utils import get_object_roles
from kadi.lib.resources.tasks import _publish_resource_task
from kadi.lib.revisions.core import setup_revisions
from kadi.lib.search.core import SearchableMixin
from kadi.lib.search.elasticsearch import es
from kadi.lib.security import hash_value
from kadi.lib.utils import compact_json
from kadi.lib.utils import flatten_list
from kadi.lib.web import get_locale
from kadi.lib.web import IdentifierConverter
from kadi.lib.web import static_url
from kadi.lib.web import url_for
from kadi.modules.accounts.providers import LocalProvider
from kadi.modules.accounts.providers.core import init_auth_providers
from kadi.modules.accounts.utils import json_user
from kadi.modules.main.tasks import _clean_resources_task
from kadi.modules.notifications.tasks import _send_mail_task
from kadi.modules.records.tasks import _merge_chunks_task
from kadi.modules.records.tasks import _purge_record_task
from kadi.modules.workflows.models import Workflow  # pylint: disable=unused-import
from kadi.plugins import impl
from kadi.plugins import spec
from kadi.plugins.core import run_hook
from kadi.plugins.core import template_hook
from kadi.plugins.utils import get_plugin_frontend_translations
from kadi.plugins.utils import get_plugin_scripts


# This warning can happen when accessing the server the application runs on directly by
# IP address. Werkzeug will just return an invalid match (404) in this case, triggering
# the usual error handling of the application.
warnings.filterwarnings(
    "ignore",
    module="flask.app",
    category=UserWarning,
    message="Current server name '.*' doesn't match configured server name '.*'",
)


class Kadi(Flask):
    r"""The main application class.

    :param environment: (optional) The environment the application should run in.
        Defaults to the value of the ``KADI_ENV`` environment variable or the production
        environment.
    """

    def __init__(self, import_name, environment=None):
        if environment is None:
            environment = os.environ.get(const.VAR_ENV, const.ENV_PRODUCTION)

        if environment not in [
            const.ENV_PRODUCTION,
            const.ENV_DEVELOPMENT,
            const.ENV_TESTING,
        ]:
            raise KadiConfigurationError(
                f"Invalid environment, must be one of '{const.ENV_PRODUCTION}',"
                f" '{const.ENV_DEVELOPMENT}' or '{const.ENV_TESTING}'."
            )

        super().__init__(import_name)

        self.config[const.VAR_ENV] = environment

    @property
    def environment(self):
        """Get the current environment of the application."""
        return self.config[const.VAR_ENV]


def create_app(environment=None, config=None):
    """Create a new application object.

    :param environment: (optional) The environment the application should run in. See
        :class:`Kadi`.
    :param config: (optional) Additional configuration dictionary that takes precedence
        over configuration values defined via the configuration file.
    :return: The new application object.
    """
    app = Kadi(__name__, environment=environment)

    _init_config(app, config)
    _init_logging(app)
    _init_plugins(app)
    _init_extensions(app)
    _init_celery(app)
    _init_app(app)
    _init_jinja(app)

    return app


CONFIG_REQUIRED = [
    "SQLALCHEMY_DATABASE_URI",
    "STORAGE_PATH",
    "MISC_UPLOADS_PATH",
    "SERVER_NAME",
    "SECRET_KEY",
]

CONFIG_DEPRECATED = [
    ("RATELIMIT_STORAGE_URI", "RATELIMIT_STORAGE_URL"),
    ("UPLOAD_USER_QUOTA", "MAX_UPLOAD_USER_QUOTA"),
]


def _init_config(app, config):
    app.config.from_object(CONFIG_CLASSES[app.environment])

    if os.environ.get(const.VAR_CONFIG):
        app.config.from_envvar(const.VAR_CONFIG)

    if config is not None:
        app.config.update(config)

    # Interpolate all placeholders, and make sure that the paths are always absolute.
    interpolations = {
        "instance_path": os.path.abspath(app.instance_path),
        "root_path": os.path.abspath(app.root_path),
        "static_path": os.path.abspath(app.static_folder),
    }

    for key, value in app.config.items():
        if isinstance(value, str):
            app.config[key] = value.format(**interpolations)

    # Allow for the maximum content length to be at least the configured upload chunk
    # size, maximum size for direct uploads and maximum image size plus some additional
    # padding of 1 MB.
    max_size = max(
        app.config["UPLOAD_CHUNK_SIZE"],
        app.config["UPLOAD_CHUNKED_BOUNDARY"],
        app.config["IMAGES_MAX_SIZE"],
    )
    app.config["MAX_CONTENT_LENGTH"] = max_size + const.ONE_MB

    # Set up the manifest mapping, see also "kadi.cli.commands.assets".
    app.config["MANIFEST_MAPPING"] = None
    manifest_path = app.config["MANIFEST_PATH"]

    if os.path.exists(manifest_path):
        with open(manifest_path, encoding="utf-8") as f:
            app.config["MANIFEST_MAPPING"] = json.load(f)

    # Specify the amount of "X-Forwarded-*" header values to trust.
    if app.config["PROXY_FIX_ENABLE"]:
        app.wsgi_app = ProxyFix(app.wsgi_app, **app.config["PROXY_FIX_HEADERS"])

    # Automatically enable all workflow features when experimental features are enabled.
    if app.config["EXPERIMENTAL_FEATURES"]:
        app.config["WORKFLOW_FEATURES"] = True

    # Map various renamed config keys to their new counterpart. These should probably be
    # marked as deprecated in the future, but for now we just allow both. Note that the
    # deprecated keys currently take precedence if specified.
    for (new_key, old_key) in CONFIG_DEPRECATED:
        if old_key in app.config:
            app.config[new_key] = app.config[old_key]

    # If not testing, verify that the most important, required config values have at
    # least been set.
    if not app.testing:
        for key in CONFIG_REQUIRED:
            if not app.config[key]:
                msg = f"The '{key}' configuration value has not been set."

                # Add some additional information if the app was created via the CLI.
                if os.environ.get(const.VAR_CLI) == "1":
                    msg += (
                        " Maybe the Kadi CLI does not have access to the Kadi"
                        " configuration file?"
                    )

                raise KadiConfigurationError(msg)


def _init_logging(app):
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
    )

    # Flasks default handler is a StreamHandler writing to the stream specified by the
    # WSGI server or to stderr outside of a request.
    default_handler.setFormatter(formatter)
    app.logger.setLevel(logging.INFO)

    # Setup SMTP logging, if applicable.
    mail_error_logs = app.config["MAIL_ERROR_LOGS"]

    if mail_error_logs:
        auth = None
        secure = None

        if app.config["SMTP_USERNAME"] and app.config["SMTP_PASSWORD"]:
            auth = (app.config["SMTP_USERNAME"], app.config["SMTP_PASSWORD"])
            if app.config["SMTP_USE_TLS"]:
                secure = ()

        mail_handler = SMTPHandler(
            mailhost=(app.config["SMTP_HOST"], app.config["SMTP_PORT"]),
            fromaddr=app.config["MAIL_NO_REPLY"],
            toaddrs=mail_error_logs,
            subject=f"[{app.config['MAIL_SUBJECT_HEADER']}] Error log",
            credentials=auth,
            secure=secure,
        )
        mail_handler.setFormatter(formatter)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    # Disable non-error messages in the Elasticsearch logger, which otherwise seem to
    # propagate to the Celery logger.
    logging.getLogger("elasticsearch").setLevel(logging.ERROR)

    # Disable non-error messages in "fonttools", which is used by "fpdf2" but produces
    # some unwanted log messages.
    logging.getLogger("fontTools.subset").setLevel(logging.ERROR)


def _init_plugins(app):
    plugin_manager = PluginManager("kadi")
    plugin_manager.add_hookspecs(spec)

    # Load all configured plugins that registered themselves via the plugin entry point.
    for plugin in app.config["PLUGINS"]:
        plugin_manager.load_setuptools_entrypoints(
            app.config["PLUGIN_ENTRYPOINT"], name=plugin
        )

    # Register all built-in hook implementations.
    plugin_manager.register(impl)

    # Simply store the plugin manager instance on the application instance.
    app.plugin_manager = plugin_manager


def _init_extensions(app):
    babel.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db, directory=app.config["MIGRATIONS_PATH"])
    oauth.init_app(app)
    talisman.init_app(app, **app.config["FLASK_TALISMAN_OPTIONS"])

    sentry_dsn = app.config["SENTRY_DSN"]
    if sentry_dsn:
        # pylint: disable=abstract-class-instantiated
        sentry_sdk.init(
            dsn=sentry_dsn, integrations=[CeleryIntegration(), FlaskIntegration()]
        )


def _init_celery(app):
    # This function will initialize Celery for use in both the application and the
    # actual worker processes to start and execute tasks respectively.

    config_prefix = "CELERY_"

    for key, value in app.config.items():
        if key.startswith(config_prefix):
            setattr(celery.conf, key[len(config_prefix) :].lower(), value)

    class ContextTask(celery.Task):
        """Wrapper for tasks to run inside their own application context."""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    # Manually register all tasks.
    for task in [
        _apply_role_rules_task,
        _clean_resources_task,
        _merge_chunks_task,
        _publish_resource_task,
        _purge_record_task,
        _send_mail_task,
    ]:
        celery.tasks.register(task)


def _register_capabilities(app):
    capabilities = []

    for capability in flatten_list(run_hook("kadi_register_capabilities")):
        if capability not in capabilities:
            capabilities.append(capability)
        else:
            warnings.warn(f"Capability '{capability}' is already registered.")

    app.config["CAPABILITIES"].append(capabilities)


def _register_storages(app):
    storages = OrderedDict()

    for storage in flatten_list(run_hook("kadi_get_storages")):
        storage_type = storage.storage_type

        if storage_type not in storages:
            storages[storage_type] = storage
        else:
            warnings.warn(f"Storage of type '{storage_type}' is already registered.")

    app.config["STORAGES"] = storages


def _init_backend_translations(app):
    # See also "kadi.cli.commands.i18n".
    translations_path = app.config["BACKEND_TRANSLATIONS_PATH"]
    plugin_translations_paths = run_hook("kadi_get_translations_paths")

    if plugin_translations_paths:
        # List the main translations path last, so it will take precedence.
        translations_path = f"{';'.join(plugin_translations_paths)};{translations_path}"

    app.config["BABEL_TRANSLATION_DIRECTORIES"] = translations_path


def _check_database(app):
    # If in a production environment and the app was not created via the CLI, check for
    # pending database revisions. Certain CLI commands may still perform this check
    # separately, regardless of environment, if required.
    if app.environment == const.ENV_PRODUCTION and os.environ.get(const.VAR_CLI) != "1":
        with app.app_context():
            if has_pending_revisions():
                raise KadiConfigurationError(
                    "The database schema is not up to date. Maybe you forgot to run"
                    " 'kadi db upgrade'?"
                )


def _init_app(app):
    # Register custom URL converters.
    app.url_map.converters["identifier"] = IdentifierConverter

    # Initialize Elasticsearch.
    es.init_app(app)

    if app.config["ELASTICSEARCH_HOSTS"]:
        SearchableMixin.register_search_listeners()

    # Perform all remaining initializations, starting with the capabilities.
    with app.app_context():
        _register_capabilities(app)
        _register_storages(app)
        _init_backend_translations(app)

        run_hook("kadi_register_blueprints", app=app)
        run_hook("kadi_register_oauth2_providers", registry=oauth)

    setup_revisions()
    init_auth_providers(app)

    SimpleTimestampMixin.register_timestamp_listener()
    StateTimestampMixin.register_timestamp_listener()

    # Check if the database is up to date, if applicable.
    _check_database(app)

    # Setup some values that will be imported automatically when running "kadi shell".
    @app.shell_context_processor
    def _shell_context():
        return {"const": const}


def _init_jinja(app):
    # Provide access to some useful builtins in all templates.
    for builtin in [any, bool, len, list, reversed, sorted]:
        app.jinja_env.globals[builtin.__name__] = builtin

    # Register all other globally used modules and functions.
    app.jinja_env.globals.update(
        {
            "const": const,
            "environment": app.environment,
            "get_locale": get_locale,
            "get_object_roles": get_object_roles,
            "get_sys_config": get_sys_config,
            "has_oauth2_providers": has_oauth2_providers,
            "get_plugin_frontend_translations": get_plugin_frontend_translations,
            "get_plugin_scripts": get_plugin_scripts,
            "has_permission": has_permission,
            "hash_value": hash_value,
            "json_user": json_user,
            "registration_allowed": LocalProvider.registration_allowed,
            "static_url": static_url,
            "template_hook": template_hook,
            "url_for": url_for,
        }
    )

    # Register all globally used custom filters.
    app.jinja_env.filters.update(
        {
            "duration": duration,
            "filesize": filesize,
            "escaped_json": compact_json,
            "truncate": truncate,
        }
    )

    # Register all custom extensions.
    app.jinja_env.add_extension("kadi.lib.jinja.SnippetExtension")
