'''
# AWS::ControlTower Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as controltower
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for ControlTower construct libraries](https://constructs.dev/search?q=controltower)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::ControlTower resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ControlTower.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::ControlTower](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ControlTower.html).

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
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnEnabledControl(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_controltower.CfnEnabledControl",
):
    '''A CloudFormation ``AWS::ControlTower::EnabledControl``.

    The resource represents an enabled control. It specifies an asynchronous operation that creates AWS resources on the specified organizational unit and the accounts it contains. The resources created will vary according to the control that you specify.

    :cloudformationResource: AWS::ControlTower::EnabledControl
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledcontrol.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_controltower as controltower
        
        cfn_enabled_control = controltower.CfnEnabledControl(self, "MyCfnEnabledControl",
            control_identifier="controlIdentifier",
            target_identifier="targetIdentifier"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        control_identifier: builtins.str,
        target_identifier: builtins.str,
    ) -> None:
        '''Create a new ``AWS::ControlTower::EnabledControl``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param control_identifier: The ARN of the control. Only *Strongly recommended* and *Elective* controls are permitted, with the exception of the *Region deny* guardrail.
        :param target_identifier: The ARN of the organizational unit.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__617f70d867b99ee40e1a3614dbae322b524b83eac4d34c59f9960d35b9f04e0e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEnabledControlProps(
            control_identifier=control_identifier, target_identifier=target_identifier
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c5b9cb758d25f9cf9cf2a601481ba87426f557c0d82b67d906842d157e9dbc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4195a27f22ffbe3822367f9c012009b10458baad902d8ac21651e9b56d59427)
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
    @jsii.member(jsii_name="controlIdentifier")
    def control_identifier(self) -> builtins.str:
        '''The ARN of the control.

        Only *Strongly recommended* and *Elective* controls are permitted, with the exception of the *Region deny* guardrail.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledcontrol.html#cfn-controltower-enabledcontrol-controlidentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "controlIdentifier"))

    @control_identifier.setter
    def control_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1666d5fd625c670cbfd396a62fd57cc782d781e2a0775ea8c15fffe4c7567dde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="targetIdentifier")
    def target_identifier(self) -> builtins.str:
        '''The ARN of the organizational unit.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledcontrol.html#cfn-controltower-enabledcontrol-targetidentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetIdentifier"))

    @target_identifier.setter
    def target_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29e6fcae5884b895bfae011c3a7f77953085b5d4e1e43d2d4d5a1106aac28b20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetIdentifier", value)


@jsii.data_type(
    jsii_type="monocdk.aws_controltower.CfnEnabledControlProps",
    jsii_struct_bases=[],
    name_mapping={
        "control_identifier": "controlIdentifier",
        "target_identifier": "targetIdentifier",
    },
)
class CfnEnabledControlProps:
    def __init__(
        self,
        *,
        control_identifier: builtins.str,
        target_identifier: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnEnabledControl``.

        :param control_identifier: The ARN of the control. Only *Strongly recommended* and *Elective* controls are permitted, with the exception of the *Region deny* guardrail.
        :param target_identifier: The ARN of the organizational unit.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledcontrol.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_controltower as controltower
            
            cfn_enabled_control_props = controltower.CfnEnabledControlProps(
                control_identifier="controlIdentifier",
                target_identifier="targetIdentifier"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa72ebfd5d066c6bdc40364b3f725b2ff456f72e2c1797b8216e2c92c60208d1)
            check_type(argname="argument control_identifier", value=control_identifier, expected_type=type_hints["control_identifier"])
            check_type(argname="argument target_identifier", value=target_identifier, expected_type=type_hints["target_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "control_identifier": control_identifier,
            "target_identifier": target_identifier,
        }

    @builtins.property
    def control_identifier(self) -> builtins.str:
        '''The ARN of the control.

        Only *Strongly recommended* and *Elective* controls are permitted, with the exception of the *Region deny* guardrail.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledcontrol.html#cfn-controltower-enabledcontrol-controlidentifier
        '''
        result = self._values.get("control_identifier")
        assert result is not None, "Required property 'control_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_identifier(self) -> builtins.str:
        '''The ARN of the organizational unit.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-controltower-enabledcontrol.html#cfn-controltower-enabledcontrol-targetidentifier
        '''
        result = self._values.get("target_identifier")
        assert result is not None, "Required property 'target_identifier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnabledControlProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnEnabledControl",
    "CfnEnabledControlProps",
]

publication.publish()

def _typecheckingstub__617f70d867b99ee40e1a3614dbae322b524b83eac4d34c59f9960d35b9f04e0e(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    control_identifier: builtins.str,
    target_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c5b9cb758d25f9cf9cf2a601481ba87426f557c0d82b67d906842d157e9dbc1(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4195a27f22ffbe3822367f9c012009b10458baad902d8ac21651e9b56d59427(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1666d5fd625c670cbfd396a62fd57cc782d781e2a0775ea8c15fffe4c7567dde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e6fcae5884b895bfae011c3a7f77953085b5d4e1e43d2d4d5a1106aac28b20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa72ebfd5d066c6bdc40364b3f725b2ff456f72e2c1797b8216e2c92c60208d1(
    *,
    control_identifier: builtins.str,
    target_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
