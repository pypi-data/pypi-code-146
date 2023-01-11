from dataclasses import asdict
from dataclasses import dataclass
import inspect
import logging
from logging import Logger
import os
from typing import Dict, List

from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0
import click

logging.basicConfig()

DISABLE_SIGNUP_CONNECTION_OPTIONS = {"disable_signup": True}


@dataclass
class Auth0Config:
    domain: str
    m2m_client_id: str
    m2m_client_secret: str
    auth0_truera_aad_connection_id: str = None
    login_domain: str = None

    @property
    def auth0_login_domain(self):
        return self.login_domain or self.domain


@dataclass
class TruEraDeployment:
    deployment_id: str
    truera_fqdn: str

    @property
    def auth0_client_name(self) -> str:
        return f"{self.deployment_id}"

    @property
    def auth0_connection_name(self) -> str:
        return f"{self.deployment_id}-db"


# NOTE: Need to turn off existing configuration at the Auth0 tenant level that auth-connectes any new client to any existing connection
@dataclass
class Auth0CreateClientBody:
    name: str
    # NOTE: These callbacks do not support wildcards.
    callbacks: List[str]
    # NOTE: Auth0 enforces uniquencess of client_aliases. client_alias must always be set as [client name].
    allowed_logout_urls: List[str]
    client_aliases: List[str]
    initiate_login_uri: str
    organization_usage: str = "allow"
    token_endpoint_auth_method: str = "client_secret_post"
    logo_uri: str = "https://truera.com/wp-content/uploads/2021/04/Group-70.svg"
    oidc_conformant: bool = True  # NOTE: This is needed for the Auth0 client to support the invitation flow.
    # grant_types: List[str] # TODO: Do we need this?


@dataclass
class Auth0CreateConnectionBody:
    name: str
    options: Dict
    strategy: str = "auth0"
    # enabled_clients: List[str] # NOTE: We will update this post-creation


@dataclass
class Auth0Client:
    name: str
    client_id: str
    client_secret: str
    callbacks: List[str]


@dataclass
class Auth0Connection:
    name: str
    id: str
    strategy: str
    enabled_clients: List[str]


# Util functions:
def auth0_client_factory(client_data: Dict) -> Auth0Client:
    """Construct Auth0Client dataclass instance from raw json"""
    client_fields = list(inspect.signature(Auth0Client).parameters.keys())
    return Auth0Client(**{k: client_data[k] for k in client_fields})


def auth0_connection_factory(connection_data: Dict) -> Auth0Connection:
    """Construct Auth0Connection dataclass instance from raw json"""
    connection_fields = list(
        inspect.signature(Auth0Connection).parameters.keys()
    )
    return Auth0Connection(**{k: connection_data[k] for k in connection_fields})


def build_client_oidc_config(
    client: Auth0Client, auth0_config: Auth0Config
) -> str:
    config_lst = [
        f'export TRUERA_OIDC_USER_ID_PROPERTY=email',  # This sets email as the ID field
        f'export TRUERA_KONG_OIDC_BASE_URL="https://{auth0_config.auth0_login_domain}"',
        'export TRUERA_KONG_OIDC_DISCOVERY_SUFFIX=".well-known/openid-configuration"',
        f'export TRUERA_KONG_OIDC_CLIENT_ID="{client.client_id}"',
        f'export TRUERA_KONG_OIDC_CLIENT_SECRET="{client.client_secret}"',
        f'export TRUERA_KONG_OIDC_END_SESSION_ENDPOINT="https://{auth0_config.auth0_login_domain}/v2/logout?federated'
        f'&client_id={client.client_id}"',
        'export TRUERA_KONG_OIDC_REALM="/"\n'
    ]
    return "\n".join(config_lst)


