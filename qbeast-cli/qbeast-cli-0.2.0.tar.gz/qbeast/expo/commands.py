import click
from qbeast.expo.expo import get_share, create_share_and_schema, create_invite, add_table

# Qbeast Sharing API version definition
__version__ = "0.1.0"


@click.group()
def expo():
    """qbeast expo commands"""
    pass


@expo.command("create")
@click.argument("share_name")
@click.argument("table_name")
@click.argument("location")
@click.argument("account_id")
def register_dataset(share_name, table_name, location, account_id):
    """Add a table to the share, creates the share if not exists"""
    success, reply = get_share(share_name)

    if not reply.get("name"):
        print("Share not found, creating...")
        success, reply = create_share_and_schema(share_name)

    share_name = reply.get("name")

    success, reply = add_table(share_name, table_name, location, account_id)

    return success, reply


@expo.command("invite")
@click.argument("share_name")
@click.argument("invitee_email")
@click.argument("invitee_name", default='')
def invite(share_name, invitee_email, invitee_name):
    """Invite a user to a share"""
    success, reply = create_invite(share_name, invitee_email, invitee_name)

    return success, reply
