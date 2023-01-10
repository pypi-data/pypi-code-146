from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List

from dict_tools import differ


async def search_raw(
    hub,
    ctx,
    resource_id: str = None,
    load_balancer_arn: str = None,
) -> Dict:
    """
    1. Describes specified listeners or the listeners for the specified Application Load Balancer,
        Network Load Balancer or Gateway Load Balancer.
    2. You must specify either a load balancer or one or more listeners. The return will be in the same
        format as what boto3 api returns.
    3. Here, resource_id get higher priority in search than load_balancer_arn i.e. if both load_balancer_arn
        and resource_id are not None, search is done with resource_id than load_balancer_arn.

    Args:
        resource_id(str, Optional):
            AWS ELBv2 Listener ARN to identify the resource.

        load_balancer_arn(str, Optional):
            The Amazon Resource Name (ARN) of the load balancer.

    Returns:
        {"result": True|False, "comment": A message List, "ret": Dict}

    """
    ret = result = dict(comment=[], ret=None, result=True)
    if resource_id:
        ret = await hub.exec.boto3.client.elbv2.describe_listeners(
            ctx,
            ListenerArns=[resource_id],
        )
    elif load_balancer_arn:
        ret = await hub.exec.boto3.client.elbv2.describe_listeners(
            ctx,
            LoadBalancerArn=load_balancer_arn,
        )
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]
    return result


