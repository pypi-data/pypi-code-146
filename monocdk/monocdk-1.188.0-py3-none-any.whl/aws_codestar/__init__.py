'''
# AWS::CodeStar Construct Library

## GitHub Repository

To create a new GitHub Repository and commit the assets from S3 bucket into the repository after it is created:

```python
import monocdk as codestar
import monocdk as s3


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

from .._jsii import *

import constructs as _constructs_77d1e7e8
from .. import (
    CfnResource as _CfnResource_e0a482dc,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    Resource as _Resource_abff4495,
    SecretValue as _SecretValue_c18506ef,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_s3 import IBucket as _IBucket_73486e29


@jsii.implements(_IInspectable_82c04a63)
class CfnGitHubRepository(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codestar.CfnGitHubRepository",
):
    '''A CloudFormation ``AWS::CodeStar::GitHubRepository``.

    The ``AWS::CodeStar::GitHubRepository`` resource creates a GitHub repository where users can store source code for use with AWS workflows. You must provide a location for the source code ZIP file in the AWS CloudFormation template, so the code can be uploaded to the created repository. You must have created a personal access token in GitHub to provide in the AWS CloudFormation template. AWS uses this token to connect to GitHub on your behalf. For more information about using a GitHub source repository with AWS CodeStar projects, see `AWS CodeStar Project Files and Resources <https://docs.aws.amazon.com/codestar/latest/userguide/templates.html#templates-whatis>`_ .

    :cloudformationResource: AWS::CodeStar::GitHubRepository
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_codestar as codestar
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        repository_name: builtins.str,
        repository_owner: builtins.str,
        code: typing.Optional[typing.Union[typing.Union["CfnGitHubRepository.CodeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        connection_arn: typing.Optional[builtins.str] = None,
        enable_issues: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        is_private: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e6417a8cd803b26540e4b0aeb36c45a341ff26da7e791df675df50fb97584c4)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e316e6706e3d8c947158e9450f45c1c0ce5b1b7d89bbac929d3e37a79a874fc3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd458298fc1e20ba4a7ff1d912df53387d79a747e37d7a388fc8e490b1f7a8d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78ad89e3d016b25b56cffa283f881b0d0f6a6ac7e932d07e77309aa8bfab79ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e100b8474946ec04f4b7eee7ef43bf55a420a9bef06925b5b6caf56a5e3ff1d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryOwner", value)

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(
        self,
    ) -> typing.Optional[typing.Union["CfnGitHubRepository.CodeProperty", _IResolvable_a771d0ef]]:
        '''Information about code to be committed to a repository after it is created in an AWS CloudFormation stack.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-code
        '''
        return typing.cast(typing.Optional[typing.Union["CfnGitHubRepository.CodeProperty", _IResolvable_a771d0ef]], jsii.get(self, "code"))

    @code.setter
    def code(
        self,
        value: typing.Optional[typing.Union["CfnGitHubRepository.CodeProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06fdac87038483579345a9d6e16a8575f32eb023fd4accf654d2d02f77114e71)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0ba8394d7ea0b0c6071ce2aafef37306e47a68e53ea2cef4deeba55a7342f99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionArn", value)

    @builtins.property
    @jsii.member(jsii_name="enableIssues")
    def enable_issues(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Indicates whether to enable issues for the GitHub repository.

        You can use GitHub issues to track information and bugs for your repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-enableissues
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enableIssues"))

    @enable_issues.setter
    def enable_issues(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5402b5c800b0a50cb0141a0d17dd4219f94ff7e43b6c26a07a63b3c2e88bcdb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIssues", value)

    @builtins.property
    @jsii.member(jsii_name="isPrivate")
    def is_private(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Indicates whether the GitHub repository is a private repository.

        If so, you choose who can see and commit to this repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-isprivate
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "isPrivate"))

    @is_private.setter
    def is_private(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd7dbdce873af1a204d661071d9d24c0d4bf72acfbe3dba81f1c9736ad4016c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01d8678cd01273d281a5e55ee2af6acc9e50cc0f76c18cd129b895b27b681911)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f2170856c0701f4ac4b7480e4d4e6c71d349c174fbbd977f616360503a7e403)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryDescription", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_codestar.CfnGitHubRepository.CodeProperty",
        jsii_struct_bases=[],
        name_mapping={"s3": "s3"},
    )
    class CodeProperty:
        def __init__(
            self,
            *,
            s3: typing.Union[typing.Union["CfnGitHubRepository.S3Property", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''The ``Code`` property type specifies information about code to be committed.

            ``Code`` is a property of the ``AWS::CodeStar::GitHubRepository`` resource.

            :param s3: Information about the Amazon S3 bucket that contains a ZIP file of code to be committed to the repository.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-code.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_codestar as codestar
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__151b349c77f1a4f8ded96e7a22c46e35ac66f8e14e1da6dedbbed79e929b9805)
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3": s3,
            }

        @builtins.property
        def s3(
            self,
        ) -> typing.Union["CfnGitHubRepository.S3Property", _IResolvable_a771d0ef]:
            '''Information about the Amazon S3 bucket that contains a ZIP file of code to be committed to the repository.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-code.html#cfn-codestar-githubrepository-code-s3
            '''
            result = self._values.get("s3")
            assert result is not None, "Required property 's3' is missing"
            return typing.cast(typing.Union["CfnGitHubRepository.S3Property", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codestar.CfnGitHubRepository.S3Property",
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
                from monocdk import aws_codestar as codestar
                
                s3_property = codestar.CfnGitHubRepository.S3Property(
                    bucket="bucket",
                    key="key",
                
                    # the properties below are optional
                    object_version="objectVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__51e1fbe1a2a485214d39aeb1220ee489138a0d32cffa831dc40b075b935090d9)
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
    jsii_type="monocdk.aws_codestar.CfnGitHubRepositoryProps",
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
        code: typing.Optional[typing.Union[typing.Union[CfnGitHubRepository.CodeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        connection_arn: typing.Optional[builtins.str] = None,
        enable_issues: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        is_private: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
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
            from monocdk import aws_codestar as codestar
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__e87d67c3c5cc77f8471f3efaaa8ccca8c715c75e7b8da3a6f4de11fc3de05c5d)
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
    ) -> typing.Optional[typing.Union[CfnGitHubRepository.CodeProperty, _IResolvable_a771d0ef]]:
        '''Information about code to be committed to a repository after it is created in an AWS CloudFormation stack.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-code
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[typing.Union[CfnGitHubRepository.CodeProperty, _IResolvable_a771d0ef]], result)

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
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Indicates whether to enable issues for the GitHub repository.

        You can use GitHub issues to track information and bugs for your repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-enableissues
        '''
        result = self._values.get("enable_issues")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def is_private(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Indicates whether the GitHub repository is a private repository.

        If so, you choose who can see and commit to this repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-isprivate
        '''
        result = self._values.get("is_private")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

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
    jsii_type="monocdk.aws_codestar.GitHubRepositoryProps",
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
        access_token: _SecretValue_c18506ef,
        contents_bucket: _IBucket_73486e29,
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

            import monocdk as codestar
            import monocdk as s3
            
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2da2743ba4706217d329c539152fb16db4d9d4b2167a0eb5fba6ea9bee9d4e6)
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
    def access_token(self) -> _SecretValue_c18506ef:
        '''(experimental) The GitHub user's personal access token for the GitHub repository.

        :stability: experimental
        '''
        result = self._values.get("access_token")
        assert result is not None, "Required property 'access_token' is missing"
        return typing.cast(_SecretValue_c18506ef, result)

    @builtins.property
    def contents_bucket(self) -> _IBucket_73486e29:
        '''(experimental) The name of the Amazon S3 bucket that contains the ZIP file with the content to be committed to the new repository.

        :stability: experimental
        '''
        result = self._values.get("contents_bucket")
        assert result is not None, "Required property 'contents_bucket' is missing"
        return typing.cast(_IBucket_73486e29, result)

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


@jsii.interface(jsii_type="monocdk.aws_codestar.IGitHubRepository")
class IGitHubRepository(_IResource_8c1dbbbd, typing_extensions.Protocol):
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
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) GitHubRepository resource interface.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_codestar.IGitHubRepository"

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


@jsii.enum(jsii_type="monocdk.aws_codestar.RepositoryVisibility")
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
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codestar.GitHubRepository",
):
    '''(experimental) The GitHubRepository resource.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as codestar
        import monocdk as s3
        
        
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
        access_token: _SecretValue_c18506ef,
        contents_bucket: _IBucket_73486e29,
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ec831a56afa88faddd96488fe6165c0e0a638d756d5118859307b5cef1b35e6)
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

def _typecheckingstub__8e6417a8cd803b26540e4b0aeb36c45a341ff26da7e791df675df50fb97584c4(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    repository_name: builtins.str,
    repository_owner: builtins.str,
    code: typing.Optional[typing.Union[typing.Union[CfnGitHubRepository.CodeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    connection_arn: typing.Optional[builtins.str] = None,
    enable_issues: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    is_private: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    repository_access_token: typing.Optional[builtins.str] = None,
    repository_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e316e6706e3d8c947158e9450f45c1c0ce5b1b7d89bbac929d3e37a79a874fc3(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd458298fc1e20ba4a7ff1d912df53387d79a747e37d7a388fc8e490b1f7a8d0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ad89e3d016b25b56cffa283f881b0d0f6a6ac7e932d07e77309aa8bfab79ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e100b8474946ec04f4b7eee7ef43bf55a420a9bef06925b5b6caf56a5e3ff1d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06fdac87038483579345a9d6e16a8575f32eb023fd4accf654d2d02f77114e71(
    value: typing.Optional[typing.Union[CfnGitHubRepository.CodeProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ba8394d7ea0b0c6071ce2aafef37306e47a68e53ea2cef4deeba55a7342f99(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5402b5c800b0a50cb0141a0d17dd4219f94ff7e43b6c26a07a63b3c2e88bcdb7(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd7dbdce873af1a204d661071d9d24c0d4bf72acfbe3dba81f1c9736ad4016c(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01d8678cd01273d281a5e55ee2af6acc9e50cc0f76c18cd129b895b27b681911(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f2170856c0701f4ac4b7480e4d4e6c71d349c174fbbd977f616360503a7e403(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151b349c77f1a4f8ded96e7a22c46e35ac66f8e14e1da6dedbbed79e929b9805(
    *,
    s3: typing.Union[typing.Union[CfnGitHubRepository.S3Property, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e1fbe1a2a485214d39aeb1220ee489138a0d32cffa831dc40b075b935090d9(
    *,
    bucket: builtins.str,
    key: builtins.str,
    object_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87d67c3c5cc77f8471f3efaaa8ccca8c715c75e7b8da3a6f4de11fc3de05c5d(
    *,
    repository_name: builtins.str,
    repository_owner: builtins.str,
    code: typing.Optional[typing.Union[typing.Union[CfnGitHubRepository.CodeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    connection_arn: typing.Optional[builtins.str] = None,
    enable_issues: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    is_private: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    repository_access_token: typing.Optional[builtins.str] = None,
    repository_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2da2743ba4706217d329c539152fb16db4d9d4b2167a0eb5fba6ea9bee9d4e6(
    *,
    access_token: _SecretValue_c18506ef,
    contents_bucket: _IBucket_73486e29,
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

def _typecheckingstub__4ec831a56afa88faddd96488fe6165c0e0a638d756d5118859307b5cef1b35e6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_token: _SecretValue_c18506ef,
    contents_bucket: _IBucket_73486e29,
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
