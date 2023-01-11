from dataclasses import asdict
from dataclasses import dataclass
import json
import logging
from logging import Logger
import os
import time
from typing import Dict, List, Sequence

import click
import requests
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError

# This is the "firstName" field of the admin user. Needed because we require it to be populated.
TRUERA_KEYCLOAK_ADMIN_IDENTIFIER = "truera_admin"
# Keep in sync with kong.oidc.tmpl.yaml + supervisord.conf + common.sh
TRUERA_KEYCLOAK_PORT = 9180
TRUERA_KEYCLOAK_ROUTE = "/keycloak"
# Base route for keycloak requests
TRUERA_KEYCLOAK_AUTH_BASE_ROUTE = TRUERA_KEYCLOAK_ROUTE + "/auth"
# Filename of oidc config
TRUERA_OIDC_CONFIG_FILENAME = "truera-oidc.rc"
# Filename of usermanagement client creds
TRUERA_USERMANAGEMENT_CLIENT_CREDS_FILENAME = "truera-usermanagement-client.json"

# environment variable to persist keycloak user id. Keep in sync with run.sh
ENV_TRUERA_KEYCLOAK_USER_ID = "TRUERA_KEYCLOAK_USER_ID"
KEYCLOAK_CONFIG_LOGGER = "truera.KeycloakConfiguration"

# Token expiration time in seconds
KEYCLOAK_ACCESS_TOKEN_LIFESPAN = 900

KEYCLOAK_KONG_CLIENT_IDENTIFIER = "kong-client"
KEYCLOAK_USERMANAGEMENT_CLIENT_IDENTIFIER = "usermanagement-client"


class KeycloakInitializationException(Exception):
    pass


@dataclass
class KeycloakCreateClientInfo:
    clientId: str
    name: str
    id: str
    redirectUris: List[str]
    rootUrl: str
    serviceAccountsEnabled: bool
    protocol: str = "openid-connect"
    enabled: bool = True
    consentRequired: bool = False
    clientAuthenticatorType: str = "client-secret"
    surrogateAuthRequired: bool = True
    standardFlowEnabled: bool = True
    publicClient: bool = False


@dataclass
class KeycloakClientInfo:
    client_id: str
    client_secret: str


@dataclass
class KeycloakUserInfo():
    id: str
    username: str


@dataclass
class KeycloakUserRole():
    id: str
    name: str


@dataclass
class KeycloakAdminUser:
    truera_keycloak_admin_user: str
    truera_keycloak_admin_password: str
    truera_keycloak_admin_identifier: str = TRUERA_KEYCLOAK_ADMIN_IDENTIFIER


@dataclass
class TrueraConfiguration:
    truera_secrets_home: str
    truera_fqdn: str
    truera_kong_http_port: str
    truera_kong_https_port: str
    truera_deployment_url: str
    truera_keycloak_port: str = TRUERA_KEYCLOAK_PORT
    truera_keycloak_auth_base_route: str = TRUERA_KEYCLOAK_AUTH_BASE_ROUTE

    @property
    def valid_redirect_uris(self) -> Sequence[str]:
        return [
            f"http://{self.truera_fqdn}:{self.truera_kong_http_port}/*",
            f"https://{self.truera_fqdn}:{self.truera_kong_https_port}/*",
            f"http://{self.truera_fqdn}/*",
            f"https://{self.truera_fqdn}/*",
        ]

    @property
    def keycloak_internal_connection_string(self) -> str:
        return f"http://localhost:{self.truera_keycloak_port}{self.truera_keycloak_auth_base_route}"

    @property
    def keycloak_oidc_discovery_base_url(self) -> str:
        # Note: This needs to be the externally visible url since the login endpoint that the user is directed to is configured from this.
        return f"{self.truera_deployment_url}{self.truera_keycloak_auth_base_route}/realms/"

    @property
    def oidc_config_filepath(self) -> str:
        return os.path.join(
            self.truera_secrets_home, TRUERA_OIDC_CONFIG_FILENAME
        )

    @property
    def usermanagement_client_creds_filepath(self) -> str:
        return os.path.join(
            self.truera_secrets_home,
            TRUERA_USERMANAGEMENT_CLIENT_CREDS_FILENAME
        )


