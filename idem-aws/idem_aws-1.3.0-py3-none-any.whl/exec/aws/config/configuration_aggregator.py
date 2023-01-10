"""Exec module for Amazon Configuration Aggregator."""
from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict:
    """Get a Configuration Aggregator resource from AWS for a given name or resource_id.

    Args:
        name(str):
            The name of the Configuration Aggregator.

        resource_id(str, Optional):
            AWS Configuration Aggregator id to identify the resource.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_configuration_aggregators

    Examples:
        Calling from the CLI:

        .. code-block:: bash

            $ idem exec aws.config.configuration_aggregator.get name="name"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.config.configuration_aggregator.get
                - kwargs:
                    name: "unmanaged_configuration_aggregator"
    """
    result = dict(comment=[], ret=None, result=True)
    if not resource_id:
        resource_id = name
    configuration_aggregator = (
        await hub.exec.boto3.client.config.describe_configuration_aggregators(
            ctx, ConfigurationAggregatorNames=[name]
        )
    )
    if not configuration_aggregator["result"]:
        if "NoSuchConfigurationAggregatorException" in str(
            configuration_aggregator["comment"]
        ):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.config.configuration_aggregator", name=name
                )
            )
            result["comment"] += list(configuration_aggregator["comment"])
            return result
        result["comment"] += list(configuration_aggregator["comment"])
        result["result"] = False
        return result
    if not ((configuration_aggregator["ret"])["ConfigurationAggregators"]):
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.config.configuration_aggregator", name=name
            )
        )
        return result

    ret = await hub.tool.aws.config.conversion_utils.convert_raw_config_aggregator_to_present(
        ctx,
        raw_resource=((configuration_aggregator["ret"])["ConfigurationAggregators"])[0],
    )
    result["ret"] = ret
    return result


async def list_(hub, ctx, names: List[str] = None) -> Dict:
    """Get a Configuration Aggregator resources from AWS.

    Args:
        names(List[str] = Optional):
            The name of the Configuration Aggregators.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_configuration_aggregators

    Examples:
        Calling from the CLI:

        .. code-block:: bash

            $ idem exec aws.config.configuration_aggregator.list configuration_aggregator_names="names"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.config.configuration_aggregator.list
                - kwargs:
                    configuration_aggregator_names: ["unmanaged_configuration_aggregator"]
    """
    result = dict(comment=[], ret=[], result=True)
    configuration_aggregators = (
        await hub.exec.boto3.client.config.describe_configuration_aggregators(
            ctx, ConfigurationAggregatorNames=names
        )
    )
    if not configuration_aggregators["result"]:
        result["comment"] = configuration_aggregators["comment"]
        result["result"] = False
        return result

    for configuration_aggregator in configuration_aggregators["ret"][
        "ConfigurationAggregators"
    ]:
        resource_translated = await hub.tool.aws.config.conversion_utils.convert_raw_config_aggregator_to_present(
            ctx, raw_resource=configuration_aggregator
        )
        result["ret"].append(resource_translated)
    result["comment"] = "Found Configuration Aggregators"
    return result
