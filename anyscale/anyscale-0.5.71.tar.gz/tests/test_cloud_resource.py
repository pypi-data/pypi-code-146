from datetime import datetime
import json
import random
import re
import string
import sys
from typing import Callable, Dict, List, Optional
from unittest.mock import Mock, patch

import boto3
from botocore.exceptions import ClientError
from moto import mock_iam
import pytest

from anyscale.cloud_resource import (
    aws_subnet_has_enough_capacity,
    verify_aws_cloudformation_stack,
    verify_aws_efs,
    verify_aws_iam_roles,
    verify_aws_s3,
    verify_aws_security_groups,
    verify_aws_subnets,
    verify_aws_vpc,
)
from anyscale.conf import ANYSCALE_IAM_ROLE_NAME
from anyscale.shared_anyscale_utils.aws import AwsRoleArn
from anyscale.shared_anyscale_utils.conf import ANYSCALE_HOST
from frontend.cli.anyscale.aws_iam_policies import (
    AMAZON_ECR_READONLY_ACCESS_POLICY_ARN,
    AMAZON_S3_FULL_ACCESS_POLICY_ARN,
    ANYSCALE_IAM_PERMISSIONS_EC2_INITIAL_RUN,
    ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE,
    get_anyscale_aws_iam_assume_role_policy,
)
from frontend.cli.anyscale.cli_logger import BlockLogger
from frontend.cli.anyscale.client.openapi_client.models.create_cloud_resource import (
    CreateCloudResource,
)


DEFAULT_RAY_IAM_ROLE = "ray-autoscaler-v1"


def _create_roles(anyscale_account: str):
    iam = boto3.client("iam")
    suffix = "".join(random.choices(string.ascii_lowercase, k=10))
    control_plane_role = iam.create_role(
        RoleName=ANYSCALE_IAM_ROLE_NAME + suffix,
        AssumeRolePolicyDocument=json.dumps(
            get_anyscale_aws_iam_assume_role_policy(
                anyscale_aws_account=anyscale_account
            )
        ),
    )["Role"]["Arn"]

    # Create & Configure the Dataplane Role
    dataplane_role_name = DEFAULT_RAY_IAM_ROLE + suffix
    dataplane_role = iam.create_role(
        RoleName=dataplane_role_name, AssumeRolePolicyDocument="{}"
    )["Role"]["Arn"]

    iam.attach_role_policy(
        RoleName=dataplane_role_name, PolicyArn=AMAZON_ECR_READONLY_ACCESS_POLICY_ARN
    )
    iam.attach_role_policy(
        RoleName=dataplane_role_name, PolicyArn=AMAZON_S3_FULL_ACCESS_POLICY_ARN
    )
    return [control_plane_role, dataplane_role]


def generate_cloud_resource_mock_aws() -> CreateCloudResource:
    return CreateCloudResource(
        aws_vpc_id="fake_aws_vpc_id",
        aws_subnet_ids=["fake_aws_subnet_id_0"],
        aws_iam_role_arns=[
            "arn:aws:iam::123:role/mock_anyscale_role",
            "arn:aws:iam::123:role/mock_dataplane_role",
        ],
        aws_security_groups=["fake_aws_security_group_0"],
        aws_s3_id="fake_aws_s3_id",
        aws_efs_id="fake_aws_efs_id",
        aws_cloudformation_stack_id="fake_aws_cloudformation_stack_id",
    )


def _attach_iam_roles_to_role(role_arn: str) -> None:
    iam = boto3.client("iam")
    role_name = AwsRoleArn.from_string(role_arn).to_role_name()

    steady_state = iam.create_policy(
        PolicyName="".join(random.choices(string.ascii_lowercase, k=10)),
        PolicyDocument=json.dumps(ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE),
    )["Policy"]["Arn"]
    iam.attach_role_policy(RoleName=role_name, PolicyArn=steady_state)

    initial_run = iam.create_policy(
        PolicyName="".join(random.choices(string.ascii_lowercase, k=10)),
        PolicyDocument=json.dumps(ANYSCALE_IAM_PERMISSIONS_EC2_INITIAL_RUN),
    )["Policy"]["Arn"]
    iam.attach_role_policy(RoleName=role_name, PolicyArn=initial_run)


