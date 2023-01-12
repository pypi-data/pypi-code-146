"""GDN data connector target for Macrometa GDN collections."""
import pkg_resources
from c8connector import C8Connector, Sample, ConfigAttributeType, Schema
from c8connector import ConfigProperty


class GDNCollectionTargetConnector(C8Connector):
    """GDNCollectionTargetConnector's C8Connector impl."""

    def name(self) -> str:
        """Returns the name of the connector."""
        return "collection"

    def package_name(self) -> str:
        """Returns the package name of the connector (i.e. PyPi package name)."""
        return "macrometa-target-collection"

    def version(self) -> str:
        """Returns the version of the connector."""
        return pkg_resources.get_distribution('macrometa_target_collection').version

    def type(self) -> str:
        """Returns the type of the connector."""
        return "target"

    def description(self) -> str:
        """Returns the description of the connector."""
        return "Data connector source for GDN Collections"

    def validate(self, integration: dict) -> None:
        """Validate given configurations against the connector.
        If invalid, throw an exception with the cause.
        """
        pass

    def samples(self, integration: dict) -> list[Sample]:
        """Fetch sample data using the given configurations."""
        return []

    def schemas(self, integration: dict) -> list[Schema]:
        """Get supported schemas using the given configurations."""
        return []

    def config(self) -> list[ConfigProperty]:
        """Get configuration parameters for the connector."""
        return [
            ConfigProperty('region', 'Region URL', ConfigAttributeType.STRING, True, False,
                           description="Fully qualified region URL.",
                           placeholder_value='api-sample-ap-west.eng.macrometa.io'),
            ConfigProperty('api_key', 'API Key', ConfigAttributeType.STRING, True, False,
                           description="API key.",
                           placeholder_value='my_apikey'),
            ConfigProperty('fabric', 'Fabric', ConfigAttributeType.STRING, True, False,
                           description="Fabric name.",
                           default_value='_system'),
            ConfigProperty('target_collection', 'Target Collection', ConfigAttributeType.STRING, True, True,
                           description="Target collection name.",
                           placeholder_value='my_collection'),
            ConfigProperty('batch_size_rows', 'Batch Size', ConfigAttributeType.INT, False, False,
                           description='Maximum number of rows inserted per batch.',
                           default_value='50'),
            ConfigProperty('batch_flush_interval', 'Batch Flush Interval (Seconds)',
                           ConfigAttributeType.INT, False, False,
                           description='Time between batch flush executions.',
                           default_value='60'),
            ConfigProperty('batch_flush_min_time_gap', 'Batch Flush Minimum Time Gap (Seconds)',
                           ConfigAttributeType.INT, False, False,
                           description='Minimum time gap between two batch flush tasks.',
                           default_value='60'),
        ]

    def capabilities(self) -> list[str]:
        """Return the capabilities[1] of the connector.
        [1] https://docs.meltano.com/contribute/plugins#how-to-test-a-tap
        """
        return []
