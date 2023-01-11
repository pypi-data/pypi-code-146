'''
# Lifecycle Hook for the CDK AWS AutoScaling Library

This library contains integration classes for AutoScaling lifecycle hooks.
Instances of these classes should be passed to the
`autoScalingGroup.addLifecycleHook()` method.

Lifecycle hooks can be activated in one of the following ways:

* Invoke a Lambda function
* Publish to an SNS topic
* Send to an SQS queue

For more information on using this library, see the README of the
`@aws-cdk/aws-autoscaling` library.

For more information about lifecycle hooks, see
[Amazon EC2 AutoScaling Lifecycle hooks](https://docs.aws.amazon.com/autoscaling/ec2/userguide/lifecycle-hooks.html) in the Amazon EC2 User Guide.
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
from ..aws_autoscaling import (
    BindHookTargetOptions as _BindHookTargetOptions_96ca3565,
    ILifecycleHookTarget as _ILifecycleHookTarget_e29def65,
    LifecycleHook as _LifecycleHook_373de924,
    LifecycleHookTargetConfig as _LifecycleHookTargetConfig_295b808c,
)
from ..aws_iam import IRole as _IRole_59af6f50
from ..aws_kms import IKey as _IKey_36930160
from ..aws_lambda import IFunction as _IFunction_6e14f09e
from ..aws_sns import ITopic as _ITopic_465e36b9
from ..aws_sqs import IQueue as _IQueue_45a01ab4


@jsii.implements(_ILifecycleHookTarget_e29def65)
class FunctionHook(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_autoscaling_hooktargets.FunctionHook",
):
    '''(experimental) Use a Lambda Function as a hook target.

    Internally creates a Topic to make the connection.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_autoscaling_hooktargets as autoscaling_hooktargets
        from monocdk import aws_kms as kms
        from monocdk import aws_lambda as lambda_
        
        # function_: lambda.Function
        # key: kms.Key
        
        function_hook = autoscaling_hooktargets.FunctionHook(function_, key)
    '''

    def __init__(
        self,
        fn: _IFunction_6e14f09e,
        encryption_key: typing.Optional[_IKey_36930160] = None,
    ) -> None:
        '''
        :param fn: Function to invoke in response to a lifecycle event.
        :param encryption_key: If provided, this key is used to encrypt the contents of the SNS topic.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d312b80dbfd5d3578ad8715b41b028b126572c20a29b22a4424a6fd6656852f)
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
        jsii.create(self.__class__, self, [fn, encryption_key])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _constructs_77d1e7e8.Construct,
        *,
        lifecycle_hook: _LifecycleHook_373de924,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> _LifecycleHookTargetConfig_295b808c:
        '''(experimental) If the ``IRole`` does not exist in ``options``, will create an ``IRole`` and an SNS Topic and attach both to the lifecycle hook.

        If the ``IRole`` does exist in ``options``, will only create an SNS Topic and attach it to the lifecycle hook.

        :param _scope: -
        :param lifecycle_hook: (experimental) The lifecycle hook to attach to. [disable-awslint:ref-via-interface]
        :param role: (experimental) The role to use when attaching to the lifecycle hook. [disable-awslint:ref-via-interface] Default: : a role is not created unless the target arn is specified

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb6ee79c50d0a4b7746817152b0636589895e414546e61efc0b115c28dc3b91d)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        options = _BindHookTargetOptions_96ca3565(
            lifecycle_hook=lifecycle_hook, role=role
        )

        return typing.cast(_LifecycleHookTargetConfig_295b808c, jsii.invoke(self, "bind", [_scope, options]))


@jsii.implements(_ILifecycleHookTarget_e29def65)
class QueueHook(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_autoscaling_hooktargets.QueueHook",
):
    '''(experimental) Use an SQS queue as a hook target.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_autoscaling_hooktargets as autoscaling_hooktargets
        from monocdk import aws_sqs as sqs
        
        # queue: sqs.Queue
        
        queue_hook = autoscaling_hooktargets.QueueHook(queue)
    '''

    def __init__(self, queue: _IQueue_45a01ab4) -> None:
        '''
        :param queue: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4203c31de2d0420f227c8a767b2c4801709389f27046b121fb3ed6f287b41c64)
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        jsii.create(self.__class__, self, [queue])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _constructs_77d1e7e8.Construct,
        *,
        lifecycle_hook: _LifecycleHook_373de924,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> _LifecycleHookTargetConfig_295b808c:
        '''(experimental) If an ``IRole`` is found in ``options``, grant it access to send messages.

        Otherwise, create a new ``IRole`` and grant it access to send messages.

        :param _scope: -
        :param lifecycle_hook: (experimental) The lifecycle hook to attach to. [disable-awslint:ref-via-interface]
        :param role: (experimental) The role to use when attaching to the lifecycle hook. [disable-awslint:ref-via-interface] Default: : a role is not created unless the target arn is specified

        :return: the ``IRole`` with access to send messages and the ARN of the queue it has access to send messages to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec57a90113cf3d91ba451bdbb058a8638c4db610fd852551ff266399bfee113)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        options = _BindHookTargetOptions_96ca3565(
            lifecycle_hook=lifecycle_hook, role=role
        )

        return typing.cast(_LifecycleHookTargetConfig_295b808c, jsii.invoke(self, "bind", [_scope, options]))


@jsii.implements(_ILifecycleHookTarget_e29def65)
class TopicHook(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_autoscaling_hooktargets.TopicHook",
):
    '''(experimental) Use an SNS topic as a hook target.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_autoscaling_hooktargets as autoscaling_hooktargets
        from monocdk import aws_sns as sns
        
        # topic: sns.Topic
        
        topic_hook = autoscaling_hooktargets.TopicHook(topic)
    '''

    def __init__(self, topic: _ITopic_465e36b9) -> None:
        '''
        :param topic: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dbca5bd7df6478ca447fa4e8f394ec95780b84db1e5f2044c147371e30f1219)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        jsii.create(self.__class__, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _constructs_77d1e7e8.Construct,
        *,
        lifecycle_hook: _LifecycleHook_373de924,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> _LifecycleHookTargetConfig_295b808c:
        '''(experimental) If an ``IRole`` is found in ``options``, grant it topic publishing permissions.

        Otherwise, create a new ``IRole`` and grant it topic publishing permissions.

        :param _scope: -
        :param lifecycle_hook: (experimental) The lifecycle hook to attach to. [disable-awslint:ref-via-interface]
        :param role: (experimental) The role to use when attaching to the lifecycle hook. [disable-awslint:ref-via-interface] Default: : a role is not created unless the target arn is specified

        :return: the ``IRole`` with topic publishing permissions and the ARN of the topic it has publishing permission to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dde25ed5709024874df03f64eb5d490bc901d50d4ef04d99e3032af1b3bb154c)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        options = _BindHookTargetOptions_96ca3565(
            lifecycle_hook=lifecycle_hook, role=role
        )

        return typing.cast(_LifecycleHookTargetConfig_295b808c, jsii.invoke(self, "bind", [_scope, options]))


__all__ = [
    "FunctionHook",
    "QueueHook",
    "TopicHook",
]

publication.publish()

def _typecheckingstub__8d312b80dbfd5d3578ad8715b41b028b126572c20a29b22a4424a6fd6656852f(
    fn: _IFunction_6e14f09e,
    encryption_key: typing.Optional[_IKey_36930160] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6ee79c50d0a4b7746817152b0636589895e414546e61efc0b115c28dc3b91d(
    _scope: _constructs_77d1e7e8.Construct,
    *,
    lifecycle_hook: _LifecycleHook_373de924,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4203c31de2d0420f227c8a767b2c4801709389f27046b121fb3ed6f287b41c64(
    queue: _IQueue_45a01ab4,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec57a90113cf3d91ba451bdbb058a8638c4db610fd852551ff266399bfee113(
    _scope: _constructs_77d1e7e8.Construct,
    *,
    lifecycle_hook: _LifecycleHook_373de924,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dbca5bd7df6478ca447fa4e8f394ec95780b84db1e5f2044c147371e30f1219(
    topic: _ITopic_465e36b9,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde25ed5709024874df03f64eb5d490bc901d50d4ef04d99e3032af1b3bb154c(
    _scope: _constructs_77d1e7e8.Construct,
    *,
    lifecycle_hook: _LifecycleHook_373de924,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass
