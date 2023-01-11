'''
# Targets for AWS Elastic Load Balancing V2

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This package contains targets for ELBv2. See the README of the `@aws-cdk/aws-elasticloadbalancingv2` library.
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

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_67de8e8d
import aws_cdk.aws_elasticloadbalancingv2 as _aws_cdk_aws_elasticloadbalancingv2_e93c784f
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_5443dbc3


@jsii.implements(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancerTarget)
class AlbArnTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2-targets.AlbArnTarget",
):
    '''A single Application Load Balancer as the target for load balancing.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_elasticloadbalancingv2_targets as elasticloadbalancingv2_targets
        
        alb_arn_target = elasticloadbalancingv2_targets.AlbArnTarget("albArn", 123)
    '''

    def __init__(self, alb_arn: builtins.str, port: jsii.Number) -> None:
        '''Create a new alb target.

        :param alb_arn: The ARN of the application load balancer to load balance to.
        :param port: The port on which the target is listening.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21755603a31cc938e8e91cb63fc38c5f8fc7ccf9398b6673d6e6fd80cef9afb3)
            check_type(argname="argument alb_arn", value=alb_arn, expected_type=type_hints["alb_arn"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        jsii.create(self.__class__, self, [alb_arn, port])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(
        self,
        target_group: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkTargetGroup,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.LoadBalancerTargetProps:
        '''Register this alb target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c870055ca51103637ed10001392cc6a39ea3c2c6eb247b8f2e609df4024904a)
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.LoadBalancerTargetProps, jsii.invoke(self, "attachToNetworkTargetGroup", [target_group]))


class AlbTarget(
    AlbArnTarget,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2-targets.AlbTarget",
):
    '''A single Application Load Balancer as the target for load balancing.

    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_elasticloadbalancingv2_targets as targets
        import aws_cdk.aws_ecs as ecs
        import aws_cdk.aws_ecs_patterns as patterns
        
        # vpc: ec2.Vpc
        
        
        task = ecs.FargateTaskDefinition(self, "Task", cpu=256, memory_limit_mi_b=512)
        task.add_container("nginx",
            image=ecs.ContainerImage.from_registry("public.ecr.aws/nginx/nginx:latest"),
            port_mappings=[ecs.PortMapping(container_port=80)]
        )
        
        svc = patterns.ApplicationLoadBalancedFargateService(self, "Service",
            vpc=vpc,
            task_definition=task,
            public_load_balancer=False
        )
        
        nlb = elbv2.NetworkLoadBalancer(self, "Nlb",
            vpc=vpc,
            cross_zone_enabled=True,
            internet_facing=True
        )
        
        listener = nlb.add_listener("listener", port=80)
        
        listener.add_targets("Targets",
            targets=[targets.AlbTarget(svc.load_balancer, 80)],
            port=80
        )
        
        CfnOutput(self, "NlbEndpoint", value=f"http://{nlb.loadBalancerDnsName}")
    '''

    def __init__(
        self,
        alb: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer,
        port: jsii.Number,
    ) -> None:
        '''
        :param alb: The application load balancer to load balance to.
        :param port: The port on which the target is listening.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7746430c274e9478a37a49023fe1a79dca60e73e110bf0b07255aba94be89d6b)
            check_type(argname="argument alb", value=alb, expected_type=type_hints["alb"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        jsii.create(self.__class__, self, [alb, port])


@jsii.implements(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancerTarget, _aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancerTarget)
class InstanceIdTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2-targets.InstanceIdTarget",
):
    '''An EC2 instance that is the target for load balancing.

    If you register a target of this type, you are responsible for making
    sure the load balancer's security group can connect to the instance.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_elasticloadbalancingv2_targets as elasticloadbalancingv2_targets
        
        instance_id_target = elasticloadbalancingv2_targets.InstanceIdTarget("instanceId", 123)
    '''

    def __init__(
        self,
        instance_id: builtins.str,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new Instance target.

        :param instance_id: Instance ID of the instance to register to.
        :param port: Override the default port for the target group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7df06609f12197bd945c63619c4d8f0e808634a8ffc2a3eef4363e7bfc6c23d7)
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        jsii.create(self.__class__, self, [instance_id, port])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(
        self,
        target_group: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationTargetGroup,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.LoadBalancerTargetProps:
        '''Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb534c3f1f9d7ff3b24bb6195ec02ae558bede6b53ed337db640c51de4e408d)
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.LoadBalancerTargetProps, jsii.invoke(self, "attachToApplicationTargetGroup", [target_group]))

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(
        self,
        target_group: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkTargetGroup,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.LoadBalancerTargetProps:
        '''Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0b2386ecc3bb4ddc5d926a6639c1828bbc7b92fa91b4f341587e7ef08427b9c)
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.LoadBalancerTargetProps, jsii.invoke(self, "attachToNetworkTargetGroup", [target_group]))


class InstanceTarget(
    InstanceIdTarget,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2-targets.InstanceTarget",
):
    '''
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ec2 as ec2
        import aws_cdk.aws_elasticloadbalancingv2_targets as elasticloadbalancingv2_targets
        
        # instance: ec2.Instance
        
        instance_target = elasticloadbalancingv2_targets.InstanceTarget(instance, 123)
    '''

    def __init__(
        self,
        instance: _aws_cdk_aws_ec2_67de8e8d.Instance,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new Instance target.

        :param instance: Instance to register to.
        :param port: Override the default port for the target group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74280f986b4c3d46fed198aefaa7d4751a28cda3fe1ebf04baa124ea60fff6f1)
            check_type(argname="argument instance", value=instance, expected_type=type_hints["instance"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        jsii.create(self.__class__, self, [instance, port])


@jsii.implements(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancerTarget, _aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancerTarget)
class IpTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2-targets.IpTarget",
):
    '''An IP address that is a target for load balancing.

    Specify IP addresses from the subnets of the virtual private cloud (VPC) for
    the target group, the RFC 1918 range (10.0.0.0/8, 172.16.0.0/12, and
    192.168.0.0/16), and the RFC 6598 range (100.64.0.0/10). You can't specify
    publicly routable IP addresses.

    If you register a target of this type, you are responsible for making
    sure the load balancer's security group can send packets to the IP address.

    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_elasticloadbalancingv2_targets as elasticloadbalancingv2_targets
        
        ip_target = elasticloadbalancingv2_targets.IpTarget("ipAddress", 123, "availabilityZone")
    '''

    def __init__(
        self,
        ip_address: builtins.str,
        port: typing.Optional[jsii.Number] = None,
        availability_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new IPAddress target.

        The availabilityZone parameter determines whether the target receives
        traffic from the load balancer nodes in the specified Availability Zone
        or from all enabled Availability Zones for the load balancer.

        This parameter is not supported if the target type of the target group
        is instance. If the IP address is in a subnet of the VPC for the target
        group, the Availability Zone is automatically detected and this
        parameter is optional. If the IP address is outside the VPC, this
        parameter is required.

        With an Application Load Balancer, if the IP address is outside the VPC
        for the target group, the only supported value is all.

        Default is automatic.

        :param ip_address: The IP Address to load balance to.
        :param port: Override the group's default port.
        :param availability_zone: Availability zone to send traffic from.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a6e34c86e5621d2cdf49c460552134f4f1e3d65a5db9f0255f6926a880fa86a)
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
        jsii.create(self.__class__, self, [ip_address, port, availability_zone])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(
        self,
        target_group: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationTargetGroup,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.LoadBalancerTargetProps:
        '''Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538fbf7b0b3e47754c98a7bc0dd24dfc247b02d657b261a72565051e81586b17)
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.LoadBalancerTargetProps, jsii.invoke(self, "attachToApplicationTargetGroup", [target_group]))

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(
        self,
        target_group: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkTargetGroup,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.LoadBalancerTargetProps:
        '''Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df2f08ba4edd832789927a3c8b564fbaca97c48581cb93d5284dba9459ae6990)
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.LoadBalancerTargetProps, jsii.invoke(self, "attachToNetworkTargetGroup", [target_group]))


@jsii.implements(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancerTarget)
class LambdaTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2-targets.LambdaTarget",
):
    '''
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_lambda as lambda_
        import aws_cdk.aws_elasticloadbalancingv2_targets as targets
        
        # lambda_function: lambda.Function
        # lb: elbv2.ApplicationLoadBalancer
        
        
        listener = lb.add_listener("Listener", port=80)
        listener.add_targets("Targets",
            targets=[targets.LambdaTarget(lambda_function)],
        
            # For Lambda Targets, you need to explicitly enable health checks if you
            # want them.
            health_check=elbv2.HealthCheck(
                enabled=True
            )
        )
    '''

    def __init__(self, fn: _aws_cdk_aws_lambda_5443dbc3.IFunction) -> None:
        '''Create a new Lambda target.

        :param fn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a5760cb3aa2f74eca1347dd70774e052da1f440c8b8d4fcbb42b1aee9903c5c)
            check_type(argname="argument fn", value=fn, expected_type=type_hints["fn"])
        jsii.create(self.__class__, self, [fn])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(
        self,
        target_group: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationTargetGroup,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.LoadBalancerTargetProps:
        '''Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfc61ad2cb136d67c9d9e6a6e59d4966d27b1bdc071ddcbb70e229d5a78fd84d)
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.LoadBalancerTargetProps, jsii.invoke(self, "attachToApplicationTargetGroup", [target_group]))

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(
        self,
        target_group: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkTargetGroup,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.LoadBalancerTargetProps:
        '''Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e19af64262f9717f85fe9862d3547d4be9b07533278732d22e6986f72a9a1e84)
            check_type(argname="argument target_group", value=target_group, expected_type=type_hints["target_group"])
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.LoadBalancerTargetProps, jsii.invoke(self, "attachToNetworkTargetGroup", [target_group]))


__all__ = [
    "AlbArnTarget",
    "AlbTarget",
    "InstanceIdTarget",
    "InstanceTarget",
    "IpTarget",
    "LambdaTarget",
]

publication.publish()

def _typecheckingstub__21755603a31cc938e8e91cb63fc38c5f8fc7ccf9398b6673d6e6fd80cef9afb3(
    alb_arn: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c870055ca51103637ed10001392cc6a39ea3c2c6eb247b8f2e609df4024904a(
    target_group: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkTargetGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7746430c274e9478a37a49023fe1a79dca60e73e110bf0b07255aba94be89d6b(
    alb: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df06609f12197bd945c63619c4d8f0e808634a8ffc2a3eef4363e7bfc6c23d7(
    instance_id: builtins.str,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb534c3f1f9d7ff3b24bb6195ec02ae558bede6b53ed337db640c51de4e408d(
    target_group: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationTargetGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b2386ecc3bb4ddc5d926a6639c1828bbc7b92fa91b4f341587e7ef08427b9c(
    target_group: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkTargetGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74280f986b4c3d46fed198aefaa7d4751a28cda3fe1ebf04baa124ea60fff6f1(
    instance: _aws_cdk_aws_ec2_67de8e8d.Instance,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6e34c86e5621d2cdf49c460552134f4f1e3d65a5db9f0255f6926a880fa86a(
    ip_address: builtins.str,
    port: typing.Optional[jsii.Number] = None,
    availability_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538fbf7b0b3e47754c98a7bc0dd24dfc247b02d657b261a72565051e81586b17(
    target_group: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationTargetGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2f08ba4edd832789927a3c8b564fbaca97c48581cb93d5284dba9459ae6990(
    target_group: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkTargetGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5760cb3aa2f74eca1347dd70774e052da1f440c8b8d4fcbb42b1aee9903c5c(
    fn: _aws_cdk_aws_lambda_5443dbc3.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfc61ad2cb136d67c9d9e6a6e59d4966d27b1bdc071ddcbb70e229d5a78fd84d(
    target_group: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationTargetGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19af64262f9717f85fe9862d3547d4be9b07533278732d22e6986f72a9a1e84(
    target_group: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkTargetGroup,
) -> None:
    """Type checking stubs"""
    pass
