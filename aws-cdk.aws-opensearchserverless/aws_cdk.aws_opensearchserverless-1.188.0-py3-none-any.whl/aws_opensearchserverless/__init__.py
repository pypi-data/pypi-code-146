'''
# AWS::OpenSearchServerless Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_opensearchserverless as opensearchserverless
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

from ._jsii import *

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnAccessPolicy(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-opensearchserverless.CfnAccessPolicy",
):
    '''A CloudFormation ``AWS::OpenSearchServerless::AccessPolicy``.

    Creates a data access policy for OpenSearch Serverless. Access policies limit access to collections and the resources within them, and allow a user to access that data irrespective of the access mechanism or network source. For more information, see `Data access control for Amazon OpenSearch Serverless <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-data-access.html>`_ .

    :cloudformationResource: AWS::OpenSearchServerless::AccessPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-accesspolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_opensearchserverless as opensearchserverless
        
        cfn_access_policy = opensearchserverless.CfnAccessPolicy(self, "MyCfnAccessPolicy",
            description="description",
            name="name",
            policy="policy",
            type="type"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3bd28bec90cad86bc80879c08bebf9324f3edc04aa11566dc4d2b8d96b915d4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAccessPolicyProps(
            description=description, name=name, policy=policy, type=type
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a99229ef3ae2c403369fe2860de91587ed47b17f8fad592a599ff67d5f73b3c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2be31657476e7e37465511d82341bcbf174b678c1880d08622ddf7068fed64e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed7dd3c3cbc0234b0646b96e589a4178588cbb018a321d6f33f9c9c68dea8142)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3632e35022c7cd34bc79a0125a8954d850c17a33c2fa8970b320c5859a124cc3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d73baf636fb2987b68313f33646f63952cd321e915630c6a6b23680151828005)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd2d703f54d40690465ae00ad61788667c0f743d35277ef6ea3621497f56bd57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opensearchserverless.CfnAccessPolicyProps",
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
            import aws_cdk.aws_opensearchserverless as opensearchserverless
            
            cfn_access_policy_props = opensearchserverless.CfnAccessPolicyProps(
                description="description",
                name="name",
                policy="policy",
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__111ac1327affb42b1d3ecb402d74e3ecbe665b77152d65bf1cb7b000c053b8e6)
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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnCollection(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-opensearchserverless.CfnCollection",
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
        import aws_cdk.aws_opensearchserverless as opensearchserverless
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__e272b7938d2b0d54d4e596ef62a23a84d7dd108c0e3a69624556aa96a9ab7716)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCollectionProps(
            name=name, description=description, tags=tags, type=type
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72f2905f77b08022eeb51f77afaa9f7a70576ec6b470eb8d15214143f97b1d2f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a1f568d0395514b9bc6ab5809ddf12f104403b49249b50bdb0a43260d61b0c3)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An arbitrary set of tags (key–value pairs) to associate with the collection.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html#cfn-opensearchserverless-collection-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d914d516909e9a18b1d36d98dbf490a669a87f5b2ea97f5723f4998596fc4056)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1256765a586d346beebf5d0636c153d8d971aeb840c7240895f116956dfca178)
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
            type_hints = typing.get_type_hints(_typecheckingstub__216c7ef022c564d9aa9c01f482dc4db41111dcb157f1c095bf6c866d54a42879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opensearchserverless.CfnCollectionProps",
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
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_opensearchserverless as opensearchserverless
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__428bde2465711cba630b904347582e228b19deaa55542f771528690113e226fa)
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
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An arbitrary set of tags (key–value pairs) to associate with the collection.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-collection.html#cfn-opensearchserverless-collection-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSecurityConfig(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-opensearchserverless.CfnSecurityConfig",
):
    '''A CloudFormation ``AWS::OpenSearchServerless::SecurityConfig``.

    Specifies a security configuration for OpenSearch Serverless. For more information, see `SAML authentication for Amazon OpenSearch Serverless <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-saml.html>`_ .

    :cloudformationResource: AWS::OpenSearchServerless::SecurityConfig
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_opensearchserverless as opensearchserverless
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        saml_options: typing.Optional[typing.Union[typing.Union["CfnSecurityConfig.SamlConfigOptionsProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8240b644c263e8e7d30beb393d453e1e3564550fb3e375308ece2aab9daf8f1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSecurityConfigProps(
            description=description, name=name, saml_options=saml_options, type=type
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44aab9bcac016206d1eb6271275c3e5692e687d26593d022af6ce5e9748d593f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31ca8bce83f652644fa4c0d27d6d60e2a4f0442a51741a4436e982519f573251)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6336f60433a39d3fbeaa750292289e3a1d59a7bd4c90a522a6fa90e1eb8e51e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ccba89461d79b6fb35223e98ecd51ff26fd913362ae17764bca3c82dd6db9ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="samlOptions")
    def saml_options(
        self,
    ) -> typing.Optional[typing.Union["CfnSecurityConfig.SamlConfigOptionsProperty", _aws_cdk_core_f4b25747.IResolvable]]:
        '''SAML options for the security configuration in the form of a key-value map.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html#cfn-opensearchserverless-securityconfig-samloptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnSecurityConfig.SamlConfigOptionsProperty", _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "samlOptions"))

    @saml_options.setter
    def saml_options(
        self,
        value: typing.Optional[typing.Union["CfnSecurityConfig.SamlConfigOptionsProperty", _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f8d294b9c61f810beb28ee890a40ee1f926378137051b4b5fdf82126f697a01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2d5a1dc245a0d70f73338529accfe1286b9f90659d5326d6c7a17b45e6e7bee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-opensearchserverless.CfnSecurityConfig.SamlConfigOptionsProperty",
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
                import aws_cdk.aws_opensearchserverless as opensearchserverless
                
                saml_config_options_property = opensearchserverless.CfnSecurityConfig.SamlConfigOptionsProperty(
                    metadata="metadata",
                
                    # the properties below are optional
                    group_attribute="groupAttribute",
                    session_timeout=123,
                    user_attribute="userAttribute"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7b9e8663e3518f305351cd19a32c26cbc2e813155755114c0aea044ab47b786)
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
    jsii_type="@aws-cdk/aws-opensearchserverless.CfnSecurityConfigProps",
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
        saml_options: typing.Optional[typing.Union[typing.Union[CfnSecurityConfig.SamlConfigOptionsProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
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
            import aws_cdk.aws_opensearchserverless as opensearchserverless
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__b274b923b3a0869657026663a1554cf11ff00f083163c5cf76b4898e5e1f6760)
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
    ) -> typing.Optional[typing.Union[CfnSecurityConfig.SamlConfigOptionsProperty, _aws_cdk_core_f4b25747.IResolvable]]:
        '''SAML options for the security configuration in the form of a key-value map.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-securityconfig.html#cfn-opensearchserverless-securityconfig-samloptions
        '''
        result = self._values.get("saml_options")
        return typing.cast(typing.Optional[typing.Union[CfnSecurityConfig.SamlConfigOptionsProperty, _aws_cdk_core_f4b25747.IResolvable]], result)

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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSecurityPolicy(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-opensearchserverless.CfnSecurityPolicy",
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
        import aws_cdk.aws_opensearchserverless as opensearchserverless
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__4968652f0c16730dfd2bc0508f0c36e1d40cc69f693cb66a7561e38e50e1d3e3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSecurityPolicyProps(
            policy=policy, description=description, name=name, type=type
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ead4f638a030462e156e6347c28e47f73c3489d1037de817c88626777d391ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86fda416f87719ae04d3648843307770e59020a844c287823a11a17f43e5e457)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaa6657d2fab04218a175a69065e7323b77067d999a0c27ec97b10efdd72429f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7c2c3b2a7508b68e2ae159adf3c432963f3a2368fcbcbc263d0b1a790b0a247)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2adf5cbeb6e24354d36f40c3f6899425b89ad02a8c06cfba88beb7d1b12c290)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9502bef92c0552624b2f80023f5c3dfc1f51245777c340248a3fef13161a520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opensearchserverless.CfnSecurityPolicyProps",
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
            import aws_cdk.aws_opensearchserverless as opensearchserverless
            
            cfn_security_policy_props = opensearchserverless.CfnSecurityPolicyProps(
                policy="policy",
            
                # the properties below are optional
                description="description",
                name="name",
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e87a6de65d99d24ba6241092b119999c9c033b97bd0cf9e51e6a4ec1e9bfc81e)
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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnVpcEndpoint(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-opensearchserverless.CfnVpcEndpoint",
):
    '''A CloudFormation ``AWS::OpenSearchServerless::VpcEndpoint``.

    Creates an OpenSearch Serverless-managed interface VPC endpoint. For more information, see `Access Amazon OpenSearch Serverless using an interface endpoint <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-vpc.html>`_ .

    :cloudformationResource: AWS::OpenSearchServerless::VpcEndpoint
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-opensearchserverless-vpcendpoint.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_opensearchserverless as opensearchserverless
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__70415872f6796354643277666cfb0c7132ee019a3aace730a2b947c22c28a472)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee8b1120e07b85c18531f5290cb5b57d7cadcecb092cc1738dd3d03ef27b1e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7edb8855b278f0c361f2677c988c0b44bfded96d5cd32eb08b17587281c8b4a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d12b40ddb370e71a71aea8daf73e56e85bbba3006cde28f7d112c1733a1233c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed3a2badf2adda8fba1b1d746e31c5e7a16c8131558b07a3ad4a1adaec74b3ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23c3695a15582901c150f2f6444c9c26a16b35ed54146908f0b708d31019deee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0611e49c100eebbb1d53fd07ce9b0651e944741fba1555667652b7393ad735cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-opensearchserverless.CfnVpcEndpointProps",
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
            import aws_cdk.aws_opensearchserverless as opensearchserverless
            
            cfn_vpc_endpoint_props = opensearchserverless.CfnVpcEndpointProps(
                name="name",
                vpc_id="vpcId",
            
                # the properties below are optional
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e90fd69014167392c5e42c63fe6548b9164cc0c4ea2f3db6054b5e74b1d99718)
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

def _typecheckingstub__a3bd28bec90cad86bc80879c08bebf9324f3edc04aa11566dc4d2b8d96b915d4(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99229ef3ae2c403369fe2860de91587ed47b17f8fad592a599ff67d5f73b3c0(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2be31657476e7e37465511d82341bcbf174b678c1880d08622ddf7068fed64e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7dd3c3cbc0234b0646b96e589a4178588cbb018a321d6f33f9c9c68dea8142(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3632e35022c7cd34bc79a0125a8954d850c17a33c2fa8970b320c5859a124cc3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d73baf636fb2987b68313f33646f63952cd321e915630c6a6b23680151828005(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2d703f54d40690465ae00ad61788667c0f743d35277ef6ea3621497f56bd57(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__111ac1327affb42b1d3ecb402d74e3ecbe665b77152d65bf1cb7b000c053b8e6(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e272b7938d2b0d54d4e596ef62a23a84d7dd108c0e3a69624556aa96a9ab7716(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f2905f77b08022eeb51f77afaa9f7a70576ec6b470eb8d15214143f97b1d2f(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1f568d0395514b9bc6ab5809ddf12f104403b49249b50bdb0a43260d61b0c3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d914d516909e9a18b1d36d98dbf490a669a87f5b2ea97f5723f4998596fc4056(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1256765a586d346beebf5d0636c153d8d971aeb840c7240895f116956dfca178(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216c7ef022c564d9aa9c01f482dc4db41111dcb157f1c095bf6c866d54a42879(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428bde2465711cba630b904347582e228b19deaa55542f771528690113e226fa(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8240b644c263e8e7d30beb393d453e1e3564550fb3e375308ece2aab9daf8f1(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    saml_options: typing.Optional[typing.Union[typing.Union[CfnSecurityConfig.SamlConfigOptionsProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44aab9bcac016206d1eb6271275c3e5692e687d26593d022af6ce5e9748d593f(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ca8bce83f652644fa4c0d27d6d60e2a4f0442a51741a4436e982519f573251(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6336f60433a39d3fbeaa750292289e3a1d59a7bd4c90a522a6fa90e1eb8e51e2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ccba89461d79b6fb35223e98ecd51ff26fd913362ae17764bca3c82dd6db9ed(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8d294b9c61f810beb28ee890a40ee1f926378137051b4b5fdf82126f697a01(
    value: typing.Optional[typing.Union[CfnSecurityConfig.SamlConfigOptionsProperty, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2d5a1dc245a0d70f73338529accfe1286b9f90659d5326d6c7a17b45e6e7bee(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b9e8663e3518f305351cd19a32c26cbc2e813155755114c0aea044ab47b786(
    *,
    metadata: builtins.str,
    group_attribute: typing.Optional[builtins.str] = None,
    session_timeout: typing.Optional[jsii.Number] = None,
    user_attribute: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b274b923b3a0869657026663a1554cf11ff00f083163c5cf76b4898e5e1f6760(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    saml_options: typing.Optional[typing.Union[typing.Union[CfnSecurityConfig.SamlConfigOptionsProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4968652f0c16730dfd2bc0508f0c36e1d40cc69f693cb66a7561e38e50e1d3e3(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    policy: builtins.str,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ead4f638a030462e156e6347c28e47f73c3489d1037de817c88626777d391ff(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86fda416f87719ae04d3648843307770e59020a844c287823a11a17f43e5e457(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa6657d2fab04218a175a69065e7323b77067d999a0c27ec97b10efdd72429f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c2c3b2a7508b68e2ae159adf3c432963f3a2368fcbcbc263d0b1a790b0a247(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2adf5cbeb6e24354d36f40c3f6899425b89ad02a8c06cfba88beb7d1b12c290(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9502bef92c0552624b2f80023f5c3dfc1f51245777c340248a3fef13161a520(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87a6de65d99d24ba6241092b119999c9c033b97bd0cf9e51e6a4ec1e9bfc81e(
    *,
    policy: builtins.str,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70415872f6796354643277666cfb0c7132ee019a3aace730a2b947c22c28a472(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    vpc_id: builtins.str,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee8b1120e07b85c18531f5290cb5b57d7cadcecb092cc1738dd3d03ef27b1e7(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7edb8855b278f0c361f2677c988c0b44bfded96d5cd32eb08b17587281c8b4a7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12b40ddb370e71a71aea8daf73e56e85bbba3006cde28f7d112c1733a1233c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3a2badf2adda8fba1b1d746e31c5e7a16c8131558b07a3ad4a1adaec74b3ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c3695a15582901c150f2f6444c9c26a16b35ed54146908f0b708d31019deee(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0611e49c100eebbb1d53fd07ce9b0651e944741fba1555667652b7393ad735cd(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90fd69014167392c5e42c63fe6548b9164cc0c4ea2f3db6054b5e74b1d99718(
    *,
    name: builtins.str,
    vpc_id: builtins.str,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
