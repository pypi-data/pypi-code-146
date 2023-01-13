from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, List, Mapping, Optional, Protocol, Sequence, Union

import pandas as pd
from pydantic import BaseModel

from chalk.features import DataFrame, Feature, Features, FeatureWrapper

if TYPE_CHECKING:
    import polars as pl


class OnlineQueryContext(BaseModel):
    # The environment under which to run the resolvers.
    # API tokens can be scoped to an # environment.
    # If no environment is specified in the query,
    # but the token supports only a single environment,
    # then that environment will be taken as the scope
    # for executing the request.
    environment: Optional[str] = None

    # The tags used to scope the resolvers.
    # More information at https://docs.chalk.ai/docs/resolver-tags
    tags: Optional[List[str]] = None


class OfflineQueryContext(BaseModel):
    # The environment under which to run the resolvers.
    # API tokens can be scoped to an # environment.
    # If no environment is specified in the query,
    # but the token supports only a single environment,
    # then that environment will be taken as the scope
    # for executing the request.
    environment: Optional[str] = None


class ErrorCode(str, Enum):
    # The query contained features that do not exist.
    PARSE_FAILED = "PARSE_FAILED"

    # A resolver was required as part of running the dependency
    # graph that could not be found.
    RESOLVER_NOT_FOUND = "RESOLVER_NOT_FOUND"

    # The query is invalid. All supplied features need to be
    # rooted in the same top-level entity.
    INVALID_QUERY = "INVALID_QUERY"

    # A feature value did not match the expected schema
    # (eg. `incompatible type "int"; expected "str"`)
    VALIDATION_FAILED = "VALIDATION_FAILED"

    # The resolver for a feature errored.
    RESOLVER_FAILED = "RESOLVER_FAILED"

    # A crash in a resolver that was to produce an input for
    # the resolver crashed, and so the resolver could not run
    # crashed, and so the resolver could not run.
    UPSTREAM_FAILED = "UPSTREAM_FAILED"

    # The request was submitted with an invalid authentication header.
    UNAUTHENTICATED = "UNAUTHENTICATED"

    # An unspecified error occurred.
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"


class ErrorCodeCategory(str, Enum):

    # Request errors are raised before execution of your
    # resolver code. They may occur due to invalid feature
    # names in the input or a request that cannot be satisfied
    # by the resolvers you have defined.
    REQUEST = "REQUEST"

    # Field errors are raised while running a feature resolver
    # for a particular field. For this type of error, you’ll
    # find a feature and resolver attribute in the error type.
    # When a feature resolver crashes, you will receive null
    # value in the response. To differentiate from a resolver
    # returning a null value and a failure in the resolver,
    # you need to check the error schema.
    FIELD = "FIELD"

    # Network errors are thrown outside your resolvers.
    # For example, your request was unauthenticated,
    # connection failed, or an error occurred within Chalk.
    NETWORK = "NETWORK"


class ChalkException(BaseModel):
    # The name of the class of the exception.
    kind: str

    # The message taken from the exception.
    message: str

    # The stacktrace produced by the code.
    stacktrace: str


class ChalkError(BaseModel):
    # The type of the error
    code: ErrorCode

    # The category of the error, given in the type field for the error codes.
    # This will be one of "REQUEST", "NETWORK", and "FIELD".
    category: ErrorCodeCategory

    # A readable description of the error message.
    message: str

    # The exception that caused the failure, if applicable.
    exception: Optional[ChalkException]

    # The fully qualified name of the failing feature, eg.user.identity.has_voip_phone.
    feature: Optional[str]

    # The fully qualified name of the failing resolver, eg.my.project.get_fraud_score.
    resolver: Optional[str]


class FeatureResult(BaseModel):
    # The name of the feature requested, eg.user.identity.has_voip_phone.
    field: str

    # The value of the requested feature.
    # If an error was encountered in resolving this feature,
    # this field will be empty.
    value: Any

    # The error code encountered in resolving this feature.
    # If no error occurred, this field is empty.
    error: Optional[ChalkError]

    # The time at which this feature was computed.
    # This value could be significantly in the past if you're using caching.
    ts: datetime


