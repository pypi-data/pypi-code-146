import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
)

import click

from truera.client.private import metarepo as mr
from truera.utils.check_permission_helper import MOCK_REQUEST_CONTEXT

# This CLI is meant for the dev / onebox scenario to facilitate performing operations on metarepo that
# are common but not necessarily something needed in prod / supportable.
#
# > python truera/utils/metarepo_manipulation.py clean-table cannedreports
#
# Tables are all listed in metarepo.py.


@click.group()
def metarepo_manipulation_cli():
    pass


@metarepo_manipulation_cli.command()
@click.argument("table")
@click.option(
    "--connection_string",
    help="Connection string to truera endpoint.",
    default="http://localhost:9290"
)
def clean_table(table, connection_string):
    with mr.MetaRepo(connection_string) as metarepo:
        table_entries = metarepo.get_entities(
            request_ctx=MOCK_REQUEST_CONTEXT, entity=table
        )

        for entry in table_entries:
            entry_id = entry["id"]
            name = entry.get("name", None)
            print(f"Deleting entity with id {entry_id} and name {name}.")
            metarepo.del_entity(
                request_ctx=MOCK_REQUEST_CONTEXT,
                entity=table,
                entity_id=entry_id
            )

    print("Done")


if __name__ == '__main__':
    metarepo_manipulation_cli()
