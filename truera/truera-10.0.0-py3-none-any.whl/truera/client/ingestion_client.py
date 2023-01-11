from datetime import datetime
import logging
import os
from time import sleep
from typing import Mapping, Optional, Sequence, Union
from urllib.parse import urlparse

import pandas as pd

from truera.client.client_utils import DataOperationFailedError
from truera.client.client_utils import DataOperationPendingError
from truera.client.client_utils import EXPLANATION_ALGORITHM_TYPE_TO_STR
from truera.client.client_utils import infer_format
from truera.client.client_utils import TextExtractorParams
from truera.client.client_utils import wait_for_status
from truera.client.data_source_utils import get_column_details_for_data_source
from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.http_communicator import \
    AlreadyExistsError
from truera.client.services.artifact_interaction_client import \
    ArtifactInteractionClient
from truera.client.services.artifact_interaction_client import \
    CreateDataSplitColumnSpec
from truera.client.services.artifact_interaction_client import \
    ModelInfoForCache
from truera.client.services.artifact_interaction_client import OutputSpec
from truera.client.services.artifact_interaction_client import OutputSplitInfo
from truera.client.services.artifact_interaction_client import \
    RowsetIdentifierInfo
from truera.client.services.artifact_repo_client_factory import get_ar_client
from truera.client.services.configuration_service_client import \
    ConfigurationServiceClient
from truera.client.services.data_service_client import DataServiceClient
from truera.client.util import workspace_validation_utils
from truera.protobuf.public.data_service.data_service_messages_pb2 import \
    MATERIALIZE_STATUS_RUNNING  # pylint: disable=no-name-in-module
from truera.protobuf.public.data_service.data_service_messages_pb2 import \
    MATERIALIZE_STATUS_SUCCEDED  # pylint: disable=no-name-in-module
from truera.protobuf.public.util import split_mode_pb2 as sm_pb
from truera.utils.datetime_util import datetime_helper


class Credential(object):

    def __init__(self, name, id, *, projects_with_access=[]) -> None:
        super().__init__()
        self.name = name
        self.id = id
        self.projects_with_access = projects_with_access


