# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys

import click

from kadi.cli.main import kadi
from kadi.cli.utils import echo
from kadi.cli.utils import echo_danger
from kadi.cli.utils import echo_success
from kadi.ext.db import db
from kadi.lib.security import random_alnum
from kadi.modules.accounts.forms import NewUserForm
from kadi.modules.accounts.models import User
from kadi.modules.accounts.providers import LocalProvider


@kadi.group()
def users():
    """Utility commands for managing users."""


def _print_validation_error(form, field):
    for error in form.errors.get(field, []):
        echo_danger(f"[{field.capitalize()}] {error}")


@users.command()
def create():
    """Create a new local user."""
    if not LocalProvider.is_registered():
        echo_danger("The local provider is not registered in the application.")
        sys.exit(1)

    username_field = "username"
    displayname_field = "displayname"
    email_field = "email"

    username = click.prompt(username_field.capitalize())
    displayname = click.prompt(displayname_field.capitalize(), default=username)
    email = click.prompt(email_field.capitalize())

    form = NewUserForm(
        meta={"csrf": False},
        data={
            username_field: username,
            displayname_field: displayname,
            email_field: email,
        },
    )

    if not form.validate():
        _print_validation_error(form, username_field)
        _print_validation_error(form, displayname_field)
        _print_validation_error(form, email_field)

        sys.exit(1)

    echo(f"\n{username_field.capitalize():12s}{form.username.data}")
    echo(f"{displayname_field.capitalize():12s}{form.displayname.data}")
    echo(f"{email_field.capitalize():12s}{form.email.data}")

    if click.confirm("Do you want to create this user?"):
        password = random_alnum()
        identity = LocalProvider.register(
            username=form.username.data,
            displayname=form.displayname.data,
            email=form.email.data,
            password=password,
        )

        if identity is not None:
            echo_success(f"User with ID {identity.user.id} created successfully.\n")
            echo(f"Initial user password: {password}")
        else:
            echo_danger("Error creating user.")


@users.command()
@click.argument("user_id", type=click.INT)
def sysadmin(user_id):
    """Toggle the sysadmin state of a user."""
    user = User.query.get(user_id)

    if user is None:
        echo_danger(f"No valid user found with ID {user_id}.")
        sys.exit(1)

    echo(f"Found user with ID {user_id} with the following identities:")
    for identity in user.identities:
        echo(f"  * {identity!r}")

    if user.is_sysadmin:
        prompt = "\nDo you want to remove this user as a system administrator?"
    else:
        prompt = "\nDo you want to set this user as a system administrator?"

    if click.confirm(prompt):
        user.is_sysadmin = not user.is_sysadmin
        db.session.commit()

        echo_success("User updated successfully.")
