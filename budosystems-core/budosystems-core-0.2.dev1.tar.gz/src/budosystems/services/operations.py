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

"""'Unit of Work' pattern module."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, Optional, Any
# from typing_extensions import Self
from types import TracebackType

from budosystems.storage.repository import Repository

# Because mypy doesn't yet support typing.Self (nor typing_extensions.Self)
UoWSelfType = TypeVar('UoWSelfType', bound="UnitOfWork")
AUoWSelfType = TypeVar('AUoWSelfType', bound="AsyncUnitOfWork")

Ex = TypeVar('Ex', bound=Exception)

class UnitOfWork(ABC):
    """
    See: https://martinfowler.com/eaaCatalog/unitOfWork.html
    """
    repo: Repository
    committed: bool

    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        self.committed = False

    def __enter__(self: UoWSelfType) -> UoWSelfType:
        self.committed = False
        return self

    def __exit__(self: UoWSelfType,
                 exc_type: Optional[type[Ex]],
                 exc_val: Optional[Ex],
                 exc_tb: Optional[TracebackType]
                 ) -> bool:
        if not self.committed:
            self.rollback()
        return self.committed

    def commit(self) -> None:
        """
        This method must be called to mark the end of a complete transaction.

        Implementations of this class should override this method and call `super().commit()`.
        """
        self.committed = True

    @abstractmethod
    def rollback(self) -> None:
        """
        This method will be called if the context manager exits without being committed.

        Implementations must bring the state back to what it was before entering the context.
        """


class AsyncUnitOfWork(ABC):
    """
    See: https://martinfowler.com/eaaCatalog/unitOfWork.html
    """
    repo: Repository
    committed: bool

    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        self.committed = False

    async def __aenter__(self: AUoWSelfType) -> AUoWSelfType:
        self.committed = False
        return self

    async def __aexit__(self: AUoWSelfType,
                        exc_type: Optional[type[Ex]],
                        exc_val: Optional[Ex],
                        exc_tb: Optional[TracebackType]
                        ) -> bool:
        if not self.committed:
            await self.rollback()
        return self.committed

    async def commit(self) -> None:
        """
        This method must be called to mark the end of a complete transaction.

        Implementations of this class should override this method and call `super().commit()`.
        """
        self.committed = True

    @abstractmethod
    async def rollback(self) -> None:
        """
        This method will be called if the context manager exits without being committed.

        Implementations must bring the state back to what it was before entering the context.
        """