class Table(object):
    WAIT_BEFORE_RETRY_DURATION_IN_SEC = 0.5

    def __init__(
        self,
        rowset_id: str,
        ds_name: str,
        project_name: str,
        project_id: str,
        default_score_type: str,
        data_collection_name: str,
        ai_client: ArtifactInteractionClient,
        data_service_client: DataServiceClient,
        cs_client: ConfigurationServiceClient,
        rowset_lineage=[],
        filter_expression: str = None,
        logger: logging.Logger = None
    ) -> None:
        self._rowset_id = rowset_id
        self._ds_name = ds_name
        self._ai_client = ai_client
        self._project_name = project_name
        self._default_score_type = default_score_type
        self._data_collection_name = data_collection_name
        self._project_id = project_id
        self._data_service_client = data_service_client
        self._cs_client = cs_client
        self._data_collection_id = self._ai_client.get_data_collection_id(
            self._project_id, self._data_collection_name
        )
        self._rowset_lineage = rowset_lineage
        self._filter_expression = filter_expression
        self._logger = logger or logging.getLogger(__name__)

    def filter(self, expression: str):
        """[Alpha] Filter a table by providing a boolean expression.

        Args:
            expression (str): The expression to filter the table. Simple SQL expressions are supported:
                    `=`  : filters for equality, ex: amount = 1000
                    `!=` : filters for inequality, ex: amount != 1000
                    `<`  : filters for less-than, ex: amount < 1000
                    `<=` : filters for less-than-or-equal, ex: amount <= 1000
                    `>`  : filters for greater-than, ex: amount > 1000
                    `>=` : filters for great-than-or-equal, ex: amount >= 1000
                    `NOT`: filters records if the inner condition is not true, ex: NOT(amount >= 1000)
                    `AND`: filters records if both the conditions are true, ex: (amount >= 1000) AND (state = 'WA')
                    `OR` : filters records if any of the two conditions is true, ex: (amount >= 1000) OR (state = 'WA')
                String literals should be within quotes (''), numeric literals should not have quotes ('').
                Left side of a binary expression should be a column name (without quotes), right side of an expression should be a literal.
                For example, (amount < salary) is not a valid expression, as both left and right side of the expression are column-names.

        Raises:

            ValueError: Raised if provided expression is `None` or empty.

        Returns:
            Table: Returns a table which points to the filtered rows.
        """
        if not expression:
            raise ValueError("Please provide a filter expression.")
        _, new_rowset_id = self._ai_client.add_filter_to_rowset(
            self._project_id, self._rowset_id, self._ds_name, expression
        )
        return self._create_derived_rowset(new_rowset_id, expression)

    def get_sample_rows(
        self,
        count: int = 100,
        *,
        wait: bool = True,
        timeout_seconds: int = 300
    ) -> pd.DataFrame:
        """Get sampled rows from the table.

        Args:
            count (int, optional): The number of rows to sample. Maximum allowed is 2000. Defaults to 100.
            wait (bool, optional): If set to true, the client will wait until timeout to get data from the service. 
                This is useful when the data is still being fetched or filtered. Defaults to True.
            timeout_seconds (int, optional): Timeout used when `wait` is set to True. Defaults to 300.

        Returns:
            pd.DataFrame: Returns a pandas DataFrame containing the sampled rows.
        """
        start_time = datetime.now()
        while (True):
            try:
                return self._data_service_client.get_sample_rows(
                    self._project_id,
                    self._rowset_id,
                    count,
                    as_data_frame=True
                )
            except DataOperationPendingError:
                if wait and (
                    datetime.now() - start_time
                ).seconds <= timeout_seconds:
                    self._logger.debug("Rowset status is pending, retrying...")
                    sleep(Table.WAIT_BEFORE_RETRY_DURATION_IN_SEC)
                    continue
                else:
                    raise

    def get_status(self):
        status, error = self._ai_client.get_rowset_status(
            project_id=self._project_id,
            name=self._ds_name,
            rowset_id=self._rowset_id
        )
        if status in ["OK", "STARTED", "FAILED"]:
            return status, error
        raise RuntimeError("Unexpected status: %s error: %s" % (status, error))

    def _wait_for_materialize_operation(
        self,
        operation_id: str,
        timeout_seconds: int = 300,
        error_on_timeout=False
    ):
        """Wait for materialize_operation to have status OK or timeout to expire.  Possible states: ["PREPARING", "RUNNING", "OK", "FAILED"].

        Args:
            operation_id (str): Materialize operation id to wait on.
            timeout_seconds (int, optional): Defaults to 300.

        Raises:
            DataOperationFailedError: If status enters FAILED or unknown state.
        """
        status_lambda = lambda: self._ai_client.get_materialize_operation_status(
            self._project_id, operation_id
        )
        status = wait_for_status(
            self._logger,
            status_lambda=status_lambda,
            success_state="OK",
            running_states=["PREPARING", "RUNNING"],
            failed_state="FAILED",
            timeout_seconds=timeout_seconds,
            error_on_timeout=error_on_timeout,
            wait_duration_in_seconds=Table.WAIT_BEFORE_RETRY_DURATION_IN_SEC
        )
        return {"operation_id": operation_id, "status": status}

    def add_data_split(
        self,
        data_split_name: str,
        data_split_type: str,
        label_col_name: Optional[str] = None,
        id_col_name: Optional[str] = None,
        sample_count: int = 5000,
        sample_kind: str = "random",
        *,
        seed: int = None,
        prediction_col_name: Optional[str] = None,
        pre_data_additional_skip_cols: Optional[Sequence[str]] = None,
        model_name: Optional[str] = None,
        wait: bool = True,
        timeout_seconds: int = 300,
        timestamp_col_name: str = None,
        score_type: Optional[str] = None,
        **kwargs
    ) -> Mapping[str, str]:
        """Ingest the `Table` as a split in TruEra to use in analytics.

        Args:
            data_split_name (str): Name of the data split.
            data_split_type (str): Type of the data split, options are ['all', 'train', 'test', 'validate', 'oot', 'custom']
            label_col_name (str): Name of the label/ground truth/target column in the table.
            sample_count (int, optional): Maximum rows to use when creating the split. Defaults to 5000.
            sample_kind (str, optional): Specifies the strategy to use while sub-sampling the rows. Defaults to "random".
            wait (bool, optional): Whether to wait for the TruEra service to complete creating the data split. Defaults to True.
            timeout_seconds (int, optional): Timeout used when `wait` is set to True. Defaults to 300.
        
        Returns:
            Mapping[str, str]: Returns a dictionary with `data_split_name`, `operation_id` and `status` of the operation.
        """
        rowset_identifier = RowsetIdentifierInfo(
            self._rowset_id, None, self._project_id
        )
        output_split_info = OutputSplitInfo(
            self._project_id, self._data_collection_id, data_split_name,
            data_split_type,
            datetime_helper.create_datetime_str(
                kwargs.get("split_time_range_begin")
            ),
            datetime_helper.create_datetime_str(
                kwargs.get("split_time_range_end")
            )
        )
        if model_name:
            score_type = workspace_validation_utils.get_score_type_from_default(
                score_type, self._default_score_type
            )
        model_info_for_cache = ModelInfoForCache(
            self._project_id, model_name, score_type
        )
        create_split_col_info = CreateDataSplitColumnSpec(
            label_col_name, id_col_name,
            prediction_col_name, pre_data_additional_skip_cols,
            kwargs.get("column_spec_file"), False, timestamp_col_name
        )
        output_spec = OutputSpec(sample_count, sample_kind, seed)
        operation_id = self._ai_client.create_data_split_from_data_source(
            rowset_identifier, output_split_info, model_info_for_cache,
            create_split_col_info, output_spec,
            kwargs.get("split_mode", sm_pb.SplitMode.SPLIT_MODE_DATA_REQUIRED)
        )

        return self._wrap_materialize_wait_calls(
            operation_id, timeout_seconds, data_split_name, wait
        )

    def append_to_data_split(
        self,
        data_split_name: str,
        id_col_name: str,
        *,
        sample_count=5000,
        sample_kind: str = "random",
        seed: int = None,
        label_col_name: Optional[str] = None,
        prediction_col_name: Optional[str] = None,
        wait: bool = True,
        timeout_seconds: int = 300,
        timestamp_col_name: Optional[str] = None,
        model_name: Optional[str] = None,
        score_type: Optional[str] = None,
        **kwargs
    ) -> Mapping[str, str]:
        """Ingest the `Table` into an existing split in TruEra to use in analytics. All columns of the data frame will be ingested into pre_data except for label / prediction columns if specified. 

        Args:
            data_split_name (str): Name of the data split.
            id_col_name (str): Name of the column to use for unique ID.
            sample_count (int, optional): Maximum rows to use when creating the split. Defaults to 5000.
            sample_kind (str, optional): Specifies the strategy to use while sub-sampling the rows. Options are "random" and "first". It is not recommended to use "first" as it may result in a non-uniform sampling. Defaults to "random".
            label_col_name (str, optional): Name of the label/ground truth/target column in the table.
            prediction_col_name (str, optional): Name of the prediction column in the table.
            timestamp_col_name (str, optional): Name of the timestamp column (if using).
            seed (int, optional): Seed for reproducing the same ingestion - defaults to a random seed.
            wait (bool, optional): Whether to wait for the TruEra service to complete creating the data split. Defaults to True.
            timeout_seconds (int, optional): Timeout used when `wait` is set to True. Defaults to 300.
        
        Returns:
            Mapping[str, str]: Returns a dictionary with `data_split_name`, `operation_id` and `status` of the operation.
        """
        pre_skip_columns = [
            v for v in [label_col_name, prediction_col_name] if v is not None
        ]

        model_info_for_cache = None
        if model_name:
            score_type = workspace_validation_utils.get_score_type_from_default(
                score_type, self._default_score_type
            )
            model_info_for_cache = ModelInfoForCache(
                self._project_id, model_name, score_type
            )

        operation_id = self._ai_client.ingest_delayed(
            self._project_name,
            None,
            self._rowset_id,
            self._data_collection_name,
            data_split_name,
            seed=seed,
            approx_row_count=sample_count,
            sample_strategy=sample_kind,
            id_column=id_col_name,
            timestamp_column=timestamp_col_name,
            label_column=label_col_name,
            prediction_column=prediction_col_name,
            pre_skip_columns=pre_skip_columns,
            model_info_for_cache=model_info_for_cache
        )
        return self._wrap_materialize_wait_calls(
            operation_id, timeout_seconds, data_split_name, wait
        )

    def _wrap_materialize_wait_calls(
        self, operation_id, timeout_seconds, data_split_name, wait
    ):
        status, error = self._ai_client.get_materialize_operation_status(
            self._project_id, operation_id
        )
        result = {
            "data_split_name": data_split_name,
            "operation_id": operation_id,
            "status": status
        }
        if error or status == "FAILED":
            raise DataOperationFailedError(
                "Materialize operation failed. Cause: " + error
            )
        elif wait:
            result = self._wait_for_materialize_operation(
                operation_id, timeout_seconds
            )
            result["data_split_name"] = data_split_name

        assert status in [
            "PREPARING", "RUNNING", "OK"
        ], "Unexpected status: " + status
        return result

    def _get_background_split_id(
        self, background_split_name: Optional[str]
    ) -> str:
        if background_split_name:
            return self._ai_client.get_split_metadata(
                self._project_name, self._data_collection_name,
                background_split_name
            )["id"]
        else:
            return self._cs_client.get_base_split(
                self._project_id,
                self._data_collection_id,
                infer_base_split_if_not_set=True
            )

    def _add_delayed(
        self,
        existing_split_name: str,
        id_col_name: str,
        label_col_name: Optional[str] = None,
        prediction_col_name: Optional[str] = None,
        feature_influence_col_names: Optional[Sequence[str]] = None,
        extras_col_names: Optional[Sequence[str]] = None,
        sample_count: int = 5000,
        sample_kind: str = "random",
        *,
        timestamp_col_name: Optional[str] = None,
        model_name: Optional[str] = None,
        score_type: Optional[str] = None,
        seed: Optional[int] = None,
        wait: bool = True,
        timeout_seconds: int = 300,
        background_split_name: Optional[str] = None,
        influence_type: Optional[str] = None,
        **kwargs
    ):
        model_cache_info = None
        background_split_id = None
        if model_name:
            model_cache_info = ModelInfoForCache(
                self._project_id, model_name, score_type
            )
            if feature_influence_col_names:
                background_split_id = self._get_background_split_id(
                    background_split_name
                )
        operation_id = self._ai_client.ingest_delayed(
            project_name=self._project_name,
            data_source_name=None,
            rowset_id=self._rowset_id,
            data_collection_name=self._data_collection_name,
            existing_split_name=existing_split_name,
            label_column=label_col_name,
            prediction_column=prediction_col_name,
            timestamp_column=timestamp_col_name,
            extra_columns=extras_col_names,
            id_column=id_col_name,
            model_info_for_cache=model_cache_info,
            approx_row_count=sample_count,
            seed=seed,
            sample_strategy=sample_kind,
            feature_influence_columns=feature_influence_col_names,
            background_split_id=background_split_id,
            influence_type=influence_type
        )
        status, error = self._ai_client.get_materialize_operation_status(
            self._project_id, operation_id
        )
        result = {
            "data_split_name": existing_split_name,
            "operation_id": operation_id,
            "status": status
        }
        if error or status == "FAILED":
            raise DataOperationFailedError(
                "Materialize operation failed. Cause: " + error
            )
        elif wait:
            result = self._wait_for_materialize_operation(
                operation_id, timeout_seconds
            )
            result["data_split_name"] = existing_split_name

        assert status in [
            "PREPARING", "RUNNING", "OK"
        ], "Unexpected status: " + status
        return result

    def add_labels(
        self,
        data_split_name: str,
        label_col_name: str,
        id_col_name: str,
        sample_count: int = 5000,
        sample_kind: str = "random",
        *,
        timestamp_col_name: Optional[str] = None,
        seed: Optional[int] = None,
        wait: bool = True,
        timeout_seconds: int = 300,
        **kwargs
    ) -> Mapping[str, str]:
        """Upload labels from `Table` to an existing split in TruEra.

        Args:
            data_split_name: Name of the existing data split.
            label_col_name: Name of the label/ground truth/target column in the table.
            id_col_name: Name of the id column used to match labels with the corresponding data points.
            sample_count: Maximum rows to use when creating the split. Defaults to 5000.
            sample_kind: Specifies the strategy to use while sub-sampling the rows. One of ["random", "first"].
            timestamp_col_name: Name of the timestamp column of the labels.
            wait: Whether to wait for the TruEra service to complete creating the data split. Defaults to True.
            timeout_seconds: Timeout used when `wait` is set to True. Defaults to 300.

        Returns:
            Mapping[str, str]: Returns a dictionary with `data_split_name`, `operation_id` and `status` of the operation.
        """
        return self._add_delayed(
            existing_split_name=data_split_name,
            id_col_name=id_col_name,
            label_col_name=label_col_name,
            sample_count=sample_count,
            sample_kind=sample_kind,
            timestamp_col_name=timestamp_col_name,
            seed=seed,
            wait=wait,
            timeout_seconds=timeout_seconds,
            **kwargs,
        )

    def add_predictions(
        self,
        data_split_name: str,
        prediction_col_name: str,
        id_col_name: str,
        model_name: str,
        *,
        timestamp_col_name: Optional[str] = None,
        score_type: Optional[str] = None,
        wait: bool = True,
        timeout_seconds: int = 300,
        **kwargs
    ) -> Mapping[str, str]:
        """Upload predictions from `Table` to an existing split/model in TruEra.

        Args:
            data_split_name: Name of the existing data split.
            prediction_col_name: Name of the prediction column in the table.
            id_col_name: Name of the id column used to match predictions with the corresponding data points.
            timestamp_col_name: Name of the timestamp column of the predictions.
            score_type: String name of score type (QoI) for prediction column.
            wait: Whether to wait for the TruEra service to complete creating the data split. Defaults to True.
            timeout_seconds: Timeout used when `wait` is set to True. Defaults to 300.

        Returns:
            Mapping[str, str]: Returns a dictionary with `data_split_name`, `operation_id` and `status` of the operation.
        """
        score_type = workspace_validation_utils.get_score_type_from_default(
            score_type, self._default_score_type
        )
        return self._add_delayed(
            existing_split_name=data_split_name,
            id_col_name=id_col_name,
            prediction_col_name=prediction_col_name,
            model_name=model_name,
            score_type=score_type,
            timestamp_col_name=timestamp_col_name,
            wait=wait,
            timeout_seconds=timeout_seconds,
            **kwargs,
        )

    def add_feature_influences(
        self,
        data_split_name: str,
        feature_influence_col_names: Sequence[str],
        id_col_name: str,
        model_name: str,
        *,
        background_split_name: Optional[str] = None,
        timestamp_col_name: Optional[str] = None,
        score_type: Optional[str] = None,
        wait: bool = True,
        timeout_seconds: int = 300,
        influence_type: Optional[str] = None,
        **kwargs
    ) -> Mapping[str, str]:
        """Upload feature influences from `Table` to an existing split/model in TruEra.

        Args:
            data_split_name: Name of the existing data split.
            feature_influence_col_names: Name of the feature influence columns in the table.
            id_col_name: Name of the id column used to match predictions with the corresponding data points.
            model_name: Name of the model for which feature influences are computed.
            background_split_name: Split name that contains the background of feature influence computation. If not provided, defaults to the default background data split of the given data collection.
            timestamp_col_name: Name of the timestamp column of the predictions.
            score_type: String name of score type (QoI) for prediction column.
            wait: Whether to wait for the TruEra service to complete creating the data split. Defaults to True.
            timeout_seconds: Timeout used when `wait` is set to True. Defaults to 300.
            influence_type: String name of feature influence algorithm type

        Returns:
            Mapping[str, str]: Returns a dictionary with `data_split_name`, `operation_id` and `status` of the operation.
        """
        score_type = workspace_validation_utils.get_score_type_from_default(
            score_type, self._default_score_type
        )

        project_influence_type = self._cs_client.get_influence_algorithm_type(
            self._project_id
        )
        influence_type = EXPLANATION_ALGORITHM_TYPE_TO_STR[
            workspace_validation_utils.
            validate_influence_type_str_for_virtual_model_upload(
                influence_type, project_influence_type
            )]
        return self._add_delayed(
            existing_split_name=data_split_name,
            id_col_name=id_col_name,
            feature_influence_col_names=feature_influence_col_names,
            model_name=model_name,
            score_type=score_type,
            timestamp_col_name=timestamp_col_name,
            wait=wait,
            timeout_seconds=timeout_seconds,
            background_split_name=background_split_name,
            influence_type=influence_type,
            **kwargs,
        )

    def add_extra_data(
        self,
        data_split_name: str,
        extras_col_names: Union[str, Sequence[str]],
        id_col_name: str,
        sample_count: int = 5000,
        sample_kind: str = "random",
        *,
        timestamp_col_name: Optional[str] = None,
        seed: Optional[int] = None,
        wait: bool = True,
        timeout_seconds: int = 300,
        **kwargs
    ) -> Mapping[str, str]:
        """Upload extra_data from `Table` to an existing split in TruEra.

        Args:
            data_split_name: Name of the existing data split.
            extras_col_names: Name(s) of the extra data column(s) in the table.
            id_col_name: Name of the id column used to match extra data with the corresponding data points.
            sample_count: Maximum rows to use when creating the split. Defaults to 5000.
            sample_kind: Specifies the strategy to use while sub-sampling the rows. One of ["random", "first"].
            timestamp_col_name: Name of the timestamp column of the extra data.
            wait: Whether to wait for the TruEra service to complete creating the data split. Defaults to True.
            timeout_seconds: Timeout used when `wait` is set to True. Defaults to 300.

        Returns:
            Mapping[str, str]: Returns a dictionary with `data_split_name`, `operation_id` and `status` of the operation.
        """
        return self._add_delayed(
            existing_split_name=data_split_name,
            id_col_name=id_col_name,
            extras_col_names=extras_col_names
            if isinstance(extras_col_names, list) else [extras_col_names],
            timestamp_col_name=timestamp_col_name,
            sample_count=sample_count,
            sample_kind=sample_kind,
            seed=seed,
            wait=wait,
            timeout_seconds=timeout_seconds,
            **kwargs,
        )

    def _create_derived_rowset(self, new_rowset_id, filter_expression):
        return Table(
            new_rowset_id,
            self._ds_name,
            self._project_name,
            self._project_id,
            self._default_score_type,
            self._data_collection_name,
            ai_client=self._ai_client,
            data_service_client=self._data_service_client,
            cs_client=self._cs_client,
            rowset_lineage=[*self._rowset_lineage, self],
            filter_expression=filter_expression,
            logger=self._logger
        )

    def _repr_html_(self):
        try:
            return self.get_sample_rows(timeout_seconds=30)._repr_html_()
        except DataOperationPendingError:
            return """
            <div>
                <strong>Failed to render the rowset as the operation is still in progress.</strong>
                <p>
                This is not a failure, you can still interact with the rowset object.
                </p>
            </div>
            """

    def __repr__(self) -> str:
        lineage = [*self._rowset_lineage, self]
        return str(
            {
                "data_source":
                    self._ds_name,
                "rowset":
                    self._rowset_id,
                "data_collection":
                    self._data_collection_name,
                "project":
                    self._project_name,
                "expression":
                    " AND ".join(
                        [
                            "(%s)" % (r._filter_expression)
                            for r in lineage
                            if r._filter_expression
                        ]
                    )
            }
        )


