'''
# AWS Cloud9 Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

AWS Cloud9 is a cloud-based integrated development environment (IDE) that lets you write, run, and debug your code with just a
browser. It includes a code editor, debugger, and terminal. Cloud9 comes prepackaged with essential tools for popular
programming languages, including JavaScript, Python, PHP, and more, so you don’t need to install files or configure your
development machine to start new projects. Since your Cloud9 IDE is cloud-based, you can work on your projects from your
office, home, or anywhere using an internet-connected machine. Cloud9 also provides a seamless experience for developing
serverless applications enabling you to easily define resources, debug, and switch between local and remote execution of
serverless applications. With Cloud9, you can quickly share your development environment with your team, enabling you to pair
program and track each other's inputs in real time.

## Creating EC2 Environment

EC2 Environments are defined with `Ec2Environment`. To create an EC2 environment in the private subnet, specify
`subnetSelection` with private `subnetType`.

```python
# create a cloud9 ec2 environment in a new VPC
vpc = ec2.Vpc(self, "VPC", max_azs=3)
cloud9.Ec2Environment(self, "Cloud9Env", vpc=vpc, image_id=cloud9.ImageId.AMAZON_LINUX_2)

# or create the cloud9 environment in the default VPC with specific instanceType
default_vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)
cloud9.Ec2Environment(self, "Cloud9Env2",
    vpc=default_vpc,
    instance_type=ec2.InstanceType("t3.large"),
    image_id=cloud9.ImageId.AMAZON_LINUX_2
)

# or specify in a different subnetSelection
c9env = cloud9.Ec2Environment(self, "Cloud9Env3",
    vpc=vpc,
    subnet_selection=ec2.SubnetSelection(
        subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
    ),
    image_id=cloud9.ImageId.AMAZON_LINUX_2
)

# print the Cloud9 IDE URL in the output
CfnOutput(self, "URL", value=c9env.ide_url)
```

## Specifying EC2 AMI

Use `imageId` to specify the EC2 AMI image to be used:

```python
default_vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)
cloud9.Ec2Environment(self, "Cloud9Env2",
    vpc=default_vpc,
    instance_type=ec2.InstanceType("t3.large"),
    image_id=cloud9.ImageId.UBUNTU_18_04
)
```

## Cloning Repositories

Use `clonedRepositories` to clone one or multiple AWS Codecommit repositories into the environment:

```python
import aws_cdk.aws_codecommit as codecommit

# create a new Cloud9 environment and clone the two repositories
# vpc: ec2.Vpc


# create a codecommit repository to clone into the cloud9 environment
repo_new = codecommit.Repository(self, "RepoNew",
    repository_name="new-repo"
)

# import an existing codecommit repository to clone into the cloud9 environment
repo_existing = codecommit.Repository.from_repository_name(self, "RepoExisting", "existing-repo")
cloud9.Ec2Environment(self, "C9Env",
    vpc=vpc,
    cloned_repositories=[
        cloud9.CloneRepository.from_code_commit(repo_new, "/src/new-repo"),
        cloud9.CloneRepository.from_code_commit(repo_existing, "/src/existing-repo")
    ],
    image_id=cloud9.ImageId.AMAZON_LINUX_2
)
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_codecommit as _aws_cdk_aws_codecommit_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import constructs as _constructs_77d1e7e8


class CloneRepository(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloud9-alpha.CloneRepository",
):
    '''(experimental) The class for different repository providers.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_codecommit as codecommit
        
        # create a new Cloud9 environment and clone the two repositories
        # vpc: ec2.Vpc
        
        
        # create a codecommit repository to clone into the cloud9 environment
        repo_new = codecommit.Repository(self, "RepoNew",
            repository_name="new-repo"
        )
        
        # import an existing codecommit repository to clone into the cloud9 environment
        repo_existing = codecommit.Repository.from_repository_name(self, "RepoExisting", "existing-repo")
        cloud9.Ec2Environment(self, "C9Env",
            vpc=vpc,
            cloned_repositories=[
                cloud9.CloneRepository.from_code_commit(repo_new, "/src/new-repo"),
                cloud9.CloneRepository.from_code_commit(repo_existing, "/src/existing-repo")
            ],
            image_id=cloud9.ImageId.AMAZON_LINUX_2
        )
    '''

    @jsii.member(jsii_name="fromCodeCommit")
    @builtins.classmethod
    def from_code_commit(
        cls,
        repository: _aws_cdk_aws_codecommit_ceddda9d.IRepository,
        path: builtins.str,
    ) -> "CloneRepository":
        '''(experimental) import repository to cloud9 environment from AWS CodeCommit.

        :param repository: the codecommit repository to clone from.
        :param path: the target path in cloud9 environment.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5715f24eed483fb786c815cf1538129556b87955db8377dbc98f7d312db74b8e)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("CloneRepository", jsii.sinvoke(cls, "fromCodeCommit", [repository, path]))

    @builtins.property
    @jsii.member(jsii_name="pathComponent")
    def path_component(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "pathComponent"))

    @builtins.property
    @jsii.member(jsii_name="repositoryUrl")
    def repository_url(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryUrl"))


@jsii.enum(jsii_type="@aws-cdk/aws-cloud9-alpha.ConnectionType")
class ConnectionType(enum.Enum):
    '''(experimental) The connection type used for connecting to an Amazon EC2 environment.

    :stability: experimental
    '''

    CONNECT_SSH = "CONNECT_SSH"
    '''(experimental) Connect through SSH.

    :stability: experimental
    '''
    CONNECT_SSM = "CONNECT_SSM"
    '''(experimental) Connect through AWS Systems Manager When using SSM, service role and instance profile aren't automatically created.

    See https://docs.aws.amazon.com/cloud9/latest/user-guide/ec2-ssm.html#service-role-ssm

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloud9-alpha.Ec2EnvironmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "image_id": "imageId",
        "vpc": "vpc",
        "cloned_repositories": "clonedRepositories",
        "connection_type": "connectionType",
        "description": "description",
        "ec2_environment_name": "ec2EnvironmentName",
        "instance_type": "instanceType",
        "subnet_selection": "subnetSelection",
    },
)
class Ec2EnvironmentProps:
    def __init__(
        self,
        *,
        image_id: "ImageId",
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        cloned_repositories: typing.Optional[typing.Sequence[CloneRepository]] = None,
        connection_type: typing.Optional[ConnectionType] = None,
        description: typing.Optional[builtins.str] = None,
        ec2_environment_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties for Ec2Environment.

        :param image_id: (experimental) The image ID used for creating an Amazon EC2 environment.
        :param vpc: (experimental) The VPC that AWS Cloud9 will use to communicate with the Amazon Elastic Compute Cloud (Amazon EC2) instance.
        :param cloned_repositories: (experimental) The AWS CodeCommit repository to be cloned. Default: - do not clone any repository
        :param connection_type: (experimental) The connection type used for connecting to an Amazon EC2 environment. Valid values are: CONNECT_SSH (default) and CONNECT_SSM (connected through AWS Systems Manager) Default: - CONNECT_SSH
        :param description: (experimental) Description of the environment. Default: - no description
        :param ec2_environment_name: (experimental) Name of the environment. Default: - automatically generated name
        :param instance_type: (experimental) The type of instance to connect to the environment. Default: - t2.micro
        :param subnet_selection: (experimental) The subnetSelection of the VPC that AWS Cloud9 will use to communicate with the Amazon EC2 instance. Default: - all public subnets of the VPC are selected.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_codecommit as codecommit
            
            # create a new Cloud9 environment and clone the two repositories
            # vpc: ec2.Vpc
            
            
            # create a codecommit repository to clone into the cloud9 environment
            repo_new = codecommit.Repository(self, "RepoNew",
                repository_name="new-repo"
            )
            
            # import an existing codecommit repository to clone into the cloud9 environment
            repo_existing = codecommit.Repository.from_repository_name(self, "RepoExisting", "existing-repo")
            cloud9.Ec2Environment(self, "C9Env",
                vpc=vpc,
                cloned_repositories=[
                    cloud9.CloneRepository.from_code_commit(repo_new, "/src/new-repo"),
                    cloud9.CloneRepository.from_code_commit(repo_existing, "/src/existing-repo")
                ],
                image_id=cloud9.ImageId.AMAZON_LINUX_2
            )
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b532dbafc2fd7c4838c0d7dd941df44770ef42cfe6c754418d3d7fb3a4f9c36)
            check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument cloned_repositories", value=cloned_repositories, expected_type=type_hints["cloned_repositories"])
            check_type(argname="argument connection_type", value=connection_type, expected_type=type_hints["connection_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument ec2_environment_name", value=ec2_environment_name, expected_type=type_hints["ec2_environment_name"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_id": image_id,
            "vpc": vpc,
        }
        if cloned_repositories is not None:
            self._values["cloned_repositories"] = cloned_repositories
        if connection_type is not None:
            self._values["connection_type"] = connection_type
        if description is not None:
            self._values["description"] = description
        if ec2_environment_name is not None:
            self._values["ec2_environment_name"] = ec2_environment_name
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection

    @builtins.property
    def image_id(self) -> "ImageId":
        '''(experimental) The image ID used for creating an Amazon EC2 environment.

        :stability: experimental
        '''
        result = self._values.get("image_id")
        assert result is not None, "Required property 'image_id' is missing"
        return typing.cast("ImageId", result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''(experimental) The VPC that AWS Cloud9 will use to communicate with the Amazon Elastic Compute Cloud (Amazon EC2) instance.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def cloned_repositories(self) -> typing.Optional[typing.List[CloneRepository]]:
        '''(experimental) The AWS CodeCommit repository to be cloned.

        :default: - do not clone any repository

        :stability: experimental
        '''
        result = self._values.get("cloned_repositories")
        return typing.cast(typing.Optional[typing.List[CloneRepository]], result)

    @builtins.property
    def connection_type(self) -> typing.Optional[ConnectionType]:
        '''(experimental) The connection type used for connecting to an Amazon EC2 environment.

        Valid values are: CONNECT_SSH (default) and CONNECT_SSM (connected through AWS Systems Manager)

        :default: - CONNECT_SSH

        :stability: experimental
        '''
        result = self._values.get("connection_type")
        return typing.cast(typing.Optional[ConnectionType], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of the environment.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_environment_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the environment.

        :default: - automatically generated name

        :stability: experimental
        '''
        result = self._values.get("ec2_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''(experimental) The type of instance to connect to the environment.

        :default: - t2.micro

        :stability: experimental
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) The subnetSelection of the VPC that AWS Cloud9 will use to communicate with the Amazon EC2 instance.

        :default: - all public subnets of the VPC are selected.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2EnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-cloud9-alpha.IEc2Environment")
class IEc2Environment(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) A Cloud9 Environment.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="ec2EnvironmentArn")
    def ec2_environment_arn(self) -> builtins.str:
        '''(experimental) The arn of the EnvironmentEc2.

        :stability: experimental
        :attribute: environmentE2Arn
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="ec2EnvironmentName")
    def ec2_environment_name(self) -> builtins.str:
        '''(experimental) The name of the EnvironmentEc2.

        :stability: experimental
        :attribute: environmentEc2Name
        '''
        ...


class _IEc2EnvironmentProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) A Cloud9 Environment.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cloud9-alpha.IEc2Environment"

    @builtins.property
    @jsii.member(jsii_name="ec2EnvironmentArn")
    def ec2_environment_arn(self) -> builtins.str:
        '''(experimental) The arn of the EnvironmentEc2.

        :stability: experimental
        :attribute: environmentE2Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "ec2EnvironmentArn"))

    @builtins.property
    @jsii.member(jsii_name="ec2EnvironmentName")
    def ec2_environment_name(self) -> builtins.str:
        '''(experimental) The name of the EnvironmentEc2.

        :stability: experimental
        :attribute: environmentEc2Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "ec2EnvironmentName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEc2Environment).__jsii_proxy_class__ = lambda : _IEc2EnvironmentProxy


@jsii.enum(jsii_type="@aws-cdk/aws-cloud9-alpha.ImageId")
class ImageId(enum.Enum):
    '''(experimental) The image ID used for creating an Amazon EC2 environment.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_codecommit as codecommit
        
        # create a new Cloud9 environment and clone the two repositories
        # vpc: ec2.Vpc
        
        
        # create a codecommit repository to clone into the cloud9 environment
        repo_new = codecommit.Repository(self, "RepoNew",
            repository_name="new-repo"
        )
        
        # import an existing codecommit repository to clone into the cloud9 environment
        repo_existing = codecommit.Repository.from_repository_name(self, "RepoExisting", "existing-repo")
        cloud9.Ec2Environment(self, "C9Env",
            vpc=vpc,
            cloned_repositories=[
                cloud9.CloneRepository.from_code_commit(repo_new, "/src/new-repo"),
                cloud9.CloneRepository.from_code_commit(repo_existing, "/src/existing-repo")
            ],
            image_id=cloud9.ImageId.AMAZON_LINUX_2
        )
    '''

    AMAZON_LINUX_2 = "AMAZON_LINUX_2"
    '''(experimental) Create using Amazon Linux 2.

    :stability: experimental
    '''
    UBUNTU_18_04 = "UBUNTU_18_04"
    '''(experimental) Create using Ubunut 18.04.

    :stability: experimental
    '''


@jsii.implements(IEc2Environment)
class Ec2Environment(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloud9-alpha.Ec2Environment",
):
    '''(experimental) A Cloud9 Environment with Amazon EC2.

    :stability: experimental
    :resource: AWS::Cloud9::EnvironmentEC2
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_codecommit as codecommit
        
        # create a new Cloud9 environment and clone the two repositories
        # vpc: ec2.Vpc
        
        
        # create a codecommit repository to clone into the cloud9 environment
        repo_new = codecommit.Repository(self, "RepoNew",
            repository_name="new-repo"
        )
        
        # import an existing codecommit repository to clone into the cloud9 environment
        repo_existing = codecommit.Repository.from_repository_name(self, "RepoExisting", "existing-repo")
        cloud9.Ec2Environment(self, "C9Env",
            vpc=vpc,
            cloned_repositories=[
                cloud9.CloneRepository.from_code_commit(repo_new, "/src/new-repo"),
                cloud9.CloneRepository.from_code_commit(repo_existing, "/src/existing-repo")
            ],
            image_id=cloud9.ImageId.AMAZON_LINUX_2
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image_id: ImageId,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        cloned_repositories: typing.Optional[typing.Sequence[CloneRepository]] = None,
        connection_type: typing.Optional[ConnectionType] = None,
        description: typing.Optional[builtins.str] = None,
        ec2_environment_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param image_id: (experimental) The image ID used for creating an Amazon EC2 environment.
        :param vpc: (experimental) The VPC that AWS Cloud9 will use to communicate with the Amazon Elastic Compute Cloud (Amazon EC2) instance.
        :param cloned_repositories: (experimental) The AWS CodeCommit repository to be cloned. Default: - do not clone any repository
        :param connection_type: (experimental) The connection type used for connecting to an Amazon EC2 environment. Valid values are: CONNECT_SSH (default) and CONNECT_SSM (connected through AWS Systems Manager) Default: - CONNECT_SSH
        :param description: (experimental) Description of the environment. Default: - no description
        :param ec2_environment_name: (experimental) Name of the environment. Default: - automatically generated name
        :param instance_type: (experimental) The type of instance to connect to the environment. Default: - t2.micro
        :param subnet_selection: (experimental) The subnetSelection of the VPC that AWS Cloud9 will use to communicate with the Amazon EC2 instance. Default: - all public subnets of the VPC are selected.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccb4415ff26f23d4bbd47eed0eaf906e2fa0f0c270d17e7a8ba45aac4875bc3a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = Ec2EnvironmentProps(
            image_id=image_id,
            vpc=vpc,
            cloned_repositories=cloned_repositories,
            connection_type=connection_type,
            description=description,
            ec2_environment_name=ec2_environment_name,
            instance_type=instance_type,
            subnet_selection=subnet_selection,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromEc2EnvironmentName")
    @builtins.classmethod
    def from_ec2_environment_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        ec2_environment_name: builtins.str,
    ) -> IEc2Environment:
        '''(experimental) import from EnvironmentEc2Name.

        :param scope: -
        :param id: -
        :param ec2_environment_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d751637c6d8a0fabae0fc9fff5d25771870587a93f9436dae131c0b5f45da4a5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ec2_environment_name", value=ec2_environment_name, expected_type=type_hints["ec2_environment_name"])
        return typing.cast(IEc2Environment, jsii.sinvoke(cls, "fromEc2EnvironmentName", [scope, id, ec2_environment_name]))

    @builtins.property
    @jsii.member(jsii_name="ec2EnvironmentArn")
    def ec2_environment_arn(self) -> builtins.str:
        '''(experimental) The environment ARN of this Cloud9 environment.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "ec2EnvironmentArn"))

    @builtins.property
    @jsii.member(jsii_name="ec2EnvironmentName")
    def ec2_environment_name(self) -> builtins.str:
        '''(experimental) The environment name of this Cloud9 environment.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "ec2EnvironmentName"))

    @builtins.property
    @jsii.member(jsii_name="environmentId")
    def environment_id(self) -> builtins.str:
        '''(experimental) The environment ID of this Cloud9 environment.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentId"))

    @builtins.property
    @jsii.member(jsii_name="ideUrl")
    def ide_url(self) -> builtins.str:
        '''(experimental) The complete IDE URL of this Cloud9 environment.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "ideUrl"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''(experimental) VPC ID.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))


__all__ = [
    "CloneRepository",
    "ConnectionType",
    "Ec2Environment",
    "Ec2EnvironmentProps",
    "IEc2Environment",
    "ImageId",
]

publication.publish()

def _typecheckingstub__5715f24eed483fb786c815cf1538129556b87955db8377dbc98f7d312db74b8e(
    repository: _aws_cdk_aws_codecommit_ceddda9d.IRepository,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b532dbafc2fd7c4838c0d7dd941df44770ef42cfe6c754418d3d7fb3a4f9c36(
    *,
    image_id: ImageId,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    cloned_repositories: typing.Optional[typing.Sequence[CloneRepository]] = None,
    connection_type: typing.Optional[ConnectionType] = None,
    description: typing.Optional[builtins.str] = None,
    ec2_environment_name: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb4415ff26f23d4bbd47eed0eaf906e2fa0f0c270d17e7a8ba45aac4875bc3a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_id: ImageId,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    cloned_repositories: typing.Optional[typing.Sequence[CloneRepository]] = None,
    connection_type: typing.Optional[ConnectionType] = None,
    description: typing.Optional[builtins.str] = None,
    ec2_environment_name: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d751637c6d8a0fabae0fc9fff5d25771870587a93f9436dae131c0b5f45da4a5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    ec2_environment_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
