import json
import os
from threading import Lock

from truera.client.client_utils import get_context_storage_base_path
import truera.client.constants

connection_string_message = "Connection string to connect to Truera artifact endpoint. This can be saved via >tru save connection-string <truera endpoint>."


class CliClientContext(object):
    _default_feature_switches = {
        "timestamps_on_splits": False,
        "admin": False,
        "delayed_label": False,
        "rbac_admin": False,
        "scheduled_ingestion": False,
        "data_service_split_ingestion": True
    }

    def __init__(self, json_contents=None):
        """Create a client context.
        NOTE: Use `LocalContextStorage` to create a new CliClientContext.
        `context = LocalContextStorage.get_cli_env_context()`

        Args:
            json_contents: Parsed json from the client context. Defaults to None.
        """
        if json_contents is not None:
            self._connection_string = json_contents.get(
                "_connection_string", None
            )
            self._use_http = json_contents.get("_use_http", None)
            self._auth_type = json_contents.get("_auth_type", None)
            self._username = json_contents.get("_username", None)
            self._password = json_contents.get("_password", None)
            self._split_max_size = json_contents.get(
                "_split_max_size",
                truera.client.constants.DEFAULT_SPLIT_MAX_SIZE
            )
            self._grpc_client_timeout_sec = json_contents.get(
                "_grpc_client_timeout_sec",
                truera.client.constants.GRPC_CLIENT_TIMEOUT_IN_SECONDS
            )
            self._token = json_contents.get("_token", None)
            self._log_level = json_contents.get("_log_level", "Default")
            self.feature_switches = json_contents.get(
                "feature_switches", self._default_feature_switches
            )
            for default in self._default_feature_switches:
                if default not in self.feature_switches:
                    self.feature_switches[
                        default] = self._default_feature_switches[default]
            self._verify_cert = json_contents.get("_verify_cert", True)
        else:
            self._connection_string = None
            self._use_http = None
            self._auth_type = None
            self._username = None
            self._password = None
            self._split_max_size = truera.client.constants.DEFAULT_SPLIT_MAX_SIZE
            self._grpc_client_timeout_sec = truera.client.constants.GRPC_CLIENT_TIMEOUT_IN_SECONDS
            self._token = None
            self._log_level = "Default"
            self.feature_switches = self._default_feature_switches
            self._verify_cert = True
        truera.client.constants.GRPC_CLIENT_TIMEOUT_IN_SECONDS = self._grpc_client_timeout_sec

    @property
    def connection_string(self):
        return self._connection_string

    @connection_string.setter
    def connection_string(self, value):
        self._connection_string = value
        LocalContextStorage.write_cli_context_to_output_location(self)

    @property
    def use_http(self):
        return self._use_http

    @use_http.setter
    def use_http(self, value):
        self._use_http = value
        LocalContextStorage.write_cli_context_to_output_location(self)

    @property
    def auth_type(self):
        return self._auth_type

    @auth_type.setter
    def auth_type(self, value):
        self._auth_type = value
        LocalContextStorage.write_cli_context_to_output_location(self)

    @property
    def verify_cert(self):
        return self._verify_cert

    @verify_cert.setter
    def verify_cert(self, value):
        self._verify_cert = value
        LocalContextStorage.write_cli_context_to_output_location(self)

    @property
    def grpc_client_timeout_sec(self):
        return self._grpc_client_timeout_sec

    @grpc_client_timeout_sec.setter
    def grpc_client_timeout_sec(self, value):
        self._grpc_client_timeout_sec = value
        truera.client.constants.GRPC_CLIENT_TIMEOUT_IN_SECONDS = value
        LocalContextStorage.write_cli_context_to_output_location(self)

    @property
    def split_max_size(self):
        return self._split_max_size

    @split_max_size.setter
    def split_max_size(self, value):
        self._split_max_size = value
        LocalContextStorage.write_cli_context_to_output_location(self)

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value
        LocalContextStorage.write_cli_context_to_output_location(self)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value
        LocalContextStorage.write_cli_context_to_output_location(self)

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value
        LocalContextStorage.write_cli_context_to_output_location(self)

    @property
    def log_level(self):
        return self._log_level

    @log_level.setter
    def log_level(self, value):
        self._log_level = value
        LocalContextStorage.write_cli_context_to_output_location(self)

    def get_feature_switch_value(self, switch):
        return self.feature_switches.get(switch) or False

    def set_feature_switch_value(self, switch, value):
        self.feature_switches[switch] = value
        LocalContextStorage.write_cli_context_to_output_location(self)


