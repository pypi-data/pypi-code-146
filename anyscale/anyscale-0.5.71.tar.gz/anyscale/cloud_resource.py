import copy
import difflib
import ipaddress
import pprint
from typing import Any, Dict, List, Optional, Tuple, Union

import boto3
from botocore.exceptions import ClientError
from typing_extensions import Literal

from anyscale.aws_iam_policies import (
    AMAZON_ECR_READONLY_ACCESS_POLICY_NAME,
    AMAZON_S3_FULL_ACCESS_POLICY_NAME,
    ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE,
    get_anyscale_aws_iam_assume_role_policy,
)
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models.create_cloud_resource import (
    CreateCloudResource,
)
from anyscale.client.openapi_client.models.subnet_id_with_availability_zone_aws import (
    SubnetIdWithAvailabilityZoneAWS,
)
from anyscale.shared_anyscale_utils.aws import AwsRoleArn
from anyscale.shared_anyscale_utils.conf import ANYSCALE_HOST
from anyscale.util import (  # pylint:disable=private-import
    _get_subnet,
    contains_control_plane_role,
    filter_actions_associated_with_role,
    filter_actions_from_policy_document,
)
from anyscale.utils.s3 import verify_s3_access


# This needs to be kept in sync with the Ray autoscaler in
# https://github.com/ray-project/ray/blob/eb9c5d8fa70b1c360b821f82c7697e39ef94b25e/python/ray/autoscaler/_private/aws/config.py
# It should go away with the SSM refactor.
DEFAULT_RAY_IAM_ROLE = "ray-autoscaler-v1"


class CAPACITY_THRESHOLDS:  # noqa: N801
    """
    These are various constants for resources capacity we want to ensure we meet.
    """

    class AWS_VPC:  # noqa: N801
        HOSTS_MIN: int = ipaddress.ip_network("10.0.0.0/24").num_addresses
        HOSTS_WARN: int = ipaddress.ip_network("10.0.0.0/20").num_addresses

    class AWS_SUBNET:  # noqa: N801
        HOSTS_MIN: int = ipaddress.ip_network("10.0.0.0/28").num_addresses
        HOSTS_WARN: int = ipaddress.ip_network("10.0.0.0/24").num_addresses


def compare_dicts_diff(d1: Dict[Any, Any], d2: Dict[Any, Any]) -> str:
    """Returns a string representation of the difference of the two dictionaries.
    Example:

    Input:
    print(compare_dicts_diff({"a": {"c": 1}, "b": 2}, {"a": {"c": 2}, "d": 3}))

    Output:
    - {'a': {'c': 1}, 'b': 2}
    ?             ^    ^   ^

    + {'a': {'c': 2}, 'd': 3}
    ?             ^    ^   ^
    """

    return "\n" + "\n".join(
        difflib.ndiff(pprint.pformat(d1).splitlines(), pprint.pformat(d2).splitlines())
    )


def verify_aws_vpc(
    cloud_resource: CreateCloudResource,
    boto3_session: boto3.Session,
    logger: BlockLogger,
    ignore_capacity_errors: bool = False,  # TODO: Probably don't do this forever. Its kinda hacky
) -> bool:
    logger.info("Verifying VPC ...")
    if not cloud_resource.aws_vpc_id:
        logger.error("Missing VPC id.")
        return False

    ec2 = boto3_session.resource("ec2")
    vpc = ec2.Vpc(cloud_resource.aws_vpc_id)

    # Verify the VPC exists
    try:
        vpc.load()
    except ClientError as e:
        if e.response["Error"]["Code"] == "InvalidVpcID.NotFound":
            logger.error(f"VPC with id {cloud_resource.aws_vpc_id} does not exist.")
            return False
        raise e

    # Verify that the VPC has "enough" capacity.
    return aws_vpc_has_enough_capacity(vpc, logger) or ignore_capacity_errors


def aws_vpc_has_enough_capacity(vpc, logger: BlockLogger) -> bool:
    cidr_block = ipaddress.ip_network(vpc.cidr_block, strict=False)

    if cidr_block.num_addresses < CAPACITY_THRESHOLDS.AWS_VPC.HOSTS_MIN:
        logger.error(
            f"The provided vpc ({vpc.id})'s CIDR block ({cidr_block}) is too"
            f" small. We want at least {CAPACITY_THRESHOLDS.AWS_VPC.HOSTS_MIN} addresses,"
            f" but this vpc only has {cidr_block.num_addresses}. Please reach out to"
            f" support if this is an issue!"
        )
        return False
    elif cidr_block.num_addresses < CAPACITY_THRESHOLDS.AWS_VPC.HOSTS_WARN:
        logger.warning(
            f"The provided vpc ({vpc.id})'s CIDR block ({cidr_block}) is probably"
            f" too small. We suggest at least {CAPACITY_THRESHOLDS.AWS_VPC.HOSTS_WARN}"
            f" addresses, but this vpc only supports up to"
            f" {cidr_block.num_addresses} addresses."
        )
    else:
        logger.info(f"VPC {vpc.id} verification succeeded.")

    return True


