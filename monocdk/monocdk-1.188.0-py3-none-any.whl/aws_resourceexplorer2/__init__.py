'''
# AWS::ResourceExplorer2 Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as resourceexplorer2
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

from .._jsii import *

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnDefaultViewAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_resourceexplorer2.CfnDefaultViewAssociation",
):
    '''A CloudFormation ``AWS::ResourceExplorer2::DefaultViewAssociation``.

    Sets the specified view as the default for the AWS Region in which you call this operation. If a user makes a search query that doesn't explicitly specify the view to use, Resource Explorer chooses this default view automatically for searches performed in this AWS Region .

    :cloudformationResource: AWS::ResourceExplorer2::DefaultViewAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-defaultviewassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_resourceexplorer2 as resourceexplorer2
        
        cfn_default_view_association = resourceexplorer2.CfnDefaultViewAssociation(self, "MyCfnDefaultViewAssociation",
            view_arn="viewArn"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
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
            type_hints = typing.get_type_hints(_typecheckingstub__32531b57ec1d331b6cfb1c5bc0a376d0e1dcd3044664d0a6b21b2b750ad996ec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDefaultViewAssociationProps(view_arn=view_arn)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c36c4ef32ec49c3ecd27838658aba61ff098627248858645ef9e2d74da2b04)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f5b08c9d819f9249ab15ac3c8de61eb19068f51c534f7bcfd0040bd43e9da32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb31caeface9524ea319b027f2f3c8e3b5711b19eaf0ced62593f6b7f023ddda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "viewArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_resourceexplorer2.CfnDefaultViewAssociationProps",
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
            from monocdk import aws_resourceexplorer2 as resourceexplorer2
            
            cfn_default_view_association_props = resourceexplorer2.CfnDefaultViewAssociationProps(
                view_arn="viewArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f4287bd0264f847176e10730447846e80bdf736b15923fbedb637e2ef26a84c)
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


@jsii.implements(_IInspectable_82c04a63)
class CfnIndex(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_resourceexplorer2.CfnIndex",
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
        from monocdk import aws_resourceexplorer2 as resourceexplorer2
        
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
        scope: _Construct_e78e779f,
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
            type_hints = typing.get_type_hints(_typecheckingstub__e357394e2572dc1f8d77b33f59533c7c09321046ca09ceaf5fe33e439928ad48)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnIndexProps(type=type, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa60573b85e24c1baf771ffa7c3d24cfe3fbfb64b91bfb9e6f090f085525ab0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0484bb2fc9ffb86f0150774a502d4a386efefa8e2356f11c9e9e02d7c6a4af0)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''The specified tags are attached to only the index created in this AWS Region .

        The tags don't attach to any of the resources listed in the index.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-index.html#cfn-resourceexplorer2-index-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__be9db2e7b86681ae94cbc47ff99fb82652a7c3f4e3626689852345bf8a6f963b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="monocdk.aws_resourceexplorer2.CfnIndexProps",
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
            from monocdk import aws_resourceexplorer2 as resourceexplorer2
            
            cfn_index_props = resourceexplorer2.CfnIndexProps(
                type="type",
            
                # the properties below are optional
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a436bd08c6528e59df54bc8333d25b15f608e48417fc4ab0b03b42d8771152f)
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


@jsii.implements(_IInspectable_82c04a63)
class CfnView(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_resourceexplorer2.CfnView",
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
        from monocdk import aws_resourceexplorer2 as resourceexplorer2
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        view_name: builtins.str,
        filters: typing.Optional[typing.Union[typing.Union["CfnView.FiltersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        included_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnView.IncludedPropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c2ebb2cc7b5552c4153dcc824e9b9452181b05eff56bd5b8a04b0bb4da77add)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37deebb630d0405234aa3f50ba077cb8536b1eed8bc6ac487c6d800f2907c10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3be319d730dc44d980b2bdfa72a00bcb9387f78cc9572c222df49460383a9c74)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''Tag key and value pairs that are attached to the view.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html#cfn-resourceexplorer2-view-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__81e0d16ed909294a96f1d6f41a309a80fdd946fe1431b5ca47e4b4995d1d93b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "viewName", value)

    @builtins.property
    @jsii.member(jsii_name="filters")
    def filters(
        self,
    ) -> typing.Optional[typing.Union["CfnView.FiltersProperty", _IResolvable_a771d0ef]]:
        '''An array of strings that include search keywords, prefixes, and operators that filter the results that are returned for queries made using this view.

        When you use this view in a `Search <https://docs.aws.amazon.com/resource-explorer/latest/APIReference/API_Search.html>`_ operation, the filter string is combined with the search's ``QueryString`` parameter using a logical ``AND`` operator.

        For information about the supported syntax, see `Search query reference for Resource Explorer <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html>`_ in the *AWS Resource Explorer User Guide* .
        .. epigraph::

           This query string in the context of this operation supports only `filter prefixes <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-filters>`_ with optional `operators <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-operators>`_ . It doesn't support free-form text. For example, the string ``region:us* service:ec2 -tag:stage=prod`` includes all Amazon EC2 resources in any AWS Region that begin with the letters ``us`` and are *not* tagged with a key ``Stage`` that has the value ``prod`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html#cfn-resourceexplorer2-view-filters
        '''
        return typing.cast(typing.Optional[typing.Union["CfnView.FiltersProperty", _IResolvable_a771d0ef]], jsii.get(self, "filters"))

    @filters.setter
    def filters(
        self,
        value: typing.Optional[typing.Union["CfnView.FiltersProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__971fe0c50d1b212532f096041ac8ce8e4e197de2a2d25c330b7dc0bf7c4c53da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filters", value)

    @builtins.property
    @jsii.member(jsii_name="includedProperties")
    def included_properties(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnView.IncludedPropertyProperty", _IResolvable_a771d0ef]]]]:
        '''A list of fields that provide additional information about the view.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html#cfn-resourceexplorer2-view-includedproperties
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnView.IncludedPropertyProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "includedProperties"))

    @included_properties.setter
    def included_properties(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnView.IncludedPropertyProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__131003ee3df1849bf537c4f68edb1547663048fb66762c6d4caa36d6dd50feb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedProperties", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_resourceexplorer2.CfnView.FiltersProperty",
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
                from monocdk import aws_resourceexplorer2 as resourceexplorer2
                
                filters_property = resourceexplorer2.CfnView.FiltersProperty(
                    filter_string="filterString"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8def5b6d61bae4fb70fbf78321d6d38acc743ac397e640d6efb16cf84b27a170)
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
        jsii_type="monocdk.aws_resourceexplorer2.CfnView.IncludedPropertyProperty",
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
                from monocdk import aws_resourceexplorer2 as resourceexplorer2
                
                included_property_property = resourceexplorer2.CfnView.IncludedPropertyProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e470f5832a4dd3d83bfde2a2118f1affea584e55bacfc190dbc7b3a64f4e85ef)
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
    jsii_type="monocdk.aws_resourceexplorer2.CfnViewProps",
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
        filters: typing.Optional[typing.Union[typing.Union[CfnView.FiltersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        included_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnView.IncludedPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
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
            from monocdk import aws_resourceexplorer2 as resourceexplorer2
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe164a1dcf21546d500935947ab6aedb9f334e154c2cc48fb417c57c99f6d414)
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
    ) -> typing.Optional[typing.Union[CfnView.FiltersProperty, _IResolvable_a771d0ef]]:
        '''An array of strings that include search keywords, prefixes, and operators that filter the results that are returned for queries made using this view.

        When you use this view in a `Search <https://docs.aws.amazon.com/resource-explorer/latest/APIReference/API_Search.html>`_ operation, the filter string is combined with the search's ``QueryString`` parameter using a logical ``AND`` operator.

        For information about the supported syntax, see `Search query reference for Resource Explorer <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html>`_ in the *AWS Resource Explorer User Guide* .
        .. epigraph::

           This query string in the context of this operation supports only `filter prefixes <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-filters>`_ with optional `operators <https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html#query-syntax-operators>`_ . It doesn't support free-form text. For example, the string ``region:us* service:ec2 -tag:stage=prod`` includes all Amazon EC2 resources in any AWS Region that begin with the letters ``us`` and are *not* tagged with a key ``Stage`` that has the value ``prod`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html#cfn-resourceexplorer2-view-filters
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.Union[CfnView.FiltersProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def included_properties(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnView.IncludedPropertyProperty, _IResolvable_a771d0ef]]]]:
        '''A list of fields that provide additional information about the view.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-resourceexplorer2-view.html#cfn-resourceexplorer2-view-includedproperties
        '''
        result = self._values.get("included_properties")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnView.IncludedPropertyProperty, _IResolvable_a771d0ef]]]], result)

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

def _typecheckingstub__32531b57ec1d331b6cfb1c5bc0a376d0e1dcd3044664d0a6b21b2b750ad996ec(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    view_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c36c4ef32ec49c3ecd27838658aba61ff098627248858645ef9e2d74da2b04(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5b08c9d819f9249ab15ac3c8de61eb19068f51c534f7bcfd0040bd43e9da32(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb31caeface9524ea319b027f2f3c8e3b5711b19eaf0ced62593f6b7f023ddda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f4287bd0264f847176e10730447846e80bdf736b15923fbedb637e2ef26a84c(
    *,
    view_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e357394e2572dc1f8d77b33f59533c7c09321046ca09ceaf5fe33e439928ad48(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    type: builtins.str,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa60573b85e24c1baf771ffa7c3d24cfe3fbfb64b91bfb9e6f090f085525ab0(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0484bb2fc9ffb86f0150774a502d4a386efefa8e2356f11c9e9e02d7c6a4af0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9db2e7b86681ae94cbc47ff99fb82652a7c3f4e3626689852345bf8a6f963b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a436bd08c6528e59df54bc8333d25b15f608e48417fc4ab0b03b42d8771152f(
    *,
    type: builtins.str,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c2ebb2cc7b5552c4153dcc824e9b9452181b05eff56bd5b8a04b0bb4da77add(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    view_name: builtins.str,
    filters: typing.Optional[typing.Union[typing.Union[CfnView.FiltersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    included_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnView.IncludedPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37deebb630d0405234aa3f50ba077cb8536b1eed8bc6ac487c6d800f2907c10(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3be319d730dc44d980b2bdfa72a00bcb9387f78cc9572c222df49460383a9c74(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81e0d16ed909294a96f1d6f41a309a80fdd946fe1431b5ca47e4b4995d1d93b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__971fe0c50d1b212532f096041ac8ce8e4e197de2a2d25c330b7dc0bf7c4c53da(
    value: typing.Optional[typing.Union[CfnView.FiltersProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__131003ee3df1849bf537c4f68edb1547663048fb66762c6d4caa36d6dd50feb6(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnView.IncludedPropertyProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8def5b6d61bae4fb70fbf78321d6d38acc743ac397e640d6efb16cf84b27a170(
    *,
    filter_string: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e470f5832a4dd3d83bfde2a2118f1affea584e55bacfc190dbc7b3a64f4e85ef(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe164a1dcf21546d500935947ab6aedb9f334e154c2cc48fb417c57c99f6d414(
    *,
    view_name: builtins.str,
    filters: typing.Optional[typing.Union[typing.Union[CfnView.FiltersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    included_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnView.IncludedPropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
