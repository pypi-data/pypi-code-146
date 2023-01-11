import copy
import json
import os
import time
from typing import Any, Dict
from unittest.mock import Mock, patch

from packaging import version
import pytest

from anyscale.conf import MINIMUM_RAY_VERSION
from anyscale.util import (
    _check_python_version,
    _ray_version_major_minor,
    _update_external_ids_for_policy,
    DEFAULT_RAY_VERSION,
    extract_versions_from_image_name,
    get_latest_ray_version,
    get_ray_and_py_version_for_default_cluster_env,
    poll,
    populate_dict_with_workspace_config_if_exists,
    prepare_cloudformation_template,
    sleep_till,
    str_data_size,
    updating_printer,
)
from frontend.cli.anyscale.aws_iam_policies import (
    ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE,
    DEFAULT_RAY_IAM_ASSUME_ROLE_POLICY,
    get_anyscale_aws_iam_assume_role_policy,
)
from frontend.cli.anyscale.util import (
    contains_control_plane_role,
    filter_actions_from_policy_document,
)


def test_updating_printer() -> None:
    out = ""

    def mock_print(
        string: str, *args: Any, end: str = "\n", flush: bool = False, **kwargs: Any
    ) -> None:
        nonlocal out
        out += string
        out += end

    with patch("anyscale.util.print", new=mock_print), patch(
        "shutil.get_terminal_size"
    ) as get_terminal_size_mock:
        get_terminal_size_mock.return_value = (10, 24)
        with updating_printer() as print_status:
            print_status("Step 1")
            print_status("Step 2")
            print_status("Step 3")

    assert out == (
        "\r          \r"
        "Step 1"
        "\r          \r"
        "Step 2"
        "\r          \r"
        "Step 3"
        "\r          \r"
    )


def test_updating_printer_multiline() -> None:
    out = ""

    def mock_print(
        string: str, *args: Any, end: str = "\n", flush: bool = False, **kwargs: Any
    ) -> None:
        nonlocal out
        out += string
        out += end

    with patch("anyscale.util.print", new=mock_print), patch(
        "shutil.get_terminal_size"
    ) as get_terminal_size_mock:
        get_terminal_size_mock.return_value = (10, 24)
        with updating_printer() as print_status:
            print_status("Step 1\nExtra stuff")
            print_status("ExtraLongLine12345")
            print_status("ExtraLongLine12345\nExtra stuff")
            print_status("Step 3")

    assert out == (
        "\r          \r"
        "Step 1..."
        "\r          \r"
        "ExtraLo..."
        "\r          \r"
        "ExtraLo..."
        "\r          \r"
        "Step 3"
        "\r          \r"
    )


STATEMENT_TEMPLATE = {
    "Action": "sts:AssumeRole",
    "Effect": "Allow",
    "Principal": {"AWS": "arn:aws:iam::ACCT_ID:root"},
}


@pytest.mark.parametrize(
    "statement_policy,expected_conditions",
    [
        pytest.param(
            [STATEMENT_TEMPLATE],
            [{"StringEquals": {"sts:ExternalId": ["new_id"]}}],
            id="OneStatement,NoPrior",
        ),
        pytest.param(
            [STATEMENT_TEMPLATE, STATEMENT_TEMPLATE],
            [{"StringEquals": {"sts:ExternalId": ["new_id"]}}] * 2,
            id="TwoStatements,NoPrior",
        ),
        pytest.param(
            [
                {
                    "Condition": {"StringEquals": {"sts:ExternalId": "old_id"}},
                    **STATEMENT_TEMPLATE,  # type: ignore
                }
            ],
            [{"StringEquals": {"sts:ExternalId": ["old_id", "new_id"]}}],
            id="OneStatement,OnePriorExternal",
        ),
        pytest.param(
            [
                {
                    "Condition": {"StringEquals": {"sts:ExternalId": "old_id"}},
                    **STATEMENT_TEMPLATE,  # type: ignore
                },
                STATEMENT_TEMPLATE,
            ],
            [
                {"StringEquals": {"sts:ExternalId": ["old_id", "new_id"]}},
                {"StringEquals": {"sts:ExternalId": ["new_id"]}},
            ],
            id="TwoStatements,OnePriorExternal",
        ),
        pytest.param(
            [
                {
                    "Condition": {"StringNotEquals": {"sts:ExternalId": "old_id"}},
                    **STATEMENT_TEMPLATE,  # type: ignore
                },
                STATEMENT_TEMPLATE,
            ],
            [
                {
                    "StringEquals": {"sts:ExternalId": ["new_id"]},
                    "StringNotEquals": {"sts:ExternalId": "old_id"},
                },
            ],
            id="OneStatemnt,OtherCondition",
        ),
    ],
)
def test_update_external_ids_for_policy(statement_policy, expected_conditions):
    policy_document = {
        "Statement": statement_policy,
        "Version": "2012-10-17",
    }
    new_policy = _update_external_ids_for_policy(policy_document, "new_id")

    for new, expected in zip(new_policy["Statement"], expected_conditions):
        assert new["Condition"] == expected


