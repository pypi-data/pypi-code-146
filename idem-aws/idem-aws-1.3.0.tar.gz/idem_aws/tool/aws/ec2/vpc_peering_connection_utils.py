"""Util module for managing VPC Peering Connection."""
from typing import Any
from typing import Dict
from typing import List


async def search_raw(
    hub,
    ctx,
    filters: List = None,
    resource_id: str = None,
) -> Dict:
    """Fetch one or more VPC peering connections from AWS.

    The return will be in the same format as what the boto3 api returns.

    Args:
        resource_id(str, Optional):
            AWS VPC peering connection id to identify the resource.

        filters(str, Optional): One or more filters: for example, tag :<key>, tag-key.
            A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpc_peering_connections

    Returns:
        {"result": True|False, "comment": A message List, "ret": Dict}
    """
    result = dict(comment=[], ret=None, result=True)
    syntax_validation = hub.tool.aws.search_utils.search_filter_syntax_validation(
        filters=filters
    )
    if not syntax_validation["result"]:
        result["comment"] = list(syntax_validation["comment"])
        return result
    boto3_filter = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
        filters=filters
    )
    ret = await hub.exec.boto3.client.ec2.describe_vpc_peering_connections(
        ctx,
        Filters=boto3_filter,
        VpcPeeringConnectionIds=[resource_id] if resource_id else None,
    )
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]

    return result


async def get_vpc_peering_connection_raw(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    resource_type: str = None,
    filters: List = None,
) -> Dict:
    """Get the raw vpc peering connection resource.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str, Optional):
            AWS VPC peering connection id to identify the resource.

        resource_type(str):
            The type of the resource.

        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key.
            A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpc_peering_connections

    Returns:
        {"result": True|False, "comment": A list of messages - strings, "ret": The raw resource}
    """
    result = dict(comment=[], ret=None, result=True)
    vpc_peering_connection_ret = (
        await hub.tool.aws.ec2.vpc_peering_connection_utils.search_raw(
            ctx=ctx,
            resource_id=resource_id,
            filters=filters,
        )
    )
    if not vpc_peering_connection_ret["result"]:
        if "InvalidVpcPeeringConnectionID.NotFound" in str(
            vpc_peering_connection_ret["comment"]
        ):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type=resource_type, name=name
                )
            )
            result["comment"] += list(vpc_peering_connection_ret["comment"])
            return result
        result["comment"] += list(vpc_peering_connection_ret["comment"])
        result["result"] = False
        return result
    if not vpc_peering_connection_ret["ret"]["VpcPeeringConnections"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type=resource_type, name=name
            )
        )
        return result

    resource = vpc_peering_connection_ret["ret"]["VpcPeeringConnections"][0]
    if len(vpc_peering_connection_ret["ret"]["VpcPeeringConnections"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_type=resource_type, resource_id=resource_id
            )
        )

    result["ret"] = resource

    return result


