from typing import List
from bodosdk.api.catalog import CatalogApi
from bodosdk.models.catalog import (
    CatalogDefinition,
    CatalogInfo,
    CatalogUpdateDefinition,
)


class CatalogClient:
    def __init__(self, api: CatalogApi):
        self._api = api

    def create(self, catalog_definition: CatalogDefinition) -> CatalogInfo:
        """
        Creates catalog
        :param catalog_definition:
        :type catalog_definition: CatalogDefinition
        :return: catalog object
        :rtype: CatalogInfo
        """
        return self._api.create_catalog(catalog_definition)

    def get(self, uuid) -> CatalogInfo:
        """
        Creates catalog
        :param uuid: Get Catalog for specific uuid
        :type uuid: str
        :return: catalog object
        :rtype: CatalogInfo
        """
        return self._api.get_catalog(uuid)

    def get_by_name(self, name) -> CatalogInfo:
        """
        Creates catalog
        :param name: Get Catalog for specific name
        :type name: str
        :return: catalog object
        :rtype: CatalogInfo
        """
        return self._api.get_catalog_by_name(name)

    def list(self) -> List[CatalogInfo]:
        """
        Gets list of catalogs in a workspace
        :return:
        """
        return self._api.get_all_catalogs()

    def update(
        self, uuid, catalog_update_definition: CatalogUpdateDefinition
    ) -> CatalogInfo:
        """
        Update catalog
        :param uuid: Update Catalog for specific uuid
        :type uuid: str
        :param catalog_update_definition:
        :type catalog_update_definition: CatalogUpdateDefinition
        :return: catalog object
        :rtype: CatalogInfo
        """
        return self._api.update_catalog(uuid, catalog_update_definition)

    def remove(self, uuid):
        """
        Delete catalog
        :param uuid: uuid of the catalog to remove
        :type uuid: str
        """
        return self._api.delete_catalog(uuid)

    def remove_all(self):
        """
        Delete all catalogs in a workspace
        :return:
        """
        return self._api.delete_all_catalogs()
