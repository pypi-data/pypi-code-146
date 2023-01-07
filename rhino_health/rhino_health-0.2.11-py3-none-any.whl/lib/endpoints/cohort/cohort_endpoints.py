from typing import Optional, Union
from warnings import warn

import arrow

from rhino_health.lib.endpoints.cohort.cohort_dataclass import (
    BaseCohort,
    Cohort,
    CohortCreateInput,
    FutureCohort,
)
from rhino_health.lib.endpoints.endpoint import Endpoint, NameFilterMode, VersionMode
from rhino_health.lib.metrics.base_metric import MetricResponse
from rhino_health.lib.utils import rhino_error_wrapper


class CohortEndpoints(Endpoint):
    """
    @autoapi False
    """

    @property
    def cohort_data_class(self):
        return Cohort

    @rhino_error_wrapper
    def get_cohort(self, cohort_uid: str):
        """
        @autoapi True
        Returns a Cohort dataclass

        Parameters
        ----------
        cohort_uid: str
            UID for the cohort

        Returns
        -------
        cohort: Cohort
            Cohort dataclass

        Examples
        --------
        >>> session.cohort.get_cohort(my_cohort_uid)
        Cohort()
        """
        return self.session.get(f"/cohorts/{cohort_uid}").to_dataclass(self.cohort_data_class)

    @rhino_error_wrapper
    def get_cohort_metric(self, cohort_uid: str, metric_configuration) -> MetricResponse:
        """
        @autoapi True
        Queries the cohort with COHORT_UID on-prem and returns the result based on the METRIC_CONFIGURATION

        Parameters
        ----------
        cohort_uid: str
            UID for the cohort to query metrics against
        metric_configuration:
            Configuration for the query to run

        Returns
        -------
        metric_response: MetricResponse
            A response object containing the result of the query

        See Also
        --------
        rhino_health.lib.metrics : Dataclasses specifying possible metric configurations to send
        rhino_health.lib.metrics.base_metric.MetricResponse : Response object
        """
        return self.session.post(
            f"/cohorts/{cohort_uid}/metric/", metric_configuration.data()
        ).to_dataclass(MetricResponse)


