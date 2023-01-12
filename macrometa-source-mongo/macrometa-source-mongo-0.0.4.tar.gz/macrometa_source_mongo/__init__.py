#!/usr/bin/env python3
import copy
import json
import sys
from typing import List, Dict, Optional
from urllib import parse

import pkg_resources
import singer
from pymongo import MongoClient
from singer import metadata, metrics, utils
from c8connector import (
    C8Connector, ConfigProperty, Sample, Schema,
    ConfigAttributeType, SchemaAttribute)

from macrometa_source_mongo.sync_strategies import change_streams
from macrometa_source_mongo.sync_strategies import common
from macrometa_source_mongo.sync_strategies import full_table
from macrometa_source_mongo.sync_strategies import incremental
from macrometa_source_mongo.sync_strategies.sample_data import fetch_samples
from macrometa_source_mongo.config_utils import validate_config
from macrometa_source_mongo.db_utils import get_databases, produce_collection_schema, get_attribute_type
from macrometa_source_mongo.errors import InvalidReplicationMethodException, NoReadPrivilegeException
from macrometa_source_mongo.stream_utils import write_schema_message, \
    streams_list_to_dict, filter_streams_by_replication_method, get_streams_to_sync

LOGGER = singer.get_logger('macrometa_source_mongo')

REQUIRED_CONFIG_KEYS = [
    'host',
    'user',
    'password',
    'auth_database',
    'database',
    'source_collection'
]

REQUIRED_CONFIG_KEYS_NON_SRV = REQUIRED_CONFIG_KEYS + ['port']

LOG_BASED_METHOD = 'LOG_BASED'
INCREMENTAL_METHOD = 'INCREMENTAL'
FULL_TABLE_METHOD = 'FULL_TABLE'


def do_discover(client: MongoClient, config: Dict):
    """
    Run discovery mode where the mongodb cluster is scanned and
    all the collections of the database in config
    are turned into streams.
    The result is dumped to stdout as json
    Args:
        client:MongoDB Client instance
        config: DB config
    """
    streams = []

    if config['database'] not in get_databases(client, config):
        raise NoReadPrivilegeException(config['user'], config['database'])

    database = client[config['database']]
    collection_name = config['source_collection']
    collection = database[collection_name]
    is_view = collection.options().get('viewOn') is not None

    # Add support for views if needed here
    if is_view:
        raise KeyError(f'Views are not supported.')

    LOGGER.info("Getting collection info for db '%s', collection '%s'", database.name, collection_name)
    streams.append(produce_collection_schema(collection))

    json.dump({'streams': streams}, sys.stdout, indent=2)

    return streams


def clear_state_on_replication_change(stream: Dict, state: Dict) -> Dict:
    """
    Clears the given state if replication method of given stream has changed
    Args:
        stream: stream dictionary
        state: state

    Returns: new state

    """
    md_map = metadata.to_map(stream['metadata'])
    tap_stream_id = stream['tap_stream_id']

    # replication method changed
    current_replication_method = metadata.get(md_map, (), 'replication-method')
    last_replication_method = singer.get_bookmark(state, tap_stream_id, 'last_replication_method')
    if last_replication_method is not None and (current_replication_method != last_replication_method):
        log_msg = 'Replication method changed from %s to %s, will re-replicate entire collection %s'
        LOGGER.info(log_msg, last_replication_method, current_replication_method, tap_stream_id)
        state = singer.reset_stream(state, tap_stream_id)

    # replication key changed
    if current_replication_method == 'INCREMENTAL':
        last_replication_key = singer.get_bookmark(state, tap_stream_id, 'replication_key_name')
        current_replication_key = metadata.get(md_map, (), 'replication-key')
        if last_replication_key is not None and (current_replication_key != last_replication_key):
            log_msg = 'Replication Key changed from %s to %s, will re-replicate entire collection %s'
            LOGGER.info(log_msg, last_replication_key, current_replication_key, tap_stream_id)
            state = singer.reset_stream(state, tap_stream_id)
        state = singer.write_bookmark(state, tap_stream_id, 'replication_key_name', current_replication_key)

    state = singer.write_bookmark(state, tap_stream_id, 'last_replication_method', current_replication_method)

    return state