class KeycloakCommunicator():
    """
    Class for Interaction with the Keycloak API. API Documentation: https://www.keycloak.org/docs-api/15.0/rest-api/index.html
    """

    def __init__(
        self, keycloak_connection_string: str, keycloak_user: KeycloakAdminUser,
        logger: Logger
    ) -> None:
        self.connection_string = f"{keycloak_connection_string}"
        self.keycloak_user = keycloak_user
        self.logger = logger
        self.auth_headers = {}
        self.renew_auth_header()

    def renew_auth_header(self):
        self.logger.info("Generating auth token for keycloak")
        self.auth_headers = {
            'Authorization': f'Bearer {self.generate_auth_token()}'
        }

    def generate_auth_token(self):
        token_url = f"{self.connection_string}/realms/master/protocol/openid-connect/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = f'client_id=admin-cli&grant_type=password&username={self.keycloak_user.truera_keycloak_admin_user}&password={self.keycloak_user.truera_keycloak_admin_password}'
        try:
            token_resp = requests.post(token_url, headers=headers, data=payload)
            token_resp.raise_for_status()
            token = token_resp.json().get("access_token")
            if not token:
                raise KeycloakInitializationException(
                    "Unable to get keycloak access token"
                )
            return token
        except HTTPError as ex:
            if ex.response.status_code == 401:
                raise KeycloakInitializationException(
                    f"Invalid admin credentials: {ex.response.json()}"
                )
            raise ex

    def _make_req(
        self,
        url,
        method="GET",
        headers: Dict = {},
        data: str = None,
        ignore_exceptions: bool = False
    ):
        headers.update(self.auth_headers)
        resp = requests.request(
            method=method, url=url, headers=headers, data=data
        )
        if not ignore_exceptions:
            resp.raise_for_status()
        return resp

    def get_user_id(self, username: str):
        url = f"{self.connection_string}/admin/realms/master/users?username={username}"
        payload = json.dumps({"exact": True})
        resp = self._make_req(url, method="GET", data=payload)
        matching_users = resp.json()
        if len(matching_users) == 0:
            raise KeycloakInitializationException(
                f"Unable to find keycloak user: {username}"
            )

        return matching_users[0]["id"]

    def update_admin_user(self):
        # This updates the firstName field of the admin user. This is needed since TruEra services assume this field exists for all users.
        # This will fail if user federation is not connected.  Services should still start and ldap config can be fixed manually
        try:
            user_id = self.get_user_id(
                username=self.keycloak_user.truera_keycloak_admin_user
            )
            url = f"{self.connection_string}/admin/realms/master/users/{user_id}"
            payload = json.dumps(
                {
                    "firstName":
                        self.keycloak_user.truera_keycloak_admin_identifier
                }
            )
            headers = {"Content-Type": "application/json"}
            self._make_req(url, method="PUT", data=payload, headers=headers)
            return user_id
        except HTTPError as ex:
            self.logger.warning(
                f"Failed to add name to admin user: {ex.response.status_code} {ex.response.content}  Check ldap connection. Continuing..."
            )
            return None

    def create_keycloak_client(
        self,
        client_id: str,
        root_url: str,
        redirect_uris: Sequence[str],
        service_accounts_enabled: bool = False
    ):
        create_client_url = f"{self.connection_string}/admin/realms/master/clients"

        payload = json.dumps(
            asdict(
                KeycloakCreateClientInfo(
                    clientId=client_id,
                    name=client_id,
                    id=client_id,
                    redirectUris=redirect_uris,
                    rootUrl=root_url,
                    serviceAccountsEnabled=service_accounts_enabled
                )
            )
        )
        headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
        }
        resp = self._make_req(
            create_client_url, method="POST", headers=headers, data=payload
        )
        return resp

    def generate_client_secret(self, client_id: str):
        client_secret_url = f"{self.connection_string}/admin/realms/master/clients/{client_id}/client-secret"
        resp = self._make_req(client_secret_url, method="POST")
        client_secret = resp.json().get("value")
        if not client_secret:
            raise ValueError("Unable to generate client secret")
        return client_secret

    def get_client_secret(self, client_id: str):
        client_secret_url = f"{self.connection_string}/admin/realms/master/clients/{client_id}/client-secret"
        resp = self._make_req(client_secret_url, method="GET")
        client_secret = resp.json().get("value")
        if not client_secret:
            raise ValueError("Unable to get client secret")
        return client_secret

    def keycloak_client_exists(self, client_id: str):
        url = f"{self.connection_string}/admin/realms/master/clients?clientId={client_id}"
        resp = self._make_req(url, method="GET")
        return len(resp.json()) != 0

    def delete_existing_client(self, client_id: str):
        url = f"{self.connection_string}/admin/realms/master/clients/{client_id}"
        self._make_req(url, method="DELETE", ignore_exceptions=True)

    def get_service_account_user(self, client_id: str):
        url = f"{self.connection_string}/admin/realms/master/clients/{client_id}/service-account-user"
        resp = self._make_req(url, method="GET")
        return KeycloakUserInfo(resp.json()["id"], resp.json()["username"])

    def get_admin_role(self) -> KeycloakUserRole:
        url = f"{self.connection_string}/admin/realms/master/roles/admin"
        resp = self._make_req(url, method="GET")
        return KeycloakUserRole(resp.json()["id"], resp.json()["name"])

    def grant_role_to_user(
        self, role: KeycloakUserRole, user: KeycloakUserInfo
    ):
        url = f"{self.connection_string}/admin/realms/master/users/{user.id}/role-mappings/realm"
        self.logger.info(f"Granting role {role} to user {user.id}")
        payload = [asdict(role)]
        headers = {'Content-Type': 'application/json'}
        resp = self._make_req(
            url, method="POST", headers=headers, data=json.dumps(payload)
        )
        return resp

    def set_master_realm_configuration(self):
        self.logger.info("Updating master realm configuration...")
        url = f"{self.connection_string}/admin/realms/master"
        # get the current realm configuration
        headers = {"Content-Type": "application/json"}
        resp = self._make_req(url, method="GET", headers=headers)
        realm_representation = dict(resp.json())
        modify_dict = {
            "displayName":
                "TruEra",
            "displayNameHtml":
                "<div class=\"kc-logo-text\"><span>TruEra</span></div>",
            "accountTheme":
                "truera",
            "adminTheme":
                "truera",
            "loginTheme":
                "truera",
            "accessTokenLifespan":
                KEYCLOAK_ACCESS_TOKEN_LIFESPAN
        }
        realm_representation.update(modify_dict)
        payload = json.dumps(realm_representation)
        self._make_req(url, method="PUT", headers=headers, data=payload)