class OnlineQueryResponse(Protocol):
    # The output features and any query metadata
    data: List[FeatureResult]

    # Errors encountered while running the resolvers.
    # If no errors were encountered, this field is empty.
    errors: Optional[List[ChalkError]]

    def get_feature(self, feature: Any) -> Optional[FeatureResult]:
        """
        A convenience method for accessing feature result from the data response

        :param feature: The feature or its string representation
        :return: The FeatureResult for the feature, if it exists
        """
        ...

    def get_feature_value(self, feature: Any) -> Optional[Any]:
        """
        A convenience method for accessing feature values from the data response

        :param feature: The feature or its string representation
        :return: The value of the feature
        """
        ...


class ResolverRunStatus(str, Enum):
    RECEIVED = "received"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class ResolverRunResponse(BaseModel):
    id: str
    status: ResolverRunStatus


class WhoAmIResponse(BaseModel):
    user: str


class ChalkBaseException(Exception):
    ...


class ChalkAPIClientProtocol(Protocol):
    def trigger_resolver_run(self, resolver_fqn: str, deployment_id: Optional[str] = None) -> ResolverRunResponse:
        """
        Triggers a resolver to run.
        See https://docs.chalk.ai/docs/runs for more information.

        :param resolver_fqn: The fully qualified name of the resolver to trigger.
        :param deployment_id: Deployment ID.

        :return: Status of the resolver run and the run ID.
        """
        ...

    def get_run_status(self, run_id: str) -> ResolverRunResponse:
        """
        Retrieves the status of a resolver run.
        See https://docs.chalk.ai/docs/runs for more information.

        :param run_id: ID of the resolver run to check.

        :return: Status of the resolver run and the run ID.
        """
        ...

    def whoami(self) -> WhoAmIResponse:
        """
        Checks the identity of your client.
        Useful as a sanity test of your configuration.

        :return: the identity of your client
        """
        ...

    def query(
        self,
        input: Mapping[Union[str, Feature, FeatureWrapper, Any], Any],
        output: Sequence[Union[str, Feature, FeatureWrapper, Any]],
        staleness: Optional[Mapping[Union[str, Feature, FeatureWrapper, Any], str]] = None,
        context: Optional[OnlineQueryContext] = None,
        preview_deployment_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
    ) -> OnlineQueryResponse:
        """
        Compute features values using online resolvers.
        See https://docs.chalk.ai/docs/query-basics for more information.

        :param input: The features for which there are known values, mapped to those values.
        :param output: Outputs are the features that you'd like to compute from the inputs.
        :param staleness: Maximum staleness overrides for any output features or intermediate features.
                          See https://docs.chalk.ai/docs/query-caching for more information.
        :param context: The context object controls the environment and tags
                        under which a request should execute resolvers.
        :param preview_deployment_id: If specified, Chalk will route your request to the relevant preview
                                      deployment
        :param query_name: The name for class of query you're making, for example, "loan_application_model".
        :param correlation_id: A globally unique ID for the query, used alongside logs and
                               available in web interfaces. If None, a correlation ID will be
                               generated for you and returned on the response.
        :param meta: Arbitrary key:value pairs to associate with a query.

        :return: The outputs features and any query metadata, plus errors encountered while
        running the resolvers.
        """
        ...

    def upload_features(
        self,
        input: Mapping[Union[str, Feature, FeatureWrapper, Any], Any],
        context: Optional[OnlineQueryContext] = None,
        preview_deployment_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
    ) -> Optional[List[ChalkError]]:
        """
        Upload data to Chalk for use in offline resolvers or to prime a cache.

        :param input: The features for which there are known values, mapped to those values.
        :param context: The context object controls the environment and tags
                        under which a request should execute resolvers.
        :param preview_deployment_id: If specified, Chalk will route your request to the relevant preview
                                      deployment
        :param correlation_id: A globally unique ID for this operation, used alongside logs and
                               available in web interfaces. If None, a correlation ID will be
                               generated for you and returned on the response.
        :param query_name: Optionally associate this upload with a query name. See `.query` for more information.
        :param meta: Arbitrary key:value pairs to associate with a query.

        :return: The outputs features and any query metadata, plus errors encountered while
        running the resolvers.
        """
        ...

    def get_training_dataframe(
        self,
        input: Union[
            Mapping[Union[str, Feature], Sequence[Any]],
            pd.DataFrame,
            pl.DataFrame,
            DataFrame,
        ],
        input_times: Union[Sequence[datetime], datetime, None] = None,
        output: Sequence[Union[str, Feature, FeatureWrapper, Any]] = (),
        required_output: Sequence[Union[str, Feature, FeatureWrapper, Any]] = (),
        output_id: bool = True,
        output_ts: bool = True,
        context: Optional[OfflineQueryContext] = None,
        dataset: Optional[str] = None,
        branch: Optional[str] = None,
        max_samples: Optional[int] = None,
    ) -> pd.DataFrame:
        """
        Compute feature values from the offline store.
        See https://docs.chalk.ai/docs/training-client for more information.

        :param input: The features for which there are known values.
                      It can be a mapping of features to a list of values for each feature,
                      or an existing dataframe.
                      Each element in the dataframe or list of values represents an observation in line
                      with the timestamp in `input_times`.
        :param input_times: A list of the times of the observations from `input`.
        :param output: The features that you'd like to sample, if they exist.
                       If an output feature was never computed for a sample (row) in the resulting DataFrame,
                       its value will be ``null``.
        :param required_output: The features that you'd like to sample and must exist in each resulting row.
                                Rows where a ``required_output`` was never stored in the offline store will be
                                skipped. This differs from specifying the feature in ``output``, where instead
                                the row would be included, but the feature value would be ``null``.
        :param output_id: Whether to return the primary key feature in a column named ``__chalk__.__id__`` in the
                          resulting DataFrame.
        :param output_ts: Whether to return the timestamp feature in a column named ``__chalk__.CHALK_TS`` in the
                          resulting DataFrame.
        :param context: The environment under which you'd like to query your data.
        :param dataset: A unique name that if provided will be used to generate and save a dataset
                        constructed from the list of features computed from the inputs
        :param max_samples: The maximum number of samples to include in the dataframe. If not specified, then
                            all samples will be returned.
        :return: A dataframe with columns equal to the names of the features in output,
                 and values representing the value of the observation for each input time.
                 The output maintains the ordering from `input`
        """
        ...

    def sample(
        self,
        output: Sequence[Union[str, Feature, FeatureWrapper, Any]] = (),
        required_output: Sequence[Union[str, Feature, FeatureWrapper, Any]] = (),
        output_id: bool = True,
        output_ts: bool = True,
        max_samples: Optional[int] = None,
        dataset: Optional[str] = None,
        branch: Optional[str] = None,
        context: Optional[OfflineQueryContext] = None,
    ) -> pd.DataFrame:
        """
        Get the most recent feature values from the offline store.
        See https://docs.chalk.ai/docs/training-client for more information.

        :param output: The features that you'd like to sample, if they exist.
                       If an output feature was never computed for a sample (row) in the resulting DataFrame,
                       its value will be ``null``.
        :param required_output: The features that you'd like to sample and must exist in each resulting row.
                                Rows where a ``required_output`` was never stored in the offline store will be
                                skipped. This differs from specifying the feature in ``output``, where instead
                                the row would be included, but the feature value would be ``null``.
        :param output_id: Whether to return the primary key feature in a column named ``__chalk__.__id__`` in the
                          resulting DataFrame.
        :param output_ts: Whether to return the timestamp feature in a column named ``__chalk__.CHALK_TS`` in the
                          resulting DataFrame.
        :param max_samples: The maximum number of rows to return.
        :param context: The environment under which you'd like to query your data.

        :return: A pandas dataframe with columns equal to the names of the features in output,
                 and values representing the value of the most recent observation.

        """
        ...
