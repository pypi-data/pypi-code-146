"""ExactOnline tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
# TODO: Import your custom stream types here:
from tap_exactonline.streams import (
    ExactOnlineStream,
    ContactsStream,
    InvoiceStream,
    InvoiceLineStream,
    AccountsStream,
    AddressesStream,
    PaymentsStream,
    ReceivablesStream,
    DocumentsStream,
    DocumentAttachementsStream,
    GLAccountsStream,
    GLClassificationsStream,
    TransactionLinesStream,
)
# TODO: Compile a list of custom stream types here
#       OR rewrite discover_streams() below with your custom logic.
STREAM_TYPES = [
    ContactsStream,
    InvoiceStream,
    InvoiceLineStream,
    AccountsStream,
    AddressesStream,
    PaymentsStream,
    ReceivablesStream,
    DocumentsStream,
    DocumentAttachementsStream,
    GLAccountsStream,
    GLClassificationsStream,
    TransactionLinesStream,
]


class TapExactOnline(Tap):
    """ExactOnline tap class."""
    name = "tap-exactonline"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "rest_url",
            th.StringType,
            default='https://start.exactonline.nl/api',
            required=True,
            description="The exact online API rest url"
        ),
        th.Property(
            "base_url",
            th.StringType,
            required=True,
            description="Your website redirect url"
        ),
        th.Property(
            "auth_url",
            th.StringType,
            default='https://start.exactonline.nl/api/oauth2/auth',
            required=True,
            description="The exact online API auth url"
        ),
        th.Property(
            "token_url",
            th.StringType,
            default='https://start.exactonline.nl/api/oauth2/token',
            required=True,
            description="The exact online API token url"
        ),
        th.Property(
            "client_id",
            th.UUIDType,
            required=True,
            description="The exact online client id"
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
            description="The exact online client secret"
        ),
        th.Property(
            "secret_id",
            th.StringType,
            required=True,
            description="The aws secret with the exact credentials"
        ),
        th.Property(
            "division",
            th.IntegerType,
            required=True,
            description="The exact online division"
        ),
        th.Property(
            "record_limit",
            th.IntegerType,
            required=False,
            description="The max number of records fetched"
        ),
        th.Property(
            "stream_maps",
            th.ObjectType(),
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
