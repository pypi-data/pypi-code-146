"""Stream type classes for tap-exact."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_exact.client import ExactOnlineStream
from exactonline.resource import GET

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class SalesInvoicesStream(ExactOnlineStream):
    """Define custom stream."""

    name = "sales-invoices"
    path = "/salesinvoice/SalesInvoices?$select=InvoiceDate,InvoiceNumber,InvoiceTo,InvoiceToName,OrderDate,OrderedBy,OrderedByName,AmountDC,Modified"
    primary_keys = ["InvoiceID"]
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"
    schema = th.PropertiesList(
        th.Property("InvoiceID", th.StringType),
        th.Property(
            "InvoiceDate",
            th.DateTimeType,
            description="The invoice date"
        ),
        th.Property(
            "InvoiceNumber",
            th.IntegerType,
            description="The invoice number"
        ),
        th.Property(
            "InvoiceTo",
            th.StringType,
            description="The customer whom the invoice is made for"
        ),
        th.Property(
            "InvoiceToName",
            th.StringType,
            description="The name of the customer whom the invoice is made for"
        ),
        th.Property(
            "OrderDate",
            th.DateTimeType,
            description="The order date"
        ),
        th.Property(
            "OrderedBy",
            th.StringType,
            description="The customer who made the order"
        ),
        th.Property(
            "OrderedByName",
            th.StringType,
            description="The name of the customer who made the order"
        ),
        th.Property(
            "AmountDC",
            th.NumberType,
            description="Amount in the default currency of the company"
        ),
        th.Property(
            "Modified",
            th.DateTimeType,
            description="Last modified date"
        ),
    ).to_dict()

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Return a generator or row-type dictionary objects"""
        
        resp = self.conn.rest(GET('v1/%d/%s' % (self.division, self.path)))
        
        for row in resp:
            yield row