class IngestionClient(object):
    """Client for ingesting data from a variety of sources into the TruEra product.
    """

    def __init__(
        self,
        project: str,
        default_score_type: str,
        data_collection: str,
        artifact_interaction_client: ArtifactInteractionClient,
        data_service_client: DataServiceClient,
        configuration_service_client: ConfigurationServiceClient,
        logger: Optional[logging.Logger] = None
    ) -> None:
        super().__init__()
        self._project_name = project
        self._default_score_type = default_score_type
        self._data_collection_name = data_collection
        self._ai_client = artifact_interaction_client
        self._project_id = self._ai_client.get_project_id(project)
        self._data_service_client = data_service_client
        self._cs_client = configuration_service_client
        self._logger = logger or logging.getLogger(__name__)

    @classmethod
    def create(
        cls,
        connection_string: str,
        auth_details: AuthDetails,
        project: str,
        default_score_type: str,
        data_collection: str,
        logger=None,
        *,
        verify_cert: Union[bool, str] = True
    ):
        ar_client = get_ar_client(
            connection_string,
            auth_details,
            logger,
            use_http=True,
            verify_cert=verify_cert
        )
        data_service_client = DataServiceClient.create(
            connection_string,
            logger,
            auth_details,
            use_http=True,
            verify_cert=verify_cert
        )
        cs_client = ConfigurationServiceClient(
            connection_string,
            auth_details,
            logger,
            use_http=True,
            verify_cert=verify_cert
        )
        return IngestionClient(
            project, default_score_type, data_collection,
            ArtifactInteractionClient(ar_client, data_service_client, logger),
            data_service_client, cs_client, logger
        )

    def add_credential(
        self, name: str, secret: str, identity: str = None
    ) -> Credential:
        """Add a new credential to TruEra product. The credential is saved in a secure manner and is used 
        to authenticate with the data source to be able to perform various operations (read, filter, sample etc.).

        Args:
            name (str): Friendly name of the credential.
            secret (str): The secret to be stored.  
            identity (str, optional): Identity portion of the secret. Not needed in all cases. Defaults to None.

        Returns:
            Credential: Returns an object with the credential name and id. The secret is not stored in this object.
        """
        id = self._ai_client.add_data_source_cred(
            self._project_id, name, identity, secret
        )
        return Credential(name, id)

    def get_credential(self, name: str) -> dict:
        """Get metadata about a credential in the TruEra product. Response does not contain the credential itself. 

        Args:
            name (str): Friendly name of the credential.

        Returns:
            Dictionary containing metadata describing that credential.
        """
        return self._ai_client.get_credential_metadata(
            credential_id=None, credential_name=name
        )

    def delete_credential(self, name: str) -> None:
        """Delete a credential in the TruEra product.

        Args:
            name (str): Friendly name of the credential.
        """
        self._ai_client.delete_credential(
            credential_id=None, credential_name=name
        )

    def _validate_add_data_source(self, data_source_name: str):
        # Returns whether data_source already exists.
        def rowset_has_name(rowset_metadata):
            return "rowset" in rowset_metadata and "root_data" in rowset_metadata[
                "rowset"] and len(
                    rowset_metadata["rowset"]["root_data"]
                ) > 0 and "name" in rowset_metadata["rowset"]["root_data"][0]

        data_sources = [
            rowset_metadata["rowset"]["root_data"][0]["name"]
            for rowset_metadata in
            self._ai_client.get_all_data_sources_in_project(self._project_id)
            if rowset_has_name(rowset_metadata)
        ]
        if data_source_name in data_sources:
            raise AlreadyExistsError(
                f"Data Source \"{data_source_name}\" already exists!"
            )

    def add_data_source(
        self,
        name: str,
        uri: str,
        credentials: Optional[
            Credential] = None,  # TODO(AB#3679) take cred name as the input
        **kwargs
    ) -> Table:
        """Add a new data source in the system.

        Args:
            name (str): Friendly name of the data source.
            uri (str): URI describing the location of the data source.
                For local files this can be file:///path/to/my/file or /path/to/my/file
                For files stored in Azure Storage Blobs the expected path is wasb://container@account.blob.core.windows.net/blob
                For files stored in S3 Buckets the expected path is s3://bucket-name/file
                For mysql connections the expected path is mysql://database-endpoint.com:port
                For hive connections the expected path is hive2://database-endpoint.com:port
                For jdbc connections the expected path is jdbc:<subscheme>://database-endpoint.com:port
                For bigquery connections, the user is expected to pass a psuedo-uri 'bigquery:'. The connection is embedded in the json service acc key.
            credentials (Credential, optional): Provide the credential object if the data source requires authentication to read from it. Defaults to None.

            **format (str):The format in which the file (local) or blob (AWS S3, Azure WASB etc.) are stored in. Supported formats: CSV and Parquet.
            **column_schema (Union[str, List[Tuple[str, str]]]): For providing a schema that should be respected by the data source. This can be provided in the form of a path to a JSON/YAML file containing the schema, or a list columns each represented as a tuple<name:str, static_data_type:str>
            **first_row_is_header (bool): For text based delimited files (csv, tsv etc.), indicates if the first row provides header information. Defaults to True.
            **column_delimiter (str): For text based delimited files (csv, tsv etc.), provides the delimiter to separate column values. Defaults to ','.
            **quote_character (str): For text based delimited files (csv, tsv etc.), if quotes are used provide the quote character. Defaults to '"'.
            **null_value (str): For text based delimited files (csv, tsv etc.), the string that signifies null value. Defaults to 'null'.
            **empty_value (str): For text based delimited files (csv, tsv etc.), the string that signifies empty value. Defaults to '""'.
            **date_format (str): For text based delimited files (csv, tsv etc.), if any column has date time, provide the format string. Defaults to 'yyyy-MM-dd HH:mm:ssZZ'.
            **account_key (str): For reading from Azure Storage Blob (WASB), provide the account_key to be used to read the blob. Not required if `credential` object is provided.
            **access_key_id (str): For reading from a s3 bucket, provide the access key id to be used to read the blob. Not required if `credential` object is provided or the underlying deployment is in a role with access to the bucket.
            **secret_access_key (str): For reading from a s3 bucket, provide the secret access key to be used to read the blob. Not required if `credential` object is provided or the underlying deployment is in a role with access to the bucket.
            **database_name (str): For reading from MySQL database, provide the database name to use. Required for MySQL data source.
            **table_name (str): For reading from MySQL database, provide the table name to use. Required for MySQL data source.
        Returns:
            Table: Returns a Table object which allows interaction with the attached data.
        """
        self._validate_add_data_source(name)
        parsed = urlparse(uri)
        scheme = parsed.scheme.lower()
        source_is_user_requested = kwargs.get("user_requested", True)
        self._logger.debug("Processing URL scheme %s", scheme)
        columns = get_column_details_for_data_source(
            kwargs.get("column_schema")
        )
        if not scheme or scheme == "file":
            self._logger.info("Did not find a scheme, assuming local file")
            format = kwargs.get("format", None)
            path = parsed.path

            format = infer_format(format or "infer", path)

            if format == "csv":
                text_extractor_params = TextExtractorParams(
                    format, kwargs.get("first_row_is_header"),
                    kwargs.get("column_delimiter"),
                    kwargs.get("quote_character"), kwargs.get("null_value"),
                    kwargs.get("empty_value"), kwargs.get("date_format"),
                    columns
                )
                rowset_id = self._ai_client.upload_data_source_file(
                    self._project_id,
                    path,
                    name,
                    text_extractor_params,
                    user_requested=source_is_user_requested
                )
                return self._create_rowset(rowset_id, name)
            if format == "parquet":
                text_extractor_params = TextExtractorParams(
                    format, None, None, None, None, None, None, columns
                )
                rowset_id = self._ai_client.upload_data_source_file(
                    self._project_id,
                    path,
                    name,
                    text_extractor_params,
                    user_requested=source_is_user_requested
                )
                return self._create_rowset(rowset_id, name)
            assert False, "Format %s is not supported." % format
        elif scheme.startswith("wasb"):
            format = kwargs.get("format", None)
            format = infer_format(format or "infer", uri)
            text_extractor_params = TextExtractorParams(
                format, kwargs.get("first_row_is_header"),
                kwargs.get("column_delimiter"), kwargs.get("quote_character"),
                kwargs.get("null_value"), kwargs.get("empty_value"),
                kwargs.get("date_format"), columns
            )
            account_key = kwargs.get("account_key", None)
            rowset_id = self._ai_client.add_wasb_data_source(
                self._project_id,
                uri,
                account_key,
                credentials.id if credentials else None,
                name,
                text_extractor_params,
                user_requested=source_is_user_requested
            )
            return self._create_rowset(rowset_id, name)
        # urlparse does not parse subschemes in jdbc URLs. It sees jdbc:mysql://server.com:42000 and
        # thinks the scheme is "jdbc" rather than "jdbc:mysql". In this case, we want to fall into
        # this case and re-parse after stripping jdbc off.
        elif scheme.startswith("mysql") or (
            scheme.startswith("jdbc") and "mysql" in uri
        ):
            parsed = urlparse(uri.lstrip("jdbc:"))
            database_name = kwargs.get("database_name")
            table_name = kwargs.get("table_name")
            if not database_name or not table_name:
                raise ValueError(
                    "`database_name` and `table_name` are required parameters for using MySQL datasource."
                )
            self._logger.info(
                "Connecting to MySQL database. URL: %s, database name: %s, table name: %s",
                parsed.netloc, database_name, table_name
            )
            rowset_id = self._ai_client.add_mysql_db_data_source(
                self._project_id,
                parsed.netloc,
                database_name,
                table_name,
                None,
                None,
                credentials.id if credentials else None,
                name,
                user_requested=source_is_user_requested,
                columns=columns
            )
            return self._create_rowset(rowset_id, name)
        elif scheme.startswith("hive2") or (
            scheme.startswith("jdbc") and "hive2" in uri
        ):
            parsed = urlparse(uri.lstrip("jdbc:"))
            database_name = kwargs.get("database_name")
            table_name = kwargs.get("table_name")
            if not database_name or not table_name:
                raise ValueError(
                    "`database_name` and `table_name` are required parameters for using Hive datasource."
                )
            self._logger.info(
                "Connecting to Hive database. URL: %s, database name: %s, table name: %s",
                parsed.netloc, database_name, table_name
            )
            rowset_id = self._ai_client.add_hive_data_source(
                self._project_id,
                parsed.netloc,
                database_name,
                table_name,
                None,
                None,
                credentials.id if credentials else None,
                name,
                user_requested=source_is_user_requested
            )
            return self._create_rowset(rowset_id, name)
        elif scheme.startswith("jdbc"):
            database_name = kwargs.get("database_name")
            table_name = kwargs.get("table_name")
            if not database_name or not table_name:
                raise ValueError(
                    "`database_name` and `table_name` are required parameters for using JDBC datasource."
                )
            self._logger.info(
                "Connecting via JDBC to data source. URL: %s, database name: %s, table name: %s",
                parsed.netloc, database_name, table_name
            )
            rowset_id = self._ai_client.add_jdbc_data_source(
                self._project_id,
                uri,
                database_name,
                table_name,
                None,
                None,
                credentials.id if credentials else None,
                name,
                user_requested=source_is_user_requested,
                columns=columns
            )
            return self._create_rowset(rowset_id, name)
        elif scheme.startswith("s3"):
            format = kwargs.get("format", None)
            format = infer_format(format or "infer", uri)
            text_extractor_params = TextExtractorParams(
                format, kwargs.get("first_row_is_header"),
                kwargs.get("column_delimiter"), kwargs.get("quote_character"),
                kwargs.get("null_value"), kwargs.get("empty_value"),
                kwargs.get("date_format"), columns
            )
            access_key_id = kwargs.get("access_key_id", None)
            access_key = kwargs.get("secret_access_key", None)
            if not access_key_id:
                access_key_id = os.environ.get("AWS_ACCESS_KEY", None)
            if not access_key:
                access_key = os.environ.get("AWS_SECRET_KEY", None)
            rowset_id = self._ai_client.add_s3_bucket_data_source(
                self._project_id,
                uri,
                access_key_id,
                access_key,
                credentials.id if credentials else None,
                name,
                text_extractor_params,
                user_requested=source_is_user_requested
            )
            return self._create_rowset(rowset_id, name)
        elif "bigquery" in uri:
            database_name = kwargs.get("database_name", None)
            table_name = kwargs.get("table_name", None)
            password = kwargs.get("password", None)
            credential_id = kwargs.get("credential_id", None)
            columns = kwargs.get("columns", [])

            rowset_id = self._ai_client.add_bigquery_data_source(
                project_id=self._project_id,
                database_name=database_name,
                table_name=table_name,
                password=password,
                name=name,
                credential_id=credential_id,
                columns=columns
            )
            return self._create_rowset(rowset_id, name)
        # TODO(AB#3825): Add support for other data sources.
        raise NotImplementedError(
            "%s data source is not yet supported." % scheme
        )

    def get_data_source(self, name) -> Table:
        """Get a data source that was already created in the system.

        Args:
            name (str): The friendly name of the data source.

        Returns:
            Table: Returns a Table object which allows interaction with the attached data.
        """
        rowset_id = self._ai_client.get_root_rowset_by_name(
            self._project_id, name
        )
        return self._create_rowset(rowset_id, name)

    def _create_rowset(self, rowset_id, data_source_name):
        return Table(
            rowset_id=rowset_id,
            ds_name=data_source_name,
            project_name=self._project_name,
            project_id=self._project_id,
            default_score_type=self._default_score_type,
            data_collection_name=self._data_collection_name,
            ai_client=self._ai_client,
            data_service_client=self._data_service_client,
            cs_client=self._cs_client,
            rowset_lineage=[],
            filter_expression="",
            logger=self._logger
        )

    def _wait_for_materialize_operation(self, materialize_operation_id: str):

        def status_fn():
            materialize_data_status = self._data_service_client.get_materialize_data_status(
                self._project_id,
                materialize_operation_id=materialize_operation_id
            )
            if materialize_data_status.status == MATERIALIZE_STATUS_SUCCEDED:
                return "SUCCEDED", None
            elif materialize_data_status.status == MATERIALIZE_STATUS_RUNNING:
                return "RUNNING", None,
            else:
                return "FAILED", materialize_data_status.error

        wait_for_status(
            logger=self._logger,
            status_lambda=status_fn,
            success_state="SUCCEDED",
            running_states="RUNNING",
            failed_state="FAILED"
        )
