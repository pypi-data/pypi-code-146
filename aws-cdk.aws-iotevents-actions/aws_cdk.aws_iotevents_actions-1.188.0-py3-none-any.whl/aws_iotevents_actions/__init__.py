'''
# Actions for AWS::IoTEvents Detector Model

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This library contains integration classes to specify actions of state events of Detector Model in `@aws-cdk/aws-iotevents`.
Instances of these classes should be passed to `State` defined in `@aws-cdk/aws-iotevents`
You can define built-in actions to use a timer or set a variable, or send data to other AWS resources.

This library contains integration classes to use a timer or set a variable, or send data to other AWS resources.
AWS IoT Events can trigger actions when it detects a specified event or transition event.

Currently supported are:

* Set variable to detector instanse
* Invoke a Lambda function

## Set variable to detector instanse

The code snippet below creates an Action that set variable to detector instanse
when it is triggered.

```python
# Example automatically generated from non-compiling source. May contain errors.
import aws_cdk.aws_iotevents as iotevents
import aws_cdk.aws_iotevents_actions as actions

# input: iotevents.IInput

state = iotevents.State(
    state_name="MyState",
    on_enter=[iotevents.Event(
        event_name="test-event",
        condition=iotevents.Expression.current_input(input),
        actions=[actions, [
            actions.SetVariableAction("MyVariable",
                iotevents.Expression.input_attribute(input, "payload.temperature"))
        ]
        ]
    )]
)
```

## Invoke a Lambda function

The code snippet below creates an Action that invoke a Lambda function
when it is triggered.

```python
import aws_cdk.aws_iotevents as iotevents
import aws_cdk.aws_iotevents_actions as actions
import aws_cdk.aws_lambda as lambda_

# input: iotevents.IInput
# func: lambda.IFunction

state = iotevents.State(
    state_name="MyState",
    on_enter=[iotevents.Event(
        event_name="test-event",
        condition=iotevents.Expression.current_input(input),
        actions=[actions.LambdaInvokeAction(func)]
    )]
)
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

from ._jsii import *

import aws_cdk.aws_iam as _aws_cdk_aws_iam_940a1ce0
import aws_cdk.aws_iotevents as _aws_cdk_aws_iotevents_a4360a1f
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_5443dbc3
import constructs as _constructs_77d1e7e8


@jsii.implements(_aws_cdk_aws_iotevents_a4360a1f.IAction)
class LambdaInvokeAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iotevents-actions.LambdaInvokeAction",
):
    '''(experimental) The action to write the data to an AWS Lambda function.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_iotevents as iotevents
        import aws_cdk.aws_iotevents_actions as actions
        import aws_cdk.aws_lambda as lambda_
        
        # func: lambda.IFunction
        
        
        input = iotevents.Input(self, "MyInput",
            input_name="my_input",  # optional
            attribute_json_paths=["payload.deviceId", "payload.temperature"]
        )
        
        warm_state = iotevents.State(
            state_name="warm",
            on_enter=[iotevents.Event(
                event_name="test-enter-event",
                condition=iotevents.Expression.current_input(input),
                actions=[actions.LambdaInvokeAction(func)]
            )],
            on_input=[iotevents.Event( # optional
                event_name="test-input-event",
                actions=[actions.LambdaInvokeAction(func)])],
            on_exit=[iotevents.Event( # optional
                event_name="test-exit-event",
                actions=[actions.LambdaInvokeAction(func)])]
        )
        cold_state = iotevents.State(
            state_name="cold"
        )
        
        # transit to coldState when temperature is less than 15
        warm_state.transition_to(cold_state,
            event_name="to_coldState",  # optional property, default by combining the names of the States
            when=iotevents.Expression.lt(
                iotevents.Expression.input_attribute(input, "payload.temperature"),
                iotevents.Expression.from_string("15")),
            executing=[actions.LambdaInvokeAction(func)]
        )
        # transit to warmState when temperature is greater than or equal to 15
        cold_state.transition_to(warm_state,
            when=iotevents.Expression.gte(
                iotevents.Expression.input_attribute(input, "payload.temperature"),
                iotevents.Expression.from_string("15"))
        )
        
        iotevents.DetectorModel(self, "MyDetectorModel",
            detector_model_name="test-detector-model",  # optional
            description="test-detector-model-description",  # optional property, default is none
            evaluation_method=iotevents.EventEvaluation.SERIAL,  # optional property, default is iotevents.EventEvaluation.BATCH
            detector_key="payload.deviceId",  # optional property, default is none and single detector instance will be created and all inputs will be routed to it
            initial_state=warm_state
        )
    '''

    def __init__(self, func: _aws_cdk_aws_lambda_5443dbc3.IFunction) -> None:
        '''
        :param func: the AWS Lambda function to be invoked by this action.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b582fb3fec1fa51a6f74760b9d6237fa277baa104d235a98f42946121ca83692)
            check_type(argname="argument func", value=func, expected_type=type_hints["func"])
        jsii.create(self.__class__, self, [func])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _constructs_77d1e7e8.Construct,
        *,
        role: _aws_cdk_aws_iam_940a1ce0.IRole,
    ) -> _aws_cdk_aws_iotevents_a4360a1f.ActionConfig:
        '''(experimental) Returns the AWS IoT Events action specification.

        :param _scope: -
        :param role: (experimental) The IAM role assumed by IoT Events to perform the action.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c37a1fb7cc655623c698fe9d97c8078d3a7cab5b4cbc792856a1d2fe13408dd)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        options = _aws_cdk_aws_iotevents_a4360a1f.ActionBindOptions(role=role)

        return typing.cast(_aws_cdk_aws_iotevents_a4360a1f.ActionConfig, jsii.invoke(self, "bind", [_scope, options]))


@jsii.implements(_aws_cdk_aws_iotevents_a4360a1f.IAction)
class SetVariableAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iotevents-actions.SetVariableAction",
):
    '''(experimental) The action to create a variable with a specified value.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Example automatically generated from non-compiling source. May contain errors.
        import aws_cdk.aws_iotevents as iotevents
        import aws_cdk.aws_iotevents_actions as actions
        
        # input: iotevents.IInput
        
        state = iotevents.State(
            state_name="MyState",
            on_enter=[iotevents.Event(
                event_name="test-event",
                condition=iotevents.Expression.current_input(input),
                actions=[actions, [
                    actions.SetVariableAction("MyVariable",
                        iotevents.Expression.input_attribute(input, "payload.temperature"))
                ]
                ]
            )]
        )
    '''

    def __init__(
        self,
        variable_name: builtins.str,
        value: _aws_cdk_aws_iotevents_a4360a1f.Expression,
    ) -> None:
        '''
        :param variable_name: the name of the variable.
        :param value: the new value of the variable.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efe2ba61d24c9053170e8e9fbfcf761c5ab4ea6e9b35eb25fc682e169accb264)
            check_type(argname="argument variable_name", value=variable_name, expected_type=type_hints["variable_name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.create(self.__class__, self, [variable_name, value])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _constructs_77d1e7e8.Construct,
        *,
        role: _aws_cdk_aws_iam_940a1ce0.IRole,
    ) -> _aws_cdk_aws_iotevents_a4360a1f.ActionConfig:
        '''(experimental) Returns the AWS IoT Events action specification.

        :param _scope: -
        :param role: (experimental) The IAM role assumed by IoT Events to perform the action.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8103149dc35e03e6a6f915cfe31634c27bfae25ff97a3b1be1ad6990c2f29d33)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        _options = _aws_cdk_aws_iotevents_a4360a1f.ActionBindOptions(role=role)

        return typing.cast(_aws_cdk_aws_iotevents_a4360a1f.ActionConfig, jsii.invoke(self, "bind", [_scope, _options]))


__all__ = [
    "LambdaInvokeAction",
    "SetVariableAction",
]

publication.publish()

def _typecheckingstub__b582fb3fec1fa51a6f74760b9d6237fa277baa104d235a98f42946121ca83692(
    func: _aws_cdk_aws_lambda_5443dbc3.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c37a1fb7cc655623c698fe9d97c8078d3a7cab5b4cbc792856a1d2fe13408dd(
    _scope: _constructs_77d1e7e8.Construct,
    *,
    role: _aws_cdk_aws_iam_940a1ce0.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe2ba61d24c9053170e8e9fbfcf761c5ab4ea6e9b35eb25fc682e169accb264(
    variable_name: builtins.str,
    value: _aws_cdk_aws_iotevents_a4360a1f.Expression,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8103149dc35e03e6a6f915cfe31634c27bfae25ff97a3b1be1ad6990c2f29d33(
    _scope: _constructs_77d1e7e8.Construct,
    *,
    role: _aws_cdk_aws_iam_940a1ce0.IRole,
) -> None:
    """Type checking stubs"""
    pass