class KeycloakInitializer():

    def __init__(
        self,
        truera_config: TrueraConfiguration,
        keycloak_user: KeycloakAdminUser,
        logger: Logger,
        startup_timeout: int = 30,
        keycloak_communicator: KeycloakCommunicator = None
    ) -> None:
        self.truera_config = truera_config
        self.keycloak_user = keycloak_user
        self.startup_timeout = startup_timeout
        self.logger = logger
        self.logger.info("Waiting for keycloak to startup...")
        self._wait_for_keycloak_to_initialize()
        self.logger.info("Keycloak running")
        self.communicator = keycloak_communicator or KeycloakCommunicator(
            keycloak_connection_string=truera_config.
            keycloak_internal_connection_string,
            keycloak_user=keycloak_user,
            logger=logger
        )

    def _is_keycloak_up(self):
        try:
            resp = requests.get(
                self.truera_config.keycloak_internal_connection_string
            )
            return resp.status_code == 200
        except ConnectionError:
            return False

    def _wait_for_keycloak_to_initialize(self):
        if self.startup_timeout < 0:
            return
        start = time.time()
        while time.time() < start + self.startup_timeout:
            if self._is_keycloak_up():
                break
            time.sleep(5)

        if not self._is_keycloak_up():
            raise KeycloakInitializationException(
                "Unable to initialize keycloak"
            )

    def save_keycloak_config(
        self, kong_client: KeycloakClientInfo,
        usermanagement_client: KeycloakClientInfo
    ):
        oidc_config_filepath = self.truera_config.oidc_config_filepath
        self.logger.info(
            f"Saving keycloak oidc config with kong-client config at {oidc_config_filepath}"
        )
        if os.path.isfile(oidc_config_filepath):
            self.logger.warning(
                f"Overwriting contents of {oidc_config_filepath}"
            )
        config_lst = [
            f'export TRUERA_KONG_OIDC_BASE_URL="{self.truera_config.keycloak_oidc_discovery_base_url}"',
            'export TRUERA_KONG_OIDC_DISCOVERY_SUFFIX="/.well-known/openid-configuration"',
            f'export TRUERA_KONG_OIDC_CLIENT_ID="{kong_client.client_id}"',
            f'export TRUERA_KONG_OIDC_CLIENT_SECRET="{kong_client.client_secret}"',
            'export TRUERA_KONG_OIDC_REALM="master"\n'
        ]
        with open(oidc_config_filepath, "w") as f:
            f.write("\n".join(config_lst))

        usermanagement_client_creds_filepath = self.truera_config.usermanagement_client_creds_filepath
        self.logger.info(
            f"Saving keycloak usermanagemnet client info in {usermanagement_client_creds_filepath}"
        )
        if os.path.isfile(usermanagement_client_creds_filepath):
            self.logger.warning(
                f"Overwriting contents of {usermanagement_client_creds_filepath}"
            )
        with open(usermanagement_client_creds_filepath, "w") as f:
            json.dump(asdict(usermanagement_client), f)

    def _initialize_client(
        self,
        client_id: str,
        reinit_client: bool = False,
        service_accounts_enabled: bool = False
    ) -> KeycloakClientInfo:
        """Gets or Creates client in Keycloak with designated client_id. Returns client configuration."""
        if reinit_client:
            self.logger.info(f"Deleting existing keycloak client: {client_id}")
            self.communicator.delete_existing_client(client_id)
        print(f"client_id: {client_id}")
        if self.communicator.keycloak_client_exists(client_id):
            self.logger.info(
                f"Initializing config from existing keycloak client: {client_id}"
            )
            client_secret = self.communicator.get_client_secret(
                client_id=client_id
            )
        else:
            self.logger.info(f"Creating new keycloak client: {client_id}")
            self.communicator.create_keycloak_client(
                client_id=client_id,
                root_url=self.truera_config.truera_deployment_url,
                redirect_uris=self.truera_config.valid_redirect_uris,
                service_accounts_enabled=service_accounts_enabled
            )
            client_secret = self.communicator.generate_client_secret(
                client_id=client_id
            )

        return KeycloakClientInfo(
            client_id=client_id, client_secret=client_secret
        )

    def _give_service_account_admin(
        self, service_account_client: KeycloakClientInfo
    ):
        self.logger.info(
            f"Giving admin rights to service account: {service_account_client.client_id}"
        )
        user = self.communicator.get_service_account_user(
            client_id=service_account_client.client_id
        )
        admin_role = self.communicator.get_admin_role()
        self.communicator.grant_role_to_user(admin_role, user)

    def initialize_keycloak(self, reinit_client: bool = False):
        self.logger.debug("Updating keycloak admin user firstName")
        admin_user_id = self.communicator.update_admin_user()
        if admin_user_id:
            # TODO: waht is this for again?
            os.environ[ENV_TRUERA_KEYCLOAK_USER_ID] = admin_user_id

        # Get or Create Kong Client
        kong_client = self._initialize_client(
            client_id=KEYCLOAK_KONG_CLIENT_IDENTIFIER,
            reinit_client=reinit_client
        )
        self.logger.info(f"Initialized kong client: {kong_client.client_id}")

        # Get or Create Usermanagement Client
        # TODO: Ability to reinit this?
        usermanagement_client = self._initialize_client(
            client_id=KEYCLOAK_USERMANAGEMENT_CLIENT_IDENTIFIER,
            service_accounts_enabled=True
        )
        self._give_service_account_admin(usermanagement_client)

        self.logger.info(
            f"initialized usermanagment client: {usermanagement_client.client_id}"
        )

        self.save_keycloak_config(kong_client, usermanagement_client)

        self.communicator.set_master_realm_configuration()