def sync_traditional_stream(client: MongoClient, stream: Dict, state: Dict):
    """
    Sync given stream
    Args:
        client: MongoDb client instance
        stream: stream to sync
        state: state
    """
    tap_stream_id = stream['tap_stream_id']

    common.COUNTS[tap_stream_id] = 0
    common.TIMES[tap_stream_id] = 0
    common.SCHEMA_COUNT[tap_stream_id] = 0
    common.SCHEMA_TIMES[tap_stream_id] = 0

    md_map = metadata.to_map(stream['metadata'])
    replication_method = metadata.get(md_map, (), 'replication-method')

    if replication_method not in {INCREMENTAL_METHOD, FULL_TABLE_METHOD}:
        raise InvalidReplicationMethodException(replication_method,
                                                'replication method needs to be either FULL_TABLE or INCREMENTAL')

    database_name = metadata.get(md_map, (), 'database-name')

    # Emit a state message to indicate that we've started this stream
    state = clear_state_on_replication_change(stream, state)
    state = singer.set_currently_syncing(state, stream['tap_stream_id'])
    singer.write_message(singer.StateMessage(value=copy.deepcopy(state)))

    write_schema_message(stream)
    common.SCHEMA_COUNT[tap_stream_id] += 1

    with metrics.job_timer('sync_table') as timer:
        timer.tags['database'] = database_name
        timer.tags['table'] = stream['table_name']

        collection = client[database_name][stream["table_name"]]

        if replication_method == 'FULL_TABLE':
            full_table.sync_collection(collection, stream, state)
        else:
            incremental.sync_collection(collection, stream, state)

    state = singer.set_currently_syncing(state, None)

    singer.write_message(singer.StateMessage(value=copy.deepcopy(state)))


def sync_traditional_streams(client: MongoClient, traditional_streams: List[Dict], state: Dict):
    """
    Sync traditional streams that use either FULL_TABLE or INCREMENTAL one stream at a time.
    Args:
        client: MongoDB client instance
        traditional_streams: list of streams to sync
        state: state dictionary
    """
    for stream in traditional_streams:
        sync_traditional_stream(client, stream, state)


def sync_log_based_streams(client: MongoClient,
                           log_based_streams: List[Dict],
                           database_name: str,
                           state: Dict,
                           update_buffer_size: Optional[int],
                           await_time_ms: Optional[int]
                           ):
    """
    Sync log_based streams all at once by listening on the database-level change streams events.
    Args:
        client: MongoDB client instance
        log_based_streams:  list of streams to sync
        database_name: name of the database to sync from
        state: state dictionary
        update_buffer_size: the size of buffer used to hold detected updates
        await_time_ms:  the maximum time in milliseconds for the log based to wait for changes before exiting
    """
    if not log_based_streams:
        return

    streams = streams_list_to_dict(log_based_streams)

    for tap_stream_id, stream in streams.items():
        common.COUNTS[tap_stream_id] = 0
        common.TIMES[tap_stream_id] = 0
        common.SCHEMA_COUNT[tap_stream_id] = 0
        common.SCHEMA_TIMES[tap_stream_id] = 0

        state = clear_state_on_replication_change(stream, state)
        singer.write_message(singer.StateMessage(value=copy.deepcopy(state)))

        write_schema_message(stream)
        common.SCHEMA_COUNT[tap_stream_id] += 1

    with metrics.job_timer('sync_table') as timer:
        timer.tags['database'] = database_name
        update_buffer_size = update_buffer_size or change_streams.MIN_UPDATE_BUFFER_LENGTH
        await_time_ms = await_time_ms or change_streams.DEFAULT_AWAIT_TIME_MS

        change_streams.sync_database(client[database_name], streams, state, update_buffer_size, await_time_ms)

    state = singer.set_currently_syncing(state, None)
    singer.write_message(singer.StateMessage(value=copy.deepcopy(state)))


