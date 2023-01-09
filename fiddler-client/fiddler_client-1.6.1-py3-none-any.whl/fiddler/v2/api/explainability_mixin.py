from collections import namedtuple
from typing import List, NamedTuple, Optional, Union

import pandas as pd
from pydantic import BaseModel

from fiddler.libs.http_client import RequestClient
from fiddler.utils import logging
from fiddler.utils.pandas import try_series_retype
from fiddler.v2.utils.exceptions import handle_api_error_response
from fiddler.v2.utils.response_handler import APIResponseHandler

logger = logging.getLogger(__name__)


class DatasetDataSource(BaseModel):
    source_type = 'DATASET'
    dataset_name: str
    source: Optional[str]
    num_samples: Optional[int]


class SqlSliceQueryDataSource(BaseModel):
    source_type = 'SQL_SLICE_QUERY'
    query: str
    num_samples: Optional[int]


class RowDataSource(BaseModel):
    source_type = 'ROW'
    row: dict


class EventIdDataSource(BaseModel):
    source_type = 'EVENT_ID'
    event_id: str
    dataset_name: str


class ExplainabilityMixin:
    client: RequestClient
    organization_name: str

    EXPLAINABILITY_SERVER_VERSION = '>=22.12.0'

    @handle_api_error_response
    def get_feature_importance(
        self,
        model_name: str,
        project_name: str,
        data_source: Union[DatasetDataSource, SqlSliceQueryDataSource],
        num_iterations: Optional[int] = None,
        num_refs: Optional[int] = None,
        ci_level: Optional[float] = None,
        overwrite_cache: bool = False,
    ) -> NamedTuple:
        """
        Get global feature importance for a model over a dataset or a slice
        :param model_name: The unique identifier of the model
        :param project_name: The unique identifier of the model's project
        :param data_source: DataSource for the input dataset to compute feature
            importance on (DatasetDataSource or SqlSliceQueryDataSource)
        :param num_iterations: The maximum number of ablated model inferences
            *per feature*.
        :param num_refs: number of reference points used in the explanation
        :param ci_level: The confidence level (between 0 and 1)
        :param overwrite_cache: Whether to overwrite the cached values or not

        :return: A named tuple with the feature importance results.
        """

        request_body = dict(
            model_name=model_name,
            project_name=project_name,
            organization_name=self.organization_name,
            data_source=data_source.dict(),
            overwrite_cache=overwrite_cache,
        )

        if num_iterations is not None:
            request_body['num_iterations'] = num_iterations

        if num_refs is not None:
            request_body['num_refs'] = num_refs

        if ci_level is not None:
            request_body['ci_level'] = ci_level

        response = self.client.post(
            url='feature-importance',
            data=request_body,
        )

        response_dict = APIResponseHandler(response).get_data()

        return namedtuple('FeatureImportanceResult', response_dict)(**response_dict)

    @handle_api_error_response
    def get_feature_impact(
        self,
        model_name: str,
        project_name: str,
        data_source: Union[DatasetDataSource, SqlSliceQueryDataSource],
        num_iterations: Optional[int] = None,
        num_refs: Optional[int] = None,
        ci_level: Optional[float] = None,
        output_columns: Optional[List[str]] = None,
        min_support: Optional[int] = None,
        overwrite_cache: bool = False,
    ) -> NamedTuple:
        """
        Get global feature impact for a model over a dataset or a slice
        ::param model_name: The unique identifier of the model
        :param project_name: The unique identifier of the model's project
        :param data_source: DataSource for the input dataset to compute feature
            impact on (DatasetDataSource or SqlSliceQueryDataSource)
        :param num_iterations: The maximum number of ablated model inferences
            *per feature*.
        :param num_refs: number of reference points used in the explanation
        :param ci_level: The confidence level (between 0 and 1)
        :param output_columns: Only used for NLP (TEXT inputs) models. Output column
            names to compute feature impact on.
        :param min_support: Only used for NLP (TEXT inputs) models. Specify a minimum
            support (number of times a specific word was present in the sample data)
            to retrieve top words. Default to 15.
        :param overwrite_cache: Whether to overwrite the cached values or not

        :return: A named tuple with the feature impact results.
        """

        request_body = dict(
            model_name=model_name,
            project_name=project_name,
            organization_name=self.organization_name,
            data_source=data_source.dict(),
            overwrite_cache=overwrite_cache,
        )

        if output_columns is not None:
            request_body['output_columns'] = output_columns

        if num_iterations is not None:
            request_body['num_iterations'] = num_iterations

        if num_refs is not None:
            request_body['num_refs'] = num_refs

        if ci_level is not None:
            request_body['ci_level'] = ci_level

        if min_support is not None:
            request_body['min_support'] = min_support

        response = self.client.post(
            url='feature-impact',
            data=request_body,
        )

        response_dict = APIResponseHandler(response).get_data()

        return namedtuple('FeatureImpactResult', response_dict)(**response_dict)

    @handle_api_error_response
    def get_explanation(
        self,
        model_name: str,
        project_name: str,
        input_data_source: Union[RowDataSource, EventIdDataSource],
        ref_data_source: Optional[
            Union[DatasetDataSource, SqlSliceQueryDataSource]
        ] = None,
        explanation_type: Optional[str] = None,
        num_permutations: Optional[int] = None,
        ci_level: Optional[float] = None,
        top_n_class: Optional[int] = None,
    ) -> NamedTuple:
        """
        Get explanation for a single observation.

        :param model_name: The unique identifier of the model
        :param project_name: The unique identifier of the model's project
        :param input_data_source: DataSource for the input data to compute explanation
            on (RowDataSource, EventIdDataSource)
        :param ref_data_source: DataSource for the reference data to compute explanation
            on (DatasetDataSource, SqlSliceQueryDataSource).
            Only used for non-text models and the following methods:
            'SHAP', 'FIDDLER_SHAP', 'PERMUTE', 'MEAN_RESET'
        :param explanation_type: Explanation method name. Could be your custom
            explanation method or one of the following method:
            'SHAP', 'FIDDLER_SHAP', 'IG', 'PERMUTE', 'MEAN_RESET', 'ZERO_RESET'
        :param num_permutations: For Fiddler SHAP, that corresponds to the number of
            coalitions to sample to estimate the Shapley values of each single-reference
             game. For the permutation algorithms, this corresponds to the number
            of permutations from the dataset to use for the computation.
        :param ci_level: The confidence level (between 0 and 1) to use for the
            confidence intervals in Fiddler SHAP. Not used for other methods.
        :param top_n_class: For multiclass classification models only, specifying if
            only the n top classes are computed or all classes (when parameter is None)

        :return: A named tuple with the explanation results.
        """

        request_body = dict(
            model_name=model_name,
            project_name=project_name,
            organization_name=self.organization_name,
            input_data_source=input_data_source.dict(),
            convert_to_gem=False,
        )

        if ref_data_source is not None:
            request_body['ref_data_source'] = ref_data_source.dict()

        if explanation_type is not None:
            request_body['explanation_type'] = explanation_type

        if num_permutations is not None:
            request_body['num_permutations'] = num_permutations

        if ci_level is not None:
            request_body['ci_level'] = ci_level

        if top_n_class is not None:
            request_body['top_n_class'] = top_n_class

        response = self.client.post(
            url='explain',
            data=request_body,
        )

        response_dict = APIResponseHandler(response).get_data()

        return namedtuple('ExplainResult', response_dict)(**response_dict)

    @handle_api_error_response
    def get_fairness(
        self,
        model_name: str,
        project_name: str,
        data_source: Union[DatasetDataSource, SqlSliceQueryDataSource],
        protected_features: List[str],
        positive_outcome: Union[str, int, float, bool],
        score_threshold: Optional[float] = None,
    ) -> NamedTuple:
        """
        Get fairness analysis on a dataset or a slice.

        :param model_name: The unique identifier of the model
        :param project_name: The unique identifier of the model's project
        :param data_source: DataSource for the input dataset to compute
            fairness on (DatasetDataSource or SqlSliceQueryDataSource)
        :param protected_features: list of protected attribute names to compute
            Fairness analysis on
        :param positive_outcome: name of the positive outcome to compute
            Fairness analysis on
        :param score_threshold: Binary threshold value (between 0 and 1). Default to 0.5

        :return: A named tuple with the fairness results.
        """

        request_body = dict(
            model_name=model_name,
            project_name=project_name,
            organization_name=self.organization_name,
            data_source=data_source.dict(),
            protected_features=protected_features,
            positive_outcome=positive_outcome,
        )

        if score_threshold is not None:
            request_body['score_threshold'] = score_threshold

        response = self.client.post(
            url='fairness',
            data=request_body,
        )

        response_dict = APIResponseHandler(response).get_data()

        return namedtuple('FairnessResult', response_dict)(**response_dict)

    @handle_api_error_response
    def run_slice_query(
        self,
        project_name: str,
        query: str,
        columns: Optional[List[str]] = None,
        sample: Optional[bool] = None,
        max_rows: Optional[int] = None,
    ) -> pd.DataFrame:
        """
        Fetches data from Fiddler via a *slice query* (SQL query).

        :param project_name: The unique identifier of the model's project
        :param query: A special SQL query that begins with the keyword 'SELECT'
        :param columns: Allows caller to explicitly specify list of
                        columns to select overriding columns selected in the query.
        :param sample: Whether rows should be sample or not from the database
        :param max_rows: Number of maximum rows to fetch

        :return: Dataframe of the resulted rows
        """

        request_body = dict(
            project_name=project_name,
            organization_name=self.organization_name,
            query=query,
        )

        if sample is not None:
            request_body['sample'] = sample
        if max_rows is not None:
            request_body['max_rows'] = max_rows
        if columns is not None:
            request_body['columns'] = columns

        response = self.client.post(
            url='slice-query/fetch',
            data=request_body,
        )

        response_dict = APIResponseHandler(response).get_data()

        column_names = response_dict['meta']['columns']
        dtype_strings = response_dict['meta']['dtypes']
        df = pd.DataFrame(response_dict['rows'], columns=column_names)
        for column_name, dtype in zip(column_names, dtype_strings):
            df[column_name] = try_series_retype(df[column_name], dtype)

        return df

    @handle_api_error_response
    def get_predictions(
        self,
        model_name: str,
        project_name: str,
        input_df: pd.DataFrame,
        chunk_size: Optional[int] = None,
    ) -> pd.DataFrame:
        """
        Run model on an input dataframe

        :param model_name: The unique identifier of the model
        :param project_name: The unique identifier of the model's project
        :param input_df: Feature dataframe
        :param chunk_size: Chunk size for fetching predictions

        :return: Dataframe of the predictions
        """

        if not isinstance(input_df, pd.DataFrame):
            raise ValueError(
                f'Argument input_df should be a pandas Dataframe. '
                f'Received type {type(input_df)} instead.'
            )

        request_body = dict(
            project_name=project_name,
            organization_name=self.organization_name,
            model_name=model_name,
            data=input_df.to_dict('records'),
        )

        if chunk_size is not None:
            request_body['chunk_size'] = chunk_size

        response = self.client.post(
            url='predict',
            data=request_body,
        )

        response_dict = APIResponseHandler(response).get_data()

        return pd.DataFrame(response_dict['predictions'])
