#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from abc import ABC, abstractmethod

from katonic.fs.registry import Registry


class RegistryStore(ABC):
    """
    A registry store is a storage backend for the feature store registry.
    """

    @abstractmethod
    def create_registry(self) -> Registry:
        """
        Creates the registry in PostgreSQL database depending on the backend.

        Args:
            table_query: table query string to create a new table in the database.
            index_query: index query string to create index for the new table in the database.
        """
        pass

    @abstractmethod
    def get_registry(self) -> Registry:
        """
        Retrieves the registry from the registry path. If there is no file at that path,
        raises a FileNotFoundError.

        Args:
            get_query: table query string to create a new table in the database.
        Returns:
            Returns either the registry table stored at the registry path, or an empty registry table.
        """
        pass

    @abstractmethod
    def update_registry(self, registry: Registry):
        """
        Overwrites the current registry with the table passed in. This method
        writes to the registry path.

        Args:
            registry: the new Registry
        """
        pass

    @abstractmethod
    def teardown(self):
        """
        Tear down the registry.
        """
        pass
