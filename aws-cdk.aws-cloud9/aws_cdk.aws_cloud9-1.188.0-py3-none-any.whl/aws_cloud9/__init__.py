'''
# AWS Cloud9 Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

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
cloud9.Ec2Environment(self, "Cloud9Env", vpc=vpc)

# or create the cloud9 environment in the default VPC with specific instanceType
default_vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)
cloud9.Ec2Environment(self, "Cloud9Env2",
    vpc=default_vpc,
    instance_type=ec2.InstanceType("t3.large")
)

# or specify in a different subnetSelection
c9env = cloud9.Ec2Environment(self, "Cloud9Env3",
    vpc=vpc,
    subnet_selection=ec2.SubnetSelection(
        subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
    )
)

# print the Cloud9 IDE URL in the output
CfnOutput(self, "URL", value=c9env.ide_url)
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
    ]
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

import aws_cdk.aws_codecommit as _aws_cdk_aws_codecommit_692dd32c
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_67de8e8d
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnEnvironmentEC2(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloud9.CfnEnvironmentEC2",
):
    '''A CloudFormation ``AWS::Cloud9::EnvironmentEC2``.

    The ``AWS::Cloud9::EnvironmentEC2`` resource creates an Amazon EC2 development environment in AWS Cloud9 . For more information, see `Creating an Environment <https://docs.aws.amazon.com/cloud9/latest/user-guide/create-environment.html>`_ in the *AWS Cloud9 User Guide* .

    :cloudformationResource: AWS::Cloud9::EnvironmentEC2
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_cloud9 as cloud9
        
        cfn_environment_eC2 = cloud9.CfnEnvironmentEC2(self, "MyCfnEnvironmentEC2",
            instance_type="instanceType",
        
            # the properties below are optional
            automatic_stop_time_minutes=123,
            connection_type="connectionType",
            description="description",
            image_id="imageId",
            name="name",
            owner_arn="ownerArn",
            repositories=[cloud9.CfnEnvironmentEC2.RepositoryProperty(
                path_component="pathComponent",
                repository_url="repositoryUrl"
            )],
            subnet_id="subnetId",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        instance_type: builtins.str,
        automatic_stop_time_minutes: typing.Optional[jsii.Number] = None,
        connection_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        image_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        owner_arn: typing.Optional[builtins.str] = None,
        repositories: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union["CfnEnvironmentEC2.RepositoryProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Cloud9::EnvironmentEC2``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_type: The type of instance to connect to the environment (for example, ``t2.micro`` ).
        :param automatic_stop_time_minutes: The number of minutes until the running instance is shut down after the environment was last used.
        :param connection_type: The connection type used for connecting to an Amazon EC2 environment. Valid values are ``CONNECT_SSH`` (default) and ``CONNECT_SSM`` (connected through AWS Systems Manager ).
        :param description: The description of the environment to create.
        :param image_id: The identifier for the Amazon Machine Image (AMI) that's used to create the EC2 instance. To choose an AMI for the instance, you must specify a valid AMI alias or a valid AWS Systems Manager path. The default AMI is used if the parameter isn't explicitly assigned a value in the request. *AMI aliases* - *Amazon Linux (default): ``amazonlinux-1-x86_64``* - Amazon Linux 2: ``amazonlinux-2-x86_64`` - Ubuntu 18.04: ``ubuntu-18.04-x86_64`` *SSM paths* - *Amazon Linux (default): ``resolve:ssm:/aws/service/cloud9/amis/amazonlinux-1-x86_64``* - Amazon Linux 2: ``resolve:ssm:/aws/service/cloud9/amis/amazonlinux-2-x86_64`` - Ubuntu 18.04: ``resolve:ssm:/aws/service/cloud9/amis/ubuntu-18.04-x86_64``
        :param name: The name of the environment.
        :param owner_arn: The Amazon Resource Name (ARN) of the environment owner. This ARN can be the ARN of any AWS Identity and Access Management principal. If this value is not specified, the ARN defaults to this environment's creator.
        :param repositories: Any AWS CodeCommit source code repositories to be cloned into the development environment.
        :param subnet_id: The ID of the subnet in Amazon Virtual Private Cloud (Amazon VPC) that AWS Cloud9 will use to communicate with the Amazon Elastic Compute Cloud (Amazon EC2) instance.
        :param tags: An array of key-value pairs that will be associated with the new AWS Cloud9 development environment.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ef001bf4de14efb43e2f14efb064bafe67bf100ece9581c3443b457e29c412d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEnvironmentEC2Props(
            instance_type=instance_type,
            automatic_stop_time_minutes=automatic_stop_time_minutes,
            connection_type=connection_type,
            description=description,
            image_id=image_id,
            name=name,
            owner_arn=owner_arn,
            repositories=repositories,
            subnet_id=subnet_id,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7f42337ef2529ba5ebec429c25e2db3649fee8e55e44712602de4ac9e41d2d)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f6f92dd2830861bf1bd59423ebfb32c8279709b743cdd6e14723ba3cfc63475)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the development environment, such as ``arn:aws:cloud9:us-east-2:123456789012:environment:2bc3642873c342e485f7e0c561234567`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''The name of the environment.

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs that will be associated with the new AWS Cloud9 development environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        '''The type of instance to connect to the environment (for example, ``t2.micro`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-instancetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee3b5ffb534e9db1b863f88e365316c39cf5af4ecba3abb686a8f2d3698dc31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="automaticStopTimeMinutes")
    def automatic_stop_time_minutes(self) -> typing.Optional[jsii.Number]:
        '''The number of minutes until the running instance is shut down after the environment was last used.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-automaticstoptimeminutes
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "automaticStopTimeMinutes"))

    @automatic_stop_time_minutes.setter
    def automatic_stop_time_minutes(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bfacb916666563965d17d0d6b97cc3bd1f4960a91b8865a25f52898b3e0c083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automaticStopTimeMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def connection_type(self) -> typing.Optional[builtins.str]:
        '''The connection type used for connecting to an Amazon EC2 environment.

        Valid values are ``CONNECT_SSH`` (default) and ``CONNECT_SSM`` (connected through AWS Systems Manager ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-connectiontype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionType"))

    @connection_type.setter
    def connection_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a8539e2d0dabd697b9787fd831ce368932946e7631809fb174a07fb2ff2d88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionType", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the environment to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f17f0ad701068ea3f26386011592c6495cda01463205ee6833a91635a0bb8d20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> typing.Optional[builtins.str]:
        '''The identifier for the Amazon Machine Image (AMI) that's used to create the EC2 instance.

        To choose an AMI for the instance, you must specify a valid AMI alias or a valid AWS Systems Manager path.

        The default AMI is used if the parameter isn't explicitly assigned a value in the request.

        *AMI aliases*

        - *Amazon Linux (default): ``amazonlinux-1-x86_64``*
        - Amazon Linux 2: ``amazonlinux-2-x86_64``
        - Ubuntu 18.04: ``ubuntu-18.04-x86_64``

        *SSM paths*

        - *Amazon Linux (default): ``resolve:ssm:/aws/service/cloud9/amis/amazonlinux-1-x86_64``*
        - Amazon Linux 2: ``resolve:ssm:/aws/service/cloud9/amis/amazonlinux-2-x86_64``
        - Ubuntu 18.04: ``resolve:ssm:/aws/service/cloud9/amis/ubuntu-18.04-x86_64``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-imageid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageId"))

    @image_id.setter
    def image_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8b727883922a845604ced8dfc1e9457b4e92f6ec4074ff651699afed670cdf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a11fd8c6369ae96dba8413bab23048418689b507e734a18714e4f37d2be186f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="ownerArn")
    def owner_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the environment owner.

        This ARN can be the ARN of any AWS Identity and Access Management principal. If this value is not specified, the ARN defaults to this environment's creator.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-ownerarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerArn"))

    @owner_arn.setter
    def owner_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1696f3784c2082c0a42062fd11bc8a4e1ae04790e629f13939aa8e8d3494de3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ownerArn", value)

    @builtins.property
    @jsii.member(jsii_name="repositories")
    def repositories(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnEnvironmentEC2.RepositoryProperty", _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''Any AWS CodeCommit source code repositories to be cloned into the development environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-repositories
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnEnvironmentEC2.RepositoryProperty", _aws_cdk_core_f4b25747.IResolvable]]]], jsii.get(self, "repositories"))

    @repositories.setter
    def repositories(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnEnvironmentEC2.RepositoryProperty", _aws_cdk_core_f4b25747.IResolvable]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c2c1692b3309dae9ac320a2c92999f53ab1bc244bf04c509c2c2cc93cb78e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositories", value)

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the subnet in Amazon Virtual Private Cloud (Amazon VPC) that AWS Cloud9 will use to communicate with the Amazon Elastic Compute Cloud (Amazon EC2) instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-subnetid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37ab8081309b904e48eadc4d411e6e149b0e34b57934043c490b878e782edbdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-cloud9.CfnEnvironmentEC2.RepositoryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "path_component": "pathComponent",
            "repository_url": "repositoryUrl",
        },
    )
    class RepositoryProperty:
        def __init__(
            self,
            *,
            path_component: builtins.str,
            repository_url: builtins.str,
        ) -> None:
            '''The ``Repository`` property type specifies an AWS CodeCommit source code repository to be cloned into an AWS Cloud9 development environment.

            :param path_component: The path within the development environment's default file system location to clone the AWS CodeCommit repository into. For example, ``/REPOSITORY_NAME`` would clone the repository into the ``/home/USER_NAME/environment/REPOSITORY_NAME`` directory in the environment.
            :param repository_url: The clone URL of the AWS CodeCommit repository to be cloned. For example, for an AWS CodeCommit repository this might be ``https://git-codecommit.us-east-2.amazonaws.com/v1/repos/REPOSITORY_NAME`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloud9-environmentec2-repository.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_cloud9 as cloud9
                
                repository_property = cloud9.CfnEnvironmentEC2.RepositoryProperty(
                    path_component="pathComponent",
                    repository_url="repositoryUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__345d4f5e55d88315961d456d5b4e9e28e6cc5882d70b8f9f79eff8e139cae234)
                check_type(argname="argument path_component", value=path_component, expected_type=type_hints["path_component"])
                check_type(argname="argument repository_url", value=repository_url, expected_type=type_hints["repository_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "path_component": path_component,
                "repository_url": repository_url,
            }

        @builtins.property
        def path_component(self) -> builtins.str:
            '''The path within the development environment's default file system location to clone the AWS CodeCommit repository into.

            For example, ``/REPOSITORY_NAME`` would clone the repository into the ``/home/USER_NAME/environment/REPOSITORY_NAME`` directory in the environment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloud9-environmentec2-repository.html#cfn-cloud9-environmentec2-repository-pathcomponent
            '''
            result = self._values.get("path_component")
            assert result is not None, "Required property 'path_component' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def repository_url(self) -> builtins.str:
            '''The clone URL of the AWS CodeCommit repository to be cloned.

            For example, for an AWS CodeCommit repository this might be ``https://git-codecommit.us-east-2.amazonaws.com/v1/repos/REPOSITORY_NAME`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloud9-environmentec2-repository.html#cfn-cloud9-environmentec2-repository-repositoryurl
            '''
            result = self._values.get("repository_url")
            assert result is not None, "Required property 'repository_url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RepositoryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloud9.CfnEnvironmentEC2Props",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "automatic_stop_time_minutes": "automaticStopTimeMinutes",
        "connection_type": "connectionType",
        "description": "description",
        "image_id": "imageId",
        "name": "name",
        "owner_arn": "ownerArn",
        "repositories": "repositories",
        "subnet_id": "subnetId",
        "tags": "tags",
    },
)
class CfnEnvironmentEC2Props:
    def __init__(
        self,
        *,
        instance_type: builtins.str,
        automatic_stop_time_minutes: typing.Optional[jsii.Number] = None,
        connection_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        image_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        owner_arn: typing.Optional[builtins.str] = None,
        repositories: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnEnvironmentEC2.RepositoryProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnEnvironmentEC2``.

        :param instance_type: The type of instance to connect to the environment (for example, ``t2.micro`` ).
        :param automatic_stop_time_minutes: The number of minutes until the running instance is shut down after the environment was last used.
        :param connection_type: The connection type used for connecting to an Amazon EC2 environment. Valid values are ``CONNECT_SSH`` (default) and ``CONNECT_SSM`` (connected through AWS Systems Manager ).
        :param description: The description of the environment to create.
        :param image_id: The identifier for the Amazon Machine Image (AMI) that's used to create the EC2 instance. To choose an AMI for the instance, you must specify a valid AMI alias or a valid AWS Systems Manager path. The default AMI is used if the parameter isn't explicitly assigned a value in the request. *AMI aliases* - *Amazon Linux (default): ``amazonlinux-1-x86_64``* - Amazon Linux 2: ``amazonlinux-2-x86_64`` - Ubuntu 18.04: ``ubuntu-18.04-x86_64`` *SSM paths* - *Amazon Linux (default): ``resolve:ssm:/aws/service/cloud9/amis/amazonlinux-1-x86_64``* - Amazon Linux 2: ``resolve:ssm:/aws/service/cloud9/amis/amazonlinux-2-x86_64`` - Ubuntu 18.04: ``resolve:ssm:/aws/service/cloud9/amis/ubuntu-18.04-x86_64``
        :param name: The name of the environment.
        :param owner_arn: The Amazon Resource Name (ARN) of the environment owner. This ARN can be the ARN of any AWS Identity and Access Management principal. If this value is not specified, the ARN defaults to this environment's creator.
        :param repositories: Any AWS CodeCommit source code repositories to be cloned into the development environment.
        :param subnet_id: The ID of the subnet in Amazon Virtual Private Cloud (Amazon VPC) that AWS Cloud9 will use to communicate with the Amazon Elastic Compute Cloud (Amazon EC2) instance.
        :param tags: An array of key-value pairs that will be associated with the new AWS Cloud9 development environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_cloud9 as cloud9
            
            cfn_environment_eC2_props = cloud9.CfnEnvironmentEC2Props(
                instance_type="instanceType",
            
                # the properties below are optional
                automatic_stop_time_minutes=123,
                connection_type="connectionType",
                description="description",
                image_id="imageId",
                name="name",
                owner_arn="ownerArn",
                repositories=[cloud9.CfnEnvironmentEC2.RepositoryProperty(
                    path_component="pathComponent",
                    repository_url="repositoryUrl"
                )],
                subnet_id="subnetId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c82c4a8b3b96c7c641defd2e0263a0566263d37ff96b2b62ad4068f2f26b12)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument automatic_stop_time_minutes", value=automatic_stop_time_minutes, expected_type=type_hints["automatic_stop_time_minutes"])
            check_type(argname="argument connection_type", value=connection_type, expected_type=type_hints["connection_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument owner_arn", value=owner_arn, expected_type=type_hints["owner_arn"])
            check_type(argname="argument repositories", value=repositories, expected_type=type_hints["repositories"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_type": instance_type,
        }
        if automatic_stop_time_minutes is not None:
            self._values["automatic_stop_time_minutes"] = automatic_stop_time_minutes
        if connection_type is not None:
            self._values["connection_type"] = connection_type
        if description is not None:
            self._values["description"] = description
        if image_id is not None:
            self._values["image_id"] = image_id
        if name is not None:
            self._values["name"] = name
        if owner_arn is not None:
            self._values["owner_arn"] = owner_arn
        if repositories is not None:
            self._values["repositories"] = repositories
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def instance_type(self) -> builtins.str:
        '''The type of instance to connect to the environment (for example, ``t2.micro`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-instancetype
        '''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def automatic_stop_time_minutes(self) -> typing.Optional[jsii.Number]:
        '''The number of minutes until the running instance is shut down after the environment was last used.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-automaticstoptimeminutes
        '''
        result = self._values.get("automatic_stop_time_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def connection_type(self) -> typing.Optional[builtins.str]:
        '''The connection type used for connecting to an Amazon EC2 environment.

        Valid values are ``CONNECT_SSH`` (default) and ``CONNECT_SSM`` (connected through AWS Systems Manager ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-connectiontype
        '''
        result = self._values.get("connection_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the environment to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_id(self) -> typing.Optional[builtins.str]:
        '''The identifier for the Amazon Machine Image (AMI) that's used to create the EC2 instance.

        To choose an AMI for the instance, you must specify a valid AMI alias or a valid AWS Systems Manager path.

        The default AMI is used if the parameter isn't explicitly assigned a value in the request.

        *AMI aliases*

        - *Amazon Linux (default): ``amazonlinux-1-x86_64``*
        - Amazon Linux 2: ``amazonlinux-2-x86_64``
        - Ubuntu 18.04: ``ubuntu-18.04-x86_64``

        *SSM paths*

        - *Amazon Linux (default): ``resolve:ssm:/aws/service/cloud9/amis/amazonlinux-1-x86_64``*
        - Amazon Linux 2: ``resolve:ssm:/aws/service/cloud9/amis/amazonlinux-2-x86_64``
        - Ubuntu 18.04: ``resolve:ssm:/aws/service/cloud9/amis/ubuntu-18.04-x86_64``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-imageid
        '''
        result = self._values.get("image_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the environment owner.

        This ARN can be the ARN of any AWS Identity and Access Management principal. If this value is not specified, the ARN defaults to this environment's creator.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-ownerarn
        '''
        result = self._values.get("owner_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repositories(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnEnvironmentEC2.RepositoryProperty, _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''Any AWS CodeCommit source code repositories to be cloned into the development environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-repositories
        '''
        result = self._values.get("repositories")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnEnvironmentEC2.RepositoryProperty, _aws_cdk_core_f4b25747.IResolvable]]]], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the subnet in Amazon Virtual Private Cloud (Amazon VPC) that AWS Cloud9 will use to communicate with the Amazon Elastic Compute Cloud (Amazon EC2) instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-subnetid
        '''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs that will be associated with the new AWS Cloud9 development environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloud9-environmentec2.html#cfn-cloud9-environmentec2-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentEC2Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloneRepository(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloud9.CloneRepository",
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
            ]
        )
    '''

    @jsii.member(jsii_name="fromCodeCommit")
    @builtins.classmethod
    def from_code_commit(
        cls,
        repository: _aws_cdk_aws_codecommit_692dd32c.IRepository,
        path: builtins.str,
    ) -> "CloneRepository":
        '''(experimental) import repository to cloud9 environment from AWS CodeCommit.

        :param repository: the codecommit repository to clone from.
        :param path: the target path in cloud9 environment.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__483a1f3243fb459efb95656bb9b5fc471788e4e5976dc317cc78dc8983cc3b93)
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


@jsii.enum(jsii_type="@aws-cdk/aws-cloud9.ConnectionType")
class ConnectionType(enum.Enum):
    '''(experimental) The connection type used for connecting to an Amazon EC2 environment.

    :stability: experimental
    '''

    CONNECT_SSH = "CONNECT_SSH"
    '''(experimental) Conect through SSH.

    :stability: experimental
    '''
    CONNECT_SSM = "CONNECT_SSM"
    '''(experimental) Connect through AWS Systems Manager.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloud9.Ec2EnvironmentProps",
    jsii_struct_bases=[],
    name_mapping={
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
        vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
        cloned_repositories: typing.Optional[typing.Sequence[CloneRepository]] = None,
        connection_type: typing.Optional[ConnectionType] = None,
        description: typing.Optional[builtins.str] = None,
        ec2_environment_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.InstanceType] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties for Ec2Environment.

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

            # create a cloud9 ec2 environment in a new VPC
            vpc = ec2.Vpc(self, "VPC", max_azs=3)
            cloud9.Ec2Environment(self, "Cloud9Env", vpc=vpc)
            
            # or create the cloud9 environment in the default VPC with specific instanceType
            default_vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)
            cloud9.Ec2Environment(self, "Cloud9Env2",
                vpc=default_vpc,
                instance_type=ec2.InstanceType("t3.large")
            )
            
            # or specify in a different subnetSelection
            c9env = cloud9.Ec2Environment(self, "Cloud9Env3",
                vpc=vpc,
                subnet_selection=ec2.SubnetSelection(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
                )
            )
            
            # print the Cloud9 IDE URL in the output
            CfnOutput(self, "URL", value=c9env.ide_url)
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_67de8e8d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03edf2a3832eda1f1e0f29061da4f3377d1e509902169bcdd15d440a645268b)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument cloned_repositories", value=cloned_repositories, expected_type=type_hints["cloned_repositories"])
            check_type(argname="argument connection_type", value=connection_type, expected_type=type_hints["connection_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument ec2_environment_name", value=ec2_environment_name, expected_type=type_hints["ec2_environment_name"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
    def vpc(self) -> _aws_cdk_aws_ec2_67de8e8d.IVpc:
        '''(experimental) The VPC that AWS Cloud9 will use to communicate with the Amazon Elastic Compute Cloud (Amazon EC2) instance.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_67de8e8d.IVpc, result)

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
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.InstanceType]:
        '''(experimental) The type of instance to connect to the environment.

        :default: - t2.micro

        :stability: experimental
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.InstanceType], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection]:
        '''(experimental) The subnetSelection of the VPC that AWS Cloud9 will use to communicate with the Amazon EC2 instance.

        :default: - all public subnets of the VPC are selected.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2EnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-cloud9.IEc2Environment")
class IEc2Environment(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
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
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''(experimental) A Cloud9 Environment.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cloud9.IEc2Environment"

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


@jsii.implements(IEc2Environment)
class Ec2Environment(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloud9.Ec2Environment",
):
    '''(experimental) A Cloud9 Environment with Amazon EC2.

    :stability: experimental
    :resource: AWS::Cloud9::EnvironmentEC2
    :exampleMetadata: infused

    Example::

        # create a cloud9 ec2 environment in a new VPC
        vpc = ec2.Vpc(self, "VPC", max_azs=3)
        cloud9.Ec2Environment(self, "Cloud9Env", vpc=vpc)
        
        # or create the cloud9 environment in the default VPC with specific instanceType
        default_vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)
        cloud9.Ec2Environment(self, "Cloud9Env2",
            vpc=default_vpc,
            instance_type=ec2.InstanceType("t3.large")
        )
        
        # or specify in a different subnetSelection
        c9env = cloud9.Ec2Environment(self, "Cloud9Env3",
            vpc=vpc,
            subnet_selection=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
            )
        )
        
        # print the Cloud9 IDE URL in the output
        CfnOutput(self, "URL", value=c9env.ide_url)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
        cloned_repositories: typing.Optional[typing.Sequence[CloneRepository]] = None,
        connection_type: typing.Optional[ConnectionType] = None,
        description: typing.Optional[builtins.str] = None,
        ec2_environment_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.InstanceType] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
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
            type_hints = typing.get_type_hints(_typecheckingstub__f27b9bc1933f9777b5adf61191c8d6dc90e2bc95f3e74b10141065c99796107c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = Ec2EnvironmentProps(
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
            type_hints = typing.get_type_hints(_typecheckingstub__11b50ad064b61920cd122a41272fcef73632116c65c26761f3751a269e4c0504)
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
    def vpc(self) -> _aws_cdk_aws_ec2_67de8e8d.IVpc:
        '''(experimental) VPC ID.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_67de8e8d.IVpc, jsii.get(self, "vpc"))


__all__ = [
    "CfnEnvironmentEC2",
    "CfnEnvironmentEC2Props",
    "CloneRepository",
    "ConnectionType",
    "Ec2Environment",
    "Ec2EnvironmentProps",
    "IEc2Environment",
]

publication.publish()

def _typecheckingstub__7ef001bf4de14efb43e2f14efb064bafe67bf100ece9581c3443b457e29c412d(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    instance_type: builtins.str,
    automatic_stop_time_minutes: typing.Optional[jsii.Number] = None,
    connection_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    image_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    owner_arn: typing.Optional[builtins.str] = None,
    repositories: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnEnvironmentEC2.RepositoryProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7f42337ef2529ba5ebec429c25e2db3649fee8e55e44712602de4ac9e41d2d(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f6f92dd2830861bf1bd59423ebfb32c8279709b743cdd6e14723ba3cfc63475(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee3b5ffb534e9db1b863f88e365316c39cf5af4ecba3abb686a8f2d3698dc31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bfacb916666563965d17d0d6b97cc3bd1f4960a91b8865a25f52898b3e0c083(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a8539e2d0dabd697b9787fd831ce368932946e7631809fb174a07fb2ff2d88(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17f0ad701068ea3f26386011592c6495cda01463205ee6833a91635a0bb8d20(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b727883922a845604ced8dfc1e9457b4e92f6ec4074ff651699afed670cdf3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a11fd8c6369ae96dba8413bab23048418689b507e734a18714e4f37d2be186f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1696f3784c2082c0a42062fd11bc8a4e1ae04790e629f13939aa8e8d3494de3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c2c1692b3309dae9ac320a2c92999f53ab1bc244bf04c509c2c2cc93cb78e9(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnEnvironmentEC2.RepositoryProperty, _aws_cdk_core_f4b25747.IResolvable]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37ab8081309b904e48eadc4d411e6e149b0e34b57934043c490b878e782edbdc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345d4f5e55d88315961d456d5b4e9e28e6cc5882d70b8f9f79eff8e139cae234(
    *,
    path_component: builtins.str,
    repository_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c82c4a8b3b96c7c641defd2e0263a0566263d37ff96b2b62ad4068f2f26b12(
    *,
    instance_type: builtins.str,
    automatic_stop_time_minutes: typing.Optional[jsii.Number] = None,
    connection_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    image_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    owner_arn: typing.Optional[builtins.str] = None,
    repositories: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnEnvironmentEC2.RepositoryProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__483a1f3243fb459efb95656bb9b5fc471788e4e5976dc317cc78dc8983cc3b93(
    repository: _aws_cdk_aws_codecommit_692dd32c.IRepository,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03edf2a3832eda1f1e0f29061da4f3377d1e509902169bcdd15d440a645268b(
    *,
    vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
    cloned_repositories: typing.Optional[typing.Sequence[CloneRepository]] = None,
    connection_type: typing.Optional[ConnectionType] = None,
    description: typing.Optional[builtins.str] = None,
    ec2_environment_name: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.InstanceType] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f27b9bc1933f9777b5adf61191c8d6dc90e2bc95f3e74b10141065c99796107c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
    cloned_repositories: typing.Optional[typing.Sequence[CloneRepository]] = None,
    connection_type: typing.Optional[ConnectionType] = None,
    description: typing.Optional[builtins.str] = None,
    ec2_environment_name: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.InstanceType] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b50ad064b61920cd122a41272fcef73632116c65c26761f3751a269e4c0504(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    ec2_environment_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
