"""GDN data connector source for GDN Collections."""
from collections import Counter

import pkg_resources
import singer
from c8 import C8Client
from c8connector import C8Connector, Sample, ConfigProperty, ConfigAttributeType, Schema, SchemaAttributeType, \
    SchemaAttribute
from macrometa_source_collection.client import GDNCollectionClient
from singer import utils
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema as SingerSchema

LOGGER = singer.get_logger('macrometa_source_collection')

REQUIRED_CONFIG_KEYS = [
    'region',
    'fabric',
    'api_key',
    'source_collection'
]


class GDNCollectionSourceConnector(C8Connector):
    """GDNCollectionSourceConnector's C8Connector impl."""

    def name(self) -> str:
        """Returns the name of the connector."""
        return "collection"

    def package_name(self) -> str:
        """Returns the package name of the connector (i.e. PyPi package name)."""
        return "macrometa-source-collection"

    def version(self) -> str:
        """Returns the version of the connector."""
        return pkg_resources.get_distribution('macrometa_source_collection').version

    def type(self) -> str:
        """Returns the type of the connector."""
        return "source"

    def description(self) -> str:
        """Returns the description of the connector."""
        return "Data connector source for GDN Collections"

    def validate(self, integration: dict) -> None:
        """Validate given configurations against the connector.
        If invalid, throw an exception with the cause.
        """
        config = self.get_config(integration)
        C8Client(
            "https",
            host=config["region"],
            port=443,
            geofabric=config["fabric"],
            apikey=config["api_key"]
        ).collection(config["source_collection"])
        pass

    def samples(self, integration: dict) -> list[Sample]:
        """Fetch sample data using the given configurations."""
        config = self.get_config(integration)
        schema, data = get_schema_and_data(C8Client(
            "https",
            host=config["region"],
            port=443,
            geofabric=config["fabric"],
            apikey=config["api_key"]
        ), config["source_collection"], 10)
        return [Sample(
            schema=Schema(config["source_collection"],
                          [SchemaAttribute(k, get_attribute_type(v)) for k, v in schema.items()]),
            data=data
        )]

    def schemas(self, integration: dict) -> list[Schema]:
        """Get supported schemas using the given configurations."""
        config = self.get_config(integration)
        schema, _ = get_schema_and_data(C8Client(
            "https",
            host=config["region"],
            port=443,
            geofabric=config["fabric"],
            apikey=config["api_key"]
        ), config["source_collection"], 50)
        return [Schema(config["source_collection"],
                       [SchemaAttribute(k, get_attribute_type(v)) for k, v in schema.items()])]

    def config(self) -> list[ConfigProperty]:
        """Get configuration parameters for the connector."""
        return [
            ConfigProperty('region', 'Region URL', ConfigAttributeType.STRING, True, False,
                           description='Fully qualified region URL.',
                           placeholder_value='api-sample-ap-west.eng.macrometa.io'),
            ConfigProperty('fabric', 'Fabric', ConfigAttributeType.STRING, True, False,
                           description='Fabric name.',
                           default_value='_system'),
            ConfigProperty('api_key', 'API Key', ConfigAttributeType.STRING, True, False,
                           description='API key.',
                           placeholder_value='my_apikey'),
            ConfigProperty('source_collection', 'Source Collection', ConfigAttributeType.STRING, True, True,
                           description='Source collection name.',
                           placeholder_value='my_collection')
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
                'region': integration['region'],
                'api_key': integration['api_key'],
                'fabric': integration['fabric'],
                'source_collection': integration['source_collection']
            }
        except KeyError as e:
            raise KeyError(f'Integration property `{e}` not found.')


def get_schema_and_data(client: C8Client, collection: str, sample_size: int):
    cursor = client.execute_query(f"FOR d IN @@collection LIMIT 0, @count RETURN d",
                                  bind_vars={"@collection": collection, "count": sample_size})
    schemas = []
    schema_map = {}
    data_map = {}
    while not cursor.empty():
        rec = cursor.next()
        h = str(hash(rec.keys().__str__()))
        schema_map[h] = rec.keys()
        schemas.append(h)
        if h in data_map:
            data_map[h].append(rec)
        else:
            data_map[h] = [rec]
    schema = {"data": "object"}
    data = []
    if len(schemas) > 0:
        most_common, _ = Counter(schemas).most_common(1)[0]
        schema_keys = schema_map[most_common]
        data = data_map[most_common]
        schema = {
            k: get_singer_data_type(data[0][k]) for k in schema_keys
        }
    return schema, data


def get_singer_data_type(val):
    if type(val) == str:
        return "string"
    elif type(val) == int:
        return "integer"
    elif type(val) == float:
        return "number"
    elif type(val) == bool:
        return "boolean"
    else:
        return "object"


def get_attribute_type(source_type: str) -> SchemaAttributeType:
    if source_type == 'string':
        return SchemaAttributeType.STRING
    elif source_type == 'integer':
        return SchemaAttributeType.LONG
    elif source_type == 'boolean':
        return SchemaAttributeType.BOOLEAN
    elif source_type == 'number':
        return SchemaAttributeType.DOUBLE
    else:
        return SchemaAttributeType.OBJECT


def do_discovery(config):
    collection_name = config['source_collection']
    schema, _ = get_schema_and_data(C8Client(
        "https",
        host=config["region"],
        port=443,
        geofabric=config["fabric"],
        apikey=config["api_key"]
    ), collection_name, 50)
    schema_properties = {k: SingerSchema(type=v, format=None) for k, v in schema.items()}
    # inject `_sdc_deleted_at` prop to the schema.
    schema_properties['_sdc_deleted_at'] = SingerSchema(type=['null', 'string'], format='date-time')
    singer_schema = SingerSchema(type='object', properties=schema_properties)
    catalog = Catalog([CatalogEntry(
        table=collection_name,
        stream=collection_name,
        tap_stream_id=collection_name,
        schema=singer_schema,
        key_properties=["_key"]
    )])
    dump_catalog(catalog)
    return catalog


def dump_catalog(catalog: Catalog):
    catalog.dump()


def do_sync(conn_config, catalog, default_replication_method):
    client = GDNCollectionClient(conn_config)
    client.sync(catalog.streams[0])


def main_impl():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    conn_config = {'api_key': args.config['api_key'],
                   'region': args.config['region'],
                   'fabric': args.config['fabric'],
                   'source_collection': args.config['source_collection']}

    if args.discover:
        do_discovery(conn_config)
    elif args.catalog:
        do_sync(conn_config, args.catalog, args.config.get('default_replication_method'))
    else:
        LOGGER.info("No properties were selected")
    return


def main():
    try:
        main_impl()
    except Exception as exc:
        LOGGER.critical(exc)
