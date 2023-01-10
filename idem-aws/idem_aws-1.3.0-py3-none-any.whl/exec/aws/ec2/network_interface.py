from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str = None,
    resource_id: str = None,
    filters: List = None,
) -> Dict:
    """
    Get a Network Interface resource from AWS. Supply one of the inputs as the filter.

    Args:
        name(str): The name of the Idem state.
        resource_id(str, Optional): AWS Network Interface id to identify the resource.
        filters(list, Optional): One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
         https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_network_interfaces

    """
    result = dict(comment=[], ret=None, result=True)
    if filters:
        filters = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
            filters=filters
        )

    if resource_id:
        ret = await hub.exec.boto3.client.ec2.describe_network_interfaces(
            ctx,
            NetworkInterfaceIds=[resource_id],
            Filters=filters,
        )
    else:
        ret = await hub.exec.boto3.client.ec2.describe_network_interfaces(
            ctx,
            Filters=filters,
        )

    # If there was an error in the call then report failure
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    present_states = hub.tool.aws.ec2.network_interface.convert_to_present(ctx, ret.ret)

    # If the resource can't be found but there were no results then "result" is True and "ret" is None
    if not present_states:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.network_interface", name=name
            )
        )
        return result

    # return the first result as a plain dictionary
    result["ret"] = next(iter((present_states).values()))

    return result


async def list_(hub, ctx, name: str = None, filters: List = None) -> Dict:
    """
    Use an un-managed Network INterface as a data-source. Supply one of the inputs as the filter.

    Args:
        name(str, Optional):
            The name of the Idem state.

        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_network_interfaces

    """

    result = dict(comment=[], ret=[], result=True)
    if filters:
        filters = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
            filters=filters
        )
    ret = await hub.exec.boto3.client.ec2.describe_network_interfaces(
        ctx,
        Filters=filters,
    )

    # If there was an error in the call then report failure
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    present_states = hub.tool.aws.ec2.network_interface.convert_to_present(ctx, ret.ret)
    if not present_states:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.network_interface", name=name
            )
        )
        return result

    # Return a list of dictionaries with details about all the instances
    result["ret"] = list(present_states.values())

    return result
