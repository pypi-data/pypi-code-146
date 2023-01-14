from __future__ import annotations

import collections.abc
import time
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Iterable, List, Mapping, Optional, Sequence, Type, TypeVar, Union
from urllib.parse import urljoin

import pandas as pd
import requests
from pydantic import BaseModel, ValidationError
from requests import HTTPError

from chalk._version import __version__ as chalkpy_version
from chalk.client.client_protocol import (
    ChalkAPIClientProtocol,
    ChalkBaseException,
    ChalkError,
    FeatureResult,
    OfflineQueryContext,
    OnlineQueryContext,
    OnlineQueryResponse,
    ResolverRunResponse,
    WhoAmIResponse,
)
from chalk.client.dataset import DatasetVersion, load_dataset
from chalk.config.auth_config import load_token
from chalk.features import DataFrame, Feature, FeatureWrapper, ensure_feature
from chalk.features.pseudofeatures import CHALK_TS_FEATURE
from chalk.serialization.codec import FEATURE_CODEC
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import polars as pl

_logger = get_logger(__name__)


class _ExchangeCredentialsRequest(BaseModel):
    client_id: str
    client_secret: str
    grant_type: str


class _ExchangeCredentialsResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    # expires_at: datetime
    api_server: str
    primary_environment: Optional[str]
    engines: Optional[Mapping[str, str]] = None


class _OfflineQueryResponse(BaseModel):
    columns: List[str]
    output: List[List[Any]]
    errors: Optional[List[ChalkError]]


class _OfflineQueryInput(BaseModel):
    columns: List[str]
    values: List[List[Any]]


class _QueryRequest(BaseModel):
    inputs: Mapping[str, Any]
    outputs: List[str]
    staleness: Optional[Mapping[str, str]] = None
    context: Optional[OnlineQueryContext]
    deployment_id: Optional[str] = None
    correlation_id: Optional[str] = None
    query_name: Optional[str] = None
    meta: Optional[Mapping[str, str]] = None


class _TriggerResolverRunRequest(BaseModel):
    resolver_fqn: str


T = TypeVar("T")


class _ChalkClientConfig(BaseModel):
    client_id: str
    client_secret: str
    api_server: str
    active_environment: Optional[str]


class _OnlineQueryResponse(BaseModel):
    data: List[FeatureResult]
    errors: Optional[List[ChalkError]]


class _CreateOfflineQueryJobRequest(BaseModel):
    """
    Attributes
        output: A list of output feature root fqns to query
        destination_format: The desired output format. Should be 'CSV' or 'PARQUET'
        input: Any givens
        max_samples: The maximum number of samples
    """

    output: List[str]
    required_output: List[str]
    destination_format: str
    input: Optional[_OfflineQueryInput] = None
    max_samples: Optional[int] = None
    observed_at_lower_bound: Optional[datetime] = None
    observed_at_upper_bound: Optional[datetime] = None
    dataset_name: Optional[str] = None
    branch: Optional[str] = None
    environment: Optional[str] = None


# FIXME document
class _ComputeResolverOutputRequest(BaseModel):
    input: _OfflineQueryInput
    resolver_fqn: str
    branch: Optional[str] = None
    environment: Optional[str] = None


class _RecomputeResolverOutputRequest(BaseModel):
    persistent_id: str
    resolver_fqn: str
    branch: Optional[str] = None
    environment: Optional[str] = None


class _ComputeResolverOutputResponse(BaseModel):
    job_id: str
    persistent_id: str
    errors: Optional[List[ChalkError]]


class _CreateOfflineQueryJobResponse(BaseModel):
    """
    Attributes:
        job_id: A job ID, which can be used to retrieve the results.
    """

    job_id: str
    version: int = 1  # Deprecated
    errors: Optional[List[ChalkError]]


