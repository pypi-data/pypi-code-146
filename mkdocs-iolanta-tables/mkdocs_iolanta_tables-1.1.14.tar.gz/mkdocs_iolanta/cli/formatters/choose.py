from typing import Optional

from classes import typeclass
from rdflib import Graph

from ldflex.ldflex import QueryResult, SelectResult
from mkdocs_iolanta.cli.formatters.csv import csv_print
from mkdocs_iolanta.cli.formatters.json import print_json
from mkdocs_iolanta.cli.formatters.node_to_qname import node_to_qname
from mkdocs_iolanta.cli.formatters.pretty import pretty_print
from mkdocs_iolanta.types import QueryResultsFormat

# @typeclass
# def cli_print(
#     query_result: QueryResult,
#     output_format: QueryResultsFormat,
#     display_iri_as_qname: bool = True,
#     graph: Optional[Graph] = None,
# ):
#     """Print the datum using proper formatter with options."""


# @cli_print.instance(SelectResult)
def cli_print(
    query_result: SelectResult,
    output_format: QueryResultsFormat,
    display_iri_as_qname: bool = True,
    graph: Optional[Graph] = None,
):
    if display_iri_as_qname:
        if graph is None:
            raise NotImplementedError(
                'Cannot compute QNames if graph is not provided.',
            )

        query_result = SelectResult([
            {
                key: node_to_qname(node, graph)
                for key, node in row.items()
            }
            for row in query_result
        ])

    {
        QueryResultsFormat.CSV: csv_print,
        QueryResultsFormat.PRETTY: pretty_print,
        QueryResultsFormat.JSON: print_json,
    }[output_format](query_result)   # type: ignore
