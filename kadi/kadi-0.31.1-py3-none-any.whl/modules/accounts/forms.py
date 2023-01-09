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
from flask import current_app
from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length
from wtforms.validators import Optional
from wtforms.validators import ValidationError

from .models import LocalIdentity
from .providers.shib import ShibProvider
from kadi.lib.conversion import lower
from kadi.lib.conversion import normalize
from kadi.lib.conversion import strip
from kadi.lib.forms import BooleanField
from kadi.lib.forms import KadiForm
from kadi.lib.forms import PasswordField
from kadi.lib.forms import SelectField
from kadi.lib.forms import StringField
from kadi.lib.forms import SubmitField
from kadi.lib.forms import validate_username as _validate_username


def get_login_form(provider):
    """Get a login form based on a given authentication provider.

    All fields and labels will have the given provider's type appended to their IDs in
    the form of ``"<field_id>_<provider>"``, so rendering multiple forms on a single
    page does not lead to issues because of duplicate IDs.

    :param provider: An authentication provider as specificed in
        :const:`kadi.lib.constants.AUTH_PROVIDER_TYPES`.
    :return: The login form.
    """
    form = None
    providers = current_app.config["AUTH_PROVIDERS"]

    if provider in providers:
        form = providers[provider]["form_class"](suffix=provider)
        # Save the provider on the form so it can easily be referenced later on.
        form._provider = provider

    return form


class CredentialsLoginForm(KadiForm):
    """A general login form using a username and a password."""

    username = StringField(
        _l("Username"), filters=[lower, strip], validators=[DataRequired()]
    )

    password = PasswordField(_l("Password"), validators=[DataRequired()])

    submit = SubmitField(_l("Login"))


class ShibLoginForm(KadiForm):
    """A login form for use in Shibboleth.

    The form uses a selection field which has to be populated with the entity IDs and
    display names of all valid identity providers.
    """

    idp = SelectField(
        _l("Institution"),
        choices=ShibProvider.get_choices,
        validators=[DataRequired()],
    )

    submit = SubmitField(_l("Login"))


class NewUserForm(KadiForm):
    """A form for use in creating new local users."""

    username = StringField(
        _l("Username"),
        filters=[lower, strip],
        validators=[
            DataRequired(),
            Length(
                min=LocalIdentity.Meta.check_constraints["username"]["length"]["min"],
                max=LocalIdentity.Meta.check_constraints["username"]["length"]["max"],
            ),
            _validate_username,
        ],
        description=(
            _l(
                "Allowed are alphanumeric characters with single hyphens or underscores"
                " in between."
            )
        ),
    )

    displayname = StringField(
        _l("Display name"),
        filters=[normalize],
        validators=[
            DataRequired(),
            Length(
                max=LocalIdentity.Meta.check_constraints["displayname"]["length"]["max"]
            ),
        ],
    )

    email = StringField(
        _l("Email"),
        filters=[strip],
        validators=[
            DataRequired(),
            Email(),
            Length(max=LocalIdentity.Meta.check_constraints["email"]["length"]["max"]),
        ],
    )

    submit = SubmitField(_l("Register"))

    def validate_username(self, username):
        # pylint: disable=missing-function-docstring
        identity = LocalIdentity.query.filter_by(username=username.data).first()

        if identity is not None:
            raise ValidationError(_("Username is already in use."))


class RegistrationForm(NewUserForm):
    """A form for use in registering new local users."""

    password = PasswordField(_l("Password"), validators=[DataRequired(), Length(min=8)])

    password2 = PasswordField(
        _l("Repeat password"),
        validators=[DataRequired(), EqualTo("password", _l("Passwords do not match."))],
    )

    accept_legals = BooleanField(validators=[DataRequired()])


class RequestPasswordResetForm(KadiForm):
    """A form for use in requesting a password reset for local users."""

    username = StringField(
        _l("Username"), filters=[lower, strip], validators=[DataRequired()]
    )

    submit = SubmitField(_l("Submit request"))


class ResetPasswordForm(KadiForm):
    """A form for use in changing a local user's password."""

    password = PasswordField(_l("Password"), validators=[DataRequired(), Length(min=8)])

    password2 = PasswordField(
        _l("Repeat password"),
        validators=[DataRequired(), EqualTo("password", _l("Passwords do not match."))],
    )

    submit = SubmitField(_l("Save new password"))


class EmailConfirmationForm(KadiForm):
    """A form for use in mandatory email confirmation for local users.

    Offers an optional email field to let a user change their current email address.
    """

    email = StringField(
        _l("Wrong email address? Enter your new email address here:"),
        filters=[strip],
        validators=[
            Optional(),
            Email(),
            Length(max=LocalIdentity.Meta.check_constraints["email"]["length"]["max"]),
        ],
    )

    submit = SubmitField(_l("Resend"))
