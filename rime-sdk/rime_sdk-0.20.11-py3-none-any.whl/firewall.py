"""Library defining the interface to firewall."""
import json
import numbers
from datetime import datetime, timedelta
from typing import Any, Dict, Iterator, List, Optional, Tuple

import pandas as pd
from deprecated import deprecated

from rime_sdk.data_collector import DataCollector
from rime_sdk.internal.config_parser import (
    convert_config_to_swagger,
    convert_incremental_config_to_swagger,
)
from rime_sdk.internal.rest_error_handler import RESTErrorHandler
from rime_sdk.internal.swagger_utils import (
    DEFAULT_THRESHOLD_INFO_KEY_ORDER,
    location_args_to_data_location_swagger,
    serialize_datetime_to_proto_timestamp,
    swagger_is_empty,
)
from rime_sdk.internal.throttle_queue import ThrottleQueue
from rime_sdk.internal.utils import convert_dict_to_html, make_link
from rime_sdk.job import ContinuousTestJob
from rime_sdk.swagger import swagger_client
from rime_sdk.swagger.swagger_client import ApiClient
from rime_sdk.swagger.swagger_client.models import (
    ComponentsFirewallIdBody,
    FirewallFirewallIdBody,
    RimeBatchMetadata,
    RimeCustomImage,
    RimeCustomImageType,
    RimeDataLocation,
    RimeFirewall,
    RimeFirewallComponents,
    RimeFirewallRules,
    RimeJobMetadata,
    RimeManagedImageReference,
    RimeReferenceSetSource,
    RimeStartFirewallContinuousTestRequest,
    RimeThresholdInfo,
    RimeTimeRange,
    RimeUpdateFirewallResponse,
)
from rime_sdk.test_run import ContinuousTestRun

# 30 days in seconds
# 1 day = 86400 seconds
LIST_TEST_RUNS_INTERVAL_LENGTH_SECONDS = 30 * 86400