@click.group()
def keycloak_client_cli():
    pass


@keycloak_client_cli.command()
@click.option(
    "--truera_keycloak_admin_user",
    "-u",
    default="admin",
    type=str,
    help="keycloak admin username"
)
@click.option(
    "--truera_keycloak_admin_password",
    "-p",
    required=True,
    type=str,
    help="keycloak admin password"
)
@click.option(
    "--truera_secrets_home",
    required=True,
    type=str,
    help="path to secrets directory to save oidc configuration"
)
@click.option("--truera_fqdn", required=True, help="FQDN of truera deployment")
@click.option(
    "--truera_kong_http_port",
    required=True,
    type=str,
    help="port that kong listens on for http requests"
)
@click.option(
    "--truera_kong_https_port",
    required=True,
    type=str,
    help="port that kong listens on for https requests"
)
@click.option(
    "--reinit_keycloak_client",
    default="0",
    type=str,
    help="specify whether to recreate client"
)
@click.option(
    "--force_keycloak_http",
    default="0",
    type=str,
    help="specify whether to perform oidc discovery via http"
)
def initialize(
    truera_keycloak_admin_user,
    truera_keycloak_admin_password,
    truera_secrets_home,
    truera_fqdn,
    truera_kong_http_port,
    truera_kong_https_port,
    reinit_keycloak_client,
    force_keycloak_http,
):
    logging.basicConfig()
    logger = logging.getLogger(KEYCLOAK_CONFIG_LOGGER)
    log_level = logging.INFO
    logger.setLevel(log_level)

    if not os.path.isdir(truera_secrets_home):
        raise ValueError(f"Must set TRUERA_SECRETS_HOME to initialize keycloak")

    if truera_fqdn == "localhost" or force_keycloak_http == "1":
        truera_deployment_url = f"http://{truera_fqdn}:{truera_kong_http_port}"
    else:
        truera_deployment_url = f"https://{truera_fqdn}:{truera_kong_https_port}"

    truera_conf = TrueraConfiguration(
        truera_secrets_home=truera_secrets_home,
        truera_fqdn=truera_fqdn,
        truera_kong_http_port=truera_kong_http_port,
        truera_kong_https_port=truera_kong_https_port,
        truera_deployment_url=truera_deployment_url
    )
    keycloak_user = KeycloakAdminUser(
        truera_keycloak_admin_user=truera_keycloak_admin_user,
        truera_keycloak_admin_password=truera_keycloak_admin_password
    )

    logger.info(
        f"Configuring keycloak at {truera_conf.keycloak_internal_connection_string} for deployment {truera_deployment_url}"
    )
    initializer = KeycloakInitializer(
        truera_config=truera_conf, keycloak_user=keycloak_user, logger=logger
    )
    reinit_client = reinit_keycloak_client == "1"
    initializer.initialize_keycloak(reinit_client=reinit_client)