def _get_subnets_from_subnet_ids(subnet_ids: List[str], region: str) -> List[Any]:
    return [
        _get_subnet(subnet_arn=subnet_id, region=region) for subnet_id in subnet_ids
    ]


def verify_aws_subnets(
    cloud_resource: CreateCloudResource,
    region: str,
    is_private_network: bool,
    logger: BlockLogger,
    ignore_capacity_errors: bool = False,  # TODO: Probably don't do this forever. Its kinda hacky
) -> Union[
    Tuple[Literal[True], CreateCloudResource],  # Success
    Tuple[Literal[False], Literal[None]],  # Error
]:
    """
    Verify the subnets cloud resource of a cloud.
    This function mutates the aws_subnet_ids field in cloud_resource. It combines the subnets with its availability zone.
    Invariant: After this function, cloud_resource will always have subnet_ids_with_availability_zones instead of aws_subnet_ids.
    """
    logger.info("Verifying subnets ...")
    cloud_resource = copy.deepcopy(cloud_resource)

    if not cloud_resource.aws_vpc_id:
        logger.error("Missing VPC ID.")
        return False, None

    subnet_ids = []
    if (
        cloud_resource.aws_subnet_ids_with_availability_zones
        and len(cloud_resource.aws_subnet_ids_with_availability_zones) > 0
    ):
        subnet_ids = [
            subnet_id_with_az.subnet_id
            for subnet_id_with_az in cloud_resource.aws_subnet_ids_with_availability_zones
        ]
    elif cloud_resource.aws_subnet_ids and len(cloud_resource.aws_subnet_ids) > 0:
        subnet_ids = cloud_resource.aws_subnet_ids
    else:
        logger.error("Missing subnet IDs.")
        return False, None

    subnets = _get_subnets_from_subnet_ids(subnet_ids=subnet_ids, region=region)

    for subnet, subnet_id in zip(subnets, subnet_ids):
        # Verify subnet exists
        if not subnet:
            logger.error(f"Subnet with id {subnet_id} does not exist.")
            return False, None

        # Verify the Subnet has "enough" capacity.
        if (
            not aws_subnet_has_enough_capacity(subnet, logger)
            and not ignore_capacity_errors
        ):
            return False, None

        # Verify that the subnet is in the provided VPC all of these are in the same VPC.
        if subnet.vpc_id != cloud_resource.aws_vpc_id:
            logger.error(
                f"The subnet {subnet_id} is not in a vpc of this cloud. The vpc of this subnet is {subnet.vpc_id} and the vpc of this cloud is {cloud_resource.aws_vpc_id}."
            )
            return False, None

        # Verify that the subnet is auto-assigning public IP addresses if it's not private.
        if not is_private_network and not subnet.map_public_ip_on_launch:
            logger.warning(
                f"The subnet {subnet_id} does not have the 'Auto-assign Public IP' option enabled. This is not currently supported."
            )

        # Success!
        logger.info(f"Subnet {subnet.id}'s verification succeeded.")

    # combine subnet and its availability zone
    subnet_ids_with_availability_zones = [
        SubnetIdWithAvailabilityZoneAWS(
            subnet_id=subnet.id, availability_zone=subnet.availability_zone,
        )
        for subnet in subnets
    ]
    cloud_resource.aws_subnet_ids_with_availability_zones = (
        subnet_ids_with_availability_zones
    )
    cloud_resource.aws_subnet_ids = None

    logger.info(f"Subnets {cloud_resource.aws_subnet_ids} verification succeeded.")
    return True, cloud_resource


def aws_subnet_has_enough_capacity(subnet, logger: BlockLogger) -> bool:
    cidr_block = ipaddress.ip_network(subnet.cidr_block, strict=False)

    if cidr_block.num_addresses < CAPACITY_THRESHOLDS.AWS_SUBNET.HOSTS_MIN:
        logger.error(
            f"The provided Subnet ({subnet.id})'s CIDR block ({cidr_block}) is too"
            f" small. We want at least {CAPACITY_THRESHOLDS.AWS_SUBNET.HOSTS_MIN} addresses,"
            f" but this subnet only has {cidr_block.num_addresses}. Please reach out to"
            f" support if this is an issue!"
        )
        return False
    elif cidr_block.num_addresses < CAPACITY_THRESHOLDS.AWS_SUBNET.HOSTS_WARN:
        logger.warning(
            f"The provided Subnet ({subnet.id})'s CIDR block ({cidr_block}) is probably"
            f" too small. We suggest at least {CAPACITY_THRESHOLDS.AWS_SUBNET.HOSTS_WARN}"
            f" addresses, but this subnet only supports up to"
            f" {cidr_block.num_addresses} addresses."
        )

    return True


