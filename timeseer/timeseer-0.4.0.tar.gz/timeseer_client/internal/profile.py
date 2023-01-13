"""Convenience functions to profile a time series."""

from typing import Dict, List, Tuple

from kukur import Metadata
from pyarrow import Table

from timeseer import SeriesSelector
from timeseer_client.internal import JSONFlightClient
from timeseer_client.internal.data_services import DataServices
from timeseer_client.internal.data_sets import DataSets
from timeseer_client.internal.flows import Flows
from timeseer_client.internal.resources import Resources


def profile(
    client: JSONFlightClient, name: str, many_series: List[Tuple[Metadata, Table]]
) -> List[Dict[str, str]]:
    """Profile time series.

    This creates a Data Set, Flow and Data Service with the given name.
    Waits until the flow has been evaluated.

    Args:
        client: The client for Timeseer.
        name: The name given to the data set, flow and data service that will be created.
        many_series: A list of metadata-data pairs for the time series to be profiled.

    Returns:
        The resources that have been created.
    """
    data_sets = DataSets(client)
    data_sets.remove_data(name)
    data_sets.upload_data(
        [(_ensure_source_name(name, metadata), data) for metadata, data in many_series]
    )

    resources = Resources(client)
    data_set_resource = resources.read(dict(type="data set", name=name))
    profile_resources = [
        dict(
            type="data service",
            name=name,
            kpiSet="Data quality fundamentals",
            range=data_set_resource["range"],
        ),
        dict(
            name=name,
            dataSet=name,
            blocks=[
                dict(name="Univariate analysis", type="univariate analysis"),
                dict(
                    name="Contribute to data service",
                    type="data_service_contribute",
                    dataServiceName=name,
                    contributionBlockNames=["Univariate analysis"],
                ),
            ],
        ),
    ]
    resources.create(profile_resources)

    flows = Flows(client)
    flows.evaluate(name)

    data_services = DataServices(client)
    data_services.wait_for_evaluation(name, name)

    return [
        dict(type=resource.get("type", "flow"), name=resource["name"])
        for resource in reversed([data_set_resource] + profile_resources)
    ]


def _ensure_source_name(name: str, metadata: Metadata) -> Metadata:
    selector = SeriesSelector(name, metadata.series.tags, metadata.series.field)
    new_metadata = Metadata(selector)
    for k, v in metadata.iter_names():
        new_metadata.set_field_by_name(k, v)
    return new_metadata
