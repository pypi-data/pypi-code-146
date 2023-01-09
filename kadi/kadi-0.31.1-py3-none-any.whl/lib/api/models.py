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
from kadi.ext.db import db
from kadi.lib.db import generate_check_constraints
from kadi.lib.db import UTCDateTime
from kadi.lib.security import hash_value
from kadi.lib.security import random_bytes
from kadi.lib.utils import SimpleReprMixin
from kadi.lib.utils import utcnow


class AccessToken(SimpleReprMixin, db.Model):
    """Model to represent personal access tokens."""

    class Meta:
        """Container to store meta class attributes."""

        representation = ["id", "user_id", "name"]
        """See :class:`.SimpleReprMixin`."""

        check_constraints = {
            "name": {"length": {"max": 150}},
        }
        """See :func:`kadi.lib.db.generate_check_constraints`."""

    __tablename__ = "access_token"

    __table_args__ = generate_check_constraints(Meta.check_constraints)

    id = db.Column(db.Integer, primary_key=True)
    """The ID of the access token, auto incremented."""

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    """The ID of the user the access token belongs to."""

    name = db.Column(db.Text, nullable=False)
    """The name of the access token.

    Restricted to a maximum length of 150 characters.
    """

    token_hash = db.Column(db.Text, index=True, nullable=False)
    """The actual, hashed token."""

    expires_at = db.Column(UTCDateTime, nullable=True)
    """The optional date and time the token expires in."""

    created_at = db.Column(UTCDateTime, default=utcnow, nullable=False)
    """The date and time the token was created at."""

    last_used = db.Column(UTCDateTime, nullable=True)
    """The date and time the token was last used."""

    user = db.relationship("User", back_populates="access_tokens")

    scopes = db.relationship(
        "AccessTokenScope",
        lazy="dynamic",
        back_populates="access_token",
        cascade="all, delete-orphan",
    )

    @property
    def is_expired(self):
        """Check if the access token is expired."""
        if self.expires_at is not None:
            return self.expires_at < utcnow()

        return False

    @staticmethod
    def new_token():
        """Create a new random token.

        :return: The generated token string.
        """
        return random_bytes()

    @staticmethod
    def hash_token(token):
        """Create a secure hash of a token.

        :param token: The token to hash.
        :return: The calculated hash as a hexadecimal string.
        """
        return hash_value(token)

    @classmethod
    def get_by_token(cls, token):
        """Get an access token object from the database using a token.

        :param token: The token to search for.
        :return: The access token object or ``None``.
        """
        token_hash = cls.hash_token(token)
        return cls.query.filter_by(token_hash=token_hash).first()

    @classmethod
    def create(cls, *, user, name, expires_at=None, token=None):
        """Create a new access token and add it to the database session.

        :param user: The user the access token should belong to.
        :param name: The access token's name.
        :param expires_at: (optional) The access token's expiration date.
        :param token: (optional) The actual token, which will be hashed before
            persisting. Defaults to a token created by :meth:`new_token`.
        :return: The new :class:`AccessToken` object.
        """
        token = token if token is not None else cls.new_token()

        access_token = cls(
            user=user,
            name=name,
            token_hash=cls.hash_token(token),
            expires_at=expires_at,
        )
        db.session.add(access_token)

        return access_token


class AccessTokenScope(SimpleReprMixin, db.Model):
    """Model to represent access token scopes."""

    class Meta:
        """Container to store meta class attributes."""

        representation = ["id", "access_token_id", "object", "action"]
        """See :class:`.SimpleReprMixin`."""

    __tablename__ = "access_token_scope"

    id = db.Column(db.Integer, primary_key=True)
    """The ID of the scope, auto incremented."""

    access_token_id = db.Column(
        db.Integer, db.ForeignKey("access_token.id"), nullable=False
    )
    """The ID of the access token the scope belongs to."""

    object = db.Column(db.Text, nullable=False)
    """The object the action of the scope relates to."""

    action = db.Column(db.Text, nullable=False)
    """The action the scope allows to do related to its object."""

    access_token = db.relationship("AccessToken", back_populates="scopes")

    @classmethod
    def create(cls, *, access_token, object, action):
        """Create a new access token scope and add it to the database session.

        :param access_token: The access token the scope should belong to.
        :param object: The object of the scope.
        :param action: The action of the scope.
        :return: The new :class:`AccessTokenScope` object.
        """
        access_token_scope = cls(
            access_token=access_token, object=object, action=action
        )
        db.session.add(access_token_scope)

        return access_token_scope
