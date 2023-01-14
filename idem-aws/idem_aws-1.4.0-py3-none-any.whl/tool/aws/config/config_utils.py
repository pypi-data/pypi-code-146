from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List


async def is_resource_updated(
    hub,
    before: Dict[str, Any],
    role_arn: str,
    recording_group: Dict,
):
    if role_arn != before.get("role_arn"):
        return True

    if recording_group != before.get("recording_group"):
        return True

    return False


async def convert_raw_config_aggregator_to_present(
    hub, ctx, raw_resource: Dict[str, Any]
) -> Dict[str, Any]:
    # name is the unique identifier for Config so it is set as resource_id
    resource_id = raw_resource.get("ConfigurationAggregatorName")

    resource_parameters = OrderedDict(
        {
            "name": "name",
            "ConfigurationAggregatorName": "name",
            "ConfigurationAggregatorName": "resource_id",
            "AccountAggregationSources": "account_aggregation_sources",
            "OrganizationAggregationSource": "organization_aggregation_source",
        }
    )
    resource_translated = {"name": resource_id, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)
    return resource_translated


async def is_account_agg_source_list_equal(
    hub, new_list: List[Dict], old_list: List[Dict]
):
    new_list.sort()
    old_list.sort()
    return new_list == old_list


async def is_congiguration_aggregator_updated(
    hub,
    before: Dict[str, Any],
    account_aggregation_sources: List[Dict],
    organization_aggregation_source: Dict,
):
    # Flag to check if resource is updated or not
    resource_updated = False
    if (
        account_aggregation_sources is not None
        and before.get("account_aggregation_sources") is not None
    ):
        resource_updated = (
            await hub.tool.aws.config.config_utils.is_account_agg_source_list_equal(
                account_aggregation_sources, before.get("account_aggregation_sources")
            )
        )

    if (
        organization_aggregation_source is not None
        and before.get("organization_aggregation_source") is not None
    ):
        if organization_aggregation_source.get("RoleArn") != before.get(
            "organization_aggregation_source"
        ).get("RoleArn"):
            return False
        if (
            organization_aggregation_source.get("AllAwsRegions") is not None
            and before.get("organization_aggregation_source").get("AllAwsRegions")
            is not None
        ):
            if organization_aggregation_source.get("AllAwsRegions") != before.get(
                "organization_aggregation_source"
            ).get("AllAwsRegions"):
                return False
        return await hub.tool.aws.config.config_utils.is_account_agg_source_list_equal(
            organization_aggregation_source.get("AwsRegions"),
            before.get("organization_aggregation_source").get("AwsRegions"),
        )

    return resource_updated
