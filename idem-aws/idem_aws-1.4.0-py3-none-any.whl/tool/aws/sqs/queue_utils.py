"""Util functions for SQS Queue."""
import copy
from typing import Any
from typing import Dict


DEFAULT_ATTRIBUTES_VALUES = {
    "delay_seconds": 0,
    "maximum_message_size": 262144,
    "message_retention_period": 345600,
    "policy": None,
    "receive_message_wait_time_seconds": 0,
    "redrive_policy": None,
    "visibility_timeout": 30,
    "kms_master_key_id": None,
    "kms_data_key_reuse_period_seconds": 300,
    "sqs_managed_sse_enabled": False,
    "fifo_queue": False,
    "content_based_deduplication": False,
    "deduplication_scope": "queue",
    "fifo_throughput_limit": "perQueue",
}


def compare_present_queue_attributes(
    hub, expected_attributes: Dict[str, Any], actual_attributes: Dict[str, Any]
) -> bool:
    """Checks if the expected_attributes are contained withing actual_attributes.

    A None value in expected_attributes and a default value in actual_attributes are considered equal.

    Args:
        expected_attributes(Dict):
            The expected attributes

        actual_attributes(Dict):
            The actual attributes

    Returns:
        True if expected_attributes is contained within actual_attributes, False otherwise
    """
    for (
        expected_attribute_name,
        expected_attribute_value,
    ) in expected_attributes.items():
        actual_attribute_value = actual_attributes.get(expected_attribute_name)

        if actual_attribute_value is None:
            return actual_attribute_value == expected_attribute_value

        if expected_attribute_name == "policy":
            if not hub.tool.aws.sqs.queue_utils.are_aws_policies_equal(
                expected_attribute_value, actual_attribute_value
            ):
                return False
            continue

        if expected_attribute_value != actual_attribute_value:
            if (
                expected_attribute_value is None
                and actual_attributes.get(expected_attribute_name)
                == DEFAULT_ATTRIBUTES_VALUES[expected_attribute_name]
            ):
                continue

            return False

    return True


def are_aws_policies_equal(
    hub, expected_policy: Dict[str, Any], actual_policy: Dict[str, Any]
) -> bool:
    """Compares two AWS policies.

    Args:
        expected_policy(Dict):
            The expected policy

        actual_policy(Dict):
            The actual policy

    Returns:
        True if the policies are equal, False otherwise
    """
    if expected_policy.get("Id") != actual_policy.get("Id") or expected_policy.get(
        "Version"
    ) != actual_policy.get("Version"):
        return False

    expected_statement_list = expected_policy.get("Statement", [])
    actual_statement_list = actual_policy.get("Statement", [])

    if len(expected_statement_list) != len(actual_statement_list):
        return False

    expected_statement_list = [
        hub.tool.aws.sqs.queue_utils.sort_policy_statement_lists(v)
        for v in expected_statement_list
    ]
    actual_statement_list = [
        hub.tool.aws.sqs.queue_utils.sort_policy_statement_lists(v)
        for v in actual_statement_list
    ]

    for expected_statement in expected_statement_list:
        if expected_statement not in actual_statement_list:
            return False

    return True


def sort_policy_statement_lists(
    hub, policy_statement: Dict[str, Any]
) -> Dict[str, Any]:
    """Sorts all lists in an AWS policy statement.

    Args:
        policy_statement(Dict):
            the policy statement whose lists will be sorted

    Returns:
        AWS policy statement with sorted lists
    """
    sorted_policy_statement = copy.deepcopy(policy_statement)

    if "Principal" in sorted_policy_statement:
        principal = sorted_policy_statement.get("Principal")
        if isinstance(principal, Dict):
            for key, value in principal.items():
                if isinstance(value, list):
                    sorted_policy_statement["Principal"][key] = sorted(value)
    elif "NotPrincipal" in sorted_policy_statement:
        not_principal = sorted_policy_statement.get("NotPrincipal")
        if isinstance(not_principal, Dict):
            for key, value in not_principal.items():
                if isinstance(value, list):
                    sorted_policy_statement["NotPrincipal"][key] = sorted(value)

    action_block = sorted_policy_statement.get("Action")
    if isinstance(action_block, list):
        sorted_policy_statement["Action"] = sorted(action_block)

    if "Resource" in sorted_policy_statement:
        resource_block = sorted_policy_statement.get("Resource")
        if isinstance(resource_block, list):
            sorted_policy_statement["Resource"] = sorted(resource_block)
    elif "NotResource" in sorted_policy_statement:
        not_resource_block = sorted_policy_statement.get("NotResource")
        if isinstance(not_resource_block, list):
            sorted_policy_statement["NotResource"] = sorted(not_resource_block)

    condition_map = sorted_policy_statement.get("Condition", {})
    for condition_type_string, condition in condition_map.items():
        for condition_key_string, condition_value in condition.items():
            if isinstance(condition_value, list):
                sorted_policy_statement["Condition"][condition_type_string][
                    condition_key_string
                ] = sorted(map(lambda x: str(x), condition_value))

    return sorted_policy_statement