async def update_vpc_peering_connection_options(
    hub,
    ctx,
    name,
    vpc_peering_connection_id: str,
    initial_options_ret: Dict[str, Any],
    new_options: Dict[str, bool],
) -> Dict[str, Any]:
    """Update VPC peering connection options.

    Args:
        vpc_peering_connection_id(str):
            AWS vpc peering connection resource id

        name(str):
            The name of the idem resource.

        initial_options_ret(dict[str, True|False]):
            Dictionary of the CURRENT VPC peering connection options for the accepter and the requester.

        new_options(dict[str, True|False]):
            Dictionary of the NEW VPC peering connection options for the accepter and the requester.

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": dict of updated options}
    """
    result = dict(comment=(), result=True, ret=None)

    # Create the existing options' dictionary by containing
    # only the options properties and not the resource_id, name etc.
    existing_options = {
        key: initial_options_ret["ret"][key]
        for key in initial_options_ret["ret"].keys() & new_options.keys()
    }

    if not new_options or all(value is None for value in new_options.values()):
        return result

    if None in new_options.values():
        for key, value in new_options.items():
            if value is None:
                new_options[key] = existing_options[key]

    if new_options != existing_options:
        if not ctx.get("test", False):
            modify_options_ret = (
                await hub.exec.boto3.client.ec2.modify_vpc_peering_connection_options(
                    ctx,
                    **{
                        "AccepterPeeringConnectionOptions": {
                            "AllowDnsResolutionFromRemoteVpc": new_options[
                                "peer_allow_remote_vpc_dns_resolution"
                            ],
                            "AllowEgressFromLocalClassicLinkToRemoteVpc": new_options[
                                "peer_allow_classic_link_to_remote_vpc"
                            ],
                            "AllowEgressFromLocalVpcToRemoteClassicLink": new_options[
                                "peer_allow_vpc_to_remote_classic_link"
                            ],
                        },
                        "RequesterPeeringConnectionOptions": {
                            "AllowDnsResolutionFromRemoteVpc": new_options[
                                "allow_remote_vpc_dns_resolution"
                            ],
                            "AllowEgressFromLocalClassicLinkToRemoteVpc": new_options[
                                "allow_classic_link_to_remote_vpc"
                            ],
                            "AllowEgressFromLocalVpcToRemoteClassicLink": new_options[
                                "allow_vpc_to_remote_classic_link"
                            ],
                        },
                        "VpcPeeringConnectionId": vpc_peering_connection_id,
                    },
                )
            )

            if not modify_options_ret["result"]:
                result["comment"] = modify_options_ret["comment"]
                result["result"] = False
                return result

        if result["result"]:
            # See which values are different in the dictionary and add those in ret property
            result["ret"] = {
                key: new_options[key]
                for key in existing_options
                if new_options[key] != existing_options[key]
            }

    if ctx.get("test", False):
        result[
            "comment"
        ] = hub.tool.aws.comment_utils.would_update_resource_options_comment(
            "aws.ec2.vpc_peering_connection_options",
            name,
            vpc_peering_connection_id,
        )
    else:
        result["comment"] = hub.tool.aws.comment_utils.update_resource_options_comment(
            "aws.ec2.vpc_peering_connection_options",
            name,
            vpc_peering_connection_id,
        )

    return result


async def activate_vpc_peering_connection(
    hub,
    ctx,
    resource_type: str,
    name: str,
    vpc_peering_connection_id: str,
    current_status: str,
    new_status: str,
) -> Dict[str, Any]:
    """Accept VPC peering connection - set the status to active.

    Args:
        resource_type(str):
            The AWS resource type.

        name(str):
            The name of the idem resource.

        vpc_peering_connection_id(str):
            AWS vpc peering connection resource id

        current_status(str):
            The CURRENT status of the VPC peering connection.

        new_status(str):
            The NEW status of the VPC peering connection.

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": dict of updated status}
    """
    result = dict(comment=(), result=True, ret=None)
    if (
        current_status != "pending-acceptance"
        and current_status != "initiating-request"
    ) or new_status != "active":
        result["comment"] += (
            "Status could not be updated because either the old status is not pending-acceptance or "
            "the new one is not active ",
        )
        result["result"] = False
        return result

    if not ctx.get("test", False):
        accept_ret = await hub.exec.boto3.client.ec2.accept_vpc_peering_connection(
            ctx, VpcPeeringConnectionId=vpc_peering_connection_id
        )

        if not accept_ret["result"]:
            result["comment"] = accept_ret["comment"]
            result["result"] = False
            return result

    if result["result"]:
        # If the connection status is accepted, it means the status is "active"
        result["ret"] = {"connection_status": "active"}

    if ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_update_status_comment(
            resource_type,
            name,
            vpc_peering_connection_id,
            new_status,
        )
    else:
        result["comment"] = hub.tool.aws.comment_utils.update_status_comment(
            resource_type,
            name,
            vpc_peering_connection_id,
            new_status,
        )

    return result