@pytest.mark.parametrize(
    "image_name, expected, exception_substr",
    [
        ("anyscale/ray-ml:1.11.1-py38-gpu", ("py38", "1.11.1"), None),
        ("anyscale/ray:1.12-py37-cpu", ("py37", "1.12"), None),
        ("anyscale/ray:1.12-py37", ("py37", "1.12"), None),
        ("anyscale/ray:1.12py37", None, "got 1.12py37"),
    ],
)
def test_extract_versions_from_image_name(image_name, expected, exception_substr):
    if exception_substr is not None:
        with pytest.raises(ValueError) as exc_info:
            extract_versions_from_image_name(image_name)
        assert exception_substr in str(exc_info.value)
    else:
        python_version, ray_version = extract_versions_from_image_name(image_name)
        assert (python_version, ray_version) == expected


@pytest.mark.parametrize(
    "ray_version, expected, exception_substr",
    [
        ("1.12", (1, 12), None),
        ("0.0", (0, 0), None),
        ("0:0", (0, 0), "unexpected"),
        ("112", (0, 0), "unexpected"),
        ("", (0, 0), "unexpected"),
        ("1.x", (0, 0), "unexpected"),
        ("0x10.12", (0, 0), "unexpected"),
    ],
)
def test_ray_version_major_minor(ray_version, expected, exception_substr):
    if exception_substr is not None:
        with pytest.raises(Exception) as exc_info:
            _ray_version_major_minor(ray_version)
        assert exception_substr in str(exc_info.value)
    else:
        got = _ray_version_major_minor(ray_version)
        assert got == expected


@pytest.mark.parametrize(
    "python_version, exception_substr",
    [
        ("py36", None),
        ("py37", None),
        ("py38", None),
        ("py39", None),
        ("py10", "got py10"),
        ("py3.6", "got py3.6"),
        ("py3", "got py3."),
        ("py35", "got py35"),
    ],
)
def test_python_version_major_minor(python_version, exception_substr):
    if exception_substr is not None:
        with pytest.raises(Exception) as exc_info:
            _check_python_version(python_version)
        assert exception_substr in str(exc_info.value)
    else:
        _check_python_version(python_version)


def test_poll():
    """Test the poll function."""

    end_time = time.time() + 0.5
    sleep_till(end_time)
    assert time.time() == pytest.approx(end_time)

    # This should poll forever
    count = 0
    start_time = time.time()
    for i in poll(0.01):
        count += 1
        assert count == i
        if count > 100:
            break
    assert count == 101
    assert time.time() == pytest.approx(start_time + 1.01)

    # Assert we stop iterating at max iter
    expected_i = 1
    for i in poll(0.01, max_iter=5):
        assert i == expected_i
        expected_i += 1
        assert i <= 5


def test_str_data_size():
    assert str_data_size("abcd") == 4

    # Serialized form: '{"hi": "ih"}'
    assert str_data_size(json.dumps({"hi": "ih"})) == 12


