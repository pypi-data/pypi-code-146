from typing import List, Optional, Union
from warnings import warn

import arrow

from rhino_health.lib.endpoints.data_schema.data_schema_dataclass import (
    Dataschema,
    FutureDataschema,
)
from rhino_health.lib.endpoints.endpoint import Endpoint, NameFilterMode, VersionMode
from rhino_health.lib.utils import alias, rhino_error_wrapper


class DataschemaEndpoints(Endpoint):
    """
    @autoapi False
    """

    @property
    def data_schema_data_class(self):
        """
        @autoapi False
        """
        return Dataschema

    @rhino_error_wrapper
    def get_data_schemas(self, data_schema_uids: Optional[List[str]] = None) -> List[Dataschema]:
        """
        @autoapi True
        Gets the Data Schemas with the specified DATA_SCHEMA_UIDS

        .. warning:: This feature is under development and the interface may change
        """
        if not data_schema_uids:
            return self.session.get("/dataschemas/").to_dataclasses(self.data_schema_data_class)
        else:
            return [
                self.session.get(f"/dataschemas/{data_schema_uid}/").to_dataclass(
                    self.data_schema_data_class
                )
                for data_schema_uid in data_schema_uids
            ]

    get_dataschemas = alias(get_data_schemas, "get_dataschemas", base_object="session.data_schema")
    """ @autoapi False """


class DataschemaFutureEndpoints(DataschemaEndpoints):
    """
    @objname DataschameEndpoints
    """

    @property
    def data_schema_data_class(self):
        return FutureDataschema

    @rhino_error_wrapper
    def get_data_schema_by_name(
        self, name, version=VersionMode.LATEST, project_uid=None
    ) -> Optional[Dataschema]:
        """
        Returns the latest or a specific Dataschema dataclass

        .. warning:: This feature is under development and the interface may change
        .. warning:: There is no uniqueness constraint on the name for data_schemas so you may not get the correct result
        .. warning:: VersionMode.ALL will return the same as VersionMode.LATEST

        Parameters
        ----------
        name: str
            Full name for the Dataschema
        version: Optional[Union[int, VersionMode]]
            Version of the Dataschema, latest by default, for an earlier version pass in an integer
        project_uid: Optional[str]
            Project UID to search under

        Returns
        -------
        data_schema: Optional[Dataschema]
            Dataschema with the name or None if not found

        Examples
        --------
        >>> session.data_schema.get_data_schema_by_name("My Dataschema")
        Dataschema("My Dataschema")
        """
        if version == VersionMode.ALL:
            warn(
                "VersionMode.ALL behaves the same as VersionMode.LATEST for get_data_schema_by_name(), did you mean to use search_for_data_schemas_by_name()?",
                RuntimeWarning,
            )
        results = self.search_for_data_schemas_by_name(
            name, version, project_uid, NameFilterMode.EXACT
        )
        if len(results) > 1:
            warn(
                "More than one data schema was found with the name for the provided project,"
                "please verify the schema is correct. This function returns the last created schema",
                RuntimeWarning,
            )
        return max(results, key=lambda x: arrow.get(x.created_at)) if results else None

    get_dataschema_by_name = alias(
        get_data_schema_by_name, "get_dataschema_by_name", base_object="session.data_schema"
    )
    """ @autoapi False """

    @rhino_error_wrapper
    def search_for_data_schemas_by_name(
        self,
        name: str,
        version: Optional[Union[int, VersionMode]] = VersionMode.LATEST,
        project_uid: Optional[str] = None,
        name_filter_mode: Optional[NameFilterMode] = NameFilterMode.CONTAINS,
    ):
        """
        Returns DataSchema dataclasses

        .. warning:: This feature is under development and the interface may change

        Parameters
        ----------
        name: str
            Full or partial name for the Dataschema
        version: Optional[Union[int, VersionMode]]
            Version of the Dataschema, latest by default
        project_uid: Optional[str]
            Project UID to search under
        name_filter_mode: Optional[NameFilterMode]
            Only return results with the specified filter mode. By default uses CONTAINS

        Returns
        -------
        data_schemas: List[Dataschema]
            Dataschema dataclasses that match the name

        Examples
        --------
        >>> session.data_schema.search_for_data_schemas_by_name("My Dataschema")
        [Dataschema(name="My Dataschema")]

        See Also
        --------
        rhino_health.lib.endpoints.endpoint.FilterMode : Different modes to filter by
        rhino_health.lib.endpoints.endpoint.VersionMode : Return specific versions


        """
        query_params = self._get_filter_query_params(
            {"name": name, "object_version": version, "project_uid": project_uid},
            name_filter_mode=name_filter_mode,
        )
        results = self.session.get("/dataschemas", params=query_params)
        return results.to_dataclasses(self.data_schema_data_class)

    search_for_dataschemas_by_name = alias(
        search_for_data_schemas_by_name,
        "search_for_dataschemas_by_name",
        base_object="session.data_schema",
    )
    """ @autoapi False """

    @rhino_error_wrapper
    def create_data_schema(self, data_schema, return_existing=True, add_version_if_exists=False):
        """
        @autoapi False

        Adds a new data_schema

        Parameters
        ----------
        data_schema: DataschemaCreateInput
            DataschemaCreateInput data class
        return_existing: bool
            If a Dataschema with the name already exists, return it instead of creating one.
            Takes precedence over add_version_if_exists
        add_version_if_exists
            If a Dataschema with the name already exists, create a new version.

        Returns
        -------
        data_schema: Dataschema
            Dataschema dataclass

        Examples
        --------
        >>> session.data_schema.create_data_schema(create_data_schema_input)
        Dataschema()
        """
        if return_existing or add_version_if_exists:
            for project_uid in data_schema.project_uids:
                # We need to iterate through the different project_uids because the user may not have permission to get from the first one
                try:
                    existing_dataschema = self.search_for_data_schemas_by_name(
                        data_schema.name,
                        project_uid=project_uid,
                        name_filter_mode=NameFilterMode.EXACT,
                    )[0]
                    if return_existing:
                        return existing_dataschema
                    else:
                        data_schema.base_version_uid = (
                            existing_dataschema.base_version_uid or existing_dataschema.uid
                        )
                        data_schema.__fields_set__.discard("version")
                        break
                except Exception:
                    # If no existing Dataschema exists do nothing
                    pass
        result = self.session.post(
            "/dataschemas",
            data_schema.dict(by_alias=True, exclude_unset=True),
            adapter_kwargs={"data_as_json": True},
        )
        return result.to_dataclass(self.data_schema_data_class)

    # @rhino_error_wrapper
    # def get_data_schema_csv(self, data_schema_uid: str):
    #     """
    #     @autoapi False
    #
    #     .. warning:: This feature is under development and incomplete
    #     """
    #     # TODO: What does this actually do do we need this?
    #     raise NotImplementedError()
    #     # return self.session.get(f"/dataschemas/{data_schema_uid}/export_to_csv")

    @rhino_error_wrapper
    def remove_data_schema(self, dataschema_uid: str):
        """
        Removes a Dataschema with the DATASCHAMA_UID from the system

        .. warning:: This feature is under development and incomplete
        """
        return self.session.post(f"/dataschemas/{dataschema_uid}/remove")

    remove_dataschema = alias(
        remove_data_schema, "remove_dataschema", base_object="session.data_schema"
    )
    """ @autoapi False """
