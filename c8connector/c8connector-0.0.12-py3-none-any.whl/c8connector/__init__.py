#  Copyright (c) 2022 Macrometa Corp All rights reserved.
from enum import Enum


class ConfigAttributeType(Enum):
    """C8Connector ConfigAttributeType"""
    STRING = "string"
    INT = "integer"
    BOOLEAN = "boolean"
    DATE = "date_iso8601"
    EMAIL = "email"
    PASSWORD = "password"
    OAUTH = "oauth"
    OPTIONS = "options"
    FILE = "file"
    ARRAY = "array"
    OBJECT = "object"
    HIDDEN = "hidden"


class SchemaAttributeType(Enum):
    """C8Connector SchemaAttributeType"""
    BOOLEAN = "bool"
    INT = "int"
    LONG = "long"
    FLOAT = "float"
    DOUBLE = "double"
    STRING = "string"
    OBJECT = "object"


class ConfigProperty:
    """C8Connector config property"""

    def __init__(self, name: str, display_name: str, type: ConfigAttributeType, is_mandatory: bool,
                 is_dynamic: bool, description: str, default_value: str = '', placeholder_value: str = ''):
        """
        Parameters
        :param name: Name of the config property
        :param display_name: Display name of the config property
        :param type: Attribute type of the config property
        :param is_mandatory: Boolean indicating whether the property is mandatory
        :param is_dynamic: Boolean indicating whether the property is dynamic
        :param description: Description of the config property
        :param default_value: Default value of the property
        :param placeholder_value: Placeholder value of the property
        """
        self.name = name
        self.type = type
        self.display_name = display_name
        self.is_mandatory = is_mandatory
        self.is_dynamic = is_dynamic
        self.description = description
        self.default_value = default_value
        self.placeholder_value = placeholder_value


class SchemaAttribute:
    """C8Connector Attribute"""

    def __init__(self, name: str, type: SchemaAttributeType):
        self.name = name
        self.type = type


class Schema:
    """C8Connector Schema"""

    def __init__(self, name: str, attributes: list[SchemaAttribute]):
        self.name = name
        self.attributes = attributes


class Sample:
    """C8Connector Sample"""

    def __init__(self, schema: Schema, data: list[dict]):
        self.schema = schema
        self.data = data


class C8ConnectorMeta(type):
    """C8Connector metaclass"""

    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return (
                hasattr(subclass, 'name') and callable(subclass.name) and
                hasattr(subclass, 'package_name') and callable(subclass.package_name) and
                hasattr(subclass, 'version') and callable(subclass.version) and
                hasattr(subclass, 'type') and callable(subclass.type) and
                hasattr(subclass, 'description') and callable(subclass.description) and
                hasattr(subclass, 'validate') and callable(subclass.validate) and
                hasattr(subclass, 'samples') and callable(subclass.samples) and
                hasattr(subclass, 'schemas') and callable(subclass.schemas) and
                hasattr(subclass, 'config') and callable(subclass.config) and
                hasattr(subclass, 'capabilities') and callable(subclass.capabilities)
        )


class C8Connector(metaclass=C8ConnectorMeta):
    """C8Connector superclass"""

    def name(self) -> str:
        """Returns the name of the connector."""
        pass

    def package_name(self) -> str:
        """Returns the package name of the connector (i.e. PyPi package name)."""
        pass

    def version(self) -> str:
        """Returns the version of the connector."""
        pass

    def type(self) -> str:
        """Returns the type of the connector."""
        pass

    def description(self) -> str:
        """Returns the description of the connector."""
        pass

    def validate(self, integration: dict) -> None:
        """Validate given configurations against the connector.
        If invalid, throw an exception with the cause.
        """
        pass

    def samples(self, integration: dict) -> list[Sample]:
        """Fetch sample data using the given configurations."""
        pass

    def schemas(self, integration: dict) -> list[Schema]:
        """Get supported schemas using the given configurations."""
        pass

    def config(self) -> list[ConfigProperty]:
        """Get configuration parameters for the connector."""
        pass

    def capabilities(self) -> list[str]:
        """Return the capabilities[1] of the connector.
        [1] https://docs.meltano.com/contribute/plugins#how-to-test-a-tap
        """
        pass
