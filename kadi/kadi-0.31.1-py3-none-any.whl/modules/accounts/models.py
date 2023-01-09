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
from flask_babel import lazy_gettext as _l
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

import kadi.lib.constants as const
from kadi.ext.db import db
from kadi.lib.config.core import get_user_config
from kadi.lib.config.core import MISSING
from kadi.lib.config.core import set_user_config
from kadi.lib.db import generate_check_constraints
from kadi.lib.db import SimpleTimestampMixin
from kadi.lib.db import UTCDateTime
from kadi.lib.security import decode_jwt
from kadi.lib.security import encode_jwt
from kadi.lib.utils import SimpleReprMixin
from kadi.lib.utils import StringEnum
from kadi.lib.utils import utcnow
from kadi.modules.sysadmin.utils import get_legals_modification_date
from kadi.modules.sysadmin.utils import legals_acceptance_required


class UserState(StringEnum):
    """String enum containing all possible state values for users."""

    __values__ = [const.MODEL_STATE_ACTIVE, "inactive", const.MODEL_STATE_DELETED]


class User(SimpleReprMixin, SimpleTimestampMixin, UserMixin, db.Model):
    """Model to represent users.

    In general, every resource that a user "owns" should be linked to this model. Each
    user can also potentially have multiple identities associated with it, all pointing
    to the same user.
    """

    class Meta:
        """Container to store meta class attributes."""

        representation = [
            "id",
            "new_user_id",
            "latest_identity_id",
            "is_sysadmin",
            "state",
        ]
        """See :class:`.SimpleReprMixin`."""

        timestamp_exclude = [
            "identities",
            "records",
            "record_links",
            "files",
            "temporary_files",
            "uploads",
            "collections",
            "templates",
            "groups",
            "favorites",
            "workflows",
            "revisions",
            "tasks",
            "notifications",
            "access_tokens",
            "oauth2_tokens",
            "config_items",
            "permissions",
            "roles",
        ]
        """See :class:`.SimpleTimestampMixin`."""

        check_constraints = {
            "about": {"length": {"max": 10_000}},
            "state": {"values": UserState.__values__},
        }
        """See :func:`kadi.lib.db.generate_check_constraints`."""

    __tablename__ = "user"

    __table_args__ = generate_check_constraints(Meta.check_constraints) + (
        # Defined here so Alembic can resolve the cyclic user/identity reference.
        db.ForeignKeyConstraint(
            ["latest_identity_id"], ["identity.id"], use_alter=True
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    """The ID of the user, auto incremented."""

    about = db.Column(db.Text, default="", nullable=False)
    """Additional personal information.

    Restricted to a maximum length of 10_000 characters.
    """

    image_name = db.Column(UUID(as_uuid=True), nullable=True)
    """The optional name/identifier of a user's profile image.

    This identifier is used to build the local file path where the actual image is
    stored.
    """

    email_is_private = db.Column(db.Boolean, default=True, nullable=False)
    """Flag indicating whether a user's email address is private.

    A private email is only visible to the user themselves, while a public one is
    visible to every logged-in user.
    """

    new_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    """Points to a new user ID when the user was merged with another one."""

    latest_identity_id = db.Column(db.Integer, nullable=True)
    """Points to the ID of the latest identity the user logged in with."""

    is_sysadmin = db.Column(db.Boolean, default=False, nullable=False)
    """Flag indicating whether a user is a system administrator.

    System administrators are allowed to perform certain administrative actions
    separately from any permissions.
    """

    legals_accepted = db.Column(UTCDateTime, nullable=True)
    """Flag indicating if and when a user accepted the legal notices, if configured."""

    state = db.Column(db.Text, index=True, nullable=False)
    """The state of the user."""

    identity = db.relationship("Identity", foreign_keys="User.latest_identity_id")

    identities = db.relationship(
        "Identity",
        lazy="dynamic",
        foreign_keys="Identity.user_id",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    records = db.relationship("Record", lazy="dynamic", back_populates="creator")

    record_links = db.relationship(
        "RecordLink", lazy="dynamic", back_populates="creator"
    )

    files = db.relationship("File", lazy="dynamic", back_populates="creator")

    temporary_files = db.relationship(
        "TemporaryFile", lazy="dynamic", back_populates="creator"
    )

    uploads = db.relationship("Upload", lazy="dynamic", back_populates="creator")

    collections = db.relationship(
        "Collection", lazy="dynamic", back_populates="creator"
    )

    templates = db.relationship("Template", lazy="dynamic", back_populates="creator")

    groups = db.relationship("Group", lazy="dynamic", back_populates="creator")

    favorites = db.relationship(
        "Favorite", lazy="dynamic", back_populates="user", cascade="all, delete-orphan"
    )

    workflows = db.relationship(
        "Workflow",
        lazy="dynamic",
        back_populates="creator",
        cascade="all, delete-orphan",
    )

    revisions = db.relationship("Revision", lazy="dynamic", back_populates="user")

    tasks = db.relationship(
        "Task", lazy="dynamic", back_populates="creator", cascade="all, delete-orphan"
    )

    notifications = db.relationship(
        "Notification",
        lazy="dynamic",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    access_tokens = db.relationship(
        "AccessToken",
        lazy="dynamic",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    oauth2_tokens = db.relationship(
        "OAuth2Token",
        lazy="dynamic",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    config_items = db.relationship(
        "ConfigItem",
        lazy="dynamic",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    permissions = db.relationship(
        "Permission",
        secondary="user_permission",
        lazy="dynamic",
        back_populates="users",
    )

    roles = db.relationship(
        "Role", secondary="user_role", lazy="dynamic", back_populates="users"
    )

    @property
    def is_merged(self):
        """Check if a user was merged."""
        return self.new_user_id is not None

    @property
    def email_confirmed(self):
        """Check if a local user's email is confirmed.

        This is the case if the user's current identity is not local or if their email
        address was confirmed explicitely.
        """
        return (
            not self.identity.type == const.AUTH_PROVIDER_TYPE_LOCAL
            or self.identity.email_confirmed
        )

    @property
    def needs_email_confirmation(self):
        """Check if a user needs email confirmation.

        This is the case if the user's email has not yet been confirmed and email
        confirmation is required by the local authentication provider.
        """
        from .providers.local import LocalProvider

        return not self.email_confirmed and LocalProvider.email_confirmation_required()

    @property
    def needs_legals_acceptance(self):
        """Check if a user needs to accept the legal notices.

        This is the case if accepting the legal notices is required and the user did not
        accept them (or changes to them) yet.
        """

        # Check if accepting the legal notices is required at all.
        if not legals_acceptance_required():
            return False

        # Check if the user never accepted the legal notices before.
        if self.legals_accepted is None:
            return True

        # Check if there is a valid modification date of the legal notices. If so,
        # compare this date to the date of acceptance.
        modification_date = get_legals_modification_date()

        if modification_date is not None:
            return self.legals_accepted < modification_date

        # Otherwise, we consider the legal notices as accepted.
        return False

    @classmethod
    def create(cls, state=UserState.ACTIVE):
        """Create a new user and add it to the database session.

        :param state: (optional) The state of the user.
        :return: The new :class:`User` object.
        """
        user = cls(state=state)
        db.session.add(user)

        return user

    def accept_legals(self):
        """Accept the legal notices for this user.

        Automatically sets the date of acceptance to the current date.
        """
        self.legals_accepted = utcnow()

    def get_config(self, key, default=MISSING, decrypt=False):
        """Get the value of a user-specific config item from the database.

        Convenience method that wraps :func:`kadi.lib.config.core.get_user_config` with
        the user set accordingly.
        """
        return get_user_config(key, user=self, default=default, decrypt=decrypt)

    def set_config(self, key, value, encrypt=False):
        """Set the value of a user-specific config item in the database.

        Convenience method that wraps :func:`kadi.lib.config.core.set_user_config` with
        the user set accordingly.
        """
        return set_user_config(key, value, user=self, encrypt=encrypt)


class Identity(SimpleReprMixin, SimpleTimestampMixin, db.Model):
    """Model to represent base identities.

    This model uses its :attr:`type` column to specify different types of identities.
    Each specific identity (i.e. each subclass of this model) needs at least a unique
    ``username``, a ``displayname`` and an ``email`` column.
    """

    class Meta:
        """Container to store meta class attributes."""

        representation = ["id", "user_id", "type"]
        """See :class:`.SimpleReprMixin`."""

    __tablename__ = "identity"

    id = db.Column(db.Integer, primary_key=True)
    """The ID of the identity, auto incremented."""

    # Needs to be nullable because of the "post_update" in the "user" relationship.
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    """The ID of the user the identity belongs to."""

    type = db.Column(db.Text, nullable=False)
    """The identity type.

    Used by SQLAlchemy to distinguish between different identity types and to
    automatically select from the correct identity table using joined table inheritance.
    """

    # "post_update" is needed because otherwise deleting a user/identity can cause
    # issues due to the cyclic user/identity relationship.
    user = db.relationship(
        "User",
        foreign_keys="Identity.user_id",
        back_populates="identities",
        post_update=True,
    )

    __mapper_args__ = {"polymorphic_identity": "identity", "polymorphic_on": type}


class LocalIdentity(Identity):
    """Model to represent local identities."""

    class Meta:
        """Container to store meta class attributes."""

        representation = ["id", "username", "email"]
        """See :class:`.SimpleReprMixin`."""

        identity_type = {"type": const.AUTH_PROVIDER_TYPE_LOCAL, "name": _l("Local")}
        """The type and full name of the identity."""

        check_constraints = {
            "username": {"length": {"min": 3, "max": 50}},
            "email": {"length": {"max": 256}},
            "displayname": {"length": {"max": 150}},
        }
        """See :func:`kadi.lib.db.generate_check_constraints`."""

    __tablename__ = "local_identity"

    __table_args__ = generate_check_constraints(Meta.check_constraints)

    __mapper_args__ = {"polymorphic_identity": Meta.identity_type["type"]}

    id = db.Column(db.Integer, db.ForeignKey("identity.id"), primary_key=True)
    """The ID of the local identity and of the associated identity."""

    username = db.Column(db.Text, index=True, unique=True, nullable=False)
    """Unique username.

    Restricted to a minimum length of 3 and a maximum length of 50 characters.
    """

    email = db.Column(db.Text, nullable=False)
    """Email address.

    Restricted to a maximum length of 256 characters.
    """

    displayname = db.Column(db.Text, nullable=False)
    """Display name.

    Restricted to a maximum length of 150 characters.
    """

    password_hash = db.Column(db.Text, nullable=False)
    """Hashed password using PBKDF2 with SHA256 and a salt value of 16 chars."""

    email_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    """Indicates whether the user's email has been confirmed or not."""

    @staticmethod
    def _decode_token(token, type):
        payload = decode_jwt(token)

        if payload is None or payload.get("type") != type:
            return None

        return payload

    @classmethod
    def decode_email_confirmation_token(cls, token):
        """Decode the given JSON web token of type ``"email_confirmation"``.

        See also :meth:`get_email_confirmation_token`.

        :param token: The token to decode.
        :return: The tokens decoded payload or ``None`` if the token is invalid or
            expired.
        """
        return cls._decode_token(token, "email_confirmation")

    @classmethod
    def decode_password_reset_token(cls, token):
        """Decode the given JSON web token of type ``"password_reset"``.

        See also :meth:`get_password_reset_token`.

        :param token: The token to decode.
        :return: The tokens decoded payload or ``None`` if the token is invalid or
            expired.
        """
        return cls._decode_token(token, "password_reset")

    @classmethod
    def create(cls, *, user, username, email, displayname, password):
        """Create a new local identity and add it to the database session.

        :param user: The user the identity should belong to.
        :param username: The identity's unique username.
        :param email: The identity's email.
        :param displayname: The identity's display name.
        :param password: The identity's password, which will be hashed securely before
            persisting.
        :return: The new :class:`LocalIdentity` object.
        """
        local_identity = cls(
            user=user, username=username, email=email, displayname=displayname
        )

        local_identity.set_password(password)
        db.session.add(local_identity)

        return local_identity

    def set_password(self, password):
        """Set an identity's password.

        :param password: The password, which will be hashed securely before persisting.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if an identity's password matches the given password.

        The given password will be hashed and checked against the stored password hash.

        :param password: The password to check.
        :return: True if the passwords match, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def get_email_confirmation_token(self, email=None, expires_in=const.ONE_HOUR):
        """Create a new JSON web token of type ``"email_confirmation"``.

        Besides its type, the token includes the ID and email address of this identity.

        :param email: (optional) An email to include in the payload of the token, which
            can be used to change an identity's email on confirmation. Defaults to the
            identity's current email.
        :param expires_in: (optional) The time in seconds the token will expire in.
        :return: The encoded token.
        """
        return encode_jwt(
            {
                "type": "email_confirmation",
                "id": self.id,
                "email": email if email is not None else self.email,
            },
            expires_in=expires_in,
        )

    def get_password_reset_token(self, expires_in=const.ONE_HOUR):
        """Create a new JSON web token of type ``"password_reset"``.

        Besides its type, the token includes the ID of this identity.

        :param expires_in: (optional) The time in seconds the token will expire in.
        :return: The encoded token.
        """
        return encode_jwt(
            {"type": "password_reset", "id": self.id}, expires_in=expires_in
        )


class LDAPIdentity(Identity):
    """Model to represent LDAP identities."""

    class Meta:
        """Container to store meta class attributes."""

        representation = ["id", "username", "email"]
        """See :class:`.SimpleReprMixin`."""

        identity_type = {"type": const.AUTH_PROVIDER_TYPE_LDAP, "name": "LDAP"}
        """The type and full name of the identity."""

        check_constraints = {
            "displayname": {"length": {"max": 150}},
        }
        """See :func:`kadi.lib.db.generate_check_constraints`."""

    __tablename__ = "ldap_identity"

    __table_args__ = generate_check_constraints(Meta.check_constraints)

    __mapper_args__ = {"polymorphic_identity": Meta.identity_type["type"]}

    id = db.Column(db.Integer, db.ForeignKey("identity.id"), primary_key=True)
    """The ID of the LDAP identity and of the associated identity."""

    username = db.Column(db.Text, index=True, unique=True, nullable=False)
    """Unique username."""

    email = db.Column(db.Text, nullable=False)
    """Email address."""

    displayname = db.Column(db.Text, nullable=False)
    """Display name.

    Restricted to a maximum length of 150 characters.
    """

    @classmethod
    def create(cls, *, user, username, email, displayname):
        """Create a new LDAP identity and add it to the database session.

        :param user: The user the identity should belong to.
        :param username: The identity's unique username.
        :param email: The identity's email.
        :param displayname: The identity's display name.
        :return: The new :class:`LDAPIdentity` object.
        """
        ldap_identity = cls(
            user=user, username=username, email=email, displayname=displayname
        )
        db.session.add(ldap_identity)

        return ldap_identity


class ShibIdentity(Identity):
    """Model to represent Shibboleth identities."""

    class Meta:
        """Container to store meta class attributes."""

        representation = ["id", "username", "email"]
        """See :class:`.SimpleReprMixin`."""

        identity_type = {"type": const.AUTH_PROVIDER_TYPE_SHIB, "name": "Shibboleth"}
        """The type and full name of the identity."""

        check_constraints = {
            "displayname": {"length": {"max": 150}},
        }
        """See :func:`kadi.lib.db.generate_check_constraints`."""

    __tablename__ = "shib_identity"

    __table_args__ = generate_check_constraints(Meta.check_constraints)

    __mapper_args__ = {"polymorphic_identity": Meta.identity_type["type"]}

    id = db.Column(db.Integer, db.ForeignKey("identity.id"), primary_key=True)
    """The ID of the Shibboleth identity and of the associated identity."""

    username = db.Column(db.Text, index=True, unique=True, nullable=False)
    """Unique username."""

    email = db.Column(db.Text, nullable=False)
    """Email address."""

    displayname = db.Column(db.Text, nullable=False)
    """Display name.

    Restricted to a maximum length of 150 characters.
    """

    @classmethod
    def create(cls, *, user, username, email, displayname):
        """Create a new Shibboleth identity and add it to the database session.

        :param user: The user the identity should belong to.
        :param username: The identity's unique username.
        :param email: The identity's email.
        :param displayname: The identity's display name.
        :return: The new :class:`ShibIdentity` object.
        """
        shib_identity = cls(
            user=user, username=username, email=email, displayname=displayname
        )
        db.session.add(shib_identity)

        return shib_identity


# Auxiliary table for user roles.
db.Table(
    "user_role",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
)


# Auxiliary table for fine-grained user permissions. Currently still unused, as user
# permissions are managed in bulk via roles.
db.Table(
    "user_permission",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column(
        "permission_id", db.Integer, db.ForeignKey("permission.id"), primary_key=True
    ),
)