def _attach_inline_iam_policy_to_role(role_arn: str) -> None:
    iam = boto3.client("iam")
    role_name = AwsRoleArn.from_string(role_arn).to_role_name()

    iam.put_role_policy(
        RoleName=role_name,
        PolicyName="".join(random.choices(string.ascii_lowercase, k=10)),
        PolicyDocument=json.dumps(ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE),
    )
    iam.put_role_policy(
        RoleName=role_name,
        PolicyName="".join(random.choices(string.ascii_lowercase, k=10)),
        PolicyDocument=json.dumps(ANYSCALE_IAM_PERMISSIONS_EC2_INITIAL_RUN),
    )


def _create_instance_profile_for_role(
    role_arn: str, instance_profile_name: Optional[str]
) -> None:
    role_name = AwsRoleArn.from_string(role_arn).to_role_name()
    if instance_profile_name is None:
        instance_profile_name = role_name

    iam = boto3.client("iam")
    iam.create_instance_profile(InstanceProfileName=instance_profile_name)
    iam.add_role_to_instance_profile(
        RoleName=role_name, InstanceProfileName=instance_profile_name,
    )


def generate_aws_security_groups() -> List[Mock]:
    ip_permission_443 = {"FromPort": 443}
    ip_permission_22 = {"FromPort": 22}
    inbound_ip_permissions = [
        ip_permission_443,
        ip_permission_22,
        {
            "IpProtocol": "-1",
            "UserIdGroupPairs": [{"GroupId": "fake_aws_security_group_0"}],
        },
    ]
    anyscale_security_group = Mock(ip_permissions=inbound_ip_permissions)
    return anyscale_security_group


def generate_aws_subnets() -> List[Mock]:
    return [
        Mock(
            id="mock_id_0",
            cidr_block="0.0.0.0/18",
            vpc_id="fake_aws_vpc_id",
            availability_zone="us-west-2a",
        ),
        Mock(
            id="mock_id_1",
            cidr_block="0.0.0.0/19",
            vpc_id="fake_aws_vpc_id",
            availability_zone="us-west-2c",
        ),
        Mock(
            id="mock_id_2",
            cidr_block="1.2.3.4/20",
            vpc_id="fake_aws_vpc_id",
            availability_zone="us-west-2b",
        ),
    ]


def generate_network_interfaces_mock(cloud_resource: CreateCloudResource) -> List[Mock]:
    return [
        Mock(
            subnet_id=subnet_id,
            groups=[
                {"GroupId": security_group_id}
                for security_group_id in cloud_resource.aws_security_groups
            ],
        )
        for subnet_id in cloud_resource.aws_subnet_ids
    ]


@pytest.mark.parametrize(
    "vpc_exists,vpc_cidr_block,expected_result,expected_log_message",
    [
        pytest.param(False, "0.0.0.0/0", False, r"does not exist."),
        # Happy sizes
        pytest.param(True, "0.0.1.0/0", True, r"verification succeeded."),
        pytest.param(True, "0.0.2.0/20", True, r"verification succeeded."),
        # Warn sizes
        pytest.param(
            True, "0.0.3.0/21", True, r"but this vpc only supports up to \d+ addresses",
        ),
        pytest.param(
            True, "0.0.4.0/24", True, r"but this vpc only supports up to \d+ addresses",
        ),
        # Error sizes
        pytest.param(
            True,
            "0.0.4.0/25",
            False,
            r"Please reach out to support if this is an issue!",
        ),
    ],
)
def test_verify_aws_vpc(
    capsys,
    vpc_exists: bool,
    vpc_cidr_block: str,
    expected_result: bool,
    expected_log_message: str,
):
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    vpc_mock = Mock(cidr_block=vpc_cidr_block) if vpc_exists else Mock()
    if not vpc_exists:
        vpc_mock.load = Mock(
            side_effect=ClientError(
                error_response={"Error": {"Code": "InvalidVpcID.NotFound"}},
                operation_name="DescribeVpcs",
            )
        )
    ec2_mock = Mock(Vpc=Mock(return_value=vpc_mock))
    boto3_session_mock = Mock(resource=Mock(return_value=ec2_mock))

    result = verify_aws_vpc(
        cloud_resource=cloud_resource_mock,
        boto3_session=boto3_session_mock,
        logger=BlockLogger(),
    )
    assert result == expected_result

    stdout, stderr = capsys.readouterr()
    sys.stdout.write(stdout)
    sys.stderr.write(stderr)

    if expected_log_message:
        assert re.search(expected_log_message, stderr)