def do_sync(client: MongoClient, catalog: Dict, config: Dict, state: Dict):
    """
    Syncs all the selected streams in the catalog
    Args:
        client: MongoDb client instance
        catalog: dictionary with all the streams details
        config: config dictionary
        state: state
    """
    validate_config(config)

    all_streams = catalog['streams']
    streams_to_sync = get_streams_to_sync(all_streams, state)

    log_based_streams, traditional_streams = filter_streams_by_replication_method(streams_to_sync)

    LOGGER.debug('Starting sync of traditional streams ...')
    sync_traditional_streams(client, traditional_streams, state)
    LOGGER.debug('Sync of traditional streams done')

    LOGGER.debug('Starting sync of log based streams ...')
    sync_log_based_streams(client,
                           log_based_streams,
                           config['database'],
                           state,
                           config.get('update_buffer_size'),
                           config.get('await_time_ms')
                           )
    LOGGER.debug('Sync of log based streams done')

    LOGGER.info(common.get_sync_summary(catalog))


def get_connection_string(config: Dict):
    """
    Generates a MongoClientConnectionString based on configuration
    Args:
        config: DB config

    Returns: A MongoClient connection string
    """
    srv = config.get('srv') == 'true'

    # Default SSL verify mode to true, give option to disable
    verify_mode = config.get('verify_mode', 'true') == 'true'
    use_ssl = config.get('ssl') == 'true'

    connection_query = {
        'readPreference': 'secondaryPreferred',
        'authSource': config['auth_database'],
    }

    if config.get('replica_set'):
        connection_query['replicaSet'] = config['replica_set']

    if use_ssl:
        connection_query['tls'] = 'true'

    # NB: "sslAllowInvalidCertificates" must ONLY be supplied if `SSL` is true.
    if not verify_mode and use_ssl:
        connection_query['tlsAllowInvalidCertificates'] = 'true'

    query_string = parse.urlencode(connection_query)

    port = "" if srv else f":{int(config['port'])}"

    connection_string = f'{"mongodb+srv" if srv else "mongodb"}://{config["user"]}:' \
                        f'{config["password"]}@{config["host"]}' \
                        f'{port}/{config["database"]}?{query_string}'

    return connection_string


def main_impl():
    """
    Main function
    """
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    config = args.config
    srv = config.get('srv') == 'true'

    if not srv:
        args = utils.parse_args(REQUIRED_CONFIG_KEYS_NON_SRV)
        config = args.config

    connection_string = get_connection_string(config)
    client = MongoClient(connection_string)

    LOGGER.info('Connected to MongoDB host: %s, version: %s',
                config['host'],
                client.server_info().get('version', 'unknown'))

    common.INCLUDE_SCHEMAS_IN_DESTINATION_STREAM_NAME = \
        (config.get('include_schemas_in_destination_stream_name') == 'true')

    if args.discover:
        do_discover(client, config)
    elif args.catalog:
        state = args.state or {}
        do_sync(client, args.catalog.to_dict(), config, state)