def test_prepare_cloudformation_template():

    mock_region = "us-east-1"
    mock_cfn_stack_name = "mock_cfn_stack_name"
    mock_cloud_id = "mock_cloud_id"

    mock_azs = [
        "us-east-1a",
        "us-east-1b",
        "us-east-1c",
        "us-east-1d",
        "us-east-1e",
        "us-east-1f",
    ]

    with patch("anyscale.util.get_availability_zones", new=Mock(return_value=mock_azs)):
        cfn_template = prepare_cloudformation_template(
            mock_region, mock_cfn_stack_name, mock_cloud_id
        )

    assert (
        cfn_template
        == """Description: This tempalte creates the resources necessary for anyscale clouds to function.
Transform: AWS::LanguageExtensions
Parameters:
  EnvironmentName:
    Description: Anyscale deploy environment. Used in resource names and tags.
    Type: String

  CloudID:
    Description: ID of the anyscale cloud.
    Type: String

  VpcCIDR:
    Description: CIDR for the anyscale cloud VPC.
    Type: String
    Default: 10.0.0.0/16

  AnyscaleAWSAccountID:
    Description: Anyscale control plane AWS account.
    Type: String
    Default: 525325868955

  AnyscaleCrossAccountIAMRoleName:
    Description: Name of the cross account IAM role.
    Type: String

  AnyscaleCrossAccountIAMPolicySteadyState:
    Description: Stead state IAM policy document
    Type: String

  AnyscaleCrossAccountIAMPolicyInitialRun:
    Description: Initial run IAM policy document
    Type: String

  AnyscaleSecurityGroupName:
    Description: Name of the anyscale security group
    Type: String
    Default: "anyscale-security-group"

  ClusterNodeIAMRoleArn:
    Description: ARN of the data plane cluster IAM role
    Type: String

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref VpcCIDR
      EnableDnsSupport: true
      EnableDnsHostnames: true
      Tags:
        - Key: Name
          Value: !Ref AWS::StackName
        - Key: anyscale-cloud-id
          Value: !Ref CloudID
        - Key: anyscale-deploy-environment
          Value: !Ref EnvironmentName

  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: !Ref AWS::StackName
        - Key: anyscale-cloud-id
          Value: !Ref CloudID
        - Key: anyscale-deploy-environment
          Value: !Ref EnvironmentName

  InternetGatewayAttachment:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      InternetGatewayId: !Ref InternetGateway
      VpcId: !Ref VPC


  Subnet0:
    Type: AWS::EC2::Subnet
    Properties:
        VpcId: !Ref VPC
        AvailabilityZone: us-east-1a
        CidrBlock: 10.0.0.0/19
        MapPublicIpOnLaunch: true
        Tags:
        - Key: Name
          Value: mock_cfn_stack_name-subnet-us-east-1a
        - Key: anyscale-cloud-id
          Value: mock_cloud_id

  Subnet1:
    Type: AWS::EC2::Subnet
    Properties:
        VpcId: !Ref VPC
        AvailabilityZone: us-east-1b
        CidrBlock: 10.0.32.0/19
        MapPublicIpOnLaunch: true
        Tags:
        - Key: Name
          Value: mock_cfn_stack_name-subnet-us-east-1b
        - Key: anyscale-cloud-id
          Value: mock_cloud_id

  Subnet2:
    Type: AWS::EC2::Subnet
    Properties:
        VpcId: !Ref VPC
        AvailabilityZone: us-east-1c
        CidrBlock: 10.0.64.0/19
        MapPublicIpOnLaunch: true
        Tags:
        - Key: Name
          Value: mock_cfn_stack_name-subnet-us-east-1c
        - Key: anyscale-cloud-id
          Value: mock_cloud_id

  Subnet3:
    Type: AWS::EC2::Subnet
    Properties:
        VpcId: !Ref VPC
        AvailabilityZone: us-east-1d
        CidrBlock: 10.0.96.0/19
        MapPublicIpOnLaunch: true
        Tags:
        - Key: Name
          Value: mock_cfn_stack_name-subnet-us-east-1d
        - Key: anyscale-cloud-id
          Value: mock_cloud_id

  Subnet4:
    Type: AWS::EC2::Subnet
    Properties:
        VpcId: !Ref VPC
        AvailabilityZone: us-east-1e
        CidrBlock: 10.0.128.0/19
        MapPublicIpOnLaunch: true
        Tags:
        - Key: Name
          Value: mock_cfn_stack_name-subnet-us-east-1e
        - Key: anyscale-cloud-id
          Value: mock_cloud_id

  Subnet5:
    Type: AWS::EC2::Subnet
    Properties:
        VpcId: !Ref VPC
        AvailabilityZone: us-east-1f
        CidrBlock: 10.0.160.0/19
        MapPublicIpOnLaunch: true
        Tags:
        - Key: Name
          Value: mock_cfn_stack_name-subnet-us-east-1f
        - Key: anyscale-cloud-id
          Value: mock_cloud_id

  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub ${AWS::StackName} Public Routes
        - Key: anyscale-cloud-id
          Value: !Ref CloudID
        - Key: anyscale-deploy-environment
          Value: !Ref EnvironmentName

  DefaultPublicRoute:
    Type: AWS::EC2::Route
    DependsOn: InternetGatewayAttachment
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway


  Subnet0RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
        RouteTableId: !Ref PublicRouteTable
        SubnetId: !Ref Subnet0

  Subnet1RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
        RouteTableId: !Ref PublicRouteTable
        SubnetId: !Ref Subnet1

  Subnet2RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
        RouteTableId: !Ref PublicRouteTable
        SubnetId: !Ref Subnet2

  Subnet3RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
        RouteTableId: !Ref PublicRouteTable
        SubnetId: !Ref Subnet3

  Subnet4RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
        RouteTableId: !Ref PublicRouteTable
        SubnetId: !Ref Subnet4

  Subnet5RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
        RouteTableId: !Ref PublicRouteTable
        SubnetId: !Ref Subnet5

  AnyscaleSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Ref AnyscaleSecurityGroupName
      GroupDescription: "Anyscale security group"
      VpcId: !Ref VPC
      SecurityGroupIngress:
        # For https
        - IpProtocol: "tcp"
          FromPort: 443
          ToPort: 443
          CidrIp: "0.0.0.0/0"
        # For ssh
        - IpProtocol: "tcp"
          FromPort: 22
          ToPort: 22
          CidrIp: "0.0.0.0/0"
      Tags:
        - Key: anyscale-cloud-id
          Value: !Ref CloudID
        - Key: anyscale-deploy-environment
          Value: !Ref EnvironmentName

  # This allows ray cluster nodes to talk to each other since all nodes have the same security group attached.
  # This also allows ray cluster nodes to talk to EFS since they have the same security group attached.
  AnyscaleSecurityGroupIntraClusterIngressRule:
    Type: AWS::EC2::SecurityGroupIngress
    Properties:
      IpProtocol: "-1"
      GroupId: !Ref AnyscaleSecurityGroup
      SourceSecurityGroupId: !Ref AnyscaleSecurityGroup

  S3Bucket:
    Type: AWS::S3::Bucket
    Description: Anyscale managed s3 bucket.
    DeletionPolicy: Retain
    Properties:
      BucketName: !Sub anyscale-${EnvironmentName}-data-${AWS::StackName}
      CorsConfiguration:
        CorsRules:
          - AllowedHeaders:
              - '*'
            AllowedMethods:
              - GET
            AllowedOrigins:
              - https://console.anyscale.com
            Id: AnyscaleCORSRule
      PublicAccessBlockConfiguration:
        BlockPublicAcls: True
        BlockPublicPolicy: True
        IgnorePublicAcls: True
        RestrictPublicBuckets: True
      Tags:
        - Key: anyscale-cloud-id
          Value: !Ref CloudID
        - Key: anyscale-deploy-environment
          Value: !Ref EnvironmentName

  S3BucketPolicy:
    Type: AWS::S3::BucketPolicy
    Description: Bucket policy that allow ray autoscaler role to access the bucket.
    Properties:
      Bucket: !Ref S3Bucket
      PolicyDocument:
        Version: 2012-10-17
        Statement:
          - Action:
              - "s3:PutObject"
              - "s3:DeleteObject"
              - "s3:GetObject"
              - "s3:ListBucket"
            Effect: Allow
            Resource:
              - !Sub arn:aws:s3:::${S3Bucket}
              - !Sub arn:aws:s3:::${S3Bucket}/*
            Principal:
              AWS:
                - !Ref ClusterNodeIAMRoleArn
                - !GetAtt
                  - customerRole
                  - Arn
  EFS:
    Type: AWS::EFS::FileSystem
    Properties:
        BackupPolicy:
          Status: ENABLED
        Encrypted: true
        LifecyclePolicies:
          - TransitionToIA: AFTER_60_DAYS
        PerformanceMode: generalPurpose
        Encrypted: true
        ThroughputMode: bursting
        FileSystemTags:
          - Key: anyscale-cloud-id
            Value: !Ref CloudID
          - Key: anyscale-deploy-environment
            Value: !Ref EnvironmentName

  EFSMountTarget:
    Type: AWS::EFS::MountTarget
    Properties:
        FileSystemId: !Ref EFS
        SecurityGroups:
          - !Ref AnyscaleSecurityGroup
        SubnetId: !Ref Subnet1

  customerRole:
    Type: 'AWS::IAM::Role'
    Properties:
      RoleName: !Ref AnyscaleCrossAccountIAMRoleName
      AssumeRolePolicyDocument:
        Statement:
          - Action: 'sts:AssumeRole'
            Effect: Allow
            Principal:
              AWS: !Ref AnyscaleAWSAccountID
            Sid: 'AnyscaleControlPlaneAssumeRole'
            Condition:
              StringEquals:
                  sts:ExternalId: !Ref CloudID
        Version: 2012-10-17
      Path: /
      Tags:
        - Key: Name
          Value: !Ref AWS::StackName
        - Key: anyscale-cloud-id
          Value: !Ref CloudID
        - Key: anyscale-deploy-environment
          Value: !Ref EnvironmentName

  IAMPermissionEC2SteadyState:
    Type: AWS::IAM::Policy
    Properties:
      PolicyDocument: !Ref AnyscaleCrossAccountIAMPolicySteadyState
      PolicyName: Anyscale_IAM_Policy_Steady_State
      Roles:
        - !Ref customerRole

  IAMPermissionEC2InitialRun:
    Type: AWS::IAM::Policy
    Properties:
      PolicyDocument: !Ref AnyscaleCrossAccountIAMPolicyInitialRun
      PolicyName: Anyscale_IAM_Policy_Initial_Setup
      Roles:
        - !Ref customerRole

Outputs:
  VPC:
    Description: A reference to the created VPC
    Value: !Ref VPC

  SubnetsWithAvailabilityZones:
    Description: A list of the subnets with their availability zones
    Value:
      Fn::ToJsonString:
        [{"subnet_id": !Ref Subnet0, "availability_zone": !GetAtt Subnet0.AvailabilityZone},{"subnet_id": !Ref Subnet1, "availability_zone": !GetAtt Subnet1.AvailabilityZone},{"subnet_id": !Ref Subnet2, "availability_zone": !GetAtt Subnet2.AvailabilityZone},{"subnet_id": !Ref Subnet3, "availability_zone": !GetAtt Subnet3.AvailabilityZone},{"subnet_id": !Ref Subnet4, "availability_zone": !GetAtt Subnet4.AvailabilityZone},{"subnet_id": !Ref Subnet5, "availability_zone": !GetAtt Subnet5.AvailabilityZone}]

  AnyscaleSecurityGroup:
    Description: Anyscale Security group
    Value: !Ref AnyscaleSecurityGroup

  S3Bucket:
    Description: Anyscale managed S3 bucket
    Value: !Ref S3Bucket

  EFS:
    Description: Anyscale managed EFS
    Value: !Ref EFS

  EFSMountTargetIP:
    Description: Anyscale managed EFS mount target
    Value: !GetAtt
      - EFSMountTarget
      - IpAddress

  AnyscaleIAMRole:
    Description: ARN of the cross-account IAM role
    Value: !GetAtt
      - customerRole
      - Arn
"""
    )