def _get_roles_from_cloud_resource(
    cloud_resource: CreateCloudResource,
    boto3_session: boto3.Session,
    logger: BlockLogger,
) -> Optional[List[Any]]:
    iam = boto3_session.resource("iam")
    roles = [
        iam.Role(AwsRoleArn.from_string(role_arn).to_role_name())
        for role_arn in cloud_resource.aws_iam_role_arns
    ]
    # Validate the roles exist.
    # `.load()` will throw an exception if the Role does not exist.
    for role in roles:
        try:
            role.load()
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchEntity":
                logger.error(f"Could not find role: {role.name}")
                return None
            raise e
    return roles


def verify_aws_iam_roles(
    cloud_resource: CreateCloudResource,
    boto3_session: boto3.Session,
    anyscale_aws_account: str,
    logger: BlockLogger,
) -> bool:
    logger.info("Verifying IAM roles ...")
    if not cloud_resource.aws_iam_role_arns:
        logger.error("Missing IAM role arns.")
        return False
    roles = _get_roles_from_cloud_resource(cloud_resource, boto3_session, logger)
    if roles is None:
        return False

    # verifying control plane role: anyscale iam role
    anyscale_iam_role = roles[0]
    assume_role_policy_document = anyscale_iam_role.assume_role_policy_document
    if not contains_control_plane_role(
        assume_role_policy_document=assume_role_policy_document,
        anyscale_aws_account=anyscale_aws_account,
    ):
        logger.warning(
            f"Anyscale IAM role {anyscale_iam_role.arn} does not contain expected assume role policy. It must allow assume role from arn:aws:iam::{anyscale_aws_account}:root."
        )
        expected_assume_role_policy_document = get_anyscale_aws_iam_assume_role_policy(
            anyscale_aws_account=anyscale_aws_account
        )
        logger.warning(
            compare_dicts_diff(
                assume_role_policy_document, expected_assume_role_policy_document
            )
        )

    allow_actions_expected = filter_actions_from_policy_document(
        ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE
    )
    allow_actions_on_role = filter_actions_associated_with_role(
        boto3_session, anyscale_iam_role
    )
    allow_actions_missing = allow_actions_expected - allow_actions_on_role
    if allow_actions_missing:
        logger.warning(
            f"IAM role {anyscale_iam_role.arn} does not have sufficient permissions. We suggest adding these actions to ensure that cluster management works properly: {allow_actions_missing}."
        )

    # verifying data plane role: ray autoscaler role
    cluster_node_role = roles[1]
    policy_names = [
        policy.policy_name for policy in cluster_node_role.attached_policies.all()
    ]
    if AMAZON_ECR_READONLY_ACCESS_POLICY_NAME not in policy_names:
        logger.warning(
            f"Dataplane role {cluster_node_role.arn} does not contain policy {AMAZON_ECR_READONLY_ACCESS_POLICY_NAME}. This is safe to ignore if you are not pulling custom Docker Images from an ECR repository."
        )
    if AMAZON_S3_FULL_ACCESS_POLICY_NAME not in policy_names:
        logger.warning(
            f"Dataplane role {cluster_node_role.arn} does not contain policy {AMAZON_S3_FULL_ACCESS_POLICY_NAME}. We suggest adding these S3 privileges to ensure logs are working properly."
        )

    if (
        len(
            [
                profile
                for profile in cluster_node_role.instance_profiles.all()
                if profile.name == cluster_node_role.name
            ]
        )
        == 0
    ):
        logger.warning(
            f"Dataplane role {cluster_node_role.arn} is required to have an instance profile with the name {cluster_node_role.name}."
            "\nPlease create this isntance profile and associate it to the role."
        )
        return False

    logger.info(f"IAM roles {cloud_resource.aws_iam_role_arns} verification succeeded.")
    return True


