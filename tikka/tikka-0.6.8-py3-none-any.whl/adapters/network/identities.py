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
import logging
from typing import Optional

from tikka.domains.entities.identity import Identity
from tikka.interfaces.adapters.network.identities import NetworkIdentitiesInterface


class NetworkIdentities(NetworkIdentitiesInterface):
    """
    NetworkIdentities class
    """

    def get_identity_index(self, address: str) -> Optional[int]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkIdentitiesInterface.get_identity_index.__doc__
        )
        if not self.connections.is_connected():
            return None
        if self.connections.rpc.client is None:
            return None

        try:
            result = self.connections.rpc.client.query(
                "Identity", "IdentityIndexOf", [address]
            )
        except Exception as exception:
            logging.exception(exception)
            return None

        return result.value

    def get_identity(self, index: int) -> Optional[Identity]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkIdentitiesInterface.get_identity.__doc__
        )
        if not self.connections.is_connected():
            return None
        if self.connections.rpc.client is None:
            return None

        try:
            result = self.connections.rpc.client.query(
                "Identity", "Identities", [index]
            )
        except Exception as exception:
            logging.exception(exception)
            return None
        return Identity(
            index=index,
            next_creatable_on=result["next_creatable_identity_on"].value,
            removable_on=int(result["removable_on"].value),
            status=result["status"].value,
        )