def test_verify_aws_subnets(capsys):
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    subnets_mock = generate_aws_subnets()
    with patch.multiple(
        "anyscale.cloud_resource",
        _get_subnets_from_subnet_ids=Mock(return_value=subnets_mock),
    ):
        result, _ = verify_aws_subnets(
            cloud_resource=cloud_resource_mock,
            region="fake_region",
            is_private_network=False,
            logger=BlockLogger(),
        )
        assert result

        _, stderr = capsys.readouterr()
        assert re.search(r"verification succeeded.", stderr)


def test_verify_aws_subnets_no_subnets():
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    cloud_resource_mock.aws_subnet_ids = None
    cloud_resource_mock.aws_subnet_ids_with_availability_zones = None
    result, returned_cloud_resource = verify_aws_subnets(
        cloud_resource=cloud_resource_mock,
        region="fake_region",
        is_private_network=False,
        logger=BlockLogger(),
    )
    assert result is False
    assert returned_cloud_resource is None


@pytest.mark.parametrize(
    "subnet_cidr,has_capacity,expected_log_message",
    [
        # Happy sizes
        ("0.0.0.0/0", True, None),
        ("0.0.1.0/24", True, None),
        # Warn sizes
        ("0.0.2.0/25", True, r"but this subnet only supports up to \d+ addresses"),
        ("0.0.3.0/28", True, r"but this subnet only supports up to \d+ addresses"),
        # Error sizes
        ("0.0.3.0/29", False, r"Please reach out to support if this is an issue!"),
    ],
)
def test_aws_subnet_has_enough_capacity(
    subnet_cidr, has_capacity, expected_log_message, capsys
):
    subnet = Mock()
    subnet.id = "vpc-fake_id"
    subnet.cidr_block = subnet_cidr

    assert aws_subnet_has_enough_capacity(subnet, BlockLogger()) == has_capacity

    stdout, stderr = capsys.readouterr()
    sys.stdout.write(stdout)
    sys.stderr.write(stderr)

    if expected_log_message:
        assert re.search(expected_log_message, stderr)


@mock_iam
@pytest.mark.parametrize(
    "iam_roles_mock_fn,expect_warning",
    [
        pytest.param(lambda _: None, True, id="No Policies"),
        pytest.param(_attach_iam_roles_to_role, False, id="Separate Policies"),
        pytest.param(_attach_inline_iam_policy_to_role, False, id="Inline Policies"),
    ],
)
def test_verify_aws_iam_roles(
    iam_roles_mock_fn: Callable[[str], None], expect_warning: bool
):
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    cp_role_arn, dp_role_arn = _create_roles("fake_anyscale_aws_account")
    _create_instance_profile_for_role(dp_role_arn, None)
    cloud_resource_mock.aws_iam_role_arns = [cp_role_arn, dp_role_arn]
    iam_roles_mock_fn(cp_role_arn)
    mock_logger = Mock()
    assert verify_aws_iam_roles(
        cloud_resource=cloud_resource_mock,
        boto3_session=boto3.Session(),
        anyscale_aws_account="fake_anyscale_aws_account",
        logger=mock_logger,
    )

    if expect_warning:
        assert len(mock_logger.warning.mock_calls) == 1
    else:
        mock_logger.warning.assert_not_called()

    assert len(mock_logger.info.mock_calls) == 2


@mock_iam
def test_verify_aws_iam_roles_instance_profiles():
    """Tests that the dataplane role only passes validation if it has
    an InstanceProfile with the same name as the Role."""
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    cp_role_arn, dp_role_arn = _create_roles("fake_anyscale_aws_account")
    cloud_resource_mock.aws_iam_role_arns = [cp_role_arn, dp_role_arn]
    mock_logger = Mock()

    # No instance profile for role
    assert not verify_aws_iam_roles(
        cloud_resource=cloud_resource_mock,
        boto3_session=boto3.Session(),
        anyscale_aws_account="fake_anyscale_aws_account",
        logger=mock_logger,
    )

    # Create an instance profile for the role, but with the wrong name
    _create_instance_profile_for_role(dp_role_arn, "wrong_name")
    assert not verify_aws_iam_roles(
        cloud_resource=cloud_resource_mock,
        boto3_session=boto3.Session(),
        anyscale_aws_account="fake_anyscale_aws_account",
        logger=mock_logger,
    )

    # Create a correct insance profile with the role!
    _create_instance_profile_for_role(dp_role_arn, None)
    assert verify_aws_iam_roles(
        cloud_resource=cloud_resource_mock,
        boto3_session=boto3.Session(),
        anyscale_aws_account="fake_anyscale_aws_account",
        logger=mock_logger,
    )