@pytest.mark.parametrize("request_output", ["mock_latest_version", Exception()])
def test_get_latest_ray_version(request_output):
    if isinstance(request_output, str):
        mock_get = Mock(
            return_value=Mock(
                json=Mock(return_value={"info": {"version": request_output}})
            )
        )
    else:
        mock_get = Mock(side_effect=request_output)

    expected_latest_version = (
        request_output if isinstance(request_output, str) else DEFAULT_RAY_VERSION
    )
    with patch.multiple("anyscale.util.requests", get=mock_get):
        latest_ray_version = get_latest_ray_version()
        assert latest_ray_version == expected_latest_version
    mock_get.assert_called_once_with("https://pypi.org/pypi/ray/json")


@pytest.mark.parametrize(
    "pyversion_param", [["3", "6"], ["3", "7"], ["3", "8"], ["3", "9"]]
)
def test_get_ray_and_py_version_for_default_cluster_env(pyversion_param):
    # TODO(nikita): This test should be run in an environment that has Ray
    # installed, and one that doesn't have Ray installed. The
    # `import ray` statement inside the method cannot be mocked.
    mock_get_latest_ray_version = Mock(return_value="mock_latest_ray_version")
    with patch.multiple(
        "anyscale.util.sys", version_info=pyversion_param
    ), patch.multiple(
        "anyscale.util", get_latest_ray_version=mock_get_latest_ray_version
    ):
        ray_version, pyversion = get_ray_and_py_version_for_default_cluster_env()
    assert pyversion == "".join(str(x) for x in pyversion_param)
    try:
        import ray

        assert version.parse(ray_version) == version.parse(ray.__version__)
        assert version.parse(ray_version) >= version.parse(MINIMUM_RAY_VERSION)
    except ImportError:
        assert ray_version == "mock_latest_ray_version"


