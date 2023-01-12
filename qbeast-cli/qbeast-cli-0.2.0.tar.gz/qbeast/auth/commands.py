import click
import getpass
from qbeast.predefs import qbeast_config_path, profile_filename
from qbeast.auth.auth import login_with_password
from qbeast.config import update_bearer_token, create_profile


@click.command("login")
def login():
    """Authenticate using the email and password"""
    print("Please enter your Qbeast Studio credentials")
    username = input("Username (e-mail): ")
    password = getpass.getpass("Password: ")
    success, reply = login_with_password(username, password)
    if not success:
        print(f"Login not valid")
        exit(1)
    update_bearer_token(reply["token"])
    create_profile()
    print("You can use the Sharing profile " + qbeast_config_path + '/' + profile_filename)
    return success, reply