class _GetOfflineQueryJobResponse(BaseModel):
    """
    Attributes:
        is_finished: Whether the export job is finished (it runs asynchronously)
        signed_urls: A list of signed URLs that the client can download to retrieve the exported data.
    """

    is_finished: bool
    version: int
    urls: List[str]
    errors: Optional[List[ChalkError]]


class ChalkOfflineQueryException(ChalkBaseException):
    message: str
    errors: List[ChalkError]

    def __init__(self, message: str, errors: List[ChalkError]):
        self.message = message
        self.errors = errors
        super().__init__(message + "\n" + "\n".join(["\t" + e.message for e in errors[0:3]]))


class ChalkResolverRunException(ChalkBaseException):
    message: str

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ChalkDatasetDownloadException(ChalkBaseException):
    message: str

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class OnlineQueryResponseWrapper(OnlineQueryResponse):
    data: List[FeatureResult]
    errors: List[ChalkError]
    warnings: List[str]

    def __init__(self, data: List[FeatureResult], errors: List[ChalkError], warnings: List[str]):
        self.data = data
        self.errors = errors
        self.warnings = warnings
        for d in self.data:
            if d.value is not None:
                try:
                    d.value = FEATURE_CODEC.decode_fqn(d.field, d.value)
                except Exception:
                    self.warnings.append(
                        f"Return data {d.field}:{d.value} cannot be decoded. Attempting to JSON decode"
                    )

        self._values = {d.field: d for d in self.data}

    def __repr__(self) -> str:
        info = self.errors if self.errors else self.data
        return repr(pd.DataFrame([vars(x) for x in info]))

    def _repr_html_(self) -> str | None:
        info = self.errors if self.errors else self.data
        return pd.DataFrame([vars(x) for x in info])._repr_html_()

    def get_feature(self, feature: Any) -> Optional[FeatureResult]:
        # Typing `feature` as Any, as the Features will be typed as the underlying datatypes, not as Feature
        return self._values.get(str(feature))

    def get_feature_value(self, feature: Any) -> Optional[Any]:
        # Typing `feature` as Any, as the Features will be typed as the underlying datatypes, not as Feature
        v = self.get_feature(feature)
        return v and v.value


