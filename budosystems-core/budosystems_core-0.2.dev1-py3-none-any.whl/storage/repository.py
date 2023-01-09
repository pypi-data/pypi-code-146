#
#  Copyright (c) 2021.  Budo Systems
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#

"""
General facility for working with storage repositories
(e.g. RDBMS, NoSQL DBs, in-memory)
"""
from abc import ABC, abstractmethod
from typing import Any, TypeVar, Union
from enum import Enum
from uuid import UUID

from budosystems.models.core import Entity

from .query import Query

__all__ = ['SaveOption', 'Repository', 'ET',
           'RepositoryError', 'RepositoryNotAccessible',
           'EntitySaveFailed', 'EntityReadFailed', 'EntityDeleteFailed',
           'EntityNotFound', 'EntityAlreadyExists', 'QueryError']

class SaveOption(Enum):
    """Options for what to allow when saving to the repository."""
    create_only = 'Create Only'
    update_only = 'Update Only'
    create_or_update = 'Create or Update'


ET = TypeVar('ET', bound=Entity)

class Repository(ABC):
    """Interface for storage repositories."""
    # TODO: Decide whether to implement the __{get,set,delete}_item__ magic methods

    @abstractmethod
    def __init__(self, **kwargs: Any) -> None:
        """
        Abstract initializer that accepts arbitrary keyword arguments.

        Implementations should specify more precisely those it needs.

        :param kwargs: Keyword arguments used for initializing the repository.
        """

    @abstractmethod
    def load(self, entity_type: type[ET], entity_id: UUID) -> ET:
        """
        An implementation will return an Entity with an ID matching the parameter.

        :param entity_type: The specific type of `Entity` expected.
        :param entity_id: The ID used to search the repository.
        :returns: The `Entity` matching the ID.
        :raises EntityReadError: If the repository fails to retrieve an Entity with the given ID.
        """

    @abstractmethod
    def save(self, entity: Entity,
             save_option: SaveOption = SaveOption.create_or_update
             ) -> None:
        """
        An implementation will store the provided entity.

        :param entity: The entity object needing to be stored.
        :param save_option: Whether to allow creation, update, or both.
        :raises EntitySaveError: If the repository failed to store the given Entity.

            Reasons for failure related to the `save_option` parameter are reported as
        :raises EntityAlreadyExists: If `save_option` is set to `SaveOption.create_only` and a
            matching entity already exists in the repository.
        :raises EntityNotFound: If `save_option` is set to `SaveOption.update_only` and a matching
            entity does not currently exist in the repository.
        """

    @abstractmethod
    def delete(self, entity_type: type[ET], entity_id: UUID, must_exist: bool = False) -> None:
        """An implementation will delete Entity with an ID matching the parameter.

        :param entity_type: The specific type of `Entity` expected.
        :param entity_id: The ID of the entity to be deleted.
        :param must_exist: If ``True``, raises an exception if no entity with the ID
            exists in the repository.  If ``False`` (default), proceed silently.
        :raises EntityNotFound: If `must_exist` is set to True and a matching
            entity does not already exist in the repository.
        """

    @abstractmethod
    def match(self, entity_type: type[ET], data: dict[str, Any]) -> list[ET]:
        """An implementation will return every instance of `entity_type` with field
        values matching `data`.

        :param entity_type: The specific type of `Entity` expected.
        :param data: Mapping where the keys correspond to the field names of the entities,
            and the values correspond to the field values to match.  Omitted keys are not matched.
        """

    @abstractmethod
    def find_entities(self, query: Query) -> list[Entity]:
        """
        An implementation will search for entities according to the query.

        :param query: Specification of the entities to return.
        :returns: A (possibly empty) list of the entities satisfying the query.
        :raises QueryError: If there are problems with the query.
        """

    @abstractmethod
    def find_data(self, query: Query) -> list[dict[str, Any]]:
        """
        An implementation will search for data according to the query.

        The structure and format of the expected data is specified in the query.

        :param query: Specification of the data to return.
        :returns: A (possibly empty) list of the data entries satisfying the query.
        :raises QueryError: If there are problems with the query.
        """


# TODO: Should these be left as exceptions, or changed to `Event`s?
class RepositoryError(Exception):
    """General Repository related exception."""
    reason: Union[str, Exception, None]

    def __init__(self, *args: Any, reason: Union[str, Exception, None] = None) -> None:
        super().__init__(*args)
        self.reason = reason


class EntityNotFound(RepositoryError):
    """This exception gets raised if the repository attempts to find an
    entity, but it is not found."""


class EntityAlreadyExists(RepositoryError):
    """This exception gets raised if the repository attempts to overwrite an
    existing entity when it expects none with the same ID to be there."""


class EntitySaveFailed(RepositoryError):
    """This exception gets raised if an attempt to save an `Entity` has failed."""


class EntityReadFailed(RepositoryError):
    """This exception gets raised if an attempt to load an `Entity` has failed."""


class EntityDeleteFailed(RepositoryError):
    """This exception gets raised if an attempt to delete an `Entity` has failed."""


class RepositoryNotAccessible(RepositoryError):
    """This exception gets raised if the repository cannot be accessed."""


class QueryError(RepositoryError):
    """This exception gets raised if there are problems interpreting the query."""
