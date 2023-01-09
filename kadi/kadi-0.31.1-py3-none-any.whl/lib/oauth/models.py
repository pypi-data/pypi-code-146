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
from sqlalchemy_utils.types.encrypted.encrypted_type import StringEncryptedType

from kadi.ext.db import db
from kadi.ext.db import KadiAesEngine
from kadi.lib.db import unique_constraint
from kadi.lib.db import UTCDateTime
from kadi.lib.utils import SimpleReprMixin
from kadi.lib.utils import utcnow


class OAuth2Token(SimpleReprMixin, db.Model):
    """Model to represent OAuth2 client bearer tokens.

    Note that this model uses encrypted fields and can potentially raise a
    :class:`.KadiDecryptionKeyError` when a value cannot be decrypted.
    """

    class Meta:
        """Container to store meta class attributes."""

        representation = ["id", "user_id", "name"]
        """See :class:`.SimpleReprMixin`."""

    __tablename__ = "oauth2_token"

    __table_args__ = (unique_constraint(__tablename__, "user_id", "name"),)

    id = db.Column(db.Integer, primary_key=True)
    """The ID of the token, auto incremented."""

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    """The ID of the user the token belongs to."""

    name = db.Column(db.Text, nullable=False)
    """The name of the token."""

    access_token = db.Column(
        StringEncryptedType(
            type_in=db.Text, engine=KadiAesEngine, key=KadiAesEngine.get_secret_key
        ),
        nullable=False,
    )
    """The actual access token, stored encrypted."""

    refresh_token = db.Column(
        StringEncryptedType(
            type_in=db.Text, engine=KadiAesEngine, key=KadiAesEngine.get_secret_key
        ),
        nullable=True,
    )
    """The optional refresh token, stored encrypted."""

    expires_at = db.Column(UTCDateTime, nullable=True)
    """The optional expiration date and time of the access token."""

    user = db.relationship("User", back_populates="oauth2_tokens")

    @property
    def is_expired(self):
        """Check if the OAuth2 token is expired."""
        if self.expires_at is not None:
            return self.expires_at < utcnow()

        return False

    def to_token(self):
        """Convert the OAuth2 token in a format usable by an Authlib client.

        :return: A dictionary representation of the OAuth2 token.
        """
        expires_at = None

        if self.expires_at is not None:
            expires_at = int(self.expires_at.timestamp())

        return {
            "token_type": "bearer",
            "expires_at": expires_at,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
        }

    @classmethod
    def create(cls, *, user, name, access_token, refresh_token=None, expires_at=None):
        """Create a new OAuth2 bearer token and add it to the database session.

        :param user: The user the token should belong to.
        :param name: The name of the token.
        :param access_token: The actual access token.
        :param refresh_token: (optional) The refresh token.
        :param expires_at: (optional) The expiration date and time of the access token.
        :return: The new :class:`OAuth2Token` object.
        """
        oauth2_token = cls(
            user=user,
            name=name,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
        )
        db.session.add(oauth2_token)

        return oauth2_token
