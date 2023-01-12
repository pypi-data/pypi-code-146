"""Gordo client."""
import itertools
import logging
import pickle
import copy

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from time import sleep
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union, cast

import pandas as pd
import requests
import wrapt
from cachetools import TTLCache, cached
from gordo_core.base import (
    GordoBaseDataset,
    DatasetWithProvider,
    import_dataset,
    create_with_provider,
    create_dataset,
)
from gordo_core.data_providers.base import GordoBaseDataProvider
from sklearn.base import BaseEstimator

from gordo_client.dataframe import (
    dataframe_from_dict,
    dataframe_from_parquet_bytes,
    dataframe_into_parquet_bytes,
    dataframe_to_dict,
)
from gordo_client.io import BadGordoRequest, HttpUnprocessableEntity, NotFound, ResourceGone, _handle_response
from gordo_client.schemas import Machine, Metadata
from gordo_client.utils import PredictionResult

logger = logging.getLogger(__name__)


class Client:
    """
    Basic client shipped with Gordo

    Enables some basic communication with a deployed Gordo project
    """

    def __init__(
        self,
        project: str,
        host: str = "localhost",
        port: int = 443,
        scheme: str = "https",
        metadata: Optional[dict] = None,
        data_provider: Optional[GordoBaseDataProvider] = None,
        prediction_forwarder: Optional[Callable[[pd.DataFrame, Machine, dict, pd.DataFrame], None]] = None,
        batch_size: int = 100000,
        parallelism: int = 10,
        forward_resampled_sensors: bool = False,
        n_retries: int = 5,
        use_parquet: bool = False,
        session: Optional[requests.Session] = None,
        all_columns: bool = False,
    ):
        """

        Parameters
        ----------
        project: str
            Name of the project.
        host: str
            Host of where to find controller and other services.
        port: int
            Port to communicate on.
        scheme: str
            The request scheme to use, ie 'https'.
        metadata: Optional[dict]
            Arbitrary mapping of key-value pairs to save to influx with
            prediction runs in 'tags' property
        data_provider: Optional[GordoBaseDataProvider]
            The data provider to use for the dataset. If not set, the client
            will fall back to using the GET /prediction machine
        prediction_forwarder: Optional[Callable[[pd.DataFrame, Machine, dict, pd.DataFrame], None]]
            callable which will take a dataframe of predictions,
            ``Machine``, the metadata, and the dataframe of resampled sensor
            values and forward them somewhere.
        batch_size: int
            How many samples to send to the server, only applicable when data
            provider is supplied.
        parallelism: int
            The maximum number of tasks to run at a given time when
            running predictions
        forward_resampled_sensors: bool
            If true then forward resampled sensor values to the prediction_forwarder
        n_retries: int
            Number of times the client should attempt to retry a failed prediction request. Each time the client
            retires the time it sleeps before retrying is exponentially calculated.
        use_parquet: bool
            Pass the data to the server using the parquet protocol. Default is True
            and recommended as it's more efficient for larger batch sizes. If False JSON
            is used for sending the data back and forth.
        session: Optional[requests.Session]
            The http session object to use for making requests.
        all_columns: bool
            Return all columns for prediction. Including `smooth-..` columns
        """

        self.base_url = f"{scheme}://{host}:{port}"
        self.server_endpoint = f"{self.base_url}/gordo/v0/{project}"
        self.metadata = metadata if metadata is not None else dict()
        self.prediction_forwarder = prediction_forwarder
        self.data_provider = data_provider
        self.use_parquet = use_parquet
        self.project_name = project

        # Default, failing back to /prediction on http code 422
        self.prediction_path = "/anomaly/prediction"
        self.batch_size = batch_size
        self.parallelism = parallelism
        self.forward_resampled_sensors = forward_resampled_sensors
        self.n_retries = n_retries
        self.format = "parquet" if use_parquet else "json"
        self.session = session or requests.Session()
        self.all_columns = all_columns

    @wrapt.synchronized
    @cached(TTLCache(maxsize=1, ttl=5))
    def get_revisions(self):
        """
        Gets the available revisions served by the server.

        Returns
        ------
        dict
            Dictionary with two keys, `available-revisions` and `latest`. The first is
            a list of all available revisions, and `latest` is the latest and default
            revision.
        """
        resp = self.session.get(f"{self.base_url}/gordo/v0/{self.project_name}/revisions")
        resp_json = _handle_response(resp=resp, resource_name="List of available revisions from server")
        return resp_json

    def _get_latest_revision(self) -> str:
        return self.get_revisions()["latest"]

    @wrapt.synchronized
    @cached(TTLCache(maxsize=64, ttl=30))
    def _get_available_machines(self, revision):
        resp = self.session.get(f"{self.base_url}/gordo/v0/{self.project_name}/models", params={"revision": revision})
        model_response = _handle_response(resp=resp, resource_name=f"Model name listing for revision {revision}")
        if "models" not in model_response:
            raise ValueError(f"Invalid response from server, key 'model' not found in: {model_response}")
        model_response["revision"] = model_response.get("revision", revision)
        return model_response

    def get_available_machines(self, revision: Optional[str] = None):
        """Returns a dict representing the /models endpoint of the project for the given revision.

        Contains at least a key `models` which contains the name of the models the
        server can serve for that revision, and a key `revision` containing the
        revision."""
        return self._get_available_machines(revision=revision or self._get_latest_revision())

    def get_machine_names(self, revision: Optional[str] = None):
        """Returns the list of machine names served by a given revision, or latest
        revision if no revision is passed"""
        model_response = self._get_available_machines(revision=revision or self._get_latest_revision())
        return model_response.get("models")

    def _get_machines(self, revision: Optional[str] = None, machine_names: Optional[List[str]] = None) -> List[Machine]:
        """
        Returns a list of :class:`gordo.workflow.config_elements.machine.Machine` elements served by the server for
        the provided machine names.

        Parameters
        ----------
        revision: Optional[str]
            Revision to fetch machines for. If None then the latest revision is fetched
            from the server.
        machine_names: Optional[List[str]]
            List of names of machines to fetch metadata for. If None then all machines
            for the given revision is fetched.


        Returns
        -------
        List[Machine]
        """
        _machine_names: List[str] = machine_names or self.get_machine_names(revision=revision)
        with ThreadPoolExecutor(max_workers=self.parallelism) as executor:
            machines = executor.map(
                lambda machine: self.machine_from_server(
                    name=machine, revision=revision or self._get_latest_revision()
                ),
                _machine_names,
            )
            return list(machines)

    @wrapt.synchronized
    @cached(TTLCache(maxsize=32, ttl=600))
    def machine_from_server(self, name: str, revision: str) -> Machine:
        resp = self.session.get(
            f"{self.base_url}/gordo/v0/{self.project_name}/{name}/metadata", params={"revision": revision}
        )
        metadata = _handle_response(resp=resp, resource_name=f"Machine metadata for {name}")
        if isinstance(metadata, dict) and metadata.get("metadata", None):
            return Machine(**metadata.get("metadata", None))
        else:
            raise NotFound(f"Machine {name} not found")

    def download_model(self, revision=None, targets: Optional[List[str]] = None) -> Dict[str, BaseEstimator]:
        """
        Download the actual model(s) from the ML server /download-model.

        Returns
        -------
        Dict[str, BaseEstimator]
            Mapping of target name to the model
        """
        models = dict()
        for machine_name in targets or self.get_machine_names(revision=revision):
            resp = self.session.get(f"{self.base_url}/gordo/v0/{self.project_name}/{machine_name}/download-model")
            content = _handle_response(resp, resource_name=f"Model download for model {machine_name}")
            if isinstance(content, bytes):
                models[machine_name] = pickle.loads(content)
            else:
                raise ValueError(
                    f"Got unexpected return type: {type(content)} when attempting to"
                    f" download the model {machine_name}."
                )
        return models

    def get_metadata(self, revision: Optional[str] = None, targets: Optional[List[str]] = None) -> Dict[str, Metadata]:
        """
        Get the machine metadata for provided machines, or all if no machine names are provided.

        Parameters
        ----------
        revision: Optional[str]
            Revision to fetch machines for. If None then the latest revision is fetched
            from the server.
        targets: Optional[List[str]]
            List of names of machines to fetch metadata for. If None then all machines
            for the given revision is fetched.

        Returns
        -------
        Dict[str, Metadata]
            Mapping of target names to their metadata
        """
        #  Value expression in dictionary comprehension has incompatible type "Optional[Metadata]"; expected type "Metadata"
        machines = self._get_machines(revision=revision, machine_names=targets)
        return {ep.name: copy.copy(ep.metadata) for ep in machines}

    def predict(
        self, start: datetime, end: datetime, targets: Optional[List[str]] = None, revision: Optional[str] = None
    ) -> Iterable[Tuple[str, pd.DataFrame, List[str]]]:
        """
        Start the prediction process.

        Parameters
        ----------
        start: datetime
        end: datetime
        targets: Optional[List[str]]
            Optionally only target certain machines, referring to them by name.
        revision: Optional[str]
            Revision of the model to run predictions again, defaulting to latest.

        Raises
        -----
        ResourceGone
            If the sever returns a 410, most likely because the revision is too old

        Returns
        -------
        List[Tuple[str, pandas.core.DataFrame, List[str]]
            A list of tuples, where:
              0th element is the target name
              1st element is the dataframe of the predictions; complete with a DateTime index.
              2nd element is a list of error messages (if any) for running the predictions
        """
        rev = revision or self._get_latest_revision()
        machines = self._get_machines(revision=rev, machine_names=targets)

        # For every machine, start making predictions for the time range
        with ThreadPoolExecutor(max_workers=self.parallelism) as executor:
            jobs = executor.map(
                lambda ep: self.predict_single_machine(machine=ep, start=start, end=end, revision=rev), machines
            )
            return [(j.name, j.predictions, j.error_messages) for j in jobs]

    def predict_single_machine(
        self, machine: Machine, start: datetime, end: datetime, revision: str
    ) -> PredictionResult:
        """
        Get predictions based on the /prediction POST machine of Gordo ML Servers.

        Parameters
        ----------
        machine: Machine
            Named tuple which has 'machine' specifying the full url to the base ml server
        start: datetime
        end: datetime
        revision: str
            Revision of the model to use

        Returns
        -------
        dict
            Prediction response from /prediction GET
        """

        # Fetch all of the raw data
        X, y = self._raw_data(machine, start, end)

        # Forward sensor data
        if self.prediction_forwarder is not None and self.forward_resampled_sensors:
            self.prediction_forwarder(resampled_sensor_data=X)  # type: ignore

        max_indx = len(X.index) - 1  # Maximum allowable index values

        # Start making batch predictions
        with ThreadPoolExecutor(max_workers=self.parallelism) as executor:
            jobs = executor.map(
                lambda i: self._send_prediction_request(
                    X,
                    y,
                    chunk=slice(i, i + self.batch_size),
                    machine=machine,
                    start=X.index[i],
                    end=X.index[i + self.batch_size if i + self.batch_size <= max_indx else max_indx],
                    revision=revision,
                ),
                range(0, X.shape[0], self.batch_size),
            )

            # Accumulate the batched predictions
            prediction_dfs = []
            error_messages: List[str] = []
            for prediction_result in jobs:
                if prediction_result.predictions is not None:
                    prediction_dfs.append(prediction_result.predictions)
                error_messages.extend(prediction_result.error_messages)

            predictions = pd.concat(prediction_dfs).sort_index() if prediction_dfs else pd.DataFrame()
        return PredictionResult(name=machine.name, predictions=predictions, error_messages=error_messages)

    def _send_prediction_request(
        self,
        X: pd.DataFrame,
        y: Optional[pd.DataFrame],
        chunk: slice,
        machine: Machine,
        start: datetime,
        end: datetime,
        revision: str,
    ):
        """
        Post a slice of data to the machine.

        Parameters
        ----------
        X: pandas.core.DataFrame
            The data for the model, in pandas representation
        chunk: slice
            The slice to take from DataFrame.iloc for the batch size
        machine: Machine
        start: datetime
        end: datetime

        Notes
        -----
        PredictionResult.predictions may be None if the prediction process fails

        Returns
        -------
        PredictionResult

        Raises
        -----
        ResourceGone
            If the sever returns a 410, most likely because the revision is too old
        """
        params = {"format": self.format, "revision": revision}
        if self.all_columns:
            params["all_columns"] = "true"
        kwargs: Dict[str, Any] = dict(
            url=f"{self.base_url}/gordo/v0/{self.project_name}/{machine.name}{self.prediction_path}", params=params
        )

        # We're going to serialize the data as either JSON or Arrow
        if self.use_parquet:
            kwargs["files"] = {
                "X": dataframe_into_parquet_bytes(X.iloc[chunk]),
                "y": dataframe_into_parquet_bytes(y.iloc[chunk]) if y is not None else None,
            }
        else:
            kwargs["json"] = {
                "X": dataframe_to_dict(X.iloc[chunk]),
                "y": dataframe_to_dict(y.iloc[chunk]) if y is not None else None,
            }

        # Start attempting to get predictions for this batch
        for current_attempt in itertools.count(start=1):
            try:
                try:
                    resp = _handle_response(self.session.post(**kwargs))
                except HttpUnprocessableEntity:
                    self.prediction_path = "/prediction"
                    kwargs["url"] = f"{self.base_url}/gordo/v0/{self.project_name}/{machine.name}{self.prediction_path}"
                    resp = _handle_response(self.session.post(**kwargs))
            # If it was an IO or TimeoutError, we can retry
            except (IOError, TimeoutError, requests.ConnectionError, requests.HTTPError) as exc:
                if current_attempt <= self.n_retries:
                    time_to_sleep = min(2 ** (current_attempt + 2), 300)
                    logger.warning(
                        f"Failed to get response on attempt {current_attempt} out of {self.n_retries} attempts."
                    )
                    sleep(time_to_sleep)
                    continue
                else:
                    msg = (
                        f"Failed to get predictions for dates {start} -> {end} "
                        f"for target: '{machine.name}' Error: {exc}"
                    )
                    logger.error(msg)

                    return PredictionResult(name=machine.name, predictions=None, error_messages=[msg])

            # No point in retrying a BadGordoRequest
            except (BadGordoRequest, NotFound) as exc:
                msg = (
                    f"Failed with bad request or not found for dates {start} -> {end} "
                    f"for target: '{machine.name}' Error: {exc}"
                )
                logger.error(msg)
                return PredictionResult(name=machine.name, predictions=None, error_messages=[msg])
            except ResourceGone:
                raise

            # Process response and return if no exception
            else:
                predictions = self.dataframe_from_response(resp)
                # Forward predictions to any other consumer if registered.
                if self.prediction_forwarder is not None:
                    self.prediction_forwarder(  # type: ignore
                        predictions=predictions, machine=machine, metadata=self.metadata
                    )
                return PredictionResult(name=machine.name, predictions=predictions, error_messages=[])

    def _get_dataset(self, machine: Machine, start: datetime, end: datetime) -> GordoBaseDataset:
        """
        Apply client setting to machine dataset.

        Parameters
        ----------
        machine: Machine
            Named tuple representing the machine info from controller
        start: datetime
        end: datetime

        Returns
        -------
        GordoBaseDataset
        """
        # We want to adjust for any model offset. If the model outputs less than it got in, it requires
        # extra data than what we're being asked to get predictions for.
        # just to give us some buffer zone.

        resolution = machine.dataset["resolution"]
        n_intervals = machine.metadata.build_metadata.model.model_offset + 5
        start = self._adjust_for_offset(dt=start, resolution=resolution, n_intervals=n_intervals)

        # Re-create the machine's dataset but updating to use the client's
        # data provider and changing the dates of data we want.
        config = copy.copy(machine.dataset)
        config.update({"train_start_date": start, "train_end_date": end})

        dataset_type = config.pop("type", None)
        if dataset_type is None:
            raise ValueError("dataset.type is empty")
        dataset_cls = import_dataset(dataset_type)
        if self.data_provider is not None:
            if not issubclass(dataset_cls, DatasetWithProvider):
                raise ValueError("Unable to apply custom data_provider for non DatasetWithProvider dataset class")
            config["data_provider"] = self.data_provider
            dataset = create_with_provider(dataset_cls, config)
        else:
            dataset = create_dataset(dataset_cls, config)
        return dataset

    @staticmethod
    def _extract_build_metadata(machine: Machine) -> dict:
        metadata = machine.metadata
        return metadata.build_metadata.dataset.dict()

    def _raw_data(self, machine: Machine, start: datetime, end: datetime) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Fetch the required raw data in this time range which would satisfy this machine's /prediction POST.

        Parameters
        ----------
        machine: Machine
            Named tuple representing the machine info from controller
        start: datetime
        end: datetime

        Returns
        -------
        Tuple[pandas.core.DataFrame, pandas.core.DataFrame]
            The dataframes representing X and y.
        """
        dataset = self._get_dataset(machine, start, end)
        build_metadata = self._extract_build_metadata(machine)
        return dataset.get_client_data(build_metadata)

    @staticmethod
    def _adjust_for_offset(dt: datetime, resolution: str, n_intervals: int = 100):
        """
        Adjust the given date by multiplying ``n_intervals`` by ``resolution``.

        Such that a date of 12:00:00 with ``n_intervals=2`` and ``resolution='10m'`` (10 minutes)
        would result in 11:40

        Parameters
        ----------
        dt: datetime
            Initial datetime to adjust.
        resolution: str
            A string code capable of being parsed by :meth::`pandas.Timedelta`.
        n_intervals: int
            Number of resolution steps to take earlier than the given date.

        Returns
        -------
        datetime
            The new offset datetime object.

        Examples
        --------
        >>> import dateutil
        >>> date = dateutil.parser.isoparse("2019-01-01T12:00:00+00:00")
        >>> offset_date = Client._adjust_for_offset(dt=date, resolution='15m', n_intervals=5)
        >>> str(offset_date)
        '2019-01-01 10:45:00+00:00'
        """
        return dt - (pd.Timedelta(resolution) * n_intervals)

    @staticmethod
    def dataframe_from_response(response: Union[dict, bytes]) -> pd.DataFrame:
        """
        Convert response from server into dataframe.

        The response from the server, parsed as either JSON / dict or raw bytes,
        of which would be expected to be loadable from :func:`server.utils.dataframe_from_parquet_bytes`

        Parameters
        ----------
        response: Union[dict, bytes]
            The parsed response from the ML server.

        Returns
        -------
        pandas.DataFrame
        """
        if isinstance(response, dict):
            return dataframe_from_dict(response["data"])
        return dataframe_from_parquet_bytes(response)


def make_date_ranges(start: datetime, end: datetime, max_interval_days: int, freq: str = "H"):
    """
    Split start and end datetimes into a list of datetime intervals.

    If the interval between start and end is less than ``max_interval_days`` then
    the resulting list will contain the original start & end. ie. [(start, end)]

    Otherwise it will split the intervals by ``freq``, parse-able by pandas.

    Parameters
    ----------
    start: datetime
    end: datetime
    max_interval_days: int
        Maximum days between start and end before splitting into intervals
    freq: str
        String frequency parse-able by Pandas

    Returns
    -------
    List[Tuple[datetime, datetime]]
    """
    if (end - start).days >= max_interval_days:
        # Split into 1hr data ranges
        date_range = pd.date_range(start, end, freq=freq)
        return [(date_range[i], date_range[i + 1]) for i in range(0, len(date_range) - 1)]
    return [(start, end)]
