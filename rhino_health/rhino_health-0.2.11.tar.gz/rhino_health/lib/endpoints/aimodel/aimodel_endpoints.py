from typing import Optional, Union
from warnings import warn

import arrow

from rhino_health.lib.endpoints.aimodel.aimodel_dataclass import (
    AIModel,
    AIModelCreateInput,
    AIModelMultiCohortInput,
    AIModelRunAsyncResponse,
    AIModelRunInput,
    AIModelRunSyncResponse,
    AIModelTrainAsyncResponse,
    AIModelTrainInput,
)
from rhino_health.lib.endpoints.endpoint import Endpoint, NameFilterMode, VersionMode
from rhino_health.lib.utils import rhino_error_wrapper


class AIModelEndpoints(Endpoint):
    """
    @autoapi True

    Rhino SDK LTS supported endpoints
    """

    @property
    def aimodel_data_class(self):
        """
        @autoapi False
        """
        return AIModel

    @rhino_error_wrapper
    def get_aimodel(self, aimodel_uid: str):
        """
        Returns a AIModel dataclass

        Parameters
        ----------
        aimodel_uid: str
            UID for the aimodel

        Returns
        -------
        aimodel: AIModel
            AIModel dataclass

        Examples
        --------
        >>> session.aimodel.get_aimodel(my_aimodel_uid)
        AIModel()
        """
        result = self.session.get(f"/aimodels/{aimodel_uid}")
        return result.to_dataclass(self.aimodel_data_class)

    @rhino_error_wrapper
    def get_aimodel_by_name(
        self, name, version=VersionMode.LATEST, project_uid=None
    ) -> Optional[AIModel]:
        """
        Returns the latest or a specific AIModel dataclass

        .. warning:: VersionMode.ALL will return the same as VersionMode.LATEST

        Parameters
        ----------
        name: str
            Full name for the AIModel
        version: Optional[Union[int, VersionMode]]
            Version of the AIModel, latest by default, for an earlier version pass in an integer
        project_uid: Optional[str]
            Project UID to search under

        Returns
        -------
        aimodel: Optional[AIModel]
            AIModel with the name or None if not found

        Examples
        --------
        >>> session.aimodel.get_aimodel_by_name("My AIModel")
        AIModel(name="My AIModel")
        """
        if version == VersionMode.ALL:
            warn(
                "VersionMode.ALL behaves the same as VersionMode.LATEST for get_aimodel_by_name(), did you mean to use search_for_aimodels_by_name()?",
                RuntimeWarning,
            )
        results = self.search_for_aimodels_by_name(name, version, project_uid, NameFilterMode.EXACT)
        return max(results, key=lambda x: arrow.get(x.created_at)) if results else None

    def search_for_aimodels_by_name(
        self,
        name,
        version: Optional[Union[int, VersionMode]] = VersionMode.LATEST,
        project_uid: Optional[str] = None,
        name_filter_mode: Optional[NameFilterMode] = NameFilterMode.CONTAINS,
    ):
        """
        Returns AIModel dataclasses

        Parameters
        ----------
        name: str
            Full or partial name for the AIModel
        version: Optional[Union[int, VersionMode]]
            Version of the AIModel, latest by default
        project_uid: Optional[str]
            Project UID to search under
        name_filter_mode: Optional[NameFilterMode]
            Only return results with the specified filter mode. By default uses CONTAINS

        Returns
        -------
        aimodels: List[AIModel]
            AIModel dataclasses that match the name

        Examples
        --------
        >>> session.aimodel.search_for_aimodels_by_name("My AIModel")
        [AIModel(name="My AIModel)]

        See Also
        --------
        rhino_health.lib.endpoints.endpoint.FilterMode : Different modes to filter by
        rhino_health.lib.endpoints.endpoint.VersionMode : Which version to return
        """
        query_params = self._get_filter_query_params(
            {"name": name, "object_version": version, "project_uid": project_uid},
            name_filter_mode=name_filter_mode,
        )
        results = self.session.get("/aimodels", params=query_params)
        return results.to_dataclasses(self.aimodel_data_class)

    @rhino_error_wrapper
    def create_aimodel(
        self, aimodel: AIModelCreateInput, return_existing=True, add_version_if_exists=False
    ):
        """
        Returns a AIModel dataclass

        Parameters
        ----------
        aimodel: AIModelCreateInput
            AIModelCreateInput data class
        return_existing: bool
            If an AIModel with the name already exists, return it instead of creating one.
            Takes precedence over add_version_if_exists
        add_version_if_exists
            If an AIModel with the name already exists, create a new version.

        Returns
        -------
        aimodel: AIModel
            AIModel dataclass

        Examples
        --------
        >>> session.aimodel.create_aimodel(create_aimodel_input)
        AIModel()
        """
        if return_existing or add_version_if_exists:
            try:
                existing_aimodel = self.search_for_aimodels_by_name(
                    aimodel.name,
                    project_uid=aimodel.project_uid,
                    name_filter_mode=NameFilterMode.EXACT,
                )[0]
                if return_existing:
                    return existing_aimodel
                else:
                    aimodel.base_version_uid = (
                        existing_aimodel.base_version_uid or existing_aimodel.uid
                    )
                    aimodel.__fields_set__.discard("version")
            except Exception:
                # If no existing AI Model exists do nothing
                pass
        result = self.session.post(
            f"/aimodels",
            data=aimodel.dict(by_alias=True, exclude_unset=True),
            adapter_kwargs={"data_as_json": True},
        )
        return result.to_dataclass(self.aimodel_data_class)

    @rhino_error_wrapper
    def run_aimodel(
        self, aimodel: Union[AIModelRunInput, AIModelMultiCohortInput]
    ) -> Union[AIModelRunSyncResponse, AIModelRunAsyncResponse]:
        """
        @autoapi True
        Returns a model_action_uid

        .. warning:: This feature is under development and the return response may change

        Parameters
        ----------
        aimodel: Union[AIModelRunInput, AIModelMultiCohortInput]
            AIModelRunInput or AIModelMultiCohortInput data class

        Returns
        -------
        model_response: Union[AIModelRunSyncResponse, AIModelRunAsyncResponse]
            Response dataclass depending on if the request was run synchronously

        Examples
        --------
        >>> session.aimodel.run_aimodel(run_aimodel_input)
        AIModelRunSyncResponse()

        See Also
        --------
        rhino_health.lib.endpoints.aimodel.aimodel_dataclass.AIModelRunSyncResponse : AIModelRunSyncResponse Dataclass
        rhino_health.lib.endpoints.aimodel.aimodel_dataclass.AIModelRunAsyncResponse : AIModelRunAsyncResponse Dataclass
        """
        output_dataclass = AIModelRunSyncResponse if aimodel.sync else AIModelRunAsyncResponse
        return self.session.post(
            f"/aimodels/{aimodel.aimodel_uid}/run",
            data=aimodel.dict(by_alias=True, exclude_unset=True),
            adapter_kwargs={"data_as_json": True},
        ).to_dataclass(output_dataclass)

    @rhino_error_wrapper
    def train_aimodel(self, aimodel: AIModelTrainInput):
        """
        @autoapi True
        Returns a dict {status, d}

        .. warning:: This feature is under development and the return response may change

        Parameters
        ----------
        aimodel: AIModelTrainInput
            AIModelTrainInput data class

        Returns
        -------
        model_action_uid: str

        Examples
        --------
        >>> session.aimodel.train_aimodel(run_nvflare_aimodel_input)
        AIModelNVFlareAsyncResponse()

        See Also
        --------
        rhino_health.lib.endpoints.aimodel.aimodel_dataclass.AIModelTrainAsyncResponse : AIModelTrainAsyncResponse Dataclass
        """
        return self.session.post(
            f"/aimodels/{aimodel.aimodel_uid}/train",
            data=aimodel.dict(by_alias=True, exclude_unset=True),
            adapter_kwargs={"data_as_json": True},
        ).to_dataclass(AIModelTrainAsyncResponse)