class TrueraWorkspaceClientContext(object):
    _default_feature_switches = {
        "workspace_use_tables_for_split_ingestion": True,
        "create_model_tests_on_split_ingestion": False
    }

    def __init__(self, json_contents=None):
        """Create a truera workspace client context.
        NOTE: Use `LocalContextStorage` to create a new TrueraWorkspaceClientContext.
        `context = LocalContextStorage.get_workspace_env_context()`

        Args:
            json_contents: Parsed json from the client context. Defaults to None.
        """
        self.feature_switches = {}
        if json_contents is not None:
            for feature in TrueraWorkspaceClientContext._default_feature_switches:
                self.feature_switches[feature] = json_contents.get(
                    feature, TrueraWorkspaceClientContext.
                    _default_feature_switches[feature]
                )
        else:
            for feature_key, default_value in self._default_feature_switches.items(
            ):
                self.feature_switches[feature_key] = default_value

    @staticmethod
    def get_allowed_features():
        return TrueraWorkspaceClientContext._default_feature_switches.keys()

    def check_switch_allowed(self, switch):
        if not switch in TrueraWorkspaceClientContext.get_allowed_features():
            raise ValueError(
                f"Unknown switch provided {switch}. Valid list: {TrueraWorkspaceClientContext.get_allowed_features()}."
            )

    def get_feature_switch_value(self, switch):
        self.check_switch_allowed(switch)
        return self.feature_switches[switch]

    def set_feature_switch_value(self, switch, value):
        self.check_switch_allowed(switch)
        self.feature_switches[switch] = value
        LocalContextStorage.write_workspace_context_to_output_location(self)


class LocalContextStorage(object):
    _cli_context_storage_location = os.path.join(
        get_context_storage_base_path(), "cli", "context.json"
    )
    _truera_workspace_context_storage_location = os.path.join(
        get_context_storage_base_path(), "workspace", "context.json"
    )

    cli_context_instance = None
    workspace_context_instance = None
    instance_lock = Lock()

    @staticmethod
    def _get_contents_from_storage_location(location):
        if not os.path.isfile(location):
            return None

        with open(location, "r") as fp:
            contents = fp.read()

        return json.loads(contents)

    @staticmethod
    def _get_context_from_cli_context_storage_location():
        json_contents = LocalContextStorage._get_contents_from_storage_location(
            LocalContextStorage._cli_context_storage_location
        )
        return CliClientContext(json_contents)

    @staticmethod
    def _get_context_from_workspace_context_storage_location():
        json_contents = LocalContextStorage._get_contents_from_storage_location(
            LocalContextStorage._truera_workspace_context_storage_location
        )
        return TrueraWorkspaceClientContext(json_contents)

    @staticmethod
    def _write_context_to_location(location, dict_contents):
        LocalContextStorage.instance_lock.acquire()
        try:
            json_contents = json.dumps(dict_contents)

            os.makedirs(os.path.dirname(location), exist_ok=True)

            with open(location, "w") as fp:
                fp.write(json_contents)
        finally:
            LocalContextStorage.instance_lock.release()

    @staticmethod
    def write_cli_context_to_output_location(context):
        LocalContextStorage._write_context_to_location(
            LocalContextStorage._cli_context_storage_location, context.__dict__
        )

    @staticmethod
    def write_workspace_context_to_output_location(context):
        LocalContextStorage._write_context_to_location(
            LocalContextStorage._truera_workspace_context_storage_location,
            context.__dict__
        )

    @staticmethod
    def get_cli_env_context():
        LocalContextStorage.instance_lock.acquire()
        try:
            if not LocalContextStorage.cli_context_instance:
                LocalContextStorage.cli_context_instance = LocalContextStorage._get_context_from_cli_context_storage_location(
                )
            return LocalContextStorage.cli_context_instance
        finally:
            LocalContextStorage.instance_lock.release()

    @staticmethod
    def get_workspace_env_context():
        LocalContextStorage.instance_lock.acquire()
        try:
            if not LocalContextStorage.workspace_context_instance:
                LocalContextStorage.workspace_context_instance = LocalContextStorage._get_context_from_workspace_context_storage_location(
                )
            return LocalContextStorage.workspace_context_instance
        finally:
            LocalContextStorage.instance_lock.release()