async def update(
    hub,
    ctx,
    name: str,
    current_state: Dict[str, Any],
    input_map: Dict[str, Any],
    resource_id: str,
    plan_state: Dict[str, Any],
):
    """
    1. Replaces the specified properties of the specified listener. Any property that is not updated, remains unchanged.
    2. Changing the protocol from HTTPS to HTTP, or from TLS to TCP, removes the security policy and default certificate
       properties. If you change the protocol from HTTP to HTTPS, or from TCP to TLS, you must add the security policy
       and default certificate properties.
    3. To add an item to a list, remove an item from a list, or update an item in a list, you must provide the entire
       list. For example, to add an action, specify a list with the current actions plus the new action.
    4. Adds the specified SSL server certificate to the certificate list for the specified HTTPS/ TLS listener. If the
       certificate in already in the certificate list, the call is successful but the certificate is not added again.
    5. Removes the specified certificate from the certificate list for the specified HTTPS or TLS listener.

    Args:
        name(str):
            The name of the AWS ElasticLoadBalancingv2 Listener.

        current_state(dict[str, Any]):
            response returned by describe on an AWS ElasticLoadBalancingv2 Listener

        input_map(dict[str, Any]):
            a dictionary with newly passed values of params.

        resource_id(str):
            AWS ElasticLoadBalancingv2 Listener Amazon Resource Name (ARN).

        plan_state(dict[str, Any]):
            idem --test state for update on AWS ElasticLoadBalancingv2 Listener.

    Returns:
        {"result": True|False, "comment": A message List, "ret": None}
    """
    result = dict(comment=[], result=True, ret=[])
    if not ctx.get("test", False):
        if input_map:
            ret = compare_config(current_state=current_state, updated_state=input_map)
            if (ret["result"] and ret["ret"]) or input_map.get("default_actions"):
                modify_listener = await hub.exec.boto3.client.elbv2.modify_listener(
                    ctx,
                    ListenerArn=resource_id,
                    Port=ret["ret"].get("Port"),
                    Protocol=ret["ret"].get("Protocol"),
                    SslPolicy=ret["ret"].get("SslPolicy"),
                    Certificates=ret["ret"].get("DefaultCertificates"),
                    DefaultActions=input_map.get("default_actions"),
                    AlpnPolicy=ret["ret"].get("AlpnPolicy"),
                )
                if not modify_listener["result"]:
                    result["comment"] = list(modify_listener["comment"])
                    result["result"] = False
                    return result
                result["comment"].append("Modified Listener.")
                result["ret"].append(
                    {"modify_listener": modify_listener["ret"]["Listeners"][0]}
                )

        if input_map.get("certificates"):
            ret = compare_certificates(
                old_certificates=current_state.get("certificates"),
                new_certificates=input_map.get("certificates"),
            )
            if ret["ret"]:
                if ret["ret"].get("to_remove"):
                    remove_certificates = (
                        await hub.exec.boto3.client.elbv2.remove_listener_certificates(
                            ctx,
                            ListenerArn=resource_id,
                            Certificates=ret["ret"]["to_remove"],
                        )
                    )
                    if not remove_certificates["result"]:
                        result["comment"] += list(remove_certificates["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append("Removed Certificates.")
                    result["ret"].append(
                        {"remove_certificates": remove_certificates["ret"]}
                    )

                if ret["ret"].get("to_add"):
                    add_certificates = (
                        await hub.exec.boto3.client.elbv2.add_listener_certificates(
                            ctx,
                            ListenerArn=resource_id,
                            Certificates=ret["ret"]["to_add"],
                        )
                    )
                    if not add_certificates["result"]:
                        result["comment"] += list(add_certificates["comment"])
                        result["result"] = False
                        return result
                    result["comment"].append("Added Certificates.")
                    result["ret"].append({"add_certificates": add_certificates["ret"]})
    else:
        update_params = OrderedDict(
            {
                "name": name,
                "protocol": input_map.get("protocol"),
                "port": input_map.get("port"),
                "ssl_policy": input_map.get("ssl_policy"),
                "certificates": input_map.get("certificates"),
                "default_certificates": input_map.get("default_certificates"),
                "alpn_policy": input_map.get("alpn_policy"),
                "tags": input_map.get("tags"),
                "resource_id": resource_id,
            }
        )

        if compare_default_actions(
            current_state.get("default_actions"), input_map.get("default_actions")
        )["ret"]:
            plan_state["default_actions"] = input_map["default_actions"]

        for key, value in update_params.items():
            if value is not None:
                plan_state[key] = value
        result["ret"] = plan_state
    return result


def compare_certificates(
    old_certificates: List[Dict[str, Any]] = None,
    new_certificates: List[Dict[str, Any]] = None,
):
    """
    Compares old_certificates and new_certificates and return the new list of certificates that need to be updated.

    Args:
        old_certificates(list[dict[str, Any]]):
            Existing list of certificates to be removed from AWS ElasticLoadBalancingv2 Listener.

        new_certificates(list[dict[str, Any]]):
            Newer list of certificates to be added to AWS ElasticLoadBalancingv2 Listener.

    Returns: Dict[str, Dict]

    """
    result = dict(ret=None)
    to_remove = []
    to_add = []
    old_certificates_map = {
        certificate.get("CertificateArn"): certificate
        for certificate in old_certificates or []
    }
    if new_certificates is not None:
        for certificate in new_certificates:
            if certificate.get("CertificateArn") in old_certificates_map:
                del old_certificates_map[certificate.get("CertificateArn")]
            else:
                to_add.append(certificate)
        to_remove = list(old_certificates_map.values())
        result["ret"] = {"to_add": to_add, "to_remove": to_remove}
    return result


def compare_default_actions(
    old_default_actions: List[Dict[str, Any]] = None,
    new_default_actions: List[Dict[str, Any]] = None,
):
    """
    Compares old_default_actions and new_default_actions and return the new list of default_actions that need to be updated.

    Args:
        old_default_actions(list[dict[str, Any]]):
            Existing list of default_actions to be removed from AWS ElasticLoadBalancingv2 Listener.

        new_default_actions(list[dict[str, Any]]):
            Newer list of default_actions to be added to AWS ElasticLoadBalancingv2 Listener.

    Returns: Dict[str, Dict]

    """
    result = dict(ret=None)
    to_remove = []
    to_add = []
    old_default_actions_map = {
        certificate.get("TargetGroupArn"): certificate
        for certificate in old_default_actions or []
    }
    if new_default_actions is not None:
        for certificate in new_default_actions:
            if certificate.get("TargetGroupArn") in old_default_actions_map:
                del old_default_actions_map[certificate.get("TargetGroupArn")]
            else:
                to_add.append(certificate)
        to_remove = list(old_default_actions_map.values())
        if to_add or to_remove:
            result["ret"] = {"to_add": to_add, "to_remove": to_remove}
    return result


def compare_config(current_state: Dict[str, Any], updated_state: Dict[str, Any]):
    """
    Compares listener's existing configuration with newly passed inputs and returns details of the diff.

    Args:
        current_state (dict[str, Any]):
            response returned by describe on an AWS ELBv2 Listener

        updated_state (dict[st, Any]):
            Newly passed values for update function as dictionary .

    Returns:
        {"result": True|False, "ret": Dict}

    """
    result = dict(result=False, ret={})
    target_group_params = {
        "Port": "port",
        "Protocol": "protocol",
        "SslPolicy": "ssl_policy",
        "AlpnPolicy": "alpn_policy",
        "DefaultCertificates": "default_certificates",
    }
    current_config_mapping = {}
    for name, value in target_group_params.items():
        if current_state.get(value):
            current_config_mapping[name] = current_state.get(value)

    updated_config_mapping = {}
    for name, value in target_group_params.items():
        if updated_state.get(value):
            updated_config_mapping[name] = updated_state.get(value)

    diff_in_config = differ.deep_diff(current_config_mapping, updated_config_mapping)

    if diff_in_config.get("new"):
        result["result"] = True
        result["ret"] = diff_in_config.get("new")

    return result
