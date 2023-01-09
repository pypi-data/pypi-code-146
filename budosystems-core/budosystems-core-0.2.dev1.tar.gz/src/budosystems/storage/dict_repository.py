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
"""Reference implementation of `Repository` using a Dictionary."""

from typing import Any, Union
from uuid import UUID
from collections import defaultdict

from attr import evolve, fields

from budosystems.models.core import Entity, MissingBudoObject
from .query import Query
from .repository import (Repository, SaveOption, ET, EntityReadFailed, EntitySaveFailed,
                         EntityDeleteFailed, EntityAlreadyExists, EntityNotFound)


class DictRepository(Repository):
    """Dictionary-based Repository"""

    _data: dict[type[Entity], dict[UUID, Union[Entity, MissingBudoObject]]]

    def __init__(self) -> None:
        super().__init__()
        self._data = {}

    def load(self, entity_type: type[ET], entity_id: UUID) -> ET:
        """See `Repository.load`"""

        if entity_type not in self._data:
            raise EntityReadFailed(reason=TypeError(f"No table for {entity_type}"))
        val = self._data[entity_type][entity_id]
        if val is MissingBudoObject():
            raise EntityReadFailed(
                    reason=EntityNotFound(f"Could not find {entity_id} in table {entity_type}")
            )
        if not isinstance(val, entity_type):
            raise EntityReadFailed(
                    reason=TypeError(f"Invalid type {type(val)}, expected {entity_type}")
            )

        # Returning a copy of the value ensures changes are not propagated to the repository
        # until an explicit call to save.
        return evolve(val)

    def save(self, entity: Entity, save_option: SaveOption = SaveOption.create_or_update) -> None:
        """See `Repository.save`"""

        entity_type = type(entity)

        # Ensure there is storage for the entity type
        if entity_type not in self._data:
            self._data[entity_type] = defaultdict(MissingBudoObject)
        table = self._data[entity_type]

        # Check save restrictions
        if save_option == SaveOption.create_only and entity.entity_id in table:
            raise EntitySaveFailed(reason=EntityAlreadyExists())
        if save_option == SaveOption.update_only and entity.entity_id not in table:
            raise EntitySaveFailed(reason=EntityNotFound())

        self.delete(entity_type, entity.entity_id)

        # Save a copy of the entity.  This ensures that further changes to the entity
        # are not propagated to the repository until explicitly saved again.
        table[entity.entity_id] = evolve(entity)

    def delete(self, entity_type: type[ET], entity_id: UUID, must_exist: bool = False) -> None:
        """See `Repository.delete`"""

        if entity_type not in self._data:
            if must_exist:
                raise EntityDeleteFailed(
                        reason=TypeError(f"Entity type {entity_type} not found is storage.")
                )
            return

        if entity_id in self._data[entity_type]:
            entity = self._data[entity_type][entity_id]
            for f in fields(entity_type):
                # Remove fields, thereby unlinking references to other entities (if any)
                delattr(entity, f.name)
            del self._data[entity_type][entity_id]
        elif must_exist:
            raise EntityDeleteFailed(
                    reason=EntityNotFound(f"Entity ID {entity_id} not found is storage.")
            )
        return

    def match(self, entity_type: type[ET], data: dict[str, Any]) -> list[ET]:
        """See `Repository.match`"""

        entities: list[ET] = []

        if entity_type not in self._data:
            return entities

        for ent in self._data[entity_type].values():
            if ent is MissingBudoObject():
                continue
            if not isinstance(ent, entity_type):
                raise TypeError(f"Unexpected object '{str(ent)}' of type {type(ent)}, "
                                f"expected type {entity_type}")
            if all(getattr(ent, k) == v for k, v in data.items()):
                entities.append(ent)

        return entities

    def find_entities(self, query: Query) -> list[Entity]:
        """See `Repository.find_entities`"""

        raise NotImplementedError()

    def find_data(self, query: Query) -> list[dict[str, Any]]:
        """See `Repository.find_data`"""

        raise NotImplementedError()