class Firewall:
    """Firewall object wrapper with helpful methods for working with RIME Firewall.

    Attributes:
        api_client: ApiClient
                The client used to query about the status of the job.
        firewall_id: str
            How to refer to the FW in the backend.
            Use this attribute to specify the Firewall for tasks in the backend.
    """

    # A throttler that limits the number of model tests to roughly 20 every 5 minutes.
    # This is a static variable for Client.
    _throttler = ThrottleQueue(desired_events_per_epoch=20, epoch_duration_sec=300)

    def __init__(self, api_client: ApiClient, firewall_id: str) -> None:
        """Create a new Firewall wrapper object.

        Arguments:
            api_client: ApiClient
                The client used to query about the status of the job.
            firewall_id: str
                The identifier for the RIME job that this object monitors.
        """
        self._api_client = api_client
        self._firewall_id = firewall_id
        self._data_collector = DataCollector(self._api_client, self._firewall_id)

    def __eq__(self, obj: Any) -> bool:
        """Check if this FWInstance is equivalent to 'obj'."""
        return isinstance(obj, Firewall) and self._firewall_id == obj._firewall_id

    def __repr__(self) -> str:
        """Return string representation of the object."""
        return f"Firewall({self._firewall_id})"

    def _repr_html_(self) -> str:
        """Return HTML representation of the object."""
        info = {
            "Firewall ID": self._firewall_id,
            "Link": make_link(
                "https://" + self.get_link(), link_text="Firewall Overview Page"
            ),
        }
        return convert_dict_to_html(info)

    def get_config(self) -> dict:
        """Return the current config of the firewall.

        Warnings:
            The output of this method may be changing over time if the reference set
            source is set to a rolling window.
        """
        firewall = self._get_firewall()
        typed_config = firewall.typed_cli_config
        if not typed_config or swagger_is_empty(typed_config):
            config_proto = firewall.cli_config
            return json.loads(config_proto.data.decode("utf-8"))
        return typed_config.to_dict()

    @deprecated("get_stress_test_config is deprecated, use get_config instead.")
    def get_stress_test_config(self) -> dict:
        """Return the current stress test config.

        Deprecated version of get_config.

        :meta private:
        """
        return self.get_config()

    def _get_batch_metadata(self) -> RimeBatchMetadata:
        """Return batch metadata for firewall."""
        firewall = self._get_firewall()
        return firewall.batch_metadata

    def get_metric_thresholds(self) -> pd.DataFrame:
        """Return the current thresholds for metrics tracked over time.

        Returns:
            A Pandas DataFrame where each row is a threshold for a
            different metric and each column is a threshold attribute.
        """
        bm = self._get_batch_metadata()
        parsed_thresholds = []
        for proto_threshold_info in bm.threshold_infos:
            threshold_dict = proto_threshold_info.to_dict()
            parsed_thresholds.append(threshold_dict)
        # Reorder DataFrame columns so metric_name is always first.
        metric_threshold_df = pd.DataFrame(parsed_thresholds).reindex(
            DEFAULT_THRESHOLD_INFO_KEY_ORDER, axis=1
        )
        return metric_threshold_df

    def update_metric_thresholds(
        self,
        metric_name: str,
        low: Optional[float] = None,
        medium: Optional[float] = None,
        high: Optional[float] = None,
        disabled: Optional[bool] = None,
    ) -> RimeUpdateFirewallResponse:
        """Update the current threshold for a metric tracked over time."""
        bm = self._get_batch_metadata()
        valid_metric_names = [threshold.metric_name for threshold in bm.threshold_infos]
        if metric_name not in valid_metric_names:
            raise ValueError(f"Firewall does not currently track metric {metric_name}.")
        if low is not None and not isinstance(low, numbers.Number):
            raise ValueError(f"Low severity threshold must be a number. Got {low}")
        if medium is not None and not isinstance(medium, numbers.Number):
            raise ValueError(
                f"Medium severity threshold must be a number. Got {medium}"
            )
        if high is not None and not isinstance(high, numbers.Number):
            raise ValueError(f"High severity threshold must be a number. Got {high}")
        if disabled is not None and not isinstance(disabled, bool):
            raise ValueError("disabled must be a boolean value.")

        parsed_thresholds = []
        for existing_proto_threshold_info in bm.threshold_infos:
            existing_metric_name = existing_proto_threshold_info.metric_name
            threshold_dict = existing_proto_threshold_info.to_dict()
            if existing_metric_name == metric_name:
                new_low = low if low is not None else threshold_dict["low"]
                new_medium = medium if medium is not None else threshold_dict["medium"]
                new_high = high if high is not None else threshold_dict["high"]
                if (
                    new_low == new_medium  # pylint: disable=consider-using-in
                    or new_medium == new_high  # pylint: disable=consider-using-in
                ):
                    print(
                        f"WARNING: setting equal thresholds is not recommended.\n"
                        f"Current thresholds for [{metric_name}]: "
                        f"Low {new_low}, Medium {new_medium}, High {new_high}."
                    )
                updated_threshold_info = RimeThresholdInfo(
                    metric_name=metric_name,
                    direction=threshold_dict["direction"],
                    low=new_low,
                    medium=new_medium,
                    high=new_high,
                    disabled=disabled
                    if disabled is not None
                    else threshold_dict["disabled"],
                )
                parsed_thresholds.append(updated_threshold_info)
            else:
                existing_threshold_info = RimeThresholdInfo(**threshold_dict)
                parsed_thresholds.append(existing_threshold_info)
        return self._update_firewall_components(metric_thresholds=parsed_thresholds)

    def get_scheduled_ct_info(self) -> Tuple[bool, dict]:
        """Return the status of scheduled CT and the location data is pulled from.

        Returns:
            Tuple[bool, dict]:
                The first value is a boolean indicating whether
                Scheduled CT has been activated. The second is a dictionary
                containing information about the data location used to run CT.

        Example:

        .. code-block:: python

            # Understand if Scheduled CT is running and from which location data is pulled from.
            is_ct_activated, location_args = firewall.get_scheduled_ct_info()
        """
        firewall = self._get_firewall()
        schedule_status = firewall.run_ct_schedule
        data_location_info = firewall.data_location_info
        data_location_dict = data_location_info.to_dict()
        return schedule_status, data_location_dict

    def get_firewall_rules(self) -> dict:
        """Return the current firewall rules."""
        firewall = self._get_firewall()
        config_proto = firewall.firewall_rules
        return json.loads(config_proto.data.decode("utf-8"))

    def get_data_collector(self) -> DataCollector:
        """Get Data Collector, create if None."""
        if self._data_collector is None:
            self._data_collector = DataCollector(self._api_client, self._firewall_id)
        return self._data_collector

    def delete_firewall(self) -> None:
        """Delete firewall."""
        with RESTErrorHandler():
            api = swagger_client.FirewallServiceApi(self._api_client)
            api.firewall_service_delete_firewall(firewall_id=self._firewall_id)

    def _update_firewall(self, **update_params: Any) -> RimeUpdateFirewallResponse:
        req = FirewallFirewallIdBody(**update_params)
        with RESTErrorHandler():
            api = swagger_client.FirewallServiceApi(self._api_client)
            return api.firewall_service_update_firewall_test_run_id(
                body=req, firewall_id=self._firewall_id
            )

    def update_firewall_stress_test_run(
        self, stress_test_run_id: str
    ) -> RimeUpdateFirewallResponse:
        """Update firewall with stress test run id.

        Arguments:
            stress_test_run_id: Stress Test Run ID to configure new firewall

        Returns:
            UpdateFirewallResponse

        Raises:
            ValueError
                If the provided status_filters array has invalid values.
                If the request to the ModelTest service failed.
        """
        return self._update_firewall(stress_test_run_id=stress_test_run_id)

    def update_stress_test_config(
        self, stress_test_config: Dict[str, Any]
    ) -> RimeUpdateFirewallResponse:
        """Update firewall with stress test config.

        Arguments:
            stress_test_config: Stress Test Config to configure new firewall

        Returns:
            UpdateFirewallResponse

        Raises:
            ValueError
                If the provided values are improperly formatted
                If the request to the ModelTest service failed.

        Warnings:
            Updating the stress test config also resets firewall thresholds and rules.
        """
        return self._update_firewall_components(stress_test_config=stress_test_config)

    def activate_ct_schedule(
        self,
        location_type: str,
        location_info: Optional[Dict] = None,
        data_params: Optional[Dict] = None,
        rolling_window_duration: Optional[timedelta] = None,
        reference_set_time_bin: Optional[Tuple[datetime, datetime]] = None,
    ) -> RimeUpdateFirewallResponse:
        """Activate CT Schedule for this firewall with a given data type.

        Arguments:
            location_type: Type of location that ScheduledCT will pull data from.
            location_info: Information needed to access the data location provided.
            data_params: Optional[Dict]
                Information needed to process data from the data location provided.
                By default, these are obtained from your reference information.
                Eg. `pred_col`, `timestamp_col`, `label_col`, etc...
            rolling_window_duration: Optional[timedelta]
                Fixed Time duration of rolling window
            reference_set_time_bin: Optional[Tuple[datetime, datetime]]
                Start and end times of fixed time bin

        Returns:
            UpdateFirewallResponse

        Raises:
            ValueError
                If the schedule has already been activated
                If the data_type is invalid
                If the request to the Firewall service failed
        """
        firewall = self._get_firewall()
        if firewall.run_ct_schedule:
            raise ValueError("Scheduler already activated")

        stress_test_id, data_location_info = self._get_location_update_info(
            location_type, location_info, data_params
        )
        reference_set_source = get_reference_set_source(
            rolling_window_duration=rolling_window_duration,
            reference_set_time_bin=reference_set_time_bin,
        )
        return self._update_firewall(
            run_ct_schedule=True,
            stress_test_run_id=stress_test_id,
            data_location_info=data_location_info,
            reference_set_source=reference_set_source,
        )

    def deactivate_ct_schedule(self) -> RimeUpdateFirewallResponse:
        """Deactivate CT Schedule for this firewall.

        Returns:
            UpdateFirewallResponse

        Raises:
            ValueError
                If the request to the ModelTest service failed
        """
        return self._update_firewall_components(run_ct_schedule=False)

    def _get_firewall(self) -> RimeFirewall:
        with RESTErrorHandler():
            api = swagger_client.FirewallServiceApi(self._api_client)
            res = api.firewall_service_list_firewalls(firewall_ids=[self._firewall_id])
        return res.firewalls[0]

    def _get_location_update_info(
        self,
        location_type: str,
        location_info: Optional[Dict] = None,
        data_params: Optional[Dict] = None,
    ) -> Tuple[str, RimeDataLocation]:
        """Return all info needed to update location."""
        firewall = self._get_firewall()
        stress_test_id = firewall.stress_test_run_id

        data_type = self._get_data_type()

        data_location_info = location_args_to_data_location_swagger(
            location_type, location_info, data_params, data_type
        )
        return stress_test_id, data_location_info

    def update_location_info(
        self,
        location_type: str,
        location_info: Optional[Dict] = None,
        data_params: Optional[Dict] = None,
        rolling_window_duration: Optional[timedelta] = None,
        reference_set_time_bin: Optional[Tuple[datetime, datetime]] = None,
    ) -> RimeUpdateFirewallResponse:
        """Update the location associated with this firewall.

        Arguments:
            location_type: Type of location that the firewall is associated with.
            location_info: Information needed to access the data location provided.
            data_params: Optional[Dict]
                Information needed to process data from the data location provided.
                By default, these are obtained from your reference information.
                Eg. `pred_col`, `timestamp_col`, `label_col`, etc...
            rolling_window_duration: Optional[timedelta]
                Fixed Time duration of rolling window
            reference_set_time_bin: Optional[Tuple[datetime, datetime]]
                Start and end times of fixed time bin

        Returns:
            UpdateFirewallResponse

        Raises:
            ValueError
                If the location_type, location_info or data_params are invalid
                If the request to the Firewall service failed
        """
        stress_test_id, data_location_info = self._get_location_update_info(
            location_type, location_info, data_params
        )
        reference_set_source = get_reference_set_source(
            rolling_window_duration=rolling_window_duration,
            reference_set_time_bin=reference_set_time_bin,
        )
        return self._update_firewall(
            stress_test_run_id=stress_test_id,
            data_location_info=data_location_info,
            reference_set_source=reference_set_source,
        )

    def _update_firewall_components(
        self,
        stress_test_config: Optional[Dict[str, Any]] = None,
        firewall_rules: Optional[dict] = None,
        metric_thresholds: Optional[List[RimeThresholdInfo]] = None,
        run_ct_schedule: Optional[bool] = None,
        location_type: Optional[str] = None,
        location_info: Optional[Dict] = None,
        data_params: Optional[Dict] = None,
        rime_managed_image: Optional[str] = None,
    ) -> RimeUpdateFirewallResponse:
        """Update the firewall components manually.

        Only valid non-null arguments are updated.

        Arguments:
            cli_config: CLI Config to update the firewall with.
            firewall_rules: Firewall Rules to update the firewall with.
            metric_thresholds: Threshold info for each summary metric.
            run_ct_schedule: Flag for ct scheduler.
            location_type: Type of location that ScheduledCT will pull data from.
            location_info: Information needed to access the data location provided.
            data_params: Optional[Dict]
                Information needed to process data from the data location provided.
                By default, these are obtained from your reference information.
                Eg. `pred_col`, `timestamp_col`, `label_col`, etc...
            rime_managed_image: Optional[str]
                Name of a managed image to use when running the model test.
                The image must have all dependencies required by your model. To create
                new managed images with your desired dependencies, use the client's
                ``create_managed_image()`` method.


        Returns:
            UpdateFirewallResponse

        Raises:
            ValueError
                If the provided values are improperly formatted
                If the request to the ModelTest service failed.
        """
        components_kwargs: Dict[str, Any] = {}
        data_type = self._get_data_type()
        if stress_test_config is not None:
            typed_cli_config = convert_config_to_swagger(stress_test_config, data_type)
            components_kwargs["typed_cli_config"] = typed_cli_config
        if firewall_rules is not None:
            components_kwargs["firewall_rules"] = RimeFirewallRules(
                data=json.dumps(firewall_rules).encode("utf-8")
            )
        if metric_thresholds is not None:
            components_kwargs["threshold_infos"] = metric_thresholds
        components = (
            RimeFirewallComponents(**components_kwargs) if components_kwargs else None
        )
        req = ComponentsFirewallIdBody(components=components)

        # Prevent location info from being provided without location type
        if location_info is not None and location_type is None:
            raise ValueError("Must Specify both location type and location info.")
        if run_ct_schedule is not None:
            req.run_ct_schedule = run_ct_schedule
        if location_type is not None:
            location_args = location_args_to_data_location_swagger(
                location_type, location_info, data_params, data_type
            )
            req.data_location_info = location_args

        if rime_managed_image:
            req.managed_image = RimeManagedImageReference(name=rime_managed_image)

        with RESTErrorHandler():
            api = swagger_client.FirewallServiceApi(self._api_client)
            return api.firewall_service_update_firewall_components(
                body=req, firewall_id=self._firewall_id
            )

    def update_managed_image(
        self, rime_managed_image: str,
    ) -> RimeUpdateFirewallResponse:
        """Update the managed image associated with this firewall.

        rime_managed_image: str
            Name of a managed image to use when running the model test.
            The image must have all dependencies required by your model. To create
            new managed images with your desired dependencies, use the client's
            ``create_managed_image()`` method.
        """
        return self._update_firewall_components(rime_managed_image=rime_managed_image)

    def get_managed_image(self) -> str:
        """Return the name of the managed image associated with this firewall."""
        firewall = self._get_firewall()
        if firewall.managed_image:
            managed_image_name = firewall.managed_image.name
            if managed_image_name == "":
                return "No Managed Image On Firewall"
        else:
            return "No Managed Image on Firewall"
        return managed_image_name

    def get_link(self) -> str:
        """Get the web app URL to the firewall.

        This link directs to your organization's deployment of RIME.
        You can view more detailed information about the firewall
        in the web app, including helpful visualizations, key insights on your
        model's performance, and explanations of test results for each batch.

        Note: this is a string that should be copy-pasted into a browser.
        """
        firewall = self._get_firewall()
        return firewall.web_app_url.url

    def _get_data_type(self) -> str:
        """Get firewall data type."""
        with RESTErrorHandler():
            api = swagger_client.FirewallServiceApi(self._api_client)
            sres = api.firewall_service_get_service_metrics(
                firewall_id=self._firewall_id
            )
        return sres.input_type

    def _get_incremental_config_request(
        self,
        test_run_config: Dict,
        disable_firewall_events: bool,
        override_existing_bins: bool,
    ) -> RimeStartFirewallContinuousTestRequest:
        """Get incremental config request."""
        req = RimeStartFirewallContinuousTestRequest(
            firewall_id=self._firewall_id,
            disable_firewall_events=disable_firewall_events,
            override_existing_bins=override_existing_bins,
        )
        # TODO: this will eventually take in the config_dict in order to load format
        data_type = self._get_data_type()

        if "eval_data_info" in test_run_config:
            eval_data_info = test_run_config["eval_data_info"]
            test_run_config_type = eval_data_info.get("type", None)
            if test_run_config_type == "delta_lake":
                if "server_hostname" in eval_data_info or "http_path" in eval_data_info:
                    raise ValueError(
                        "Server hostname and http_path will be provided by "
                        "the specified data source name. They should not be specified "
                        "in the incremental CT config."
                    )

        swagger_config = convert_incremental_config_to_swagger(
            test_run_config, data_type
        )
        req.incremental_config = swagger_config
        return req

    @deprecated(
        "run_firewall_incremental_data is deprecated, "
        "use start_continuous_test instead."
    )
    def run_firewall_incremental_data(
        self,
        test_run_config: dict,
        disable_firewall_events: bool = True,
        override_existing_bins: bool = False,
        custom_image: Optional[RimeCustomImage] = None,
        rime_managed_image: Optional[str] = None,
        ram_request_megabytes: Optional[int] = None,
        cpu_request_millicores: Optional[int] = None,
    ) -> ContinuousTestJob:
        """Run firewall continuous tests.

        Deprecated version of run_continuous_tests.

        :meta private:
        """
        return self.start_continuous_test(
            test_run_config,
            disable_firewall_events=disable_firewall_events,
            override_existing_bins=override_existing_bins,
            custom_image=custom_image,
            rime_managed_image=rime_managed_image,
            ram_request_megabytes=ram_request_megabytes,
            cpu_request_millicores=cpu_request_millicores,
        )

    def start_continuous_test(
        self,
        test_run_config: dict,
        disable_firewall_events: bool = True,
        override_existing_bins: bool = False,
        custom_image: Optional[RimeCustomImage] = None,
        rime_managed_image: Optional[str] = None,
        ram_request_megabytes: Optional[int] = None,
        cpu_request_millicores: Optional[int] = None,
        agent_id: Optional[str] = None,
        data_source_id: Optional[str] = None,
    ) -> ContinuousTestJob:
        """Start a RIME model firewall test on the backend's ModelTesting service.

        This allows you to run Firewall Test job on the RIME
        backend. This will run firewall on a batch of tabular data.

        Arguments:
            test_run_config: dict
                Configuration for the test to be run, which specifies paths to
                the model and datasets to used for the test.
            custom_image: Optional[RimeCustomImage]
                Specification of a customized container image to use running the model
                test. The image must have all dependencies required by your model.
                The image must specify a name for the image and optional a pull secret
                (of type RimeCustomImagePullSecret) with the name of the kubernetes pull
                secret used to access the given image.
            rime_managed_image: Optional[str]
                Name of a managed image to use when running the model test.
                The image must have all dependencies required by your model. To create
                new managed images with your desired dependencies, use the client's
                ``create_managed_image()`` method.
            ram_request_megabytes: Optional[int]
                Megabytes of RAM requested for the stress test job. If none
                specified, will default to 4000MB. The limit is equal to the megabytes
                requested.
            cpu_request_millicores: Optional[int]
                Millicores of CPU requested for the stress test job. If none
                specified, will default to 1500mi. The limit is equal to millicores
                requested.
            agent_id: Optional[str]
                Identifier for the agent where the continuous test will be run.
                If not specified, the workspace's default agent is used.
            data_source_id: Optional[str]
                ID of the data source which is used in the arguments. Only
                Specify this if you are running a config that requires this source.

        Returns:
            A ``Job`` providing information about the model stress test
            job.

        Raises:
            ValueError
                If the request to the ModelTest service failed.

        Example:

        .. code-block:: python

            # This example will likely not work for you because it requires permissions
            # to a specific S3 bucket. This demonstrates how you might specify such a
            # configuration.
            incremental_config = {
                "eval_path": "s3://rime-datasets/
                   fraud_continuous_testing/eval_2021_04_30_to_2021_05_01.csv",
                "timestamp_col": "timestamp"
            }
            # Run the job using the specified config and the default Docker image in
            # the RIME backend. Use the RIME Managed Image "tensorflow115".
            # This assumes you have already created the Managed Image and waited for it
            # to be ready.
            firewall = rime_client.get_firewall("foo")
            job =
                firewall.run_firewall_incremental_data(
                    test_run_config=incremental_config,
                    rime_managed_image="tensorflow115",
                    ram_request_megabytes=8000,
                    cpu_request_millicores=2000)
        """
        # TODO(blaine): Add config validation service.
        if not isinstance(test_run_config, dict):
            raise ValueError("The configuration must be a dictionary")

        if custom_image and rime_managed_image:
            raise ValueError(
                "Cannot specify both 'custom_image' and 'rime_managed_image'"
            )

        if ram_request_megabytes is not None and ram_request_megabytes <= 0:
            raise ValueError(
                "The requested number of megabytes of RAM must be positive"
            )

        if cpu_request_millicores is not None and cpu_request_millicores <= 0:
            raise ValueError(
                "The requested number of millicores of CPU must be positive"
            )

        req = self._get_incremental_config_request(
            test_run_config, disable_firewall_events, override_existing_bins,
        )
        if custom_image:
            req.custom_image_type = RimeCustomImageType(testing_image=custom_image)
        if rime_managed_image:
            req.custom_image_type = RimeCustomImageType(
                managed_image=RimeManagedImageReference(name=rime_managed_image)
            )
        if ram_request_megabytes:
            req.ram_request_megabytes = ram_request_megabytes
        if cpu_request_millicores:
            req.cpu_request_millicores = cpu_request_millicores
        # This setup means that if agent_id = "", the request uses default agent id.
        if agent_id:
            req.agent_id = agent_id
        if data_source_id:
            req.data_source_id = data_source_id
        with RESTErrorHandler():
            Firewall._throttler.throttle(  # pylint: disable=W0212
                throttling_msg="Your request is throttled to limit # of model tests."
            )
            api = swagger_client.ModelTestingApi(self._api_client)
            job: RimeJobMetadata = api.model_testing_start_firewall_continuous_test(
                body=req
            ).job
        return ContinuousTestJob(self._api_client, job.job_id)

    def list_test_runs(self) -> Iterator[ContinuousTestRun]:
        """List the continuous test runs associated with this firewall."""
        with RESTErrorHandler():
            api = swagger_client.FirewallServiceApi(self._api_client)
            interval = None
            while True:
                if not interval:
                    res = api.firewall_service_list_test_run_summaries(
                        firewall_id=self._firewall_id,
                    )
                else:
                    res = api.firewall_service_list_test_run_summaries(
                        firewall_id=self._firewall_id,
                        interval_start_time_epoch_seconds=interval.start_time_epoch_seconds,  # pylint: disable=line-too-long
                        interval_end_time_epoch_seconds=interval.end_time_epoch_seconds,
                    )
                if not res.summaries or len(res.summaries) == 0:
                    break
                for batch_summary in res.summaries:
                    metadata = batch_summary.batch_result_metadata
                    start_time = metadata.start_time_epoch_seconds
                    end_time = metadata.end_time_epoch_seconds
                    test_run_id = metadata.test_run_id
                    test_run = ContinuousTestRun(
                        self._api_client, test_run_id, (start_time, end_time)
                    )
                    yield test_run
                # The batch summaries are sorted in reverse chronological order.
                # Construct the interval for the next page by using the previous
                # start time as the end time for the next interval.
                next_end_time = res.interval.start_time_epoch_seconds
                next_start_time_sec = (
                    next_end_time.timestamp() - LIST_TEST_RUNS_INTERVAL_LENGTH_SECONDS
                )
                next_start_time = datetime.fromtimestamp(next_start_time_sec)

                next_interval = RimeTimeRange(
                    start_time_epoch_seconds=serialize_datetime_to_proto_timestamp(
                        next_start_time
                    ),
                    end_time_epoch_seconds=serialize_datetime_to_proto_timestamp(
                        next_end_time
                    ),
                )
                interval = next_interval

    def get_model_status(self, test_run_id: Optional[str] = None) -> pd.DataFrame:
        """Return the model status of the firewall in detail.

        Args:
            test_run_id: an optional string. if not specified, will obtain the
            model status corresponding to the latest test run.

        Returns a Pandas Dataframe with the following columns:
            1. name: Name of the metric
            2. value: Value of the metric
            3. severity: Severity of the metric
            4. disabled: Whether or not the metric is disabled
        """
        with RESTErrorHandler():
            api = swagger_client.FirewallServiceApi(self._api_client)
            if test_run_id:
                res = api.firewall_service_get_model_status(
                    firewall_id=self._firewall_id, test_run_id=test_run_id
                )
            else:
                res = api.firewall_service_get_model_status(
                    firewall_id=self._firewall_id
                )
        res_dict: dict = {
            "name": [],
            "value": [],
            "severity": [],
            "disabled": [],
        }
        if res.issues:
            for issue in res.issues:
                res_dict["name"].append(issue.name)
                res_dict["value"].append(issue.value)
                res_dict["severity"].append(issue.severity)
                res_dict["disabled"].append(issue.disabled)
        return pd.DataFrame.from_dict(res_dict)


