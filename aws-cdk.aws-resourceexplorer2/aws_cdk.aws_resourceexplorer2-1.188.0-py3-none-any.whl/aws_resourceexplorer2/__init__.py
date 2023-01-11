'''
# AWS::ResourceExplorer2 Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_resourceexplorer2 as resourceexplorer2
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for ResourceExplorer2 construct libraries](https://constructs.dev/search?q=resourceexplorer2)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::ResourceExplorer2 resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ResourceExplorer2.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::ResourceExplorer2](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ResourceExplorer2.html).

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
class CfnDefaultViewAssociation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-resourceexplorer2.CfnDefaultViewAssociation",
):
    '''A CloudFormation ``AWS::ResourceExplorer2::DefaultViewAssociation``.

    Sets the specified view as the default for the AWS Region in which you call this operation. If a user makes a search query that doesn't explicitly specify the view to use, Resource Explorer chooses this default view automatically for searches performed in this AWS Region .

    :cloudformationResource: AWS::ResourceExplorer2::DefaultViewAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-defaultviewassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_resourceexplorer2 as resourceexplorer2
        
        cfn_default_view_association = resourceexplorer2.CfnDefaultViewAssociation(self, "MyCfnDefaultViewAssociation",
            view_arn="viewArn"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        view_arn: builtins.str,
    ) -> None:
        '''Create a new ``AWS::ResourceExplorer2::DefaultViewAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param view_arn: The ARN of the view to set as the default for the AWS Region and AWS account in which you call this operation. The specified view must already exist in the specified Region.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c2da475d56c948c288533ced762ab7897e6db24e4d2e90c3d51c134ce536cc7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDefaultViewAssociationProps(view_arn=view_arn)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c1991d7fb35fca7af4fa8b0204feb57ac53024e6ecf310e4bcfd8ce17e5abd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3fc05a927965b20fad72c3e0907075cea84bb99112e763eb97b22e152815a37)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAssociatedAwsPrincipal")
    def attr_associated_aws_principal(self) -> builtins.str:
        '''The unique identifier of the principal for which the specified view was made the default for the AWS Region that contains the view.

        For example:

        ``123456789012``

        :cloudformationAttribute: AssociatedAwsPrincipal
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssociatedAwsPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="viewArn")
    def view_arn(self) -> builtins.str:
        '''The ARN of the view to set as the default for the AWS Region and AWS account in which you call this operation.

        The specified view must already exist in the specified Region.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-defaultviewassociation.html#cfn-resourceexplorer2-defaultviewassociation-viewarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "viewArn"))

    @view_arn.setter
    def view_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82cb8e8a33ae4102ffda8441795c1e10172f1a940ebf9d5b62eb1568329bd13d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "viewArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-resourceexplorer2.CfnDefaultViewAssociationProps",
    jsii_struct_bases=[],
    name_mapping={"view_arn": "viewArn"},
)
class CfnDefaultViewAssociationProps:
    def __init__(self, *, view_arn: builtins.str) -> None:
        '''Properties for defining a ``CfnDefaultViewAssociation``.

        :param view_arn: The ARN of the view to set as the default for the AWS Region and AWS account in which you call this operation. The specified view must already exist in the specified Region.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-defaultviewassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_resourceexplorer2 as resourceexplorer2
            
            cfn_default_view_association_props = resourceexplorer2.CfnDefaultViewAssociationProps(
                view_arn="viewArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba079c22cc779cb6a8a1caec0cae902a29f558f18248f89fcbade29fc37dc6cb)
            check_type(argname="argument view_arn", value=view_arn, expected_type=type_hints["view_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "view_arn": view_arn,
        }

    @builtins.property
    def view_arn(self) -> builtins.str:
        '''The ARN of the view to set as the default for the AWS Region and AWS account in which you call this operation.

        The specified view must already exist in the specified Region.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-defaultviewassociation.html#cfn-resourceexplorer2-defaultviewassociation-viewarn
        '''
        result = self._values.get("view_arn")
        assert result is not None, "Required property 'view_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDefaultViewAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnIndex(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-resourceexplorer2.CfnIndex",
):
    '''A CloudFormation ``AWS::ResourceExplorer2::Index``.

    Turns on Resource Explorer in the AWS Region in which you called this operation by creating an index. Resource Explorer begins discovering the resources in this Region and stores the details about the resources in the index so that they can be queried by using the `Search <https://docs.aws.amazon.com/resource-explorer/latest/APIReference/API_Search.html>`_ operation.

    You can create either a local index that returns search results from only the AWS Region in which the index exists, or you can create an aggregator index that returns search results from all AWS Regions in the AWS account .

    For more details about what happens when you turn on Resource Explorer in an AWS Region , see `Turning on Resource Explorer to index your resources in an AWS Region <https://docs.aws.amazon.com/resource-explorer/latest/userguide/manage-service-activate.html>`_ in the *AWS Resource Explorer User Guide.*

    If this is the first AWS Region in which you've created an index for Resource Explorer, this operation also creates a service-linked role in your AWS account that allows Resource Explorer to search for your resources and populate the index.
    .. epigraph::

       To successfully create an index, you must have ``resource-explorer-2:TagResource`` permission, even if you don't specify tags to be added to the index.

    :cloudformationResource: AWS::ResourceExplorer2::Index
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-index.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_resourceexplorer2 as resourceexplorer2
        
        cfn_index = resourceexplorer2.CfnIndex(self, "MyCfnIndex",
            type="type",
        
            # the properties below are optional
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        type: builtins.str,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::ResourceExplorer2::Index``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param type: Specifies the type of the index in this Region. For information about the aggregator index and how it differs from a local index, see `Turning on cross-Region search by creating an aggregator index <https://docs.aws.amazon.com/resource-explorer/latest/userguide/manage-aggregator-region.html>`_ in the *AWS Resource Explorer User Guide.* .
        :param tags: The specified tags are attached to only the index created in this AWS Region . The tags don't attach to any of the resources listed in the index.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20227bfebd09c85cf780d74f45c59bbb160f20a0bce29ebecbf1b44d8359b5aa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnIndexProps(type=type, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3170b7fcbb4270595249014b4d300fe0b6c073e7c65e0f56411a230cf69c0ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdc71e74e2b380dadc370e2c18ed90c433c5ba561b3867331e1334a90139d51e)
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
        '''The ARN of the new index for the AWS Region . For example:.

        ``arn:aws:resource-explorer-2:us-east-1:123456789012:index/EXAMPLE8-90ab-cdef-fedc-EXAMPLE22222``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrIndexState")
    def attr_index_state(self) -> builtins.str:
        '''Indicates the current state of the index. For example:.

        ``CREATING``

        :cloudformationAttribute: IndexState
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrIndexState"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The specified tags are attached to only the index created in this AWS Region .

        The tags don't attach to any of the resources listed in the index.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-index.html#cfn-resourceexplorer2-index-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''Specifies the type of the index in this Region.

        For information about the aggregator index and how it differs from a local index, see `Turning on cross-Region search by creating an aggregator index <https://docs.aws.amazon.com/resource-explorer/latest/userguide/manage-aggregator-region.html>`_ in the *AWS Resource Explorer User Guide.* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-index.html#cfn-resourceexplorer2-index-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1dd54adc2802292e9312967430d38ea22c5863889523355ec9523f808a8288)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-resourceexplorer2.CfnIndexProps",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "tags": "tags"},
)
class CfnIndexProps:
    def __init__(
        self,
        *,
        type: builtins.str,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnIndex``.

        :param type: Specifies the type of the index in this Region. For information about the aggregator index and how it differs from a local index, see `Turning on cross-Region search by creating an aggregator index <https://docs.aws.amazon.com/resource-explorer/latest/userguide/manage-aggregator-region.html>`_ in the *AWS Resource Explorer User Guide.* .
        :param tags: The specified tags are attached to only the index created in this AWS Region . The tags don't attach to any of the resources listed in the index.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-index.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_resourceexplorer2 as resourceexplorer2
            
            cfn_index_props = resourceexplorer2.CfnIndexProps(
                type="type",
            
                # the properties below are optional
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef0da209204e2d53c21a508260af5eed1089eb77d0d559299439249aad65c1e5)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def type(self) -> builtins.str:
        '''Specifies the type of the index in this Region.

        For information about the aggregator index and how it differs from a local index, see `Turning on cross-Region search by creating an aggregator index <https://docs.aws.amazon.com/resource-explorer/latest/userguide/manage-aggregator-region.html>`_ in the *AWS Resource Explorer User Guide.* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-index.html#cfn-resourceexplorer2-index-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The specified tags are attached to only the index created in this AWS Region .

        The tags don't attach to any of the resources listed in the index.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-index.html#cfn-resourceexplorer2-index-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIndexProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnView(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-resourceexplorer2.CfnView",
):
    '''A CloudFormation ``AWS::ResourceExplorer2::View``.

    Creates a view that users can query by using the `Search <https://docs.aws.amazon.com/resource-explorer/latest/APIReference/API_Search.html>`_ operation. Results from queries that you make using this view include only resources that match the view's ``Filters`` .
    .. epigraph::

       To successfully create a view, you must have ``resource-explorer-2:TagResource`` permission, even if you don't specify tags to be added to the view.

    :cloudformationResource: AWS::ResourceExplorer2::View
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_resourceexplorer2 as resourceexplorer2
        
        cfn_view = resourceexplorer2.CfnView(self, "MyCfnView",
            view_name="viewName",
        
            # the properties below are optional
            filters=resourceexplorer2.CfnView.FiltersProperty(
                filter_string="filterString"
            ),
            included_properties=[resourceexplorer2.CfnView.IncludedPropertyProperty(
                name="name"
            )],
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        view_name: builtins.str,
        filters: typing.Optional[typing.Union[typing.Union["CfnView.FiltersProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        included_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnView.IncludedPropertyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::ResourceExplorer2::View``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param view_name: The name of the new view.
        :param filters: An array of strings that include search keywords, prefixes, and operators that filter the results that are returned for queries made using this view. When you use this view in a `Search <https://docs.aws.amazon.com/resource-explorer/latest/APIReference/API_Search.html>`_ operation, the filter string is combined with the search's ``QueryString`` parameter using a logical ``AND`` operator. For information about the supported syntax, see `Search query reference for Resource Explorer <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html>`_ in the *AWS Resource Explorer User Guide* . .. epigraph:: This query string in the context of this operation supports only `filter prefixes <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-filters>`_ with optional `operators <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-operators>`_ . It doesn't support free-form text. For example, the string ``region:us* service:ec2 -tag:stage=prod`` includes all Amazon EC2 resources in any AWS Region that begin with the letters ``us`` and are *not* tagged with a key ``Stage`` that has the value ``prod`` .
        :param included_properties: A list of fields that provide additional information about the view.
        :param tags: Tag key and value pairs that are attached to the view.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3808e0a534b2b7613d84b40b05b479df010f4cd5de8559a72ec8eaa68112c3e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnViewProps(
            view_name=view_name,
            filters=filters,
            included_properties=included_properties,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c0aab9b113af754877675b0e250df1a0a65bfd5c31e57f5576b46bfece32409)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4af493207e1c203969a8133742f1aa6d8cdcfb632659dadb71c056723311de0e)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrViewArn")
    def attr_view_arn(self) -> builtins.str:
        '''The ARN of the new view. For example:.

        ``arn:aws:resource-explorer-2:us-east-1:123456789012:view/MyView/EXAMPLE8-90ab-cdef-fedc-EXAMPLE22222``

        :cloudformationAttribute: ViewArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrViewArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Tag key and value pairs that are attached to the view.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html#cfn-resourceexplorer2-view-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="viewName")
    def view_name(self) -> builtins.str:
        '''The name of the new view.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html#cfn-resourceexplorer2-view-viewname
        '''
        return typing.cast(builtins.str, jsii.get(self, "viewName"))

    @view_name.setter
    def view_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085922cbc6c3d901b89ab3a74c4c1260d7fb04939e2cc0a9683758cffbcbb3d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "viewName", value)

    @builtins.property
    @jsii.member(jsii_name="filters")
    def filters(
        self,
    ) -> typing.Optional[typing.Union["CfnView.FiltersProperty", _aws_cdk_core_f4b25747.IResolvable]]:
        '''An array of strings that include search keywords, prefixes, and operators that filter the results that are returned for queries made using this view.

        When you use this view in a `Search <https://docs.aws.amazon.com/resource-explorer/latest/APIReference/API_Search.html>`_ operation, the filter string is combined with the search's ``QueryString`` parameter using a logical ``AND`` operator.

        For information about the supported syntax, see `Search query reference for Resource Explorer <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html>`_ in the *AWS Resource Explorer User Guide* .
        .. epigraph::

           This query string in the context of this operation supports only `filter prefixes <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-filters>`_ with optional `operators <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-operators>`_ . It doesn't support free-form text. For example, the string ``region:us* service:ec2 -tag:stage=prod`` includes all Amazon EC2 resources in any AWS Region that begin with the letters ``us`` and are *not* tagged with a key ``Stage`` that has the value ``prod`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html#cfn-resourceexplorer2-view-filters
        '''
        return typing.cast(typing.Optional[typing.Union["CfnView.FiltersProperty", _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "filters"))

    @filters.setter
    def filters(
        self,
        value: typing.Optional[typing.Union["CfnView.FiltersProperty", _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dd6007dce8ef21c35e0ff868eaa1d594efc03e4aad54f7e5817e9be78f56b12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filters", value)

    @builtins.property
    @jsii.member(jsii_name="includedProperties")
    def included_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnView.IncludedPropertyProperty"]]]]:
        '''A list of fields that provide additional information about the view.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html#cfn-resourceexplorer2-view-includedproperties
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnView.IncludedPropertyProperty"]]]], jsii.get(self, "includedProperties"))

    @included_properties.setter
    def included_properties(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnView.IncludedPropertyProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a8f0b40f8d5cb8ccb33173342d4041e64bee2c3de9a316ba5f50511780720f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedProperties", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-resourceexplorer2.CfnView.FiltersProperty",
        jsii_struct_bases=[],
        name_mapping={"filter_string": "filterString"},
    )
    class FiltersProperty:
        def __init__(self, *, filter_string: builtins.str) -> None:
            '''An object with a ``FilterString`` that specifies which resources to include in the results of queries made using this view.

            :param filter_string: ``CfnView.FiltersProperty.FilterString``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourceexplorer2-view-filters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_resourceexplorer2 as resourceexplorer2
                
                filters_property = resourceexplorer2.CfnView.FiltersProperty(
                    filter_string="filterString"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d19c7be70e98a54465f806861fbbd8fb77135f5383e7dda42c768d86c8969a40)
                check_type(argname="argument filter_string", value=filter_string, expected_type=type_hints["filter_string"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "filter_string": filter_string,
            }

        @builtins.property
        def filter_string(self) -> builtins.str:
            '''``CfnView.FiltersProperty.FilterString``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourceexplorer2-view-filters.html#cfn-resourceexplorer2-view-filters-filterstring
            '''
            result = self._values.get("filter_string")
            assert result is not None, "Required property 'filter_string' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FiltersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-resourceexplorer2.CfnView.IncludedPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class IncludedPropertyProperty:
        def __init__(self, *, name: builtins.str) -> None:
            '''Information about an additional property that describes a resource, that you can optionally include in a view.

            :param name: The name of the property that is included in this view.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourceexplorer2-view-includedproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_resourceexplorer2 as resourceexplorer2
                
                included_property_property = resourceexplorer2.CfnView.IncludedPropertyProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0745f3d5c3a085e96f1ccbd2628286387745d5329067dd58b6704240cc4ebfc8)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the property that is included in this view.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resourceexplorer2-view-includedproperty.html#cfn-resourceexplorer2-view-includedproperty-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IncludedPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-resourceexplorer2.CfnViewProps",
    jsii_struct_bases=[],
    name_mapping={
        "view_name": "viewName",
        "filters": "filters",
        "included_properties": "includedProperties",
        "tags": "tags",
    },
)
class CfnViewProps:
    def __init__(
        self,
        *,
        view_name: builtins.str,
        filters: typing.Optional[typing.Union[typing.Union[CfnView.FiltersProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        included_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnView.IncludedPropertyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnView``.

        :param view_name: The name of the new view.
        :param filters: An array of strings that include search keywords, prefixes, and operators that filter the results that are returned for queries made using this view. When you use this view in a `Search <https://docs.aws.amazon.com/resource-explorer/latest/APIReference/API_Search.html>`_ operation, the filter string is combined with the search's ``QueryString`` parameter using a logical ``AND`` operator. For information about the supported syntax, see `Search query reference for Resource Explorer <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html>`_ in the *AWS Resource Explorer User Guide* . .. epigraph:: This query string in the context of this operation supports only `filter prefixes <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-filters>`_ with optional `operators <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-operators>`_ . It doesn't support free-form text. For example, the string ``region:us* service:ec2 -tag:stage=prod`` includes all Amazon EC2 resources in any AWS Region that begin with the letters ``us`` and are *not* tagged with a key ``Stage`` that has the value ``prod`` .
        :param included_properties: A list of fields that provide additional information about the view.
        :param tags: Tag key and value pairs that are attached to the view.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_resourceexplorer2 as resourceexplorer2
            
            cfn_view_props = resourceexplorer2.CfnViewProps(
                view_name="viewName",
            
                # the properties below are optional
                filters=resourceexplorer2.CfnView.FiltersProperty(
                    filter_string="filterString"
                ),
                included_properties=[resourceexplorer2.CfnView.IncludedPropertyProperty(
                    name="name"
                )],
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b8b2f465133290d1c90a8fece7121e8af8f04acb355e50075a62a4d0ed6f40)
            check_type(argname="argument view_name", value=view_name, expected_type=type_hints["view_name"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument included_properties", value=included_properties, expected_type=type_hints["included_properties"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "view_name": view_name,
        }
        if filters is not None:
            self._values["filters"] = filters
        if included_properties is not None:
            self._values["included_properties"] = included_properties
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def view_name(self) -> builtins.str:
        '''The name of the new view.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html#cfn-resourceexplorer2-view-viewname
        '''
        result = self._values.get("view_name")
        assert result is not None, "Required property 'view_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filters(
        self,
    ) -> typing.Optional[typing.Union[CfnView.FiltersProperty, _aws_cdk_core_f4b25747.IResolvable]]:
        '''An array of strings that include search keywords, prefixes, and operators that filter the results that are returned for queries made using this view.

        When you use this view in a `Search <https://docs.aws.amazon.com/resource-explorer/latest/APIReference/API_Search.html>`_ operation, the filter string is combined with the search's ``QueryString`` parameter using a logical ``AND`` operator.

        For information about the supported syntax, see `Search query reference for Resource Explorer <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html>`_ in the *AWS Resource Explorer User Guide* .
        .. epigraph::

           This query string in the context of this operation supports only `filter prefixes <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-filters>`_ with optional `operators <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-operators>`_ . It doesn't support free-form text. For example, the string ``region:us* service:ec2 -tag:stage=prod`` includes all Amazon EC2 resources in any AWS Region that begin with the letters ``us`` and are *not* tagged with a key ``Stage`` that has the value ``prod`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html#cfn-resourceexplorer2-view-filters
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.Union[CfnView.FiltersProperty, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def included_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnView.IncludedPropertyProperty]]]]:
        '''A list of fields that provide additional information about the view.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html#cfn-resourceexplorer2-view-includedproperties
        '''
        result = self._values.get("included_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnView.IncludedPropertyProperty]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tag key and value pairs that are attached to the view.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html#cfn-resourceexplorer2-view-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnViewProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDefaultViewAssociation",
    "CfnDefaultViewAssociationProps",
    "CfnIndex",
    "CfnIndexProps",
    "CfnView",
    "CfnViewProps",
]

publication.publish()

def _typecheckingstub__5c2da475d56c948c288533ced762ab7897e6db24e4d2e90c3d51c134ce536cc7(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    view_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1991d7fb35fca7af4fa8b0204feb57ac53024e6ecf310e4bcfd8ce17e5abd2(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3fc05a927965b20fad72c3e0907075cea84bb99112e763eb97b22e152815a37(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82cb8e8a33ae4102ffda8441795c1e10172f1a940ebf9d5b62eb1568329bd13d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba079c22cc779cb6a8a1caec0cae902a29f558f18248f89fcbade29fc37dc6cb(
    *,
    view_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20227bfebd09c85cf780d74f45c59bbb160f20a0bce29ebecbf1b44d8359b5aa(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    type: builtins.str,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3170b7fcbb4270595249014b4d300fe0b6c073e7c65e0f56411a230cf69c0ae(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc71e74e2b380dadc370e2c18ed90c433c5ba561b3867331e1334a90139d51e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1dd54adc2802292e9312967430d38ea22c5863889523355ec9523f808a8288(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef0da209204e2d53c21a508260af5eed1089eb77d0d559299439249aad65c1e5(
    *,
    type: builtins.str,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3808e0a534b2b7613d84b40b05b479df010f4cd5de8559a72ec8eaa68112c3e(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    view_name: builtins.str,
    filters: typing.Optional[typing.Union[typing.Union[CfnView.FiltersProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    included_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnView.IncludedPropertyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c0aab9b113af754877675b0e250df1a0a65bfd5c31e57f5576b46bfece32409(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af493207e1c203969a8133742f1aa6d8cdcfb632659dadb71c056723311de0e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085922cbc6c3d901b89ab3a74c4c1260d7fb04939e2cc0a9683758cffbcbb3d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd6007dce8ef21c35e0ff868eaa1d594efc03e4aad54f7e5817e9be78f56b12(
    value: typing.Optional[typing.Union[CfnView.FiltersProperty, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a8f0b40f8d5cb8ccb33173342d4041e64bee2c3de9a316ba5f50511780720f0(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnView.IncludedPropertyProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19c7be70e98a54465f806861fbbd8fb77135f5383e7dda42c768d86c8969a40(
    *,
    filter_string: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0745f3d5c3a085e96f1ccbd2628286387745d5329067dd58b6704240cc4ebfc8(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b8b2f465133290d1c90a8fece7121e8af8f04acb355e50075a62a4d0ed6f40(
    *,
    view_name: builtins.str,
    filters: typing.Optional[typing.Union[typing.Union[CfnView.FiltersProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    included_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnView.IncludedPropertyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
