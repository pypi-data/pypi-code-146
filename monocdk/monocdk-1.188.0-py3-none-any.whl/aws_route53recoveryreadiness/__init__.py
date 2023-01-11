'''
# AWS::Route53RecoveryReadiness Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as route53recoveryreadiness
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
class CfnCell(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53recoveryreadiness.CfnCell",
):
    '''A CloudFormation ``AWS::Route53RecoveryReadiness::Cell``.

    Creates a cell in an account.

    :cloudformationResource: AWS::Route53RecoveryReadiness::Cell
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-cell.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53recoveryreadiness as route53recoveryreadiness
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        cell_name: typing.Optional[builtins.str] = None,
        cells: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Route53RecoveryReadiness::Cell``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cell_name: The name of the cell to create.
        :param cells: A list of cell Amazon Resource Names (ARNs) contained within this cell, for use in nested cells. For example, Availability Zones within specific AWS Regions .
        :param tags: A collection of tags associated with a resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f1fc0c171fbcb7086f5f1ca48fff0312f7d383e9e119f20060320330f711067)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCellProps(cell_name=cell_name, cells=cells, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e7caf352c7f690a92e5c5981bb857ebfada99d536910de49e303ebec415b502)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23cdf7569e354aa85c52a9f06e5a6da00a012469fbb801ae08da7db7344a0ec2)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''A collection of tags associated with a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-cell.html#cfn-route53recoveryreadiness-cell-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__85e19ce29aad9cf1b109a592b5a63535736966f0788fe5a26ab65849e2da797f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e3adbb83195ebbe1f122d693f401c09c8790f42a3299bca5c1fb06ac50ef595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cells", value)


