from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel

from chalk.integrations.named import load_integration_variable
from chalk.streams.base import StreamSource
from chalk.utils.duration import Duration
from chalk.utils.string import comma_whitespace_split


class KafkaSource(StreamSource, BaseModel, frozen=True):
    bootstrap_server: Optional[Union[str, List[str]]] = None
    topic: Optional[Union[str, List[str]]] = None
    ssl_keystore_location: Optional[str] = None
    """
    An S3 or GCS URI that points to the keystore file that should be
        used for brokers. You must configure the appropriate AWS or
        GCP integration in order for Chalk to be able to access these
        files.
    """

    client_id_prefix: str = "chalk/"
    group_id_prefix: str = "chalk/"

    security_protocol: Literal["PLAINTEXT", "SSL", "SASL_PLAINTEXT", "SASL_SSL"] = "PLAINTEXT"
    """
    Protocol used to communicate with brokers.
            Valid values are: PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL.
            Default: PLAINTEXT.
    """

    sasl_mechanism: Literal["PLAIN", "GSSAPI", "SCRAM-SHA-256", "SCRAM-SHA-512", "OAUTHBEARER"] = "PLAIN"
    """
    Authentication mechanism when security_protocol
            is configured for SASL_PLAINTEXT or SASL_SSL. Valid values are:
            PLAIN, GSSAPI, SCRAM-SHA-256, SCRAM-SHA-512, OAUTHBEARER.
            Default: PLAIN
    """

    sasl_username: Optional[str] = None
    """
    Username for SASL PLAIN, SCRAM-SHA-256, or SCRAM-SHA-512 authentication.
            Default: None
    """

    sasl_password: Optional[str] = None
    """
    Password for SASL PLAIN, SCRAM-SHA-256, or SCRAM-SHA-512 authentication.
            Default: None
    """

    name: Optional[str] = None
    """
    The name of the integration, as configured in your web dashboard portal.
    """

    late_arrival_deadline: Duration = "infinity"
    """
    Messages older than this deadline will not be processed.
    """

    def __init__(
        self,
        *,
        bootstrap_server: Optional[Union[str, List[str]]] = None,
        topic: Optional[Union[str, List[str]]] = None,
        ssl_keystore_location: Optional[str] = None,
        client_id_prefix: Optional[str] = None,
        group_id_prefix: Optional[str] = None,
        security_protocol: Optional[str] = None,
        sasl_mechanism: Optional[Literal["PLAIN", "GSSAPI", "SCRAM-SHA-256", "SCRAM-SHA-512", "OAUTHBEARER"]] = None,
        sasl_username: Optional[str] = None,
        sasl_password: Optional[str] = None,
        name: Optional[str] = None,
        late_arrival_deadline: Duration = "infinity",
    ):
        super(KafkaSource, self).__init__(
            bootstrap_server=bootstrap_server
            or load_integration_variable(
                name="KAFKA_BOOTSTRAP_SERVER", integration_name=name, parser=comma_whitespace_split
            ),
            topic=topic
            or load_integration_variable(name="KAFKA_TOPIC", integration_name=name, parser=comma_whitespace_split),
            ssl_keystore_location=ssl_keystore_location
            or load_integration_variable(name="KAFKA_SSL_KEYSTORE_LOCATION", integration_name=name),
            client_id_prefix=client_id_prefix
            or load_integration_variable(name="KAFKA_CLIENT_ID_PREFIX", integration_name=name)
            or KafkaSource.__fields__.get("client_id_prefix").default,
            group_id_prefix=group_id_prefix
            or load_integration_variable(name="KAFKA_GROUP_ID_PREFIX", integration_name=name)
            or KafkaSource.__fields__.get("group_id_prefix").default,
            security_protocol=security_protocol
            or load_integration_variable(name="KAFKA_SECURITY_PROTOCOL", integration_name=name)
            or KafkaSource.__fields__.get("security_protocol").default,
            sasl_mechanism=sasl_mechanism
            or load_integration_variable(name="KAFKA_SASL_MECHANISM", integration_name=name)
            or KafkaSource.__fields__.get("sasl_mechanism").default,
            sasl_username=sasl_username or load_integration_variable(name="KAFKA_SASL_USERNAME", integration_name=name),
            sasl_password=sasl_password or load_integration_variable(name="KAFKA_SASL_PASSWORD", integration_name=name),
            name=name,
            late_arrival_deadline=late_arrival_deadline,
        )

    def config_to_json(self) -> Any:
        return self.json()