def verify_aws_security_groups(
    cloud_resource: CreateCloudResource,
    boto3_session: boto3.Session,
    logger: BlockLogger,
) -> bool:
    logger.info("Verifying security groups ...")
    if not cloud_resource.aws_security_groups:
        logger.error("Missing security group IDs.")
        return False

    ec2 = boto3_session.resource("ec2")
    anyscale_security_group_arn = cloud_resource.aws_security_groups[0]
    anyscale_security_group = ec2.SecurityGroup(anyscale_security_group_arn)
    try:
        anyscale_security_group.load()
    except ClientError as e:
        if e.response["Error"]["Code"] == "InvalidGroup.NotFound":
            logger.error(
                f"Security group with id {anyscale_security_group_arn} does not exist."
            )
            return False
        raise e

    # Now we only have one security group defining inbound rules.
    # 443 is for HTTPS ingress
    # 22 is for SSH
    inbound_ip_permissions = anyscale_security_group.ip_permissions
    expected_open_ports = [443, 22]

    inbound_ip_permissions_with_specific_port = [
        ip_permission["FromPort"]
        for ip_permission in inbound_ip_permissions
        if "FromPort" in ip_permission
    ]
    inbound_sg_rule_with_self = []  # type: ignore
    for sg_rule in inbound_ip_permissions:
        if sg_rule.get("IpProtocol") == "-1":
            inbound_sg_rule_with_self.extend(sg_rule.get("UserIdGroupPairs"))  # type: ignore

    missing_open_ports = []
    for port in expected_open_ports:
        if not any(
            (
                inbound_ip_permission_port == port
                for inbound_ip_permission_port in inbound_ip_permissions_with_specific_port
            )
        ):
            missing_open_ports.append(port)
    if missing_open_ports:
        # TODO (sluo): update the doc link to our website once the page is up.
        logger.warning(
            f"Security group with id {anyscale_security_group_arn} does not contain inbound permission for ports: {missing_open_ports}. These ports are used for interaction with the clusters from Anyscale UI. Please make sure to configure them according to https://docs.google.com/document/d/12QE0nZwZELvR6ocW_mDISzA568VGOQgwYXECNlvCcVk"
        )

    if not any(
        sg_rule.get("GroupId") == anyscale_security_group_arn
        for sg_rule in inbound_sg_rule_with_self
    ):
        logger.error(
            f"Security group with id {anyscale_security_group_arn} does not contain inbound permission for all ports for traffic from the same security group."
        )
        return False

    if len(inbound_ip_permissions_with_specific_port) > len(expected_open_ports):
        logger.warning(
            f"Security group with id {anyscale_security_group_arn} allows access to more than {expected_open_ports}. This may not be safe by default."
        )

    logger.info(
        f"Security group {cloud_resource.aws_security_groups} verification succeeded."
    )
    return True


def verify_aws_s3(
    cloud_resource: CreateCloudResource,
    boto3_session: boto3.Session,
    logger: BlockLogger,
) -> bool:
    logger.info("Verifying S3 ...")
    if not cloud_resource.aws_s3_id:
        logger.error("Missing S3 ID.")
        return False

    s3 = boto3_session.resource("s3")
    bucket_name = cloud_resource.aws_s3_id.split(":")[-1]
    s3_bucket = s3.Bucket(bucket_name)

    # Check for the existence of `creation_date` because this incurs a `list_bucket` call.
    # Calling `.load()` WILL NOT ERROR in cases where the caller does not have access to the bucket.
    if s3_bucket.creation_date is None:
        logger.error(f"S3 object with id {cloud_resource.aws_s3_id} does not exist.")
        return False

    has_correct_cors_rule = False
    """
    Verify CORS rules. The correct CORS rule should look like:
    [{
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET"
        ],
        "AllowedOrigins": [
            "https://console.anyscale-staging.com"
        ],
        "ExposeHeaders": []
    }]
    """
    for rule in s3_bucket.Cors().cors_rules:
        assert isinstance(rule, dict), "Malformed CORS rule."
        has_correct_cors_rule = (
            ANYSCALE_HOST in rule.get("AllowedOrigins", [])
            and "*" in rule.get("AllowedHeaders", [])
            and "GET" in rule.get("AllowedMethods", [])
        )

    if not has_correct_cors_rule:
        logger.warning(
            f"S3 bucket {bucket_name} does not have the correct CORS rule for Anyscale. This is safe to ignore if you are not using Anyscale UI. Otherwise please create the correct CORS rule for Anyscale according to https://docs.google.com/document/d/12QE0nZwZELvR6ocW_mDISzA568VGOQgwYXECNlvCcVk"
        )

    roles = _get_roles_from_cloud_resource(cloud_resource, boto3_session, logger)
    if roles is None:
        return False

    if not verify_s3_access(boto3_session, s3_bucket, roles[0], logger):
        logger.warning(
            f"S3 Bucket {bucket_name} does not appear to have correct permissions for the Anyscale Control Plane role {roles[0].name}"
        )

    if not verify_s3_access(boto3_session, s3_bucket, roles[1], logger):
        logger.warning(
            f"S3 Bucket {bucket_name} does not appear to have correct permissions for the Data Plane role {roles[1].name}"
        )
    logger.info(f"S3 {cloud_resource.aws_s3_id} verification succeeded.")
    return True


