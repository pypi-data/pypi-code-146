# Copyright 2021 Vincent Texier <vit@free.fr>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional

from tikka.adapters.repository.sqlite3 import Sqlite3RepositoryInterface
from tikka.domains.entities.identity import Identity
from tikka.interfaces.adapters.repository.identities import (
    IdentitiesRepositoryInterface,
)

TABLE_NAME = "identities"


class Sqlite3IdentitiesRepository(
    IdentitiesRepositoryInterface, Sqlite3RepositoryInterface
):
    """
    Sqlite3IdentitiesRepository class
    """

    def add(self, identity: Identity) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            IdentitiesRepositoryInterface.add.__doc__
        )

        # insert only non hidden fields
        self.client.insert(
            TABLE_NAME,
            **get_fields_from_identity(identity),
        )

    def get(self, index: int) -> Optional[Identity]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            IdentitiesRepositoryInterface.get.__doc__
        )

        row = self.client.select_one(
            f"SELECT * FROM {TABLE_NAME} WHERE index_=?", (index,)
        )
        if row is None:
            return None

        return Identity(*row)

    def update(self, identity: Identity) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            IdentitiesRepositoryInterface.update.__doc__
        )

        # update only non hidden fields
        self.client.update(
            TABLE_NAME,
            f"index_='{identity.index}'",
            **get_fields_from_identity(identity),
        )

    def delete(self, index: int) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            IdentitiesRepositoryInterface.delete.__doc__
        )

        self.client.delete(TABLE_NAME, index_=index)

    def exists(self, index: int) -> bool:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            IdentitiesRepositoryInterface.exists.__doc__
        )

        row = self.client.select_one(
            f"SELECT count(index_) FROM {TABLE_NAME} WHERE index_=?", (index,)
        )
        if row is None:
            return False

        return row[0] == 1


def get_fields_from_identity(identity: Identity) -> dict:
    """
    Return a dict of supported fields with normalized value

    :param identity: Identity instance
    :return:
    """
    fields = {}
    for (key, value) in identity.__dict__.items():
        if key.startswith("_"):
            continue
        if key == "index":
            # index is a reserved keyword in sqlite3
            key = "index_"
        fields[key] = value

    return fields