def test_verify_aws_security_groups():
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    security_group_mock = generate_aws_security_groups()
    ec2_mock = Mock(SecurityGroup=Mock(return_value=security_group_mock))
    boto3_session_mock = Mock(resource=Mock(return_value=ec2_mock))

    result = verify_aws_security_groups(
        cloud_resource=cloud_resource_mock,
        boto3_session=boto3_session_mock,
        logger=Mock(),
    )
    assert result


@pytest.mark.parametrize(
    "s3_exists,expected_result",
    [
        pytest.param(False, False, id="S3-Does-Not-Exist"),
        pytest.param(True, True, id="S3-Exists"),
    ],
)
@pytest.mark.parametrize(
    "cors_rules,expected_warning_call_count",
    [
        pytest.param(
            [
                {
                    "AllowedHeaders": ["*"],
                    "AllowedMethods": ["GET"],
                    "AllowedOrigins": [ANYSCALE_HOST],
                    "ExposeHeaders": [],
                }
            ],
            0,
            id="CorrectCORS",
        ),
        pytest.param(
            [
                {
                    "AllowedHeaders": ["*"],
                    "AllowedMethods": ["GET"],
                    "AllowedOrigins": [],
                    "ExposeHeaders": [],
                }
            ],
            1,
            id="ImproperCORS",
        ),
        pytest.param([{}], 1, id="NoCORS"),
    ],
)
def test_verify_aws_s3(
    s3_exists: bool,
    expected_result: bool,
    cors_rules: List[Dict[str, List[str]]],
    expected_warning_call_count: int,
):
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    s3_mock = Mock()
    s3_bucket_mock = (
        Mock(Cors=Mock(return_value=Mock(cors_rules=cors_rules)),)
        if s3_exists
        else Mock()
    )
    s3_bucket_mock.creation_date = datetime.now() if s3_exists else None
    s3_mock = Mock(Bucket=Mock(return_value=s3_bucket_mock))
    boto3_session_mock = Mock(resource=Mock(return_value=s3_mock))
    mock_logger = Mock()

    with patch.multiple(
        "anyscale.cloud_resource", verify_s3_access=Mock(return_value=True),
    ):
        result = verify_aws_s3(
            cloud_resource=cloud_resource_mock,
            boto3_session=boto3_session_mock,
            logger=mock_logger,
        )

    if s3_exists:
        assert mock_logger.warning.call_count == expected_warning_call_count
    else:
        assert mock_logger.error.call_count == 1
        assert mock_logger.warning.call_count == 0

    assert result == expected_result


@pytest.mark.parametrize(
    "efs_exists,expected_result",
    [pytest.param(False, False), pytest.param(True, True)],
)
def test_verify_aws_efs(efs_exists: bool, expected_result: bool):
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    efs_client_mock = Mock(
        describe_file_systems=Mock(
            return_value={"FileSystems": [{"k": "v"}]} if efs_exists else {}
        ),
        describe_mount_targets=Mock(return_value={"MountTargets": Mock()}),
    )
    boto3_session_mock = Mock(client=Mock(return_value=efs_client_mock),)
    network_interfaces_mock = generate_network_interfaces_mock(cloud_resource_mock)

    with patch.multiple(
        "anyscale.cloud_resource",
        _get_network_interfaces_from_mount_targets=Mock(
            return_value=network_interfaces_mock
        ),
    ):
        result = verify_aws_efs(
            cloud_resource=cloud_resource_mock,
            boto3_session=boto3_session_mock,
            logger=Mock(),
        )
        assert result == expected_result


@pytest.mark.parametrize(
    "cloudformation_stack_exists,expected_result",
    [pytest.param(False, False), pytest.param(True, True)],
)
def test_verify_aws_cloudformation_stack(
    cloudformation_stack_exists: bool, expected_result: bool
):
    cloud_resource_mock = generate_cloud_resource_mock_aws()
    cloudformation_stack_mock = Mock() if cloudformation_stack_exists else None
    cloudformation_mock = Mock(Stack=Mock(return_value=cloudformation_stack_mock))
    boto3_session_mock = Mock(resource=Mock(return_value=cloudformation_mock))

    result = verify_aws_cloudformation_stack(
        cloud_resource=cloud_resource_mock,
        boto3_session=boto3_session_mock,
        logger=Mock(),
    )
    assert result == expected_result