def _get_network_interfaces_from_mount_targets(
    mount_targets_response: dict, boto3_session: Any, logger: BlockLogger
) -> List[Any]:
    ec2 = boto3_session.resource("ec2")
    network_interfaces = []
    for network_interface_id in [
        mount_target["NetworkInterfaceId"]
        for mount_target in mount_targets_response["MountTargets"]
    ]:
        network_interface = ec2.NetworkInterface(network_interface_id)
        try:
            network_interface.load()
        except ClientError as e:
            logger.warning(f"Network interface loading error: {e}")
            continue
        network_interfaces.append(network_interface)
    return network_interfaces


def verify_aws_efs(
    cloud_resource: CreateCloudResource,
    boto3_session: boto3.Session,
    logger: BlockLogger,
) -> bool:
    logger.info("Verifying EFS ...")
    if not cloud_resource.aws_efs_id:
        logger.error("Missing EFS ID.")
        return False
    subnet_ids = []
    if (
        cloud_resource.aws_subnet_ids_with_availability_zones
        and len(cloud_resource.aws_subnet_ids_with_availability_zones) > 0
    ):
        subnet_ids = [
            subnet_id_with_az.subnet_id
            for subnet_id_with_az in cloud_resource.aws_subnet_ids_with_availability_zones
        ]
    elif cloud_resource.aws_subnet_ids and len(cloud_resource.aws_subnet_ids) > 0:
        subnet_ids = cloud_resource.aws_subnet_ids
    else:
        logger.error("Missing subnet IDs.")
        return False
    if not cloud_resource.aws_security_groups:
        logger.error("Missing security group IDs.")
        return False

    client = boto3_session.client("efs")
    try:
        file_systems_response = client.describe_file_systems(
            FileSystemId=cloud_resource.aws_efs_id
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "FileSystemNotFound":
            logger.error(f"EFS with id {cloud_resource.aws_efs_id} does not exist.")
            return False
        raise e

    if len(file_systems_response.get("FileSystems", [])) == 0:
        logger.error(f"EFS with id {cloud_resource.aws_efs_id} does not exist.")
        return False

    # verify that there is a mount target for each subnet and security group
    mount_targets_response = client.describe_mount_targets(
        FileSystemId=cloud_resource.aws_efs_id
    )
    if not mount_targets_response.get("MountTargets"):
        logger.warning(
            f"EFS with id {cloud_resource.aws_efs_id} does not contain mount targets."
        )
    else:
        network_interfaces = _get_network_interfaces_from_mount_targets(
            mount_targets_response, boto3_session, logger
        )
        expected_security_group_id = cloud_resource.aws_security_groups[0]
        for subnet_id in subnet_ids:
            contains_subnet_id_security_group = False
            for network_interface in network_interfaces:
                network_interface_security_group_ids = [
                    group["GroupId"]
                    for group in network_interface.groups
                    if group.get("GroupId")
                ]
                if (
                    network_interface.subnet_id == subnet_id
                    and expected_security_group_id
                    in network_interface_security_group_ids
                ):
                    contains_subnet_id_security_group = True
                    break
            if not contains_subnet_id_security_group:
                logger.warning(
                    f"EFS with id {cloud_resource.aws_efs_id} does not contain network interface with subnet id {subnet_id} and security group id {cloud_resource.aws_security_groups[0]}."
                )

    logger.info(f"EFS {cloud_resource.aws_efs_id} verification succeeded.")
    return True


def verify_aws_cloudformation_stack(
    cloud_resource: CreateCloudResource,
    boto3_session: boto3.Session,
    logger: BlockLogger,
) -> bool:
    logger.info("Verifying CloudFormation stack ...")
    if not cloud_resource.aws_cloudformation_stack_id:
        logger.error("Missing CloudFormation stack id.")
        return False

    cloudformation = boto3_session.resource("cloudformation")
    stack = cloudformation.Stack(cloud_resource.aws_cloudformation_stack_id)
    if not stack:
        logger.error(
            f"CloudFormation stack with id {cloud_resource.aws_cloudformation_stack_id} does not exist."
        )
        return False

    logger.info(
        f"CloudFormation stack {cloud_resource.aws_cloudformation_stack_id} verification succeeded."
    )
    return True
