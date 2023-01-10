"""State module for managing Amazon Organizations Policy Attachments."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]

TREQ = {
    "present": {
        "require": [
            "aws.organizations.organization.present",
            "aws.organizations.organization_unit.present",
            "aws.organizations.account.present",
            "aws.organizations.policy.present",
        ],
    },
}


async def present(
    hub, ctx, name: str, policy_id: str, target_id: str
) -> Dict[str, Any]:
    """Attaches a policy to a root, an organizational unit (OU), or an individual account.

    How the policy affects accounts depends on the type of policy. The only supported policy types are
    ``SERVICE_CONTROL_POLICY``, ``AISERVICES_OPT_OUT_POLICY``, ``TAG_POLICY`` and ``BACKUP_POLICY``.

    Args:
        name(str):
            An Idem name of the resource.
        policy_id(str):
            The unique identifier (ID) of the policy that you want to attach to the target.
        target_id(str):
            The unique identifier (ID) of the root, OU, or account that you want to attach the policy to.

    Request syntax:
      .. code-block:: sls

        [idem_test_aws_organizations_policy_attachment]:
          aws.organizations.policy_attachment.present:
            - name: 'string'
            - policy_id: 'string'
            - target_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_organizations_policy_attachment:
              aws.organizations.policy_attachment.present:
                - name: 'idem_test_policy_attachment'
                - policy_id: 'p-123456789012'
                - target_id: 'ou-root-id'
    """
    result = dict(comment="", name=name, result=True, old_state=None, new_state=None)

    try:
        before_ret = await hub.tool.aws.organizations.policy_attachment.is_target_policy_attached(
            ctx, policy_id=policy_id, target_id=target_id
        )
    except hub.tool.boto3.exception.ClientError as e:
        result["comment"] = f"{e.__class__.__name__}: {e}"
        result["result"] = False
        return result

    # If before_ret has False result and has an error message in comment, then immediately return with the error.
    if before_ret["result"] is False and before_ret["comment"]:
        result["result"] = False
        result["comment"] = before_ret["comment"]
        return result

    if ctx.get("test", False):
        if before_ret["result"]:
            result[
                "comment"
            ] = f"aws.organizations.policy_attachment {name} already exists"
        else:
            result[
                "comment"
            ] = f"Would attach aws.organizations.policy_attachment {name}"
        return result

    if before_ret["result"]:
        result["old_state"] = before_ret["ret"]
        result["new_state"] = copy.deepcopy(before_ret["ret"])
        result["comment"] = f"'{name}' already exists"
    else:
        try:
            ret = await hub.exec.boto3.client.organizations.attach_policy(
                ctx,
                PolicyId=policy_id,
                TargetId=target_id,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] = f"Attached '{name}'"
            result["new_state"] = {"PolicyId": policy_id}
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] = f"{e.__class__.__name__}: {e}"
            result["result"] = False
    return result


async def absent(hub, ctx, name: str, policy_id: str, target_id: str) -> Dict[str, Any]:
    """Detaches a policy from a target root, organizational unit (OU), or account.

    .. warning::
        If the policy being detached is a service control policy (SCP), the changes to permissions for
        Identity and Access Management (IAM) users and roles in affected accounts are immediate.

    Every root, OU, and account must have at least one SCP attached. If you want to replace the default
    ``FullAWSAccess`` policy with an SCP that limits the permissions that can be delegated, you must attach
    the replacement SCP before you can remove the default SCP. This is the authorization strategy of an
    ``allow list``. If you instead attach a second SCP and leave the ``FullAWSAccess`` SCP still attached,
    and specify ``"Effect": "Deny"`` in the second SCP to override the ``"Effect": "Allow"`` in the
    ``FullAWSAccess`` policy (or any other attached SCP), you're using the authorization strategy of a ``deny list``.

    Args:
        name(str):
            An Idem name of the resource.
        policy_id(str):
            The unique identifier (ID) of the policy you want to detach.
        target_id(str):
            The unique identifier (ID) of the root, OU, or account that you want to detach the policy from.

    Request syntax:
      .. code-block:: sls

        [idem_test_aws_organizations_policy_attachment]:
          aws.organizations.policy_attachment.absent:
            - name: 'string'
            - policy_id: 'string'
            - target_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_organizations_policy_attachment:
              aws.organizations.policy_attachment.absent:
                - name: 'idem_test_policy_attachment'
                - policy_id: 'p-123456789012'
                - target_id: 'ou-root-id'
    """
    result = dict(comment="", name=name, result=True, old_state=None, new_state=None)

    try:
        before_ret = await hub.tool.aws.organizations.policy_attachment.is_target_policy_attached(
            ctx, policy_id=policy_id, target_id=target_id
        )
    except hub.tool.boto3.exception.ClientError as e:
        result["comment"] = f"{e.__class__.__name__}: {e}"
        result["result"] = False
        return result

    if before_ret["result"] is False and before_ret["comment"]:
        result["result"] = False
        result["comment"] = before_ret["comment"]
        return result

    if not before_ret["result"]:
        result["comment"] = f"'{name}' already absent"
    elif ctx.get("test", False):
        result["comment"] = f"Would detach aws.organizations.policy_attachment {name}"
        return result
    else:
        try:
            result["old_state"] = before_ret["ret"]
            ret = await hub.exec.boto3.client.organizations.detach_policy(
                ctx,
                PolicyId=policy_id,
                TargetId=target_id,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                result["result"] = False
                return result
            result["comment"] = f"Detached '{name}'"
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] = f"{e.__class__.__name__}: {e}"
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes AWS Organization Policy attachments in a way that can be recreated/managed with the corresponding "present" function.

    This operation can be called only from the organization's management account
    or by a member account that is a delegated administrator for an AWS service.

    The supported policy types are ``SERVICE_CONTROL_POLICY``, ``TAG_POLICY``, ``AISERVICES_OPT_OUT_POLICY`` and ``BACKUP_POLICY``.

    Returns:
        Dict[str, Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.organizations.policy_attachment
    """

    result = {}
    list_all_policies = []
    filters = [
        "SERVICE_CONTROL_POLICY",
        "TAG_POLICY",
        "BACKUP_POLICY",
        "AISERVICES_OPT_OUT_POLICY",
    ]

    for filter in filters:

        list_policies = await hub.exec.boto3.client.organizations.list_policies(
            ctx, Filter=filter
        )

        if not list_policies:
            hub.log.debug(
                f"Could not describe policy with error: {list_policies['comment']}"
            )
            return {}

        if list_policies["ret"]["Policies"]:
            list_all_policies.extend(list_policies["ret"]["Policies"])

    if list_all_policies:

        for policy in list_all_policies:

            policy_attachments_ret = (
                await hub.exec.boto3.client.organizations.list_targets_for_policy(
                    ctx, PolicyId=policy["Id"]
                )
            )

            if not policy_attachments_ret["result"]:
                hub.log.warning(
                    f"Could not get attached target list with policy {policy['Id']} with error"
                    f" {policy_attachments_ret['comment']} . Describe will skip this policy and continue."
                )
            else:
                targets = policy_attachments_ret["ret"].get("Targets", [])

                if not targets:
                    hub.log.warning(
                        f"Attached target list with policy {policy['Id']} is empty."
                        f"Describe will skip this policy and continue."
                    )
                    continue

                for target in targets:
                    resource_name = f"{target['TargetId']}-{policy['Id']}"
                    translated_target = list()
                    translated_target.append({"policy_id": policy["Id"]})
                    translated_target.append({"target_id": target["TargetId"]})

                    result[resource_name] = {
                        "aws.organizations.policy_attachment.present": translated_target
                    }

    return result