@pytest.mark.parametrize(
    "config_dict",
    [
        {},
        {"name": "test-job"},
        {
            "name": "test-job",
            "entrypoint": "python test.py",
            "build_id": "test_build_id",
            "compute_config_id": "test_compute_config_id",
        },
        {
            "name": "test-job",
            "entrypoint": "python test.py",
            "build_id": "test_build_id",
            "cloud": "test_cloud_name",
        },
    ],
)
def test_populate_dict_method(config_dict):
    original_dict = copy.deepcopy(config_dict)
    updated_dict = populate_dict_with_workspace_config_if_exists(config_dict, Mock())
    assert original_dict == updated_dict


@pytest.mark.parametrize(
    "config_dict",
    [
        {"name": "test-job"},
        {"name": "test-job", "entrypoint": "python test.py"},
        {
            "name": "test-job",
            "entrypoint": "python test.py",
            "compute_config_id": "user_provided_compute_config_id",
        },
        {
            "name": "test-job",
            "entrypoint": "python test.py",
            "build_id": "user_provided_build_id",
        },
        {
            "name": "test-job",
            "entrypoint": "python test.py",
            "project_id": "user_provided_project_id",
            "build_id": "user_provided_build_id",
            "compute_config_id": "user_provided_compute_config_id",
        },
    ],
)
def test_populate_dict_method_in_workspace(config_dict: Dict[str, Any]):
    original_dict = copy.deepcopy(config_dict)
    mock_base_api_client = Mock()
    values_from_cluster = {
        "project_id": "test_project_id",
        "cluster_compute_id": "test_compute_config_id",
        "cluster_environment_build_id": "test_build_id",
    }
    parsed_config = {
        "project_id": "test_project_id",
        "compute_config_id": "test_compute_config_id",
        "build_id": "test_build_id",
    }
    mock_cluster = Mock(**values_from_cluster)
    mock_base_api_client.get_cluster = Mock(return_value=Mock(result=mock_cluster))
    with patch.dict(
        os.environ,
        {
            "ANYSCALE_EXPERIMENTAL_WORKSPACE_ID": "Test_workspace_id",
            "ANYSCALE_SESSION_ID": "test_session_id",
        },
        clear=True,
    ):
        updated_dict = populate_dict_with_workspace_config_if_exists(
            config_dict, mock_base_api_client
        )

    # The values from the original dict takes priority
    assert dict(parsed_config, **original_dict) == updated_dict