@jsii.data_type(
    jsii_type="monocdk.aws_route53recoveryreadiness.CfnCellProps",
    jsii_struct_bases=[],
    name_mapping={"cell_name": "cellName", "cells": "cells", "tags": "tags"},
)
class CfnCellProps:
    def __init__(
        self,
        *,
        cell_name: typing.Optional[builtins.str] = None,
        cells: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_route53recoveryreadiness as route53recoveryreadiness
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__84a0c2c07baccfd850236d4a1cffa00bc805bc9c6730b5dbb7d3371965e9541a)
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
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A collection of tags associated with a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-cell.html#cfn-route53recoveryreadiness-cell-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCellProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnReadinessCheck(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53recoveryreadiness.CfnReadinessCheck",
):
    '''A CloudFormation ``AWS::Route53RecoveryReadiness::ReadinessCheck``.

    Creates a readiness check in an account. A readiness check monitors a resource set in your application, such as a set of Amazon Aurora instances, that Application Recovery Controller is auditing recovery readiness for. The audits run once every minute on every resource that's associated with a readiness check.

    :cloudformationResource: AWS::Route53RecoveryReadiness::ReadinessCheck
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-readinesscheck.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53recoveryreadiness as route53recoveryreadiness
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        readiness_check_name: typing.Optional[builtins.str] = None,
        resource_set_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Route53RecoveryReadiness::ReadinessCheck``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param readiness_check_name: The name of the readiness check to create.
        :param resource_set_name: The name of the resource set to check.
        :param tags: A collection of tags associated with a resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f90c0fa2b82ccff3c40c0d2249b2fd925bf78c29280bd8e7ace6b9176c84bf91)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnReadinessCheckProps(
            readiness_check_name=readiness_check_name,
            resource_set_name=resource_set_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__353f963cb3b28cac741137e7b837785fb5bf6e7e980edf416b8dfb882690e738)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b608fa45248ae667d3b36b339f938d93b5bf1a715f2b4919776ef141684fae89)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''A collection of tags associated with a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-readinesscheck.html#cfn-route53recoveryreadiness-readinesscheck-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0218ba2f71cba1d5fe98177db9f79c45505c17c5113b1a4e9cbce33f38a2efed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c98ad06f971073c2d858553717bc3656d88df37e862a3366449fe2e51832db7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceSetName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_route53recoveryreadiness.CfnReadinessCheckProps",
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
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_route53recoveryreadiness as route53recoveryreadiness
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5cc9591e7fc8846dd0045cdf3e559d05ed722b143b73714004900d9e308c27b)
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
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A collection of tags associated with a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-readinesscheck.html#cfn-route53recoveryreadiness-readinesscheck-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReadinessCheckProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnRecoveryGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53recoveryreadiness.CfnRecoveryGroup",
):
    '''A CloudFormation ``AWS::Route53RecoveryReadiness::RecoveryGroup``.

    Creates a recovery group in an account. A recovery group corresponds to an application and includes a list of the cells that make up the application.

    :cloudformationResource: AWS::Route53RecoveryReadiness::RecoveryGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-recoverygroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53recoveryreadiness as route53recoveryreadiness
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        cells: typing.Optional[typing.Sequence[builtins.str]] = None,
        recovery_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Route53RecoveryReadiness::RecoveryGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cells: A list of the cell Amazon Resource Names (ARNs) in the recovery group.
        :param recovery_group_name: The name of the recovery group to create.
        :param tags: A collection of tags associated with a resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9c424198a99017d65047284ae5cd01df4cdb42d190ce68ff8f623c9e899c1e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRecoveryGroupProps(
            cells=cells, recovery_group_name=recovery_group_name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83a5c879572794c2de2d914708779e8209b12351ba566e6835309736dc0aed9d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d877aa5e7a01a3591d87c2799243dc486409dae74aca3a8d995cbd69cbefef7)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''A collection of tags associated with a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-recoverygroup.html#cfn-route53recoveryreadiness-recoverygroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__56188fe1b7d2f9db534b57fade34ee51969dfe0e1afdbc5f65040b85cad5f2c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f72cda09d84b4239e27aea9c552d660c45ac7ed8405a42f26ff6d0e9bcf22b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryGroupName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_route53recoveryreadiness.CfnRecoveryGroupProps",
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
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_route53recoveryreadiness as route53recoveryreadiness
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__9362839126196e5c0451ca734469c3e56c4ff23c69e2aa96f1f21a374f4f2311)
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
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A collection of tags associated with a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-recoverygroup.html#cfn-route53recoveryreadiness-recoverygroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRecoveryGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnResourceSet(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53recoveryreadiness.CfnResourceSet",
):
    '''A CloudFormation ``AWS::Route53RecoveryReadiness::ResourceSet``.

    Creates a resource set. A resource set is a set of resources of one type that span multiple cells. You can associate a resource set with a readiness check to monitor the resources for failover readiness.

    :cloudformationResource: AWS::Route53RecoveryReadiness::ResourceSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53recoveryreadiness as route53recoveryreadiness
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        resources: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnResourceSet.ResourceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        resource_set_type: builtins.str,
        resource_set_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__47a7a168d53601d968304c2f647cddbd92d1ef86ad06f14e93590eba948ace89)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f43f36d452494849870b457816a85593cab2d39abc24b55714918e457f06b983)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a30ad089f78bdd91ac003f3b954834d62f62421bf9653eb2dd59579888c45ce3)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''A tag to associate with the parameters for a resource set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html#cfn-route53recoveryreadiness-resourceset-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnResourceSet.ResourceProperty", _IResolvable_a771d0ef]]]:
        '''A list of resource objects in the resource set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html#cfn-route53recoveryreadiness-resourceset-resources
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnResourceSet.ResourceProperty", _IResolvable_a771d0ef]]], jsii.get(self, "resources"))

    @resources.setter
    def resources(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnResourceSet.ResourceProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f263ee4b41c9c9dbe234e61368975e3d4f17310f1afaed3e1a98d1bca78df1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a6bd9fcedd9717cd1721e9c2ef3b0a8a09186aebdcd0c7a353207bdc4421511)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9881ef9b8ba48d4b364c4dbc1a25ab42ddad33333c7849d8fdfc53ad5dc5f92d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceSetName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_route53recoveryreadiness.CfnResourceSet.DNSTargetResourceProperty",
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
            target_resource: typing.Optional[typing.Union[typing.Union["CfnResourceSet.TargetResourceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_route53recoveryreadiness as route53recoveryreadiness
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__3fe284b4f84c8e46c93dfdae981eaf0f193605a0e0c93ac11026634b4386c3b7)
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
        ) -> typing.Optional[typing.Union["CfnResourceSet.TargetResourceProperty", _IResolvable_a771d0ef]]:
            '''The target resource that the Route 53 record points to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-dnstargetresource.html#cfn-route53recoveryreadiness-resourceset-dnstargetresource-targetresource
            '''
            result = self._values.get("target_resource")
            return typing.cast(typing.Optional[typing.Union["CfnResourceSet.TargetResourceProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DNSTargetResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_route53recoveryreadiness.CfnResourceSet.NLBResourceProperty",
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
                from monocdk import aws_route53recoveryreadiness as route53recoveryreadiness
                
                n_lBResource_property = route53recoveryreadiness.CfnResourceSet.NLBResourceProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9965dffd50660ecde6f10ee7949c02be19aa45d9fcc67ef46853f7c05988377b)
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
        jsii_type="monocdk.aws_route53recoveryreadiness.CfnResourceSet.R53ResourceRecordProperty",
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
                from monocdk import aws_route53recoveryreadiness as route53recoveryreadiness
                
                r53_resource_record_property = route53recoveryreadiness.CfnResourceSet.R53ResourceRecordProperty(
                    domain_name="domainName",
                    record_set_id="recordSetId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2f519cbf7c1589f68b396a2c79d321ed69b485ae7281b5a06155d2693370c3d0)
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
        jsii_type="monocdk.aws_route53recoveryreadiness.CfnResourceSet.ResourceProperty",
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
            dns_target_resource: typing.Optional[typing.Union[typing.Union["CfnResourceSet.DNSTargetResourceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_route53recoveryreadiness as route53recoveryreadiness
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__61679b7f28198ce32a79c0bcc7ef87340f984718d29f55dced5e3f8929330ed9)
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
        ) -> typing.Optional[typing.Union["CfnResourceSet.DNSTargetResourceProperty", _IResolvable_a771d0ef]]:
            '''A component for DNS/routing control readiness checks.

            This is a required setting when ``ResourceSet`` ``ResourceSetType`` is set to ``AWS::Route53RecoveryReadiness::DNSTargetResource`` . Do not set it for any other ``ResourceSetType`` setting.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-resource.html#cfn-route53recoveryreadiness-resourceset-resource-dnstargetresource
            '''
            result = self._values.get("dns_target_resource")
            return typing.cast(typing.Optional[typing.Union["CfnResourceSet.DNSTargetResourceProperty", _IResolvable_a771d0ef]], result)

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
        jsii_type="monocdk.aws_route53recoveryreadiness.CfnResourceSet.TargetResourceProperty",
        jsii_struct_bases=[],
        name_mapping={"nlb_resource": "nlbResource", "r53_resource": "r53Resource"},
    )
    class TargetResourceProperty:
        def __init__(
            self,
            *,
            nlb_resource: typing.Optional[typing.Union[typing.Union["CfnResourceSet.NLBResourceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            r53_resource: typing.Optional[typing.Union[typing.Union["CfnResourceSet.R53ResourceRecordProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The target resource that the Route 53 record points to.

            :param nlb_resource: The Network Load Balancer resource that a DNS target resource points to.
            :param r53_resource: The Route 53 resource that a DNS target resource record points to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-targetresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_route53recoveryreadiness as route53recoveryreadiness
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__71e4b643decc97b2d09b22422590f15303afacd8c025f3c44307d40689583fcc)
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
        ) -> typing.Optional[typing.Union["CfnResourceSet.NLBResourceProperty", _IResolvable_a771d0ef]]:
            '''The Network Load Balancer resource that a DNS target resource points to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-targetresource.html#cfn-route53recoveryreadiness-resourceset-targetresource-nlbresource
            '''
            result = self._values.get("nlb_resource")
            return typing.cast(typing.Optional[typing.Union["CfnResourceSet.NLBResourceProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def r53_resource(
            self,
        ) -> typing.Optional[typing.Union["CfnResourceSet.R53ResourceRecordProperty", _IResolvable_a771d0ef]]:
            '''The Route 53 resource that a DNS target resource record points to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53recoveryreadiness-resourceset-targetresource.html#cfn-route53recoveryreadiness-resourceset-targetresource-r53resource
            '''
            result = self._values.get("r53_resource")
            return typing.cast(typing.Optional[typing.Union["CfnResourceSet.R53ResourceRecordProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_route53recoveryreadiness.CfnResourceSetProps",
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
        resources: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnResourceSet.ResourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        resource_set_type: builtins.str,
        resource_set_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_route53recoveryreadiness as route53recoveryreadiness
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__78581c262b5631a304634d2c11f3c0de5c6cb41280a7067c036d43a6893a9269)
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
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnResourceSet.ResourceProperty, _IResolvable_a771d0ef]]]:
        '''A list of resource objects in the resource set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html#cfn-route53recoveryreadiness-resourceset-resources
        '''
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnResourceSet.ResourceProperty, _IResolvable_a771d0ef]]], result)

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
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A tag to associate with the parameters for a resource set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53recoveryreadiness-resourceset.html#cfn-route53recoveryreadiness-resourceset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

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

def _typecheckingstub__0f1fc0c171fbcb7086f5f1ca48fff0312f7d383e9e119f20060320330f711067(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    cell_name: typing.Optional[builtins.str] = None,
    cells: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7caf352c7f690a92e5c5981bb857ebfada99d536910de49e303ebec415b502(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23cdf7569e354aa85c52a9f06e5a6da00a012469fbb801ae08da7db7344a0ec2(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e19ce29aad9cf1b109a592b5a63535736966f0788fe5a26ab65849e2da797f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3adbb83195ebbe1f122d693f401c09c8790f42a3299bca5c1fb06ac50ef595(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a0c2c07baccfd850236d4a1cffa00bc805bc9c6730b5dbb7d3371965e9541a(
    *,
    cell_name: typing.Optional[builtins.str] = None,
    cells: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90c0fa2b82ccff3c40c0d2249b2fd925bf78c29280bd8e7ace6b9176c84bf91(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    readiness_check_name: typing.Optional[builtins.str] = None,
    resource_set_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__353f963cb3b28cac741137e7b837785fb5bf6e7e980edf416b8dfb882690e738(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b608fa45248ae667d3b36b339f938d93b5bf1a715f2b4919776ef141684fae89(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0218ba2f71cba1d5fe98177db9f79c45505c17c5113b1a4e9cbce33f38a2efed(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c98ad06f971073c2d858553717bc3656d88df37e862a3366449fe2e51832db7f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5cc9591e7fc8846dd0045cdf3e559d05ed722b143b73714004900d9e308c27b(
    *,
    readiness_check_name: typing.Optional[builtins.str] = None,
    resource_set_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9c424198a99017d65047284ae5cd01df4cdb42d190ce68ff8f623c9e899c1e(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    cells: typing.Optional[typing.Sequence[builtins.str]] = None,
    recovery_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a5c879572794c2de2d914708779e8209b12351ba566e6835309736dc0aed9d(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d877aa5e7a01a3591d87c2799243dc486409dae74aca3a8d995cbd69cbefef7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56188fe1b7d2f9db534b57fade34ee51969dfe0e1afdbc5f65040b85cad5f2c8(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f72cda09d84b4239e27aea9c552d660c45ac7ed8405a42f26ff6d0e9bcf22b1b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9362839126196e5c0451ca734469c3e56c4ff23c69e2aa96f1f21a374f4f2311(
    *,
    cells: typing.Optional[typing.Sequence[builtins.str]] = None,
    recovery_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a7a168d53601d968304c2f647cddbd92d1ef86ad06f14e93590eba948ace89(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    resources: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnResourceSet.ResourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    resource_set_type: builtins.str,
    resource_set_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f43f36d452494849870b457816a85593cab2d39abc24b55714918e457f06b983(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a30ad089f78bdd91ac003f3b954834d62f62421bf9653eb2dd59579888c45ce3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f263ee4b41c9c9dbe234e61368975e3d4f17310f1afaed3e1a98d1bca78df1b(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnResourceSet.ResourceProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a6bd9fcedd9717cd1721e9c2ef3b0a8a09186aebdcd0c7a353207bdc4421511(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9881ef9b8ba48d4b364c4dbc1a25ab42ddad33333c7849d8fdfc53ad5dc5f92d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe284b4f84c8e46c93dfdae981eaf0f193605a0e0c93ac11026634b4386c3b7(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    hosted_zone_arn: typing.Optional[builtins.str] = None,
    record_set_id: typing.Optional[builtins.str] = None,
    record_type: typing.Optional[builtins.str] = None,
    target_resource: typing.Optional[typing.Union[typing.Union[CfnResourceSet.TargetResourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9965dffd50660ecde6f10ee7949c02be19aa45d9fcc67ef46853f7c05988377b(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f519cbf7c1589f68b396a2c79d321ed69b485ae7281b5a06155d2693370c3d0(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    record_set_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61679b7f28198ce32a79c0bcc7ef87340f984718d29f55dced5e3f8929330ed9(
    *,
    component_id: typing.Optional[builtins.str] = None,
    dns_target_resource: typing.Optional[typing.Union[typing.Union[CfnResourceSet.DNSTargetResourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    readiness_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e4b643decc97b2d09b22422590f15303afacd8c025f3c44307d40689583fcc(
    *,
    nlb_resource: typing.Optional[typing.Union[typing.Union[CfnResourceSet.NLBResourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    r53_resource: typing.Optional[typing.Union[typing.Union[CfnResourceSet.R53ResourceRecordProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78581c262b5631a304634d2c11f3c0de5c6cb41280a7067c036d43a6893a9269(
    *,
    resources: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnResourceSet.ResourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    resource_set_type: builtins.str,
    resource_set_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
