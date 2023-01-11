'''
# AWS::OpenSearchServerless Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as opensearchserverless
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for OpenSearchServerless construct libraries](https://constructs.dev/search?q=opensearchserverless)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::OpenSearchServerless resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_OpenSearchServerless.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::OpenSearchServerless](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_OpenSearchServerless.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
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

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnAccessPolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_opensearchserverless.CfnAccessPolicy",
):
    '''A CloudFormation ``AWS::OpenSearchServerless::AccessPolicy``.

    Creates a data access policy for OpenSearch Serverless. Access policies limit access to collections and the resources within them, and allow a user to access that data irrespective of the access mechanism or network source. For more information, see `Data access control for Amazon OpenSearch Serverless <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-data-access.html>`_ .

    :cloudformationResource: AWS::OpenSearchServerless::AccessPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-accesspolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_opensearchserverless as opensearchserverless
        
        cfn_access_policy = opensearchserverless.CfnAccessPolicy(self, "MyCfnAccessPolicy",
            description="description",
            name="name",
            policy="policy",
            type="type"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::OpenSearchServerless::AccessPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: The description of the policy.
        :param name: The name of the policy.
        :param policy: The JSON policy document without any whitespaces.
        :param type: The type of access policy. Currently the only option is ``data`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27a367a6312a43a7616c08444a9311625136a1e385d41542e81c0dbd7ff33f60)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAccessPolicyProps(
            description=description, name=name, policy=policy, type=type
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2df93156faacb191b54dbae2a83e0b027ad6bfbaeee9493d535d1bba000071)
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
            type_hints = typing.get_type_hints(_typecheckingstub__387f926baef02a52ef5d7682b70c074de0d08caef9f01c7a1b6507d681addced)
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
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-accesspolicy.html#cfn-opensearchserverless-accesspolicy-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__841dc7debaafa3c6cd44bd5fcc77b2bfc5ddb471adb6b1625e2c3ac2fcc5c1bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-accesspolicy.html#cfn-opensearchserverless-accesspolicy-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29e28f48e0475aa9d14bcc788751403310b305122ce76bdfbf03808d21ae808a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional[builtins.str]:
        '''The JSON policy document without any whitespaces.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-accesspolicy.html#cfn-opensearchserverless-accesspolicy-policy
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f09b5a81720b4f5b1f7e09bd8c0a4c27093054b58b00600f1c1e4bbc48f73948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of access policy.

        Currently the only option is ``data`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-accesspolicy.html#cfn-opensearchserverless-accesspolicy-type
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da96826508d1dbd5fb33fd0d339579deb0e83010de0403a6d354890a45751183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="monocdk.aws_opensearchserverless.CfnAccessPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "policy": "policy",
        "type": "type",
    },
)
class CfnAccessPolicyProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAccessPolicy``.

        :param description: The description of the policy.
        :param name: The name of the policy.
        :param policy: The JSON policy document without any whitespaces.
        :param type: The type of access policy. Currently the only option is ``data`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-accesspolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_opensearchserverless as opensearchserverless
            
            cfn_access_policy_props = opensearchserverless.CfnAccessPolicyProps(
                description="description",
                name="name",
                policy="policy",
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3be9b20c3b2a883cd552d08a73e1ad422aa3bd803caef2fa86547ceaf0b524)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if policy is not None:
            self._values["policy"] = policy
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-accesspolicy.html#cfn-opensearchserverless-accesspolicy-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-accesspolicy.html#cfn-opensearchserverless-accesspolicy-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''The JSON policy document without any whitespaces.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-accesspolicy.html#cfn-opensearchserverless-accesspolicy-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of access policy.

        Currently the only option is ``data`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-accesspolicy.html#cfn-opensearchserverless-accesspolicy-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnCollection(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_opensearchserverless.CfnCollection",
):
    '''A CloudFormation ``AWS::OpenSearchServerless::Collection``.

    Specifies an OpenSearch Serverless collection. For more information, see `Creating and managing Amazon OpenSearch Serverless collections <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-manage.html>`_ in the *Amazon OpenSearch Service Developer Guide* .
    .. epigraph::

       You must create a matching `encryption policy <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-encryption.html>`_ in order for a collection to be created successfully. You can specify the policy resource within the same CloudFormation template as the collection resource if you use the `DependsOn <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html>`_ attribute. See `Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html#aws-resource-opensearchserverless-collection--examples>`_ for a sample template. Otherwise the encryption policy must already exist before you create the collection.

    :cloudformationResource: AWS::OpenSearchServerless::Collection
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_opensearchserverless as opensearchserverless
        
        cfn_collection = opensearchserverless.CfnCollection(self, "MyCfnCollection",
            name="name",
        
            # the properties below are optional
            description="description",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::OpenSearchServerless::Collection``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the collection. Collection names must meet the following criteria: - Starts with a lowercase letter - Unique to your account and AWS Region - Contains between 3 and 28 characters - Contains only lowercase letters a-z, the numbers 0-9, and the hyphen (-)
        :param description: A description of the collection.
        :param tags: An arbitrary set of tags (key–value pairs) to associate with the collection. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param type: The type of collection. Possible values are ``SEARCH`` and ``TIMESERIES`` . For more information, see `Choosing a collection type <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-overview.html#serverless-usecase>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a2c115b24965b6400bca796ac908dd7f08c320ad90e0b6ab3a8c6d20faec90)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCollectionProps(
            name=name, description=description, tags=tags, type=type
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52a0e5549e3ae211a5a752e7aed2fadd2cb6176483d477775ea91308c9bdd9ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3daf910d7176eca6731bcffb4e5b51adfc2acfbaba873575376f2f29a3472eed)
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
        '''The Amazon Resource Name (ARN) of the collection.

        For example, ``arn:aws:aoss:us-east-1:123456789012:collection/07tjusf2h91cunochc`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCollectionEndpoint")
    def attr_collection_endpoint(self) -> builtins.str:
        '''Collection-specific endpoint used to submit index, search, and data upload requests to an OpenSearch Serverless collection.

        For example, ``https://07tjusf2h91cunochc.us-east-1.aoss.amazonaws.com`` .

        :cloudformationAttribute: CollectionEndpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCollectionEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="attrDashboardEndpoint")
    def attr_dashboard_endpoint(self) -> builtins.str:
        '''Collection-specific endpoint used to access OpenSearch Dashboards.

        For example, ``https://07tjusf2h91cunochc.us-east-1.aoss.amazonaws.com/_dashboards`` .

        :cloudformationAttribute: DashboardEndpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDashboardEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''A unique identifier for the collection.

        For example, ``07tjusf2h91cunochc`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''An arbitrary set of tags (key–value pairs) to associate with the collection.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html#cfn-opensearchserverless-collection-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the collection.

        Collection names must meet the following criteria:

        - Starts with a lowercase letter
        - Unique to your account and AWS Region
        - Contains between 3 and 28 characters
        - Contains only lowercase letters a-z, the numbers 0-9, and the hyphen (-)

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html#cfn-opensearchserverless-collection-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e926880265dfbe0263d37a65cf95dd7f19894e0b3a9f662ebfbfe56d30b9247)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the collection.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html#cfn-opensearchserverless-collection-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e648a9793b1e512660d3ee849b5be008547c3027f009fe63c3b2ad2c88b96c51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of collection.

        Possible values are ``SEARCH`` and ``TIMESERIES`` . For more information, see `Choosing a collection type <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-overview.html#serverless-usecase>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html#cfn-opensearchserverless-collection-type
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d0963f4e622826af60da3c785183ea9324602c7127f875bc83dcf4b3742a449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="monocdk.aws_opensearchserverless.CfnCollectionProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "tags": "tags",
        "type": "type",
    },
)
class CfnCollectionProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnCollection``.

        :param name: The name of the collection. Collection names must meet the following criteria: - Starts with a lowercase letter - Unique to your account and AWS Region - Contains between 3 and 28 characters - Contains only lowercase letters a-z, the numbers 0-9, and the hyphen (-)
        :param description: A description of the collection.
        :param tags: An arbitrary set of tags (key–value pairs) to associate with the collection. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param type: The type of collection. Possible values are ``SEARCH`` and ``TIMESERIES`` . For more information, see `Choosing a collection type <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-overview.html#serverless-usecase>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_opensearchserverless as opensearchserverless
            
            cfn_collection_props = opensearchserverless.CfnCollectionProps(
                name="name",
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57cf850fdbb9c8d47d5625e4e21ee039efdbf7a2131eb39e91f7cb3fb2fc9dda)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the collection.

        Collection names must meet the following criteria:

        - Starts with a lowercase letter
        - Unique to your account and AWS Region
        - Contains between 3 and 28 characters
        - Contains only lowercase letters a-z, the numbers 0-9, and the hyphen (-)

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html#cfn-opensearchserverless-collection-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the collection.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html#cfn-opensearchserverless-collection-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An arbitrary set of tags (key–value pairs) to associate with the collection.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html#cfn-opensearchserverless-collection-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of collection.

        Possible values are ``SEARCH`` and ``TIMESERIES`` . For more information, see `Choosing a collection type <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-overview.html#serverless-usecase>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html#cfn-opensearchserverless-collection-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCollectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSecurityConfig(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_opensearchserverless.CfnSecurityConfig",
):
    '''A CloudFormation ``AWS::OpenSearchServerless::SecurityConfig``.

    Specifies a security configuration for OpenSearch Serverless. For more information, see `SAML authentication for Amazon OpenSearch Serverless <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-saml.html>`_ .

    :cloudformationResource: AWS::OpenSearchServerless::SecurityConfig
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_opensearchserverless as opensearchserverless
        
        cfn_security_config = opensearchserverless.CfnSecurityConfig(self, "MyCfnSecurityConfig",
            description="description",
            name="name",
            saml_options=opensearchserverless.CfnSecurityConfig.SamlConfigOptionsProperty(
                metadata="metadata",
        
                # the properties below are optional
                group_attribute="groupAttribute",
                session_timeout=123,
                user_attribute="userAttribute"
            ),
            type="type"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        saml_options: typing.Optional[typing.Union[typing.Union["CfnSecurityConfig.SamlConfigOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::OpenSearchServerless::SecurityConfig``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: The description of the security configuration.
        :param name: The name of the security configuration.
        :param saml_options: SAML options for the security configuration in the form of a key-value map.
        :param type: The type of security configuration. Currently the only option is ``saml`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b024fbc2402d421ba676f29bc9ab8584b713140c9e5fb428ccb830adadc204)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSecurityConfigProps(
            description=description, name=name, saml_options=saml_options, type=type
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5795914c95f2e7d38fb9bd17d7c60916c3b7cfefa3cd967a49017c7b1757681)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37033d377c0fd95ce098010a6144472bf3345b4e9c36921c1e2e81f3c4ea51b1)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The unique identifier of the security configuration.

        For example, ``saml/123456789012/myprovider`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the security configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html#cfn-opensearchserverless-securityconfig-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e3d85d9803af71337da86798bf596c9e7f7f09eecd201469275dbf7f0ebeaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the security configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html#cfn-opensearchserverless-securityconfig-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4362b66ad7a13679057a51292215964d004d2cf6918122fef99dbba6b885fc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="samlOptions")
    def saml_options(
        self,
    ) -> typing.Optional[typing.Union["CfnSecurityConfig.SamlConfigOptionsProperty", _IResolvable_a771d0ef]]:
        '''SAML options for the security configuration in the form of a key-value map.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html#cfn-opensearchserverless-securityconfig-samloptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnSecurityConfig.SamlConfigOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "samlOptions"))

    @saml_options.setter
    def saml_options(
        self,
        value: typing.Optional[typing.Union["CfnSecurityConfig.SamlConfigOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f489569af2f787c0a732b8639fdbfcdc796d09083d453bbe7f8d2203d56fb288)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samlOptions", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of security configuration.

        Currently the only option is ``saml`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html#cfn-opensearchserverless-securityconfig-type
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6ba9b88cd1fdafd23a8c47cf8674c1429dc4fba25321c7fa97914bfadb79bb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_opensearchserverless.CfnSecurityConfig.SamlConfigOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metadata": "metadata",
            "group_attribute": "groupAttribute",
            "session_timeout": "sessionTimeout",
            "user_attribute": "userAttribute",
        },
    )
    class SamlConfigOptionsProperty:
        def __init__(
            self,
            *,
            metadata: builtins.str,
            group_attribute: typing.Optional[builtins.str] = None,
            session_timeout: typing.Optional[jsii.Number] = None,
            user_attribute: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes SAML options for an OpenSearch Serverless security configuration in the form of a key-value map.

            :param metadata: The XML IdP metadata file generated from your identity provider.
            :param group_attribute: The group attribute for this SAML integration.
            :param session_timeout: The session timeout, in minutes. Minimum is 15 minutes and maximum is 1440 minutes (24 hours or 1 day). Default is 60 minutes.
            :param user_attribute: A user attribute for this SAML integration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-samlconfigoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_opensearchserverless as opensearchserverless
                
                saml_config_options_property = opensearchserverless.CfnSecurityConfig.SamlConfigOptionsProperty(
                    metadata="metadata",
                
                    # the properties below are optional
                    group_attribute="groupAttribute",
                    session_timeout=123,
                    user_attribute="userAttribute"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c55480e2ea627b8d00c75b03950e637aa77cbb77f293710cd4f853f09a672972)
                check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
                check_type(argname="argument group_attribute", value=group_attribute, expected_type=type_hints["group_attribute"])
                check_type(argname="argument session_timeout", value=session_timeout, expected_type=type_hints["session_timeout"])
                check_type(argname="argument user_attribute", value=user_attribute, expected_type=type_hints["user_attribute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "metadata": metadata,
            }
            if group_attribute is not None:
                self._values["group_attribute"] = group_attribute
            if session_timeout is not None:
                self._values["session_timeout"] = session_timeout
            if user_attribute is not None:
                self._values["user_attribute"] = user_attribute

        @builtins.property
        def metadata(self) -> builtins.str:
            '''The XML IdP metadata file generated from your identity provider.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-samlconfigoptions.html#cfn-opensearchserverless-securityconfig-samlconfigoptions-metadata
            '''
            result = self._values.get("metadata")
            assert result is not None, "Required property 'metadata' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def group_attribute(self) -> typing.Optional[builtins.str]:
            '''The group attribute for this SAML integration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-samlconfigoptions.html#cfn-opensearchserverless-securityconfig-samlconfigoptions-groupattribute
            '''
            result = self._values.get("group_attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_timeout(self) -> typing.Optional[jsii.Number]:
            '''The session timeout, in minutes.

            Minimum is 15 minutes and maximum is 1440 minutes (24 hours or 1 day). Default is 60 minutes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-samlconfigoptions.html#cfn-opensearchserverless-securityconfig-samlconfigoptions-sessiontimeout
            '''
            result = self._values.get("session_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def user_attribute(self) -> typing.Optional[builtins.str]:
            '''A user attribute for this SAML integration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-opensearchserverless-securityconfig-samlconfigoptions.html#cfn-opensearchserverless-securityconfig-samlconfigoptions-userattribute
            '''
            result = self._values.get("user_attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SamlConfigOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_opensearchserverless.CfnSecurityConfigProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "saml_options": "samlOptions",
        "type": "type",
    },
)
class CfnSecurityConfigProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        saml_options: typing.Optional[typing.Union[typing.Union[CfnSecurityConfig.SamlConfigOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSecurityConfig``.

        :param description: The description of the security configuration.
        :param name: The name of the security configuration.
        :param saml_options: SAML options for the security configuration in the form of a key-value map.
        :param type: The type of security configuration. Currently the only option is ``saml`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_opensearchserverless as opensearchserverless
            
            cfn_security_config_props = opensearchserverless.CfnSecurityConfigProps(
                description="description",
                name="name",
                saml_options=opensearchserverless.CfnSecurityConfig.SamlConfigOptionsProperty(
                    metadata="metadata",
            
                    # the properties below are optional
                    group_attribute="groupAttribute",
                    session_timeout=123,
                    user_attribute="userAttribute"
                ),
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3d73abfb4916a8d896b85ad5c6a6937b6bcdf4e7df30eafdc1a8bc175afa043)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument saml_options", value=saml_options, expected_type=type_hints["saml_options"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if saml_options is not None:
            self._values["saml_options"] = saml_options
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the security configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html#cfn-opensearchserverless-securityconfig-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the security configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html#cfn-opensearchserverless-securityconfig-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml_options(
        self,
    ) -> typing.Optional[typing.Union[CfnSecurityConfig.SamlConfigOptionsProperty, _IResolvable_a771d0ef]]:
        '''SAML options for the security configuration in the form of a key-value map.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html#cfn-opensearchserverless-securityconfig-samloptions
        '''
        result = self._values.get("saml_options")
        return typing.cast(typing.Optional[typing.Union[CfnSecurityConfig.SamlConfigOptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of security configuration.

        Currently the only option is ``saml`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html#cfn-opensearchserverless-securityconfig-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecurityConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSecurityPolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_opensearchserverless.CfnSecurityPolicy",
):
    '''A CloudFormation ``AWS::OpenSearchServerless::SecurityPolicy``.

    Creates an encryption or network policy to be used by one or more OpenSearch Serverless collections.

    Network policies specify access to a collection and its OpenSearch Dashboards endpoint from public networks or specific VPC endpoints. For more information, see `Network access for Amazon OpenSearch Serverless <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-network.html>`_ .

    Encryption policies specify a KMS encryption key to assign to particular collections. For more information, see `Encryption at rest for Amazon OpenSearch Serverless <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-encryption.html>`_ .

    :cloudformationResource: AWS::OpenSearchServerless::SecurityPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securitypolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_opensearchserverless as opensearchserverless
        
        cfn_security_policy = opensearchserverless.CfnSecurityPolicy(self, "MyCfnSecurityPolicy",
            policy="policy",
        
            # the properties below are optional
            description="description",
            name="name",
            type="type"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        policy: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::OpenSearchServerless::SecurityPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy: The JSON policy document without any whitespaces.
        :param description: The description of the security policy.
        :param name: The name of the policy.
        :param type: The type of security policy. Can be either ``encryption`` or ``network`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3fc7ebab5ca7ea441076b84402dad4edc6f038ab679427460c4a5fae1fd3e7d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSecurityPolicyProps(
            policy=policy, description=description, name=name, type=type
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b6a9ef50ac948f78c7a8ce8a0fa8e30a2bf5d68c72580c51a26e5f4f75d6250)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00007d4b6e47300462a6cde371f3aa291c03272f8073e79f34c08e0e7d5e8175)
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
    @jsii.member(jsii_name="policy")
    def policy(self) -> builtins.str:
        '''The JSON policy document without any whitespaces.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securitypolicy.html#cfn-opensearchserverless-securitypolicy-policy
        '''
        return typing.cast(builtins.str, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fff6cb2ec86cd9c1ceeea15954eabb2210851b86222051186cb03ee9f0f71fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the security policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securitypolicy.html#cfn-opensearchserverless-securitypolicy-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72323f45a1a80458213c526e1e3bfe871e72979cd121ccd7a0b54b1b01dea8b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securitypolicy.html#cfn-opensearchserverless-securitypolicy-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eaea7e6368a62178b0c967e3d08150c2c21bc3cc6ec5ecd3178a002b910e04a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of security policy.

        Can be either ``encryption`` or ``network`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securitypolicy.html#cfn-opensearchserverless-securitypolicy-type
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff62259a466638ac15d89527514b00a25c35cd2cbf4d9dc073bca64226b7f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="monocdk.aws_opensearchserverless.CfnSecurityPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy": "policy",
        "description": "description",
        "name": "name",
        "type": "type",
    },
)
class CfnSecurityPolicyProps:
    def __init__(
        self,
        *,
        policy: builtins.str,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSecurityPolicy``.

        :param policy: The JSON policy document without any whitespaces.
        :param description: The description of the security policy.
        :param name: The name of the policy.
        :param type: The type of security policy. Can be either ``encryption`` or ``network`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securitypolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_opensearchserverless as opensearchserverless
            
            cfn_security_policy_props = opensearchserverless.CfnSecurityPolicyProps(
                policy="policy",
            
                # the properties below are optional
                description="description",
                name="name",
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f98b36d1cabf4fdb1928bfdaf08919c838bb64be0f04e3b8e0ec27d3761864d)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy": policy,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def policy(self) -> builtins.str:
        '''The JSON policy document without any whitespaces.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securitypolicy.html#cfn-opensearchserverless-securitypolicy-policy
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the security policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securitypolicy.html#cfn-opensearchserverless-securitypolicy-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securitypolicy.html#cfn-opensearchserverless-securitypolicy-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of security policy.

        Can be either ``encryption`` or ``network`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securitypolicy.html#cfn-opensearchserverless-securitypolicy-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecurityPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnVpcEndpoint(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_opensearchserverless.CfnVpcEndpoint",
):
    '''A CloudFormation ``AWS::OpenSearchServerless::VpcEndpoint``.

    Creates an OpenSearch Serverless-managed interface VPC endpoint. For more information, see `Access Amazon OpenSearch Serverless using an interface endpoint <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-vpc.html>`_ .

    :cloudformationResource: AWS::OpenSearchServerless::VpcEndpoint
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-vpcendpoint.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_opensearchserverless as opensearchserverless
        
        cfn_vpc_endpoint = opensearchserverless.CfnVpcEndpoint(self, "MyCfnVpcEndpoint",
            name="name",
            vpc_id="vpcId",
        
            # the properties below are optional
            security_group_ids=["securityGroupIds"],
            subnet_ids=["subnetIds"]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: builtins.str,
        vpc_id: builtins.str,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::OpenSearchServerless::VpcEndpoint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the endpoint.
        :param vpc_id: The ID of the VPC from which you access OpenSearch Serverless.
        :param security_group_ids: The unique identifiers of the security groups that define the ports, protocols, and sources for inbound traffic that you are authorizing into your endpoint.
        :param subnet_ids: The ID of the subnets from which you access OpenSearch Serverless.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56ed57a1526740c8a2bb96b05afcc84f82eec756a31cbfeafe80b1922a6139d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnVpcEndpointProps(
            name=name,
            vpc_id=vpc_id,
            security_group_ids=security_group_ids,
            subnet_ids=subnet_ids,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__431eeb3bcfe1dac6b534254889d8c0b8815224f2b48f69b9eabbf73b3d63659e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ae795aaf8077ca5d319aff5f307ef9648b3a24d27aef900c1a35f1ea4f6ad5e)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The unique identifier of the endpoint.

        For example, ``vpce-050f79086ee71ac05`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-vpcendpoint.html#cfn-opensearchserverless-vpcendpoint-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f178e6a6a18437d09af324b9bc3d1ac11530ec8df302b042aab25888c62dc84c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        '''The ID of the VPC from which you access OpenSearch Serverless.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-vpcendpoint.html#cfn-opensearchserverless-vpcendpoint-vpcid
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35328f8f764f066a986436fae7fd35cdfadc6d0b540bb2619fc647b346608cad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The unique identifiers of the security groups that define the ports, protocols, and sources for inbound traffic that you are authorizing into your endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-vpcendpoint.html#cfn-opensearchserverless-vpcendpoint-securitygroupids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08cfa981ba67e496b9e6b3cc08c3756c6d15650c10a4fbaded81d7114e08973a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ID of the subnets from which you access OpenSearch Serverless.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-vpcendpoint.html#cfn-opensearchserverless-vpcendpoint-subnetids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c56e13ae4ca0b6f97d75ad3b80f5eaeca12bf7b70d8eef9c43b90a78a57478be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value)


@jsii.data_type(
    jsii_type="monocdk.aws_opensearchserverless.CfnVpcEndpointProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "vpc_id": "vpcId",
        "security_group_ids": "securityGroupIds",
        "subnet_ids": "subnetIds",
    },
)
class CfnVpcEndpointProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        vpc_id: builtins.str,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnVpcEndpoint``.

        :param name: The name of the endpoint.
        :param vpc_id: The ID of the VPC from which you access OpenSearch Serverless.
        :param security_group_ids: The unique identifiers of the security groups that define the ports, protocols, and sources for inbound traffic that you are authorizing into your endpoint.
        :param subnet_ids: The ID of the subnets from which you access OpenSearch Serverless.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-vpcendpoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_opensearchserverless as opensearchserverless
            
            cfn_vpc_endpoint_props = opensearchserverless.CfnVpcEndpointProps(
                name="name",
                vpc_id="vpcId",
            
                # the properties below are optional
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604052620a3f43b74733e45c0876431249bb8808a1d87d95267107ac6f15826b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "vpc_id": vpc_id,
        }
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-vpcendpoint.html#cfn-opensearchserverless-vpcendpoint-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''The ID of the VPC from which you access OpenSearch Serverless.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-vpcendpoint.html#cfn-opensearchserverless-vpcendpoint-vpcid
        '''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The unique identifiers of the security groups that define the ports, protocols, and sources for inbound traffic that you are authorizing into your endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-vpcendpoint.html#cfn-opensearchserverless-vpcendpoint-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ID of the subnets from which you access OpenSearch Serverless.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-vpcendpoint.html#cfn-opensearchserverless-vpcendpoint-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVpcEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAccessPolicy",
    "CfnAccessPolicyProps",
    "CfnCollection",
    "CfnCollectionProps",
    "CfnSecurityConfig",
    "CfnSecurityConfigProps",
    "CfnSecurityPolicy",
    "CfnSecurityPolicyProps",
    "CfnVpcEndpoint",
    "CfnVpcEndpointProps",
]

publication.publish()

def _typecheckingstub__27a367a6312a43a7616c08444a9311625136a1e385d41542e81c0dbd7ff33f60(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2df93156faacb191b54dbae2a83e0b027ad6bfbaeee9493d535d1bba000071(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__387f926baef02a52ef5d7682b70c074de0d08caef9f01c7a1b6507d681addced(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841dc7debaafa3c6cd44bd5fcc77b2bfc5ddb471adb6b1625e2c3ac2fcc5c1bd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e28f48e0475aa9d14bcc788751403310b305122ce76bdfbf03808d21ae808a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f09b5a81720b4f5b1f7e09bd8c0a4c27093054b58b00600f1c1e4bbc48f73948(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da96826508d1dbd5fb33fd0d339579deb0e83010de0403a6d354890a45751183(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3be9b20c3b2a883cd552d08a73e1ad422aa3bd803caef2fa86547ceaf0b524(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a2c115b24965b6400bca796ac908dd7f08c320ad90e0b6ab3a8c6d20faec90(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a0e5549e3ae211a5a752e7aed2fadd2cb6176483d477775ea91308c9bdd9ff(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3daf910d7176eca6731bcffb4e5b51adfc2acfbaba873575376f2f29a3472eed(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e926880265dfbe0263d37a65cf95dd7f19894e0b3a9f662ebfbfe56d30b9247(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e648a9793b1e512660d3ee849b5be008547c3027f009fe63c3b2ad2c88b96c51(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d0963f4e622826af60da3c785183ea9324602c7127f875bc83dcf4b3742a449(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57cf850fdbb9c8d47d5625e4e21ee039efdbf7a2131eb39e91f7cb3fb2fc9dda(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b024fbc2402d421ba676f29bc9ab8584b713140c9e5fb428ccb830adadc204(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    saml_options: typing.Optional[typing.Union[typing.Union[CfnSecurityConfig.SamlConfigOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5795914c95f2e7d38fb9bd17d7c60916c3b7cfefa3cd967a49017c7b1757681(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37033d377c0fd95ce098010a6144472bf3345b4e9c36921c1e2e81f3c4ea51b1(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e3d85d9803af71337da86798bf596c9e7f7f09eecd201469275dbf7f0ebeaf(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4362b66ad7a13679057a51292215964d004d2cf6918122fef99dbba6b885fc2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f489569af2f787c0a732b8639fdbfcdc796d09083d453bbe7f8d2203d56fb288(
    value: typing.Optional[typing.Union[CfnSecurityConfig.SamlConfigOptionsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6ba9b88cd1fdafd23a8c47cf8674c1429dc4fba25321c7fa97914bfadb79bb1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55480e2ea627b8d00c75b03950e637aa77cbb77f293710cd4f853f09a672972(
    *,
    metadata: builtins.str,
    group_attribute: typing.Optional[builtins.str] = None,
    session_timeout: typing.Optional[jsii.Number] = None,
    user_attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d73abfb4916a8d896b85ad5c6a6937b6bcdf4e7df30eafdc1a8bc175afa043(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    saml_options: typing.Optional[typing.Union[typing.Union[CfnSecurityConfig.SamlConfigOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3fc7ebab5ca7ea441076b84402dad4edc6f038ab679427460c4a5fae1fd3e7d(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    policy: builtins.str,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b6a9ef50ac948f78c7a8ce8a0fa8e30a2bf5d68c72580c51a26e5f4f75d6250(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00007d4b6e47300462a6cde371f3aa291c03272f8073e79f34c08e0e7d5e8175(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fff6cb2ec86cd9c1ceeea15954eabb2210851b86222051186cb03ee9f0f71fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72323f45a1a80458213c526e1e3bfe871e72979cd121ccd7a0b54b1b01dea8b8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eaea7e6368a62178b0c967e3d08150c2c21bc3cc6ec5ecd3178a002b910e04a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff62259a466638ac15d89527514b00a25c35cd2cbf4d9dc073bca64226b7f38(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f98b36d1cabf4fdb1928bfdaf08919c838bb64be0f04e3b8e0ec27d3761864d(
    *,
    policy: builtins.str,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56ed57a1526740c8a2bb96b05afcc84f82eec756a31cbfeafe80b1922a6139d(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    vpc_id: builtins.str,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431eeb3bcfe1dac6b534254889d8c0b8815224f2b48f69b9eabbf73b3d63659e(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae795aaf8077ca5d319aff5f307ef9648b3a24d27aef900c1a35f1ea4f6ad5e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f178e6a6a18437d09af324b9bc3d1ac11530ec8df302b042aab25888c62dc84c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35328f8f764f066a986436fae7fd35cdfadc6d0b540bb2619fc647b346608cad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08cfa981ba67e496b9e6b3cc08c3756c6d15650c10a4fbaded81d7114e08973a(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c56e13ae4ca0b6f97d75ad3b80f5eaeca12bf7b70d8eef9c43b90a78a57478be(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604052620a3f43b74733e45c0876431249bb8808a1d87d95267107ac6f15826b(
    *,
    name: builtins.str,
    vpc_id: builtins.str,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