class MongoSourceConnector(C8Connector):
    """MongoSourceConnector's C8Connector impl."""

    def name(self) -> str:
        """Returns the name of the connector."""
        return "mongo"

    def package_name(self) -> str:
        """Returns the package name of the connector (i.e. PyPi package name)."""
        return "macrometa-source-mongo"

    def version(self) -> str:
        """Returns the version of the connector."""
        return pkg_resources.get_distribution('macrometa_source_mongo').version

    def type(self) -> str:
        """Returns the type of the connector."""
        return "source"

    def description(self) -> str:
        """Returns the description of the connector."""
        return "GDN data connector source for Mongo"

    def validate(self, integration: dict) -> None:
        """Validate given configurations against the connector.
        If invalid, throw an exception with the cause.
        """
        config = self.get_config(integration)
        client = self.get_client(config)
        do_discover(client, config)

    def samples(self, integration: dict) -> list[Sample]:
        """Fetch sample data using the provided configurations."""
        config = self.get_config(integration)
        client = self.get_client(config)
        streams = do_discover(client, config)
        results = []
        for stream in streams:
            schema, data = fetch_samples(client, config, stream)[:10]
            results.append(Sample(
                schema=Schema(stream["table_name"],
                              [SchemaAttribute(k, get_attribute_type(v)) for k, v in schema.items()]),
                data=data
            ))
        return results

    def schemas(self, integration: dict) -> list[Schema]:
        """Get supported schemas using the given configurations."""
        config = self.get_config(integration)
        client = self.get_client(config)
        streams = do_discover(client, config)
        results = []
        for stream in streams:
            schema, _ = fetch_samples(client, config, stream)[:10]
            results.append(Schema(stream["table_name"],
                                  [SchemaAttribute(k, get_attribute_type(v)) for k, v in schema.items()]))
        return results

    def config(self) -> list[ConfigProperty]:
        """Get configuration parameters for the connector."""
        return [
            ConfigProperty('host', ConfigAttributeType.STRING, True, False,
                           description='MongoDB host',
                           example='51.25.44.24'),
            ConfigProperty('port', ConfigAttributeType.INT, True, False,
                           description='MongoDB port',
                           example='27017'),
            ConfigProperty('user', ConfigAttributeType.STRING, True, False,
                           description='MongoDB user',
                           example='mongo'),
            ConfigProperty('password', ConfigAttributeType.STRING, True, False,
                           description='MongoDB password',
                           example='password'),
            ConfigProperty('auth_database', ConfigAttributeType.STRING, True, False,
                           description='MongoDB authentication database',
                           example='auth_database'),
            ConfigProperty('source_collection', ConfigAttributeType.STRING, True, True,
                           description="Source collection name", example="SampleCollection"),
            ConfigProperty('database', ConfigAttributeType.STRING, True, False,
                           description='MongoDB database name',
                           example='mongo'),
            ConfigProperty('srv', ConfigAttributeType.BOOLEAN, False, False,
                           description='Uses a `mongodb+srv` protocol to connect. Disables the usage of `port` '
                                       'argument if set to `True`',
                           example='true'),
            ConfigProperty('replica_set', ConfigAttributeType.STRING, False, False,
                           description='Name of replica set',
                           example='replica'),
            ConfigProperty('ssl', ConfigAttributeType.BOOLEAN, False, False,
                           description='can be set to true to connect using ssl',
                           example='false'),
            ConfigProperty('verify_mode', ConfigAttributeType.BOOLEAN, False, False,
                           description='Default SSL verify mode',
                           example='true'),
            ConfigProperty('include_schemas_in_destination_stream_name', ConfigAttributeType.BOOLEAN, False, False,
                           description='forces the stream names to take the form `<database_name>-<collection_name>` '
                                       'instead of `<collection_name>`',
                           example='false'),
            ConfigProperty('update_buffer_size', ConfigAttributeType.INT, False, False,
                           description='[LOG_BASED] The size of the buffer that holds detected update operations in '
                                       'memory, the buffer is flushed once the size is reached',
                           example='1'),
            ConfigProperty('await_time_ms', ConfigAttributeType.INT, False, False,
                           description='[LOG_BASED] The maximum amount of time in milliseconds the loge_base method '
                                       'waits for new data changes before exiting',
                           example='1000'),
        ]

    def capabilities(self) -> list[str]:
        """Return the capabilities[1] of the connector.
        [1] https://docs.meltano.com/contribute/plugins#how-to-test-a-tap
        """
        return ['catalog', 'discover', 'state']

    @staticmethod
    def get_config(integration: dict) -> dict:
        try:
            return {
                # Required config keys
                'host': integration['host'],
                'user': integration['user'],
                'password': integration['password'],
                'port': integration['port'],
                'database': integration['database'],
                'auth_database': integration['auth_database'],
                'source_collection': integration['source_collection'],
                # Optional config keys
                'srv': integration.get('srv'),
                'replica_set': integration.get('replica_set'),
                'ssl': integration.get('ssl', False),
                'verify_mode': integration.get('verify_mode', True),
                'include_schemas_in_destination_stream_name': integration.get(
                    'include_schemas_in_destination_stream_name', False),
                'update_buffer_size': float(integration.get('update_buffer_size', 1)),
                'await_time_ms': integration.get('await_time_ms', 1000),
            }
        except KeyError as e:
            raise KeyError(f'Integration property `{e}` not found.')

    @staticmethod
    def get_client(config: Dict) -> MongoClient:
        connection_string = get_connection_string(config)
        client = MongoClient(connection_string)
        LOGGER.info('Connected to MongoDB host: %s, version: %s',
                    config['host'],
                    client.server_info().get('version', 'unknown'))
        return client


def main():
    """
    Main
    """
    try:
        main_impl()
    except Exception as exc:
        LOGGER.exception(exc)
        raise exc
