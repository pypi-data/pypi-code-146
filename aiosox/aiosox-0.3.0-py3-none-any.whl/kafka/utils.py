
import orjson
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from kafka.coordinator.assignors.roundrobin import RoundRobinPartitionAssignor


def kafka_serialize(value):
    """function to handle encoding of a value"""
    if value is None:
        return None
    result = None
    try:
        result = orjson.dumps(value)
    except orjson.JSONEncodeError as e:
        return None
    return result


def kafka_deserialize(value):
    """function to handle decoding of a value"""
    if not isinstance(value, bytes):
        return orjson.loads(orjson.dumps(value))
    decoded_byte_value = value.decode("utf-8")
    return orjson.loads(orjson.dumps(decoded_byte_value))


def get_kafka_consumer(
    *topics,
    bootstrap_servers="localhost",
    group_id: str|None,
    key_deserializer=kafka_deserialize,
    value_deserializer=kafka_deserialize,
    fetch_max_wait_ms=500,
    fetch_max_bytes=52428800,
    fetch_min_bytes=1,
    max_partition_fetch_bytes=1 * 1024 * 1024,
    request_timeout_ms=40 * 1000,
    retry_backoff_ms=100,
    auto_offset_reset="latest",
    enable_auto_commit=True,
    auto_commit_interval_ms=5000,
    check_crcs=True,
    metadata_max_age_ms=5 * 60 * 1000,
    partition_assignment_strategy=(RoundRobinPartitionAssignor,),
    max_poll_interval_ms=300000,
    rebalance_timeout_ms=None,
    session_timeout_ms=10000,
    heartbeat_interval_ms=3000,
    consumer_timeout_ms=200,
    max_poll_records=None,
    ssl_context=None,
    security_protocol="PLAINTEXT",
    api_version="auto",
    exclude_internal_topics=True,
    connections_max_idle_ms=540000,
    isolation_level="read_uncommitted",
    sasl_mechanism="PLAIN",
    sasl_plain_password=None,
    sasl_plain_username=None,
    sasl_kerberos_service_name="kafka",
    sasl_kerberos_domain_name=None,
    sasl_oauth_token_provider=None,
    ssl_cert=None,
) -> AIOKafkaConsumer:
    """function to get an instance of aiokafka consumer"""

    return AIOKafkaConsumer(
        *topics,
        value_deserializer=value_deserializer,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset=auto_offset_reset,
        isolation_level=isolation_level,
        group_id=group_id,
        key_deserializer=key_deserializer,
        fetch_max_wait_ms=fetch_max_wait_ms,
        fetch_max_bytes=fetch_max_bytes,
        fetch_min_bytes=fetch_min_bytes,
        max_partition_fetch_bytes=max_partition_fetch_bytes,
        request_timeout_ms=request_timeout_ms,
        retry_backoff_ms=retry_backoff_ms,
        enable_auto_commit=enable_auto_commit,
        auto_commit_interval_ms=auto_commit_interval_ms,
        check_crcs=check_crcs,
        metadata_max_age_ms=metadata_max_age_ms,
        partition_assignment_strategy=partition_assignment_strategy,
        max_poll_interval_ms=max_poll_interval_ms,
        rebalance_timeout_ms=rebalance_timeout_ms,
        session_timeout_ms=session_timeout_ms,
        heartbeat_interval_ms=heartbeat_interval_ms,
        consumer_timeout_ms=consumer_timeout_ms,
        max_poll_records=max_poll_records,
        ssl_context=ssl_context,
        security_protocol=security_protocol,
        api_version=api_version,
        exclude_internal_topics=exclude_internal_topics,
        connections_max_idle_ms=connections_max_idle_ms,
        sasl_mechanism=sasl_mechanism,
        sasl_plain_password=sasl_plain_password,
        sasl_plain_username=sasl_plain_username,
        sasl_kerberos_service_name=sasl_kerberos_service_name,
        sasl_kerberos_domain_name=sasl_kerberos_domain_name,
        sasl_oauth_token_provider=sasl_oauth_token_provider,
    )


def get_kafka_producer(
    bootstrap_servers: str,
) -> AIOKafkaProducer:
    security_protocol = "PLAINTEXT"

    return AIOKafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=kafka_serialize,
        security_protocol=security_protocol,
    )
