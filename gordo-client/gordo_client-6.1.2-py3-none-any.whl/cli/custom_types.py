"""Custom click types."""
import os
import typing

import click
import yaml
from dateutil import parser
from gordo_core.data_providers.base import GordoBaseDataProvider
from gordo_core.exceptions import ConfigException


class DataProviderParam(click.ParamType):
    """Load a DataProvider from JSON/YAML representation or from a JSON/YAML file."""

    name = "data-provider"

    def convert(self, value, param, ctx):
        """Convert the value for data provider."""
        if os.path.isfile(value):
            with open(value) as f:
                config = yaml.safe_load(f)
        else:
            config = yaml.safe_load(value)

        try:
            provider = GordoBaseDataProvider.from_dict(config)
        except ConfigException as e:
            self.fail(str(e))
        return provider


class IsoFormatDateTime(click.ParamType):
    """Parse a string into an ISO formatted datetime object."""

    name = "iso-datetime"

    def convert(self, value, param, ctx):
        """Convert the value for iso date."""
        try:
            return parser.isoparse(value)
        except ValueError:
            self.fail(f"Failed to parse date '{value}' as ISO formatted date'")


def key_value_par(val) -> typing.Tuple[str, str]:
    """Split input of 'key,val'."""
    return val.split(",")