class Auth0Initializer():

    def __init__(self, auth0_config: Auth0Config, logger: Logger) -> None:
        self.auth0_config = auth0_config
        self.logger = logger
        self.logger.info(
            f"Connecting to Auth0 using config: {self.auth0_config}"
        )
        self.management_token = self._get_management_token()
        self.auth0 = Auth0(
            domain=self.auth0_config.domain, token=self.management_token
        )

    def _get_management_token(self):
        # NOTE: This needs to be an auth0 M2M client that is authorized for the auth0 management API.
        return GetToken(domain=self.auth0_config.domain).client_credentials(
            client_id=self.auth0_config.m2m_client_id,
            client_secret=self.auth0_config.m2m_client_secret,
            audience=f"https://{self.auth0_config.domain}/api/v2/"
        )["access_token"]

    def _get_client_if_exists(self, client_name: str) -> Auth0Client:
        existing_clients = self.auth0.clients.all(per_page=100)
        existing_client_names = [c["name"] for c in existing_clients]
        if client_name in existing_client_names:
            client_data = existing_clients[
                existing_client_names.index(client_name)]
            return auth0_client_factory(client_data)
        return None

    def _get_connection_if_exists(
        self, connection_name: str
    ) -> Auth0Connection:
        existing_connections = self.auth0.connections.all(per_page=100)
        existing_connection_names = [c["name"] for c in existing_connections]
        if connection_name in existing_connection_names:
            connection_data = existing_connections[
                existing_connection_names.index(connection_name)]
            return auth0_connection_factory(connection_data)
        return None

    def _get_connection_by_id(self, connection_id) -> Auth0Connection:
        connection_data = self.auth0.connections.get(connection_id)
        return auth0_connection_factory(connection_data)

    def _update_connection_with_clients(
        self, connection: Auth0Connection, clients_to_enable: List[str]
    ):
        """Ensures that all client ids in given list are enabled in the given connection"""
        # NOTE: Must enable M2M service client in connection in order to programatically provision users
        clients_to_enable = [
            c for c in clients_to_enable if c not in connection.enabled_clients
        ]
        if clients_to_enable:
            self.logger.info(
                f"Updating connection {connection.name} with clients {clients_to_enable}"
            )
            connection.enabled_clients.extend(clients_to_enable)
            self.auth0.connections.update(
                connection.id, {"enabled_clients": connection.enabled_clients}
            )

    def get_or_create_client(
        self, truera_deployment: TruEraDeployment
    ) -> Auth0Client:
        client_name = truera_deployment.auth0_client_name
        client = self._get_client_if_exists(client_name)
        if client:
            self.logger.info(f"Using existing Auth0 Client: {client.name}")
            return client

        self.logger.info(f"Creating new Auth0 Client: {client_name}")
        create_client_body = Auth0CreateClientBody(
            name=client_name,
            client_aliases=[client_name],
            initiate_login_uri=f"https://{truera_deployment.truera_fqdn}",
            callbacks=[
                # NOTE: localhost:8000 is hardcoded here to support local environments.
                f"http://localhost:8000/cb",
                f"http://{truera_deployment.truera_fqdn}/cb",
                f"https://{truera_deployment.truera_fqdn}/cb"
            ],
            allowed_logout_urls=[
                f"http://{truera_deployment.truera_fqdn}",
                f"https://{truera_deployment.truera_fqdn}"
            ]
        )
        client_data = self.auth0.clients.create(asdict(create_client_body))
        return auth0_client_factory(client_data)

    def get_or_create_connection(
        self, truera_deployment: TruEraDeployment
    ) -> Auth0Connection:
        conn_name = truera_deployment.auth0_connection_name
        conn = self._get_connection_if_exists(conn_name)
        if conn:
            self.logger.info(f"Using existing Auth0 Connection: {conn_name}")
            return conn

        self.logger.info(f"Creating new Auth0 Connection: {conn_name}")
        create_connection_body = Auth0CreateConnectionBody(
            name=conn_name, options=DISABLE_SIGNUP_CONNECTION_OPTIONS
        )
        conn_data = self.auth0.connections.create(
            asdict(create_connection_body)
        )
        return auth0_connection_factory(conn_data)

    def initialize(
        self,
        truera_deployment: TruEraDeployment,
        attach_truera_aad_connection: bool = True
    ) -> str:
        self.logger.info(
            f"Initializing Auth0 client + connection for deployment: {truera_deployment}"
        )
        client: Auth0Client = self.get_or_create_client(truera_deployment)
        connection: Auth0Connection = self.get_or_create_connection(
            truera_deployment
        )
        self._update_connection_with_clients(
            connection, [client.client_id, self.auth0_config.m2m_client_id]
        )
        self.logger.info(f"Auth0 Client: {client.name}, {client.client_id}")
        self.logger.info(
            f"Auth0 Connection: {connection.name}, {connection.id}"
        )

        if attach_truera_aad_connection:
            self.logger.info("Enabling client in truera AAD connection")
            aad_connection = self._get_connection_by_id(
                self.auth0_config.auth0_truera_aad_connection_id
            )
            self._update_connection_with_clients(
                aad_connection,
                [client.client_id, self.auth0_config.m2m_client_id]
            )

        return build_client_oidc_config(client, self.auth0_config)

    def destroy(self, truera_deployment: TruEraDeployment) -> None:
        self.logger.info(
            f"Tearing down Auth0 resources for deployment: {truera_deployment}"
        )
        # TODO: Implement
        pass


