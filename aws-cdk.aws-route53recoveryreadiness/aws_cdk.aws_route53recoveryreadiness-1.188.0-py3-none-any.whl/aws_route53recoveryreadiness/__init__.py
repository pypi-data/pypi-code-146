'''
# AWS::Route53RecoveryReadiness Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_route53recoveryreadiness as route53recoveryreadiness
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Route53RecoveryReadiness construct libraries](https://constructs.dev/search?q=route53recoveryreadiness)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Route53RecoveryReadiness resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Route53RecoveryReadiness.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Route53RecoveryReadiness](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Route53RecoveryReadiness.html).

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
class CfnCell(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53recoveryreadiness.CfnCell",
):
    '''A CloudFormation ``AWS::Route53RecoveryReadiness::Cell``.

    Creates a cell in an account.

    :cloudformationResource: AWS::Route53RecoveryReadiness::Cell
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-cell.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_route53recoveryreadiness as route53recoveryreadiness
        
        cfn_cell = route53recoveryreadiness.CfnCell(self, "MyCfnCell",
            cell_name="cellName",
            cells=["cells"],
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
        cell_name: typing.Optional[builtins.str] = None,
        cells: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Route53RecoveryReadiness::Cell``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cell_name: The name of the cell to create.
        :param cells: A list of cell Amazon Resource Names (ARNs) contained within this cell, for use in nested cells. For example, Availability Zones within specific AWS Regions .
        :param tags: A collection of tags associated with a resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2e9ddd87e6b794e10435fcc379020436acd7c060581bf0990ce29855723663)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCellProps(cell_name=cell_name, cells=cells, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c22be4dc98cdd514d243cf61c6d26275aae23a87d6728bae709370e0c8aaa7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e98172395adb31dce58899437b11cfc389660e9f2d2a818c90adda054db6798d)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCellArn")
    def attr_cell_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the cell.

        :cloudformationAttribute: CellArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCellArn"))

    @builtins.property
    @jsii.member(jsii_name="attrParentReadinessScopes")
    def attr_parent_readiness_scopes(self) -> typing.List[builtins.str]:
        '''The readiness scope for the cell, which can be a cell Amazon Resource Name (ARN) or a recovery group ARN.

        This is a list but currently can have only one element.

        :cloudformationAttribute: ParentReadinessScopes
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrParentReadinessScopes"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A collection of tags associated with a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-cell.html#cfn-route53recoveryreadiness-cell-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="cellName")
    def cell_name(self) -> typing.Optional[builtins.str]:
        '''The name of the cell to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-cell.html#cfn-route53recoveryreadiness-cell-cellname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cellName"))

    @cell_name.setter
    def cell_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__766872b5a82b2a0ffe6d8ac73cf4f14330e2a0fac5bacc2ae60b235f42f1cec3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cellName", value)

    @builtins.property
    @jsii.member(jsii_name="cells")
    def cells(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of cell Amazon Resource Names (ARNs) contained within this cell, for use in nested cells.

        For example, Availability Zones within specific AWS Regions .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-cell.html#cfn-route53recoveryreadiness-cell-cells
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cells"))

    @cells.setter
    def cells(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a4305bf57aef9afa59e0e6c80df5b9dd6e0620dacb43e8225a4b5539319ff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cells", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53recoveryreadiness.CfnCellProps",
    jsii_struct_bases=[],
    name_mapping={"cell_name": "cellName", "cells": "cells", "tags": "tags"},
)
class CfnCellProps:
    def __init__(
        self,
        *,
        cell_name: typing.Optional[builtins.str] = None,
        cells: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnCell``.

        :param cell_name: The name of the cell to create.
        :param cells: A list of cell Amazon Resource Names (ARNs) contained within this cell, for use in nested cells. For example, Availability Zones within specific AWS Regions .
        :param tags: A collection of tags associated with a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-cell.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_route53recoveryreadiness as route53recoveryreadiness
            
            cfn_cell_props = route53recoveryreadiness.CfnCellProps(
                cell_name="cellName",
                cells=["cells"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf52a50cdde3a3bd02e61fddb85a82969e78251df2f06fb6ad904eea2ec7539e)
            check_type(argname="argument cell_name", value=cell_name, expected_type=type_hints["cell_name"])
            check_type(argname="argument cells", value=cells, expected_type=type_hints["cells"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cell_name is not None:
            self._values["cell_name"] = cell_name
        if cells is not None:
            self._values["cells"] = cells
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def cell_name(self) -> typing.Optional[builtins.str]:
        '''The name of the cell to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-cell.html#cfn-route53recoveryreadiness-cell-cellname
        '''
        result = self._values.get("cell_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cells(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of cell Amazon Resource Names (ARNs) contained within this cell, for use in nested cells.

        For example, Availability Zones within specific AWS Regions .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-cell.html#cfn-route53recoveryreadiness-cell-cells
        '''
        result = self._values.get("cells")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A collection of tags associated with a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-cell.html#cfn-route53recoveryreadiness-cell-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCellProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnReadinessCheck(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53recoveryreadiness.CfnReadinessCheck",
):
    '''A CloudFormation ``AWS::Route53RecoveryReadiness::ReadinessCheck``.

    Creates a readiness check in an account. A readiness check monitors a resource set in your application, such as a set of Amazon Aurora instances, that Application Recovery Controller is auditing recovery readiness for. The audits run once every minute on every resource that's associated with a readiness check.

    :cloudformationResource: AWS::Route53RecoveryReadiness::ReadinessCheck
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-readinesscheck.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_route53recoveryreadiness as route53recoveryreadiness
        
        cfn_readiness_check = route53recoveryreadiness.CfnReadinessCheck(self, "MyCfnReadinessCheck",
            readiness_check_name="readinessCheckName",
            resource_set_name="resourceSetName",
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
        readiness_check_name: typing.Optional[builtins.str] = None,
        resource_set_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Route53RecoveryReadiness::ReadinessCheck``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param readiness_check_name: The name of the readiness check to create.
        :param resource_set_name: The name of the resource set to check.
        :param tags: A collection of tags associated with a resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d0e9da9f4ba6bb564b96f152d7c3494446de3bacdf0931e328096d1199e6356)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnReadinessCheckProps(
            readiness_check_name=readiness_check_name,
            resource_set_name=resource_set_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1ef51553e4df6e5a8f50f6dfc8e14805f62841451b8a18b4bec758db79bf00c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91754d67960bc134c0b3059e674816cb8fbe966d32f60751ead5fa09ce140a2c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrReadinessCheckArn")
    def attr_readiness_check_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the readiness check.

        :cloudformationAttribute: ReadinessCheckArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrReadinessCheckArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A collection of tags associated with a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-readinesscheck.html#cfn-route53recoveryreadiness-readinesscheck-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="readinessCheckName")
    def readiness_check_name(self) -> typing.Optional[builtins.str]:
        '''The name of the readiness check to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-readinesscheck.html#cfn-route53recoveryreadiness-readinesscheck-readinesscheckname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readinessCheckName"))

    @readiness_check_name.setter
    def readiness_check_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5b8920d3fbd1c702fa821fb2e8b1e6980fa69b9cc60086ba1973d4a03ff53fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readinessCheckName", value)

    @builtins.property
    @jsii.member(jsii_name="resourceSetName")
    def resource_set_name(self) -> typing.Optional[builtins.str]:
        '''The name of the resource set to check.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-readinesscheck.html#cfn-route53recoveryreadiness-readinesscheck-resourcesetname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceSetName"))

    @resource_set_name.setter
    def resource_set_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75f6a8f2843e45953863f3b6ff4b018bdf90216ceac0caad9c4f0d8c5f34b4b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceSetName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53recoveryreadiness.CfnReadinessCheckProps",
    jsii_struct_bases=[],
    name_mapping={
        "readiness_check_name": "readinessCheckName",
        "resource_set_name": "resourceSetName",
        "tags": "tags",
    },
)
class CfnReadinessCheckProps:
    def __init__(
        self,
        *,
        readiness_check_name: typing.Optional[builtins.str] = None,
        resource_set_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnReadinessCheck``.

        :param readiness_check_name: The name of the readiness check to create.
        :param resource_set_name: The name of the resource set to check.
        :param tags: A collection of tags associated with a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-readinesscheck.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_route53recoveryreadiness as route53recoveryreadiness
            
            cfn_readiness_check_props = route53recoveryreadiness.CfnReadinessCheckProps(
                readiness_check_name="readinessCheckName",
                resource_set_name="resourceSetName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b82f5bb55d7175c31e6652da68e49d94d6875cb76b07c6086aadacb4bc0336a)
            check_type(argname="argument readiness_check_name", value=readiness_check_name, expected_type=type_hints["readiness_check_name"])
            check_type(argname="argument resource_set_name", value=resource_set_name, expected_type=type_hints["resource_set_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if readiness_check_name is not None:
            self._values["readiness_check_name"] = readiness_check_name
        if resource_set_name is not None:
            self._values["resource_set_name"] = resource_set_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def readiness_check_name(self) -> typing.Optional[builtins.str]:
        '''The name of the readiness check to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-readinesscheck.html#cfn-route53recoveryreadiness-readinesscheck-readinesscheckname
        '''
        result = self._values.get("readiness_check_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_set_name(self) -> typing.Optional[builtins.str]:
        '''The name of the resource set to check.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-readinesscheck.html#cfn-route53recoveryreadiness-readinesscheck-resourcesetname
        '''
        result = self._values.get("resource_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A collection of tags associated with a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-readinesscheck.html#cfn-route53recoveryreadiness-readinesscheck-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReadinessCheckProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRecoveryGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53recoveryreadiness.CfnRecoveryGroup",
):
    '''A CloudFormation ``AWS::Route53RecoveryReadiness::RecoveryGroup``.

    Creates a recovery group in an account. A recovery group corresponds to an application and includes a list of the cells that make up the application.

    :cloudformationResource: AWS::Route53RecoveryReadiness::RecoveryGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-recoverygroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_route53recoveryreadiness as route53recoveryreadiness
        
        cfn_recovery_group = route53recoveryreadiness.CfnRecoveryGroup(self, "MyCfnRecoveryGroup",
            cells=["cells"],
            recovery_group_name="recoveryGroupName",
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
        cells: typing.Optional[typing.Sequence[builtins.str]] = None,
        recovery_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Route53RecoveryReadiness::RecoveryGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cells: A list of the cell Amazon Resource Names (ARNs) in the recovery group.
        :param recovery_group_name: The name of the recovery group to create.
        :param tags: A collection of tags associated with a resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f9406d9c2f45aa476d0ee8c42fffa1adc07e5ed89c3c02a1a399ac500209b0e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRecoveryGroupProps(
            cells=cells, recovery_group_name=recovery_group_name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6693b956ad78984ca3fb88ff53e6b60bedff96986f4c194e715a2d0b22046a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bc333755d9f289b824a275b1861ea2829e8541de4a208d8412a160f4a18ea10)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrRecoveryGroupArn")
    def attr_recovery_group_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the recovery group.

        :cloudformationAttribute: RecoveryGroupArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRecoveryGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A collection of tags associated with a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-recoverygroup.html#cfn-route53recoveryreadiness-recoverygroup-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="cells")
    def cells(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the cell Amazon Resource Names (ARNs) in the recovery group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-recoverygroup.html#cfn-route53recoveryreadiness-recoverygroup-cells
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cells"))

    @cells.setter
    def cells(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__775f2ef5609f39ca5fbbe9c211aec6ba37088bd682db51039b8d5a64762fd7a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cells", value)

    @builtins.property
    @jsii.member(jsii_name="recoveryGroupName")
    def recovery_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the recovery group to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-recoverygroup.html#cfn-route53recoveryreadiness-recoverygroup-recoverygroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recoveryGroupName"))

    @recovery_group_name.setter
    def recovery_group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__527cb07915b0feb400933c65084da7a609bf55c2a9c20e06e8be89de76c4d941)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryGroupName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53recoveryreadiness.CfnRecoveryGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "cells": "cells",
        "recovery_group_name": "recoveryGroupName",
        "tags": "tags",
    },
)
class CfnRecoveryGroupProps:
    def __init__(
        self,
        *,
        cells: typing.Optional[typing.Sequence[builtins.str]] = None,
        recovery_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRecoveryGroup``.

        :param cells: A list of the cell Amazon Resource Names (ARNs) in the recovery group.
        :param recovery_group_name: The name of the recovery group to create.
        :param tags: A collection of tags associated with a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-recoverygroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_route53recoveryreadiness as route53recoveryreadiness
            
            cfn_recovery_group_props = route53recoveryreadiness.CfnRecoveryGroupProps(
                cells=["cells"],
                recovery_group_name="recoveryGroupName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba5d2a209dd5cbae7ef71604a801ba6f5b550663c10a8a418365dd70b0ea2b8f)
            check_type(argname="argument cells", value=cells, expected_type=type_hints["cells"])
            check_type(argname="argument recovery_group_name", value=recovery_group_name, expected_type=type_hints["recovery_group_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cells is not None:
            self._values["cells"] = cells
        if recovery_group_name is not None:
            self._values["recovery_group_name"] = recovery_group_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def cells(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the cell Amazon Resource Names (ARNs) in the recovery group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-recoverygroup.html#cfn-route53recoveryreadiness-recoverygroup-cells
        '''
        result = self._values.get("cells")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def recovery_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the recovery group to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-recoverygroup.html#cfn-route53recoveryreadiness-recoverygroup-recoverygroupname
        '''
        result = self._values.get("recovery_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A collection of tags associated with a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-recoverygroup.html#cfn-route53recoveryreadiness-recoverygroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRecoveryGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnResourceSet(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53recoveryreadiness.CfnResourceSet",
):
    '''A CloudFormation ``AWS::Route53RecoveryReadiness::ResourceSet``.

    Creates a resource set. A resource set is a set of resources of one type that span multiple cells. You can associate a resource set with a readiness check to monitor the resources for failover readiness.

    :cloudformationResource: AWS::Route53RecoveryReadiness::ResourceSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_route53recoveryreadiness as route53recoveryreadiness
        
        cfn_resource_set = route53recoveryreadiness.CfnResourceSet(self, "MyCfnResourceSet",
            resources=[route53recoveryreadiness.CfnResourceSet.ResourceProperty(
                component_id="componentId",
                dns_target_resource=route53recoveryreadiness.CfnResourceSet.DNSTargetResourceProperty(
                    domain_name="domainName",
                    hosted_zone_arn="hostedZoneArn",
                    record_set_id="recordSetId",
                    record_type="recordType",
                    target_resource=route53recoveryreadiness.CfnResourceSet.TargetResourceProperty(
                        nlb_resource=route53recoveryreadiness.CfnResourceSet.NLBResourceProperty(
                            arn="arn"
                        ),
                        r53_resource=route53recoveryreadiness.CfnResourceSet.R53ResourceRecordProperty(
                            domain_name="domainName",
                            record_set_id="recordSetId"
                        )
                    )
                ),
                readiness_scopes=["readinessScopes"],
                resource_arn="resourceArn"
            )],
            resource_set_type="resourceSetType",
        
            # the properties below are optional
            resource_set_name="resourceSetName",
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
        resources: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union["CfnResourceSet.ResourceProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
        resource_set_type: builtins.str,
        resource_set_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Route53RecoveryReadiness::ResourceSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resources: A list of resource objects in the resource set.
        :param resource_set_type: The resource type of the resources in the resource set. Enter one of the following values for resource type:. AWS::AutoScaling::AutoScalingGroup, AWS::CloudWatch::Alarm, AWS::EC2::CustomerGateway, AWS::DynamoDB::Table, AWS::EC2::Volume, AWS::ElasticLoadBalancing::LoadBalancer, AWS::ElasticLoadBalancingV2::LoadBalancer, AWS::MSK::Cluster, AWS::RDS::DBCluster, AWS::Route53::HealthCheck, AWS::SQS::Queue, AWS::SNS::Topic, AWS::SNS::Subscription, AWS::EC2::VPC, AWS::EC2::VPNConnection, AWS::EC2::VPNGateway, AWS::Route53RecoveryReadiness::DNSTargetResource. Note that AWS::Route53RecoveryReadiness::DNSTargetResource is only used for this setting. It isn't an actual AWS CloudFormation resource type.
        :param resource_set_name: The name of the resource set to create.
        :param tags: A tag to associate with the parameters for a resource set.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b257d03ffc58b055905ce922b1f3b2a4a8f1cd53e34c58637034e5d75944434)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourceSetProps(
            resources=resources,
            resource_set_type=resource_set_type,
            resource_set_name=resource_set_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1f69c32ffab0fbadd9b7ac7eea2fa8de3341f36d2b2ea76bd8b506b982526c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb10cefab7d5959e5df301c3e85af513faa4d379fd28a370496bd8de5a769e71)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrResourceSetArn")
    def attr_resource_set_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the resource set.

        :cloudformationAttribute: ResourceSetArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResourceSetArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A tag to associate with the parameters for a resource set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html#cfn-route53recoveryreadiness-resourceset-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnResourceSet.ResourceProperty", _aws_cdk_core_f4b25747.IResolvable]]]:
        '''A list of resource objects in the resource set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html#cfn-route53recoveryreadiness-resourceset-resources
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnResourceSet.ResourceProperty", _aws_cdk_core_f4b25747.IResolvable]]], jsii.get(self, "resources"))

    @resources.setter
    def resources(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnResourceSet.ResourceProperty", _aws_cdk_core_f4b25747.IResolvable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bc7ac36e7e0272a458a1018eab32f75ba939098002cb6da28e508c2a4fe680c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value)

    @builtins.property
    @jsii.member(jsii_name="resourceSetType")
    def resource_set_type(self) -> builtins.str:
        '''The resource type of the resources in the resource set. Enter one of the following values for resource type:.

        AWS::AutoScaling::AutoScalingGroup, AWS::CloudWatch::Alarm, AWS::EC2::CustomerGateway, AWS::DynamoDB::Table, AWS::EC2::Volume, AWS::ElasticLoadBalancing::LoadBalancer, AWS::ElasticLoadBalancingV2::LoadBalancer, AWS::MSK::Cluster, AWS::RDS::DBCluster, AWS::Route53::HealthCheck, AWS::SQS::Queue, AWS::SNS::Topic, AWS::SNS::Subscription, AWS::EC2::VPC, AWS::EC2::VPNConnection, AWS::EC2::VPNGateway, AWS::Route53RecoveryReadiness::DNSTargetResource.

        Note that AWS::Route53RecoveryReadiness::DNSTargetResource is only used for this setting. It isn't an actual AWS CloudFormation resource type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html#cfn-route53recoveryreadiness-resourceset-resourcesettype
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceSetType"))

    @resource_set_type.setter
    def resource_set_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc9b8300128f5fbb2959bfda399fe9a0f1929bd71d17403fd6c2368331c950ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceSetType", value)

    @builtins.property
    @jsii.member(jsii_name="resourceSetName")
    def resource_set_name(self) -> typing.Optional[builtins.str]:
        '''The name of the resource set to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html#cfn-route53recoveryreadiness-resourceset-resourcesetname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceSetName"))

    @resource_set_name.setter
    def resource_set_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d07fdf282431da7077f2eaa20bbb04277a2e91ba62cc311c4a4415e0b4f3ae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceSetName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-route53recoveryreadiness.CfnResourceSet.DNSTargetResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "domain_name": "domainName",
            "hosted_zone_arn": "hostedZoneArn",
            "record_set_id": "recordSetId",
            "record_type": "recordType",
            "target_resource": "targetResource",
        },
    )
    class DNSTargetResourceProperty:
        def __init__(
            self,
            *,
            domain_name: typing.Optional[builtins.str] = None,
            hosted_zone_arn: typing.Optional[builtins.str] = None,
            record_set_id: typing.Optional[builtins.str] = None,
            record_type: typing.Optional[builtins.str] = None,
            target_resource: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceSet.TargetResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A component for DNS/routing control readiness checks and architecture checks.

            :param domain_name: The domain name that acts as an ingress point to a portion of the customer application.
            :param hosted_zone_arn: The hosted zone Amazon Resource Name (ARN) that contains the DNS record with the provided name of the target resource.
            :param record_set_id: The Route 53 record set ID that uniquely identifies a DNS record, given a name and a type.
            :param record_type: The type of DNS record of the target resource.
            :param target_resource: The target resource that the Route 53 record points to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-dnstargetresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_route53recoveryreadiness as route53recoveryreadiness
                
                d_nSTarget_resource_property = route53recoveryreadiness.CfnResourceSet.DNSTargetResourceProperty(
                    domain_name="domainName",
                    hosted_zone_arn="hostedZoneArn",
                    record_set_id="recordSetId",
                    record_type="recordType",
                    target_resource=route53recoveryreadiness.CfnResourceSet.TargetResourceProperty(
                        nlb_resource=route53recoveryreadiness.CfnResourceSet.NLBResourceProperty(
                            arn="arn"
                        ),
                        r53_resource=route53recoveryreadiness.CfnResourceSet.R53ResourceRecordProperty(
                            domain_name="domainName",
                            record_set_id="recordSetId"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4cf25dd0fd6283d084f039c71c94a33fd31e9e460de932e91010359a01a8eb6e)
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument hosted_zone_arn", value=hosted_zone_arn, expected_type=type_hints["hosted_zone_arn"])
                check_type(argname="argument record_set_id", value=record_set_id, expected_type=type_hints["record_set_id"])
                check_type(argname="argument record_type", value=record_type, expected_type=type_hints["record_type"])
                check_type(argname="argument target_resource", value=target_resource, expected_type=type_hints["target_resource"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_name is not None:
                self._values["domain_name"] = domain_name
            if hosted_zone_arn is not None:
                self._values["hosted_zone_arn"] = hosted_zone_arn
            if record_set_id is not None:
                self._values["record_set_id"] = record_set_id
            if record_type is not None:
                self._values["record_type"] = record_type
            if target_resource is not None:
                self._values["target_resource"] = target_resource

        @builtins.property
        def domain_name(self) -> typing.Optional[builtins.str]:
            '''The domain name that acts as an ingress point to a portion of the customer application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-dnstargetresource.html#cfn-route53recoveryreadiness-resourceset-dnstargetresource-domainname
            '''
            result = self._values.get("domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_arn(self) -> typing.Optional[builtins.str]:
            '''The hosted zone Amazon Resource Name (ARN) that contains the DNS record with the provided name of the target resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-dnstargetresource.html#cfn-route53recoveryreadiness-resourceset-dnstargetresource-hostedzonearn
            '''
            result = self._values.get("hosted_zone_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def record_set_id(self) -> typing.Optional[builtins.str]:
            '''The Route 53 record set ID that uniquely identifies a DNS record, given a name and a type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-dnstargetresource.html#cfn-route53recoveryreadiness-resourceset-dnstargetresource-recordsetid
            '''
            result = self._values.get("record_set_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def record_type(self) -> typing.Optional[builtins.str]:
            '''The type of DNS record of the target resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-dnstargetresource.html#cfn-route53recoveryreadiness-resourceset-dnstargetresource-recordtype
            '''
            result = self._values.get("record_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_resource(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceSet.TargetResourceProperty"]]:
            '''The target resource that the Route 53 record points to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-dnstargetresource.html#cfn-route53recoveryreadiness-resourceset-dnstargetresource-targetresource
            '''
            result = self._values.get("target_resource")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceSet.TargetResourceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DNSTargetResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-route53recoveryreadiness.CfnResourceSet.NLBResourceProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class NLBResourceProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''The Network Load Balancer resource that a DNS target resource points to.

            :param arn: The Network Load Balancer resource Amazon Resource Name (ARN).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-nlbresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_route53recoveryreadiness as route53recoveryreadiness
                
                n_lBResource_property = route53recoveryreadiness.CfnResourceSet.NLBResourceProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8b9255128a114a0f336c0191f504126b961c5bc5020825525f23f98dc018f278)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Network Load Balancer resource Amazon Resource Name (ARN).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-nlbresource.html#cfn-route53recoveryreadiness-resourceset-nlbresource-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NLBResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-route53recoveryreadiness.CfnResourceSet.R53ResourceRecordProperty",
        jsii_struct_bases=[],
        name_mapping={"domain_name": "domainName", "record_set_id": "recordSetId"},
    )
    class R53ResourceRecordProperty:
        def __init__(
            self,
            *,
            domain_name: typing.Optional[builtins.str] = None,
            record_set_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Route 53 resource that a DNS target resource record points to.

            :param domain_name: The DNS target domain name.
            :param record_set_id: The Route 53 Resource Record Set ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-r53resourcerecord.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_route53recoveryreadiness as route53recoveryreadiness
                
                r53_resource_record_property = route53recoveryreadiness.CfnResourceSet.R53ResourceRecordProperty(
                    domain_name="domainName",
                    record_set_id="recordSetId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2b103e19353e28f82c0975c397eb1148c0407b59398e7fa9fb082616e9bf552c)
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument record_set_id", value=record_set_id, expected_type=type_hints["record_set_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_name is not None:
                self._values["domain_name"] = domain_name
            if record_set_id is not None:
                self._values["record_set_id"] = record_set_id

        @builtins.property
        def domain_name(self) -> typing.Optional[builtins.str]:
            '''The DNS target domain name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-r53resourcerecord.html#cfn-route53recoveryreadiness-resourceset-r53resourcerecord-domainname
            '''
            result = self._values.get("domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def record_set_id(self) -> typing.Optional[builtins.str]:
            '''The Route 53 Resource Record Set ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-r53resourcerecord.html#cfn-route53recoveryreadiness-resourceset-r53resourcerecord-recordsetid
            '''
            result = self._values.get("record_set_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "R53ResourceRecordProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-route53recoveryreadiness.CfnResourceSet.ResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_id": "componentId",
            "dns_target_resource": "dnsTargetResource",
            "readiness_scopes": "readinessScopes",
            "resource_arn": "resourceArn",
        },
    )
    class ResourceProperty:
        def __init__(
            self,
            *,
            component_id: typing.Optional[builtins.str] = None,
            dns_target_resource: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceSet.DNSTargetResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            readiness_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
            resource_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The resource element of a resource set.

            :param component_id: The component identifier of the resource, generated when DNS target resource is used.
            :param dns_target_resource: A component for DNS/routing control readiness checks. This is a required setting when ``ResourceSet`` ``ResourceSetType`` is set to ``AWS::Route53RecoveryReadiness::DNSTargetResource`` . Do not set it for any other ``ResourceSetType`` setting.
            :param readiness_scopes: The recovery group Amazon Resource Name (ARN) or the cell ARN that the readiness checks for this resource set are scoped to.
            :param resource_arn: The Amazon Resource Name (ARN) of the AWS resource. This is a required setting for all ``ResourceSet`` ``ResourceSetType`` settings except ``AWS::Route53RecoveryReadiness::DNSTargetResource`` . Do not set this when ``ResourceSetType`` is set to ``AWS::Route53RecoveryReadiness::DNSTargetResource`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-resource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_route53recoveryreadiness as route53recoveryreadiness
                
                resource_property = route53recoveryreadiness.CfnResourceSet.ResourceProperty(
                    component_id="componentId",
                    dns_target_resource=route53recoveryreadiness.CfnResourceSet.DNSTargetResourceProperty(
                        domain_name="domainName",
                        hosted_zone_arn="hostedZoneArn",
                        record_set_id="recordSetId",
                        record_type="recordType",
                        target_resource=route53recoveryreadiness.CfnResourceSet.TargetResourceProperty(
                            nlb_resource=route53recoveryreadiness.CfnResourceSet.NLBResourceProperty(
                                arn="arn"
                            ),
                            r53_resource=route53recoveryreadiness.CfnResourceSet.R53ResourceRecordProperty(
                                domain_name="domainName",
                                record_set_id="recordSetId"
                            )
                        )
                    ),
                    readiness_scopes=["readinessScopes"],
                    resource_arn="resourceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7a26506b8a194203a820017e64388456df627df6c626226e4b5771f2355ebd78)
                check_type(argname="argument component_id", value=component_id, expected_type=type_hints["component_id"])
                check_type(argname="argument dns_target_resource", value=dns_target_resource, expected_type=type_hints["dns_target_resource"])
                check_type(argname="argument readiness_scopes", value=readiness_scopes, expected_type=type_hints["readiness_scopes"])
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_id is not None:
                self._values["component_id"] = component_id
            if dns_target_resource is not None:
                self._values["dns_target_resource"] = dns_target_resource
            if readiness_scopes is not None:
                self._values["readiness_scopes"] = readiness_scopes
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn

        @builtins.property
        def component_id(self) -> typing.Optional[builtins.str]:
            '''The component identifier of the resource, generated when DNS target resource is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-resource.html#cfn-route53recoveryreadiness-resourceset-resource-componentid
            '''
            result = self._values.get("component_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dns_target_resource(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceSet.DNSTargetResourceProperty"]]:
            '''A component for DNS/routing control readiness checks.

            This is a required setting when ``ResourceSet`` ``ResourceSetType`` is set to ``AWS::Route53RecoveryReadiness::DNSTargetResource`` . Do not set it for any other ``ResourceSetType`` setting.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-resource.html#cfn-route53recoveryreadiness-resourceset-resource-dnstargetresource
            '''
            result = self._values.get("dns_target_resource")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceSet.DNSTargetResourceProperty"]], result)

        @builtins.property
        def readiness_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The recovery group Amazon Resource Name (ARN) or the cell ARN that the readiness checks for this resource set are scoped to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-resource.html#cfn-route53recoveryreadiness-resourceset-resource-readinessscopes
            '''
            result = self._values.get("readiness_scopes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS resource.

            This is a required setting for all ``ResourceSet`` ``ResourceSetType`` settings except ``AWS::Route53RecoveryReadiness::DNSTargetResource`` . Do not set this when ``ResourceSetType`` is set to ``AWS::Route53RecoveryReadiness::DNSTargetResource`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-resource.html#cfn-route53recoveryreadiness-resourceset-resource-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-route53recoveryreadiness.CfnResourceSet.TargetResourceProperty",
        jsii_struct_bases=[],
        name_mapping={"nlb_resource": "nlbResource", "r53_resource": "r53Resource"},
    )
    class TargetResourceProperty:
        def __init__(
            self,
            *,
            nlb_resource: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceSet.NLBResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            r53_resource: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceSet.R53ResourceRecordProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The target resource that the Route 53 record points to.

            :param nlb_resource: The Network Load Balancer resource that a DNS target resource points to.
            :param r53_resource: The Route 53 resource that a DNS target resource record points to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-targetresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_route53recoveryreadiness as route53recoveryreadiness
                
                target_resource_property = route53recoveryreadiness.CfnResourceSet.TargetResourceProperty(
                    nlb_resource=route53recoveryreadiness.CfnResourceSet.NLBResourceProperty(
                        arn="arn"
                    ),
                    r53_resource=route53recoveryreadiness.CfnResourceSet.R53ResourceRecordProperty(
                        domain_name="domainName",
                        record_set_id="recordSetId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__13466e42949f7a4052609589cf5d993beacc065d45d3c8e7556e9193faf8a458)
                check_type(argname="argument nlb_resource", value=nlb_resource, expected_type=type_hints["nlb_resource"])
                check_type(argname="argument r53_resource", value=r53_resource, expected_type=type_hints["r53_resource"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if nlb_resource is not None:
                self._values["nlb_resource"] = nlb_resource
            if r53_resource is not None:
                self._values["r53_resource"] = r53_resource

        @builtins.property
        def nlb_resource(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceSet.NLBResourceProperty"]]:
            '''The Network Load Balancer resource that a DNS target resource points to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-targetresource.html#cfn-route53recoveryreadiness-resourceset-targetresource-nlbresource
            '''
            result = self._values.get("nlb_resource")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceSet.NLBResourceProperty"]], result)

        @builtins.property
        def r53_resource(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceSet.R53ResourceRecordProperty"]]:
            '''The Route 53 resource that a DNS target resource record points to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-targetresource.html#cfn-route53recoveryreadiness-resourceset-targetresource-r53resource
            '''
            result = self._values.get("r53_resource")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceSet.R53ResourceRecordProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53recoveryreadiness.CfnResourceSetProps",
    jsii_struct_bases=[],
    name_mapping={
        "resources": "resources",
        "resource_set_type": "resourceSetType",
        "resource_set_name": "resourceSetName",
        "tags": "tags",
    },
)
class CfnResourceSetProps:
    def __init__(
        self,
        *,
        resources: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnResourceSet.ResourceProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
        resource_set_type: builtins.str,
        resource_set_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnResourceSet``.

        :param resources: A list of resource objects in the resource set.
        :param resource_set_type: The resource type of the resources in the resource set. Enter one of the following values for resource type:. AWS::AutoScaling::AutoScalingGroup, AWS::CloudWatch::Alarm, AWS::EC2::CustomerGateway, AWS::DynamoDB::Table, AWS::EC2::Volume, AWS::ElasticLoadBalancing::LoadBalancer, AWS::ElasticLoadBalancingV2::LoadBalancer, AWS::MSK::Cluster, AWS::RDS::DBCluster, AWS::Route53::HealthCheck, AWS::SQS::Queue, AWS::SNS::Topic, AWS::SNS::Subscription, AWS::EC2::VPC, AWS::EC2::VPNConnection, AWS::EC2::VPNGateway, AWS::Route53RecoveryReadiness::DNSTargetResource. Note that AWS::Route53RecoveryReadiness::DNSTargetResource is only used for this setting. It isn't an actual AWS CloudFormation resource type.
        :param resource_set_name: The name of the resource set to create.
        :param tags: A tag to associate with the parameters for a resource set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_route53recoveryreadiness as route53recoveryreadiness
            
            cfn_resource_set_props = route53recoveryreadiness.CfnResourceSetProps(
                resources=[route53recoveryreadiness.CfnResourceSet.ResourceProperty(
                    component_id="componentId",
                    dns_target_resource=route53recoveryreadiness.CfnResourceSet.DNSTargetResourceProperty(
                        domain_name="domainName",
                        hosted_zone_arn="hostedZoneArn",
                        record_set_id="recordSetId",
                        record_type="recordType",
                        target_resource=route53recoveryreadiness.CfnResourceSet.TargetResourceProperty(
                            nlb_resource=route53recoveryreadiness.CfnResourceSet.NLBResourceProperty(
                                arn="arn"
                            ),
                            r53_resource=route53recoveryreadiness.CfnResourceSet.R53ResourceRecordProperty(
                                domain_name="domainName",
                                record_set_id="recordSetId"
                            )
                        )
                    ),
                    readiness_scopes=["readinessScopes"],
                    resource_arn="resourceArn"
                )],
                resource_set_type="resourceSetType",
            
                # the properties below are optional
                resource_set_name="resourceSetName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__408ba82ff39834ae0b00cb405274466f24be6e411d17ed0cca228e35f19bb110)
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument resource_set_type", value=resource_set_type, expected_type=type_hints["resource_set_type"])
            check_type(argname="argument resource_set_name", value=resource_set_name, expected_type=type_hints["resource_set_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resources": resources,
            "resource_set_type": resource_set_type,
        }
        if resource_set_name is not None:
            self._values["resource_set_name"] = resource_set_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def resources(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnResourceSet.ResourceProperty, _aws_cdk_core_f4b25747.IResolvable]]]:
        '''A list of resource objects in the resource set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html#cfn-route53recoveryreadiness-resourceset-resources
        '''
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnResourceSet.ResourceProperty, _aws_cdk_core_f4b25747.IResolvable]]], result)

    @builtins.property
    def resource_set_type(self) -> builtins.str:
        '''The resource type of the resources in the resource set. Enter one of the following values for resource type:.

        AWS::AutoScaling::AutoScalingGroup, AWS::CloudWatch::Alarm, AWS::EC2::CustomerGateway, AWS::DynamoDB::Table, AWS::EC2::Volume, AWS::ElasticLoadBalancing::LoadBalancer, AWS::ElasticLoadBalancingV2::LoadBalancer, AWS::MSK::Cluster, AWS::RDS::DBCluster, AWS::Route53::HealthCheck, AWS::SQS::Queue, AWS::SNS::Topic, AWS::SNS::Subscription, AWS::EC2::VPC, AWS::EC2::VPNConnection, AWS::EC2::VPNGateway, AWS::Route53RecoveryReadiness::DNSTargetResource.

        Note that AWS::Route53RecoveryReadiness::DNSTargetResource is only used for this setting. It isn't an actual AWS CloudFormation resource type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html#cfn-route53recoveryreadiness-resourceset-resourcesettype
        '''
        result = self._values.get("resource_set_type")
        assert result is not None, "Required property 'resource_set_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_set_name(self) -> typing.Optional[builtins.str]:
        '''The name of the resource set to create.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html#cfn-route53recoveryreadiness-resourceset-resourcesetname
        '''
        result = self._values.get("resource_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A tag to associate with the parameters for a resource set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html#cfn-route53recoveryreadiness-resourceset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnCell",
    "CfnCellProps",
    "CfnReadinessCheck",
    "CfnReadinessCheckProps",
    "CfnRecoveryGroup",
    "CfnRecoveryGroupProps",
    "CfnResourceSet",
    "CfnResourceSetProps",
]

publication.publish()

def _typecheckingstub__dc2e9ddd87e6b794e10435fcc379020436acd7c060581bf0990ce29855723663(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    cell_name: typing.Optional[builtins.str] = None,
    cells: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c22be4dc98cdd514d243cf61c6d26275aae23a87d6728bae709370e0c8aaa7d(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e98172395adb31dce58899437b11cfc389660e9f2d2a818c90adda054db6798d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__766872b5a82b2a0ffe6d8ac73cf4f14330e2a0fac5bacc2ae60b235f42f1cec3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a4305bf57aef9afa59e0e6c80df5b9dd6e0620dacb43e8225a4b5539319ff5(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf52a50cdde3a3bd02e61fddb85a82969e78251df2f06fb6ad904eea2ec7539e(
    *,
    cell_name: typing.Optional[builtins.str] = None,
    cells: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0e9da9f4ba6bb564b96f152d7c3494446de3bacdf0931e328096d1199e6356(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    readiness_check_name: typing.Optional[builtins.str] = None,
    resource_set_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ef51553e4df6e5a8f50f6dfc8e14805f62841451b8a18b4bec758db79bf00c(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91754d67960bc134c0b3059e674816cb8fbe966d32f60751ead5fa09ce140a2c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5b8920d3fbd1c702fa821fb2e8b1e6980fa69b9cc60086ba1973d4a03ff53fb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75f6a8f2843e45953863f3b6ff4b018bdf90216ceac0caad9c4f0d8c5f34b4b1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b82f5bb55d7175c31e6652da68e49d94d6875cb76b07c6086aadacb4bc0336a(
    *,
    readiness_check_name: typing.Optional[builtins.str] = None,
    resource_set_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f9406d9c2f45aa476d0ee8c42fffa1adc07e5ed89c3c02a1a399ac500209b0e(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    cells: typing.Optional[typing.Sequence[builtins.str]] = None,
    recovery_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6693b956ad78984ca3fb88ff53e6b60bedff96986f4c194e715a2d0b22046a7(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bc333755d9f289b824a275b1861ea2829e8541de4a208d8412a160f4a18ea10(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775f2ef5609f39ca5fbbe9c211aec6ba37088bd682db51039b8d5a64762fd7a3(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__527cb07915b0feb400933c65084da7a609bf55c2a9c20e06e8be89de76c4d941(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba5d2a209dd5cbae7ef71604a801ba6f5b550663c10a8a418365dd70b0ea2b8f(
    *,
    cells: typing.Optional[typing.Sequence[builtins.str]] = None,
    recovery_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b257d03ffc58b055905ce922b1f3b2a4a8f1cd53e34c58637034e5d75944434(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    resources: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnResourceSet.ResourceProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
    resource_set_type: builtins.str,
    resource_set_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1f69c32ffab0fbadd9b7ac7eea2fa8de3341f36d2b2ea76bd8b506b982526c(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb10cefab7d5959e5df301c3e85af513faa4d379fd28a370496bd8de5a769e71(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc7ac36e7e0272a458a1018eab32f75ba939098002cb6da28e508c2a4fe680c(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnResourceSet.ResourceProperty, _aws_cdk_core_f4b25747.IResolvable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc9b8300128f5fbb2959bfda399fe9a0f1929bd71d17403fd6c2368331c950ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d07fdf282431da7077f2eaa20bbb04277a2e91ba62cc311c4a4415e0b4f3ae4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf25dd0fd6283d084f039c71c94a33fd31e9e460de932e91010359a01a8eb6e(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    hosted_zone_arn: typing.Optional[builtins.str] = None,
    record_set_id: typing.Optional[builtins.str] = None,
    record_type: typing.Optional[builtins.str] = None,
    target_resource: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceSet.TargetResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b9255128a114a0f336c0191f504126b961c5bc5020825525f23f98dc018f278(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b103e19353e28f82c0975c397eb1148c0407b59398e7fa9fb082616e9bf552c(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    record_set_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a26506b8a194203a820017e64388456df627df6c626226e4b5771f2355ebd78(
    *,
    component_id: typing.Optional[builtins.str] = None,
    dns_target_resource: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceSet.DNSTargetResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    readiness_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13466e42949f7a4052609589cf5d993beacc065d45d3c8e7556e9193faf8a458(
    *,
    nlb_resource: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceSet.NLBResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    r53_resource: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceSet.R53ResourceRecordProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408ba82ff39834ae0b00cb405274466f24be6e411d17ed0cca228e35f19bb110(
    *,
    resources: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnResourceSet.ResourceProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
    resource_set_type: builtins.str,
    resource_set_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
