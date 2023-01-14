import datetime
import logging
import os
import sentry_sdk
from .version import __version__
from typing import Callable, Optional, List
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import request
from flask import send_from_directory
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.routing import IntegerConverter
from werkzeug.utils import safe_join
from werkzeug.middleware.proxy_fix import ProxyFix
from katatachi.content import ContentStore
from katatachi.interface.api import ApiBlueprintFactory
from katatachi.mod_view import ModViewQuery
from katatachi.mod_view import ModViewRenderer
from katatachi.mod_view import ModViewStore
from katatachi.pipeline import Pipeline
from katatachi.reconciler import Reconciler, start_reconciler_blocking
from katatachi.utils import DatabaseMigration
from katatachi.utils import getenv_or_raise, getenv_or_meh
from katatachi.worker import WorkerQueue
from katatachi.worker import GlobalMetadataStore
from katatachi.worker import MetadataStoreFactory
from katatachi.worker import WorkContextFactory
from katatachi.worker import WorkerCache
from katatachi.worker import WorkerConfigStore
from katatachi.worker import WorkFactory
from katatachi.worker import WorkerRunStore
from katatachi.pipeline import configure_pipeline_mod_views, configure_pipeline_workers
from katatachi.blueprints import worker_blueprint_factory, mod_view_blueprint_factory, pipeline_blueprint_factory


logger = logging.getLogger(__name__)


database_migration = DatabaseMigration(
    mongo_admin_connection_string=getenv_or_raise("MONGODB_ADMIN_CONNECTION_STRING"),
    mongo_db=getenv_or_raise("MONGODB_DB"),
    redis_url=getenv_or_raise("REDIS_URL"),
    redis_key_prefix=getenv_or_raise("REDIS_KEY_PREFIX"),
)