def get_reference_set_source(
    rolling_window_duration: Optional[timedelta] = None,
    reference_set_time_bin: Optional[Tuple[datetime, datetime]] = None,
    file_path: Optional[str] = None,
) -> Optional[RimeReferenceSetSource]:
    """Get reference set source protobuf message.

    At most one of the arguments should be provided.

    Arguments:
        rolling_window_duration: time duration of rolling window
        reference_set_time_bin: start and end times of fix time bin
        file_path: location of reference set in S3 bucket.
    """
    num_reference_set_args = sum(
        [
            rolling_window_duration is not None,
            reference_set_time_bin is not None,
            file_path is not None,
        ]
    )
    if num_reference_set_args > 1:
        raise ValueError(
            "At most one of `rolling_window_seconds`, `reference_set_time_bin` or "
            f"`file_path` may be set but {num_reference_set_args} were provided."
        )
    elif rolling_window_duration is not None:
        return RimeReferenceSetSource(
            rolling_window_seconds=str(rolling_window_duration.total_seconds())
        )
    elif reference_set_time_bin is not None:
        start_time, end_time = reference_set_time_bin
        reference_set_time_bin_range = RimeTimeRange(
            start_time_epoch_seconds=serialize_datetime_to_proto_timestamp(start_time),
            end_time_epoch_seconds=serialize_datetime_to_proto_timestamp(end_time),
        )
        return RimeReferenceSetSource(time_range=reference_set_time_bin_range)
    elif file_path is not None:
        return RimeReferenceSetSource(file_path=file_path)
    else:
        return None