@keycloak_client_cli.command()
@click.option(
    "--truera_keycloak_admin_user",
    "-u",
    default="admin",
    help="keycloak admin username"
)
@click.option(
    "--truera_keycloak_admin_password",
    "-p",
    required=True,
    help="keycloak admin password"
)
def add_keycloak_user_as_truera_admin(
    truera_keycloak_admin_user, truera_keycloak_admin_password
):
    logging.basicConfig()
    logger = logging.getLogger(KEYCLOAK_CONFIG_LOGGER)
    log_level = logging.INFO
    logger.setLevel(log_level)

    truera_conf = TrueraConfiguration("", "", "", "", "")
    keycloak_user = KeycloakAdminUser(
        truera_keycloak_admin_user=truera_keycloak_admin_user,
        truera_keycloak_admin_password=truera_keycloak_admin_password
    )
    comm = KeycloakCommunicator(
        keycloak_connection_string=truera_conf.
        keycloak_internal_connection_string,
        keycloak_user=keycloak_user,
        logger=logger
    )
    user_id = comm.get_user_id(truera_keycloak_admin_user)

    logger.info(f"Adding keycloak user {user_id} as truera admin")
    headers = {
        'X-Consumer-Username': 'truera',
        'X-Consumer-Id': 'truera',
        'X-Tenant-Id': 'on-prem'
    }
    response = requests.post(
        f"http://localhost:9298/admin/{user_id}", headers=headers
    )
    if response.status_code != 200:
        logger.warning(
            f"Failed to add keycloak user '{truera_keycloak_admin_user}' as truera admin. status_code={response.status_code} error={response.text}"
        )


if __name__ == "__main__":
    keycloak_client_cli()
