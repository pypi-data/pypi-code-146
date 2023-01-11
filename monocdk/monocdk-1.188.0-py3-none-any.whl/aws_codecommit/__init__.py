'''
# AWS CodeCommit Construct Library

AWS CodeCommit is a version control service that enables you to privately store and manage Git repositories in the AWS cloud.

For further information on CodeCommit,
see the [AWS CodeCommit documentation](https://docs.aws.amazon.com/codecommit).

To add a CodeCommit Repository to your stack:

```python
repo = codecommit.Repository(self, "Repository",
    repository_name="MyRepositoryName",
    description="Some description."
)
```

Use the `repositoryCloneUrlHttp`, `repositoryCloneUrlSsh` or `repositoryCloneUrlGrc`
property to clone your repository.

To add an Amazon SNS trigger to your repository:

```python
# repo: codecommit.Repository


# trigger is established for all repository actions on all branches by default.
repo.notify("arn:aws:sns:*:123456789012:my_topic")
```

## Add initial commit

It is possible to initialize the Repository via the `Code` class.
It provides methods for loading code from a directory, `.zip` file and from a pre-created CDK Asset.

Example:

```python
repo = codecommit.Repository(self, "Repository",
    repository_name="MyRepositoryName",
    code=codecommit.Code.from_directory(path.join(__dirname, "directory/"), "develop")
)
```

## Events

CodeCommit repositories emit Amazon CloudWatch events for certain activities.
Use the `repo.onXxx` methods to define rules that trigger on these events
and invoke targets as a result:

```python
import monocdk as sns
import monocdk as targets

# repo: codecommit.Repository
# project: codebuild.PipelineProject
# my_topic: sns.Topic


# starts a CodeBuild project when a commit is pushed to the "master" branch of the repo
repo.on_commit("CommitToMaster",
    target=targets.CodeBuildProject(project),
    branches=["master"]
)

# publishes a message to an Amazon SNS topic when a comment is made on a pull request
rule = repo.on_comment_on_pull_request("CommentOnPullRequest",
    target=targets.SnsTopic(my_topic)
)
```

## CodeStar Notifications

To define CodeStar Notification rules for Repositories, use one of the `notifyOnXxx()` methods.
They are very similar to `onXxx()` methods for CloudWatch events:

```python
import monocdk as chatbot

# repository: codecommit.Repository

target = chatbot.SlackChannelConfiguration(self, "MySlackChannel",
    slack_channel_configuration_name="YOUR_CHANNEL_NAME",
    slack_workspace_id="YOUR_SLACK_WORKSPACE_ID",
    slack_channel_id="YOUR_SLACK_CHANNEL_ID"
)
rule = repository.notify_on_pull_request_created("NotifyOnPullRequestCreated", target)
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

from .._jsii import *

import constructs as _constructs_77d1e7e8
from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    Resource as _Resource_abff4495,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_codestarnotifications import (
    DetailType as _DetailType_50204ab4,
    INotificationRule as _INotificationRule_e22254bb,
    INotificationRuleSource as _INotificationRuleSource_904910c7,
    INotificationRuleTarget as _INotificationRuleTarget_31f512df,
    NotificationRuleOptions as _NotificationRuleOptions_8645c987,
    NotificationRuleSourceConfig as _NotificationRuleSourceConfig_fd02300e,
)
from ..aws_events import (
    EventPattern as _EventPattern_a23fbf37,
    IRuleTarget as _IRuleTarget_d45ec729,
    OnEventOptions as _OnEventOptions_d5081088,
    Rule as _Rule_6cfff189,
)
from ..aws_iam import Grant as _Grant_bcb5eae7, IGrantable as _IGrantable_4c5a91d1
from ..aws_s3_assets import Asset as _Asset_d07e8c00


@jsii.implements(_IInspectable_82c04a63)
class CfnRepository(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codecommit.CfnRepository",
):
    '''A CloudFormation ``AWS::CodeCommit::Repository``.

    Creates a new, empty repository.

    :cloudformationResource: AWS::CodeCommit::Repository
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_codecommit as codecommit
        
        cfn_repository = codecommit.CfnRepository(self, "MyCfnRepository",
            repository_name="repositoryName",
        
            # the properties below are optional
            code=codecommit.CfnRepository.CodeProperty(
                s3=codecommit.CfnRepository.S3Property(
                    bucket="bucket",
                    key="key",
        
                    # the properties below are optional
                    object_version="objectVersion"
                ),
        
                # the properties below are optional
                branch_name="branchName"
            ),
            repository_description="repositoryDescription",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            triggers=[codecommit.CfnRepository.RepositoryTriggerProperty(
                destination_arn="destinationArn",
                events=["events"],
                name="name",
        
                # the properties below are optional
                branches=["branches"],
                custom_data="customData"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        repository_name: builtins.str,
        code: typing.Optional[typing.Union[typing.Union["CfnRepository.CodeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        repository_description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        triggers: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRepository.RepositoryTriggerProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        '''Create a new ``AWS::CodeCommit::Repository``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param repository_name: The name of the new repository to be created. .. epigraph:: The repository name must be unique across the calling AWS account . Repository names are limited to 100 alphanumeric, dash, and underscore characters, and cannot include certain characters. For more information about the limits on repository names, see `Quotas <https://docs.aws.amazon.com/codecommit/latest/userguide/limits.html>`_ in the *AWS CodeCommit User Guide* . The suffix .git is prohibited.
        :param code: Information about code to be committed to a repository after it is created in an AWS CloudFormation stack. Information about code is only used in resource creation. Updates to a stack will not reflect changes made to code properties after initial resource creation. .. epigraph:: You can only use this property to add code when creating a repository with a AWS CloudFormation template at creation time. This property cannot be used for updating code to an existing repository.
        :param repository_description: A comment or description about the new repository. .. epigraph:: The description field for a repository accepts all HTML characters and all valid Unicode characters. Applications that do not HTML-encode the description and display it in a webpage can expose users to potentially malicious code. Make sure that you HTML-encode the description field in any application that uses this API to display the repository description on a webpage.
        :param tags: One or more tag key-value pairs to use when tagging this repository.
        :param triggers: The JSON block of configuration information for each trigger.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138c763af5bf3552be2c0297711208a0a9ddb27d3d6d8d783bdc84b0279008e8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRepositoryProps(
            repository_name=repository_name,
            code=code,
            repository_description=repository_description,
            tags=tags,
            triggers=triggers,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c3c9a38e189e8c10098c38ad2d36fb65dc5bdb08345a8ff330cd8defd15dc9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a95098a5b5d23ad477d7ad15ec7a5ffe3b4a01ce45fd707fcfee84a932a13ee)
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
        '''When you pass the logical ID of this resource, the function returns the Amazon Resource Name (ARN) of the repository.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCloneUrlHttp")
    def attr_clone_url_http(self) -> builtins.str:
        '''When you pass the logical ID of this resource, the function returns the URL to use for cloning the repository over HTTPS.

        :cloudformationAttribute: CloneUrlHttp
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCloneUrlHttp"))

    @builtins.property
    @jsii.member(jsii_name="attrCloneUrlSsh")
    def attr_clone_url_ssh(self) -> builtins.str:
        '''When you pass the logical ID of this resource, the function returns the URL to use for cloning the repository over SSH.

        :cloudformationAttribute: CloneUrlSsh
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCloneUrlSsh"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''When you pass the logical ID of this resource, the function returns the repository's name.

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''One or more tag key-value pairs to use when tagging this repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''The name of the new repository to be created.

        .. epigraph::

           The repository name must be unique across the calling AWS account . Repository names are limited to 100 alphanumeric, dash, and underscore characters, and cannot include certain characters. For more information about the limits on repository names, see `Quotas <https://docs.aws.amazon.com/codecommit/latest/userguide/limits.html>`_ in the *AWS CodeCommit User Guide* . The suffix .git is prohibited.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-repositoryname
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))

    @repository_name.setter
    def repository_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e4c8ce166d7b0de46a08c034bd1a7afcd09961e177f6ef3b9842cafb236d4c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryName", value)

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(
        self,
    ) -> typing.Optional[typing.Union["CfnRepository.CodeProperty", _IResolvable_a771d0ef]]:
        '''Information about code to be committed to a repository after it is created in an AWS CloudFormation stack.

        Information about code is only used in resource creation. Updates to a stack will not reflect changes made to code properties after initial resource creation.
        .. epigraph::

           You can only use this property to add code when creating a repository with a AWS CloudFormation template at creation time. This property cannot be used for updating code to an existing repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-code
        '''
        return typing.cast(typing.Optional[typing.Union["CfnRepository.CodeProperty", _IResolvable_a771d0ef]], jsii.get(self, "code"))

    @code.setter
    def code(
        self,
        value: typing.Optional[typing.Union["CfnRepository.CodeProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c17f1618c777f7ca79020f0e1664d223f03aaba7a9cbe234043479387ec0339)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "code", value)

    @builtins.property
    @jsii.member(jsii_name="repositoryDescription")
    def repository_description(self) -> typing.Optional[builtins.str]:
        '''A comment or description about the new repository.

        .. epigraph::

           The description field for a repository accepts all HTML characters and all valid Unicode characters. Applications that do not HTML-encode the description and display it in a webpage can expose users to potentially malicious code. Make sure that you HTML-encode the description field in any application that uses this API to display the repository description on a webpage.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-repositorydescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryDescription"))

    @repository_description.setter
    def repository_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2222af807d41424f5860b1e1192ad08c137070db39e28a29a22c482b5f4dc2f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryDescription", value)

    @builtins.property
    @jsii.member(jsii_name="triggers")
    def triggers(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRepository.RepositoryTriggerProperty", _IResolvable_a771d0ef]]]]:
        '''The JSON block of configuration information for each trigger.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-triggers
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRepository.RepositoryTriggerProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "triggers"))

    @triggers.setter
    def triggers(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRepository.RepositoryTriggerProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f147d495a9ff1902010a9c6541609faacc556a8e5b5d73a01e0e820a2d8194fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggers", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_codecommit.CfnRepository.CodeProperty",
        jsii_struct_bases=[],
        name_mapping={"s3": "s3", "branch_name": "branchName"},
    )
    class CodeProperty:
        def __init__(
            self,
            *,
            s3: typing.Union[typing.Union["CfnRepository.S3Property", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            branch_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about code to be committed.

            :param s3: Information about the Amazon S3 bucket that contains a ZIP file of code to be committed to the repository. Changes to this property are ignored after initial resource creation.
            :param branch_name: Optional. Specifies a branch name to be used as the default branch when importing code into a repository on initial creation. If this property is not set, the name *main* will be used for the default branch for the repository. Changes to this property are ignored after initial resource creation. We recommend using this parameter to set the name to *main* to align with the default behavior of CodeCommit unless another name is needed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-code.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_codecommit as codecommit
                
                code_property = codecommit.CfnRepository.CodeProperty(
                    s3=codecommit.CfnRepository.S3Property(
                        bucket="bucket",
                        key="key",
                
                        # the properties below are optional
                        object_version="objectVersion"
                    ),
                
                    # the properties below are optional
                    branch_name="branchName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__732dcde002b52900cf0f056286147721c52681c4d24374e8a2ae9f8a7f6a1ed1)
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
                check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3": s3,
            }
            if branch_name is not None:
                self._values["branch_name"] = branch_name

        @builtins.property
        def s3(self) -> typing.Union["CfnRepository.S3Property", _IResolvable_a771d0ef]:
            '''Information about the Amazon S3 bucket that contains a ZIP file of code to be committed to the repository.

            Changes to this property are ignored after initial resource creation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-code.html#cfn-codecommit-repository-code-s3
            '''
            result = self._values.get("s3")
            assert result is not None, "Required property 's3' is missing"
            return typing.cast(typing.Union["CfnRepository.S3Property", _IResolvable_a771d0ef], result)

        @builtins.property
        def branch_name(self) -> typing.Optional[builtins.str]:
            '''Optional.

            Specifies a branch name to be used as the default branch when importing code into a repository on initial creation. If this property is not set, the name *main* will be used for the default branch for the repository. Changes to this property are ignored after initial resource creation. We recommend using this parameter to set the name to *main* to align with the default behavior of CodeCommit unless another name is needed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-code.html#cfn-codecommit-repository-code-branchname
            '''
            result = self._values.get("branch_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codecommit.CfnRepository.RepositoryTriggerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_arn": "destinationArn",
            "events": "events",
            "name": "name",
            "branches": "branches",
            "custom_data": "customData",
        },
    )
    class RepositoryTriggerProperty:
        def __init__(
            self,
            *,
            destination_arn: builtins.str,
            events: typing.Sequence[builtins.str],
            name: builtins.str,
            branches: typing.Optional[typing.Sequence[builtins.str]] = None,
            custom_data: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about a trigger for a repository.

            .. epigraph::

               If you want to receive notifications about repository events, consider using notifications instead of triggers. For more information, see `Configuring notifications for repository events <https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-repository-email.html>`_ .

            :param destination_arn: The ARN of the resource that is the target for a trigger (for example, the ARN of a topic in Amazon SNS).
            :param events: The repository events that cause the trigger to run actions in another service, such as sending a notification through Amazon SNS. .. epigraph:: The valid value "all" cannot be used with any other values.
            :param name: The name of the trigger.
            :param branches: The branches to be included in the trigger configuration. If you specify an empty array, the trigger applies to all branches. .. epigraph:: Although no content is required in the array, you must include the array itself.
            :param custom_data: Any custom data associated with the trigger to be included in the information sent to the target of the trigger.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_codecommit as codecommit
                
                repository_trigger_property = codecommit.CfnRepository.RepositoryTriggerProperty(
                    destination_arn="destinationArn",
                    events=["events"],
                    name="name",
                
                    # the properties below are optional
                    branches=["branches"],
                    custom_data="customData"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d5e411564b8ff3f43f467c50e6abecb164f56e11e313eb292bf5ee90aa2a4267)
                check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
                check_type(argname="argument custom_data", value=custom_data, expected_type=type_hints["custom_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destination_arn": destination_arn,
                "events": events,
                "name": name,
            }
            if branches is not None:
                self._values["branches"] = branches
            if custom_data is not None:
                self._values["custom_data"] = custom_data

        @builtins.property
        def destination_arn(self) -> builtins.str:
            '''The ARN of the resource that is the target for a trigger (for example, the ARN of a topic in Amazon SNS).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-destinationarn
            '''
            result = self._values.get("destination_arn")
            assert result is not None, "Required property 'destination_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def events(self) -> typing.List[builtins.str]:
            '''The repository events that cause the trigger to run actions in another service, such as sending a notification through Amazon SNS.

            .. epigraph::

               The valid value "all" cannot be used with any other values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-events
            '''
            result = self._values.get("events")
            assert result is not None, "Required property 'events' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the trigger.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def branches(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The branches to be included in the trigger configuration.

            If you specify an empty array, the trigger applies to all branches.
            .. epigraph::

               Although no content is required in the array, you must include the array itself.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-branches
            '''
            result = self._values.get("branches")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def custom_data(self) -> typing.Optional[builtins.str]:
            '''Any custom data associated with the trigger to be included in the information sent to the target of the trigger.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-customdata
            '''
            result = self._values.get("custom_data")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RepositoryTriggerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codecommit.CfnRepository.S3Property",
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
            '''Information about the Amazon S3 bucket that contains the code that will be committed to the new repository.

            Changes to this property are ignored after initial resource creation.

            :param bucket: The name of the Amazon S3 bucket that contains the ZIP file with the content that will be committed to the new repository. This can be specified using the name of the bucket in the AWS account . Changes to this property are ignored after initial resource creation.
            :param key: The key to use for accessing the Amazon S3 bucket. Changes to this property are ignored after initial resource creation. For more information, see `Creating object key names <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html>`_ and `Uploading objects <https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html>`_ in the Amazon S3 User Guide.
            :param object_version: The object version of the ZIP file, if versioning is enabled for the Amazon S3 bucket. Changes to this property are ignored after initial resource creation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-s3.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_codecommit as codecommit
                
                s3_property = codecommit.CfnRepository.S3Property(
                    bucket="bucket",
                    key="key",
                
                    # the properties below are optional
                    object_version="objectVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__67ea2cd814e721c8483c10d9b6229d225311fa63b482e4cd1837e981a5371565)
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
            '''The name of the Amazon S3 bucket that contains the ZIP file with the content that will be committed to the new repository.

            This can be specified using the name of the bucket in the AWS account . Changes to this property are ignored after initial resource creation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-s3.html#cfn-codecommit-repository-s3-bucket
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''The key to use for accessing the Amazon S3 bucket.

            Changes to this property are ignored after initial resource creation. For more information, see `Creating object key names <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html>`_ and `Uploading objects <https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html>`_ in the Amazon S3 User Guide.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-s3.html#cfn-codecommit-repository-s3-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def object_version(self) -> typing.Optional[builtins.str]:
            '''The object version of the ZIP file, if versioning is enabled for the Amazon S3 bucket.

            Changes to this property are ignored after initial resource creation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-s3.html#cfn-codecommit-repository-s3-objectversion
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
    jsii_type="monocdk.aws_codecommit.CfnRepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "repository_name": "repositoryName",
        "code": "code",
        "repository_description": "repositoryDescription",
        "tags": "tags",
        "triggers": "triggers",
    },
)
class CfnRepositoryProps:
    def __init__(
        self,
        *,
        repository_name: builtins.str,
        code: typing.Optional[typing.Union[typing.Union[CfnRepository.CodeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        repository_description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        triggers: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRepository.RepositoryTriggerProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRepository``.

        :param repository_name: The name of the new repository to be created. .. epigraph:: The repository name must be unique across the calling AWS account . Repository names are limited to 100 alphanumeric, dash, and underscore characters, and cannot include certain characters. For more information about the limits on repository names, see `Quotas <https://docs.aws.amazon.com/codecommit/latest/userguide/limits.html>`_ in the *AWS CodeCommit User Guide* . The suffix .git is prohibited.
        :param code: Information about code to be committed to a repository after it is created in an AWS CloudFormation stack. Information about code is only used in resource creation. Updates to a stack will not reflect changes made to code properties after initial resource creation. .. epigraph:: You can only use this property to add code when creating a repository with a AWS CloudFormation template at creation time. This property cannot be used for updating code to an existing repository.
        :param repository_description: A comment or description about the new repository. .. epigraph:: The description field for a repository accepts all HTML characters and all valid Unicode characters. Applications that do not HTML-encode the description and display it in a webpage can expose users to potentially malicious code. Make sure that you HTML-encode the description field in any application that uses this API to display the repository description on a webpage.
        :param tags: One or more tag key-value pairs to use when tagging this repository.
        :param triggers: The JSON block of configuration information for each trigger.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codecommit as codecommit
            
            cfn_repository_props = codecommit.CfnRepositoryProps(
                repository_name="repositoryName",
            
                # the properties below are optional
                code=codecommit.CfnRepository.CodeProperty(
                    s3=codecommit.CfnRepository.S3Property(
                        bucket="bucket",
                        key="key",
            
                        # the properties below are optional
                        object_version="objectVersion"
                    ),
            
                    # the properties below are optional
                    branch_name="branchName"
                ),
                repository_description="repositoryDescription",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                triggers=[codecommit.CfnRepository.RepositoryTriggerProperty(
                    destination_arn="destinationArn",
                    events=["events"],
                    name="name",
            
                    # the properties below are optional
                    branches=["branches"],
                    custom_data="customData"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d721eea3db77201398649ea6b8db802a256f00e901998fa1855041c1a16fb4)
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument repository_description", value=repository_description, expected_type=type_hints["repository_description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument triggers", value=triggers, expected_type=type_hints["triggers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_name": repository_name,
        }
        if code is not None:
            self._values["code"] = code
        if repository_description is not None:
            self._values["repository_description"] = repository_description
        if tags is not None:
            self._values["tags"] = tags
        if triggers is not None:
            self._values["triggers"] = triggers

    @builtins.property
    def repository_name(self) -> builtins.str:
        '''The name of the new repository to be created.

        .. epigraph::

           The repository name must be unique across the calling AWS account . Repository names are limited to 100 alphanumeric, dash, and underscore characters, and cannot include certain characters. For more information about the limits on repository names, see `Quotas <https://docs.aws.amazon.com/codecommit/latest/userguide/limits.html>`_ in the *AWS CodeCommit User Guide* . The suffix .git is prohibited.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-repositoryname
        '''
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def code(
        self,
    ) -> typing.Optional[typing.Union[CfnRepository.CodeProperty, _IResolvable_a771d0ef]]:
        '''Information about code to be committed to a repository after it is created in an AWS CloudFormation stack.

        Information about code is only used in resource creation. Updates to a stack will not reflect changes made to code properties after initial resource creation.
        .. epigraph::

           You can only use this property to add code when creating a repository with a AWS CloudFormation template at creation time. This property cannot be used for updating code to an existing repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-code
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[typing.Union[CfnRepository.CodeProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def repository_description(self) -> typing.Optional[builtins.str]:
        '''A comment or description about the new repository.

        .. epigraph::

           The description field for a repository accepts all HTML characters and all valid Unicode characters. Applications that do not HTML-encode the description and display it in a webpage can expose users to potentially malicious code. Make sure that you HTML-encode the description field in any application that uses this API to display the repository description on a webpage.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-repositorydescription
        '''
        result = self._values.get("repository_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''One or more tag key-value pairs to use when tagging this repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def triggers(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnRepository.RepositoryTriggerProperty, _IResolvable_a771d0ef]]]]:
        '''The JSON block of configuration information for each trigger.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-triggers
        '''
        result = self._values.get("triggers")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnRepository.RepositoryTriggerProperty, _IResolvable_a771d0ef]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Code(metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk.aws_codecommit.Code"):
    '''(experimental) Represents the contents to initialize the repository with.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        repo = codecommit.Repository(self, "Repository",
            repository_name="MyRepositoryName",
            code=codecommit.Code.from_directory(path.join(__dirname, "directory/"), "develop")
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(
        cls,
        asset: _Asset_d07e8c00,
        branch: typing.Optional[builtins.str] = None,
    ) -> "Code":
        '''(experimental) Code from user-supplied asset.

        :param asset: pre-existing asset.
        :param branch: the name of the branch to create in the repository. Default is "main"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa0f76f159146579873b68d1beac8a858c945e09ed865fe240c2bdf5281d051)
            check_type(argname="argument asset", value=asset, expected_type=type_hints["asset"])
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
        return typing.cast("Code", jsii.sinvoke(cls, "fromAsset", [asset, branch]))

    @jsii.member(jsii_name="fromDirectory")
    @builtins.classmethod
    def from_directory(
        cls,
        directory_path: builtins.str,
        branch: typing.Optional[builtins.str] = None,
    ) -> "Code":
        '''(experimental) Code from directory.

        :param directory_path: the path to the local directory containing the contents to initialize the repository with.
        :param branch: the name of the branch to create in the repository. Default is "main"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c62fb86e7834a96d40f790c41fd9773d2d3c638a23e6e105d0851f15f5805bf4)
            check_type(argname="argument directory_path", value=directory_path, expected_type=type_hints["directory_path"])
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
        return typing.cast("Code", jsii.sinvoke(cls, "fromDirectory", [directory_path, branch]))

    @jsii.member(jsii_name="fromZipFile")
    @builtins.classmethod
    def from_zip_file(
        cls,
        file_path: builtins.str,
        branch: typing.Optional[builtins.str] = None,
    ) -> "Code":
        '''(experimental) Code from preexisting ZIP file.

        :param file_path: the path to the local ZIP file containing the contents to initialize the repository with.
        :param branch: the name of the branch to create in the repository. Default is "main"

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1f11d439ccf00f2f69065aaf3f894bd3120674e5d6f2babb69cb9f6028e0b3)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
        return typing.cast("Code", jsii.sinvoke(cls, "fromZipFile", [file_path, branch]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: _constructs_77d1e7e8.Construct) -> "CodeConfig":
        '''(experimental) This method is called after a repository is passed this instance of Code in its 'code' property.

        :param scope: the binding scope.

        :stability: experimental
        '''
        ...


class _CodeProxy(Code):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: _constructs_77d1e7e8.Construct) -> "CodeConfig":
        '''(experimental) This method is called after a repository is passed this instance of Code in its 'code' property.

        :param scope: the binding scope.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d41bfd4e9bebf3964620753a344107a78408a5806bf13847736528b1f9a813d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("CodeConfig", jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Code).__jsii_proxy_class__ = lambda : _CodeProxy


@jsii.data_type(
    jsii_type="monocdk.aws_codecommit.CodeConfig",
    jsii_struct_bases=[],
    name_mapping={"code": "code"},
)
class CodeConfig:
    def __init__(
        self,
        *,
        code: typing.Union[CfnRepository.CodeProperty, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) Represents the structure to pass into the underlying CfnRepository class.

        :param code: (experimental) represents the underlying code structure.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codecommit as codecommit
            
            code_config = codecommit.CodeConfig(
                code=codecommit.CfnRepository.CodeProperty(
                    s3=codecommit.CfnRepository.S3Property(
                        bucket="bucket",
                        key="key",
            
                        # the properties below are optional
                        object_version="objectVersion"
                    ),
            
                    # the properties below are optional
                    branch_name="branchName"
                )
            )
        '''
        if isinstance(code, dict):
            code = CfnRepository.CodeProperty(**code)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7ac3d9f3ec19c377559bdd2220f562bc56a01bf733576f3f5b924e9dfba65c8)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "code": code,
        }

    @builtins.property
    def code(self) -> CfnRepository.CodeProperty:
        '''(experimental) represents the underlying code structure.

        :stability: experimental
        '''
        result = self._values.get("code")
        assert result is not None, "Required property 'code' is missing"
        return typing.cast(CfnRepository.CodeProperty, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_codecommit.IRepository")
class IRepository(
    _IResource_8c1dbbbd,
    _INotificationRuleSource_904910c7,
    typing_extensions.Protocol,
):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> builtins.str:
        '''(experimental) The ARN of this Repository.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="repositoryCloneUrlGrc")
    def repository_clone_url_grc(self) -> builtins.str:
        '''(experimental) The HTTPS (GRC) clone URL.

        HTTPS (GRC) is the protocol to use with git-remote-codecommit (GRC).

        It is the recommended method for supporting connections made with federated
        access, identity providers, and temporary credentials.

        :see: https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-git-remote-codecommit.html
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="repositoryCloneUrlHttp")
    def repository_clone_url_http(self) -> builtins.str:
        '''(experimental) The HTTP clone URL.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="repositoryCloneUrlSsh")
    def repository_clone_url_ssh(self) -> builtins.str:
        '''(experimental) The SSH clone URL.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''(experimental) The human-visible name of this Repository.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given principal identity permissions to perform the actions on this repository.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions to pull this repository.

        :param grantee: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions to pull and push this repository.

        :param grantee: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions to read this repository.

        :param grantee: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="notifiyOnPullRequestMerged")
    def notifiy_on_pull_request_merged(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(deprecated) Defines a CodeStar Notification rule which triggers when a pull request is merged.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :deprecated: this method has a typo in its name, use notifyOnPullRequestMerged instead

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="notifyOn")
    def notify_on(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        events: typing.Sequence["RepositoryNotificationEvents"],
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule triggered when the project events specified by you are emitted. Similar to ``onEvent`` API.

        You can also use the methods to define rules for the specific event emitted.
        eg: ``notifyOnPullRequstCreated``.

        :param id: -
        :param target: -
        :param events: (experimental) A list of event types associated with this notification rule for CodeCommit repositories. For a complete list of event types and IDs, see Notification concepts in the Developer Tools Console User Guide.
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :return: CodeStar Notifications rule associated with this repository.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="notifyOnApprovalRuleOverridden")
    def notify_on_approval_rule_overridden(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when an approval rule is overridden.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="notifyOnApprovalStatusChanged")
    def notify_on_approval_status_changed(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when an approval status is changed.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="notifyOnBranchOrTagCreated")
    def notify_on_branch_or_tag_created(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when a new branch or tag is created.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="notifyOnBranchOrTagDeleted")
    def notify_on_branch_or_tag_deleted(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when a branch or tag is deleted.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="notifyOnPullRequestComment")
    def notify_on_pull_request_comment(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when a comment is made on a pull request.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="notifyOnPullRequestCreated")
    def notify_on_pull_request_created(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when a pull request is created.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="notifyOnPullRequestMerged")
    def notify_on_pull_request_merged(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when a pull request is merged.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onCommentOnCommit")
    def on_comment_on_commit(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a comment is made on a commit.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onCommentOnPullRequest")
    def on_comment_on_pull_request(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a comment is made on a pull request.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onCommit")
    def on_commit(
        self,
        id: builtins.str,
        *,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a commit is pushed to a branch.

        :param id: -
        :param branches: (experimental) The branch to monitor. Default: - All branches
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onPullRequestStateChange")
    def on_pull_request_state_change(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a pull request state is changed.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onReferenceCreated")
    def on_reference_created(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a reference is created (i.e. a new branch/tag is created) to the repository.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onReferenceDeleted")
    def on_reference_deleted(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a reference is delete (i.e. a branch/tag is deleted) from the repository.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onReferenceUpdated")
    def on_reference_updated(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a reference is updated (i.e. a commit is pushed to an existing or new branch) from the repository.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a "CodeCommit Repository State Change" event occurs.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        ...


class _IRepositoryProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
    jsii.proxy_for(_INotificationRuleSource_904910c7), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_codecommit.IRepository"

    @builtins.property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> builtins.str:
        '''(experimental) The ARN of this Repository.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryArn"))

    @builtins.property
    @jsii.member(jsii_name="repositoryCloneUrlGrc")
    def repository_clone_url_grc(self) -> builtins.str:
        '''(experimental) The HTTPS (GRC) clone URL.

        HTTPS (GRC) is the protocol to use with git-remote-codecommit (GRC).

        It is the recommended method for supporting connections made with federated
        access, identity providers, and temporary credentials.

        :see: https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-git-remote-codecommit.html
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryCloneUrlGrc"))

    @builtins.property
    @jsii.member(jsii_name="repositoryCloneUrlHttp")
    def repository_clone_url_http(self) -> builtins.str:
        '''(experimental) The HTTP clone URL.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryCloneUrlHttp"))

    @builtins.property
    @jsii.member(jsii_name="repositoryCloneUrlSsh")
    def repository_clone_url_ssh(self) -> builtins.str:
        '''(experimental) The SSH clone URL.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryCloneUrlSsh"))

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''(experimental) The human-visible name of this Repository.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given principal identity permissions to perform the actions on this repository.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9532fb0f7de7f2a31a80b677369766a00fce0b4577b4da77f1664bd1e00084ab)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions to pull this repository.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20c07d3296f0901b2300a63e21b532a6ec2ab59dbba12e490de5147bce98d054)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPull", [grantee]))

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions to pull and push this repository.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bef35ac0048e27ffe1c086fcb0f49dee24dda1176a680c6fb3c4fcb9a2c06133)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPullPush", [grantee]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions to read this repository.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__411068c6e2373fd52b7392dd416bd3b389ece859b17f0b93f8989151e924b097)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="notifiyOnPullRequestMerged")
    def notifiy_on_pull_request_merged(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(deprecated) Defines a CodeStar Notification rule which triggers when a pull request is merged.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :deprecated: this method has a typo in its name, use notifyOnPullRequestMerged instead

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__969ea68c9fd04e72482de6677f6f97d5658d7ad02d9d8afd37b64ab2b5cb4f80)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _NotificationRuleOptions_8645c987(
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        return typing.cast(_INotificationRule_e22254bb, jsii.invoke(self, "notifiyOnPullRequestMerged", [id, target, options]))

    @jsii.member(jsii_name="notifyOn")
    def notify_on(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        events: typing.Sequence["RepositoryNotificationEvents"],
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule triggered when the project events specified by you are emitted. Similar to ``onEvent`` API.

        You can also use the methods to define rules for the specific event emitted.
        eg: ``notifyOnPullRequstCreated``.

        :param id: -
        :param target: -
        :param events: (experimental) A list of event types associated with this notification rule for CodeCommit repositories. For a complete list of event types and IDs, see Notification concepts in the Developer Tools Console User Guide.
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :return: CodeStar Notifications rule associated with this repository.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895786268843e4dc61577d5aabe884d5889c9e09d0dc4e45340bf550c60e98f3)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = RepositoryNotifyOnOptions(
            events=events,
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        return typing.cast(_INotificationRule_e22254bb, jsii.invoke(self, "notifyOn", [id, target, options]))

    @jsii.member(jsii_name="notifyOnApprovalRuleOverridden")
    def notify_on_approval_rule_overridden(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when an approval rule is overridden.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2712084918cf295073c479053a4b783816a994249fc93e5f4b4d74299b9fdb3)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _NotificationRuleOptions_8645c987(
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        return typing.cast(_INotificationRule_e22254bb, jsii.invoke(self, "notifyOnApprovalRuleOverridden", [id, target, options]))

    @jsii.member(jsii_name="notifyOnApprovalStatusChanged")
    def notify_on_approval_status_changed(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when an approval status is changed.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55430598a11091e6e5d302f707e88f16c513158c06f448a95f5571882271b8e9)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _NotificationRuleOptions_8645c987(
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        return typing.cast(_INotificationRule_e22254bb, jsii.invoke(self, "notifyOnApprovalStatusChanged", [id, target, options]))

    @jsii.member(jsii_name="notifyOnBranchOrTagCreated")
    def notify_on_branch_or_tag_created(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when a new branch or tag is created.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df66651c740f53e5625a122eb24397c7230a745d49aa891308a9e602cce35a09)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _NotificationRuleOptions_8645c987(
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        return typing.cast(_INotificationRule_e22254bb, jsii.invoke(self, "notifyOnBranchOrTagCreated", [id, target, options]))

    @jsii.member(jsii_name="notifyOnBranchOrTagDeleted")
    def notify_on_branch_or_tag_deleted(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when a branch or tag is deleted.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a489769acab158057a35e66cf3e6c6e4c00c8928bafcb2721b811428859ac5)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _NotificationRuleOptions_8645c987(
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        return typing.cast(_INotificationRule_e22254bb, jsii.invoke(self, "notifyOnBranchOrTagDeleted", [id, target, options]))

    @jsii.member(jsii_name="notifyOnPullRequestComment")
    def notify_on_pull_request_comment(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when a comment is made on a pull request.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19cedd9ad64701ea0e5b6e03de6da7dee39df720624bec2b0a7979d75c009951)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _NotificationRuleOptions_8645c987(
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        return typing.cast(_INotificationRule_e22254bb, jsii.invoke(self, "notifyOnPullRequestComment", [id, target, options]))

    @jsii.member(jsii_name="notifyOnPullRequestCreated")
    def notify_on_pull_request_created(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when a pull request is created.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415ef28018465177c719dba45064a51e2b7877ecf8f248213c22661bf1199f7e)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _NotificationRuleOptions_8645c987(
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        return typing.cast(_INotificationRule_e22254bb, jsii.invoke(self, "notifyOnPullRequestCreated", [id, target, options]))

    @jsii.member(jsii_name="notifyOnPullRequestMerged")
    def notify_on_pull_request_merged(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when a pull request is merged.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66af67f59190aa64b6129dd91545ce52bd770d7f89cf297a27d0aaad57c0f504)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _NotificationRuleOptions_8645c987(
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        return typing.cast(_INotificationRule_e22254bb, jsii.invoke(self, "notifyOnPullRequestMerged", [id, target, options]))

    @jsii.member(jsii_name="onCommentOnCommit")
    def on_comment_on_commit(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a comment is made on a commit.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c222bbaf7d9edaad6612bb791190b6270de2de32b7f6094648ec1b8ff3f5109)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onCommentOnCommit", [id, options]))

    @jsii.member(jsii_name="onCommentOnPullRequest")
    def on_comment_on_pull_request(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a comment is made on a pull request.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63ed90364a91822929d8f6dbf50eacacb1dd1beceaf2ac0b73fd637245b230e9)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onCommentOnPullRequest", [id, options]))

    @jsii.member(jsii_name="onCommit")
    def on_commit(
        self,
        id: builtins.str,
        *,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a commit is pushed to a branch.

        :param id: -
        :param branches: (experimental) The branch to monitor. Default: - All branches
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa148a1e5590e4a415483930d161f416df5a0d0e337be07df0f32b48104fdf66)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = OnCommitOptions(
            branches=branches,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onCommit", [id, options]))

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d120edae194b90e2a80f7af14430f27827dced063b24e7c8123fe0a188b9096)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onEvent", [id, options]))

    @jsii.member(jsii_name="onPullRequestStateChange")
    def on_pull_request_state_change(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a pull request state is changed.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a5bb8df110c27d751752311b21db4ff247eef97bb38c97acac49c6a3411ac95)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onPullRequestStateChange", [id, options]))

    @jsii.member(jsii_name="onReferenceCreated")
    def on_reference_created(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a reference is created (i.e. a new branch/tag is created) to the repository.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4835ede748cc9b59e7c07e1f2d55eb3f378eea8ce3d9c59168c9e467c3b78b5e)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onReferenceCreated", [id, options]))

    @jsii.member(jsii_name="onReferenceDeleted")
    def on_reference_deleted(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a reference is delete (i.e. a branch/tag is deleted) from the repository.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9cf32afd45ba378d4b579b1fb2084afbb03afccb16ef74d5db4f05e5792ae7)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onReferenceDeleted", [id, options]))

    @jsii.member(jsii_name="onReferenceUpdated")
    def on_reference_updated(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a reference is updated (i.e. a commit is pushed to an existing or new branch) from the repository.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcb3b93164a720f5d36e6423cd2d64cc0e0865b023cf5404369982e1f1dd5b06)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onReferenceUpdated", [id, options]))

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a "CodeCommit Repository State Change" event occurs.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00778a902217726a81ff27f476d3c711842ed9a5505aa303dd3eadbbca39908c)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onStateChange", [id, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRepository).__jsii_proxy_class__ = lambda : _IRepositoryProxy


@jsii.data_type(
    jsii_type="monocdk.aws_codecommit.OnCommitOptions",
    jsii_struct_bases=[_OnEventOptions_d5081088],
    name_mapping={
        "description": "description",
        "event_pattern": "eventPattern",
        "rule_name": "ruleName",
        "target": "target",
        "branches": "branches",
    },
)
class OnCommitOptions(_OnEventOptions_d5081088):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for the onCommit() method.

        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param branches: (experimental) The branch to monitor. Default: - All branches

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as codecommit
            import monocdk as targets
            
            # repo: codecommit.Repository
            
            my_topic = sns.Topic(self, "Topic")
            
            repo.on_commit("OnCommit",
                target=targets.SnsTopic(my_topic)
            )
        '''
        if isinstance(event_pattern, dict):
            event_pattern = _EventPattern_a23fbf37(**event_pattern)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b99e70e05908e0b867feec6d72921264aeb152c1bb5b874fec8ef3ca8c59bb3)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument event_pattern", value=event_pattern, expected_type=type_hints["event_pattern"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if target is not None:
            self._values["target"] = target
        if branches is not None:
            self._values["branches"] = branches

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the rule's purpose.

        :default: - No description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_pattern(self) -> typing.Optional[_EventPattern_a23fbf37]:
        '''(experimental) Additional restrictions for the event to route to the specified target.

        The method that generates the rule probably imposes some type of event
        filtering. The filtering implied by what you pass here is added
        on top of that filtering.

        :default: - No additional filtering based on an event pattern.

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html
        :stability: experimental
        '''
        result = self._values.get("event_pattern")
        return typing.cast(typing.Optional[_EventPattern_a23fbf37], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the rule.

        :default: AWS CloudFormation generates a unique physical ID.

        :stability: experimental
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[_IRuleTarget_d45ec729]:
        '''(experimental) The target to register for the event.

        :default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[_IRuleTarget_d45ec729], result)

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The branch to monitor.

        :default: - All branches

        :stability: experimental
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCommitOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReferenceEvent(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codecommit.ReferenceEvent",
):
    '''(experimental) Fields of CloudWatch Events that change references.

    :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#codebuild_event_type
    :stability: experimental
    '''

    @jsii.python.classproperty
    @jsii.member(jsii_name="commitId")
    def commit_id(cls) -> builtins.str:
        '''(experimental) Commit id this reference now points to.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "commitId"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="eventType")
    def event_type(cls) -> builtins.str:
        '''(experimental) The type of reference event.

        'referenceCreated', 'referenceUpdated' or 'referenceDeleted'

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "eventType"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="referenceFullName")
    def reference_full_name(cls) -> builtins.str:
        '''(experimental) Full reference name.

        For example, 'refs/tags/myTag'

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "referenceFullName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="referenceName")
    def reference_name(cls) -> builtins.str:
        '''(experimental) Name of reference changed (branch or tag name).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "referenceName"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="referenceType")
    def reference_type(cls) -> builtins.str:
        '''(experimental) Type of reference changed.

        'branch' or 'tag'

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "referenceType"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="repositoryId")
    def repository_id(cls) -> builtins.str:
        '''(experimental) Id of the CodeCommit repository.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "repositoryId"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="repositoryName")
    def repository_name(cls) -> builtins.str:
        '''(experimental) Name of the CodeCommit repository.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "repositoryName"))


@jsii.implements(IRepository)
class Repository(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codecommit.Repository",
):
    '''(experimental) Provides a CodeCommit Repository.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # project: codebuild.PipelineProject
        
        repository = codecommit.Repository(self, "MyRepository",
            repository_name="MyRepository"
        )
        project = codebuild.PipelineProject(self, "MyProject")
        
        source_output = codepipeline.Artifact()
        source_action = codepipeline_actions.CodeCommitSourceAction(
            action_name="CodeCommit",
            repository=repository,
            output=source_output
        )
        build_action = codepipeline_actions.CodeBuildAction(
            action_name="CodeBuild",
            project=project,
            input=source_output,
            outputs=[codepipeline.Artifact()],  # optional
            execute_batch_build=True,  # optional, defaults to false
            combine_batch_build_artifacts=True
        )
        
        codepipeline.Pipeline(self, "MyPipeline",
            stages=[codebuild.aws_codepipeline.StageProps(
                stage_name="Source",
                actions=[source_action]
            ), codebuild.aws_codepipeline.StageProps(
                stage_name="Build",
                actions=[build_action]
            )
            ]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        repository_name: builtins.str,
        code: typing.Optional[Code] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param repository_name: (experimental) Name of the repository. This property is required for all CodeCommit repositories.
        :param code: (experimental) The contents with which to initialize the repository after it has been created. Default: - No initialization (create empty repo)
        :param description: (experimental) A description of the repository. Use the description to identify the purpose of the repository. Default: - No description.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67b702110160741503b9effcbfd9c051c8c729fd31b130fb7bdb78ff438978f8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RepositoryProps(
            repository_name=repository_name, code=code, description=description
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromRepositoryArn")
    @builtins.classmethod
    def from_repository_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        repository_arn: builtins.str,
    ) -> IRepository:
        '''(experimental) Imports a codecommit repository.

        :param scope: -
        :param id: -
        :param repository_arn: (e.g. ``arn:aws:codecommit:us-east-1:123456789012:MyDemoRepo``).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441ff7aa7d7085d3b4aa8a61ea92744b1f222f0193a619c2d040cdf0f4ba7b7d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument repository_arn", value=repository_arn, expected_type=type_hints["repository_arn"])
        return typing.cast(IRepository, jsii.sinvoke(cls, "fromRepositoryArn", [scope, id, repository_arn]))

    @jsii.member(jsii_name="fromRepositoryName")
    @builtins.classmethod
    def from_repository_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        repository_name: builtins.str,
    ) -> IRepository:
        '''
        :param scope: -
        :param id: -
        :param repository_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__765246864edff89547cacd11109965bc8ee740241f64c20bad75ce8e00a437ce)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
        return typing.cast(IRepository, jsii.sinvoke(cls, "fromRepositoryName", [scope, id, repository_name]))

    @jsii.member(jsii_name="bindAsNotificationRuleSource")
    def bind_as_notification_rule_source(
        self,
        _scope: _constructs_77d1e7e8.Construct,
    ) -> _NotificationRuleSourceConfig_fd02300e:
        '''(experimental) Returns a source configuration for notification rule.

        :param _scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae75e12836ae0459cc9ca43abd5f7d8fc62898ed4c8ab76200a3bdcd5d0448e)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(_NotificationRuleSourceConfig_fd02300e, jsii.invoke(self, "bindAsNotificationRuleSource", [_scope]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _IGrantable_4c5a91d1,
        *actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given principal identity permissions to perform the actions on this repository.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0711effefea0a53fa7cbbc7c433ecf56b484767ee8c5d0771604fbabcd82a43b)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantPull")
    def grant_pull(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions to pull this repository.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d15c9fca5739262c65a2fe8cb883b7aee2819b762237c1396f9c5115274f399)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPull", [grantee]))

    @jsii.member(jsii_name="grantPullPush")
    def grant_pull_push(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions to pull and push this repository.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__056cd07322b8dfafdcca44fe34cc77f40ff2d615a1a7b364b1c47d73abbb4247)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPullPush", [grantee]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions to read this repository.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e617b08ed6b867571778b8b5fb9e9683a474eef17435d0a91344cba5f0a7fd8)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="notifiyOnPullRequestMerged")
    def notifiy_on_pull_request_merged(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when a pull request is merged.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c429c9c889235d6540654cdbb73c5065882dd297d8855deadee14acaed3f6f)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _NotificationRuleOptions_8645c987(
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        return typing.cast(_INotificationRule_e22254bb, jsii.invoke(self, "notifiyOnPullRequestMerged", [id, target, options]))

    @jsii.member(jsii_name="notify")
    def notify(
        self,
        arn: builtins.str,
        *,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_data: typing.Optional[builtins.str] = None,
        events: typing.Optional[typing.Sequence["RepositoryEventTrigger"]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "Repository":
        '''(experimental) Create a trigger to notify another service to run actions on repository events.

        :param arn: Arn of the resource that repository events will notify.
        :param branches: (experimental) The names of the branches in the AWS CodeCommit repository that contain events that you want to include in the trigger. If you don't specify at least one branch, the trigger applies to all branches.
        :param custom_data: (experimental) When an event is triggered, additional information that AWS CodeCommit includes when it sends information to the target.
        :param events: (experimental) The repository events for which AWS CodeCommit sends information to the target, which you specified in the DestinationArn property.If you don't specify events, the trigger runs for all repository events.
        :param name: (experimental) A name for the trigger.Triggers on a repository must have unique names.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b92f05ebac3742cefbfcb3cef3fa4e8cf55eab719c14ccbc4674509c7956127)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        options = RepositoryTriggerOptions(
            branches=branches, custom_data=custom_data, events=events, name=name
        )

        return typing.cast("Repository", jsii.invoke(self, "notify", [arn, options]))

    @jsii.member(jsii_name="notifyOn")
    def notify_on(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        events: typing.Sequence["RepositoryNotificationEvents"],
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule triggered when the project events specified by you are emitted. Similar to ``onEvent`` API.

        You can also use the methods to define rules for the specific event emitted.
        eg: ``notifyOnPullRequstCreated``.

        :param id: -
        :param target: -
        :param events: (experimental) A list of event types associated with this notification rule for CodeCommit repositories. For a complete list of event types and IDs, see Notification concepts in the Developer Tools Console User Guide.
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e45a0fb1fe80dbce55cc4a7a756c8ad319cbf2f424126fe57041de9a8457d4)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = RepositoryNotifyOnOptions(
            events=events,
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        return typing.cast(_INotificationRule_e22254bb, jsii.invoke(self, "notifyOn", [id, target, options]))

    @jsii.member(jsii_name="notifyOnApprovalRuleOverridden")
    def notify_on_approval_rule_overridden(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when an approval rule is overridden.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3baece54499f81167fa8c66847ff77e7dbec0ca657de100221ca982bcb9794f)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _NotificationRuleOptions_8645c987(
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        return typing.cast(_INotificationRule_e22254bb, jsii.invoke(self, "notifyOnApprovalRuleOverridden", [id, target, options]))

    @jsii.member(jsii_name="notifyOnApprovalStatusChanged")
    def notify_on_approval_status_changed(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when an approval status is changed.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b18ae82af152694e517a6074c97ebb59d73c6e8e3d56879c1d40a79da5fe931)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _NotificationRuleOptions_8645c987(
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        return typing.cast(_INotificationRule_e22254bb, jsii.invoke(self, "notifyOnApprovalStatusChanged", [id, target, options]))

    @jsii.member(jsii_name="notifyOnBranchOrTagCreated")
    def notify_on_branch_or_tag_created(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when a new branch or tag is created.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac8e3677bec422cfc130e3c9df1f99139fab001792183e3c7f6a78d62d0863fb)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _NotificationRuleOptions_8645c987(
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        return typing.cast(_INotificationRule_e22254bb, jsii.invoke(self, "notifyOnBranchOrTagCreated", [id, target, options]))

    @jsii.member(jsii_name="notifyOnBranchOrTagDeleted")
    def notify_on_branch_or_tag_deleted(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when a branch or tag is deleted.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a58ec02341a5eccad3e7f7c6224b0b44b3a93232882f08ed9cc863610d0eab2)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _NotificationRuleOptions_8645c987(
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        return typing.cast(_INotificationRule_e22254bb, jsii.invoke(self, "notifyOnBranchOrTagDeleted", [id, target, options]))

    @jsii.member(jsii_name="notifyOnPullRequestComment")
    def notify_on_pull_request_comment(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when a comment is made on a pull request.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c825c1bc19eb7b66e833e954e68237a9016091fb996a5a5e978ed62643affd5e)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _NotificationRuleOptions_8645c987(
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        return typing.cast(_INotificationRule_e22254bb, jsii.invoke(self, "notifyOnPullRequestComment", [id, target, options]))

    @jsii.member(jsii_name="notifyOnPullRequestCreated")
    def notify_on_pull_request_created(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when a pull request is created.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6031d863d03a31f78adbc2bcf252e1c00f1e8ef84f5e8a66e3bdfe63dab042)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _NotificationRuleOptions_8645c987(
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        return typing.cast(_INotificationRule_e22254bb, jsii.invoke(self, "notifyOnPullRequestCreated", [id, target, options]))

    @jsii.member(jsii_name="notifyOnPullRequestMerged")
    def notify_on_pull_request_merged(
        self,
        id: builtins.str,
        target: _INotificationRuleTarget_31f512df,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
    ) -> _INotificationRule_e22254bb:
        '''(experimental) Defines a CodeStar Notification rule which triggers when a pull request is merged.

        :param id: -
        :param target: -
        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f312b36168f77a4b8e7f2e3260b07b61fa8fe1c762211c4e5d5f177ccc78bada)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _NotificationRuleOptions_8645c987(
            detail_type=detail_type,
            enabled=enabled,
            notification_rule_name=notification_rule_name,
        )

        return typing.cast(_INotificationRule_e22254bb, jsii.invoke(self, "notifyOnPullRequestMerged", [id, target, options]))

    @jsii.member(jsii_name="onCommentOnCommit")
    def on_comment_on_commit(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a comment is made on a commit.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4e398919e437dcb2792b256e666ccf8506ebbb277cfc8f2617ec1195141a077)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onCommentOnCommit", [id, options]))

    @jsii.member(jsii_name="onCommentOnPullRequest")
    def on_comment_on_pull_request(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a comment is made on a pull request.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c692cff4290ae8eab9eeab58c024a8a518f43df14e895f8ad4d047e93dd4359)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onCommentOnPullRequest", [id, options]))

    @jsii.member(jsii_name="onCommit")
    def on_commit(
        self,
        id: builtins.str,
        *,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a commit is pushed to a branch.

        :param id: -
        :param branches: (experimental) The branch to monitor. Default: - All branches
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e62fe5d2cbdb235a45fbcbdb37b7f68a4c9a1cd9721f87fc717cf2168912985)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = OnCommitOptions(
            branches=branches,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onCommit", [id, options]))

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c653bc8df5da90bf8bde8cb0e984d885950c98dabbc9f21ecc4b5b7056e07921)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onEvent", [id, options]))

    @jsii.member(jsii_name="onPullRequestStateChange")
    def on_pull_request_state_change(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a pull request state is changed.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40289a89949d9bb1a0583d26b86206c78f22fbf6d49a4d479ed8dd8db6601754)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onPullRequestStateChange", [id, options]))

    @jsii.member(jsii_name="onReferenceCreated")
    def on_reference_created(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a reference is created (i.e. a new branch/tag is created) to the repository.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aba71a293de533d43b9303a3845ef7673f90a5e4df14ca39cb92a3f2b667866)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onReferenceCreated", [id, options]))

    @jsii.member(jsii_name="onReferenceDeleted")
    def on_reference_deleted(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a reference is delete (i.e. a branch/tag is deleted) from the repository.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f241da44db7ed952910cc114ac9604aa42abc3bafd1b353ab4c55a04839880)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onReferenceDeleted", [id, options]))

    @jsii.member(jsii_name="onReferenceUpdated")
    def on_reference_updated(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a reference is updated (i.e. a commit is pushed to an existing or new branch) from the repository.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc55d51c35ce0db927ba2d521b9c6d55ea6e112637c5be6514651f7423a3788a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onReferenceUpdated", [id, options]))

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event rule which triggers when a "CodeCommit Repository State Change" event occurs.

        :param id: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b075258fbc00f67aa9ec7f42c7423bb3e45ec6e2227cc08037861d8960b7d797)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _OnEventOptions_d5081088(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onStateChange", [id, options]))

    @builtins.property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> builtins.str:
        '''(experimental) The ARN of this Repository.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryArn"))

    @builtins.property
    @jsii.member(jsii_name="repositoryCloneUrlGrc")
    def repository_clone_url_grc(self) -> builtins.str:
        '''(experimental) The HTTPS (GRC) clone URL.

        HTTPS (GRC) is the protocol to use with git-remote-codecommit (GRC).

        It is the recommended method for supporting connections made with federated
        access, identity providers, and temporary credentials.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryCloneUrlGrc"))

    @builtins.property
    @jsii.member(jsii_name="repositoryCloneUrlHttp")
    def repository_clone_url_http(self) -> builtins.str:
        '''(experimental) The HTTP clone URL.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryCloneUrlHttp"))

    @builtins.property
    @jsii.member(jsii_name="repositoryCloneUrlSsh")
    def repository_clone_url_ssh(self) -> builtins.str:
        '''(experimental) The SSH clone URL.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryCloneUrlSsh"))

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        '''(experimental) The human-visible name of this Repository.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))


@jsii.enum(jsii_type="monocdk.aws_codecommit.RepositoryEventTrigger")
class RepositoryEventTrigger(enum.Enum):
    '''(experimental) Repository events that will cause the trigger to run actions in another service.

    :stability: experimental
    '''

    ALL = "ALL"
    '''
    :stability: experimental
    '''
    UPDATE_REF = "UPDATE_REF"
    '''
    :stability: experimental
    '''
    CREATE_REF = "CREATE_REF"
    '''
    :stability: experimental
    '''
    DELETE_REF = "DELETE_REF"
    '''
    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_codecommit.RepositoryNotificationEvents")
class RepositoryNotificationEvents(enum.Enum):
    '''(experimental) List of event types for AWS CodeCommit.

    :see: https://docs.aws.amazon.com/dtconsole/latest/userguide/concepts.html#events-ref-repositories
    :stability: experimental
    '''

    COMMIT_COMMENT = "COMMIT_COMMENT"
    '''(experimental) Trigger notication when comment made on commit.

    :stability: experimental
    '''
    PULL_REQUEST_COMMENT = "PULL_REQUEST_COMMENT"
    '''(experimental) Trigger notification when comment made on pull request.

    :stability: experimental
    '''
    APPROVAL_STATUS_CHANGED = "APPROVAL_STATUS_CHANGED"
    '''(experimental) Trigger notification when approval status changed.

    :stability: experimental
    '''
    APPROVAL_RULE_OVERRIDDEN = "APPROVAL_RULE_OVERRIDDEN"
    '''(experimental) Trigger notifications when approval rule is overridden.

    :stability: experimental
    '''
    PULL_REQUEST_CREATED = "PULL_REQUEST_CREATED"
    '''(experimental) Trigger notification when pull request created.

    :stability: experimental
    '''
    PULL_REQUEST_SOURCE_UPDATED = "PULL_REQUEST_SOURCE_UPDATED"
    '''(experimental) Trigger notification when pull request source updated.

    :stability: experimental
    '''
    PULL_REQUEST_STATUS_CHANGED = "PULL_REQUEST_STATUS_CHANGED"
    '''(experimental) Trigger notification when pull request status is changed.

    :stability: experimental
    '''
    PULL_REQUEST_MERGED = "PULL_REQUEST_MERGED"
    '''(experimental) Trigger notification when pull requset is merged.

    :stability: experimental
    '''
    BRANCH_OR_TAG_CREATED = "BRANCH_OR_TAG_CREATED"
    '''(experimental) Trigger notification when a branch or tag is created.

    :stability: experimental
    '''
    BRANCH_OR_TAG_DELETED = "BRANCH_OR_TAG_DELETED"
    '''(experimental) Trigger notification when a branch or tag is deleted.

    :stability: experimental
    '''
    BRANCH_OR_TAG_UPDATED = "BRANCH_OR_TAG_UPDATED"
    '''(experimental) Trigger notification when a branch or tag is updated.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_codecommit.RepositoryNotifyOnOptions",
    jsii_struct_bases=[_NotificationRuleOptions_8645c987],
    name_mapping={
        "detail_type": "detailType",
        "enabled": "enabled",
        "notification_rule_name": "notificationRuleName",
        "events": "events",
    },
)
class RepositoryNotifyOnOptions(_NotificationRuleOptions_8645c987):
    def __init__(
        self,
        *,
        detail_type: typing.Optional[_DetailType_50204ab4] = None,
        enabled: typing.Optional[builtins.bool] = None,
        notification_rule_name: typing.Optional[builtins.str] = None,
        events: typing.Sequence[RepositoryNotificationEvents],
    ) -> None:
        '''(experimental) Additional options to pass to the notification rule.

        :param detail_type: (experimental) The level of detail to include in the notifications for this resource. BASIC will include only the contents of the event as it would appear in AWS CloudWatch. FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created. Default: DetailType.FULL
        :param enabled: (experimental) The status of the notification rule. If the enabled is set to DISABLED, notifications aren't sent for the notification rule. Default: true
        :param notification_rule_name: (experimental) The name for the notification rule. Notification rule names must be unique in your AWS account. Default: - generated from the ``id``
        :param events: (experimental) A list of event types associated with this notification rule for CodeCommit repositories. For a complete list of event types and IDs, see Notification concepts in the Developer Tools Console User Guide.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codecommit as codecommit
            from monocdk import aws_codestarnotifications as codestarnotifications
            
            repository_notify_on_options = codecommit.RepositoryNotifyOnOptions(
                events=[codecommit.RepositoryNotificationEvents.COMMIT_COMMENT],
            
                # the properties below are optional
                detail_type=codestarnotifications.DetailType.BASIC,
                enabled=False,
                notification_rule_name="notificationRuleName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b08d3ebffafc9f7f2ec129ddca33b44c47f8a9118d20518f2690f25e18c8ebb)
            check_type(argname="argument detail_type", value=detail_type, expected_type=type_hints["detail_type"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument notification_rule_name", value=notification_rule_name, expected_type=type_hints["notification_rule_name"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "events": events,
        }
        if detail_type is not None:
            self._values["detail_type"] = detail_type
        if enabled is not None:
            self._values["enabled"] = enabled
        if notification_rule_name is not None:
            self._values["notification_rule_name"] = notification_rule_name

    @builtins.property
    def detail_type(self) -> typing.Optional[_DetailType_50204ab4]:
        '''(experimental) The level of detail to include in the notifications for this resource.

        BASIC will include only the contents of the event as it would appear in AWS CloudWatch.
        FULL will include any supplemental information provided by AWS CodeStar Notifications and/or the service for the resource for which the notification is created.

        :default: DetailType.FULL

        :stability: experimental
        '''
        result = self._values.get("detail_type")
        return typing.cast(typing.Optional[_DetailType_50204ab4], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) The status of the notification rule.

        If the enabled is set to DISABLED, notifications aren't sent for the notification rule.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def notification_rule_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for the notification rule.

        Notification rule names must be unique in your AWS account.

        :default: - generated from the ``id``

        :stability: experimental
        '''
        result = self._values.get("notification_rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def events(self) -> typing.List[RepositoryNotificationEvents]:
        '''(experimental) A list of event types associated with this notification rule for CodeCommit repositories.

        For a complete list of event types and IDs, see Notification concepts in the Developer Tools Console User Guide.

        :see: https://docs.aws.amazon.com/dtconsole/latest/userguide/concepts.html#concepts-api
        :stability: experimental
        '''
        result = self._values.get("events")
        assert result is not None, "Required property 'events' is missing"
        return typing.cast(typing.List[RepositoryNotificationEvents], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryNotifyOnOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_codecommit.RepositoryProps",
    jsii_struct_bases=[],
    name_mapping={
        "repository_name": "repositoryName",
        "code": "code",
        "description": "description",
    },
)
class RepositoryProps:
    def __init__(
        self,
        *,
        repository_name: builtins.str,
        code: typing.Optional[Code] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param repository_name: (experimental) Name of the repository. This property is required for all CodeCommit repositories.
        :param code: (experimental) The contents with which to initialize the repository after it has been created. Default: - No initialization (create empty repo)
        :param description: (experimental) A description of the repository. Use the description to identify the purpose of the repository. Default: - No description.

        :stability: experimental
        :exampleMetadata: lit=lib/aws-codepipeline-actions/test/integ.cfn-template-from-repo.lit.ts infused

        Example::

            # Source stage: read from repository
            repo = codecommit.Repository(stack, "TemplateRepo",
                repository_name="template-repo"
            )
            source_output = codepipeline.Artifact("SourceArtifact")
            source = cpactions.CodeCommitSourceAction(
                action_name="Source",
                repository=repo,
                output=source_output,
                trigger=cpactions.CodeCommitTrigger.POLL
            )
            source_stage = {
                "stage_name": "Source",
                "actions": [source]
            }
            
            # Deployment stage: create and deploy changeset with manual approval
            stack_name = "OurStack"
            change_set_name = "StagedChangeSet"
            
            prod_stage = {
                "stage_name": "Deploy",
                "actions": [
                    cpactions.CloudFormationCreateReplaceChangeSetAction(
                        action_name="PrepareChanges",
                        stack_name=stack_name,
                        change_set_name=change_set_name,
                        admin_permissions=True,
                        template_path=source_output.at_path("template.yaml"),
                        run_order=1
                    ),
                    cpactions.ManualApprovalAction(
                        action_name="ApproveChanges",
                        run_order=2
                    ),
                    cpactions.CloudFormationExecuteChangeSetAction(
                        action_name="ExecuteChanges",
                        stack_name=stack_name,
                        change_set_name=change_set_name,
                        run_order=3
                    )
                ]
            }
            
            codepipeline.Pipeline(stack, "Pipeline",
                stages=[source_stage, prod_stage
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e04d07c2ffdb287154d3fa06b9de216b06015dda3f1870c60848c83c94c982cc)
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_name": repository_name,
        }
        if code is not None:
            self._values["code"] = code
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def repository_name(self) -> builtins.str:
        '''(experimental) Name of the repository.

        This property is required for all CodeCommit repositories.

        :stability: experimental
        '''
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def code(self) -> typing.Optional[Code]:
        '''(experimental) The contents with which to initialize the repository after it has been created.

        :default: - No initialization (create empty repo)

        :stability: experimental
        '''
        result = self._values.get("code")
        return typing.cast(typing.Optional[Code], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the repository.

        Use the description to identify the
        purpose of the repository.

        :default: - No description.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_codecommit.RepositoryTriggerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "branches": "branches",
        "custom_data": "customData",
        "events": "events",
        "name": "name",
    },
)
class RepositoryTriggerOptions:
    def __init__(
        self,
        *,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        custom_data: typing.Optional[builtins.str] = None,
        events: typing.Optional[typing.Sequence[RepositoryEventTrigger]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Creates for a repository trigger to an SNS topic or Lambda function.

        :param branches: (experimental) The names of the branches in the AWS CodeCommit repository that contain events that you want to include in the trigger. If you don't specify at least one branch, the trigger applies to all branches.
        :param custom_data: (experimental) When an event is triggered, additional information that AWS CodeCommit includes when it sends information to the target.
        :param events: (experimental) The repository events for which AWS CodeCommit sends information to the target, which you specified in the DestinationArn property.If you don't specify events, the trigger runs for all repository events.
        :param name: (experimental) A name for the trigger.Triggers on a repository must have unique names.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codecommit as codecommit
            
            repository_trigger_options = codecommit.RepositoryTriggerOptions(
                branches=["branches"],
                custom_data="customData",
                events=[codecommit.RepositoryEventTrigger.ALL],
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__297c4cea56ab32a05c65812129d9862d9dd382ee822f154e088c13735dbb444d)
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument custom_data", value=custom_data, expected_type=type_hints["custom_data"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches
        if custom_data is not None:
            self._values["custom_data"] = custom_data
        if events is not None:
            self._values["events"] = events
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The names of the branches in the AWS CodeCommit repository that contain events that you want to include in the trigger.

        If you don't specify at
        least one branch, the trigger applies to all branches.

        :stability: experimental
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def custom_data(self) -> typing.Optional[builtins.str]:
        '''(experimental) When an event is triggered, additional information that AWS CodeCommit includes when it sends information to the target.

        :stability: experimental
        '''
        result = self._values.get("custom_data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def events(self) -> typing.Optional[typing.List[RepositoryEventTrigger]]:
        '''(experimental) The repository events for which AWS CodeCommit sends information to the target, which you specified in the DestinationArn property.If you don't specify events, the trigger runs for all repository events.

        :stability: experimental
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.List[RepositoryEventTrigger]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the trigger.Triggers on a repository must have unique names.

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryTriggerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnRepository",
    "CfnRepositoryProps",
    "Code",
    "CodeConfig",
    "IRepository",
    "OnCommitOptions",
    "ReferenceEvent",
    "Repository",
    "RepositoryEventTrigger",
    "RepositoryNotificationEvents",
    "RepositoryNotifyOnOptions",
    "RepositoryProps",
    "RepositoryTriggerOptions",
]

publication.publish()

def _typecheckingstub__138c763af5bf3552be2c0297711208a0a9ddb27d3d6d8d783bdc84b0279008e8(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    repository_name: builtins.str,
    code: typing.Optional[typing.Union[typing.Union[CfnRepository.CodeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    repository_description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    triggers: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRepository.RepositoryTriggerProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c3c9a38e189e8c10098c38ad2d36fb65dc5bdb08345a8ff330cd8defd15dc9(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a95098a5b5d23ad477d7ad15ec7a5ffe3b4a01ce45fd707fcfee84a932a13ee(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e4c8ce166d7b0de46a08c034bd1a7afcd09961e177f6ef3b9842cafb236d4c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c17f1618c777f7ca79020f0e1664d223f03aaba7a9cbe234043479387ec0339(
    value: typing.Optional[typing.Union[CfnRepository.CodeProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2222af807d41424f5860b1e1192ad08c137070db39e28a29a22c482b5f4dc2f5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f147d495a9ff1902010a9c6541609faacc556a8e5b5d73a01e0e820a2d8194fc(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnRepository.RepositoryTriggerProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__732dcde002b52900cf0f056286147721c52681c4d24374e8a2ae9f8a7f6a1ed1(
    *,
    s3: typing.Union[typing.Union[CfnRepository.S3Property, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    branch_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e411564b8ff3f43f467c50e6abecb164f56e11e313eb292bf5ee90aa2a4267(
    *,
    destination_arn: builtins.str,
    events: typing.Sequence[builtins.str],
    name: builtins.str,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ea2cd814e721c8483c10d9b6229d225311fa63b482e4cd1837e981a5371565(
    *,
    bucket: builtins.str,
    key: builtins.str,
    object_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d721eea3db77201398649ea6b8db802a256f00e901998fa1855041c1a16fb4(
    *,
    repository_name: builtins.str,
    code: typing.Optional[typing.Union[typing.Union[CfnRepository.CodeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    repository_description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    triggers: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRepository.RepositoryTriggerProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa0f76f159146579873b68d1beac8a858c945e09ed865fe240c2bdf5281d051(
    asset: _Asset_d07e8c00,
    branch: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62fb86e7834a96d40f790c41fd9773d2d3c638a23e6e105d0851f15f5805bf4(
    directory_path: builtins.str,
    branch: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1f11d439ccf00f2f69065aaf3f894bd3120674e5d6f2babb69cb9f6028e0b3(
    file_path: builtins.str,
    branch: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d41bfd4e9bebf3964620753a344107a78408a5806bf13847736528b1f9a813d(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ac3d9f3ec19c377559bdd2220f562bc56a01bf733576f3f5b924e9dfba65c8(
    *,
    code: typing.Union[CfnRepository.CodeProperty, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9532fb0f7de7f2a31a80b677369766a00fce0b4577b4da77f1664bd1e00084ab(
    grantee: _IGrantable_4c5a91d1,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c07d3296f0901b2300a63e21b532a6ec2ab59dbba12e490de5147bce98d054(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef35ac0048e27ffe1c086fcb0f49dee24dda1176a680c6fb3c4fcb9a2c06133(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__411068c6e2373fd52b7392dd416bd3b389ece859b17f0b93f8989151e924b097(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__969ea68c9fd04e72482de6677f6f97d5658d7ad02d9d8afd37b64ab2b5cb4f80(
    id: builtins.str,
    target: _INotificationRuleTarget_31f512df,
    *,
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895786268843e4dc61577d5aabe884d5889c9e09d0dc4e45340bf550c60e98f3(
    id: builtins.str,
    target: _INotificationRuleTarget_31f512df,
    *,
    events: typing.Sequence[RepositoryNotificationEvents],
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2712084918cf295073c479053a4b783816a994249fc93e5f4b4d74299b9fdb3(
    id: builtins.str,
    target: _INotificationRuleTarget_31f512df,
    *,
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55430598a11091e6e5d302f707e88f16c513158c06f448a95f5571882271b8e9(
    id: builtins.str,
    target: _INotificationRuleTarget_31f512df,
    *,
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df66651c740f53e5625a122eb24397c7230a745d49aa891308a9e602cce35a09(
    id: builtins.str,
    target: _INotificationRuleTarget_31f512df,
    *,
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a489769acab158057a35e66cf3e6c6e4c00c8928bafcb2721b811428859ac5(
    id: builtins.str,
    target: _INotificationRuleTarget_31f512df,
    *,
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19cedd9ad64701ea0e5b6e03de6da7dee39df720624bec2b0a7979d75c009951(
    id: builtins.str,
    target: _INotificationRuleTarget_31f512df,
    *,
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415ef28018465177c719dba45064a51e2b7877ecf8f248213c22661bf1199f7e(
    id: builtins.str,
    target: _INotificationRuleTarget_31f512df,
    *,
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66af67f59190aa64b6129dd91545ce52bd770d7f89cf297a27d0aaad57c0f504(
    id: builtins.str,
    target: _INotificationRuleTarget_31f512df,
    *,
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c222bbaf7d9edaad6612bb791190b6270de2de32b7f6094648ec1b8ff3f5109(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ed90364a91822929d8f6dbf50eacacb1dd1beceaf2ac0b73fd637245b230e9(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa148a1e5590e4a415483930d161f416df5a0d0e337be07df0f32b48104fdf66(
    id: builtins.str,
    *,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d120edae194b90e2a80f7af14430f27827dced063b24e7c8123fe0a188b9096(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5bb8df110c27d751752311b21db4ff247eef97bb38c97acac49c6a3411ac95(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4835ede748cc9b59e7c07e1f2d55eb3f378eea8ce3d9c59168c9e467c3b78b5e(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9cf32afd45ba378d4b579b1fb2084afbb03afccb16ef74d5db4f05e5792ae7(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb3b93164a720f5d36e6423cd2d64cc0e0865b023cf5404369982e1f1dd5b06(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00778a902217726a81ff27f476d3c711842ed9a5505aa303dd3eadbbca39908c(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b99e70e05908e0b867feec6d72921264aeb152c1bb5b874fec8ef3ca8c59bb3(
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b702110160741503b9effcbfd9c051c8c729fd31b130fb7bdb78ff438978f8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    repository_name: builtins.str,
    code: typing.Optional[Code] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441ff7aa7d7085d3b4aa8a61ea92744b1f222f0193a619c2d040cdf0f4ba7b7d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    repository_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765246864edff89547cacd11109965bc8ee740241f64c20bad75ce8e00a437ce(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    repository_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae75e12836ae0459cc9ca43abd5f7d8fc62898ed4c8ab76200a3bdcd5d0448e(
    _scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0711effefea0a53fa7cbbc7c433ecf56b484767ee8c5d0771604fbabcd82a43b(
    grantee: _IGrantable_4c5a91d1,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d15c9fca5739262c65a2fe8cb883b7aee2819b762237c1396f9c5115274f399(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056cd07322b8dfafdcca44fe34cc77f40ff2d615a1a7b364b1c47d73abbb4247(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e617b08ed6b867571778b8b5fb9e9683a474eef17435d0a91344cba5f0a7fd8(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c429c9c889235d6540654cdbb73c5065882dd297d8855deadee14acaed3f6f(
    id: builtins.str,
    target: _INotificationRuleTarget_31f512df,
    *,
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b92f05ebac3742cefbfcb3cef3fa4e8cf55eab719c14ccbc4674509c7956127(
    arn: builtins.str,
    *,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_data: typing.Optional[builtins.str] = None,
    events: typing.Optional[typing.Sequence[RepositoryEventTrigger]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e45a0fb1fe80dbce55cc4a7a756c8ad319cbf2f424126fe57041de9a8457d4(
    id: builtins.str,
    target: _INotificationRuleTarget_31f512df,
    *,
    events: typing.Sequence[RepositoryNotificationEvents],
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3baece54499f81167fa8c66847ff77e7dbec0ca657de100221ca982bcb9794f(
    id: builtins.str,
    target: _INotificationRuleTarget_31f512df,
    *,
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b18ae82af152694e517a6074c97ebb59d73c6e8e3d56879c1d40a79da5fe931(
    id: builtins.str,
    target: _INotificationRuleTarget_31f512df,
    *,
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac8e3677bec422cfc130e3c9df1f99139fab001792183e3c7f6a78d62d0863fb(
    id: builtins.str,
    target: _INotificationRuleTarget_31f512df,
    *,
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a58ec02341a5eccad3e7f7c6224b0b44b3a93232882f08ed9cc863610d0eab2(
    id: builtins.str,
    target: _INotificationRuleTarget_31f512df,
    *,
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c825c1bc19eb7b66e833e954e68237a9016091fb996a5a5e978ed62643affd5e(
    id: builtins.str,
    target: _INotificationRuleTarget_31f512df,
    *,
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6031d863d03a31f78adbc2bcf252e1c00f1e8ef84f5e8a66e3bdfe63dab042(
    id: builtins.str,
    target: _INotificationRuleTarget_31f512df,
    *,
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f312b36168f77a4b8e7f2e3260b07b61fa8fe1c762211c4e5d5f177ccc78bada(
    id: builtins.str,
    target: _INotificationRuleTarget_31f512df,
    *,
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e398919e437dcb2792b256e666ccf8506ebbb277cfc8f2617ec1195141a077(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c692cff4290ae8eab9eeab58c024a8a518f43df14e895f8ad4d047e93dd4359(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e62fe5d2cbdb235a45fbcbdb37b7f68a4c9a1cd9721f87fc717cf2168912985(
    id: builtins.str,
    *,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c653bc8df5da90bf8bde8cb0e984d885950c98dabbc9f21ecc4b5b7056e07921(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40289a89949d9bb1a0583d26b86206c78f22fbf6d49a4d479ed8dd8db6601754(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aba71a293de533d43b9303a3845ef7673f90a5e4df14ca39cb92a3f2b667866(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f241da44db7ed952910cc114ac9604aa42abc3bafd1b353ab4c55a04839880(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc55d51c35ce0db927ba2d521b9c6d55ea6e112637c5be6514651f7423a3788a(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b075258fbc00f67aa9ec7f42c7423bb3e45ec6e2227cc08037861d8960b7d797(
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b08d3ebffafc9f7f2ec129ddca33b44c47f8a9118d20518f2690f25e18c8ebb(
    *,
    detail_type: typing.Optional[_DetailType_50204ab4] = None,
    enabled: typing.Optional[builtins.bool] = None,
    notification_rule_name: typing.Optional[builtins.str] = None,
    events: typing.Sequence[RepositoryNotificationEvents],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04d07c2ffdb287154d3fa06b9de216b06015dda3f1870c60848c83c94c982cc(
    *,
    repository_name: builtins.str,
    code: typing.Optional[Code] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297c4cea56ab32a05c65812129d9862d9dd382ee822f154e088c13735dbb444d(
    *,
    branches: typing.Optional[typing.Sequence[builtins.str]] = None,
    custom_data: typing.Optional[builtins.str] = None,
    events: typing.Optional[typing.Sequence[RepositoryEventTrigger]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