class App(object):
    # pipelines are instantiated with app so that
    # state migrations can be checked and run with database migration
    def __init__(self, pipeline: Optional[Pipeline] = None):
        ###
        # Preliminary
        ###
        if "SENTRY_DSN" in os.environ:
            logger.info("SENTRY_DSN environ found, settings up sentry")
            sentry_sdk.init(os.environ["SENTRY_DSN"])
            sentry_enabled = True
        else:
            logger.info("Not setting up sentry")
            sentry_enabled = False
        self.pause_workers = getenv_or_meh("PAUSE_WORKERS", "false") == "true"
        self.instance_title = getenv_or_meh("INSTANCE_TITLE", "Untitled")
        self.pipeline = pipeline  # type: Optional[Pipeline]
        self.flask_app = None  # type: Optional[Flask]

        ###
        # Core
        ###
        self.worker_cache = WorkerCache()
        self.content_store = ContentStore(
            connection_string=getenv_or_raise("MONGODB_CONNECTION_STRING"),
            db=getenv_or_raise("MONGODB_DB"),
        )
        metadata_store_factory = MetadataStoreFactory(
            connection_string=getenv_or_raise("MONGODB_CONNECTION_STRING"),
            db=getenv_or_raise("MONGODB_DB"),
        )
        self.worker_run_store = WorkerRunStore(
            connection_string=getenv_or_raise("MONGODB_CONNECTION_STRING"),
            db=getenv_or_raise("MONGODB_DB"),
            worker_cache=self.worker_cache
        )
        self.worker_context_factory = WorkContextFactory(
            content_store=self.content_store,
            worker_run_store=self.worker_run_store,
            metadata_store_factory=metadata_store_factory,
        )
        self.worker_config_store = WorkerConfigStore(
            connection_string=getenv_or_raise("MONGODB_CONNECTION_STRING"),
            db=getenv_or_raise("MONGODB_DB"),
            worker_cache=self.worker_cache,
        )
        self.global_metadata_store = GlobalMetadataStore(
            connection_string=getenv_or_raise("MONGODB_CONNECTION_STRING"),
            db=getenv_or_raise("MONGODB_DB"),
        )

        ###
        # Mod view
        ###
        self.mod_view_store = ModViewStore()
        self.boards_renderer = ModViewRenderer(self.content_store)

        ###
        # API
        ###
        self.api_blueprint_factories = []  # type: List[ApiBlueprintFactory]

        ###
        # Worker
        ###
        self.work_factory = WorkFactory(
            work_context_factory=self.worker_context_factory,
            worker_cache=self.worker_cache,
            worker_config_store=self.worker_config_store,
            worker_run_store=self.worker_run_store,
            sentry_enabled=sentry_enabled,
        )
        self.worker_queue = WorkerQueue(
            redis_url=getenv_or_raise("REDIS_URL"),
            work_factory=self.work_factory,
        )

    def register_worker_module(self, module_name: str, constructor: Callable):
        self.worker_cache.register_module(module_name, constructor)

    def add_api_blueprint(self, api_blueprint_factory: ApiBlueprintFactory):
        self.api_blueprint_factories.append(api_blueprint_factory)

    def add_mod_view(self, name: str, mod_view: ModViewQuery):
        self.mod_view_store.add_mod_view(name, mod_view)

    def configure_pipeline_mod_views(self):
        configure_pipeline_mod_views(
            pipeline=self.pipeline,
            mod_view_store=self.mod_view_store,
        )

    def configure_pipeline_workers(self):
        configure_pipeline_workers(
            pipeline=self.pipeline,
            worker_config_store=self.worker_config_store,
            worker_cache=self.worker_cache
        )

    def get_flask_app(self) -> Flask:
        if self.flask_app:
            return self.flask_app

        logger.info("Initialing web app")
        database_migration.assert_latest()
        if self.pipeline:
            self.configure_pipeline_mod_views()
            self.configure_pipeline_workers()

        ###
        # Flask
        ###
        flask_app = Flask(__name__)
        CORS(flask_app)

        ###
        # Rate limit
        ###
        flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app, x_for=1)
        limiter = Limiter(
            flask_app,
            key_func=get_remote_address,
            storage_uri="memory://",
            strategy='moving-window'
        )

        @flask_app.errorhandler(429)
        def ratelimit_handler(_):
            return 'rate limit exceeded', 429

        ###
        # Web UI
        ###
        my_path = os.path.abspath(__file__)
        my_par_path = os.path.dirname(my_path)
        web_root = os.path.join(my_par_path, "web")
        if not os.path.exists(web_root):
            raise RuntimeError(f"Static web artifact is not found under {web_root}")

        # copy-pasta from https://github.com/pallets/flask/issues/2643
        class SignedIntConverter(IntegerConverter):
            regex = r"-?\d+"

        flask_app.url_map.converters["signed_int"] = SignedIntConverter

        @flask_app.route("/", methods=["GET"])
        def _index():
            return redirect("/web")

        @flask_app.route("/health", methods=["GET"])
        def _health():
            return "OK", 200

        @flask_app.route("/version", methods=["GET"])
        def _version():
            return __version__, 200

        def _send_index() -> str:
            filename = safe_join(web_root, "index.html")
            with open(filename, "rb") as f:
                return (
                    f.read()
                    .decode("utf-8")
                    .replace("${INSTANCE_TITLE}", self.instance_title)
                )

        @flask_app.route("/web", methods=["GET"])
        @flask_app.route("/web/<path:filename>", methods=["GET"])
        def _web(filename=""):
            if filename == "":
                return _send_index()
            elif os.path.exists(os.path.join(web_root, *filename.split("/"))):
                return send_from_directory(web_root, filename)
            else:
                return _send_index()

        ###
        # Auth
        ###
        flask_app.config["JWT_SECRET_KEY"] = getenv_or_raise("JWT_SECRET_KEY")
        JWTManager(flask_app)
        admin_username = getenv_or_raise("ADMIN_USERNAME")
        admin_password = getenv_or_raise("ADMIN_PASSWORD")

        @flask_app.before_request
        def _before_request():
            if request.path.startswith("/apiInternal"):
                verify_jwt_in_request()

        @flask_app.route("/auth", methods=["POST"])
        @limiter.limit('1/second')
        def _auth():
            username = request.json.get("username", None)
            password = request.json.get("password", None)
            if not username:
                return jsonify({"status": "error", "message": "Missing username"}), 400
            if not password:
                return jsonify({"status": "error", "message": "Missing password"}), 400
            if username != admin_username or password != admin_password:
                return (
                    jsonify({"status": "error", "message": "Wrong username/password"}),
                    401,
                )
            access_token = create_access_token(
                identity=username,
                expires_delta=datetime.timedelta(days=365),  # todo: just for now
            )
            return jsonify({"status": "ok", "access_token": access_token}), 200

        ###
        # Core blueprints
        ###
        flask_app.register_blueprint(pipeline_blueprint_factory(
            pipeline=self.pipeline,
            worker_config_store=self.worker_config_store,
            worker_cache=self.worker_cache,
            content_store=self.content_store,
        ), url_prefix="/apiInternal/pipeline")
        flask_app.register_blueprint(worker_blueprint_factory(
            worker_cache=self.worker_cache,
            worker_config_store=self.worker_config_store,
            global_metadata_store=self.global_metadata_store,
            worker_run_store=self.worker_run_store,
        ), url_prefix="/apiInternal/worker")
        flask_app.register_blueprint(mod_view_blueprint_factory(
            mod_view_store=self.mod_view_store,
            content_store=self.content_store,
            mod_view_renderer=self.boards_renderer,
        ), url_prefix="/apiInternal/boards")

        ###
        # API blueprints
        ###
        def exempt_api_rate_limit():
            if 'API_INTERNAL_KEY' not in os.environ:
                return False
            query_params = request.args.to_dict()
            res = 'api_key' in query_params and query_params['api_key'] == os.environ['API_INTERNAL_KEY']
            return res

        for api_blueprint_factory in self.api_blueprint_factories:
            api_blueprint = api_blueprint_factory(self.content_store)
            limiter.limit(getenv_or_meh("API_RATE_LIMIT", "5/second"), exempt_when=exempt_api_rate_limit)(api_blueprint)
            flask_app.register_blueprint(api_blueprint, url_prefix="/api")

        self.flask_app = flask_app
        return flask_app

    def start_web_dev(self):
        self.get_flask_app().run(
            host="0.0.0.0",
            port=int(getenv_or_meh("PORT", 5000)),
            debug=True,
            # avoid using reloader for now
            # because there is no non-hacky way to tell if the app is running under gunicorn for production
            # and hence we should not add any conditional, including WERKZEUG_RUN_MAIN which is used for telling reload
            use_reloader=False,
        )

    def start_clock(self):
        database_migration.assert_latest()
        if self.pipeline:
            self.configure_pipeline_workers()
        reconciler = Reconciler(self.worker_config_store, self.worker_queue, self.pause_workers)
        start_reconciler_blocking(reconciler)

    def start_worker(self):
        database_migration.assert_latest()
        if self.pipeline:
            self.configure_pipeline_workers()
        self.worker_queue.start_worker()


def start_database_migration():
    database_migration.migrate()