class CohortFutureEndpoints(CohortEndpoints):
    """
    @autoapi True
    @objname CohortEndpoints

    Endpoints available to interact with Cohorts on the Rhino Platform

    Notes
    -----
    You should access these endpoints from the RhinoSession object
    """

    @property
    def cohort_data_class(self):
        """
        @autoapi False
        Dataclass to return for a cohort endpoint for backwards compatibility
        """
        return FutureCohort

    @rhino_error_wrapper
    def get_cohort_by_name(
        self, name, version=VersionMode.LATEST, project_uid=None
    ) -> Optional[Cohort]:
        """
        Returns the latest or a specific Cohort dataclass

        .. warning:: VersionMode.ALL will return the same as VersionMode.LATEST

        Parameters
        ----------
        name: str
            Full name for the Cohort
        version: Optional[Union[int, VersionMode]]
            Version of the Cohort, latest by default, for an earlier version pass in an integer

        project_uid: Optional[str]
            Project UID to search under

        Returns
        -------
        cohort: Optional[Cohort]
            Cohort with the name or None if not found

        Examples
        --------
        >>> session.cohort.get_cohort_by_name("My Cohort")
        Cohort(name="My Cohort")
        """
        if version == VersionMode.ALL:
            warn(
                "VersionMode.ALL behaves the same as VersionMode.LATEST for get_cohort_by_name(), did you mean to use search_for_cohorts_by_name()?",
                RuntimeWarning,
            )
        results = self.search_for_cohorts_by_name(name, version, project_uid, NameFilterMode.EXACT)
        return max(results, key=lambda x: arrow.get(x.created_at)) if results else None

    @rhino_error_wrapper
    def search_for_cohorts_by_name(
        self,
        name: str,
        version: Optional[Union[int, VersionMode]] = VersionMode.LATEST,
        project_uid: Optional[str] = None,
        name_filter_mode: Optional[NameFilterMode] = NameFilterMode.CONTAINS,
    ):
        """
        Returns Cohort dataclasses

        Parameters
        ----------
        name: str
            Full or partial name for the Cohort
        version: Optional[Union[int, VersionMode]]
            Version of the Cohort, latest by default
        project_uid: Optional[str]
            Project UID to search under
        name_filter_mode: Optional[NameFilterMode]
            Only return results with the specified filter mode, By default uses CONTAINS

        Returns
        -------
        cohorts: List[Cohort]
            Cohort dataclasses that match the name

        Examples
        --------
        >>> session.cohort.search_for_cohorts_by_name("My Cohort")
        [Cohort(name="My Cohort")]

        See Also
        --------
        rhino_health.lib.endpoints.endpoint.FilterMode : Different modes to filter by
        rhino_health.lib.endpoints.endpoint.VersionMode : Which version to return
        """
        query_params = self._get_filter_query_params(
            {"name": name, "object_version": version, "project_uid": project_uid},
            name_filter_mode=name_filter_mode,
        )
        result = self.session.get("/cohorts", params=query_params)
        return result.to_dataclasses(self.cohort_data_class)

    @rhino_error_wrapper
    def add_cohort(
        self, cohort: CohortCreateInput, return_existing=True, add_version_if_exists=False
    ) -> Cohort:
        """
        Adds a new cohort on the remote instance.

        .. warning:: This feature is under development and the interface may change

        Parameters
        ----------
        cohort: CohortCreateInput
            CohortCreateInput data class
        return_existing: bool
            If a Cohort with the name already exists, return it instead of creating one.
            Takes precedence over add_version_if_exists
        add_version_if_exists
            If a Cohort with the name already exists, create a new version.

        Returns
        -------
        cohort: Cohort
            Cohort dataclass

        Examples
        --------
        >>> session.chort.add_cohort(add_cohort_input)
        Cohort()
        """
        if return_existing or add_version_if_exists:
            try:
                existing_cohort = self.search_for_cohorts_by_name(
                    cohort.name,
                    project_uid=cohort.project_uid,
                    name_filter_mode=NameFilterMode.EXACT,
                )[0]
                if return_existing:
                    return existing_cohort
                else:
                    cohort.base_version_uid = (
                        existing_cohort.base_version_uid or existing_cohort.uid
                    )
                    cohort.__fields_set__.discard("version")
            except Exception:
                # If no existing AI Model exists do nothing
                pass
        newly_created_cohort = self._create_cohort(cohort)
        self._import_cohort_data(newly_created_cohort.uid, cohort)
        return self.get_cohort(newly_created_cohort.uid)

    @rhino_error_wrapper
    def _create_cohort(self, cohort: BaseCohort) -> Cohort:
        """
        Creates a new cohort on the remote instance.

        This function is intended for internal use only

        .. warning:: This feature is under development and the interface may change
        """
        return self.session.post("/cohorts/", cohort.create_args()).to_dataclass(
            self.cohort_data_class
        )

    @rhino_error_wrapper
    def _import_cohort_data(self, cohort_uid: str, import_data: CohortCreateInput):
        """
        Imports cohort data on an existing cohort.

        This function is intended for internal use only

        .. warning:: This feature is under development and the interface may change
        """
        return self.session.post(f"/cohorts/{cohort_uid}/import", import_data.import_args())

    @rhino_error_wrapper
    def export_cohort(self, cohort_uid: str, output_location: str, output_format: str):
        """
        Sends a export cohort request to the ON-PREM instance holding the specified COHORT_UID.
        The file will be exported to OUTPUT_LOCATION on the on-prem instance in OUTPUT_FORMAT

        .. warning:: This feature is under development and the interface may change

        Parameters
        ----------
        cohort_uid: str
            UID for the cohort to export information on
        output_location: str
            Path to output the exported data to on the remote on-prem instance
        output_format: str
            The format to export the cohort data in
        """
        return self.session.get(
            f"/cohorts/{cohort_uid}/export",
            params={"output_location": output_location, "output_format": output_format},
        )

    @rhino_error_wrapper
    def sync_cohort_info(self, cohort_uid: str):
        """
        Initializes a data sync from the relevant on-prem instance for the provided COHORT_UID

        .. warning:: This feature is under development and the interface may change

        Parameters
        ----------
        cohort_uid: str
            UID for the cohort to sync info
        """
        # TODO: what should this return value be?
        return self.session.get(f"/cohorts/{cohort_uid}/info")

    @rhino_error_wrapper
    def remove_cohort(self, cohort_uid: str):
        """
        Remove a cohort with COHORT_UID from the system

        .. warning:: This feature is under development and the interface may change

        Parameters
        ----------
        cohort_uid: str
            UID for the cohort to remove
        """
        # TODO: what should this return value be?
        return self.session.post(f"/cohorts/{cohort_uid}/remove", {})
