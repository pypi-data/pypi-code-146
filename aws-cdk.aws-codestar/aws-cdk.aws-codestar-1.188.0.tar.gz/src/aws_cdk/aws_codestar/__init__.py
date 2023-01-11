'''
# AWS::CodeStar Construct Library

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

## GitHub Repository

To create a new GitHub Repository and commit the assets from S3 bucket into the repository after it is created:

```python
import aws_cdk.aws_codestar as codestar
import aws_cdk.aws_s3 as s3


codestar.GitHubRepository(self, "GitHubRepo",
    owner="aws",
    repository_name="aws-cdk",
    access_token=SecretValue.secrets_manager("my-github-token",
        json_field="token"
    ),
    contents_bucket=s3.Bucket.from_bucket_name(self, "Bucket", "bucket-name"),
    contents_key="import.zip"
)
```

## Update or Delete the GitHubRepository

At this moment, updates to the `GitHubRepository` are not supported and the repository will not be deleted upon the deletion of the CloudFormation stack. You will need to update or delete the GitHub repository manually.
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

import aws_cdk.aws_s3 as _aws_cdk_aws_s3_55f001a5
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnGitHubRepository(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codestar.CfnGitHubRepository",
):
    '''A CloudFormation ``AWS::CodeStar::GitHubRepository``.

    The ``AWS::CodeStar::GitHubRepository`` resource creates a GitHub repository where users can store source code for use with AWS workflows. You must provide a location for the source code ZIP file in the AWS CloudFormation template, so the code can be uploaded to the created repository. You must have created a personal access token in GitHub to provide in the AWS CloudFormation template. AWS uses this token to connect to GitHub on your behalf. For more information about using a GitHub source repository with AWS CodeStar projects, see `AWS CodeStar Project Files and Resources <https://docs.aws.amazon.com/codestar/latest/userguide/templates.html#templates-whatis>`_ .

    :cloudformationResource: AWS::CodeStar::GitHubRepository
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_codestar as codestar
        
        cfn_git_hub_repository = codestar.CfnGitHubRepository(self, "MyCfnGitHubRepository",
            repository_name="repositoryName",
            repository_owner="repositoryOwner",
        
            # the properties below are optional
            code=codestar.CfnGitHubRepository.CodeProperty(
                s3=codestar.CfnGitHubRepository.S3Property(
                    bucket="bucket",
                    key="key",
        
                    # the properties below are optional
                    object_version="objectVersion"
                )
            ),
            connection_arn="connectionArn",
            enable_issues=False,
            is_private=False,
            repository_access_token="repositoryAccessToken",
            repository_description="repositoryDescription"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        repository_name: builtins.str,
        repository_owner: builtins.str,
        code: typing.Optional[typing.Union[typing.Union["CfnGitHubRepository.CodeProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        connection_arn: typing.Optional[builtins.str] = None,
        enable_issues: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        is_private: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        repository_access_token: typing.Optional[builtins.str] = None,
        repository_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CodeStar::GitHubRepository``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param repository_name: The name of the repository you want to create in GitHub with AWS CloudFormation stack creation.
        :param repository_owner: The GitHub user name for the owner of the GitHub repository to be created. If this repository should be owned by a GitHub organization, provide its name.
        :param code: Information about code to be committed to a repository after it is created in an AWS CloudFormation stack.
        :param connection_arn: ``AWS::CodeStar::GitHubRepository.ConnectionArn``.
        :param enable_issues: Indicates whether to enable issues for the GitHub repository. You can use GitHub issues to track information and bugs for your repository.
        :param is_private: Indicates whether the GitHub repository is a private repository. If so, you choose who can see and commit to this repository.
        :param repository_access_token: The GitHub user's personal access token for the GitHub repository.
        :param repository_description: A comment or description about the new repository. This description is displayed in GitHub after the repository is created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26b449b083110032741dd9724b5a92f29982430d1e05f5d63333a3653c4f8337)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGitHubRepositoryProps(
            repository_name=repository_name,
            repository_owner=repository_owner,
            code=code,
            connection_arn=connection_arn,
            enable_issues=enable_issues,
            is_private=is_private,
            repository_access_token=repository_access_token,
            repository_description=repository_description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13b3396147e53963bba3ead51f99cee7f28e4f126567b00e1dd55d3798216b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f3d420fd6a36b825e10f4fac4dcffb885efe0365d1e5f228e4a1e42a9913b62)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''The name of the repository you want to create in GitHub with AWS CloudFormation stack creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositoryname
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))

    @repository_name.setter
    def repository_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ada9a998bd4e3b4cb453bfe71eada51be569d5dc78806fc083aba0cb0b5b64f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryName", value)

    @builtins.property
    @jsii.member(jsii_name="repositoryOwner")
    def repository_owner(self) -> builtins.str:
        '''The GitHub user name for the owner of the GitHub repository to be created.

        If this repository should be owned by a GitHub organization, provide its name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositoryowner
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryOwner"))

    @repository_owner.setter
    def repository_owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d47151ed8bc080b487c1a66685dc96d68e8fa4d20cf117b1c89ec62e65174d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryOwner", value)

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(
        self,
    ) -> typing.Optional[typing.Union["CfnGitHubRepository.CodeProperty", _aws_cdk_core_f4b25747.IResolvable]]:
        '''Information about code to be committed to a repository after it is created in an AWS CloudFormation stack.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-code
        '''
        return typing.cast(typing.Optional[typing.Union["CfnGitHubRepository.CodeProperty", _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "code"))

    @code.setter
    def code(
        self,
        value: typing.Optional[typing.Union["CfnGitHubRepository.CodeProperty", _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f57b1016b905ddaabee37dc4a1fd1e22614f03b2460d4c6c51c50c70870f649)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value)

    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::CodeStar::GitHubRepository.ConnectionArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-connectionarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionArn"))

    @connection_arn.setter
    def connection_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab0929e046b0f60f895dcb001e270b2545043f0d162061f32081b2e791b9ef7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionArn", value)

    @builtins.property
    @jsii.member(jsii_name="enableIssues")
    def enable_issues(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Indicates whether to enable issues for the GitHub repository.

        You can use GitHub issues to track information and bugs for your repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-enableissues
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "enableIssues"))

    @enable_issues.setter
    def enable_issues(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce611142bef4a35ed37ee8c0eada80912098229ee1cdfa028edba7cd851b880f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIssues", value)

    @builtins.property
    @jsii.member(jsii_name="isPrivate")
    def is_private(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Indicates whether the GitHub repository is a private repository.

        If so, you choose who can see and commit to this repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-isprivate
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "isPrivate"))

    @is_private.setter
    def is_private(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08f106dfae269a0beb48d95c12b83a85bf204b5bcffbe10d29496108b5b67f60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isPrivate", value)

    @builtins.property
    @jsii.member(jsii_name="repositoryAccessToken")
    def repository_access_token(self) -> typing.Optional[builtins.str]:
        '''The GitHub user's personal access token for the GitHub repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositoryaccesstoken
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryAccessToken"))

    @repository_access_token.setter
    def repository_access_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605cc24b62fe3c1bcd8f7997fbe99a6df9965c4f7638a5dd1d059f62b8c7bc71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryAccessToken", value)

    @builtins.property
    @jsii.member(jsii_name="repositoryDescription")
    def repository_description(self) -> typing.Optional[builtins.str]:
        '''A comment or description about the new repository.

        This description is displayed in GitHub after the repository is created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositorydescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryDescription"))

    @repository_description.setter
    def repository_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0058d63c67af46ad5ec90a867768b28bbe6f57c7675e279f79a16b3e8916894a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryDescription", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codestar.CfnGitHubRepository.CodeProperty",
        jsii_struct_bases=[],
        name_mapping={"s3": "s3"},
    )
    class CodeProperty:
        def __init__(
            self,
            *,
            s3: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnGitHubRepository.S3Property", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''The ``Code`` property type specifies information about code to be committed.

            ``Code`` is a property of the ``AWS::CodeStar::GitHubRepository`` resource.

            :param s3: Information about the Amazon S3 bucket that contains a ZIP file of code to be committed to the repository.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-code.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codestar as codestar
                
                code_property = codestar.CfnGitHubRepository.CodeProperty(
                    s3=codestar.CfnGitHubRepository.S3Property(
                        bucket="bucket",
                        key="key",
                
                        # the properties below are optional
                        object_version="objectVersion"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__754427423db91f6c6b2a4c327c3224c0335085b8310df22e5211ddb92251033a)
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3": s3,
            }

        @builtins.property
        def s3(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGitHubRepository.S3Property"]:
            '''Information about the Amazon S3 bucket that contains a ZIP file of code to be committed to the repository.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-code.html#cfn-codestar-githubrepository-code-s3
            '''
            result = self._values.get("s3")
            assert result is not None, "Required property 's3' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnGitHubRepository.S3Property"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-codestar.CfnGitHubRepository.S3Property",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "key": "key",
            "object_version": "objectVersion",
        },
    )
    class S3Property:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            object_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``S3`` property type specifies information about the Amazon S3 bucket that contains the code to be committed to the new repository.

            ``S3`` is a property of the ``AWS::CodeStar::GitHubRepository`` resource.

            :param bucket: The name of the Amazon S3 bucket that contains the ZIP file with the content to be committed to the new repository.
            :param key: The S3 object key or file name for the ZIP file.
            :param object_version: The object version of the ZIP file, if versioning is enabled for the Amazon S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-s3.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_codestar as codestar
                
                s3_property = codestar.CfnGitHubRepository.S3Property(
                    bucket="bucket",
                    key="key",
                
                    # the properties below are optional
                    object_version="objectVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a905417257973206e54dde52a31e3898c00041afc5a3e67292e8717f2681645)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument object_version", value=object_version, expected_type=type_hints["object_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket": bucket,
                "key": key,
            }
            if object_version is not None:
                self._values["object_version"] = object_version

        @builtins.property
        def bucket(self) -> builtins.str:
            '''The name of the Amazon S3 bucket that contains the ZIP file with the content to be committed to the new repository.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-s3.html#cfn-codestar-githubrepository-s3-bucket
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''The S3 object key or file name for the ZIP file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-s3.html#cfn-codestar-githubrepository-s3-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def object_version(self) -> typing.Optional[builtins.str]:
            '''The object version of the ZIP file, if versioning is enabled for the Amazon S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-s3.html#cfn-codestar-githubrepository-s3-objectversion
            '''
            result = self._values.get("object_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codestar.CfnGitHubRepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "repository_name": "repositoryName",
        "repository_owner": "repositoryOwner",
        "code": "code",
        "connection_arn": "connectionArn",
        "enable_issues": "enableIssues",
        "is_private": "isPrivate",
        "repository_access_token": "repositoryAccessToken",
        "repository_description": "repositoryDescription",
    },
)
class CfnGitHubRepositoryProps:
    def __init__(
        self,
        *,
        repository_name: builtins.str,
        repository_owner: builtins.str,
        code: typing.Optional[typing.Union[typing.Union[CfnGitHubRepository.CodeProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        connection_arn: typing.Optional[builtins.str] = None,
        enable_issues: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        is_private: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        repository_access_token: typing.Optional[builtins.str] = None,
        repository_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnGitHubRepository``.

        :param repository_name: The name of the repository you want to create in GitHub with AWS CloudFormation stack creation.
        :param repository_owner: The GitHub user name for the owner of the GitHub repository to be created. If this repository should be owned by a GitHub organization, provide its name.
        :param code: Information about code to be committed to a repository after it is created in an AWS CloudFormation stack.
        :param connection_arn: ``AWS::CodeStar::GitHubRepository.ConnectionArn``.
        :param enable_issues: Indicates whether to enable issues for the GitHub repository. You can use GitHub issues to track information and bugs for your repository.
        :param is_private: Indicates whether the GitHub repository is a private repository. If so, you choose who can see and commit to this repository.
        :param repository_access_token: The GitHub user's personal access token for the GitHub repository.
        :param repository_description: A comment or description about the new repository. This description is displayed in GitHub after the repository is created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_codestar as codestar
            
            cfn_git_hub_repository_props = codestar.CfnGitHubRepositoryProps(
                repository_name="repositoryName",
                repository_owner="repositoryOwner",
            
                # the properties below are optional
                code=codestar.CfnGitHubRepository.CodeProperty(
                    s3=codestar.CfnGitHubRepository.S3Property(
                        bucket="bucket",
                        key="key",
            
                        # the properties below are optional
                        object_version="objectVersion"
                    )
                ),
                connection_arn="connectionArn",
                enable_issues=False,
                is_private=False,
                repository_access_token="repositoryAccessToken",
                repository_description="repositoryDescription"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c0c844d2c5533a577aec08aecd7b53c8697af473dfa9d73c9870e56a110eb07)
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument repository_owner", value=repository_owner, expected_type=type_hints["repository_owner"])
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument connection_arn", value=connection_arn, expected_type=type_hints["connection_arn"])
            check_type(argname="argument enable_issues", value=enable_issues, expected_type=type_hints["enable_issues"])
            check_type(argname="argument is_private", value=is_private, expected_type=type_hints["is_private"])
            check_type(argname="argument repository_access_token", value=repository_access_token, expected_type=type_hints["repository_access_token"])
            check_type(argname="argument repository_description", value=repository_description, expected_type=type_hints["repository_description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_name": repository_name,
            "repository_owner": repository_owner,
        }
        if code is not None:
            self._values["code"] = code
        if connection_arn is not None:
            self._values["connection_arn"] = connection_arn
        if enable_issues is not None:
            self._values["enable_issues"] = enable_issues
        if is_private is not None:
            self._values["is_private"] = is_private
        if repository_access_token is not None:
            self._values["repository_access_token"] = repository_access_token
        if repository_description is not None:
            self._values["repository_description"] = repository_description

    @builtins.property
    def repository_name(self) -> builtins.str:
        '''The name of the repository you want to create in GitHub with AWS CloudFormation stack creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositoryname
        '''
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_owner(self) -> builtins.str:
        '''The GitHub user name for the owner of the GitHub repository to be created.

        If this repository should be owned by a GitHub organization, provide its name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositoryowner
        '''
        result = self._values.get("repository_owner")
        assert result is not None, "Required property 'repository_owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def code(
        self,
    ) -> typing.Optional[typing.Union[CfnGitHubRepository.CodeProperty, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Information about code to be committed to a repository after it is created in an AWS CloudFormation stack.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-code
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[typing.Union[CfnGitHubRepository.CodeProperty, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def connection_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::CodeStar::GitHubRepository.ConnectionArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-connectionarn
        '''
        result = self._values.get("connection_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_issues(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Indicates whether to enable issues for the GitHub repository.

        You can use GitHub issues to track information and bugs for your repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-enableissues
        '''
        result = self._values.get("enable_issues")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def is_private(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Indicates whether the GitHub repository is a private repository.

        If so, you choose who can see and commit to this repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-isprivate
        '''
        result = self._values.get("is_private")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def repository_access_token(self) -> typing.Optional[builtins.str]:
        '''The GitHub user's personal access token for the GitHub repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositoryaccesstoken
        '''
        result = self._values.get("repository_access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_description(self) -> typing.Optional[builtins.str]:
        '''A comment or description about the new repository.

        This description is displayed in GitHub after the repository is created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositorydescription
        '''
        result = self._values.get("repository_description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGitHubRepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-codestar.GitHubRepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_token": "accessToken",
        "contents_bucket": "contentsBucket",
        "contents_key": "contentsKey",
        "owner": "owner",
        "repository_name": "repositoryName",
        "contents_s3_version": "contentsS3Version",
        "description": "description",
        "enable_issues": "enableIssues",
        "visibility": "visibility",
    },
)
class GitHubRepositoryProps:
    def __init__(
        self,
        *,
        access_token: _aws_cdk_core_f4b25747.SecretValue,
        contents_bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
        contents_key: builtins.str,
        owner: builtins.str,
        repository_name: builtins.str,
        contents_s3_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_issues: typing.Optional[builtins.bool] = None,
        visibility: typing.Optional["RepositoryVisibility"] = None,
    ) -> None:
        '''(experimental) Construction properties of {@link GitHubRepository}.

        :param access_token: (experimental) The GitHub user's personal access token for the GitHub repository.
        :param contents_bucket: (experimental) The name of the Amazon S3 bucket that contains the ZIP file with the content to be committed to the new repository.
        :param contents_key: (experimental) The S3 object key or file name for the ZIP file.
        :param owner: (experimental) The GitHub user name for the owner of the GitHub repository to be created. If this repository should be owned by a GitHub organization, provide its name
        :param repository_name: (experimental) The name of the repository you want to create in GitHub with AWS CloudFormation stack creation.
        :param contents_s3_version: (experimental) The object version of the ZIP file, if versioning is enabled for the Amazon S3 bucket. Default: - not specified
        :param description: (experimental) A comment or description about the new repository. This description is displayed in GitHub after the repository is created. Default: - no description
        :param enable_issues: (experimental) Indicates whether to enable issues for the GitHub repository. You can use GitHub issues to track information and bugs for your repository. Default: true
        :param visibility: (experimental) Indicates whether the GitHub repository is a private repository. If so, you choose who can see and commit to this repository. Default: RepositoryVisibility.PUBLIC

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_codestar as codestar
            import aws_cdk.aws_s3 as s3
            
            
            codestar.GitHubRepository(self, "GitHubRepo",
                owner="aws",
                repository_name="aws-cdk",
                access_token=SecretValue.secrets_manager("my-github-token",
                    json_field="token"
                ),
                contents_bucket=s3.Bucket.from_bucket_name(self, "Bucket", "bucket-name"),
                contents_key="import.zip"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03e310e77b0f6f40e3bb812fd1bc49583ce56642771f3c54003c3697f2bc8c31)
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument contents_bucket", value=contents_bucket, expected_type=type_hints["contents_bucket"])
            check_type(argname="argument contents_key", value=contents_key, expected_type=type_hints["contents_key"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument contents_s3_version", value=contents_s3_version, expected_type=type_hints["contents_s3_version"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_issues", value=enable_issues, expected_type=type_hints["enable_issues"])
            check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_token": access_token,
            "contents_bucket": contents_bucket,
            "contents_key": contents_key,
            "owner": owner,
            "repository_name": repository_name,
        }
        if contents_s3_version is not None:
            self._values["contents_s3_version"] = contents_s3_version
        if description is not None:
            self._values["description"] = description
        if enable_issues is not None:
            self._values["enable_issues"] = enable_issues
        if visibility is not None:
            self._values["visibility"] = visibility

    @builtins.property
    def access_token(self) -> _aws_cdk_core_f4b25747.SecretValue:
        '''(experimental) The GitHub user's personal access token for the GitHub repository.

        :stability: experimental
        '''
        result = self._values.get("access_token")
        assert result is not None, "Required property 'access_token' is missing"
        return typing.cast(_aws_cdk_core_f4b25747.SecretValue, result)

    @builtins.property
    def contents_bucket(self) -> _aws_cdk_aws_s3_55f001a5.IBucket:
        '''(experimental) The name of the Amazon S3 bucket that contains the ZIP file with the content to be committed to the new repository.

        :stability: experimental
        '''
        result = self._values.get("contents_bucket")
        assert result is not None, "Required property 'contents_bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_55f001a5.IBucket, result)

    @builtins.property
    def contents_key(self) -> builtins.str:
        '''(experimental) The S3 object key or file name for the ZIP file.

        :stability: experimental
        '''
        result = self._values.get("contents_key")
        assert result is not None, "Required property 'contents_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def owner(self) -> builtins.str:
        '''(experimental) The GitHub user name for the owner of the GitHub repository to be created.

        If this
        repository should be owned by a GitHub organization, provide its name

        :stability: experimental
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_name(self) -> builtins.str:
        '''(experimental) The name of the repository you want to create in GitHub with AWS CloudFormation stack creation.

        :stability: experimental
        '''
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def contents_s3_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The object version of the ZIP file, if versioning is enabled for the Amazon S3 bucket.

        :default: - not specified

        :stability: experimental
        '''
        result = self._values.get("contents_s3_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A comment or description about the new repository.

        This description is displayed in GitHub after the repository
        is created.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_issues(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether to enable issues for the GitHub repository.

        You can use GitHub issues to track information
        and bugs for your repository.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enable_issues")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def visibility(self) -> typing.Optional["RepositoryVisibility"]:
        '''(experimental) Indicates whether the GitHub repository is a private repository.

        If so, you choose who can see and commit to
        this repository.

        :default: RepositoryVisibility.PUBLIC

        :stability: experimental
        '''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional["RepositoryVisibility"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubRepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-codestar.IGitHubRepository")
class IGitHubRepository(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''(experimental) GitHubRepository resource interface.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        '''(experimental) the repository owner.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="repo")
    def repo(self) -> builtins.str:
        '''(experimental) the repository name.

        :stability: experimental
        '''
        ...


class _IGitHubRepositoryProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''(experimental) GitHubRepository resource interface.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-codestar.IGitHubRepository"

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        '''(experimental) the repository owner.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="repo")
    def repo(self) -> builtins.str:
        '''(experimental) the repository name.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "repo"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGitHubRepository).__jsii_proxy_class__ = lambda : _IGitHubRepositoryProxy


@jsii.enum(jsii_type="@aws-cdk/aws-codestar.RepositoryVisibility")
class RepositoryVisibility(enum.Enum):
    '''(experimental) Visibility of the GitHubRepository.

    :stability: experimental
    '''

    PRIVATE = "PRIVATE"
    '''(experimental) private repository.

    :stability: experimental
    '''
    PUBLIC = "PUBLIC"
    '''(experimental) public repository.

    :stability: experimental
    '''


@jsii.implements(IGitHubRepository)
class GitHubRepository(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-codestar.GitHubRepository",
):
    '''(experimental) The GitHubRepository resource.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_codestar as codestar
        import aws_cdk.aws_s3 as s3
        
        
        codestar.GitHubRepository(self, "GitHubRepo",
            owner="aws",
            repository_name="aws-cdk",
            access_token=SecretValue.secrets_manager("my-github-token",
                json_field="token"
            ),
            contents_bucket=s3.Bucket.from_bucket_name(self, "Bucket", "bucket-name"),
            contents_key="import.zip"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_token: _aws_cdk_core_f4b25747.SecretValue,
        contents_bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
        contents_key: builtins.str,
        owner: builtins.str,
        repository_name: builtins.str,
        contents_s3_version: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_issues: typing.Optional[builtins.bool] = None,
        visibility: typing.Optional[RepositoryVisibility] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param access_token: (experimental) The GitHub user's personal access token for the GitHub repository.
        :param contents_bucket: (experimental) The name of the Amazon S3 bucket that contains the ZIP file with the content to be committed to the new repository.
        :param contents_key: (experimental) The S3 object key or file name for the ZIP file.
        :param owner: (experimental) The GitHub user name for the owner of the GitHub repository to be created. If this repository should be owned by a GitHub organization, provide its name
        :param repository_name: (experimental) The name of the repository you want to create in GitHub with AWS CloudFormation stack creation.
        :param contents_s3_version: (experimental) The object version of the ZIP file, if versioning is enabled for the Amazon S3 bucket. Default: - not specified
        :param description: (experimental) A comment or description about the new repository. This description is displayed in GitHub after the repository is created. Default: - no description
        :param enable_issues: (experimental) Indicates whether to enable issues for the GitHub repository. You can use GitHub issues to track information and bugs for your repository. Default: true
        :param visibility: (experimental) Indicates whether the GitHub repository is a private repository. If so, you choose who can see and commit to this repository. Default: RepositoryVisibility.PUBLIC

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e7ea239c3efeec10dca809e128e7979d3913c4069c413a241f37c7523ce9c1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubRepositoryProps(
            access_token=access_token,
            contents_bucket=contents_bucket,
            contents_key=contents_key,
            owner=owner,
            repository_name=repository_name,
            contents_s3_version=contents_s3_version,
            description=description,
            enable_issues=enable_issues,
            visibility=visibility,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        '''(experimental) the repository owner.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="repo")
    def repo(self) -> builtins.str:
        '''(experimental) the repository name.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "repo"))


__all__ = [
    "CfnGitHubRepository",
    "CfnGitHubRepositoryProps",
    "GitHubRepository",
    "GitHubRepositoryProps",
    "IGitHubRepository",
    "RepositoryVisibility",
]

publication.publish()

def _typecheckingstub__26b449b083110032741dd9724b5a92f29982430d1e05f5d63333a3653c4f8337(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    repository_name: builtins.str,
    repository_owner: builtins.str,
    code: typing.Optional[typing.Union[typing.Union[CfnGitHubRepository.CodeProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    connection_arn: typing.Optional[builtins.str] = None,
    enable_issues: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    is_private: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    repository_access_token: typing.Optional[builtins.str] = None,
    repository_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13b3396147e53963bba3ead51f99cee7f28e4f126567b00e1dd55d3798216b8(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3d420fd6a36b825e10f4fac4dcffb885efe0365d1e5f228e4a1e42a9913b62(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada9a998bd4e3b4cb453bfe71eada51be569d5dc78806fc083aba0cb0b5b64f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d47151ed8bc080b487c1a66685dc96d68e8fa4d20cf117b1c89ec62e65174d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f57b1016b905ddaabee37dc4a1fd1e22614f03b2460d4c6c51c50c70870f649(
    value: typing.Optional[typing.Union[CfnGitHubRepository.CodeProperty, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab0929e046b0f60f895dcb001e270b2545043f0d162061f32081b2e791b9ef7d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce611142bef4a35ed37ee8c0eada80912098229ee1cdfa028edba7cd851b880f(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08f106dfae269a0beb48d95c12b83a85bf204b5bcffbe10d29496108b5b67f60(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605cc24b62fe3c1bcd8f7997fbe99a6df9965c4f7638a5dd1d059f62b8c7bc71(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0058d63c67af46ad5ec90a867768b28bbe6f57c7675e279f79a16b3e8916894a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754427423db91f6c6b2a4c327c3224c0335085b8310df22e5211ddb92251033a(
    *,
    s3: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnGitHubRepository.S3Property, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a905417257973206e54dde52a31e3898c00041afc5a3e67292e8717f2681645(
    *,
    bucket: builtins.str,
    key: builtins.str,
    object_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0c844d2c5533a577aec08aecd7b53c8697af473dfa9d73c9870e56a110eb07(
    *,
    repository_name: builtins.str,
    repository_owner: builtins.str,
    code: typing.Optional[typing.Union[typing.Union[CfnGitHubRepository.CodeProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    connection_arn: typing.Optional[builtins.str] = None,
    enable_issues: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    is_private: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    repository_access_token: typing.Optional[builtins.str] = None,
    repository_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e310e77b0f6f40e3bb812fd1bc49583ce56642771f3c54003c3697f2bc8c31(
    *,
    access_token: _aws_cdk_core_f4b25747.SecretValue,
    contents_bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
    contents_key: builtins.str,
    owner: builtins.str,
    repository_name: builtins.str,
    contents_s3_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_issues: typing.Optional[builtins.bool] = None,
    visibility: typing.Optional[RepositoryVisibility] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e7ea239c3efeec10dca809e128e7979d3913c4069c413a241f37c7523ce9c1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_token: _aws_cdk_core_f4b25747.SecretValue,
    contents_bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
    contents_key: builtins.str,
    owner: builtins.str,
    repository_name: builtins.str,
    contents_s3_version: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_issues: typing.Optional[builtins.bool] = None,
    visibility: typing.Optional[RepositoryVisibility] = None,
) -> None:
    """Type checking stubs"""
    pass