@click.group()
def auth0_client_cli():
    pass


@auth0_client_cli.command()
@click.option(
    "--truera_deployment_id",
    required=True,
    help="Account name of truera deployment"
)
@click.option(
    "--truera_fqdn", required=True, help="TRUERA_FQDN for truera deployment"
)
@click.option(
    "--auth0_domain", required=True, help="Auth0 domain for to create client"
)
@click.option(
    "--auth0_m2m_client_id", required=True, help="Auth0 M2M client id"
)
@click.option(
    "--auth0_m2m_client_secret", required=True, help="Auth0 M2M client secret"
)
@click.option(
    "--auth0_truera_aad_connection_id",
    required=True,
    help="Auth0 truera AAD connection id"
)
@click.option(
    "--auth0_login_domain",
    default=None,
    help=
    "Auth0 login domain. If none given, assumed to be the same as 'auth0_domain'"
)
@click.option(
    "--oidc_config_output_file",
    default=None,
    help="Absolute filepath to output oidc config"
)
def initialize(
    truera_deployment_id: str, truera_fqdn: str, auth0_domain: str,
    auth0_m2m_client_id: str, auth0_m2m_client_secret: str,
    auth0_truera_aad_connection_id: str, auth0_login_domain: str,
    oidc_config_output_file: str
):
    logger = logging.getLogger("truera.Auth0Initializer")
    log_level = logging.INFO
    logger.setLevel(log_level)

    truera_deployment = TruEraDeployment(
        deployment_id=truera_deployment_id, truera_fqdn=truera_fqdn
    )

    auth0_config = Auth0Config(
        domain=auth0_domain,
        m2m_client_id=auth0_m2m_client_id,
        m2m_client_secret=auth0_m2m_client_secret,
        auth0_truera_aad_connection_id=auth0_truera_aad_connection_id,
        login_domain=auth0_login_domain
    )

    auth0_initializer = Auth0Initializer(auth0_config, logger)

    attach_truera_aad_connection = True if auth0_truera_aad_connection_id else False
    oidc_config = auth0_initializer.initialize(
        truera_deployment, attach_truera_aad_connection
    )

    if oidc_config_output_file:
        if not os.path.isdir(os.path.dirname(oidc_config_output_file)):
            raise ValueError(
                f"Directory {os.path.dirname(oidc_config_output_file)} does not exist!"
            )
        logger.info(f"Saving oidc config to file {oidc_config_output_file}")
        with open(oidc_config_output_file, "w") as f:
            f.write(oidc_config)
    else:
        logger.info(f"No outfile given for oidc config -> printing to stdout")
        print(oidc_config)


@auth0_client_cli.command()
@click.option(
    "--truera_deployment_id",
    required=True,
    help="Account name of truera deployment"
)
@click.option(
    "--auth0_domain", required=True, help="Auth0 domain for to create client"
)
@click.option(
    "--auth0_m2m_client_id", required=True, help="Auth0 M2M client id"
)
@click.option(
    "--auth0_m2m_client_secret", required=True, help="Auth0 M2M client secret"
)
def destroy(
    truera_deployment_id: str,
    auth0_domain: str,
    auth0_m2m_client_id: str,
    auth0_m2m_client_secret: str,
):
    logger = logging.getLogger("truera.Auth0Initializer")
    log_level = logging.INFO
    logger.setLevel(log_level)

    truera_deployment = TruEraDeployment(
        deployment_id=truera_deployment_id, truera_fqdn=None
    )

    auth0_config = Auth0Config(
        domain=auth0_domain,
        m2m_client_id=auth0_m2m_client_id,
        m2m_client_secret=auth0_m2m_client_secret,
        auth0_truera_aad_connection_id=None
    )

    auth0_initializer = Auth0Initializer(auth0_config, logger)
    auth0_initializer.destroy(truera_deployment)


if __name__ == "__main__":
    auth0_client_cli()
