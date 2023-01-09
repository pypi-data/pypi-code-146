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
from datetime import timedelta

from flask import current_app
from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from flask_login import current_user
from marshmallow import fields
from marshmallow import ValidationError
from marshmallow.validate import OneOf
from marshmallow.validate import Range
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length
from wtforms.validators import Optional

import kadi.lib.constants as const
from kadi.lib.api.models import AccessToken
from kadi.lib.conversion import empty_str
from kadi.lib.conversion import normalize
from kadi.lib.conversion import strip
from kadi.lib.forms import BaseConfigForm
from kadi.lib.forms import BooleanField
from kadi.lib.forms import FileField
from kadi.lib.forms import JSONField
from kadi.lib.forms import KadiForm
from kadi.lib.forms import LFTextAreaField
from kadi.lib.forms import PasswordField
from kadi.lib.forms import StringField
from kadi.lib.forms import SubmitField
from kadi.lib.forms import UTCDateTimeField
from kadi.lib.schemas import KadiSchema
from kadi.lib.utils import utcnow
from kadi.modules.accounts.models import LocalIdentity
from kadi.modules.accounts.models import User


class EditProfileForm(KadiForm):
    """A form for use in editing a user's profile information.

    :param user: The user to prepopulate the fields with.
    """

    displayname = StringField(
        _l("Display name"), filters=[normalize], validators=[DataRequired()]
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

    show_email = BooleanField(_l("Show email address on profile"))

    about = LFTextAreaField(
        _l("About"),
        filters=[empty_str],
        validators=[Length(max=User.Meta.check_constraints["about"]["length"]["max"])],
    )

    image = FileField(_l("Profile picture"))

    remove_image = BooleanField(_l("Remove current profile picture"))

    submit = SubmitField(_l("Save changes"))

    def __init__(self, user, *args, **kwargs):
        data = {
            "displayname": user.identity.displayname,
            "email": user.identity.email,
            "show_email": not user.email_is_private,
            "about": user.about,
        }

        super().__init__(*args, data=data, **kwargs)

        if user.identity.type != const.AUTH_PROVIDER_TYPE_LOCAL:
            self.email.description = _(
                "Automatically set based on your %(type)s account.",
                type=user.identity.Meta.identity_type["name"],
            )

        self.displayname.validators.append(
            Length(
                max=current_app.config["AUTH_PROVIDERS"][user.identity.type][
                    "identity_class"
                ].Meta.check_constraints["displayname"]["length"]["max"]
            )
        )


class ChangePasswordForm(KadiForm):
    """A form for use in changing a local user's password."""

    password = PasswordField(_l("Current password"), validators=[DataRequired()])

    new_password = PasswordField(
        _l("New password"), validators=[DataRequired(), Length(min=8)]
    )

    new_password2 = PasswordField(
        _l("Repeat new password"),
        validators=[
            DataRequired(),
            EqualTo("new_password", _l("Passwords do not match.")),
        ],
    )

    submit = SubmitField(_l("Save changes"))


class _HomeLayoutSchema(KadiSchema):
    resource = fields.String(
        required=True, validate=OneOf(["record", "collection", "template", "group"])
    )

    visibility = fields.String(
        required=True,
        validate=OneOf(
            ["all", const.MODEL_VISIBILITY_PRIVATE, const.MODEL_VISIBILITY_PUBLIC]
        ),
    )

    creator = fields.String(required=True, validate=OneOf(["any", "self"]))

    max_items = fields.Integer(required=True, validate=Range(min=0, max=10))


class HomeLayoutField(JSONField):
    """Custom field to process and validate preferences for the home page layout."""

    def __init__(self, *args, **kwargs):
        kwargs["default"] = const.USER_CONFIG_HOME_LAYOUT_DEFAULT
        super().__init__(*args, **kwargs)

    def process_formdata(self, valuelist):
        super().process_formdata(valuelist)

        if valuelist:
            try:
                schema = _HomeLayoutSchema(many=True)
                self.data = schema.load(self.data)

            except ValidationError as e:
                self.data = self.default
                raise ValueError("Invalid data structure.") from e


class CustomizationPreferencesForm(BaseConfigForm):
    """A form for use in setting user-specific config items related to customization.

    :param user: (optional) The user to pass to :class:`.BaseConfigForm`. Defaults to
        the current user.
    """

    hide_introduction = BooleanField(
        _l("Hide introduction"),
        description=_l('Hide the "Get started" section on the home page.'),
    )

    home_layout = HomeLayoutField(
        _l("Home page layout"),
        description=_l(
            'Resource types to be shown on the home page in the "Latest Updates"'
            " section with corresponding filters. Note that only groups with membership"
            " are shown."
        ),
    )

    def __init__(self, *args, user=None, **kwargs):
        user = user if user is not None else current_user
        super().__init__(*args, user=user, **kwargs)


class NewAccessTokenForm(KadiForm):
    """A form for use in creating new access tokens."""

    name = StringField(
        _l("Name"),
        filters=[normalize],
        validators=[
            DataRequired(),
            Length(max=AccessToken.Meta.check_constraints["name"]["length"]["max"]),
        ],
    )

    expires_at = UTCDateTimeField(
        _l("Expires at"),
        validators=[Optional()],
        description=_l("The default expiration date is %(num)d weeks.", num=4),
        default=lambda: utcnow() + timedelta(days=28),
    )

    submit = SubmitField(_l("Create token"))