@pytest.mark.parametrize(
    "policy_document,expected_actions",
    [
        pytest.param(
            ANYSCALE_IAM_PERMISSIONS_EC2_STEADY_STATE,
            {
                "iam:PassRole",
                "iam:GetInstanceProfile",
                "ec2:DescribeAvailabilityZones",
                "ec2:DescribeInstanceTypes",
                "ec2:DescribeRegions",
                "ec2:DescribeInstances",
                "ec2:DescribeSubnets",
                "ec2:DescribeRouteTables",
                "ec2:DescribeSecurityGroups",
                "ec2:RunInstances",
                "ec2:StartInstances",
                "ec2:StopInstances",
                "ec2:TerminateInstances",
                "ec2:CreateTags",
                "ec2:DeleteTags",
                "ec2:CancelSpotInstanceRequests",
                "ec2:ModifyImageAttribute",
                "ec2:ModifyInstanceAttribute",
                "ec2:RequestSpotInstances",
                "ec2:AttachVolume",
                "ec2:CreateVolume",
                "ec2:DescribeVolumes",
                "ec2:AssociateIamInstanceProfile",
                "ec2:DisassociateIamInstanceProfile",
                "ec2:ReplaceIamInstanceProfileAssociation",
                "ec2:CreatePlacementGroup",
                "ec2:AllocateAddress",
                "ec2:ReleaseAddress",
                "ec2:DescribeIamInstanceProfileAssociations",
                "ec2:DescribeInstanceStatus",
                "ec2:DescribePlacementGroups",
                "ec2:DescribePrefixLists",
                "ec2:DescribeReservedInstancesOfferings",
                "ec2:DescribeSpotInstanceRequests",
                "ec2:DescribeSpotPriceHistory",
                "elasticfilesystem:DescribeMountTargets",
            },
        ),
        pytest.param(DEFAULT_RAY_IAM_ASSUME_ROLE_POLICY, {"sts:AssumeRole"},),
        pytest.param(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"Service": ["ec2.amazonaws.com"]},
                        "Action": ["sts:AssumeRole", "sts:AssumeRole"],
                    },
                    {
                        "Effect": "Allow",
                        "Principal": {"Service": ["ec2.amazonaws.com"]},
                        "Action": ["sts:AssumeRole", "sts:AssumeRole"],
                    },
                ],
            },
            {"sts:AssumeRole"},
        ),
        pytest.param(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Deny",
                        "Principal": {"Service": ["ec2.amazonaws.com"]},
                        "Action": ["sts:AssumeRole", "sts:AssumeRole"],
                    },
                    {
                        "Effect": "Deny",
                        "Principal": {"Service": ["ec2.amazonaws.com"]},
                        "Action": ["sts:AssumeRole", "sts:AssumeRole"],
                    },
                ],
            },
            set(),
        ),
    ],
)
def test_filter_actions_from_policy_document(policy_document, expected_actions):
    actions = filter_actions_from_policy_document(policy_document=policy_document)
    assert actions == expected_actions


@pytest.mark.parametrize(
    "assume_role_policy_document,expected_result",
    [
        pytest.param(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"AWS": "000000"},
                        "Action": "sts:AssumeRole",
                    },
                ],
            },
            True,
        ),
        pytest.param(
            get_anyscale_aws_iam_assume_role_policy(anyscale_aws_account="000000"),
            True,
        ),
        pytest.param(
            {
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": [
                                "arn:aws:iam::other_account",
                                "arn:aws:iam::000000:root",
                            ]
                        },
                        "Action": "sts:AssumeRole",
                    },
                ],
            },
            True,
        ),
        pytest.param(
            {
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": [
                                "arn:aws:iam::other_account",
                                "arn:aws:iam::another_account:root",
                            ]
                        },
                        "Action": "sts:AssumeRole",
                    },
                ],
            },
            False,
        ),
        pytest.param(
            {
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"Service": "arn:aws:iam::000000:root"},
                        "Action": "sts:AssumeRole",
                    },
                ],
            },
            False,
        ),
    ],
)
def test_contains_control_plane_role(assume_role_policy_document, expected_result):
    result = contains_control_plane_role(
        assume_role_policy_document=assume_role_policy_document,
        anyscale_aws_account="000000",
    )
    assert result == expected_result