class ChalkAPIClientImpl(ChalkAPIClientProtocol):
    def __init__(
        self,
        *,
        client_id: Optional[str],
        client_secret: Optional[str],
        environment: Optional[str],
        api_server: Optional[str],
    ):
        if client_id is not None and client_secret is not None:
            self._config = _ChalkClientConfig(
                client_id=client_id,
                client_secret=client_secret,
                api_server=api_server or "https://api.chalk.ai",
                active_environment=environment,
            )
        else:
            token = load_token()
            if token is None:
                raise ValueError(
                    (
                        "Could not find .chalk.yml config file for project, "
                        "and explicit configuration was not provided. "
                        "You may need to run `chalk login` from your command line, "
                        "or check that your working directory is set to the root of "
                        "your project."
                    )
                )
            self._config = _ChalkClientConfig(
                client_id=token.clientId,
                client_secret=token.clientSecret,
                api_server=api_server or token.apiServer or "https://api.chalk.ai",
                active_environment=environment or token.activeEnvironment,
            )

        self._default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": f"chalkpy-{chalkpy_version}",
            "X-Chalk-Client-Id": self._config.client_id,
        }
        self._exchanged_credentials = False
        self._primary_environment = None

    def _exchange_credentials(self):
        _logger.debug("Performing a credentials exchange")
        resp = requests.post(
            url=urljoin(self._config.api_server, f"v1/oauth/token"),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json=_ExchangeCredentialsRequest(
                client_id=self._config.client_id,
                client_secret=self._config.client_secret,
                grant_type="client_credentials",
            ).dict(),
            timeout=10,
        )
        resp.raise_for_status()
        response_json = resp.json()
        try:
            creds = _ExchangeCredentialsResponse(**response_json)
        except ValidationError:
            raise HTTPError(response=resp)
        self._default_headers["Authorization"] = f"Bearer {creds.access_token}"
        self._primary_environment = creds.primary_environment
        self._exchanged_credentials = True

    def _get_headers(self, environment_override: Optional[str]):
        x_chalk_env_id = environment_override or self._config.active_environment or self._primary_environment
        headers = dict(self._default_headers)  # shallow copy
        if x_chalk_env_id is not None:
            headers["X-Chalk-Env-Id"] = x_chalk_env_id
        return headers

    def _request(
        self,
        method: str,
        uri: str,
        response: Type[T],
        json: Optional[BaseModel] = None,
        use_engine: bool = False,
        environment_override: Optional[str] = None,
    ) -> T:
        # Track whether we already exchanged credentials for this request
        exchanged_credentials = False
        if not self._exchanged_credentials:
            exchanged_credentials = True
            self._exchange_credentials()
        headers = self._get_headers(environment_override=environment_override)
        url = urljoin(self._config.api_server, uri)
        json_body = json and json.dict()
        r = requests.request(method=method, headers=headers, url=url, json=json_body)
        if r.status_code in (401, 403) and not exchanged_credentials:
            # It is possible that credentials expired, or that we changed permissions since we last
            # got a token. Exchange them and try again
            self._exchange_credentials()
            r = requests.request(method=method, headers=headers, url=url, json=json_body)

        r.raise_for_status()
        return response(**r.json())

    def whoami(self) -> WhoAmIResponse:
        return self._request(method="GET", uri=f"/v1/who-am-i", response=WhoAmIResponse)

    def upload_features(
        self,
        input: Mapping[Union[str, Feature, FeatureWrapper, Any], Any],
        context: Optional[OnlineQueryContext] = None,
        preview_deployment_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
    ) -> Optional[List[ChalkError]]:
        return self.query(
            input=input,
            output=list(input.keys()),
            staleness=None,
            context=context,
            preview_deployment_id=preview_deployment_id,
            correlation_id=correlation_id,
            query_name=query_name,
            meta=meta,
        ).errors

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
        warnings: List[str] = []
        encoded_inputs = {}
        for feature, value in input.items():
            try:
                feature = ensure_feature(feature)
                encoded_inputs[feature.fqn] = FEATURE_CODEC.encode(feature, value)
            except Exception:
                warnings.append(f"Input {feature} not recognized. JSON encoding {feature} and requesting anyways")
                encoded_inputs[feature] = value
        outputs: List[str] = [str(feature) for feature in output]

        request = _QueryRequest(
            inputs=encoded_inputs,
            outputs=outputs,
            staleness={} if staleness is None else {ensure_feature(k).root_fqn: v for k, v in staleness.items()},
            context=context,
            deployment_id=preview_deployment_id,
            correlation_id=correlation_id,
            query_name=query_name,
            meta=meta,
        )

        resp = self._request(
            method="POST",
            uri="/v1/query/online",
            json=request,
            response=_OnlineQueryResponse,
            use_engine=preview_deployment_id is None,
            environment_override=context.environment if context else None,
        )
        return OnlineQueryResponseWrapper(data=resp.data, errors=resp.errors or [], warnings=warnings)

    def get_training_dataframe(
        self,
        input: Union[Mapping[Union[str, Feature, FeatureWrapper, Any], Any], pd.DataFrame, pl.DataFrame, DataFrame],
        input_times: Union[Sequence[datetime], datetime, None] = None,
        output: Sequence[Union[str, Feature, FeatureWrapper, Any]] = (),
        required_output: Sequence[Union[str, Feature, FeatureWrapper, Any]] = (),
        output_ts: bool = False,
        context: Optional[OfflineQueryContext] = None,
        dataset: Optional[str] = None,
        branch: Optional[str] = None,
        max_samples: Optional[int] = None,
    ) -> pd.DataFrame:
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[polars]")
        if isinstance(input, (DataFrame, pl.DataFrame)):
            input = input.to_pandas()

        if isinstance(input, collections.abc.Mapping):
            input = {str(k): v for (k, v) in input.items()}

        if not isinstance(input, pd.DataFrame):
            input = pd.DataFrame(input)

        if len(output) == 0 and len(required_output) == 0:
            raise ValueError("Either 'output' or 'required_output' must be specified.")

        self._get_headers(environment_override=None)

        return self._get_training_dataframe(
            input=input,
            input_times=input_times,
            optional_output=[str(x) for x in output],
            required_output=[str(x) for x in required_output],
            output_id=False,
            output_ts=output_ts,
            context=context,
            dataset=dataset,
            branch=branch,
            max_samples=max_samples,
        )

    def _get_training_dataframe(
        self,
        input: pd.DataFrame,
        input_times: Union[Sequence[datetime], datetime, None],
        optional_output: List[str],
        required_output: List[str],
        output_id: bool,
        output_ts: bool,
        max_samples: Optional[int],
        context: Optional[OfflineQueryContext],
        dataset: Optional[str],
        branch: Optional[str],
    ) -> pd.DataFrame:
        columns = input.columns
        matrix: List[List[Any]] = input.T.values.tolist()

        columns_fqn = [str(c) for c in (*columns, CHALK_TS_FEATURE)]

        if input_times is None:
            input_times = datetime.now(timezone.utc)
        if isinstance(input_times, datetime):
            input_times = [input_times for _ in range(len(input))]

        matrix.append([a for a in input_times])

        for col_index, column in enumerate(matrix):
            for row_index, value in enumerate(column):
                try:
                    encoded_feature = FEATURE_CODEC.encode_fqn(
                        fqn=columns_fqn[col_index],
                        value=value,
                    )
                except (KeyError, ValueError, TypeError):
                    encoded_feature = value

                matrix[col_index][row_index] = encoded_feature

        query_input = _OfflineQueryInput(
            columns=columns_fqn,
            values=matrix,
        )

        response = self._create_and_await_offline_query_job(
            optional_output=optional_output,
            required_output=required_output,
            query_input=query_input,
            output_id=output_id,
            output_ts=output_ts,
            dataset_name=dataset,
            branch=branch,
            max_samples=max_samples,
            environment=context and context.environment,
        )
        return response.to_pandas()

    def sample(
        self,
        output: Sequence[Union[str, Feature, FeatureWrapper, Any]],
        required_output: Sequence[Union[str, Feature, FeatureWrapper, Any]] = (),
        output_id: bool = False,
        output_ts: bool = False,
        max_samples: Optional[int] = None,
        dataset: Optional[str] = None,
        branch: Optional[str] = None,
        context: Optional[OfflineQueryContext] = None,
    ) -> pd.DataFrame:
        optional_output_root_fqns = [str(f) for f in output]
        required_output_root_fqns = [str(f) for f in required_output]

        if len(output) == 0 and len(required_output) == 0:
            raise ValueError("Either 'output' or 'required_output' must be specified.")

        try:
            response = self._create_and_await_offline_query_job(
                query_input=None,
                optional_output=optional_output_root_fqns,
                required_output=required_output_root_fqns,
                max_samples=max_samples,
                output_id=output_id,
                output_ts=output_ts,
                dataset_name=dataset,
                branch=branch,
                environment=context and context.environment,
            )
        except HTTPError as e:
            _logger.debug("Got HTTP Exception while processing sample query", exc_info=e)
            raise ChalkOfflineQueryException(message=f"HTTP error while processing sample query.", errors=[])

        return response.to_pandas()

    def trigger_resolver_run(
        self,
        resolver_fqn: str,
        deployment_id: Optional[str] = None,
    ) -> ResolverRunResponse:
        _logger.debug(f'Triggering resolver {resolver_fqn} to run with deployment ID "{deployment_id}"')

        request = _TriggerResolverRunRequest(resolver_fqn=resolver_fqn)
        try:
            response = self._request(
                method="POST",
                uri="/v1/runs/trigger",
                json=request,
                response=ResolverRunResponse,
            )
        except HTTPError as e:

            detail = e.response.json().get("detail")
            if detail is not None:
                raise ChalkResolverRunException(message=detail)
            else:
                raise

        return response

    def get_run_status(self, run_id: str) -> ResolverRunResponse:
        try:
            response = self._request(
                method="GET",
                uri=f"/v1/runs/{run_id}",
                response=ResolverRunResponse,
            )
        except HTTPError as e:

            detail = e.response.json().get("detail")
            if detail is not None:
                raise ChalkResolverRunException(message=detail)
            else:
                raise

        return response

    def _create_and_await_offline_query_job(
        self,
        optional_output: List[str],
        required_output: List[str],
        query_input: Optional[_OfflineQueryInput],
        max_samples: Optional[int],
        dataset_name: Optional[str],
        branch: Optional[str],
        environment: Optional[str],
        output_id: bool,
        output_ts: bool,
    ) -> pl.DataFrame:
        req = _CreateOfflineQueryJobRequest(
            output=optional_output,
            required_output=required_output,
            destination_format="PARQUET",
            input=query_input,
            max_samples=max_samples,
            dataset_name=dataset_name,
            branch=branch,
            environment=environment,
        )
        response = self._create_offline_query_job(request=req)

        if response.errors is not None and len(response.errors) > 0:
            raise ChalkOfflineQueryException(message="Failed to execute offline query", errors=response.errors)

        while True:
            status = self._get_job_status(job_id=response.job_id)
            if status.is_finished:
                break
            time.sleep(0.5)
        return load_dataset(
            uris=status.urls,
            output_features=[*optional_output, *required_output],
            version=DatasetVersion(response.version),
            output_id=output_id,
            output_ts=output_ts,
        )

    def compute_resolver_output(
        self,
        input: Union[Mapping[Union[str, Feature], Any], pl.DataFrame, pd.DataFrame, DataFrame],
        input_times: List[datetime],
        resolver: str,
    ) -> pl.DataFrame:
        if not isinstance(input, DataFrame):
            input = DataFrame(input)
        input = input.to_pandas()

        columns = input.columns
        matrix = input.T.values.tolist()

        columns_fqn = [str(c) for c in (*columns, CHALK_TS_FEATURE)]

        matrix.append([a for a in input_times])

        for col_index, column in enumerate(matrix):
            for row_index, value in enumerate(column):
                matrix[col_index][row_index] = FEATURE_CODEC.encode_fqn(
                    fqn=columns_fqn[col_index],
                    value=value,
                )

        query_input = _OfflineQueryInput(
            columns=columns_fqn,
            values=matrix,
        )
        request = _ComputeResolverOutputRequest(input=query_input, resolver_fqn=resolver)
        response = self._request(
            method="POST", uri="/v1/compute_resolver_output", json=request, response=_ComputeResolverOutputResponse
        )

        if response.errors is not None and len(response.errors) > 0:
            raise ChalkOfflineQueryException(message="Failed to execute offline query", errors=response.errors)

        while True:
            status = self._get_compute_job_status(job_id=response.job_id)
            if status.is_finished:
                break
            time.sleep(0.5)

        return load_dataset(uris=status.urls, version=DatasetVersion.COMPUTE_RESOLVER_OUTPUT_V1, executor=None)

    def _get_compute_job_status(self, job_id: str) -> _GetOfflineQueryJobResponse:
        return self._request(
            method="GET", uri=f"/v1/compute_resolver_output/{job_id}", response=_GetOfflineQueryJobResponse
        )

    def _create_offline_query_job(self, request: _CreateOfflineQueryJobRequest):
        response = self._request(
            method="POST", uri="/v2/offline_query", json=request, response=_CreateOfflineQueryJobResponse
        )
        return response

    def _get_job_status(self, job_id: str) -> _GetOfflineQueryJobResponse:
        return self._request(method="GET", uri=f"/v2/offline_query/{job_id}", response=_GetOfflineQueryJobResponse)
