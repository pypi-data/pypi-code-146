'''
# CDK Construct library for higher-level ECS Constructs

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This library provides higher-level Amazon ECS constructs which follow common architectural patterns. It contains:

* Application Load Balanced Services
* Network Load Balanced Services
* Queue Processing Services
* Scheduled Tasks (cron jobs)
* Additional Examples

## Application Load Balanced Services

To define an Amazon ECS service that is behind an application load balancer, instantiate one of the following:

* `ApplicationLoadBalancedEc2Service`

```python
# cluster: ecs.Cluster

load_balanced_ecs_service = ecs_patterns.ApplicationLoadBalancedEc2Service(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("test"),
        environment={
            "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
            "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
        }
    ),
    desired_count=2
)
```

* `ApplicationLoadBalancedFargateService`

```python
# cluster: ecs.Cluster

load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    cpu=512,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    )
)

load_balanced_fargate_service.target_group.configure_health_check(
    path="/custom-health-path"
)
```

Instead of providing a cluster you can specify a VPC and CDK will create a new ECS cluster.
If you deploy multiple services CDK will only create one cluster per VPC.

You can omit `cluster` and `vpc` to let CDK create a new VPC with two AZs and create a cluster inside this VPC.

You can customize the health check for your target group; otherwise it defaults to `HTTP` over port `80` hitting path `/`.

Fargate services will use the `LATEST` platform version by default, but you can override by providing a value for the `platformVersion` property in the constructor.

Fargate services use the default VPC Security Group unless one or more are provided using the `securityGroups` property in the constructor.

By setting `redirectHTTP` to true, CDK will automatically create a listener on port 80 that redirects HTTP traffic to the HTTPS port.

If you specify the option `recordType` you can decide if you want the construct to use CNAME or Route53-Aliases as record sets.

If you need to encrypt the traffic between the load balancer and the ECS tasks, you can set the `targetProtocol` to `HTTPS`.

Additionally, if more than one application target group are needed, instantiate one of the following:

* `ApplicationMultipleTargetGroupsEc2Service`

```python
# One application load balancer with one listener and two target groups.
# cluster: ecs.Cluster

load_balanced_ec2_service = ecs_patterns.ApplicationMultipleTargetGroupsEc2Service(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=256,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageProps(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    ),
    target_groups=[ecsPatterns.ApplicationTargetProps(
        container_port=80
    ), ecsPatterns.ApplicationTargetProps(
        container_port=90,
        path_pattern="a/b/c",
        priority=10
    )
    ]
)
```

* `ApplicationMultipleTargetGroupsFargateService`

```python
# One application load balancer with one listener and two target groups.
# cluster: ecs.Cluster

load_balanced_fargate_service = ecs_patterns.ApplicationMultipleTargetGroupsFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    cpu=512,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageProps(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    ),
    target_groups=[ecsPatterns.ApplicationTargetProps(
        container_port=80
    ), ecsPatterns.ApplicationTargetProps(
        container_port=90,
        path_pattern="a/b/c",
        priority=10
    )
    ]
)
```

## Network Load Balanced Services

To define an Amazon ECS service that is behind a network load balancer, instantiate one of the following:

* `NetworkLoadBalancedEc2Service`

```python
# cluster: ecs.Cluster

load_balanced_ecs_service = ecs_patterns.NetworkLoadBalancedEc2Service(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    task_image_options=ecsPatterns.NetworkLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("test"),
        environment={
            "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
            "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
        }
    ),
    desired_count=2
)
```

* `NetworkLoadBalancedFargateService`

```python
# cluster: ecs.Cluster

load_balanced_fargate_service = ecs_patterns.NetworkLoadBalancedFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    cpu=512,
    task_image_options=ecsPatterns.NetworkLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    )
)
```

The CDK will create a new Amazon ECS cluster if you specify a VPC and omit `cluster`. If you deploy multiple services the CDK will only create one cluster per VPC.

If `cluster` and `vpc` are omitted, the CDK creates a new VPC with subnets in two Availability Zones and a cluster within this VPC.

If you specify the option `recordType` you can decide if you want the construct to use CNAME or Route53-Aliases as record sets.

Additionally, if more than one network target group is needed, instantiate one of the following:

* NetworkMultipleTargetGroupsEc2Service

```python
# Two network load balancers, each with their own listener and target group.
# cluster: ecs.Cluster

load_balanced_ec2_service = ecs_patterns.NetworkMultipleTargetGroupsEc2Service(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=256,
    task_image_options=ecsPatterns.NetworkLoadBalancedTaskImageProps(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    ),
    load_balancers=[ecsPatterns.NetworkLoadBalancerProps(
        name="lb1",
        listeners=[ecsPatterns.NetworkListenerProps(
            name="listener1"
        )
        ]
    ), ecsPatterns.NetworkLoadBalancerProps(
        name="lb2",
        listeners=[ecsPatterns.NetworkListenerProps(
            name="listener2"
        )
        ]
    )
    ],
    target_groups=[ecsPatterns.NetworkTargetProps(
        container_port=80,
        listener="listener1"
    ), ecsPatterns.NetworkTargetProps(
        container_port=90,
        listener="listener2"
    )
    ]
)
```

* NetworkMultipleTargetGroupsFargateService

```python
# Two network load balancers, each with their own listener and target group.
# cluster: ecs.Cluster

load_balanced_fargate_service = ecs_patterns.NetworkMultipleTargetGroupsFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=512,
    task_image_options=ecsPatterns.NetworkLoadBalancedTaskImageProps(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    ),
    load_balancers=[ecsPatterns.NetworkLoadBalancerProps(
        name="lb1",
        listeners=[ecsPatterns.NetworkListenerProps(
            name="listener1"
        )
        ]
    ), ecsPatterns.NetworkLoadBalancerProps(
        name="lb2",
        listeners=[ecsPatterns.NetworkListenerProps(
            name="listener2"
        )
        ]
    )
    ],
    target_groups=[ecsPatterns.NetworkTargetProps(
        container_port=80,
        listener="listener1"
    ), ecsPatterns.NetworkTargetProps(
        container_port=90,
        listener="listener2"
    )
    ]
)
```

## Queue Processing Services

To define a service that creates a queue and reads from that queue, instantiate one of the following:

* `QueueProcessingEc2Service`

```python
# cluster: ecs.Cluster

queue_processing_ec2_service = ecs_patterns.QueueProcessingEc2Service(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    image=ecs.ContainerImage.from_registry("test"),
    command=["-c", "4", "amazon.com"],
    enable_logging=False,
    desired_task_count=2,
    environment={
        "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
        "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
    },
    max_scaling_capacity=5,
    container_name="test"
)
```

* `QueueProcessingFargateService`

```python
# cluster: ecs.Cluster

queue_processing_fargate_service = ecs_patterns.QueueProcessingFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=512,
    image=ecs.ContainerImage.from_registry("test"),
    command=["-c", "4", "amazon.com"],
    enable_logging=False,
    desired_task_count=2,
    environment={
        "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
        "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
    },
    max_scaling_capacity=5,
    container_name="test"
)
```

when queue not provided by user, CDK will create a primary queue and a dead letter queue with default redrive policy and attach permission to the task to be able to access the primary queue.

## Scheduled Tasks

To define a task that runs periodically, there are 2 options:

* `ScheduledEc2Task`

```python
# Instantiate an Amazon EC2 Task to run at a scheduled interval
# cluster: ecs.Cluster

ecs_scheduled_task = ecs_patterns.ScheduledEc2Task(self, "ScheduledTask",
    cluster=cluster,
    scheduled_ec2_task_image_options=ecsPatterns.ScheduledEc2TaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
        memory_limit_mi_b=256,
        environment={"name": "TRIGGER", "value": "CloudWatch Events"}
    ),
    schedule=appscaling.Schedule.expression("rate(1 minute)"),
    enabled=True,
    rule_name="sample-scheduled-task-rule"
)
```

* `ScheduledFargateTask`

```python
# cluster: ecs.Cluster

scheduled_fargate_task = ecs_patterns.ScheduledFargateTask(self, "ScheduledFargateTask",
    cluster=cluster,
    scheduled_fargate_task_image_options=ecsPatterns.ScheduledFargateTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
        memory_limit_mi_b=512
    ),
    schedule=appscaling.Schedule.expression("rate(1 minute)"),
    platform_version=ecs.FargatePlatformVersion.LATEST
)
```

## Additional Examples

In addition to using the constructs, users can also add logic to customize these constructs:

### Configure HTTPS on an ApplicationLoadBalancedFargateService

```python
from aws_cdk.aws_route53 import HostedZone
from aws_cdk.aws_certificatemanager import Certificate
from aws_cdk.aws_elasticloadbalancingv2 import SslPolicy

# vpc: ec2.Vpc
# cluster: ecs.Cluster


domain_zone = HostedZone.from_lookup(self, "Zone", domain_name="example.com")
certificate = Certificate.from_certificate_arn(self, "Cert", "arn:aws:acm:us-east-1:123456:certificate/abcdefg")
load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
    vpc=vpc,
    cluster=cluster,
    certificate=certificate,
    ssl_policy=SslPolicy.RECOMMENDED,
    domain_name="api.example.com",
    domain_zone=domain_zone,
    redirect_hTTP=True,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    )
)
```

### Add Schedule-Based Auto-Scaling to an ApplicationLoadBalancedFargateService

```python
# cluster: ecs.Cluster

load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    desired_count=1,
    cpu=512,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    )
)

scalable_target = load_balanced_fargate_service.service.auto_scale_task_count(
    min_capacity=5,
    max_capacity=20
)

scalable_target.scale_on_schedule("DaytimeScaleDown",
    schedule=appscaling.Schedule.cron(hour="8", minute="0"),
    min_capacity=1
)

scalable_target.scale_on_schedule("EveningRushScaleUp",
    schedule=appscaling.Schedule.cron(hour="20", minute="0"),
    min_capacity=10
)
```

### Add Metric-Based Auto-Scaling to an ApplicationLoadBalancedFargateService

```python
# cluster: ecs.Cluster

load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    desired_count=1,
    cpu=512,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    )
)

scalable_target = load_balanced_fargate_service.service.auto_scale_task_count(
    min_capacity=1,
    max_capacity=20
)

scalable_target.scale_on_cpu_utilization("CpuScaling",
    target_utilization_percent=50
)

scalable_target.scale_on_memory_utilization("MemoryScaling",
    target_utilization_percent=50
)
```

### Change the default Deployment Controller

```python
# cluster: ecs.Cluster

load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    desired_count=1,
    cpu=512,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    ),
    deployment_controller=ecs.DeploymentController(
        type=ecs.DeploymentControllerType.CODE_DEPLOY
    )
)
```

### Deployment circuit breaker and rollback

Amazon ECS [deployment circuit breaker](https://aws.amazon.com/tw/blogs/containers/announcing-amazon-ecs-deployment-circuit-breaker/)
automatically rolls back unhealthy service deployments without the need for manual intervention. Use `circuitBreaker` to enable
deployment circuit breaker and optionally enable `rollback` for automatic rollback. See [Using the deployment circuit breaker](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html)
for more details.

```python
# cluster: ecs.Cluster

service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    desired_count=1,
    cpu=512,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    ),
    circuit_breaker=ecs.DeploymentCircuitBreaker(rollback=True)
)
```

### Set deployment configuration on QueueProcessingService

```python
# cluster: ecs.Cluster

queue_processing_fargate_service = ecs_patterns.QueueProcessingFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=512,
    image=ecs.ContainerImage.from_registry("test"),
    command=["-c", "4", "amazon.com"],
    enable_logging=False,
    desired_task_count=2,
    environment={},
    max_scaling_capacity=5,
    max_healthy_percent=200,
    min_healthy_percent=66
)
```

### Set taskSubnets and securityGroups for QueueProcessingFargateService

```python
# vpc: ec2.Vpc
# security_group: ec2.SecurityGroup

queue_processing_fargate_service = ecs_patterns.QueueProcessingFargateService(self, "Service",
    vpc=vpc,
    memory_limit_mi_b=512,
    image=ecs.ContainerImage.from_registry("test"),
    security_groups=[security_group],
    task_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)
)
```

### Define tasks with public IPs for QueueProcessingFargateService

```python
# vpc: ec2.Vpc

queue_processing_fargate_service = ecs_patterns.QueueProcessingFargateService(self, "Service",
    vpc=vpc,
    memory_limit_mi_b=512,
    image=ecs.ContainerImage.from_registry("test"),
    assign_public_ip=True
)
```

### Define tasks with custom queue parameters for QueueProcessingFargateService

```python
# vpc: ec2.Vpc

queue_processing_fargate_service = ecs_patterns.QueueProcessingFargateService(self, "Service",
    vpc=vpc,
    memory_limit_mi_b=512,
    image=ecs.ContainerImage.from_registry("test"),
    max_receive_count=42,
    retention_period=Duration.days(7),
    visibility_timeout=Duration.minutes(5)
)
```

### Set capacityProviderStrategies for QueueProcessingFargateService

```python
# cluster: ecs.Cluster

cluster.enable_fargate_capacity_providers()

queue_processing_fargate_service = ecs_patterns.QueueProcessingFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=512,
    image=ecs.ContainerImage.from_registry("test"),
    capacity_provider_strategies=[ecs.CapacityProviderStrategy(
        capacity_provider="FARGATE_SPOT",
        weight=2
    ), ecs.CapacityProviderStrategy(
        capacity_provider="FARGATE",
        weight=1
    )
    ]
)
```

### Set a custom container-level Healthcheck for QueueProcessingFargateService

```python
# vpc: ec2.Vpc
# security_group: ec2.SecurityGroup

queue_processing_fargate_service = ecs_patterns.QueueProcessingFargateService(self, "Service",
    vpc=vpc,
    memory_limit_mi_b=512,
    image=ecs.ContainerImage.from_registry("test"),
    health_check=ecs.HealthCheck(
        command=["CMD-SHELL", "curl -f http://localhost/ || exit 1"],
        # the properties below are optional
        interval=Duration.minutes(30),
        retries=123,
        start_period=Duration.minutes(30),
        timeout=Duration.minutes(30)
    )
)
```

### Set capacityProviderStrategies for QueueProcessingEc2Service

```python
import aws_cdk.aws_autoscaling as autoscaling


vpc = ec2.Vpc(self, "Vpc", max_azs=1)
cluster = ecs.Cluster(self, "EcsCluster", vpc=vpc)
auto_scaling_group = autoscaling.AutoScalingGroup(self, "asg",
    vpc=vpc,
    instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
    machine_image=ecs.EcsOptimizedImage.amazon_linux2()
)
capacity_provider = ecs.AsgCapacityProvider(self, "provider",
    auto_scaling_group=auto_scaling_group
)
cluster.add_asg_capacity_provider(capacity_provider)

queue_processing_fargate_service = ecs_patterns.QueueProcessingFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=512,
    image=ecs.ContainerImage.from_registry("test"),
    capacity_provider_strategies=[ecs.CapacityProviderStrategy(
        capacity_provider=capacity_provider.capacity_provider_name
    )
    ]
)
```

### Select specific vpc subnets for ApplicationLoadBalancedFargateService

```python
# cluster: ecs.Cluster

load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    desired_count=1,
    cpu=512,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    ),
    task_subnets=ec2.SubnetSelection(
        subnets=[ec2.Subnet.from_subnet_id(self, "subnet", "VpcISOLATEDSubnet1Subnet80F07FA0")]
    )
)
```

### Set PlatformVersion for ScheduledFargateTask

```python
# cluster: ecs.Cluster

scheduled_fargate_task = ecs_patterns.ScheduledFargateTask(self, "ScheduledFargateTask",
    cluster=cluster,
    scheduled_fargate_task_image_options=ecsPatterns.ScheduledFargateTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
        memory_limit_mi_b=512
    ),
    schedule=appscaling.Schedule.expression("rate(1 minute)"),
    platform_version=ecs.FargatePlatformVersion.VERSION1_4
)
```

### Set SecurityGroups for ScheduledFargateTask

```python
vpc = ec2.Vpc(self, "Vpc", max_azs=1)
cluster = ecs.Cluster(self, "EcsCluster", vpc=vpc)
security_group = ec2.SecurityGroup(self, "SG", vpc=vpc)

scheduled_fargate_task = ecs_patterns.ScheduledFargateTask(self, "ScheduledFargateTask",
    cluster=cluster,
    scheduled_fargate_task_image_options=ecsPatterns.ScheduledFargateTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
        memory_limit_mi_b=512
    ),
    schedule=appscaling.Schedule.expression("rate(1 minute)"),
    security_groups=[security_group]
)
```

### Use the REMOVE_DEFAULT_DESIRED_COUNT feature flag

The REMOVE_DEFAULT_DESIRED_COUNT feature flag is used to override the default desiredCount that is autogenerated by the CDK. This will set the desiredCount of any service created by any of the following constructs to be undefined.

* ApplicationLoadBalancedEc2Service
* ApplicationLoadBalancedFargateService
* NetworkLoadBalancedEc2Service
* NetworkLoadBalancedFargateService
* QueueProcessingEc2Service
* QueueProcessingFargateService

If a desiredCount is not passed in as input to the above constructs, CloudFormation will either create a new service to start up with a desiredCount of 1, or update an existing service to start up with the same desiredCount as prior to the update.

To enable the feature flag, ensure that the REMOVE_DEFAULT_DESIRED_COUNT flag within an application stack context is set to true, like so:

```python
# stack: Stack

stack.node.set_context(cxapi.ECS_REMOVE_DEFAULT_DESIRED_COUNT, True)
```

The following is an example of an application with the REMOVE_DEFAULT_DESIRED_COUNT feature flag enabled:

```python
from aws_cdk.core import App, Stack
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_ecs_patterns as ecs_patterns
import aws_cdk.cx_api as cxapi
import path as path

app = App()

stack = Stack(app, "aws-ecs-patterns-queue")
stack.node.set_context(cxapi.ECS_REMOVE_DEFAULT_DESIRED_COUNT, True)

vpc = ec2.Vpc(stack, "VPC",
    max_azs=2
)

ecs_patterns.QueueProcessingFargateService(stack, "QueueProcessingService",
    vpc=vpc,
    memory_limit_mi_b=512,
    image=ecs.AssetImage(path.join(__dirname, "..", "sqs-reader"))
)
```

### Deploy application and metrics sidecar

The following is an example of deploying an application along with a metrics sidecar container that utilizes `dockerLabels` for discovery:

```python
# cluster: ecs.Cluster
# vpc: ec2.Vpc

service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
    cluster=cluster,
    vpc=vpc,
    desired_count=1,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
        docker_labels={
            "application.label.one": "first_label",
            "application.label.two": "second_label"
        }
    )
)

service.task_definition.add_container("Sidecar",
    image=ecs.ContainerImage.from_registry("example/metrics-sidecar")
)
```

### Select specific load balancer name ApplicationLoadBalancedFargateService

```python
# cluster: ecs.Cluster

load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    desired_count=1,
    cpu=512,
    task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    ),
    task_subnets=ec2.SubnetSelection(
        subnets=[ec2.Subnet.from_subnet_id(self, "subnet", "VpcISOLATEDSubnet1Subnet80F07FA0")]
    ),
    load_balancer_name="application-lb-name"
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

import aws_cdk.aws_applicationautoscaling as _aws_cdk_aws_applicationautoscaling_a31e8c21
import aws_cdk.aws_certificatemanager as _aws_cdk_aws_certificatemanager_1662be0d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_67de8e8d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_7896c08f
import aws_cdk.aws_elasticloadbalancingv2 as _aws_cdk_aws_elasticloadbalancingv2_e93c784f
import aws_cdk.aws_events as _aws_cdk_aws_events_efcdfa54
import aws_cdk.aws_events_targets as _aws_cdk_aws_events_targets_3ef2ed32
import aws_cdk.aws_iam as _aws_cdk_aws_iam_940a1ce0
import aws_cdk.aws_route53 as _aws_cdk_aws_route53_f47b29d4
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_48bffef9
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationListenerProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "certificate": "certificate",
        "port": "port",
        "protocol": "protocol",
        "ssl_policy": "sslPolicy",
    },
)
class ApplicationListenerProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        certificate: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
        ssl_policy: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy] = None,
    ) -> None:
        '''Properties to define an application listener.

        :param name: Name of the listener.
        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: ApplicationProtocol.HTTP. If a certificate is specified, the protocol will be set by default to ApplicationProtocol.HTTPS.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported by the ALB Listener. Default: - The recommended elastic load balancing security policy

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_certificatemanager as certificatemanager
            import aws_cdk.aws_ecs_patterns as ecs_patterns
            import aws_cdk.aws_elasticloadbalancingv2 as elbv2
            
            # certificate: certificatemanager.Certificate
            
            application_listener_props = ecs_patterns.ApplicationListenerProps(
                name="name",
            
                # the properties below are optional
                certificate=certificate,
                port=123,
                protocol=elbv2.ApplicationProtocol.HTTP,
                ssl_policy=elbv2.SslPolicy.RECOMMENDED
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3067da453bdfb236a42f515dab378ee9078b61fce8e228bb295ecf85de24514)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument ssl_policy", value=ssl_policy, expected_type=type_hints["ssl_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if certificate is not None:
            self._values["certificate"] = certificate
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the listener.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate]:
        '''Certificate Manager certificate to associate with the load balancer.

        Setting this option will set the load balancer protocol to HTTPS.

        :default:

        - No certificate associated with the load balancer, if using
        the HTTP protocol. For HTTPS, a DNS-validated certificate will be
        created for the load balancer's specified domain name.
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port on which the listener listens for requests.

        :default: - Determined from protocol if known.
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol]:
        '''The protocol for connections from clients to the load balancer.

        The load balancer port is determined from the protocol (port 80 for
        HTTP, port 443 for HTTPS).  A domain name and zone must be also be
        specified if using HTTPS.

        :default:

        ApplicationProtocol.HTTP. If a certificate is specified, the protocol will be
        set by default to ApplicationProtocol.HTTPS.
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol], result)

    @builtins.property
    def ssl_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy]:
        '''The security policy that defines which ciphers and protocols are supported by the ALB Listener.

        :default: - The recommended elastic load balancing security policy
        '''
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationLoadBalancedServiceBase(
    _aws_cdk_core_f4b25747.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancedServiceBase",
):
    '''The base class for ApplicationLoadBalancedEc2Service and ApplicationLoadBalancedFargateService services.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        certificate: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate] = None,
        circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        domain_name: typing.Optional[builtins.str] = None,
        domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancer] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        max_healthy_percent: typing.Optional[jsii.Number] = None,
        min_healthy_percent: typing.Optional[jsii.Number] = None,
        open_listener: typing.Optional[builtins.bool] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
        protocol_version: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocolVersion] = None,
        public_load_balancer: typing.Optional[builtins.bool] = None,
        record_type: typing.Optional["ApplicationLoadBalancedServiceRecordType"] = None,
        redirect_http: typing.Optional[builtins.bool] = None,
        service_name: typing.Optional[builtins.str] = None,
        ssl_policy: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy] = None,
        target_protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
        task_image_options: typing.Optional[typing.Union["ApplicationLoadBalancedTaskImageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''Constructs a new instance of the ApplicationLoadBalancedServiceBase class.

        :param scope: -
        :param id: -
        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param circuit_breaker: Whether to enable the deployment circuit breaker. If this property is defined, circuit breaker will be implicitly enabled. Default: - disabled
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the application load balancer that will serve traffic to the service. Default: - The default listener port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        :param load_balancer: The application load balancer that will serve traffic to the service. The VPC attribute of a load balancer must be specified for it to be used to create a new service with this pattern. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param load_balancer_name: Name of the load balancer. Default: - Automatically generated name.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param open_listener: Determines whether or not the Security Group for the Load Balancer's Listener will be open to all traffic by default. Default: true -- The security group allows ingress from all IP addresses.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: HTTP. If a certificate is specified, the protocol will be set by default to HTTPS.
        :param protocol_version: The protocol version to use. Default: ApplicationProtocolVersion.HTTP1
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param record_type: Specifies whether the Route53 record should be a CNAME, an A record using the Alias feature or no record at all. This is useful if you need to work with DNS systems that do not support alias records. Default: ApplicationLoadBalancedServiceRecordType.ALIAS
        :param redirect_http: Specifies whether the load balancer should redirect traffic on port 80 to port 443 to support HTTP->HTTPS redirects This is only valid if the protocol of the ALB is HTTPS. Default: false
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported by the ALB Listener. Default: - The recommended elastic load balancing security policy
        :param target_protocol: The protocol for connections from the load balancer to the ECS tasks. The default target port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). Default: HTTP.
        :param task_image_options: The properties required to create a new task definition. TaskDefinition or TaskImageOptions must be specified, but not both. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64cef0537f934abf500aadc14d96bae4ddd374777926a6b04a5e374daa372fda)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApplicationLoadBalancedServiceBaseProps(
            certificate=certificate,
            circuit_breaker=circuit_breaker,
            cloud_map_options=cloud_map_options,
            cluster=cluster,
            deployment_controller=deployment_controller,
            desired_count=desired_count,
            domain_name=domain_name,
            domain_zone=domain_zone,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            health_check_grace_period=health_check_grace_period,
            listener_port=listener_port,
            load_balancer=load_balancer,
            load_balancer_name=load_balancer_name,
            max_healthy_percent=max_healthy_percent,
            min_healthy_percent=min_healthy_percent,
            open_listener=open_listener,
            propagate_tags=propagate_tags,
            protocol=protocol,
            protocol_version=protocol_version,
            public_load_balancer=public_load_balancer,
            record_type=record_type,
            redirect_http=redirect_http,
            service_name=service_name,
            ssl_policy=ssl_policy,
            target_protocol=target_protocol,
            task_image_options=task_image_options,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addServiceAsTarget")
    def _add_service_as_target(
        self,
        service: _aws_cdk_aws_ecs_7896c08f.BaseService,
    ) -> None:
        '''Adds service as a target of the target group.

        :param service: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee3ce64b0c866a07372c9c74a1d3165d4d06d3f390dbbf6a5e955e28357b0d9)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        return typing.cast(None, jsii.invoke(self, "addServiceAsTarget", [service]))

    @jsii.member(jsii_name="createAWSLogDriver")
    def _create_aws_log_driver(
        self,
        prefix: builtins.str,
    ) -> _aws_cdk_aws_ecs_7896c08f.AwsLogDriver:
        '''
        :param prefix: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a5807f3882c0013e0b55ecf11dcbbb3a972022f6139ffd9b66ce12d97a835b)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.AwsLogDriver, jsii.invoke(self, "createAWSLogDriver", [prefix]))

    @jsii.member(jsii_name="getDefaultCluster")
    def _get_default_cluster(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> _aws_cdk_aws_ecs_7896c08f.Cluster:
        '''Returns the default cluster.

        :param scope: -
        :param vpc: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50622e2557761392d3a1274f54e1282c365b271f31b99b698414a01b363c0bc0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.Cluster, jsii.invoke(self, "getDefaultCluster", [scope, vpc]))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _aws_cdk_aws_ecs_7896c08f.ICluster:
        '''The cluster that hosts the service.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.ICluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> jsii.Number:
        '''(deprecated) The desired number of instantiations of the task definition to keep running on the service.

        :deprecated: - Use ``internalDesiredCount`` instead.

        :stability: deprecated
        '''
        return typing.cast(jsii.Number, jsii.get(self, "desiredCount"))

    @builtins.property
    @jsii.member(jsii_name="listener")
    def listener(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationListener:
        '''The listener for the service.'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationListener, jsii.get(self, "listener"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer:
        '''The Application Load Balancer for the service.'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer, jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationTargetGroup:
        '''The target group for the service.'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationTargetGroup, jsii.get(self, "targetGroup"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate]:
        '''Certificate Manager certificate to associate with the load balancer.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate], jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="internalDesiredCount")
    def internal_desired_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        The default is 1 for all new services and uses the existing services desired count
        when updating an existing service if one is not provided.
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "internalDesiredCount"))

    @builtins.property
    @jsii.member(jsii_name="redirectListener")
    def redirect_listener(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationListener]:
        '''The redirect listener for the service if redirectHTTP is enabled.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationListener], jsii.get(self, "redirectListener"))


class _ApplicationLoadBalancedServiceBaseProxy(ApplicationLoadBalancedServiceBase):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ApplicationLoadBalancedServiceBase).__jsii_proxy_class__ = lambda : _ApplicationLoadBalancedServiceBaseProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancedServiceBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate": "certificate",
        "circuit_breaker": "circuitBreaker",
        "cloud_map_options": "cloudMapOptions",
        "cluster": "cluster",
        "deployment_controller": "deploymentController",
        "desired_count": "desiredCount",
        "domain_name": "domainName",
        "domain_zone": "domainZone",
        "enable_ecs_managed_tags": "enableECSManagedTags",
        "health_check_grace_period": "healthCheckGracePeriod",
        "listener_port": "listenerPort",
        "load_balancer": "loadBalancer",
        "load_balancer_name": "loadBalancerName",
        "max_healthy_percent": "maxHealthyPercent",
        "min_healthy_percent": "minHealthyPercent",
        "open_listener": "openListener",
        "propagate_tags": "propagateTags",
        "protocol": "protocol",
        "protocol_version": "protocolVersion",
        "public_load_balancer": "publicLoadBalancer",
        "record_type": "recordType",
        "redirect_http": "redirectHTTP",
        "service_name": "serviceName",
        "ssl_policy": "sslPolicy",
        "target_protocol": "targetProtocol",
        "task_image_options": "taskImageOptions",
        "vpc": "vpc",
    },
)
class ApplicationLoadBalancedServiceBaseProps:
    def __init__(
        self,
        *,
        certificate: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate] = None,
        circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        domain_name: typing.Optional[builtins.str] = None,
        domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancer] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        max_healthy_percent: typing.Optional[jsii.Number] = None,
        min_healthy_percent: typing.Optional[jsii.Number] = None,
        open_listener: typing.Optional[builtins.bool] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
        protocol_version: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocolVersion] = None,
        public_load_balancer: typing.Optional[builtins.bool] = None,
        record_type: typing.Optional["ApplicationLoadBalancedServiceRecordType"] = None,
        redirect_http: typing.Optional[builtins.bool] = None,
        service_name: typing.Optional[builtins.str] = None,
        ssl_policy: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy] = None,
        target_protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
        task_image_options: typing.Optional[typing.Union["ApplicationLoadBalancedTaskImageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''The properties for the base ApplicationLoadBalancedEc2Service or ApplicationLoadBalancedFargateService service.

        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param circuit_breaker: Whether to enable the deployment circuit breaker. If this property is defined, circuit breaker will be implicitly enabled. Default: - disabled
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the application load balancer that will serve traffic to the service. Default: - The default listener port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        :param load_balancer: The application load balancer that will serve traffic to the service. The VPC attribute of a load balancer must be specified for it to be used to create a new service with this pattern. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param load_balancer_name: Name of the load balancer. Default: - Automatically generated name.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param open_listener: Determines whether or not the Security Group for the Load Balancer's Listener will be open to all traffic by default. Default: true -- The security group allows ingress from all IP addresses.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: HTTP. If a certificate is specified, the protocol will be set by default to HTTPS.
        :param protocol_version: The protocol version to use. Default: ApplicationProtocolVersion.HTTP1
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param record_type: Specifies whether the Route53 record should be a CNAME, an A record using the Alias feature or no record at all. This is useful if you need to work with DNS systems that do not support alias records. Default: ApplicationLoadBalancedServiceRecordType.ALIAS
        :param redirect_http: Specifies whether the load balancer should redirect traffic on port 80 to port 443 to support HTTP->HTTPS redirects This is only valid if the protocol of the ALB is HTTPS. Default: false
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported by the ALB Listener. Default: - The recommended elastic load balancing security policy
        :param target_protocol: The protocol for connections from the load balancer to the ECS tasks. The default target port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). Default: HTTP.
        :param task_image_options: The properties required to create a new task definition. TaskDefinition or TaskImageOptions must be specified, but not both. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_certificatemanager as certificatemanager
            import aws_cdk.aws_ec2 as ec2
            import aws_cdk.aws_ecs as ecs
            import aws_cdk.aws_ecs_patterns as ecs_patterns
            import aws_cdk.aws_elasticloadbalancingv2 as elbv2
            import aws_cdk.aws_iam as iam
            import aws_cdk.aws_route53 as route53
            import aws_cdk.aws_servicediscovery as servicediscovery
            import aws_cdk.core as cdk
            
            # application_load_balancer: elbv2.ApplicationLoadBalancer
            # certificate: certificatemanager.Certificate
            # cluster: ecs.Cluster
            # container_definition: ecs.ContainerDefinition
            # container_image: ecs.ContainerImage
            # hosted_zone: route53.HostedZone
            # log_driver: ecs.LogDriver
            # namespace: servicediscovery.INamespace
            # role: iam.Role
            # secret: ecs.Secret
            # vpc: ec2.Vpc
            
            application_load_balanced_service_base_props = ecs_patterns.ApplicationLoadBalancedServiceBaseProps(
                certificate=certificate,
                circuit_breaker=ecs.DeploymentCircuitBreaker(
                    rollback=False
                ),
                cloud_map_options=ecs.CloudMapOptions(
                    cloud_map_namespace=namespace,
                    container=container_definition,
                    container_port=123,
                    dns_record_type=servicediscovery.DnsRecordType.A,
                    dns_ttl=cdk.Duration.minutes(30),
                    failure_threshold=123,
                    name="name"
                ),
                cluster=cluster,
                deployment_controller=ecs.DeploymentController(
                    type=ecs.DeploymentControllerType.ECS
                ),
                desired_count=123,
                domain_name="domainName",
                domain_zone=hosted_zone,
                enable_eCSManaged_tags=False,
                health_check_grace_period=cdk.Duration.minutes(30),
                listener_port=123,
                load_balancer=application_load_balancer,
                load_balancer_name="loadBalancerName",
                max_healthy_percent=123,
                min_healthy_percent=123,
                open_listener=False,
                propagate_tags=ecs.PropagatedTagSource.SERVICE,
                protocol=elbv2.ApplicationProtocol.HTTP,
                protocol_version=elbv2.ApplicationProtocolVersion.GRPC,
                public_load_balancer=False,
                record_type=ecs_patterns.ApplicationLoadBalancedServiceRecordType.ALIAS,
                redirect_hTTP=False,
                service_name="serviceName",
                ssl_policy=elbv2.SslPolicy.RECOMMENDED,
                target_protocol=elbv2.ApplicationProtocol.HTTP,
                task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                    image=container_image,
            
                    # the properties below are optional
                    container_name="containerName",
                    container_port=123,
                    docker_labels={
                        "docker_labels_key": "dockerLabels"
                    },
                    enable_logging=False,
                    environment={
                        "environment_key": "environment"
                    },
                    execution_role=role,
                    family="family",
                    log_driver=log_driver,
                    secrets={
                        "secrets_key": secret
                    },
                    task_role=role
                ),
                vpc=vpc
            )
        '''
        if isinstance(circuit_breaker, dict):
            circuit_breaker = _aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker(**circuit_breaker)
        if isinstance(cloud_map_options, dict):
            cloud_map_options = _aws_cdk_aws_ecs_7896c08f.CloudMapOptions(**cloud_map_options)
        if isinstance(deployment_controller, dict):
            deployment_controller = _aws_cdk_aws_ecs_7896c08f.DeploymentController(**deployment_controller)
        if isinstance(task_image_options, dict):
            task_image_options = ApplicationLoadBalancedTaskImageOptions(**task_image_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c82f51600f49a1d66311d7d86addbe41bd436f95507e2f35c0462edfcefb6fed)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument circuit_breaker", value=circuit_breaker, expected_type=type_hints["circuit_breaker"])
            check_type(argname="argument cloud_map_options", value=cloud_map_options, expected_type=type_hints["cloud_map_options"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument deployment_controller", value=deployment_controller, expected_type=type_hints["deployment_controller"])
            check_type(argname="argument desired_count", value=desired_count, expected_type=type_hints["desired_count"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_zone", value=domain_zone, expected_type=type_hints["domain_zone"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument health_check_grace_period", value=health_check_grace_period, expected_type=type_hints["health_check_grace_period"])
            check_type(argname="argument listener_port", value=listener_port, expected_type=type_hints["listener_port"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument load_balancer_name", value=load_balancer_name, expected_type=type_hints["load_balancer_name"])
            check_type(argname="argument max_healthy_percent", value=max_healthy_percent, expected_type=type_hints["max_healthy_percent"])
            check_type(argname="argument min_healthy_percent", value=min_healthy_percent, expected_type=type_hints["min_healthy_percent"])
            check_type(argname="argument open_listener", value=open_listener, expected_type=type_hints["open_listener"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument protocol_version", value=protocol_version, expected_type=type_hints["protocol_version"])
            check_type(argname="argument public_load_balancer", value=public_load_balancer, expected_type=type_hints["public_load_balancer"])
            check_type(argname="argument record_type", value=record_type, expected_type=type_hints["record_type"])
            check_type(argname="argument redirect_http", value=redirect_http, expected_type=type_hints["redirect_http"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument ssl_policy", value=ssl_policy, expected_type=type_hints["ssl_policy"])
            check_type(argname="argument target_protocol", value=target_protocol, expected_type=type_hints["target_protocol"])
            check_type(argname="argument task_image_options", value=task_image_options, expected_type=type_hints["task_image_options"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate is not None:
            self._values["certificate"] = certificate
        if circuit_breaker is not None:
            self._values["circuit_breaker"] = circuit_breaker
        if cloud_map_options is not None:
            self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None:
            self._values["cluster"] = cluster
        if deployment_controller is not None:
            self._values["deployment_controller"] = deployment_controller
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if domain_zone is not None:
            self._values["domain_zone"] = domain_zone
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None:
            self._values["health_check_grace_period"] = health_check_grace_period
        if listener_port is not None:
            self._values["listener_port"] = listener_port
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if load_balancer_name is not None:
            self._values["load_balancer_name"] = load_balancer_name
        if max_healthy_percent is not None:
            self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None:
            self._values["min_healthy_percent"] = min_healthy_percent
        if open_listener is not None:
            self._values["open_listener"] = open_listener
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if protocol is not None:
            self._values["protocol"] = protocol
        if protocol_version is not None:
            self._values["protocol_version"] = protocol_version
        if public_load_balancer is not None:
            self._values["public_load_balancer"] = public_load_balancer
        if record_type is not None:
            self._values["record_type"] = record_type
        if redirect_http is not None:
            self._values["redirect_http"] = redirect_http
        if service_name is not None:
            self._values["service_name"] = service_name
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy
        if target_protocol is not None:
            self._values["target_protocol"] = target_protocol
        if task_image_options is not None:
            self._values["task_image_options"] = task_image_options
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate]:
        '''Certificate Manager certificate to associate with the load balancer.

        Setting this option will set the load balancer protocol to HTTPS.

        :default:

        - No certificate associated with the load balancer, if using
        the HTTP protocol. For HTTPS, a DNS-validated certificate will be
        created for the load balancer's specified domain name.
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate], result)

    @builtins.property
    def circuit_breaker(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker]:
        '''Whether to enable the deployment circuit breaker.

        If this property is defined, circuit breaker will be implicitly
        enabled.

        :default: - disabled
        '''
        result = self._values.get("circuit_breaker")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker], result)

    @builtins.property
    def cloud_map_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions]:
        '''The options for configuring an Amazon ECS service to use service discovery.

        :default: - AWS Cloud Map service discovery is not enabled.
        '''
        result = self._values.get("cloud_map_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions], result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster]:
        '''The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster], result)

    @builtins.property
    def deployment_controller(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentController]:
        '''Specifies which deployment controller to use for the service.

        For more information, see
        `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_

        :default: - Rolling update (ECS)
        '''
        result = self._values.get("deployment_controller")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentController], result)

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        :default:

        - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1;
        if true, the default is 1 for all new services and uses the existing services desired count
        when updating an existing service.
        '''
        result = self._values.get("desired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name for the service, e.g. "api.example.com.".

        :default: - No domain name.
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_zone(self) -> typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone]:
        '''The Route53 hosted zone for the domain, e.g. "example.com.".

        :default: - No Route53 hosted domain zone.
        '''
        result = self._values.get("domain_zone")
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone], result)

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        :default: false
        '''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def health_check_grace_period(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        '''
        result = self._values.get("health_check_grace_period")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        '''Listener port of the application load balancer that will serve traffic to the service.

        :default:

        - The default listener port is determined from the protocol (port 80 for HTTP,
        port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        '''
        result = self._values.get("listener_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def load_balancer(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancer]:
        '''The application load balancer that will serve traffic to the service.

        The VPC attribute of a load balancer must be specified for it to be used
        to create a new service with this pattern.

        [disable-awslint:ref-via-interface]

        :default: - a new load balancer will be created.
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancer], result)

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[builtins.str]:
        '''Name of the load balancer.

        :default: - Automatically generated name.
        '''
        result = self._values.get("load_balancer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        :default: - 100 if daemon, otherwise 200
        '''
        result = self._values.get("max_healthy_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        :default: - 0 if daemon, otherwise 50
        '''
        result = self._values.get("min_healthy_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def open_listener(self) -> typing.Optional[builtins.bool]:
        '''Determines whether or not the Security Group for the Load Balancer's Listener will be open to all traffic by default.

        :default: true -- The security group allows ingress from all IP addresses.
        '''
        result = self._values.get("open_listener")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def propagate_tags(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource]:
        '''Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        :default: - none
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource], result)

    @builtins.property
    def protocol(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol]:
        '''The protocol for connections from clients to the load balancer.

        The load balancer port is determined from the protocol (port 80 for
        HTTP, port 443 for HTTPS).  A domain name and zone must be also be
        specified if using HTTPS.

        :default:

        HTTP. If a certificate is specified, the protocol will be
        set by default to HTTPS.
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol], result)

    @builtins.property
    def protocol_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocolVersion]:
        '''The protocol version to use.

        :default: ApplicationProtocolVersion.HTTP1
        '''
        result = self._values.get("protocol_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocolVersion], result)

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[builtins.bool]:
        '''Determines whether the Load Balancer will be internet-facing.

        :default: true
        '''
        result = self._values.get("public_load_balancer")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def record_type(
        self,
    ) -> typing.Optional["ApplicationLoadBalancedServiceRecordType"]:
        '''Specifies whether the Route53 record should be a CNAME, an A record using the Alias feature or no record at all.

        This is useful if you need to work with DNS systems that do not support alias records.

        :default: ApplicationLoadBalancedServiceRecordType.ALIAS
        '''
        result = self._values.get("record_type")
        return typing.cast(typing.Optional["ApplicationLoadBalancedServiceRecordType"], result)

    @builtins.property
    def redirect_http(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether the load balancer should redirect traffic on port 80 to port 443 to support HTTP->HTTPS redirects This is only valid if the protocol of the ALB is HTTPS.

        :default: false
        '''
        result = self._values.get("redirect_http")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        :default: - CloudFormation-generated name.
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy]:
        '''The security policy that defines which ciphers and protocols are supported by the ALB Listener.

        :default: - The recommended elastic load balancing security policy
        '''
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy], result)

    @builtins.property
    def target_protocol(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol]:
        '''The protocol for connections from the load balancer to the ECS tasks.

        The default target port is determined from the protocol (port 80 for
        HTTP, port 443 for HTTPS).

        :default: HTTP.
        '''
        result = self._values.get("target_protocol")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol], result)

    @builtins.property
    def task_image_options(
        self,
    ) -> typing.Optional["ApplicationLoadBalancedTaskImageOptions"]:
        '''The properties required to create a new task definition.

        TaskDefinition or TaskImageOptions must be specified, but not both.

        :default: none
        '''
        result = self._values.get("task_image_options")
        return typing.cast(typing.Optional["ApplicationLoadBalancedTaskImageOptions"], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        :default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationLoadBalancedServiceBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancedServiceRecordType"
)
class ApplicationLoadBalancedServiceRecordType(enum.Enum):
    '''Describes the type of DNS record the service should create.'''

    ALIAS = "ALIAS"
    '''Create Route53 A Alias record.'''
    CNAME = "CNAME"
    '''Create a CNAME record.'''
    NONE = "NONE"
    '''Do not create any DNS records.'''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancedTaskImageOptions",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "container_name": "containerName",
        "container_port": "containerPort",
        "docker_labels": "dockerLabels",
        "enable_logging": "enableLogging",
        "environment": "environment",
        "execution_role": "executionRole",
        "family": "family",
        "log_driver": "logDriver",
        "secrets": "secrets",
        "task_role": "taskRole",
    },
)
class ApplicationLoadBalancedTaskImageOptions:
    def __init__(
        self,
        *,
        image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
        container_name: typing.Optional[builtins.str] = None,
        container_port: typing.Optional[jsii.Number] = None,
        docker_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        execution_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        family: typing.Optional[builtins.str] = None,
        log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
        task_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''
        :param image: The image used to start a container. Image or taskDefinition must be specified, not both. Default: - none
        :param container_name: The container name value to be specified in the task definition. Default: - none
        :param container_port: The port number on the container that is bound to the user-specified or automatically assigned host port. If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort. If you are using containers in a task with the bridge network mode and you specify a container port and not a host port, your container automatically receives a host port in the ephemeral port range. Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance. For more information, see `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_. Default: 80
        :param docker_labels: A key/value map of labels to add to the container. Default: - No labels.
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param execution_role: The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf. Default: - No value
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param task_role: The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.

        :exampleMetadata: infused

        Example::

            # cluster: ecs.Cluster
            
            load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
                cluster=cluster,
                memory_limit_mi_b=1024,
                desired_count=1,
                cpu=512,
                task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
                    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
                ),
                task_subnets=ec2.SubnetSelection(
                    subnets=[ec2.Subnet.from_subnet_id(self, "subnet", "VpcISOLATEDSubnet1Subnet80F07FA0")]
                ),
                load_balancer_name="application-lb-name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05aaf3feaac7e0a061b38a68c16d0b8804ffb202f7905eb0929220547635e0da)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument container_port", value=container_port, expected_type=type_hints["container_port"])
            check_type(argname="argument docker_labels", value=docker_labels, expected_type=type_hints["docker_labels"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
            check_type(argname="argument log_driver", value=log_driver, expected_type=type_hints["log_driver"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument task_role", value=task_role, expected_type=type_hints["task_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if container_name is not None:
            self._values["container_name"] = container_name
        if container_port is not None:
            self._values["container_port"] = container_port
        if docker_labels is not None:
            self._values["docker_labels"] = docker_labels
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if environment is not None:
            self._values["environment"] = environment
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if family is not None:
            self._values["family"] = family
        if log_driver is not None:
            self._values["log_driver"] = log_driver
        if secrets is not None:
            self._values["secrets"] = secrets
        if task_role is not None:
            self._values["task_role"] = task_role

    @builtins.property
    def image(self) -> _aws_cdk_aws_ecs_7896c08f.ContainerImage:
        '''The image used to start a container.

        Image or taskDefinition must be specified, not both.

        :default: - none
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.ContainerImage, result)

    @builtins.property
    def container_name(self) -> typing.Optional[builtins.str]:
        '''The container name value to be specified in the task definition.

        :default: - none
        '''
        result = self._values.get("container_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_port(self) -> typing.Optional[jsii.Number]:
        '''The port number on the container that is bound to the user-specified or automatically assigned host port.

        If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort.
        If you are using containers in a task with the bridge network mode and you specify a container port and not a host port,
        your container automatically receives a host port in the ephemeral port range.

        Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance.

        For more information, see
        `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_.

        :default: 80
        '''
        result = self._values.get("container_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def docker_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A key/value map of labels to add to the container.

        :default: - No labels.
        '''
        result = self._values.get("docker_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''Flag to indicate whether to enable logging.

        :default: true
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The environment variables to pass to the container.

        :default: - No environment variables.
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf.

        :default: - No value
        '''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    @builtins.property
    def family(self) -> typing.Optional[builtins.str]:
        '''The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        :default: - Automatically generated name.
        '''
        result = self._values.get("family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_driver(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver]:
        '''The log driver to use.

        :default: - AwsLogDriver if enableLogging is true
        '''
        result = self._values.get("log_driver")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]]:
        '''The secret to expose to the container as an environment variable.

        :default: - No secret environment variables.
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]], result)

    @builtins.property
    def task_role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        :default: - A task role is automatically created for you.
        '''
        result = self._values.get("task_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationLoadBalancedTaskImageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancedTaskImageProps",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "container_name": "containerName",
        "container_ports": "containerPorts",
        "docker_labels": "dockerLabels",
        "enable_logging": "enableLogging",
        "environment": "environment",
        "execution_role": "executionRole",
        "family": "family",
        "log_driver": "logDriver",
        "secrets": "secrets",
        "task_role": "taskRole",
    },
)
class ApplicationLoadBalancedTaskImageProps:
    def __init__(
        self,
        *,
        image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
        container_name: typing.Optional[builtins.str] = None,
        container_ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
        docker_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        execution_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        family: typing.Optional[builtins.str] = None,
        log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
        task_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''Options for configuring a new container.

        :param image: The image used to start a container. Image or taskDefinition must be specified, not both. Default: - none
        :param container_name: The container name value to be specified in the task definition. Default: - web
        :param container_ports: A list of port numbers on the container that is bound to the user-specified or automatically assigned host port. If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort. If you are using containers in a task with the bridge network mode and you specify a container port and not a host port, your container automatically receives a host port in the ephemeral port range. Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance. For more information, see `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_. Default: - [80]
        :param docker_labels: A key/value map of labels to add to the container. Default: - No labels.
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param execution_role: The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf. Default: - No value
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secrets to expose to the container as an environment variable. Default: - No secret environment variables.
        :param task_role: The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.

        :exampleMetadata: infused

        Example::

            # One application load balancer with one listener and two target groups.
            # cluster: ecs.Cluster
            
            load_balanced_ec2_service = ecs_patterns.ApplicationMultipleTargetGroupsEc2Service(self, "Service",
                cluster=cluster,
                memory_limit_mi_b=256,
                task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageProps(
                    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
                ),
                target_groups=[ecsPatterns.ApplicationTargetProps(
                    container_port=80
                ), ecsPatterns.ApplicationTargetProps(
                    container_port=90,
                    path_pattern="a/b/c",
                    priority=10
                )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c36449e1f00ba60ffc4a815353a98eb5ffcbe30826d188158a6da9d2c203a51)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument container_ports", value=container_ports, expected_type=type_hints["container_ports"])
            check_type(argname="argument docker_labels", value=docker_labels, expected_type=type_hints["docker_labels"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
            check_type(argname="argument log_driver", value=log_driver, expected_type=type_hints["log_driver"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument task_role", value=task_role, expected_type=type_hints["task_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if container_name is not None:
            self._values["container_name"] = container_name
        if container_ports is not None:
            self._values["container_ports"] = container_ports
        if docker_labels is not None:
            self._values["docker_labels"] = docker_labels
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if environment is not None:
            self._values["environment"] = environment
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if family is not None:
            self._values["family"] = family
        if log_driver is not None:
            self._values["log_driver"] = log_driver
        if secrets is not None:
            self._values["secrets"] = secrets
        if task_role is not None:
            self._values["task_role"] = task_role

    @builtins.property
    def image(self) -> _aws_cdk_aws_ecs_7896c08f.ContainerImage:
        '''The image used to start a container.

        Image or taskDefinition must be specified, not both.

        :default: - none
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.ContainerImage, result)

    @builtins.property
    def container_name(self) -> typing.Optional[builtins.str]:
        '''The container name value to be specified in the task definition.

        :default: - web
        '''
        result = self._values.get("container_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''A list of port numbers on the container that is bound to the user-specified or automatically assigned host port.

        If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort.
        If you are using containers in a task with the bridge network mode and you specify a container port and not a host port,
        your container automatically receives a host port in the ephemeral port range.

        Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance.

        For more information, see
        `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_.

        :default: - [80]
        '''
        result = self._values.get("container_ports")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def docker_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A key/value map of labels to add to the container.

        :default: - No labels.
        '''
        result = self._values.get("docker_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''Flag to indicate whether to enable logging.

        :default: true
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The environment variables to pass to the container.

        :default: - No environment variables.
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf.

        :default: - No value
        '''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    @builtins.property
    def family(self) -> typing.Optional[builtins.str]:
        '''The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        :default: - Automatically generated name.
        '''
        result = self._values.get("family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_driver(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver]:
        '''The log driver to use.

        :default: - AwsLogDriver if enableLogging is true
        '''
        result = self._values.get("log_driver")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]]:
        '''The secrets to expose to the container as an environment variable.

        :default: - No secret environment variables.
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]], result)

    @builtins.property
    def task_role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        :default: - A task role is automatically created for you.
        '''
        result = self._values.get("task_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationLoadBalancedTaskImageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancerProps",
    jsii_struct_bases=[],
    name_mapping={
        "listeners": "listeners",
        "name": "name",
        "domain_name": "domainName",
        "domain_zone": "domainZone",
        "public_load_balancer": "publicLoadBalancer",
    },
)
class ApplicationLoadBalancerProps:
    def __init__(
        self,
        *,
        listeners: typing.Sequence[typing.Union[ApplicationListenerProps, typing.Dict[builtins.str, typing.Any]]],
        name: builtins.str,
        domain_name: typing.Optional[builtins.str] = None,
        domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
        public_load_balancer: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Properties to define an application load balancer.

        :param listeners: Listeners (at least one listener) attached to this load balancer.
        :param name: Name of the load balancer.
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_certificatemanager as certificatemanager
            import aws_cdk.aws_ecs_patterns as ecs_patterns
            import aws_cdk.aws_elasticloadbalancingv2 as elbv2
            import aws_cdk.aws_route53 as route53
            
            # certificate: certificatemanager.Certificate
            # hosted_zone: route53.HostedZone
            
            application_load_balancer_props = ecs_patterns.ApplicationLoadBalancerProps(
                listeners=[ecs_patterns.ApplicationListenerProps(
                    name="name",
            
                    # the properties below are optional
                    certificate=certificate,
                    port=123,
                    protocol=elbv2.ApplicationProtocol.HTTP,
                    ssl_policy=elbv2.SslPolicy.RECOMMENDED
                )],
                name="name",
            
                # the properties below are optional
                domain_name="domainName",
                domain_zone=hosted_zone,
                public_load_balancer=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c36e9ce37de9abe32e03123541059975748aa637bdc219b9dd4b048003c55f3a)
            check_type(argname="argument listeners", value=listeners, expected_type=type_hints["listeners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_zone", value=domain_zone, expected_type=type_hints["domain_zone"])
            check_type(argname="argument public_load_balancer", value=public_load_balancer, expected_type=type_hints["public_load_balancer"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "listeners": listeners,
            "name": name,
        }
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if domain_zone is not None:
            self._values["domain_zone"] = domain_zone
        if public_load_balancer is not None:
            self._values["public_load_balancer"] = public_load_balancer

    @builtins.property
    def listeners(self) -> typing.List[ApplicationListenerProps]:
        '''Listeners (at least one listener) attached to this load balancer.'''
        result = self._values.get("listeners")
        assert result is not None, "Required property 'listeners' is missing"
        return typing.cast(typing.List[ApplicationListenerProps], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the load balancer.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name for the service, e.g. "api.example.com.".

        :default: - No domain name.
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_zone(self) -> typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone]:
        '''The Route53 hosted zone for the domain, e.g. "example.com.".

        :default: - No Route53 hosted domain zone.
        '''
        result = self._values.get("domain_zone")
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone], result)

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[builtins.bool]:
        '''Determines whether the Load Balancer will be internet-facing.

        :default: true
        '''
        result = self._values.get("public_load_balancer")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationLoadBalancerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationMultipleTargetGroupsServiceBase(
    _aws_cdk_core_f4b25747.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationMultipleTargetGroupsServiceBase",
):
    '''The base class for ApplicationMultipleTargetGroupsEc2Service and ApplicationMultipleTargetGroupsFargateService classes.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        load_balancers: typing.Optional[typing.Sequence[typing.Union[ApplicationLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        service_name: typing.Optional[builtins.str] = None,
        target_groups: typing.Optional[typing.Sequence[typing.Union["ApplicationTargetProps", typing.Dict[builtins.str, typing.Any]]]] = None,
        task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''Constructs a new instance of the ApplicationMultipleTargetGroupsServiceBase class.

        :param scope: -
        :param id: -
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The application load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify ALB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3564cc867433df94aab33ec6839a667de0e7a111caa89a666dbd8bf94880b88)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApplicationMultipleTargetGroupsServiceBaseProps(
            cloud_map_options=cloud_map_options,
            cluster=cluster,
            desired_count=desired_count,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            health_check_grace_period=health_check_grace_period,
            load_balancers=load_balancers,
            propagate_tags=propagate_tags,
            service_name=service_name,
            target_groups=target_groups,
            task_image_options=task_image_options,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addPortMappingForTargets")
    def _add_port_mapping_for_targets(
        self,
        container: _aws_cdk_aws_ecs_7896c08f.ContainerDefinition,
        targets: typing.Sequence[typing.Union["ApplicationTargetProps", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param container: -
        :param targets: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f39fdfd284662cd903359ba08362455d0a225b3aebfc5fd421c22301bafb4653)
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        return typing.cast(None, jsii.invoke(self, "addPortMappingForTargets", [container, targets]))

    @jsii.member(jsii_name="createAWSLogDriver")
    def _create_aws_log_driver(
        self,
        prefix: builtins.str,
    ) -> _aws_cdk_aws_ecs_7896c08f.AwsLogDriver:
        '''
        :param prefix: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65e54df5373c25b4b95c91584003b8158e5ecbaba3ca5e44f3186ac69a12f3c3)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.AwsLogDriver, jsii.invoke(self, "createAWSLogDriver", [prefix]))

    @jsii.member(jsii_name="findListener")
    def _find_listener(
        self,
        name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationListener:
        '''
        :param name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__947f8ee5f4b0dca3f170bf6db7dd4997985e1d6abad2a941c89b9ac9f0978468)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationListener, jsii.invoke(self, "findListener", [name]))

    @jsii.member(jsii_name="getDefaultCluster")
    def _get_default_cluster(
        self,
        scope: _constructs_77d1e7e8.Construct,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> _aws_cdk_aws_ecs_7896c08f.Cluster:
        '''Returns the default cluster.

        :param scope: -
        :param vpc: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c40bbd7753c10b67c4f32f1cb3f3e00c10880e06b7b11a8886c99f1bb3ea356)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.Cluster, jsii.invoke(self, "getDefaultCluster", [scope, vpc]))

    @jsii.member(jsii_name="registerECSTargets")
    def _register_ecs_targets(
        self,
        service: _aws_cdk_aws_ecs_7896c08f.BaseService,
        container: _aws_cdk_aws_ecs_7896c08f.ContainerDefinition,
        targets: typing.Sequence[typing.Union["ApplicationTargetProps", typing.Dict[builtins.str, typing.Any]]],
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationTargetGroup:
        '''
        :param service: -
        :param container: -
        :param targets: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f5f7362e36627303c74ffdfa6958885622b66d4b604e7aa500ad76cb88776e8)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationTargetGroup, jsii.invoke(self, "registerECSTargets", [service, container, targets]))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _aws_cdk_aws_ecs_7896c08f.ICluster:
        '''The cluster that hosts the service.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.ICluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> jsii.Number:
        '''(deprecated) The desired number of instantiations of the task definition to keep running on the service.

        :deprecated: - Use ``internalDesiredCount`` instead.

        :stability: deprecated
        '''
        return typing.cast(jsii.Number, jsii.get(self, "desiredCount"))

    @builtins.property
    @jsii.member(jsii_name="listener")
    def listener(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationListener:
        '''The default listener for the service (first added listener).'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationListener, jsii.get(self, "listener"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer:
        '''The default Application Load Balancer for the service (first added load balancer).'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationLoadBalancer, jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="internalDesiredCount")
    def internal_desired_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        The default is 1 for all new services and uses the existing services desired count
        when updating an existing service, if one is not provided.
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "internalDesiredCount"))

    @builtins.property
    @jsii.member(jsii_name="listeners")
    def _listeners(
        self,
    ) -> typing.List[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationListener]:
        return typing.cast(typing.List[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationListener], jsii.get(self, "listeners"))

    @_listeners.setter
    def _listeners(
        self,
        value: typing.List[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationListener],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d43742552dd69939407f4214a661813dce4c1e8c0ae93404d573fabc1a5061e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listeners", value)

    @builtins.property
    @jsii.member(jsii_name="targetGroups")
    def _target_groups(
        self,
    ) -> typing.List[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationTargetGroup]:
        return typing.cast(typing.List[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationTargetGroup], jsii.get(self, "targetGroups"))

    @_target_groups.setter
    def _target_groups(
        self,
        value: typing.List[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationTargetGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abfc91945bf5dc36f7caa9b6e7f0b3262ed07f6d78ac4a06d47e3e16c5f01841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetGroups", value)

    @builtins.property
    @jsii.member(jsii_name="logDriver")
    def _log_driver(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver]:
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver], jsii.get(self, "logDriver"))

    @_log_driver.setter
    def _log_driver(
        self,
        value: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bfac22edba40356132b69f334f71c4832769fcefd9e52cb6b9ba7326223f746)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logDriver", value)


class _ApplicationMultipleTargetGroupsServiceBaseProxy(
    ApplicationMultipleTargetGroupsServiceBase,
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ApplicationMultipleTargetGroupsServiceBase).__jsii_proxy_class__ = lambda : _ApplicationMultipleTargetGroupsServiceBaseProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationMultipleTargetGroupsServiceBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_map_options": "cloudMapOptions",
        "cluster": "cluster",
        "desired_count": "desiredCount",
        "enable_ecs_managed_tags": "enableECSManagedTags",
        "health_check_grace_period": "healthCheckGracePeriod",
        "load_balancers": "loadBalancers",
        "propagate_tags": "propagateTags",
        "service_name": "serviceName",
        "target_groups": "targetGroups",
        "task_image_options": "taskImageOptions",
        "vpc": "vpc",
    },
)
class ApplicationMultipleTargetGroupsServiceBaseProps:
    def __init__(
        self,
        *,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        load_balancers: typing.Optional[typing.Sequence[typing.Union[ApplicationLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        service_name: typing.Optional[builtins.str] = None,
        target_groups: typing.Optional[typing.Sequence[typing.Union["ApplicationTargetProps", typing.Dict[builtins.str, typing.Any]]]] = None,
        task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''The properties for the base ApplicationMultipleTargetGroupsEc2Service or ApplicationMultipleTargetGroupsFargateService service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The application load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify ALB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_certificatemanager as certificatemanager
            import aws_cdk.aws_ec2 as ec2
            import aws_cdk.aws_ecs as ecs
            import aws_cdk.aws_ecs_patterns as ecs_patterns
            import aws_cdk.aws_elasticloadbalancingv2 as elbv2
            import aws_cdk.aws_iam as iam
            import aws_cdk.aws_route53 as route53
            import aws_cdk.aws_servicediscovery as servicediscovery
            import aws_cdk.core as cdk
            
            # certificate: certificatemanager.Certificate
            # cluster: ecs.Cluster
            # container_definition: ecs.ContainerDefinition
            # container_image: ecs.ContainerImage
            # hosted_zone: route53.HostedZone
            # log_driver: ecs.LogDriver
            # namespace: servicediscovery.INamespace
            # role: iam.Role
            # secret: ecs.Secret
            # vpc: ec2.Vpc
            
            application_multiple_target_groups_service_base_props = ecs_patterns.ApplicationMultipleTargetGroupsServiceBaseProps(
                cloud_map_options=ecs.CloudMapOptions(
                    cloud_map_namespace=namespace,
                    container=container_definition,
                    container_port=123,
                    dns_record_type=servicediscovery.DnsRecordType.A,
                    dns_ttl=cdk.Duration.minutes(30),
                    failure_threshold=123,
                    name="name"
                ),
                cluster=cluster,
                desired_count=123,
                enable_eCSManaged_tags=False,
                health_check_grace_period=cdk.Duration.minutes(30),
                load_balancers=[ecs_patterns.ApplicationLoadBalancerProps(
                    listeners=[ecs_patterns.ApplicationListenerProps(
                        name="name",
            
                        # the properties below are optional
                        certificate=certificate,
                        port=123,
                        protocol=elbv2.ApplicationProtocol.HTTP,
                        ssl_policy=elbv2.SslPolicy.RECOMMENDED
                    )],
                    name="name",
            
                    # the properties below are optional
                    domain_name="domainName",
                    domain_zone=hosted_zone,
                    public_load_balancer=False
                )],
                propagate_tags=ecs.PropagatedTagSource.SERVICE,
                service_name="serviceName",
                target_groups=[ecs_patterns.ApplicationTargetProps(
                    container_port=123,
            
                    # the properties below are optional
                    host_header="hostHeader",
                    listener="listener",
                    path_pattern="pathPattern",
                    priority=123,
                    protocol=ecs.Protocol.TCP
                )],
                task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageProps(
                    image=container_image,
            
                    # the properties below are optional
                    container_name="containerName",
                    container_ports=[123],
                    docker_labels={
                        "docker_labels_key": "dockerLabels"
                    },
                    enable_logging=False,
                    environment={
                        "environment_key": "environment"
                    },
                    execution_role=role,
                    family="family",
                    log_driver=log_driver,
                    secrets={
                        "secrets_key": secret
                    },
                    task_role=role
                ),
                vpc=vpc
            )
        '''
        if isinstance(cloud_map_options, dict):
            cloud_map_options = _aws_cdk_aws_ecs_7896c08f.CloudMapOptions(**cloud_map_options)
        if isinstance(task_image_options, dict):
            task_image_options = ApplicationLoadBalancedTaskImageProps(**task_image_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb4d23ed1fd2070304a42718750e8b30644cf0924d289e64003849f0a1d51cb)
            check_type(argname="argument cloud_map_options", value=cloud_map_options, expected_type=type_hints["cloud_map_options"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument desired_count", value=desired_count, expected_type=type_hints["desired_count"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument health_check_grace_period", value=health_check_grace_period, expected_type=type_hints["health_check_grace_period"])
            check_type(argname="argument load_balancers", value=load_balancers, expected_type=type_hints["load_balancers"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument target_groups", value=target_groups, expected_type=type_hints["target_groups"])
            check_type(argname="argument task_image_options", value=task_image_options, expected_type=type_hints["task_image_options"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_map_options is not None:
            self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None:
            self._values["cluster"] = cluster
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None:
            self._values["health_check_grace_period"] = health_check_grace_period
        if load_balancers is not None:
            self._values["load_balancers"] = load_balancers
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if service_name is not None:
            self._values["service_name"] = service_name
        if target_groups is not None:
            self._values["target_groups"] = target_groups
        if task_image_options is not None:
            self._values["task_image_options"] = task_image_options
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def cloud_map_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions]:
        '''The options for configuring an Amazon ECS service to use service discovery.

        :default: - AWS Cloud Map service discovery is not enabled.
        '''
        result = self._values.get("cloud_map_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions], result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster]:
        '''The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster], result)

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        :default:

        - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1;
        if true, the default is 1 for all new services and uses the existing services desired count
        when updating an existing service.
        '''
        result = self._values.get("desired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        :default: false
        '''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def health_check_grace_period(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        '''
        result = self._values.get("health_check_grace_period")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def load_balancers(
        self,
    ) -> typing.Optional[typing.List[ApplicationLoadBalancerProps]]:
        '''The application load balancer that will serve traffic to the service.

        :default: - a new load balancer with a listener will be created.
        '''
        result = self._values.get("load_balancers")
        return typing.cast(typing.Optional[typing.List[ApplicationLoadBalancerProps]], result)

    @builtins.property
    def propagate_tags(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource]:
        '''Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        :default: - none
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        :default: - CloudFormation-generated name.
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["ApplicationTargetProps"]]:
        '''Properties to specify ALB target groups.

        :default: - default portMapping registered as target group and attached to the first defined listener
        '''
        result = self._values.get("target_groups")
        return typing.cast(typing.Optional[typing.List["ApplicationTargetProps"]], result)

    @builtins.property
    def task_image_options(
        self,
    ) -> typing.Optional[ApplicationLoadBalancedTaskImageProps]:
        '''The properties required to create a new task definition.

        Only one of TaskDefinition or TaskImageOptions must be specified.

        :default: none
        '''
        result = self._values.get("task_image_options")
        return typing.cast(typing.Optional[ApplicationLoadBalancedTaskImageProps], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        :default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationMultipleTargetGroupsServiceBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationTargetProps",
    jsii_struct_bases=[],
    name_mapping={
        "container_port": "containerPort",
        "host_header": "hostHeader",
        "listener": "listener",
        "path_pattern": "pathPattern",
        "priority": "priority",
        "protocol": "protocol",
    },
)
class ApplicationTargetProps:
    def __init__(
        self,
        *,
        container_port: jsii.Number,
        host_header: typing.Optional[builtins.str] = None,
        listener: typing.Optional[builtins.str] = None,
        path_pattern: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Protocol] = None,
    ) -> None:
        '''Properties to define an application target group.

        :param container_port: The port number of the container. Only applicable when using application/network load balancers.
        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param listener: Name of the listener the target group attached to. Default: - default listener (first added listener)
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param protocol: The protocol used for the port mapping. Only applicable when using application load balancers. Default: ecs.Protocol.TCP

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ecs as ecs
            import aws_cdk.aws_ecs_patterns as ecs_patterns
            
            application_target_props = ecs_patterns.ApplicationTargetProps(
                container_port=123,
            
                # the properties below are optional
                host_header="hostHeader",
                listener="listener",
                path_pattern="pathPattern",
                priority=123,
                protocol=ecs.Protocol.TCP
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12abe5f06f1b17c2b185768d66177f4ad029397881b5989ea2bbfd57aac41460)
            check_type(argname="argument container_port", value=container_port, expected_type=type_hints["container_port"])
            check_type(argname="argument host_header", value=host_header, expected_type=type_hints["host_header"])
            check_type(argname="argument listener", value=listener, expected_type=type_hints["listener"])
            check_type(argname="argument path_pattern", value=path_pattern, expected_type=type_hints["path_pattern"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_port": container_port,
        }
        if host_header is not None:
            self._values["host_header"] = host_header
        if listener is not None:
            self._values["listener"] = listener
        if path_pattern is not None:
            self._values["path_pattern"] = path_pattern
        if priority is not None:
            self._values["priority"] = priority
        if protocol is not None:
            self._values["protocol"] = protocol

    @builtins.property
    def container_port(self) -> jsii.Number:
        '''The port number of the container.

        Only applicable when using application/network load balancers.
        '''
        result = self._values.get("container_port")
        assert result is not None, "Required property 'container_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def host_header(self) -> typing.Optional[builtins.str]:
        '''Rule applies if the requested host matches the indicated host.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: No host condition

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
        '''
        result = self._values.get("host_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def listener(self) -> typing.Optional[builtins.str]:
        '''Name of the listener the target group attached to.

        :default: - default listener (first added listener)
        '''
        result = self._values.get("listener")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path_pattern(self) -> typing.Optional[builtins.str]:
        '''Rule applies if the requested path matches the given path pattern.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        :default: No path condition

        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        '''
        result = self._values.get("path_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Priority of this target group.

        The rule with the lowest priority will be used for every request.
        If priority is not given, these target groups will be added as
        defaults, and must not have conditions.

        Priorities must be unique.

        :default: Target groups are used as defaults
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.Protocol]:
        '''The protocol used for the port mapping.

        Only applicable when using application load balancers.

        :default: ecs.Protocol.TCP
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.Protocol], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationTargetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.NetworkListenerProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "port": "port"},
)
class NetworkListenerProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties to define an network listener.

        :param name: Name of the listener.
        :param port: The port on which the listener listens for requests. Default: 80

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ecs_patterns as ecs_patterns
            
            network_listener_props = ecs_patterns.NetworkListenerProps(
                name="name",
            
                # the properties below are optional
                port=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ecbd39f4149547628d94220753cb27eb7a24dfdd5fb4d2991028de1b71af154)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the listener.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port on which the listener listens for requests.

        :default: 80
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkLoadBalancedServiceBase(
    _aws_cdk_core_f4b25747.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancedServiceBase",
):
    '''The base class for NetworkLoadBalancedEc2Service and NetworkLoadBalancedFargateService services.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        domain_name: typing.Optional[builtins.str] = None,
        domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancer] = None,
        max_healthy_percent: typing.Optional[jsii.Number] = None,
        min_healthy_percent: typing.Optional[jsii.Number] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        public_load_balancer: typing.Optional[builtins.bool] = None,
        record_type: typing.Optional["NetworkLoadBalancedServiceRecordType"] = None,
        service_name: typing.Optional[builtins.str] = None,
        task_image_options: typing.Optional[typing.Union["NetworkLoadBalancedTaskImageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''Constructs a new instance of the NetworkLoadBalancedServiceBase class.

        :param scope: -
        :param id: -
        :param circuit_breaker: Whether to enable the deployment circuit breaker. If this property is defined, circuit breaker will be implicitly enabled. Default: - disabled
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the network load balancer that will serve traffic to the service. Default: 80
        :param load_balancer: The network load balancer that will serve traffic to the service. If the load balancer has been imported, the vpc attribute must be specified in the call to fromNetworkLoadBalancerAttributes(). [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param record_type: Specifies whether the Route53 record should be a CNAME, an A record using the Alias feature or no record at all. This is useful if you need to work with DNS systems that do not support alias records. Default: NetworkLoadBalancedServiceRecordType.ALIAS
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. One of taskImageOptions or taskDefinition must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c864defb4563f36027e80f4be19c87cda5ece2096391fd8c1e272e554b50df)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NetworkLoadBalancedServiceBaseProps(
            circuit_breaker=circuit_breaker,
            cloud_map_options=cloud_map_options,
            cluster=cluster,
            deployment_controller=deployment_controller,
            desired_count=desired_count,
            domain_name=domain_name,
            domain_zone=domain_zone,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            health_check_grace_period=health_check_grace_period,
            listener_port=listener_port,
            load_balancer=load_balancer,
            max_healthy_percent=max_healthy_percent,
            min_healthy_percent=min_healthy_percent,
            propagate_tags=propagate_tags,
            public_load_balancer=public_load_balancer,
            record_type=record_type,
            service_name=service_name,
            task_image_options=task_image_options,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addServiceAsTarget")
    def _add_service_as_target(
        self,
        service: _aws_cdk_aws_ecs_7896c08f.BaseService,
    ) -> None:
        '''Adds service as a target of the target group.

        :param service: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9aa9c0eea11a09b13fe29b8a0b72b4716f7df35dd70ca38bc07b2f2b744e95b)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        return typing.cast(None, jsii.invoke(self, "addServiceAsTarget", [service]))

    @jsii.member(jsii_name="createAWSLogDriver")
    def _create_aws_log_driver(
        self,
        prefix: builtins.str,
    ) -> _aws_cdk_aws_ecs_7896c08f.AwsLogDriver:
        '''
        :param prefix: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb2a6e0b70236d9b28dc333cc96a8ef1a77e820bd2ed170e8a2fddd1be5b2b92)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.AwsLogDriver, jsii.invoke(self, "createAWSLogDriver", [prefix]))

    @jsii.member(jsii_name="getDefaultCluster")
    def _get_default_cluster(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> _aws_cdk_aws_ecs_7896c08f.Cluster:
        '''Returns the default cluster.

        :param scope: -
        :param vpc: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0cf0cfc4b1a2a995a5d6728bb49ea80c7a0c47976526da5bc371ecf25629302)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.Cluster, jsii.invoke(self, "getDefaultCluster", [scope, vpc]))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _aws_cdk_aws_ecs_7896c08f.ICluster:
        '''The cluster that hosts the service.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.ICluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> jsii.Number:
        '''(deprecated) The desired number of instantiations of the task definition to keep running on the service.

        :deprecated: - Use ``internalDesiredCount`` instead.

        :stability: deprecated
        '''
        return typing.cast(jsii.Number, jsii.get(self, "desiredCount"))

    @builtins.property
    @jsii.member(jsii_name="listener")
    def listener(self) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkListener:
        '''The listener for the service.'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkListener, jsii.get(self, "listener"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkLoadBalancer:
        '''The Network Load Balancer for the service.'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkLoadBalancer, jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkTargetGroup:
        '''The target group for the service.'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkTargetGroup, jsii.get(self, "targetGroup"))

    @builtins.property
    @jsii.member(jsii_name="internalDesiredCount")
    def internal_desired_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        The default is 1 for all new services and uses the existing services desired count
        when updating an existing service, if one is not provided.
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "internalDesiredCount"))


class _NetworkLoadBalancedServiceBaseProxy(NetworkLoadBalancedServiceBase):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, NetworkLoadBalancedServiceBase).__jsii_proxy_class__ = lambda : _NetworkLoadBalancedServiceBaseProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancedServiceBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "circuit_breaker": "circuitBreaker",
        "cloud_map_options": "cloudMapOptions",
        "cluster": "cluster",
        "deployment_controller": "deploymentController",
        "desired_count": "desiredCount",
        "domain_name": "domainName",
        "domain_zone": "domainZone",
        "enable_ecs_managed_tags": "enableECSManagedTags",
        "health_check_grace_period": "healthCheckGracePeriod",
        "listener_port": "listenerPort",
        "load_balancer": "loadBalancer",
        "max_healthy_percent": "maxHealthyPercent",
        "min_healthy_percent": "minHealthyPercent",
        "propagate_tags": "propagateTags",
        "public_load_balancer": "publicLoadBalancer",
        "record_type": "recordType",
        "service_name": "serviceName",
        "task_image_options": "taskImageOptions",
        "vpc": "vpc",
    },
)
class NetworkLoadBalancedServiceBaseProps:
    def __init__(
        self,
        *,
        circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        domain_name: typing.Optional[builtins.str] = None,
        domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancer] = None,
        max_healthy_percent: typing.Optional[jsii.Number] = None,
        min_healthy_percent: typing.Optional[jsii.Number] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        public_load_balancer: typing.Optional[builtins.bool] = None,
        record_type: typing.Optional["NetworkLoadBalancedServiceRecordType"] = None,
        service_name: typing.Optional[builtins.str] = None,
        task_image_options: typing.Optional[typing.Union["NetworkLoadBalancedTaskImageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''The properties for the base NetworkLoadBalancedEc2Service or NetworkLoadBalancedFargateService service.

        :param circuit_breaker: Whether to enable the deployment circuit breaker. If this property is defined, circuit breaker will be implicitly enabled. Default: - disabled
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the network load balancer that will serve traffic to the service. Default: 80
        :param load_balancer: The network load balancer that will serve traffic to the service. If the load balancer has been imported, the vpc attribute must be specified in the call to fromNetworkLoadBalancerAttributes(). [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param record_type: Specifies whether the Route53 record should be a CNAME, an A record using the Alias feature or no record at all. This is useful if you need to work with DNS systems that do not support alias records. Default: NetworkLoadBalancedServiceRecordType.ALIAS
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. One of taskImageOptions or taskDefinition must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ec2 as ec2
            import aws_cdk.aws_ecs as ecs
            import aws_cdk.aws_ecs_patterns as ecs_patterns
            import aws_cdk.aws_elasticloadbalancingv2 as elbv2
            import aws_cdk.aws_iam as iam
            import aws_cdk.aws_route53 as route53
            import aws_cdk.aws_servicediscovery as servicediscovery
            import aws_cdk.core as cdk
            
            # cluster: ecs.Cluster
            # container_definition: ecs.ContainerDefinition
            # container_image: ecs.ContainerImage
            # hosted_zone: route53.HostedZone
            # log_driver: ecs.LogDriver
            # namespace: servicediscovery.INamespace
            # network_load_balancer: elbv2.NetworkLoadBalancer
            # role: iam.Role
            # secret: ecs.Secret
            # vpc: ec2.Vpc
            
            network_load_balanced_service_base_props = ecs_patterns.NetworkLoadBalancedServiceBaseProps(
                circuit_breaker=ecs.DeploymentCircuitBreaker(
                    rollback=False
                ),
                cloud_map_options=ecs.CloudMapOptions(
                    cloud_map_namespace=namespace,
                    container=container_definition,
                    container_port=123,
                    dns_record_type=servicediscovery.DnsRecordType.A,
                    dns_ttl=cdk.Duration.minutes(30),
                    failure_threshold=123,
                    name="name"
                ),
                cluster=cluster,
                deployment_controller=ecs.DeploymentController(
                    type=ecs.DeploymentControllerType.ECS
                ),
                desired_count=123,
                domain_name="domainName",
                domain_zone=hosted_zone,
                enable_eCSManaged_tags=False,
                health_check_grace_period=cdk.Duration.minutes(30),
                listener_port=123,
                load_balancer=network_load_balancer,
                max_healthy_percent=123,
                min_healthy_percent=123,
                propagate_tags=ecs.PropagatedTagSource.SERVICE,
                public_load_balancer=False,
                record_type=ecs_patterns.NetworkLoadBalancedServiceRecordType.ALIAS,
                service_name="serviceName",
                task_image_options=ecs_patterns.NetworkLoadBalancedTaskImageOptions(
                    image=container_image,
            
                    # the properties below are optional
                    container_name="containerName",
                    container_port=123,
                    docker_labels={
                        "docker_labels_key": "dockerLabels"
                    },
                    enable_logging=False,
                    environment={
                        "environment_key": "environment"
                    },
                    execution_role=role,
                    family="family",
                    log_driver=log_driver,
                    secrets={
                        "secrets_key": secret
                    },
                    task_role=role
                ),
                vpc=vpc
            )
        '''
        if isinstance(circuit_breaker, dict):
            circuit_breaker = _aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker(**circuit_breaker)
        if isinstance(cloud_map_options, dict):
            cloud_map_options = _aws_cdk_aws_ecs_7896c08f.CloudMapOptions(**cloud_map_options)
        if isinstance(deployment_controller, dict):
            deployment_controller = _aws_cdk_aws_ecs_7896c08f.DeploymentController(**deployment_controller)
        if isinstance(task_image_options, dict):
            task_image_options = NetworkLoadBalancedTaskImageOptions(**task_image_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a4157051083ba2515900e2f450140fe30cc8c2ff9435232d1bc07c3599ba80)
            check_type(argname="argument circuit_breaker", value=circuit_breaker, expected_type=type_hints["circuit_breaker"])
            check_type(argname="argument cloud_map_options", value=cloud_map_options, expected_type=type_hints["cloud_map_options"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument deployment_controller", value=deployment_controller, expected_type=type_hints["deployment_controller"])
            check_type(argname="argument desired_count", value=desired_count, expected_type=type_hints["desired_count"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_zone", value=domain_zone, expected_type=type_hints["domain_zone"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument health_check_grace_period", value=health_check_grace_period, expected_type=type_hints["health_check_grace_period"])
            check_type(argname="argument listener_port", value=listener_port, expected_type=type_hints["listener_port"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument max_healthy_percent", value=max_healthy_percent, expected_type=type_hints["max_healthy_percent"])
            check_type(argname="argument min_healthy_percent", value=min_healthy_percent, expected_type=type_hints["min_healthy_percent"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument public_load_balancer", value=public_load_balancer, expected_type=type_hints["public_load_balancer"])
            check_type(argname="argument record_type", value=record_type, expected_type=type_hints["record_type"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument task_image_options", value=task_image_options, expected_type=type_hints["task_image_options"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if circuit_breaker is not None:
            self._values["circuit_breaker"] = circuit_breaker
        if cloud_map_options is not None:
            self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None:
            self._values["cluster"] = cluster
        if deployment_controller is not None:
            self._values["deployment_controller"] = deployment_controller
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if domain_zone is not None:
            self._values["domain_zone"] = domain_zone
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None:
            self._values["health_check_grace_period"] = health_check_grace_period
        if listener_port is not None:
            self._values["listener_port"] = listener_port
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if max_healthy_percent is not None:
            self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None:
            self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if public_load_balancer is not None:
            self._values["public_load_balancer"] = public_load_balancer
        if record_type is not None:
            self._values["record_type"] = record_type
        if service_name is not None:
            self._values["service_name"] = service_name
        if task_image_options is not None:
            self._values["task_image_options"] = task_image_options
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def circuit_breaker(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker]:
        '''Whether to enable the deployment circuit breaker.

        If this property is defined, circuit breaker will be implicitly
        enabled.

        :default: - disabled
        '''
        result = self._values.get("circuit_breaker")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker], result)

    @builtins.property
    def cloud_map_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions]:
        '''The options for configuring an Amazon ECS service to use service discovery.

        :default: - AWS Cloud Map service discovery is not enabled.
        '''
        result = self._values.get("cloud_map_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions], result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster]:
        '''The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster], result)

    @builtins.property
    def deployment_controller(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentController]:
        '''Specifies which deployment controller to use for the service.

        For more information, see
        `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_

        :default: - Rolling update (ECS)
        '''
        result = self._values.get("deployment_controller")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentController], result)

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        :default:

        - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1;
        if true, the default is 1 for all new services and uses the existing services desired count
        when updating an existing service.
        '''
        result = self._values.get("desired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name for the service, e.g. "api.example.com.".

        :default: - No domain name.
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_zone(self) -> typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone]:
        '''The Route53 hosted zone for the domain, e.g. "example.com.".

        :default: - No Route53 hosted domain zone.
        '''
        result = self._values.get("domain_zone")
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone], result)

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        :default: false
        '''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def health_check_grace_period(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        '''
        result = self._values.get("health_check_grace_period")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        '''Listener port of the network load balancer that will serve traffic to the service.

        :default: 80
        '''
        result = self._values.get("listener_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def load_balancer(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancer]:
        '''The network load balancer that will serve traffic to the service.

        If the load balancer has been imported, the vpc attribute must be specified
        in the call to fromNetworkLoadBalancerAttributes().

        [disable-awslint:ref-via-interface]

        :default: - a new load balancer will be created.
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancer], result)

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        :default: - 100 if daemon, otherwise 200
        '''
        result = self._values.get("max_healthy_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        :default: - 0 if daemon, otherwise 50
        '''
        result = self._values.get("min_healthy_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def propagate_tags(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource]:
        '''Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        :default: - none
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource], result)

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[builtins.bool]:
        '''Determines whether the Load Balancer will be internet-facing.

        :default: true
        '''
        result = self._values.get("public_load_balancer")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def record_type(self) -> typing.Optional["NetworkLoadBalancedServiceRecordType"]:
        '''Specifies whether the Route53 record should be a CNAME, an A record using the Alias feature or no record at all.

        This is useful if you need to work with DNS systems that do not support alias records.

        :default: NetworkLoadBalancedServiceRecordType.ALIAS
        '''
        result = self._values.get("record_type")
        return typing.cast(typing.Optional["NetworkLoadBalancedServiceRecordType"], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        :default: - CloudFormation-generated name.
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def task_image_options(
        self,
    ) -> typing.Optional["NetworkLoadBalancedTaskImageOptions"]:
        '''The properties required to create a new task definition.

        One of taskImageOptions or taskDefinition must be specified.

        :default: - none
        '''
        result = self._values.get("task_image_options")
        return typing.cast(typing.Optional["NetworkLoadBalancedTaskImageOptions"], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        :default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkLoadBalancedServiceBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancedServiceRecordType")
class NetworkLoadBalancedServiceRecordType(enum.Enum):
    '''Describes the type of DNS record the service should create.'''

    ALIAS = "ALIAS"
    '''Create Route53 A Alias record.'''
    CNAME = "CNAME"
    '''Create a CNAME record.'''
    NONE = "NONE"
    '''Do not create any DNS records.'''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancedTaskImageOptions",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "container_name": "containerName",
        "container_port": "containerPort",
        "docker_labels": "dockerLabels",
        "enable_logging": "enableLogging",
        "environment": "environment",
        "execution_role": "executionRole",
        "family": "family",
        "log_driver": "logDriver",
        "secrets": "secrets",
        "task_role": "taskRole",
    },
)
class NetworkLoadBalancedTaskImageOptions:
    def __init__(
        self,
        *,
        image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
        container_name: typing.Optional[builtins.str] = None,
        container_port: typing.Optional[jsii.Number] = None,
        docker_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        execution_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        family: typing.Optional[builtins.str] = None,
        log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
        task_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''
        :param image: The image used to start a container. Image or taskDefinition must be specified, but not both. Default: - none
        :param container_name: The container name value to be specified in the task definition. Default: - none
        :param container_port: The port number on the container that is bound to the user-specified or automatically assigned host port. If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort. If you are using containers in a task with the bridge network mode and you specify a container port and not a host port, your container automatically receives a host port in the ephemeral port range. Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance. For more information, see `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_. Default: 80
        :param docker_labels: A key/value map of labels to add to the container. Default: - No labels.
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param execution_role: The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf. Default: - No value
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param task_role: The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.

        :exampleMetadata: infused

        Example::

            # cluster: ecs.Cluster
            
            load_balanced_ecs_service = ecs_patterns.NetworkLoadBalancedEc2Service(self, "Service",
                cluster=cluster,
                memory_limit_mi_b=1024,
                task_image_options=ecsPatterns.NetworkLoadBalancedTaskImageOptions(
                    image=ecs.ContainerImage.from_registry("test"),
                    environment={
                        "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
                        "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
                    }
                ),
                desired_count=2
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0374062df719f8c3e0e73480f72e5f4757cc946b5b04024835c9f8b671371c7c)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument container_port", value=container_port, expected_type=type_hints["container_port"])
            check_type(argname="argument docker_labels", value=docker_labels, expected_type=type_hints["docker_labels"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
            check_type(argname="argument log_driver", value=log_driver, expected_type=type_hints["log_driver"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument task_role", value=task_role, expected_type=type_hints["task_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if container_name is not None:
            self._values["container_name"] = container_name
        if container_port is not None:
            self._values["container_port"] = container_port
        if docker_labels is not None:
            self._values["docker_labels"] = docker_labels
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if environment is not None:
            self._values["environment"] = environment
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if family is not None:
            self._values["family"] = family
        if log_driver is not None:
            self._values["log_driver"] = log_driver
        if secrets is not None:
            self._values["secrets"] = secrets
        if task_role is not None:
            self._values["task_role"] = task_role

    @builtins.property
    def image(self) -> _aws_cdk_aws_ecs_7896c08f.ContainerImage:
        '''The image used to start a container.

        Image or taskDefinition must be specified, but not both.

        :default: - none
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.ContainerImage, result)

    @builtins.property
    def container_name(self) -> typing.Optional[builtins.str]:
        '''The container name value to be specified in the task definition.

        :default: - none
        '''
        result = self._values.get("container_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_port(self) -> typing.Optional[jsii.Number]:
        '''The port number on the container that is bound to the user-specified or automatically assigned host port.

        If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort.
        If you are using containers in a task with the bridge network mode and you specify a container port and not a host port,
        your container automatically receives a host port in the ephemeral port range.

        Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance.

        For more information, see
        `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_.

        :default: 80
        '''
        result = self._values.get("container_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def docker_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A key/value map of labels to add to the container.

        :default: - No labels.
        '''
        result = self._values.get("docker_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''Flag to indicate whether to enable logging.

        :default: true
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The environment variables to pass to the container.

        :default: - No environment variables.
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf.

        :default: - No value
        '''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    @builtins.property
    def family(self) -> typing.Optional[builtins.str]:
        '''The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        :default: - Automatically generated name.
        '''
        result = self._values.get("family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_driver(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver]:
        '''The log driver to use.

        :default: - AwsLogDriver if enableLogging is true
        '''
        result = self._values.get("log_driver")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]]:
        '''The secret to expose to the container as an environment variable.

        :default: - No secret environment variables.
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]], result)

    @builtins.property
    def task_role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        :default: - A task role is automatically created for you.
        '''
        result = self._values.get("task_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkLoadBalancedTaskImageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancedTaskImageProps",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "container_name": "containerName",
        "container_ports": "containerPorts",
        "docker_labels": "dockerLabels",
        "enable_logging": "enableLogging",
        "environment": "environment",
        "execution_role": "executionRole",
        "family": "family",
        "log_driver": "logDriver",
        "secrets": "secrets",
        "task_role": "taskRole",
    },
)
class NetworkLoadBalancedTaskImageProps:
    def __init__(
        self,
        *,
        image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
        container_name: typing.Optional[builtins.str] = None,
        container_ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
        docker_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        execution_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        family: typing.Optional[builtins.str] = None,
        log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
        task_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''Options for configuring a new container.

        :param image: The image used to start a container. Image or taskDefinition must be specified, but not both. Default: - none
        :param container_name: The container name value to be specified in the task definition. Default: - none
        :param container_ports: A list of port numbers on the container that is bound to the user-specified or automatically assigned host port. If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort. If you are using containers in a task with the bridge network mode and you specify a container port and not a host port, your container automatically receives a host port in the ephemeral port range. Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance. For more information, see `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_. Default: - [80]
        :param docker_labels: A key/value map of labels to add to the container. Default: - No labels.
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param execution_role: The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf. Default: - No value
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secrets to expose to the container as an environment variable. Default: - No secret environment variables.
        :param task_role: The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.

        :exampleMetadata: infused

        Example::

            # Two network load balancers, each with their own listener and target group.
            # cluster: ecs.Cluster
            
            load_balanced_ec2_service = ecs_patterns.NetworkMultipleTargetGroupsEc2Service(self, "Service",
                cluster=cluster,
                memory_limit_mi_b=256,
                task_image_options=ecsPatterns.NetworkLoadBalancedTaskImageProps(
                    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
                ),
                load_balancers=[ecsPatterns.NetworkLoadBalancerProps(
                    name="lb1",
                    listeners=[ecsPatterns.NetworkListenerProps(
                        name="listener1"
                    )
                    ]
                ), ecsPatterns.NetworkLoadBalancerProps(
                    name="lb2",
                    listeners=[ecsPatterns.NetworkListenerProps(
                        name="listener2"
                    )
                    ]
                )
                ],
                target_groups=[ecsPatterns.NetworkTargetProps(
                    container_port=80,
                    listener="listener1"
                ), ecsPatterns.NetworkTargetProps(
                    container_port=90,
                    listener="listener2"
                )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbcb7341cb40b22a087e9fdea3534d29f47d524f1b1e01b761614eb6f694a0d4)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument container_ports", value=container_ports, expected_type=type_hints["container_ports"])
            check_type(argname="argument docker_labels", value=docker_labels, expected_type=type_hints["docker_labels"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
            check_type(argname="argument log_driver", value=log_driver, expected_type=type_hints["log_driver"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument task_role", value=task_role, expected_type=type_hints["task_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if container_name is not None:
            self._values["container_name"] = container_name
        if container_ports is not None:
            self._values["container_ports"] = container_ports
        if docker_labels is not None:
            self._values["docker_labels"] = docker_labels
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if environment is not None:
            self._values["environment"] = environment
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if family is not None:
            self._values["family"] = family
        if log_driver is not None:
            self._values["log_driver"] = log_driver
        if secrets is not None:
            self._values["secrets"] = secrets
        if task_role is not None:
            self._values["task_role"] = task_role

    @builtins.property
    def image(self) -> _aws_cdk_aws_ecs_7896c08f.ContainerImage:
        '''The image used to start a container.

        Image or taskDefinition must be specified, but not both.

        :default: - none
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.ContainerImage, result)

    @builtins.property
    def container_name(self) -> typing.Optional[builtins.str]:
        '''The container name value to be specified in the task definition.

        :default: - none
        '''
        result = self._values.get("container_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''A list of port numbers on the container that is bound to the user-specified or automatically assigned host port.

        If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort.
        If you are using containers in a task with the bridge network mode and you specify a container port and not a host port,
        your container automatically receives a host port in the ephemeral port range.

        Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance.

        For more information, see
        `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_.

        :default: - [80]
        '''
        result = self._values.get("container_ports")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def docker_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A key/value map of labels to add to the container.

        :default: - No labels.
        '''
        result = self._values.get("docker_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''Flag to indicate whether to enable logging.

        :default: true
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The environment variables to pass to the container.

        :default: - No environment variables.
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf.

        :default: - No value
        '''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    @builtins.property
    def family(self) -> typing.Optional[builtins.str]:
        '''The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        :default: - Automatically generated name.
        '''
        result = self._values.get("family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_driver(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver]:
        '''The log driver to use.

        :default: - AwsLogDriver if enableLogging is true
        '''
        result = self._values.get("log_driver")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]]:
        '''The secrets to expose to the container as an environment variable.

        :default: - No secret environment variables.
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]], result)

    @builtins.property
    def task_role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        :default: - A task role is automatically created for you.
        '''
        result = self._values.get("task_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkLoadBalancedTaskImageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancerProps",
    jsii_struct_bases=[],
    name_mapping={
        "listeners": "listeners",
        "name": "name",
        "domain_name": "domainName",
        "domain_zone": "domainZone",
        "public_load_balancer": "publicLoadBalancer",
    },
)
class NetworkLoadBalancerProps:
    def __init__(
        self,
        *,
        listeners: typing.Sequence[typing.Union[NetworkListenerProps, typing.Dict[builtins.str, typing.Any]]],
        name: builtins.str,
        domain_name: typing.Optional[builtins.str] = None,
        domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
        public_load_balancer: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Properties to define an network load balancer.

        :param listeners: Listeners (at least one listener) attached to this load balancer. Default: - none
        :param name: Name of the load balancer.
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ecs_patterns as ecs_patterns
            import aws_cdk.aws_route53 as route53
            
            # hosted_zone: route53.HostedZone
            
            network_load_balancer_props = ecs_patterns.NetworkLoadBalancerProps(
                listeners=[ecs_patterns.NetworkListenerProps(
                    name="name",
            
                    # the properties below are optional
                    port=123
                )],
                name="name",
            
                # the properties below are optional
                domain_name="domainName",
                domain_zone=hosted_zone,
                public_load_balancer=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7919b2d9b5e0aebd2d208b368636438029ddfedcfa692a4c68f7033ed6fcc988)
            check_type(argname="argument listeners", value=listeners, expected_type=type_hints["listeners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_zone", value=domain_zone, expected_type=type_hints["domain_zone"])
            check_type(argname="argument public_load_balancer", value=public_load_balancer, expected_type=type_hints["public_load_balancer"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "listeners": listeners,
            "name": name,
        }
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if domain_zone is not None:
            self._values["domain_zone"] = domain_zone
        if public_load_balancer is not None:
            self._values["public_load_balancer"] = public_load_balancer

    @builtins.property
    def listeners(self) -> typing.List[NetworkListenerProps]:
        '''Listeners (at least one listener) attached to this load balancer.

        :default: - none
        '''
        result = self._values.get("listeners")
        assert result is not None, "Required property 'listeners' is missing"
        return typing.cast(typing.List[NetworkListenerProps], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the load balancer.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name for the service, e.g. "api.example.com.".

        :default: - No domain name.
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_zone(self) -> typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone]:
        '''The Route53 hosted zone for the domain, e.g. "example.com.".

        :default: - No Route53 hosted domain zone.
        '''
        result = self._values.get("domain_zone")
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone], result)

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[builtins.bool]:
        '''Determines whether the Load Balancer will be internet-facing.

        :default: true
        '''
        result = self._values.get("public_load_balancer")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkLoadBalancerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkMultipleTargetGroupsServiceBase(
    _aws_cdk_core_f4b25747.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-ecs-patterns.NetworkMultipleTargetGroupsServiceBase",
):
    '''The base class for NetworkMultipleTargetGroupsEc2Service and NetworkMultipleTargetGroupsFargateService classes.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        load_balancers: typing.Optional[typing.Sequence[typing.Union[NetworkLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        service_name: typing.Optional[builtins.str] = None,
        target_groups: typing.Optional[typing.Sequence[typing.Union["NetworkTargetProps", typing.Dict[builtins.str, typing.Any]]]] = None,
        task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''Constructs a new instance of the NetworkMultipleTargetGroupsServiceBase class.

        :param scope: -
        :param id: -
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The network load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: Name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify NLB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d206b7315599e3d8a578a68ce6cb797f4d346078d3550c92571ea6783168369)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NetworkMultipleTargetGroupsServiceBaseProps(
            cloud_map_options=cloud_map_options,
            cluster=cluster,
            desired_count=desired_count,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            health_check_grace_period=health_check_grace_period,
            load_balancers=load_balancers,
            propagate_tags=propagate_tags,
            service_name=service_name,
            target_groups=target_groups,
            task_image_options=task_image_options,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addPortMappingForTargets")
    def _add_port_mapping_for_targets(
        self,
        container: _aws_cdk_aws_ecs_7896c08f.ContainerDefinition,
        targets: typing.Sequence[typing.Union["NetworkTargetProps", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param container: -
        :param targets: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcb75bfbf1d1997d674de06caa71f633bbc1ee84514d983557db84518314266e)
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        return typing.cast(None, jsii.invoke(self, "addPortMappingForTargets", [container, targets]))

    @jsii.member(jsii_name="createAWSLogDriver")
    def _create_aws_log_driver(
        self,
        prefix: builtins.str,
    ) -> _aws_cdk_aws_ecs_7896c08f.AwsLogDriver:
        '''
        :param prefix: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125c757436a02e6588c8e16dfa29770a89bcb44e2e76ac9c96925e1f866577f8)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.AwsLogDriver, jsii.invoke(self, "createAWSLogDriver", [prefix]))

    @jsii.member(jsii_name="findListener")
    def _find_listener(
        self,
        name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkListener:
        '''
        :param name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4e737cd82b0b818a2a41eee2ca7098026dbacf121c10ef98fd453e9fcb743f7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkListener, jsii.invoke(self, "findListener", [name]))

    @jsii.member(jsii_name="getDefaultCluster")
    def _get_default_cluster(
        self,
        scope: _constructs_77d1e7e8.Construct,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> _aws_cdk_aws_ecs_7896c08f.Cluster:
        '''Returns the default cluster.

        :param scope: -
        :param vpc: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1572e84655425eb85cd862e552e8f7731bd2ad77e15e0064d77df3a437820483)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.Cluster, jsii.invoke(self, "getDefaultCluster", [scope, vpc]))

    @jsii.member(jsii_name="registerECSTargets")
    def _register_ecs_targets(
        self,
        service: _aws_cdk_aws_ecs_7896c08f.BaseService,
        container: _aws_cdk_aws_ecs_7896c08f.ContainerDefinition,
        targets: typing.Sequence[typing.Union["NetworkTargetProps", typing.Dict[builtins.str, typing.Any]]],
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkTargetGroup:
        '''
        :param service: -
        :param container: -
        :param targets: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99add5c434d77b4d4e4658b80c1eeb9146226e78b2dae1cfe95b4cc42f6b9004)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkTargetGroup, jsii.invoke(self, "registerECSTargets", [service, container, targets]))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _aws_cdk_aws_ecs_7896c08f.ICluster:
        '''The cluster that hosts the service.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.ICluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> jsii.Number:
        '''(deprecated) The desired number of instantiations of the task definition to keep running on the service.

        :deprecated: - Use ``internalDesiredCount`` instead.

        :stability: deprecated
        '''
        return typing.cast(jsii.Number, jsii.get(self, "desiredCount"))

    @builtins.property
    @jsii.member(jsii_name="listener")
    def listener(self) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkListener:
        '''The listener for the service.'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkListener, jsii.get(self, "listener"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkLoadBalancer:
        '''The Network Load Balancer for the service.'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkLoadBalancer, jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="internalDesiredCount")
    def internal_desired_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        The default is 1 for all new services and uses the existing services desired count
        when updating an existing service, if one is not provided.
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "internalDesiredCount"))

    @builtins.property
    @jsii.member(jsii_name="listeners")
    def _listeners(
        self,
    ) -> typing.List[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkListener]:
        return typing.cast(typing.List[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkListener], jsii.get(self, "listeners"))

    @_listeners.setter
    def _listeners(
        self,
        value: typing.List[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkListener],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07ca8bfb0679467f7d12a551e67b8b65cccd73c0807c3befd0494d263a0375e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listeners", value)

    @builtins.property
    @jsii.member(jsii_name="targetGroups")
    def _target_groups(
        self,
    ) -> typing.List[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkTargetGroup]:
        return typing.cast(typing.List[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkTargetGroup], jsii.get(self, "targetGroups"))

    @_target_groups.setter
    def _target_groups(
        self,
        value: typing.List[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkTargetGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d6d2afa98cdba3cd3e2148fc9f1ac440bbd4fd52fb30bc71f7f4269d2976226)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetGroups", value)

    @builtins.property
    @jsii.member(jsii_name="logDriver")
    def _log_driver(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver]:
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver], jsii.get(self, "logDriver"))

    @_log_driver.setter
    def _log_driver(
        self,
        value: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d05dd501f24dc65a80429b327cb50464fdefedaea6a6ba3ab2589bed733524e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logDriver", value)


class _NetworkMultipleTargetGroupsServiceBaseProxy(
    NetworkMultipleTargetGroupsServiceBase,
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, NetworkMultipleTargetGroupsServiceBase).__jsii_proxy_class__ = lambda : _NetworkMultipleTargetGroupsServiceBaseProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.NetworkMultipleTargetGroupsServiceBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_map_options": "cloudMapOptions",
        "cluster": "cluster",
        "desired_count": "desiredCount",
        "enable_ecs_managed_tags": "enableECSManagedTags",
        "health_check_grace_period": "healthCheckGracePeriod",
        "load_balancers": "loadBalancers",
        "propagate_tags": "propagateTags",
        "service_name": "serviceName",
        "target_groups": "targetGroups",
        "task_image_options": "taskImageOptions",
        "vpc": "vpc",
    },
)
class NetworkMultipleTargetGroupsServiceBaseProps:
    def __init__(
        self,
        *,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        load_balancers: typing.Optional[typing.Sequence[typing.Union[NetworkLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        service_name: typing.Optional[builtins.str] = None,
        target_groups: typing.Optional[typing.Sequence[typing.Union["NetworkTargetProps", typing.Dict[builtins.str, typing.Any]]]] = None,
        task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''The properties for the base NetworkMultipleTargetGroupsEc2Service or NetworkMultipleTargetGroupsFargateService service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The network load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: Name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify NLB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ec2 as ec2
            import aws_cdk.aws_ecs as ecs
            import aws_cdk.aws_ecs_patterns as ecs_patterns
            import aws_cdk.aws_iam as iam
            import aws_cdk.aws_route53 as route53
            import aws_cdk.aws_servicediscovery as servicediscovery
            import aws_cdk.core as cdk
            
            # cluster: ecs.Cluster
            # container_definition: ecs.ContainerDefinition
            # container_image: ecs.ContainerImage
            # hosted_zone: route53.HostedZone
            # log_driver: ecs.LogDriver
            # namespace: servicediscovery.INamespace
            # role: iam.Role
            # secret: ecs.Secret
            # vpc: ec2.Vpc
            
            network_multiple_target_groups_service_base_props = ecs_patterns.NetworkMultipleTargetGroupsServiceBaseProps(
                cloud_map_options=ecs.CloudMapOptions(
                    cloud_map_namespace=namespace,
                    container=container_definition,
                    container_port=123,
                    dns_record_type=servicediscovery.DnsRecordType.A,
                    dns_ttl=cdk.Duration.minutes(30),
                    failure_threshold=123,
                    name="name"
                ),
                cluster=cluster,
                desired_count=123,
                enable_eCSManaged_tags=False,
                health_check_grace_period=cdk.Duration.minutes(30),
                load_balancers=[ecs_patterns.NetworkLoadBalancerProps(
                    listeners=[ecs_patterns.NetworkListenerProps(
                        name="name",
            
                        # the properties below are optional
                        port=123
                    )],
                    name="name",
            
                    # the properties below are optional
                    domain_name="domainName",
                    domain_zone=hosted_zone,
                    public_load_balancer=False
                )],
                propagate_tags=ecs.PropagatedTagSource.SERVICE,
                service_name="serviceName",
                target_groups=[ecs_patterns.NetworkTargetProps(
                    container_port=123,
            
                    # the properties below are optional
                    listener="listener"
                )],
                task_image_options=ecs_patterns.NetworkLoadBalancedTaskImageProps(
                    image=container_image,
            
                    # the properties below are optional
                    container_name="containerName",
                    container_ports=[123],
                    docker_labels={
                        "docker_labels_key": "dockerLabels"
                    },
                    enable_logging=False,
                    environment={
                        "environment_key": "environment"
                    },
                    execution_role=role,
                    family="family",
                    log_driver=log_driver,
                    secrets={
                        "secrets_key": secret
                    },
                    task_role=role
                ),
                vpc=vpc
            )
        '''
        if isinstance(cloud_map_options, dict):
            cloud_map_options = _aws_cdk_aws_ecs_7896c08f.CloudMapOptions(**cloud_map_options)
        if isinstance(task_image_options, dict):
            task_image_options = NetworkLoadBalancedTaskImageProps(**task_image_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52c25650d1aeba8f094edeb0b7cb5e8cc102f662f61d3f9d169883bb74c174f2)
            check_type(argname="argument cloud_map_options", value=cloud_map_options, expected_type=type_hints["cloud_map_options"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument desired_count", value=desired_count, expected_type=type_hints["desired_count"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument health_check_grace_period", value=health_check_grace_period, expected_type=type_hints["health_check_grace_period"])
            check_type(argname="argument load_balancers", value=load_balancers, expected_type=type_hints["load_balancers"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument target_groups", value=target_groups, expected_type=type_hints["target_groups"])
            check_type(argname="argument task_image_options", value=task_image_options, expected_type=type_hints["task_image_options"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_map_options is not None:
            self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None:
            self._values["cluster"] = cluster
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None:
            self._values["health_check_grace_period"] = health_check_grace_period
        if load_balancers is not None:
            self._values["load_balancers"] = load_balancers
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if service_name is not None:
            self._values["service_name"] = service_name
        if target_groups is not None:
            self._values["target_groups"] = target_groups
        if task_image_options is not None:
            self._values["task_image_options"] = task_image_options
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def cloud_map_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions]:
        '''The options for configuring an Amazon ECS service to use service discovery.

        :default: - AWS Cloud Map service discovery is not enabled.
        '''
        result = self._values.get("cloud_map_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions], result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster]:
        '''The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster], result)

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        :default:

        - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1;
        if true, the default is 1 for all new services and uses the existing services desired count
        when updating an existing service.
        '''
        result = self._values.get("desired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        :default: false
        '''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def health_check_grace_period(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        '''
        result = self._values.get("health_check_grace_period")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def load_balancers(self) -> typing.Optional[typing.List[NetworkLoadBalancerProps]]:
        '''The network load balancer that will serve traffic to the service.

        :default: - a new load balancer with a listener will be created.
        '''
        result = self._values.get("load_balancers")
        return typing.cast(typing.Optional[typing.List[NetworkLoadBalancerProps]], result)

    @builtins.property
    def propagate_tags(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource]:
        '''Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        :default: - none
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''Name of the service.

        :default: - CloudFormation-generated name.
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["NetworkTargetProps"]]:
        '''Properties to specify NLB target groups.

        :default: - default portMapping registered as target group and attached to the first defined listener
        '''
        result = self._values.get("target_groups")
        return typing.cast(typing.Optional[typing.List["NetworkTargetProps"]], result)

    @builtins.property
    def task_image_options(self) -> typing.Optional[NetworkLoadBalancedTaskImageProps]:
        '''The properties required to create a new task definition.

        Only one of TaskDefinition or TaskImageOptions must be specified.

        :default: - none
        '''
        result = self._values.get("task_image_options")
        return typing.cast(typing.Optional[NetworkLoadBalancedTaskImageProps], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        :default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkMultipleTargetGroupsServiceBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.NetworkTargetProps",
    jsii_struct_bases=[],
    name_mapping={"container_port": "containerPort", "listener": "listener"},
)
class NetworkTargetProps:
    def __init__(
        self,
        *,
        container_port: jsii.Number,
        listener: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties to define a network load balancer target group.

        :param container_port: The port number of the container. Only applicable when using application/network load balancers.
        :param listener: Name of the listener the target group attached to. Default: - default listener (first added listener)

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ecs_patterns as ecs_patterns
            
            network_target_props = ecs_patterns.NetworkTargetProps(
                container_port=123,
            
                # the properties below are optional
                listener="listener"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a025dde5ba84036c647d7a71a65cbaa81877f51ed8f92c98d9c80342cbe9d9b0)
            check_type(argname="argument container_port", value=container_port, expected_type=type_hints["container_port"])
            check_type(argname="argument listener", value=listener, expected_type=type_hints["listener"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_port": container_port,
        }
        if listener is not None:
            self._values["listener"] = listener

    @builtins.property
    def container_port(self) -> jsii.Number:
        '''The port number of the container.

        Only applicable when using application/network load balancers.
        '''
        result = self._values.get("container_port")
        assert result is not None, "Required property 'container_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def listener(self) -> typing.Optional[builtins.str]:
        '''Name of the listener the target group attached to.

        :default: - default listener (first added listener)
        '''
        result = self._values.get("listener")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkTargetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QueueProcessingServiceBase(
    _aws_cdk_core_f4b25747.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-ecs-patterns.QueueProcessingServiceBase",
):
    '''The base class for QueueProcessingEc2Service and QueueProcessingFargateService services.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
        capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_7896c08f.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
        circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
        desired_task_count: typing.Optional[jsii.Number] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        family: typing.Optional[builtins.str] = None,
        log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
        max_healthy_percent: typing.Optional[jsii.Number] = None,
        max_receive_count: typing.Optional[jsii.Number] = None,
        max_scaling_capacity: typing.Optional[jsii.Number] = None,
        min_healthy_percent: typing.Optional[jsii.Number] = None,
        min_scaling_capacity: typing.Optional[jsii.Number] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        queue: typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue] = None,
        retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        scaling_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval, typing.Dict[builtins.str, typing.Any]]]] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
        service_name: typing.Optional[builtins.str] = None,
        visibility_timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''Constructs a new instance of the QueueProcessingServiceBase class.

        :param scope: -
        :param id: -
        :param image: The image used to start a container.
        :param capacity_provider_strategies: A list of Capacity Provider strategies used to place a service. Default: - undefined
        :param circuit_breaker: Whether to enable the deployment circuit breaker. If this property is defined, circuit breaker will be implicitly enabled. Default: - disabled
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_task_count: (deprecated) The desired number of instantiations of the task definition to keep running on the service. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the minScalingCapacity is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. The variable ``QUEUE_NAME`` with value ``queue.queueName`` will always be passed. Default: 'QUEUE_NAME: queue.queueName'
        :param family: The name of a family that the task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - default from underlying service.
        :param max_receive_count: The maximum number of times that a message can be received by consumers. When this value is exceeded for a message the message will be automatically sent to the Dead Letter Queue. Default: 3
        :param max_scaling_capacity: Maximum capacity to scale to. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is (desiredTaskCount * 2); if true, the default is 2.
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - default from underlying service.
        :param min_scaling_capacity: Minimum capacity to scale to. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is the desiredTaskCount; if true, the default is 1.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ Default: 'SQSQueue with CloudFormation-generated name'
        :param retention_period: The number of seconds that Dead Letter Queue retains a message. Default: Duration.days(14)
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. See `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_ Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param visibility_timeout: Timeout of processing a single message. After dequeuing, the processor has this much time to handle the message and delete it from the queue before it becomes visible again for dequeueing by another processor. Values must be between 0 and (12 hours). Default: Duration.seconds(30)
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99c4667215185f9aac504de66063e19233242bd897b690593b8482de022f9ee3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = QueueProcessingServiceBaseProps(
            image=image,
            capacity_provider_strategies=capacity_provider_strategies,
            circuit_breaker=circuit_breaker,
            cluster=cluster,
            command=command,
            deployment_controller=deployment_controller,
            desired_task_count=desired_task_count,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            enable_logging=enable_logging,
            environment=environment,
            family=family,
            log_driver=log_driver,
            max_healthy_percent=max_healthy_percent,
            max_receive_count=max_receive_count,
            max_scaling_capacity=max_scaling_capacity,
            min_healthy_percent=min_healthy_percent,
            min_scaling_capacity=min_scaling_capacity,
            propagate_tags=propagate_tags,
            queue=queue,
            retention_period=retention_period,
            scaling_steps=scaling_steps,
            secrets=secrets,
            service_name=service_name,
            visibility_timeout=visibility_timeout,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="configureAutoscalingForService")
    def _configure_autoscaling_for_service(
        self,
        service: _aws_cdk_aws_ecs_7896c08f.BaseService,
    ) -> None:
        '''Configure autoscaling based off of CPU utilization as well as the number of messages visible in the SQS queue.

        :param service: the ECS/Fargate service for which to apply the autoscaling rules to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0cd6787347fb77f1086bfe3a6bb7e691881b9281799ca3fbb92ec63905b2218)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        return typing.cast(None, jsii.invoke(self, "configureAutoscalingForService", [service]))

    @jsii.member(jsii_name="getDefaultCluster")
    def _get_default_cluster(
        self,
        scope: _constructs_77d1e7e8.Construct,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> _aws_cdk_aws_ecs_7896c08f.Cluster:
        '''Returns the default cluster.

        :param scope: -
        :param vpc: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ded2e8bb80b5710d47088763eb8e4db6258ddba4ced85427b6cbcf01ddaba503)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.Cluster, jsii.invoke(self, "getDefaultCluster", [scope, vpc]))

    @jsii.member(jsii_name="grantPermissionsToService")
    def _grant_permissions_to_service(
        self,
        service: _aws_cdk_aws_ecs_7896c08f.BaseService,
    ) -> None:
        '''Grant SQS permissions to an ECS service.

        :param service: the ECS/Fargate service to which to grant SQS permissions.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce63b3f7e49f8867b3ad775d86279487cf9973c7ce8f465f597874929dd683c)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        return typing.cast(None, jsii.invoke(self, "grantPermissionsToService", [service]))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _aws_cdk_aws_ecs_7896c08f.ICluster:
        '''The cluster where your service will be deployed.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.ICluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> jsii.Number:
        '''(deprecated) The minimum number of tasks to run.

        :deprecated: - Use ``minCapacity`` instead.

        :stability: deprecated
        '''
        return typing.cast(jsii.Number, jsii.get(self, "desiredCount"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Environment variables that will include the queue name.'''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="maxCapacity")
    def max_capacity(self) -> jsii.Number:
        '''The maximum number of instances for autoscaling to scale up to.'''
        return typing.cast(jsii.Number, jsii.get(self, "maxCapacity"))

    @builtins.property
    @jsii.member(jsii_name="minCapacity")
    def min_capacity(self) -> jsii.Number:
        '''The minimum number of instances for autoscaling to scale down to.'''
        return typing.cast(jsii.Number, jsii.get(self, "minCapacity"))

    @builtins.property
    @jsii.member(jsii_name="scalingSteps")
    def scaling_steps(
        self,
    ) -> typing.List[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval]:
        '''The scaling interval for autoscaling based off an SQS Queue size.'''
        return typing.cast(typing.List[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval], jsii.get(self, "scalingSteps"))

    @builtins.property
    @jsii.member(jsii_name="sqsQueue")
    def sqs_queue(self) -> _aws_cdk_aws_sqs_48bffef9.IQueue:
        '''The SQS queue that the service will process from.'''
        return typing.cast(_aws_cdk_aws_sqs_48bffef9.IQueue, jsii.get(self, "sqsQueue"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterQueue")
    def dead_letter_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue]:
        '''The dead letter queue for the primary SQS queue.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue], jsii.get(self, "deadLetterQueue"))

    @builtins.property
    @jsii.member(jsii_name="logDriver")
    def log_driver(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver]:
        '''The AwsLogDriver to use for logging if logging is enabled.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver], jsii.get(self, "logDriver"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]]:
        '''The secret environment variables.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]], jsii.get(self, "secrets"))


class _QueueProcessingServiceBaseProxy(QueueProcessingServiceBase):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, QueueProcessingServiceBase).__jsii_proxy_class__ = lambda : _QueueProcessingServiceBaseProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.QueueProcessingServiceBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "capacity_provider_strategies": "capacityProviderStrategies",
        "circuit_breaker": "circuitBreaker",
        "cluster": "cluster",
        "command": "command",
        "deployment_controller": "deploymentController",
        "desired_task_count": "desiredTaskCount",
        "enable_ecs_managed_tags": "enableECSManagedTags",
        "enable_logging": "enableLogging",
        "environment": "environment",
        "family": "family",
        "log_driver": "logDriver",
        "max_healthy_percent": "maxHealthyPercent",
        "max_receive_count": "maxReceiveCount",
        "max_scaling_capacity": "maxScalingCapacity",
        "min_healthy_percent": "minHealthyPercent",
        "min_scaling_capacity": "minScalingCapacity",
        "propagate_tags": "propagateTags",
        "queue": "queue",
        "retention_period": "retentionPeriod",
        "scaling_steps": "scalingSteps",
        "secrets": "secrets",
        "service_name": "serviceName",
        "visibility_timeout": "visibilityTimeout",
        "vpc": "vpc",
    },
)
class QueueProcessingServiceBaseProps:
    def __init__(
        self,
        *,
        image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
        capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_7896c08f.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
        circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
        desired_task_count: typing.Optional[jsii.Number] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        family: typing.Optional[builtins.str] = None,
        log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
        max_healthy_percent: typing.Optional[jsii.Number] = None,
        max_receive_count: typing.Optional[jsii.Number] = None,
        max_scaling_capacity: typing.Optional[jsii.Number] = None,
        min_healthy_percent: typing.Optional[jsii.Number] = None,
        min_scaling_capacity: typing.Optional[jsii.Number] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        queue: typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue] = None,
        retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        scaling_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval, typing.Dict[builtins.str, typing.Any]]]] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
        service_name: typing.Optional[builtins.str] = None,
        visibility_timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''The properties for the base QueueProcessingEc2Service or QueueProcessingFargateService service.

        :param image: The image used to start a container.
        :param capacity_provider_strategies: A list of Capacity Provider strategies used to place a service. Default: - undefined
        :param circuit_breaker: Whether to enable the deployment circuit breaker. If this property is defined, circuit breaker will be implicitly enabled. Default: - disabled
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_task_count: (deprecated) The desired number of instantiations of the task definition to keep running on the service. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the minScalingCapacity is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. The variable ``QUEUE_NAME`` with value ``queue.queueName`` will always be passed. Default: 'QUEUE_NAME: queue.queueName'
        :param family: The name of a family that the task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - default from underlying service.
        :param max_receive_count: The maximum number of times that a message can be received by consumers. When this value is exceeded for a message the message will be automatically sent to the Dead Letter Queue. Default: 3
        :param max_scaling_capacity: Maximum capacity to scale to. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is (desiredTaskCount * 2); if true, the default is 2.
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - default from underlying service.
        :param min_scaling_capacity: Minimum capacity to scale to. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is the desiredTaskCount; if true, the default is 1.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ Default: 'SQSQueue with CloudFormation-generated name'
        :param retention_period: The number of seconds that Dead Letter Queue retains a message. Default: Duration.days(14)
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. See `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_ Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param visibility_timeout: Timeout of processing a single message. After dequeuing, the processor has this much time to handle the message and delete it from the queue before it becomes visible again for dequeueing by another processor. Values must be between 0 and (12 hours). Default: Duration.seconds(30)
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ec2 as ec2
            import aws_cdk.aws_ecs as ecs
            import aws_cdk.aws_ecs_patterns as ecs_patterns
            import aws_cdk.aws_sqs as sqs
            import aws_cdk.core as cdk
            
            # cluster: ecs.Cluster
            # container_image: ecs.ContainerImage
            # log_driver: ecs.LogDriver
            # queue: sqs.Queue
            # secret: ecs.Secret
            # vpc: ec2.Vpc
            
            queue_processing_service_base_props = ecs_patterns.QueueProcessingServiceBaseProps(
                image=container_image,
            
                # the properties below are optional
                capacity_provider_strategies=[ecs.CapacityProviderStrategy(
                    capacity_provider="capacityProvider",
            
                    # the properties below are optional
                    base=123,
                    weight=123
                )],
                circuit_breaker=ecs.DeploymentCircuitBreaker(
                    rollback=False
                ),
                cluster=cluster,
                command=["command"],
                deployment_controller=ecs.DeploymentController(
                    type=ecs.DeploymentControllerType.ECS
                ),
                desired_task_count=123,
                enable_eCSManaged_tags=False,
                enable_logging=False,
                environment={
                    "environment_key": "environment"
                },
                family="family",
                log_driver=log_driver,
                max_healthy_percent=123,
                max_receive_count=123,
                max_scaling_capacity=123,
                min_healthy_percent=123,
                min_scaling_capacity=123,
                propagate_tags=ecs.PropagatedTagSource.SERVICE,
                queue=queue,
                retention_period=cdk.Duration.minutes(30),
                scaling_steps=[ScalingInterval(
                    change=123,
            
                    # the properties below are optional
                    lower=123,
                    upper=123
                )],
                secrets={
                    "secrets_key": secret
                },
                service_name="serviceName",
                visibility_timeout=cdk.Duration.minutes(30),
                vpc=vpc
            )
        '''
        if isinstance(circuit_breaker, dict):
            circuit_breaker = _aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker(**circuit_breaker)
        if isinstance(deployment_controller, dict):
            deployment_controller = _aws_cdk_aws_ecs_7896c08f.DeploymentController(**deployment_controller)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c682d33923fe884e4a8dbd393aeb9b3b7d5a38a2a50a934a7375f703b45cf9)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument capacity_provider_strategies", value=capacity_provider_strategies, expected_type=type_hints["capacity_provider_strategies"])
            check_type(argname="argument circuit_breaker", value=circuit_breaker, expected_type=type_hints["circuit_breaker"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument deployment_controller", value=deployment_controller, expected_type=type_hints["deployment_controller"])
            check_type(argname="argument desired_task_count", value=desired_task_count, expected_type=type_hints["desired_task_count"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
            check_type(argname="argument log_driver", value=log_driver, expected_type=type_hints["log_driver"])
            check_type(argname="argument max_healthy_percent", value=max_healthy_percent, expected_type=type_hints["max_healthy_percent"])
            check_type(argname="argument max_receive_count", value=max_receive_count, expected_type=type_hints["max_receive_count"])
            check_type(argname="argument max_scaling_capacity", value=max_scaling_capacity, expected_type=type_hints["max_scaling_capacity"])
            check_type(argname="argument min_healthy_percent", value=min_healthy_percent, expected_type=type_hints["min_healthy_percent"])
            check_type(argname="argument min_scaling_capacity", value=min_scaling_capacity, expected_type=type_hints["min_scaling_capacity"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
            check_type(argname="argument scaling_steps", value=scaling_steps, expected_type=type_hints["scaling_steps"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument visibility_timeout", value=visibility_timeout, expected_type=type_hints["visibility_timeout"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if capacity_provider_strategies is not None:
            self._values["capacity_provider_strategies"] = capacity_provider_strategies
        if circuit_breaker is not None:
            self._values["circuit_breaker"] = circuit_breaker
        if cluster is not None:
            self._values["cluster"] = cluster
        if command is not None:
            self._values["command"] = command
        if deployment_controller is not None:
            self._values["deployment_controller"] = deployment_controller
        if desired_task_count is not None:
            self._values["desired_task_count"] = desired_task_count
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if environment is not None:
            self._values["environment"] = environment
        if family is not None:
            self._values["family"] = family
        if log_driver is not None:
            self._values["log_driver"] = log_driver
        if max_healthy_percent is not None:
            self._values["max_healthy_percent"] = max_healthy_percent
        if max_receive_count is not None:
            self._values["max_receive_count"] = max_receive_count
        if max_scaling_capacity is not None:
            self._values["max_scaling_capacity"] = max_scaling_capacity
        if min_healthy_percent is not None:
            self._values["min_healthy_percent"] = min_healthy_percent
        if min_scaling_capacity is not None:
            self._values["min_scaling_capacity"] = min_scaling_capacity
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if queue is not None:
            self._values["queue"] = queue
        if retention_period is not None:
            self._values["retention_period"] = retention_period
        if scaling_steps is not None:
            self._values["scaling_steps"] = scaling_steps
        if secrets is not None:
            self._values["secrets"] = secrets
        if service_name is not None:
            self._values["service_name"] = service_name
        if visibility_timeout is not None:
            self._values["visibility_timeout"] = visibility_timeout
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def image(self) -> _aws_cdk_aws_ecs_7896c08f.ContainerImage:
        '''The image used to start a container.'''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.ContainerImage, result)

    @builtins.property
    def capacity_provider_strategies(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.CapacityProviderStrategy]]:
        '''A list of Capacity Provider strategies used to place a service.

        :default: - undefined
        '''
        result = self._values.get("capacity_provider_strategies")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.CapacityProviderStrategy]], result)

    @builtins.property
    def circuit_breaker(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker]:
        '''Whether to enable the deployment circuit breaker.

        If this property is defined, circuit breaker will be implicitly
        enabled.

        :default: - disabled
        '''
        result = self._values.get("circuit_breaker")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker], result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster]:
        '''The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        :default: - CMD value built into container image.
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deployment_controller(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentController]:
        '''Specifies which deployment controller to use for the service.

        For more information, see
        `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_

        :default: - Rolling update (ECS)
        '''
        result = self._values.get("deployment_controller")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentController], result)

    @builtins.property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) The desired number of instantiations of the task definition to keep running on the service.

        :default:

        - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1;
        if true, the minScalingCapacity is 1 for all new services and uses the existing services desired count
        when updating an existing service.

        :deprecated: - Use ``minScalingCapacity`` or a literal object instead.

        :stability: deprecated
        '''
        result = self._values.get("desired_task_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        :default: false
        '''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''Flag to indicate whether to enable logging.

        :default: true
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The environment variables to pass to the container.

        The variable ``QUEUE_NAME`` with value ``queue.queueName`` will
        always be passed.

        :default: 'QUEUE_NAME: queue.queueName'
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def family(self) -> typing.Optional[builtins.str]:
        '''The name of a family that the task definition is registered to.

        A family groups multiple versions of a task definition.

        :default: - Automatically generated name.
        '''
        result = self._values.get("family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_driver(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver]:
        '''The log driver to use.

        :default: - AwsLogDriver if enableLogging is true
        '''
        result = self._values.get("log_driver")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver], result)

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        :default: - default from underlying service.
        '''
        result = self._values.get("max_healthy_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_receive_count(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of times that a message can be received by consumers.

        When this value is exceeded for a message the message will be automatically sent to the Dead Letter Queue.

        :default: 3
        '''
        result = self._values.get("max_receive_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_scaling_capacity(self) -> typing.Optional[jsii.Number]:
        '''Maximum capacity to scale to.

        :default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is (desiredTaskCount * 2); if true, the default is 2.
        '''
        result = self._values.get("max_scaling_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        :default: - default from underlying service.
        '''
        result = self._values.get("min_healthy_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_scaling_capacity(self) -> typing.Optional[jsii.Number]:
        '''Minimum capacity to scale to.

        :default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is the desiredTaskCount; if true, the default is 1.
        '''
        result = self._values.get("min_scaling_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def propagate_tags(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource]:
        '''Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        :default: - none
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource], result)

    @builtins.property
    def queue(self) -> typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue]:
        '''A queue for which to process items from.

        If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See
        `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_

        :default: 'SQSQueue with CloudFormation-generated name'
        '''
        result = self._values.get("queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue], result)

    @builtins.property
    def retention_period(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The number of seconds that Dead Letter Queue retains a message.

        :default: Duration.days(14)
        '''
        result = self._values.get("retention_period")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def scaling_steps(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval]]:
        '''The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric.

        Maps a range of metric values to a particular scaling behavior. See
        `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_

        :default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        '''
        result = self._values.get("scaling_steps")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval]], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]]:
        '''The secret to expose to the container as an environment variable.

        :default: - No secret environment variables.
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        :default: - CloudFormation-generated name.
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def visibility_timeout(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''Timeout of processing a single message.

        After dequeuing, the processor has this much time to handle the message and delete it from the queue
        before it becomes visible again for dequeueing by another processor. Values must be between 0 and (12 hours).

        :default: Duration.seconds(30)
        '''
        result = self._values.get("visibility_timeout")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        :default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QueueProcessingServiceBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledEc2TaskDefinitionOptions",
    jsii_struct_bases=[],
    name_mapping={"task_definition": "taskDefinition"},
)
class ScheduledEc2TaskDefinitionOptions:
    def __init__(
        self,
        *,
        task_definition: _aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition,
    ) -> None:
        '''The properties for the ScheduledEc2Task using a task definition.

        :param task_definition: The task definition to use for tasks in the service. One of image or taskDefinition must be specified. [disable-awslint:ref-via-interface] Default: - none

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ecs as ecs
            import aws_cdk.aws_ecs_patterns as ecs_patterns
            
            # ec2_task_definition: ecs.Ec2TaskDefinition
            
            scheduled_ec2_task_definition_options = ecs_patterns.ScheduledEc2TaskDefinitionOptions(
                task_definition=ec2_task_definition
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f9043838648ba66f337b8e8eb6102a2dd574988a6641ad03674eac625feeb4)
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "task_definition": task_definition,
        }

    @builtins.property
    def task_definition(self) -> _aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition:
        '''The task definition to use for tasks in the service. One of image or taskDefinition must be specified.

        [disable-awslint:ref-via-interface]

        :default: - none
        '''
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduledEc2TaskDefinitionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledFargateTaskDefinitionOptions",
    jsii_struct_bases=[],
    name_mapping={"task_definition": "taskDefinition"},
)
class ScheduledFargateTaskDefinitionOptions:
    def __init__(
        self,
        *,
        task_definition: _aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition,
    ) -> None:
        '''The properties for the ScheduledFargateTask using a task definition.

        :param task_definition: The task definition to use for tasks in the service. Image or taskDefinition must be specified, but not both. [disable-awslint:ref-via-interface] Default: - none

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ecs as ecs
            import aws_cdk.aws_ecs_patterns as ecs_patterns
            
            # fargate_task_definition: ecs.FargateTaskDefinition
            
            scheduled_fargate_task_definition_options = ecs_patterns.ScheduledFargateTaskDefinitionOptions(
                task_definition=fargate_task_definition
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc8a83aae9ace58f8e94ffbc7b5b82a7f444c7b4b21e91a12434f57fe023795)
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "task_definition": task_definition,
        }

    @builtins.property
    def task_definition(self) -> _aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition:
        '''The task definition to use for tasks in the service. Image or taskDefinition must be specified, but not both.

        [disable-awslint:ref-via-interface]

        :default: - none
        '''
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduledFargateTaskDefinitionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ScheduledTaskBase(
    _aws_cdk_core_f4b25747.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledTaskBase",
):
    '''The base class for ScheduledEc2Task and ScheduledFargateTask tasks.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        schedule: _aws_cdk_aws_applicationautoscaling_a31e8c21.Schedule,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        desired_task_count: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        rule_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''Constructs a new instance of the ScheduledTaskBase class.

        :param scope: -
        :param id: -
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch User Guide.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_.
        :param security_groups: Existing security groups to use for your service. Default: - a new security group will be created.
        :param subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb5878ed966887ad6b48c3d5dde4d7674dd004380184dbe56803969fb69bbb2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ScheduledTaskBaseProps(
            schedule=schedule,
            cluster=cluster,
            desired_task_count=desired_task_count,
            enabled=enabled,
            rule_name=rule_name,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addTaskAsTarget")
    def _add_task_as_target(
        self,
        ecs_task_target: _aws_cdk_aws_events_targets_3ef2ed32.EcsTask,
    ) -> None:
        '''Adds task as a target of the scheduled event rule.

        :param ecs_task_target: the EcsTask to add to the event rule.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d0959a125b494a3a9272cbc0d8c7deebbb7da6e9c18cc132ac70a841137009)
            check_type(argname="argument ecs_task_target", value=ecs_task_target, expected_type=type_hints["ecs_task_target"])
        return typing.cast(None, jsii.invoke(self, "addTaskAsTarget", [ecs_task_target]))

    @jsii.member(jsii_name="addTaskDefinitionToEventTarget")
    def _add_task_definition_to_event_target(
        self,
        task_definition: _aws_cdk_aws_ecs_7896c08f.TaskDefinition,
    ) -> _aws_cdk_aws_events_targets_3ef2ed32.EcsTask:
        '''Create an ECS task using the task definition provided and add it to the scheduled event rule.

        :param task_definition: the TaskDefinition to add to the event rule.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5594af5d8c06660a4565b856ad9968199f382c4e0ab141ca08ada0efe954acc5)
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
        return typing.cast(_aws_cdk_aws_events_targets_3ef2ed32.EcsTask, jsii.invoke(self, "addTaskDefinitionToEventTarget", [task_definition]))

    @jsii.member(jsii_name="createAWSLogDriver")
    def _create_aws_log_driver(
        self,
        prefix: builtins.str,
    ) -> _aws_cdk_aws_ecs_7896c08f.AwsLogDriver:
        '''Create an AWS Log Driver with the provided streamPrefix.

        :param prefix: the Cloudwatch logging prefix.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5bf15bd25cf5fef77f57d5a52a0bfe3419040bf720324153d22cf6d62ac9e4b)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.AwsLogDriver, jsii.invoke(self, "createAWSLogDriver", [prefix]))

    @jsii.member(jsii_name="getDefaultCluster")
    def _get_default_cluster(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> _aws_cdk_aws_ecs_7896c08f.Cluster:
        '''Returns the default cluster.

        :param scope: -
        :param vpc: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9b0adcc42fc3c2b0f85bf46ef6e980efb8b45352b08a808fe7b756571a43b40)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.Cluster, jsii.invoke(self, "getDefaultCluster", [scope, vpc]))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _aws_cdk_aws_ecs_7896c08f.ICluster:
        '''The name of the cluster that hosts the service.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.ICluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="desiredTaskCount")
    def desired_task_count(self) -> jsii.Number:
        '''The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1
        '''
        return typing.cast(jsii.Number, jsii.get(self, "desiredTaskCount"))

    @builtins.property
    @jsii.member(jsii_name="eventRule")
    def event_rule(self) -> _aws_cdk_aws_events_efcdfa54.Rule:
        '''The CloudWatch Events rule for the service.'''
        return typing.cast(_aws_cdk_aws_events_efcdfa54.Rule, jsii.get(self, "eventRule"))

    @builtins.property
    @jsii.member(jsii_name="subnetSelection")
    def subnet_selection(self) -> _aws_cdk_aws_ec2_67de8e8d.SubnetSelection:
        '''In what subnets to place the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        :default: Private subnets
        '''
        return typing.cast(_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, jsii.get(self, "subnetSelection"))


class _ScheduledTaskBaseProxy(ScheduledTaskBase):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ScheduledTaskBase).__jsii_proxy_class__ = lambda : _ScheduledTaskBaseProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledTaskBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "schedule": "schedule",
        "cluster": "cluster",
        "desired_task_count": "desiredTaskCount",
        "enabled": "enabled",
        "rule_name": "ruleName",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
    },
)
class ScheduledTaskBaseProps:
    def __init__(
        self,
        *,
        schedule: _aws_cdk_aws_applicationautoscaling_a31e8c21.Schedule,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        desired_task_count: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        rule_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''The properties for the base ScheduledEc2Task or ScheduledFargateTask task.

        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch User Guide.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_.
        :param security_groups: Existing security groups to use for your service. Default: - a new security group will be created.
        :param subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_applicationautoscaling as appscaling
            import aws_cdk.aws_ec2 as ec2
            import aws_cdk.aws_ecs as ecs
            import aws_cdk.aws_ecs_patterns as ecs_patterns
            
            # cluster: ecs.Cluster
            # schedule: appscaling.Schedule
            # security_group: ec2.SecurityGroup
            # subnet: ec2.Subnet
            # subnet_filter: ec2.SubnetFilter
            # vpc: ec2.Vpc
            
            scheduled_task_base_props = ecs_patterns.ScheduledTaskBaseProps(
                schedule=schedule,
            
                # the properties below are optional
                cluster=cluster,
                desired_task_count=123,
                enabled=False,
                rule_name="ruleName",
                security_groups=[security_group],
                subnet_selection=ec2.SubnetSelection(
                    availability_zones=["availabilityZones"],
                    one_per_az=False,
                    subnet_filters=[subnet_filter],
                    subnet_group_name="subnetGroupName",
                    subnet_name="subnetName",
                    subnets=[subnet],
                    subnet_type=ec2.SubnetType.ISOLATED
                ),
                vpc=vpc
            )
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_67de8e8d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d95e4023ee9b3e5b2533a632471a9a356c3a9b1e0f66676f11458ac37c9b258)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument desired_task_count", value=desired_task_count, expected_type=type_hints["desired_task_count"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedule": schedule,
        }
        if cluster is not None:
            self._values["cluster"] = cluster
        if desired_task_count is not None:
            self._values["desired_task_count"] = desired_task_count
        if enabled is not None:
            self._values["enabled"] = enabled
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def schedule(self) -> _aws_cdk_aws_applicationautoscaling_a31e8c21.Schedule:
        '''The schedule or rate (frequency) that determines when CloudWatch Events runs the rule.

        For more information, see
        `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_
        in the Amazon CloudWatch User Guide.
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(_aws_cdk_aws_applicationautoscaling_a31e8c21.Schedule, result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster]:
        '''The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster], result)

    @builtins.property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        :default: 1
        '''
        result = self._values.get("desired_task_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the rule is enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''A name for the rule.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
        for the rule name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_.
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]]:
        '''Existing security groups to use for your service.

        :default: - a new security group will be created.
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection]:
        '''In what subnets to place the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        :default: Private subnets
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        :default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduledTaskBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledTaskImageProps",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "command": "command",
        "environment": "environment",
        "log_driver": "logDriver",
        "secrets": "secrets",
    },
)
class ScheduledTaskImageProps:
    def __init__(
        self,
        *,
        image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
    ) -> None:
        '''
        :param image: The image used to start a container. Image or taskDefinition must be specified, but not both. Default: - none
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param environment: The environment variables to pass to the container. Default: none
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ecs as ecs
            import aws_cdk.aws_ecs_patterns as ecs_patterns
            
            # container_image: ecs.ContainerImage
            # log_driver: ecs.LogDriver
            # secret: ecs.Secret
            
            scheduled_task_image_props = ecs_patterns.ScheduledTaskImageProps(
                image=container_image,
            
                # the properties below are optional
                command=["command"],
                environment={
                    "environment_key": "environment"
                },
                log_driver=log_driver,
                secrets={
                    "secrets_key": secret
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd2f39459e853466df230873bdf5ca27afa15c60fa103d8e8042a9214f53077)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument log_driver", value=log_driver, expected_type=type_hints["log_driver"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if command is not None:
            self._values["command"] = command
        if environment is not None:
            self._values["environment"] = environment
        if log_driver is not None:
            self._values["log_driver"] = log_driver
        if secrets is not None:
            self._values["secrets"] = secrets

    @builtins.property
    def image(self) -> _aws_cdk_aws_ecs_7896c08f.ContainerImage:
        '''The image used to start a container.

        Image or taskDefinition must be specified, but not both.

        :default: - none
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.ContainerImage, result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        :default: - CMD value built into container image.
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The environment variables to pass to the container.

        :default: none
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def log_driver(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver]:
        '''The log driver to use.

        :default: - AwsLogDriver if enableLogging is true
        '''
        result = self._values.get("log_driver")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]]:
        '''The secret to expose to the container as an environment variable.

        :default: - No secret environment variables.
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduledTaskImageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationLoadBalancedEc2Service(
    ApplicationLoadBalancedServiceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancedEc2Service",
):
    '''An EC2 service running on an ECS cluster fronted by an application load balancer.

    :exampleMetadata: infused

    Example::

        # cluster: ecs.Cluster
        
        load_balanced_ecs_service = ecs_patterns.ApplicationLoadBalancedEc2Service(self, "Service",
            cluster=cluster,
            memory_limit_mi_b=1024,
            task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("test"),
                environment={
                    "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
                    "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
                }
            ),
            desired_count=2
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        memory_reservation_mib: typing.Optional[jsii.Number] = None,
        placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
        placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
        task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition] = None,
        certificate: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate] = None,
        circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        domain_name: typing.Optional[builtins.str] = None,
        domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancer] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        max_healthy_percent: typing.Optional[jsii.Number] = None,
        min_healthy_percent: typing.Optional[jsii.Number] = None,
        open_listener: typing.Optional[builtins.bool] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
        protocol_version: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocolVersion] = None,
        public_load_balancer: typing.Optional[builtins.bool] = None,
        record_type: typing.Optional[ApplicationLoadBalancedServiceRecordType] = None,
        redirect_http: typing.Optional[builtins.bool] = None,
        service_name: typing.Optional[builtins.str] = None,
        ssl_policy: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy] = None,
        target_protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
        task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''Constructs a new instance of the ApplicationLoadBalancedEc2Service class.

        :param scope: -
        :param id: -
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory reserved.
        :param placement_constraints: The placement constraints to use for tasks in the service. For more information, see `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_. Default: - No constraints.
        :param placement_strategies: The placement strategies to use for tasks in the service. For more information, see `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_. Default: - No strategies.
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both.. [disable-awslint:ref-via-interface] Default: - none
        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param circuit_breaker: Whether to enable the deployment circuit breaker. If this property is defined, circuit breaker will be implicitly enabled. Default: - disabled
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the application load balancer that will serve traffic to the service. Default: - The default listener port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        :param load_balancer: The application load balancer that will serve traffic to the service. The VPC attribute of a load balancer must be specified for it to be used to create a new service with this pattern. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param load_balancer_name: Name of the load balancer. Default: - Automatically generated name.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param open_listener: Determines whether or not the Security Group for the Load Balancer's Listener will be open to all traffic by default. Default: true -- The security group allows ingress from all IP addresses.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: HTTP. If a certificate is specified, the protocol will be set by default to HTTPS.
        :param protocol_version: The protocol version to use. Default: ApplicationProtocolVersion.HTTP1
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param record_type: Specifies whether the Route53 record should be a CNAME, an A record using the Alias feature or no record at all. This is useful if you need to work with DNS systems that do not support alias records. Default: ApplicationLoadBalancedServiceRecordType.ALIAS
        :param redirect_http: Specifies whether the load balancer should redirect traffic on port 80 to port 443 to support HTTP->HTTPS redirects This is only valid if the protocol of the ALB is HTTPS. Default: false
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported by the ALB Listener. Default: - The recommended elastic load balancing security policy
        :param target_protocol: The protocol for connections from the load balancer to the ECS tasks. The default target port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). Default: HTTP.
        :param task_image_options: The properties required to create a new task definition. TaskDefinition or TaskImageOptions must be specified, but not both. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e4ae5bbd924f174122acbc2af61b1f67f7d61969f57e8671472e64fd9deb2f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApplicationLoadBalancedEc2ServiceProps(
            cpu=cpu,
            memory_limit_mib=memory_limit_mib,
            memory_reservation_mib=memory_reservation_mib,
            placement_constraints=placement_constraints,
            placement_strategies=placement_strategies,
            task_definition=task_definition,
            certificate=certificate,
            circuit_breaker=circuit_breaker,
            cloud_map_options=cloud_map_options,
            cluster=cluster,
            deployment_controller=deployment_controller,
            desired_count=desired_count,
            domain_name=domain_name,
            domain_zone=domain_zone,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            health_check_grace_period=health_check_grace_period,
            listener_port=listener_port,
            load_balancer=load_balancer,
            load_balancer_name=load_balancer_name,
            max_healthy_percent=max_healthy_percent,
            min_healthy_percent=min_healthy_percent,
            open_listener=open_listener,
            propagate_tags=propagate_tags,
            protocol=protocol,
            protocol_version=protocol_version,
            public_load_balancer=public_load_balancer,
            record_type=record_type,
            redirect_http=redirect_http,
            service_name=service_name,
            ssl_policy=ssl_policy,
            target_protocol=target_protocol,
            task_image_options=task_image_options,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _aws_cdk_aws_ecs_7896c08f.Ec2Service:
        '''The EC2 service in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.Ec2Service, jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition:
        '''The EC2 Task Definition in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition, jsii.get(self, "taskDefinition"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancedEc2ServiceProps",
    jsii_struct_bases=[ApplicationLoadBalancedServiceBaseProps],
    name_mapping={
        "certificate": "certificate",
        "circuit_breaker": "circuitBreaker",
        "cloud_map_options": "cloudMapOptions",
        "cluster": "cluster",
        "deployment_controller": "deploymentController",
        "desired_count": "desiredCount",
        "domain_name": "domainName",
        "domain_zone": "domainZone",
        "enable_ecs_managed_tags": "enableECSManagedTags",
        "health_check_grace_period": "healthCheckGracePeriod",
        "listener_port": "listenerPort",
        "load_balancer": "loadBalancer",
        "load_balancer_name": "loadBalancerName",
        "max_healthy_percent": "maxHealthyPercent",
        "min_healthy_percent": "minHealthyPercent",
        "open_listener": "openListener",
        "propagate_tags": "propagateTags",
        "protocol": "protocol",
        "protocol_version": "protocolVersion",
        "public_load_balancer": "publicLoadBalancer",
        "record_type": "recordType",
        "redirect_http": "redirectHTTP",
        "service_name": "serviceName",
        "ssl_policy": "sslPolicy",
        "target_protocol": "targetProtocol",
        "task_image_options": "taskImageOptions",
        "vpc": "vpc",
        "cpu": "cpu",
        "memory_limit_mib": "memoryLimitMiB",
        "memory_reservation_mib": "memoryReservationMiB",
        "placement_constraints": "placementConstraints",
        "placement_strategies": "placementStrategies",
        "task_definition": "taskDefinition",
    },
)
class ApplicationLoadBalancedEc2ServiceProps(ApplicationLoadBalancedServiceBaseProps):
    def __init__(
        self,
        *,
        certificate: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate] = None,
        circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        domain_name: typing.Optional[builtins.str] = None,
        domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancer] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        max_healthy_percent: typing.Optional[jsii.Number] = None,
        min_healthy_percent: typing.Optional[jsii.Number] = None,
        open_listener: typing.Optional[builtins.bool] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
        protocol_version: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocolVersion] = None,
        public_load_balancer: typing.Optional[builtins.bool] = None,
        record_type: typing.Optional[ApplicationLoadBalancedServiceRecordType] = None,
        redirect_http: typing.Optional[builtins.bool] = None,
        service_name: typing.Optional[builtins.str] = None,
        ssl_policy: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy] = None,
        target_protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
        task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        memory_reservation_mib: typing.Optional[jsii.Number] = None,
        placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
        placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
        task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition] = None,
    ) -> None:
        '''The properties for the ApplicationLoadBalancedEc2Service service.

        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param circuit_breaker: Whether to enable the deployment circuit breaker. If this property is defined, circuit breaker will be implicitly enabled. Default: - disabled
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the application load balancer that will serve traffic to the service. Default: - The default listener port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        :param load_balancer: The application load balancer that will serve traffic to the service. The VPC attribute of a load balancer must be specified for it to be used to create a new service with this pattern. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param load_balancer_name: Name of the load balancer. Default: - Automatically generated name.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param open_listener: Determines whether or not the Security Group for the Load Balancer's Listener will be open to all traffic by default. Default: true -- The security group allows ingress from all IP addresses.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: HTTP. If a certificate is specified, the protocol will be set by default to HTTPS.
        :param protocol_version: The protocol version to use. Default: ApplicationProtocolVersion.HTTP1
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param record_type: Specifies whether the Route53 record should be a CNAME, an A record using the Alias feature or no record at all. This is useful if you need to work with DNS systems that do not support alias records. Default: ApplicationLoadBalancedServiceRecordType.ALIAS
        :param redirect_http: Specifies whether the load balancer should redirect traffic on port 80 to port 443 to support HTTP->HTTPS redirects This is only valid if the protocol of the ALB is HTTPS. Default: false
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported by the ALB Listener. Default: - The recommended elastic load balancing security policy
        :param target_protocol: The protocol for connections from the load balancer to the ECS tasks. The default target port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). Default: HTTP.
        :param task_image_options: The properties required to create a new task definition. TaskDefinition or TaskImageOptions must be specified, but not both. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory reserved.
        :param placement_constraints: The placement constraints to use for tasks in the service. For more information, see `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_. Default: - No constraints.
        :param placement_strategies: The placement strategies to use for tasks in the service. For more information, see `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_. Default: - No strategies.
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both.. [disable-awslint:ref-via-interface] Default: - none

        :exampleMetadata: infused

        Example::

            # cluster: ecs.Cluster
            
            load_balanced_ecs_service = ecs_patterns.ApplicationLoadBalancedEc2Service(self, "Service",
                cluster=cluster,
                memory_limit_mi_b=1024,
                task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
                    image=ecs.ContainerImage.from_registry("test"),
                    environment={
                        "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
                        "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
                    }
                ),
                desired_count=2
            )
        '''
        if isinstance(circuit_breaker, dict):
            circuit_breaker = _aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker(**circuit_breaker)
        if isinstance(cloud_map_options, dict):
            cloud_map_options = _aws_cdk_aws_ecs_7896c08f.CloudMapOptions(**cloud_map_options)
        if isinstance(deployment_controller, dict):
            deployment_controller = _aws_cdk_aws_ecs_7896c08f.DeploymentController(**deployment_controller)
        if isinstance(task_image_options, dict):
            task_image_options = ApplicationLoadBalancedTaskImageOptions(**task_image_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b145ea706712b94e1d19bc34152617d9aee6772222ed5db90f966863e271e2d1)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument circuit_breaker", value=circuit_breaker, expected_type=type_hints["circuit_breaker"])
            check_type(argname="argument cloud_map_options", value=cloud_map_options, expected_type=type_hints["cloud_map_options"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument deployment_controller", value=deployment_controller, expected_type=type_hints["deployment_controller"])
            check_type(argname="argument desired_count", value=desired_count, expected_type=type_hints["desired_count"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_zone", value=domain_zone, expected_type=type_hints["domain_zone"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument health_check_grace_period", value=health_check_grace_period, expected_type=type_hints["health_check_grace_period"])
            check_type(argname="argument listener_port", value=listener_port, expected_type=type_hints["listener_port"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument load_balancer_name", value=load_balancer_name, expected_type=type_hints["load_balancer_name"])
            check_type(argname="argument max_healthy_percent", value=max_healthy_percent, expected_type=type_hints["max_healthy_percent"])
            check_type(argname="argument min_healthy_percent", value=min_healthy_percent, expected_type=type_hints["min_healthy_percent"])
            check_type(argname="argument open_listener", value=open_listener, expected_type=type_hints["open_listener"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument protocol_version", value=protocol_version, expected_type=type_hints["protocol_version"])
            check_type(argname="argument public_load_balancer", value=public_load_balancer, expected_type=type_hints["public_load_balancer"])
            check_type(argname="argument record_type", value=record_type, expected_type=type_hints["record_type"])
            check_type(argname="argument redirect_http", value=redirect_http, expected_type=type_hints["redirect_http"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument ssl_policy", value=ssl_policy, expected_type=type_hints["ssl_policy"])
            check_type(argname="argument target_protocol", value=target_protocol, expected_type=type_hints["target_protocol"])
            check_type(argname="argument task_image_options", value=task_image_options, expected_type=type_hints["task_image_options"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument memory_reservation_mib", value=memory_reservation_mib, expected_type=type_hints["memory_reservation_mib"])
            check_type(argname="argument placement_constraints", value=placement_constraints, expected_type=type_hints["placement_constraints"])
            check_type(argname="argument placement_strategies", value=placement_strategies, expected_type=type_hints["placement_strategies"])
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate is not None:
            self._values["certificate"] = certificate
        if circuit_breaker is not None:
            self._values["circuit_breaker"] = circuit_breaker
        if cloud_map_options is not None:
            self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None:
            self._values["cluster"] = cluster
        if deployment_controller is not None:
            self._values["deployment_controller"] = deployment_controller
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if domain_zone is not None:
            self._values["domain_zone"] = domain_zone
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None:
            self._values["health_check_grace_period"] = health_check_grace_period
        if listener_port is not None:
            self._values["listener_port"] = listener_port
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if load_balancer_name is not None:
            self._values["load_balancer_name"] = load_balancer_name
        if max_healthy_percent is not None:
            self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None:
            self._values["min_healthy_percent"] = min_healthy_percent
        if open_listener is not None:
            self._values["open_listener"] = open_listener
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if protocol is not None:
            self._values["protocol"] = protocol
        if protocol_version is not None:
            self._values["protocol_version"] = protocol_version
        if public_load_balancer is not None:
            self._values["public_load_balancer"] = public_load_balancer
        if record_type is not None:
            self._values["record_type"] = record_type
        if redirect_http is not None:
            self._values["redirect_http"] = redirect_http
        if service_name is not None:
            self._values["service_name"] = service_name
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy
        if target_protocol is not None:
            self._values["target_protocol"] = target_protocol
        if task_image_options is not None:
            self._values["task_image_options"] = task_image_options
        if vpc is not None:
            self._values["vpc"] = vpc
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None:
            self._values["memory_reservation_mib"] = memory_reservation_mib
        if placement_constraints is not None:
            self._values["placement_constraints"] = placement_constraints
        if placement_strategies is not None:
            self._values["placement_strategies"] = placement_strategies
        if task_definition is not None:
            self._values["task_definition"] = task_definition

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate]:
        '''Certificate Manager certificate to associate with the load balancer.

        Setting this option will set the load balancer protocol to HTTPS.

        :default:

        - No certificate associated with the load balancer, if using
        the HTTP protocol. For HTTPS, a DNS-validated certificate will be
        created for the load balancer's specified domain name.
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate], result)

    @builtins.property
    def circuit_breaker(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker]:
        '''Whether to enable the deployment circuit breaker.

        If this property is defined, circuit breaker will be implicitly
        enabled.

        :default: - disabled
        '''
        result = self._values.get("circuit_breaker")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker], result)

    @builtins.property
    def cloud_map_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions]:
        '''The options for configuring an Amazon ECS service to use service discovery.

        :default: - AWS Cloud Map service discovery is not enabled.
        '''
        result = self._values.get("cloud_map_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions], result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster]:
        '''The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster], result)

    @builtins.property
    def deployment_controller(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentController]:
        '''Specifies which deployment controller to use for the service.

        For more information, see
        `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_

        :default: - Rolling update (ECS)
        '''
        result = self._values.get("deployment_controller")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentController], result)

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        :default:

        - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1;
        if true, the default is 1 for all new services and uses the existing services desired count
        when updating an existing service.
        '''
        result = self._values.get("desired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name for the service, e.g. "api.example.com.".

        :default: - No domain name.
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_zone(self) -> typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone]:
        '''The Route53 hosted zone for the domain, e.g. "example.com.".

        :default: - No Route53 hosted domain zone.
        '''
        result = self._values.get("domain_zone")
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone], result)

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        :default: false
        '''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def health_check_grace_period(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        '''
        result = self._values.get("health_check_grace_period")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        '''Listener port of the application load balancer that will serve traffic to the service.

        :default:

        - The default listener port is determined from the protocol (port 80 for HTTP,
        port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        '''
        result = self._values.get("listener_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def load_balancer(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancer]:
        '''The application load balancer that will serve traffic to the service.

        The VPC attribute of a load balancer must be specified for it to be used
        to create a new service with this pattern.

        [disable-awslint:ref-via-interface]

        :default: - a new load balancer will be created.
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancer], result)

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[builtins.str]:
        '''Name of the load balancer.

        :default: - Automatically generated name.
        '''
        result = self._values.get("load_balancer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        :default: - 100 if daemon, otherwise 200
        '''
        result = self._values.get("max_healthy_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        :default: - 0 if daemon, otherwise 50
        '''
        result = self._values.get("min_healthy_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def open_listener(self) -> typing.Optional[builtins.bool]:
        '''Determines whether or not the Security Group for the Load Balancer's Listener will be open to all traffic by default.

        :default: true -- The security group allows ingress from all IP addresses.
        '''
        result = self._values.get("open_listener")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def propagate_tags(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource]:
        '''Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        :default: - none
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource], result)

    @builtins.property
    def protocol(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol]:
        '''The protocol for connections from clients to the load balancer.

        The load balancer port is determined from the protocol (port 80 for
        HTTP, port 443 for HTTPS).  A domain name and zone must be also be
        specified if using HTTPS.

        :default:

        HTTP. If a certificate is specified, the protocol will be
        set by default to HTTPS.
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol], result)

    @builtins.property
    def protocol_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocolVersion]:
        '''The protocol version to use.

        :default: ApplicationProtocolVersion.HTTP1
        '''
        result = self._values.get("protocol_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocolVersion], result)

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[builtins.bool]:
        '''Determines whether the Load Balancer will be internet-facing.

        :default: true
        '''
        result = self._values.get("public_load_balancer")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def record_type(self) -> typing.Optional[ApplicationLoadBalancedServiceRecordType]:
        '''Specifies whether the Route53 record should be a CNAME, an A record using the Alias feature or no record at all.

        This is useful if you need to work with DNS systems that do not support alias records.

        :default: ApplicationLoadBalancedServiceRecordType.ALIAS
        '''
        result = self._values.get("record_type")
        return typing.cast(typing.Optional[ApplicationLoadBalancedServiceRecordType], result)

    @builtins.property
    def redirect_http(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether the load balancer should redirect traffic on port 80 to port 443 to support HTTP->HTTPS redirects This is only valid if the protocol of the ALB is HTTPS.

        :default: false
        '''
        result = self._values.get("redirect_http")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        :default: - CloudFormation-generated name.
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy]:
        '''The security policy that defines which ciphers and protocols are supported by the ALB Listener.

        :default: - The recommended elastic load balancing security policy
        '''
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy], result)

    @builtins.property
    def target_protocol(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol]:
        '''The protocol for connections from the load balancer to the ECS tasks.

        The default target port is determined from the protocol (port 80 for
        HTTP, port 443 for HTTPS).

        :default: HTTP.
        '''
        result = self._values.get("target_protocol")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol], result)

    @builtins.property
    def task_image_options(
        self,
    ) -> typing.Optional[ApplicationLoadBalancedTaskImageOptions]:
        '''The properties required to create a new task definition.

        TaskDefinition or TaskImageOptions must be specified, but not both.

        :default: none
        '''
        result = self._values.get("task_image_options")
        return typing.cast(typing.Optional[ApplicationLoadBalancedTaskImageOptions], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        :default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        :default: none
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        :default: - No memory limit.
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        '''The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under contention, Docker attempts to keep the
        container memory within the limit. If the container requires more memory,
        it can consume up to the value specified by the Memory property or all of
        the available memory on the container instance—whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        :default: - No memory reserved.
        '''
        result = self._values.get("memory_reservation_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def placement_constraints(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]]:
        '''The placement constraints to use for tasks in the service.

        For more information, see
        `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_.

        :default: - No constraints.
        '''
        result = self._values.get("placement_constraints")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]], result)

    @builtins.property
    def placement_strategies(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]]:
        '''The placement strategies to use for tasks in the service.

        For more information, see
        `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_.

        :default: - No strategies.
        '''
        result = self._values.get("placement_strategies")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]], result)

    @builtins.property
    def task_definition(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition]:
        '''The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both..

        [disable-awslint:ref-via-interface]

        :default: - none
        '''
        result = self._values.get("task_definition")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationLoadBalancedEc2ServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationLoadBalancedFargateService(
    ApplicationLoadBalancedServiceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancedFargateService",
):
    '''A Fargate service running on an ECS cluster fronted by an application load balancer.

    :exampleMetadata: infused

    Example::

        # cluster: ecs.Cluster
        
        load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
            cluster=cluster,
            memory_limit_mi_b=1024,
            desired_count=1,
            cpu=512,
            task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
            )
        )
        
        scalable_target = load_balanced_fargate_service.service.auto_scale_task_count(
            min_capacity=1,
            max_capacity=20
        )
        
        scalable_target.scale_on_cpu_utilization("CpuScaling",
            target_utilization_percent=50
        )
        
        scalable_target.scale_on_memory_utilization("MemoryScaling",
            target_utilization_percent=50
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
        task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition] = None,
        task_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        certificate: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate] = None,
        circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        domain_name: typing.Optional[builtins.str] = None,
        domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancer] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        max_healthy_percent: typing.Optional[jsii.Number] = None,
        min_healthy_percent: typing.Optional[jsii.Number] = None,
        open_listener: typing.Optional[builtins.bool] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
        protocol_version: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocolVersion] = None,
        public_load_balancer: typing.Optional[builtins.bool] = None,
        record_type: typing.Optional[ApplicationLoadBalancedServiceRecordType] = None,
        redirect_http: typing.Optional[builtins.bool] = None,
        service_name: typing.Optional[builtins.str] = None,
        ssl_policy: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy] = None,
        target_protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
        task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''Constructs a new instance of the ApplicationLoadBalancedFargateService class.

        :param scope: -
        :param id: -
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param security_groups: The security groups to associate with the service. If you do not specify a security group, a new security group is created. Default: - A new security group is created.
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both. [disable-awslint:ref-via-interface] Default: - none
        :param task_subnets: The subnets to associate with the service. Default: - Public subnets if ``assignPublicIp`` is set, otherwise the first available one of Private, Isolated, Public, in that order.
        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param circuit_breaker: Whether to enable the deployment circuit breaker. If this property is defined, circuit breaker will be implicitly enabled. Default: - disabled
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the application load balancer that will serve traffic to the service. Default: - The default listener port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        :param load_balancer: The application load balancer that will serve traffic to the service. The VPC attribute of a load balancer must be specified for it to be used to create a new service with this pattern. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param load_balancer_name: Name of the load balancer. Default: - Automatically generated name.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param open_listener: Determines whether or not the Security Group for the Load Balancer's Listener will be open to all traffic by default. Default: true -- The security group allows ingress from all IP addresses.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: HTTP. If a certificate is specified, the protocol will be set by default to HTTPS.
        :param protocol_version: The protocol version to use. Default: ApplicationProtocolVersion.HTTP1
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param record_type: Specifies whether the Route53 record should be a CNAME, an A record using the Alias feature or no record at all. This is useful if you need to work with DNS systems that do not support alias records. Default: ApplicationLoadBalancedServiceRecordType.ALIAS
        :param redirect_http: Specifies whether the load balancer should redirect traffic on port 80 to port 443 to support HTTP->HTTPS redirects This is only valid if the protocol of the ALB is HTTPS. Default: false
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported by the ALB Listener. Default: - The recommended elastic load balancing security policy
        :param target_protocol: The protocol for connections from the load balancer to the ECS tasks. The default target port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). Default: HTTP.
        :param task_image_options: The properties required to create a new task definition. TaskDefinition or TaskImageOptions must be specified, but not both. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d8973f4b6cc15ae4ca3c237489d80bd19d510b9ae5eeae12b6236dd0e44342)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApplicationLoadBalancedFargateServiceProps(
            assign_public_ip=assign_public_ip,
            cpu=cpu,
            memory_limit_mib=memory_limit_mib,
            platform_version=platform_version,
            security_groups=security_groups,
            task_definition=task_definition,
            task_subnets=task_subnets,
            certificate=certificate,
            circuit_breaker=circuit_breaker,
            cloud_map_options=cloud_map_options,
            cluster=cluster,
            deployment_controller=deployment_controller,
            desired_count=desired_count,
            domain_name=domain_name,
            domain_zone=domain_zone,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            health_check_grace_period=health_check_grace_period,
            listener_port=listener_port,
            load_balancer=load_balancer,
            load_balancer_name=load_balancer_name,
            max_healthy_percent=max_healthy_percent,
            min_healthy_percent=min_healthy_percent,
            open_listener=open_listener,
            propagate_tags=propagate_tags,
            protocol=protocol,
            protocol_version=protocol_version,
            public_load_balancer=public_load_balancer,
            record_type=record_type,
            redirect_http=redirect_http,
            service_name=service_name,
            ssl_policy=ssl_policy,
            target_protocol=target_protocol,
            task_image_options=task_image_options,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> builtins.bool:
        '''Determines whether the service will be assigned a public IP address.'''
        return typing.cast(builtins.bool, jsii.get(self, "assignPublicIp"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _aws_cdk_aws_ecs_7896c08f.FargateService:
        '''The Fargate service in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.FargateService, jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition:
        '''The Fargate task definition in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition, jsii.get(self, "taskDefinition"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancedFargateServiceProps",
    jsii_struct_bases=[ApplicationLoadBalancedServiceBaseProps],
    name_mapping={
        "certificate": "certificate",
        "circuit_breaker": "circuitBreaker",
        "cloud_map_options": "cloudMapOptions",
        "cluster": "cluster",
        "deployment_controller": "deploymentController",
        "desired_count": "desiredCount",
        "domain_name": "domainName",
        "domain_zone": "domainZone",
        "enable_ecs_managed_tags": "enableECSManagedTags",
        "health_check_grace_period": "healthCheckGracePeriod",
        "listener_port": "listenerPort",
        "load_balancer": "loadBalancer",
        "load_balancer_name": "loadBalancerName",
        "max_healthy_percent": "maxHealthyPercent",
        "min_healthy_percent": "minHealthyPercent",
        "open_listener": "openListener",
        "propagate_tags": "propagateTags",
        "protocol": "protocol",
        "protocol_version": "protocolVersion",
        "public_load_balancer": "publicLoadBalancer",
        "record_type": "recordType",
        "redirect_http": "redirectHTTP",
        "service_name": "serviceName",
        "ssl_policy": "sslPolicy",
        "target_protocol": "targetProtocol",
        "task_image_options": "taskImageOptions",
        "vpc": "vpc",
        "assign_public_ip": "assignPublicIp",
        "cpu": "cpu",
        "memory_limit_mib": "memoryLimitMiB",
        "platform_version": "platformVersion",
        "security_groups": "securityGroups",
        "task_definition": "taskDefinition",
        "task_subnets": "taskSubnets",
    },
)
class ApplicationLoadBalancedFargateServiceProps(
    ApplicationLoadBalancedServiceBaseProps,
):
    def __init__(
        self,
        *,
        certificate: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate] = None,
        circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        domain_name: typing.Optional[builtins.str] = None,
        domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancer] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        max_healthy_percent: typing.Optional[jsii.Number] = None,
        min_healthy_percent: typing.Optional[jsii.Number] = None,
        open_listener: typing.Optional[builtins.bool] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
        protocol_version: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocolVersion] = None,
        public_load_balancer: typing.Optional[builtins.bool] = None,
        record_type: typing.Optional[ApplicationLoadBalancedServiceRecordType] = None,
        redirect_http: typing.Optional[builtins.bool] = None,
        service_name: typing.Optional[builtins.str] = None,
        ssl_policy: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy] = None,
        target_protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
        task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
        task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition] = None,
        task_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''The properties for the ApplicationLoadBalancedFargateService service.

        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param circuit_breaker: Whether to enable the deployment circuit breaker. If this property is defined, circuit breaker will be implicitly enabled. Default: - disabled
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the application load balancer that will serve traffic to the service. Default: - The default listener port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        :param load_balancer: The application load balancer that will serve traffic to the service. The VPC attribute of a load balancer must be specified for it to be used to create a new service with this pattern. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param load_balancer_name: Name of the load balancer. Default: - Automatically generated name.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param open_listener: Determines whether or not the Security Group for the Load Balancer's Listener will be open to all traffic by default. Default: true -- The security group allows ingress from all IP addresses.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: HTTP. If a certificate is specified, the protocol will be set by default to HTTPS.
        :param protocol_version: The protocol version to use. Default: ApplicationProtocolVersion.HTTP1
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param record_type: Specifies whether the Route53 record should be a CNAME, an A record using the Alias feature or no record at all. This is useful if you need to work with DNS systems that do not support alias records. Default: ApplicationLoadBalancedServiceRecordType.ALIAS
        :param redirect_http: Specifies whether the load balancer should redirect traffic on port 80 to port 443 to support HTTP->HTTPS redirects This is only valid if the protocol of the ALB is HTTPS. Default: false
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param ssl_policy: The security policy that defines which ciphers and protocols are supported by the ALB Listener. Default: - The recommended elastic load balancing security policy
        :param target_protocol: The protocol for connections from the load balancer to the ECS tasks. The default target port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). Default: HTTP.
        :param task_image_options: The properties required to create a new task definition. TaskDefinition or TaskImageOptions must be specified, but not both. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param security_groups: The security groups to associate with the service. If you do not specify a security group, a new security group is created. Default: - A new security group is created.
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both. [disable-awslint:ref-via-interface] Default: - none
        :param task_subnets: The subnets to associate with the service. Default: - Public subnets if ``assignPublicIp`` is set, otherwise the first available one of Private, Isolated, Public, in that order.

        :exampleMetadata: infused

        Example::

            # cluster: ecs.Cluster
            
            load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
                cluster=cluster,
                memory_limit_mi_b=1024,
                desired_count=1,
                cpu=512,
                task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageOptions(
                    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
                )
            )
            
            scalable_target = load_balanced_fargate_service.service.auto_scale_task_count(
                min_capacity=1,
                max_capacity=20
            )
            
            scalable_target.scale_on_cpu_utilization("CpuScaling",
                target_utilization_percent=50
            )
            
            scalable_target.scale_on_memory_utilization("MemoryScaling",
                target_utilization_percent=50
            )
        '''
        if isinstance(circuit_breaker, dict):
            circuit_breaker = _aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker(**circuit_breaker)
        if isinstance(cloud_map_options, dict):
            cloud_map_options = _aws_cdk_aws_ecs_7896c08f.CloudMapOptions(**cloud_map_options)
        if isinstance(deployment_controller, dict):
            deployment_controller = _aws_cdk_aws_ecs_7896c08f.DeploymentController(**deployment_controller)
        if isinstance(task_image_options, dict):
            task_image_options = ApplicationLoadBalancedTaskImageOptions(**task_image_options)
        if isinstance(task_subnets, dict):
            task_subnets = _aws_cdk_aws_ec2_67de8e8d.SubnetSelection(**task_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7db0768517b85af0818a09d0288b9ca5ef25c386c71cca4ec9f6c0475d2544d)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument circuit_breaker", value=circuit_breaker, expected_type=type_hints["circuit_breaker"])
            check_type(argname="argument cloud_map_options", value=cloud_map_options, expected_type=type_hints["cloud_map_options"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument deployment_controller", value=deployment_controller, expected_type=type_hints["deployment_controller"])
            check_type(argname="argument desired_count", value=desired_count, expected_type=type_hints["desired_count"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_zone", value=domain_zone, expected_type=type_hints["domain_zone"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument health_check_grace_period", value=health_check_grace_period, expected_type=type_hints["health_check_grace_period"])
            check_type(argname="argument listener_port", value=listener_port, expected_type=type_hints["listener_port"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument load_balancer_name", value=load_balancer_name, expected_type=type_hints["load_balancer_name"])
            check_type(argname="argument max_healthy_percent", value=max_healthy_percent, expected_type=type_hints["max_healthy_percent"])
            check_type(argname="argument min_healthy_percent", value=min_healthy_percent, expected_type=type_hints["min_healthy_percent"])
            check_type(argname="argument open_listener", value=open_listener, expected_type=type_hints["open_listener"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument protocol_version", value=protocol_version, expected_type=type_hints["protocol_version"])
            check_type(argname="argument public_load_balancer", value=public_load_balancer, expected_type=type_hints["public_load_balancer"])
            check_type(argname="argument record_type", value=record_type, expected_type=type_hints["record_type"])
            check_type(argname="argument redirect_http", value=redirect_http, expected_type=type_hints["redirect_http"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument ssl_policy", value=ssl_policy, expected_type=type_hints["ssl_policy"])
            check_type(argname="argument target_protocol", value=target_protocol, expected_type=type_hints["target_protocol"])
            check_type(argname="argument task_image_options", value=task_image_options, expected_type=type_hints["task_image_options"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
            check_type(argname="argument task_subnets", value=task_subnets, expected_type=type_hints["task_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate is not None:
            self._values["certificate"] = certificate
        if circuit_breaker is not None:
            self._values["circuit_breaker"] = circuit_breaker
        if cloud_map_options is not None:
            self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None:
            self._values["cluster"] = cluster
        if deployment_controller is not None:
            self._values["deployment_controller"] = deployment_controller
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if domain_zone is not None:
            self._values["domain_zone"] = domain_zone
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None:
            self._values["health_check_grace_period"] = health_check_grace_period
        if listener_port is not None:
            self._values["listener_port"] = listener_port
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if load_balancer_name is not None:
            self._values["load_balancer_name"] = load_balancer_name
        if max_healthy_percent is not None:
            self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None:
            self._values["min_healthy_percent"] = min_healthy_percent
        if open_listener is not None:
            self._values["open_listener"] = open_listener
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if protocol is not None:
            self._values["protocol"] = protocol
        if protocol_version is not None:
            self._values["protocol_version"] = protocol_version
        if public_load_balancer is not None:
            self._values["public_load_balancer"] = public_load_balancer
        if record_type is not None:
            self._values["record_type"] = record_type
        if redirect_http is not None:
            self._values["redirect_http"] = redirect_http
        if service_name is not None:
            self._values["service_name"] = service_name
        if ssl_policy is not None:
            self._values["ssl_policy"] = ssl_policy
        if target_protocol is not None:
            self._values["target_protocol"] = target_protocol
        if task_image_options is not None:
            self._values["task_image_options"] = task_image_options
        if vpc is not None:
            self._values["vpc"] = vpc
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if platform_version is not None:
            self._values["platform_version"] = platform_version
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if task_definition is not None:
            self._values["task_definition"] = task_definition
        if task_subnets is not None:
            self._values["task_subnets"] = task_subnets

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate]:
        '''Certificate Manager certificate to associate with the load balancer.

        Setting this option will set the load balancer protocol to HTTPS.

        :default:

        - No certificate associated with the load balancer, if using
        the HTTP protocol. For HTTPS, a DNS-validated certificate will be
        created for the load balancer's specified domain name.
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate], result)

    @builtins.property
    def circuit_breaker(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker]:
        '''Whether to enable the deployment circuit breaker.

        If this property is defined, circuit breaker will be implicitly
        enabled.

        :default: - disabled
        '''
        result = self._values.get("circuit_breaker")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker], result)

    @builtins.property
    def cloud_map_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions]:
        '''The options for configuring an Amazon ECS service to use service discovery.

        :default: - AWS Cloud Map service discovery is not enabled.
        '''
        result = self._values.get("cloud_map_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions], result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster]:
        '''The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster], result)

    @builtins.property
    def deployment_controller(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentController]:
        '''Specifies which deployment controller to use for the service.

        For more information, see
        `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_

        :default: - Rolling update (ECS)
        '''
        result = self._values.get("deployment_controller")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentController], result)

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        :default:

        - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1;
        if true, the default is 1 for all new services and uses the existing services desired count
        when updating an existing service.
        '''
        result = self._values.get("desired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name for the service, e.g. "api.example.com.".

        :default: - No domain name.
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_zone(self) -> typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone]:
        '''The Route53 hosted zone for the domain, e.g. "example.com.".

        :default: - No Route53 hosted domain zone.
        '''
        result = self._values.get("domain_zone")
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone], result)

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        :default: false
        '''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def health_check_grace_period(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        '''
        result = self._values.get("health_check_grace_period")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        '''Listener port of the application load balancer that will serve traffic to the service.

        :default:

        - The default listener port is determined from the protocol (port 80 for HTTP,
        port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        '''
        result = self._values.get("listener_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def load_balancer(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancer]:
        '''The application load balancer that will serve traffic to the service.

        The VPC attribute of a load balancer must be specified for it to be used
        to create a new service with this pattern.

        [disable-awslint:ref-via-interface]

        :default: - a new load balancer will be created.
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancer], result)

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[builtins.str]:
        '''Name of the load balancer.

        :default: - Automatically generated name.
        '''
        result = self._values.get("load_balancer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        :default: - 100 if daemon, otherwise 200
        '''
        result = self._values.get("max_healthy_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        :default: - 0 if daemon, otherwise 50
        '''
        result = self._values.get("min_healthy_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def open_listener(self) -> typing.Optional[builtins.bool]:
        '''Determines whether or not the Security Group for the Load Balancer's Listener will be open to all traffic by default.

        :default: true -- The security group allows ingress from all IP addresses.
        '''
        result = self._values.get("open_listener")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def propagate_tags(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource]:
        '''Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        :default: - none
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource], result)

    @builtins.property
    def protocol(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol]:
        '''The protocol for connections from clients to the load balancer.

        The load balancer port is determined from the protocol (port 80 for
        HTTP, port 443 for HTTPS).  A domain name and zone must be also be
        specified if using HTTPS.

        :default:

        HTTP. If a certificate is specified, the protocol will be
        set by default to HTTPS.
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol], result)

    @builtins.property
    def protocol_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocolVersion]:
        '''The protocol version to use.

        :default: ApplicationProtocolVersion.HTTP1
        '''
        result = self._values.get("protocol_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocolVersion], result)

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[builtins.bool]:
        '''Determines whether the Load Balancer will be internet-facing.

        :default: true
        '''
        result = self._values.get("public_load_balancer")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def record_type(self) -> typing.Optional[ApplicationLoadBalancedServiceRecordType]:
        '''Specifies whether the Route53 record should be a CNAME, an A record using the Alias feature or no record at all.

        This is useful if you need to work with DNS systems that do not support alias records.

        :default: ApplicationLoadBalancedServiceRecordType.ALIAS
        '''
        result = self._values.get("record_type")
        return typing.cast(typing.Optional[ApplicationLoadBalancedServiceRecordType], result)

    @builtins.property
    def redirect_http(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether the load balancer should redirect traffic on port 80 to port 443 to support HTTP->HTTPS redirects This is only valid if the protocol of the ALB is HTTPS.

        :default: false
        '''
        result = self._values.get("redirect_http")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        :default: - CloudFormation-generated name.
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy]:
        '''The security policy that defines which ciphers and protocols are supported by the ALB Listener.

        :default: - The recommended elastic load balancing security policy
        '''
        result = self._values.get("ssl_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy], result)

    @builtins.property
    def target_protocol(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol]:
        '''The protocol for connections from the load balancer to the ECS tasks.

        The default target port is determined from the protocol (port 80 for
        HTTP, port 443 for HTTPS).

        :default: HTTP.
        '''
        result = self._values.get("target_protocol")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol], result)

    @builtins.property
    def task_image_options(
        self,
    ) -> typing.Optional[ApplicationLoadBalancedTaskImageOptions]:
        '''The properties required to create a new task definition.

        TaskDefinition or TaskImageOptions must be specified, but not both.

        :default: none
        '''
        result = self._values.get("task_image_options")
        return typing.cast(typing.Optional[ApplicationLoadBalancedTaskImageOptions], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        :default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        '''Determines whether the service will be assigned a public IP address.

        :default: false
        '''
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        :default: 256
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''The amount (in MiB) of memory used by the task.

        This field is required and you must use one of the following values, which determines your range of valid values
        for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)

        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)

        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)

        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)

        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        This default is set in the underlying FargateTaskDefinition construct.

        :default: 512
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def platform_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion]:
        '''The platform version on which to run your service.

        If one is not specified, the LATEST platform version is used by default. For more information, see
        `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_
        in the Amazon Elastic Container Service Developer Guide.

        :default: Latest
        '''
        result = self._values.get("platform_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]]:
        '''The security groups to associate with the service.

        If you do not specify a security group, a new security group is created.

        :default: - A new security group is created.
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]], result)

    @builtins.property
    def task_definition(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition]:
        '''The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both.

        [disable-awslint:ref-via-interface]

        :default: - none
        '''
        result = self._values.get("task_definition")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition], result)

    @builtins.property
    def task_subnets(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection]:
        '''The subnets to associate with the service.

        :default: - Public subnets if ``assignPublicIp`` is set, otherwise the first available one of Private, Isolated, Public, in that order.
        '''
        result = self._values.get("task_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationLoadBalancedFargateServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationMultipleTargetGroupsEc2Service(
    ApplicationMultipleTargetGroupsServiceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationMultipleTargetGroupsEc2Service",
):
    '''An EC2 service running on an ECS cluster fronted by an application load balancer.

    :exampleMetadata: infused

    Example::

        # One application load balancer with one listener and two target groups.
        # cluster: ecs.Cluster
        
        load_balanced_ec2_service = ecs_patterns.ApplicationMultipleTargetGroupsEc2Service(self, "Service",
            cluster=cluster,
            memory_limit_mi_b=256,
            task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageProps(
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
            ),
            target_groups=[ecsPatterns.ApplicationTargetProps(
                container_port=80
            ), ecsPatterns.ApplicationTargetProps(
                container_port=90,
                path_pattern="a/b/c",
                priority=10
            )
            ]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        memory_reservation_mib: typing.Optional[jsii.Number] = None,
        placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
        placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
        task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition] = None,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        load_balancers: typing.Optional[typing.Sequence[typing.Union[ApplicationLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        service_name: typing.Optional[builtins.str] = None,
        target_groups: typing.Optional[typing.Sequence[typing.Union[ApplicationTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''Constructs a new instance of the ApplicationMultipleTargetGroupsEc2Service class.

        :param scope: -
        :param id: -
        :param cpu: The minimum number of CPU units to reserve for the container. Valid values, which determines your range of valid values for the memory parameter: Default: - No minimum CPU units reserved.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Note that this setting will be ignored if TaskImagesOptions is specified Default: - No memory reserved.
        :param placement_constraints: The placement constraints to use for tasks in the service. For more information, see `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_. Default: - No constraints.
        :param placement_strategies: The placement strategies to use for tasks in the service. For more information, see `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_. Default: - No strategies.
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The application load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify ALB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55c4425c7e9d9279036389b147894a6689a30b2767b05d0dfe45895e24006667)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApplicationMultipleTargetGroupsEc2ServiceProps(
            cpu=cpu,
            memory_limit_mib=memory_limit_mib,
            memory_reservation_mib=memory_reservation_mib,
            placement_constraints=placement_constraints,
            placement_strategies=placement_strategies,
            task_definition=task_definition,
            cloud_map_options=cloud_map_options,
            cluster=cluster,
            desired_count=desired_count,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            health_check_grace_period=health_check_grace_period,
            load_balancers=load_balancers,
            propagate_tags=propagate_tags,
            service_name=service_name,
            target_groups=target_groups,
            task_image_options=task_image_options,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _aws_cdk_aws_ecs_7896c08f.Ec2Service:
        '''The EC2 service in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.Ec2Service, jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationTargetGroup:
        '''The default target group for the service.'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationTargetGroup, jsii.get(self, "targetGroup"))

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition:
        '''The EC2 Task Definition in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition, jsii.get(self, "taskDefinition"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationMultipleTargetGroupsEc2ServiceProps",
    jsii_struct_bases=[ApplicationMultipleTargetGroupsServiceBaseProps],
    name_mapping={
        "cloud_map_options": "cloudMapOptions",
        "cluster": "cluster",
        "desired_count": "desiredCount",
        "enable_ecs_managed_tags": "enableECSManagedTags",
        "health_check_grace_period": "healthCheckGracePeriod",
        "load_balancers": "loadBalancers",
        "propagate_tags": "propagateTags",
        "service_name": "serviceName",
        "target_groups": "targetGroups",
        "task_image_options": "taskImageOptions",
        "vpc": "vpc",
        "cpu": "cpu",
        "memory_limit_mib": "memoryLimitMiB",
        "memory_reservation_mib": "memoryReservationMiB",
        "placement_constraints": "placementConstraints",
        "placement_strategies": "placementStrategies",
        "task_definition": "taskDefinition",
    },
)
class ApplicationMultipleTargetGroupsEc2ServiceProps(
    ApplicationMultipleTargetGroupsServiceBaseProps,
):
    def __init__(
        self,
        *,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        load_balancers: typing.Optional[typing.Sequence[typing.Union[ApplicationLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        service_name: typing.Optional[builtins.str] = None,
        target_groups: typing.Optional[typing.Sequence[typing.Union[ApplicationTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        memory_reservation_mib: typing.Optional[jsii.Number] = None,
        placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
        placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
        task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition] = None,
    ) -> None:
        '''The properties for the ApplicationMultipleTargetGroupsEc2Service service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The application load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify ALB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param cpu: The minimum number of CPU units to reserve for the container. Valid values, which determines your range of valid values for the memory parameter: Default: - No minimum CPU units reserved.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Note that this setting will be ignored if TaskImagesOptions is specified Default: - No memory reserved.
        :param placement_constraints: The placement constraints to use for tasks in the service. For more information, see `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_. Default: - No constraints.
        :param placement_strategies: The placement strategies to use for tasks in the service. For more information, see `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_. Default: - No strategies.
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none

        :exampleMetadata: infused

        Example::

            # One application load balancer with one listener and two target groups.
            # cluster: ecs.Cluster
            
            load_balanced_ec2_service = ecs_patterns.ApplicationMultipleTargetGroupsEc2Service(self, "Service",
                cluster=cluster,
                memory_limit_mi_b=256,
                task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageProps(
                    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
                ),
                target_groups=[ecsPatterns.ApplicationTargetProps(
                    container_port=80
                ), ecsPatterns.ApplicationTargetProps(
                    container_port=90,
                    path_pattern="a/b/c",
                    priority=10
                )
                ]
            )
        '''
        if isinstance(cloud_map_options, dict):
            cloud_map_options = _aws_cdk_aws_ecs_7896c08f.CloudMapOptions(**cloud_map_options)
        if isinstance(task_image_options, dict):
            task_image_options = ApplicationLoadBalancedTaskImageProps(**task_image_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdf0345c737fd1a9b3f21e405848bfd932b8bf7caf70c5278f3921d45ef8ae93)
            check_type(argname="argument cloud_map_options", value=cloud_map_options, expected_type=type_hints["cloud_map_options"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument desired_count", value=desired_count, expected_type=type_hints["desired_count"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument health_check_grace_period", value=health_check_grace_period, expected_type=type_hints["health_check_grace_period"])
            check_type(argname="argument load_balancers", value=load_balancers, expected_type=type_hints["load_balancers"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument target_groups", value=target_groups, expected_type=type_hints["target_groups"])
            check_type(argname="argument task_image_options", value=task_image_options, expected_type=type_hints["task_image_options"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument memory_reservation_mib", value=memory_reservation_mib, expected_type=type_hints["memory_reservation_mib"])
            check_type(argname="argument placement_constraints", value=placement_constraints, expected_type=type_hints["placement_constraints"])
            check_type(argname="argument placement_strategies", value=placement_strategies, expected_type=type_hints["placement_strategies"])
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_map_options is not None:
            self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None:
            self._values["cluster"] = cluster
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None:
            self._values["health_check_grace_period"] = health_check_grace_period
        if load_balancers is not None:
            self._values["load_balancers"] = load_balancers
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if service_name is not None:
            self._values["service_name"] = service_name
        if target_groups is not None:
            self._values["target_groups"] = target_groups
        if task_image_options is not None:
            self._values["task_image_options"] = task_image_options
        if vpc is not None:
            self._values["vpc"] = vpc
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None:
            self._values["memory_reservation_mib"] = memory_reservation_mib
        if placement_constraints is not None:
            self._values["placement_constraints"] = placement_constraints
        if placement_strategies is not None:
            self._values["placement_strategies"] = placement_strategies
        if task_definition is not None:
            self._values["task_definition"] = task_definition

    @builtins.property
    def cloud_map_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions]:
        '''The options for configuring an Amazon ECS service to use service discovery.

        :default: - AWS Cloud Map service discovery is not enabled.
        '''
        result = self._values.get("cloud_map_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions], result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster]:
        '''The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster], result)

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        :default:

        - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1;
        if true, the default is 1 for all new services and uses the existing services desired count
        when updating an existing service.
        '''
        result = self._values.get("desired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        :default: false
        '''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def health_check_grace_period(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        '''
        result = self._values.get("health_check_grace_period")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def load_balancers(
        self,
    ) -> typing.Optional[typing.List[ApplicationLoadBalancerProps]]:
        '''The application load balancer that will serve traffic to the service.

        :default: - a new load balancer with a listener will be created.
        '''
        result = self._values.get("load_balancers")
        return typing.cast(typing.Optional[typing.List[ApplicationLoadBalancerProps]], result)

    @builtins.property
    def propagate_tags(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource]:
        '''Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        :default: - none
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        :default: - CloudFormation-generated name.
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List[ApplicationTargetProps]]:
        '''Properties to specify ALB target groups.

        :default: - default portMapping registered as target group and attached to the first defined listener
        '''
        result = self._values.get("target_groups")
        return typing.cast(typing.Optional[typing.List[ApplicationTargetProps]], result)

    @builtins.property
    def task_image_options(
        self,
    ) -> typing.Optional[ApplicationLoadBalancedTaskImageProps]:
        '''The properties required to create a new task definition.

        Only one of TaskDefinition or TaskImageOptions must be specified.

        :default: none
        '''
        result = self._values.get("task_image_options")
        return typing.cast(typing.Optional[ApplicationLoadBalancedTaskImageProps], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        :default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of CPU units to reserve for the container.

        Valid values, which determines your range of valid values for the memory parameter:

        :default: - No minimum CPU units reserved.
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''The amount (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        :default: - No memory limit.
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        '''The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under heavy contention, Docker attempts to keep the
        container memory to this soft limit. However, your container can consume more
        memory when it needs to, up to either the hard limit specified with the memory
        parameter (if applicable), or all of the available memory on the container
        instance, whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        Note that this setting will be ignored if TaskImagesOptions is specified

        :default: - No memory reserved.
        '''
        result = self._values.get("memory_reservation_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def placement_constraints(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]]:
        '''The placement constraints to use for tasks in the service.

        For more information, see
        `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_.

        :default: - No constraints.
        '''
        result = self._values.get("placement_constraints")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]], result)

    @builtins.property
    def placement_strategies(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]]:
        '''The placement strategies to use for tasks in the service.

        For more information, see
        `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_.

        :default: - No strategies.
        '''
        result = self._values.get("placement_strategies")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]], result)

    @builtins.property
    def task_definition(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition]:
        '''The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified.

        [disable-awslint:ref-via-interface]

        :default: - none
        '''
        result = self._values.get("task_definition")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationMultipleTargetGroupsEc2ServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationMultipleTargetGroupsFargateService(
    ApplicationMultipleTargetGroupsServiceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationMultipleTargetGroupsFargateService",
):
    '''A Fargate service running on an ECS cluster fronted by an application load balancer.

    :exampleMetadata: infused

    Example::

        # One application load balancer with one listener and two target groups.
        # cluster: ecs.Cluster
        
        load_balanced_fargate_service = ecs_patterns.ApplicationMultipleTargetGroupsFargateService(self, "Service",
            cluster=cluster,
            memory_limit_mi_b=1024,
            cpu=512,
            task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageProps(
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
            ),
            target_groups=[ecsPatterns.ApplicationTargetProps(
                container_port=80
            ), ecsPatterns.ApplicationTargetProps(
                container_port=90,
                path_pattern="a/b/c",
                priority=10
            )
            ]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
        task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition] = None,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        load_balancers: typing.Optional[typing.Sequence[typing.Union[ApplicationLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        service_name: typing.Optional[builtins.str] = None,
        target_groups: typing.Optional[typing.Sequence[typing.Union[ApplicationTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''Constructs a new instance of the ApplicationMultipleTargetGroupsFargateService class.

        :param scope: -
        :param id: -
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The application load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify ALB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79aa857fd1297986686754fafef1b42bfe6bfd00943a5aaa24d88b612e96d3fa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApplicationMultipleTargetGroupsFargateServiceProps(
            assign_public_ip=assign_public_ip,
            cpu=cpu,
            memory_limit_mib=memory_limit_mib,
            platform_version=platform_version,
            task_definition=task_definition,
            cloud_map_options=cloud_map_options,
            cluster=cluster,
            desired_count=desired_count,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            health_check_grace_period=health_check_grace_period,
            load_balancers=load_balancers,
            propagate_tags=propagate_tags,
            service_name=service_name,
            target_groups=target_groups,
            task_image_options=task_image_options,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> builtins.bool:
        '''Determines whether the service will be assigned a public IP address.'''
        return typing.cast(builtins.bool, jsii.get(self, "assignPublicIp"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _aws_cdk_aws_ecs_7896c08f.FargateService:
        '''The Fargate service in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.FargateService, jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationTargetGroup:
        '''The default target group for the service.'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationTargetGroup, jsii.get(self, "targetGroup"))

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition:
        '''The Fargate task definition in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition, jsii.get(self, "taskDefinition"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationMultipleTargetGroupsFargateServiceProps",
    jsii_struct_bases=[ApplicationMultipleTargetGroupsServiceBaseProps],
    name_mapping={
        "cloud_map_options": "cloudMapOptions",
        "cluster": "cluster",
        "desired_count": "desiredCount",
        "enable_ecs_managed_tags": "enableECSManagedTags",
        "health_check_grace_period": "healthCheckGracePeriod",
        "load_balancers": "loadBalancers",
        "propagate_tags": "propagateTags",
        "service_name": "serviceName",
        "target_groups": "targetGroups",
        "task_image_options": "taskImageOptions",
        "vpc": "vpc",
        "assign_public_ip": "assignPublicIp",
        "cpu": "cpu",
        "memory_limit_mib": "memoryLimitMiB",
        "platform_version": "platformVersion",
        "task_definition": "taskDefinition",
    },
)
class ApplicationMultipleTargetGroupsFargateServiceProps(
    ApplicationMultipleTargetGroupsServiceBaseProps,
):
    def __init__(
        self,
        *,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        load_balancers: typing.Optional[typing.Sequence[typing.Union[ApplicationLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        service_name: typing.Optional[builtins.str] = None,
        target_groups: typing.Optional[typing.Sequence[typing.Union[ApplicationTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
        task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition] = None,
    ) -> None:
        '''The properties for the ApplicationMultipleTargetGroupsFargateService service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The application load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify ALB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none

        :exampleMetadata: infused

        Example::

            # One application load balancer with one listener and two target groups.
            # cluster: ecs.Cluster
            
            load_balanced_fargate_service = ecs_patterns.ApplicationMultipleTargetGroupsFargateService(self, "Service",
                cluster=cluster,
                memory_limit_mi_b=1024,
                cpu=512,
                task_image_options=ecsPatterns.ApplicationLoadBalancedTaskImageProps(
                    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
                ),
                target_groups=[ecsPatterns.ApplicationTargetProps(
                    container_port=80
                ), ecsPatterns.ApplicationTargetProps(
                    container_port=90,
                    path_pattern="a/b/c",
                    priority=10
                )
                ]
            )
        '''
        if isinstance(cloud_map_options, dict):
            cloud_map_options = _aws_cdk_aws_ecs_7896c08f.CloudMapOptions(**cloud_map_options)
        if isinstance(task_image_options, dict):
            task_image_options = ApplicationLoadBalancedTaskImageProps(**task_image_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b6eb13e970c39657e8d031ba170122f99503d4f0f895eb40b5de7cf4b247490)
            check_type(argname="argument cloud_map_options", value=cloud_map_options, expected_type=type_hints["cloud_map_options"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument desired_count", value=desired_count, expected_type=type_hints["desired_count"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument health_check_grace_period", value=health_check_grace_period, expected_type=type_hints["health_check_grace_period"])
            check_type(argname="argument load_balancers", value=load_balancers, expected_type=type_hints["load_balancers"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument target_groups", value=target_groups, expected_type=type_hints["target_groups"])
            check_type(argname="argument task_image_options", value=task_image_options, expected_type=type_hints["task_image_options"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_map_options is not None:
            self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None:
            self._values["cluster"] = cluster
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None:
            self._values["health_check_grace_period"] = health_check_grace_period
        if load_balancers is not None:
            self._values["load_balancers"] = load_balancers
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if service_name is not None:
            self._values["service_name"] = service_name
        if target_groups is not None:
            self._values["target_groups"] = target_groups
        if task_image_options is not None:
            self._values["task_image_options"] = task_image_options
        if vpc is not None:
            self._values["vpc"] = vpc
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if platform_version is not None:
            self._values["platform_version"] = platform_version
        if task_definition is not None:
            self._values["task_definition"] = task_definition

    @builtins.property
    def cloud_map_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions]:
        '''The options for configuring an Amazon ECS service to use service discovery.

        :default: - AWS Cloud Map service discovery is not enabled.
        '''
        result = self._values.get("cloud_map_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions], result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster]:
        '''The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster], result)

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        :default:

        - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1;
        if true, the default is 1 for all new services and uses the existing services desired count
        when updating an existing service.
        '''
        result = self._values.get("desired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        :default: false
        '''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def health_check_grace_period(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        '''
        result = self._values.get("health_check_grace_period")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def load_balancers(
        self,
    ) -> typing.Optional[typing.List[ApplicationLoadBalancerProps]]:
        '''The application load balancer that will serve traffic to the service.

        :default: - a new load balancer with a listener will be created.
        '''
        result = self._values.get("load_balancers")
        return typing.cast(typing.Optional[typing.List[ApplicationLoadBalancerProps]], result)

    @builtins.property
    def propagate_tags(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource]:
        '''Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        :default: - none
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        :default: - CloudFormation-generated name.
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List[ApplicationTargetProps]]:
        '''Properties to specify ALB target groups.

        :default: - default portMapping registered as target group and attached to the first defined listener
        '''
        result = self._values.get("target_groups")
        return typing.cast(typing.Optional[typing.List[ApplicationTargetProps]], result)

    @builtins.property
    def task_image_options(
        self,
    ) -> typing.Optional[ApplicationLoadBalancedTaskImageProps]:
        '''The properties required to create a new task definition.

        Only one of TaskDefinition or TaskImageOptions must be specified.

        :default: none
        '''
        result = self._values.get("task_image_options")
        return typing.cast(typing.Optional[ApplicationLoadBalancedTaskImageProps], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        :default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        '''Determines whether the service will be assigned a public IP address.

        :default: false
        '''
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        :default: 256
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''The amount (in MiB) of memory used by the task.

        This field is required and you must use one of the following values, which determines your range of valid values
        for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)

        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)

        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)

        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)

        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        This default is set in the underlying FargateTaskDefinition construct.

        :default: 512
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def platform_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion]:
        '''The platform version on which to run your service.

        If one is not specified, the LATEST platform version is used by default. For more information, see
        `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_
        in the Amazon Elastic Container Service Developer Guide.

        :default: Latest
        '''
        result = self._values.get("platform_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion], result)

    @builtins.property
    def task_definition(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition]:
        '''The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified.

        [disable-awslint:ref-via-interface]

        :default: - none
        '''
        result = self._values.get("task_definition")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationMultipleTargetGroupsFargateServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkLoadBalancedEc2Service(
    NetworkLoadBalancedServiceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancedEc2Service",
):
    '''An EC2 service running on an ECS cluster fronted by a network load balancer.

    :exampleMetadata: infused

    Example::

        # cluster: ecs.Cluster
        
        load_balanced_ecs_service = ecs_patterns.NetworkLoadBalancedEc2Service(self, "Service",
            cluster=cluster,
            memory_limit_mi_b=1024,
            task_image_options=ecsPatterns.NetworkLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("test"),
                environment={
                    "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
                    "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
                }
            ),
            desired_count=2
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        memory_reservation_mib: typing.Optional[jsii.Number] = None,
        placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
        placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
        task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition] = None,
        circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        domain_name: typing.Optional[builtins.str] = None,
        domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancer] = None,
        max_healthy_percent: typing.Optional[jsii.Number] = None,
        min_healthy_percent: typing.Optional[jsii.Number] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        public_load_balancer: typing.Optional[builtins.bool] = None,
        record_type: typing.Optional[NetworkLoadBalancedServiceRecordType] = None,
        service_name: typing.Optional[builtins.str] = None,
        task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''Constructs a new instance of the NetworkLoadBalancedEc2Service class.

        :param scope: -
        :param id: -
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory reserved.
        :param placement_constraints: The placement constraints to use for tasks in the service. For more information, see `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_. Default: - No constraints.
        :param placement_strategies: The placement strategies to use for tasks in the service. For more information, see `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_. Default: - No strategies.
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both.. [disable-awslint:ref-via-interface] Default: - none
        :param circuit_breaker: Whether to enable the deployment circuit breaker. If this property is defined, circuit breaker will be implicitly enabled. Default: - disabled
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the network load balancer that will serve traffic to the service. Default: 80
        :param load_balancer: The network load balancer that will serve traffic to the service. If the load balancer has been imported, the vpc attribute must be specified in the call to fromNetworkLoadBalancerAttributes(). [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param record_type: Specifies whether the Route53 record should be a CNAME, an A record using the Alias feature or no record at all. This is useful if you need to work with DNS systems that do not support alias records. Default: NetworkLoadBalancedServiceRecordType.ALIAS
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. One of taskImageOptions or taskDefinition must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2b6979d35fe5bf1f0adf4ee8cfe57979c99a6da0307d75b8b0261cb95bc0f20)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NetworkLoadBalancedEc2ServiceProps(
            cpu=cpu,
            memory_limit_mib=memory_limit_mib,
            memory_reservation_mib=memory_reservation_mib,
            placement_constraints=placement_constraints,
            placement_strategies=placement_strategies,
            task_definition=task_definition,
            circuit_breaker=circuit_breaker,
            cloud_map_options=cloud_map_options,
            cluster=cluster,
            deployment_controller=deployment_controller,
            desired_count=desired_count,
            domain_name=domain_name,
            domain_zone=domain_zone,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            health_check_grace_period=health_check_grace_period,
            listener_port=listener_port,
            load_balancer=load_balancer,
            max_healthy_percent=max_healthy_percent,
            min_healthy_percent=min_healthy_percent,
            propagate_tags=propagate_tags,
            public_load_balancer=public_load_balancer,
            record_type=record_type,
            service_name=service_name,
            task_image_options=task_image_options,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _aws_cdk_aws_ecs_7896c08f.Ec2Service:
        '''The ECS service in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.Ec2Service, jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition:
        '''The EC2 Task Definition in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition, jsii.get(self, "taskDefinition"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancedEc2ServiceProps",
    jsii_struct_bases=[NetworkLoadBalancedServiceBaseProps],
    name_mapping={
        "circuit_breaker": "circuitBreaker",
        "cloud_map_options": "cloudMapOptions",
        "cluster": "cluster",
        "deployment_controller": "deploymentController",
        "desired_count": "desiredCount",
        "domain_name": "domainName",
        "domain_zone": "domainZone",
        "enable_ecs_managed_tags": "enableECSManagedTags",
        "health_check_grace_period": "healthCheckGracePeriod",
        "listener_port": "listenerPort",
        "load_balancer": "loadBalancer",
        "max_healthy_percent": "maxHealthyPercent",
        "min_healthy_percent": "minHealthyPercent",
        "propagate_tags": "propagateTags",
        "public_load_balancer": "publicLoadBalancer",
        "record_type": "recordType",
        "service_name": "serviceName",
        "task_image_options": "taskImageOptions",
        "vpc": "vpc",
        "cpu": "cpu",
        "memory_limit_mib": "memoryLimitMiB",
        "memory_reservation_mib": "memoryReservationMiB",
        "placement_constraints": "placementConstraints",
        "placement_strategies": "placementStrategies",
        "task_definition": "taskDefinition",
    },
)
class NetworkLoadBalancedEc2ServiceProps(NetworkLoadBalancedServiceBaseProps):
    def __init__(
        self,
        *,
        circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        domain_name: typing.Optional[builtins.str] = None,
        domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancer] = None,
        max_healthy_percent: typing.Optional[jsii.Number] = None,
        min_healthy_percent: typing.Optional[jsii.Number] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        public_load_balancer: typing.Optional[builtins.bool] = None,
        record_type: typing.Optional[NetworkLoadBalancedServiceRecordType] = None,
        service_name: typing.Optional[builtins.str] = None,
        task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        memory_reservation_mib: typing.Optional[jsii.Number] = None,
        placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
        placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
        task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition] = None,
    ) -> None:
        '''The properties for the NetworkLoadBalancedEc2Service service.

        :param circuit_breaker: Whether to enable the deployment circuit breaker. If this property is defined, circuit breaker will be implicitly enabled. Default: - disabled
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the network load balancer that will serve traffic to the service. Default: 80
        :param load_balancer: The network load balancer that will serve traffic to the service. If the load balancer has been imported, the vpc attribute must be specified in the call to fromNetworkLoadBalancerAttributes(). [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param record_type: Specifies whether the Route53 record should be a CNAME, an A record using the Alias feature or no record at all. This is useful if you need to work with DNS systems that do not support alias records. Default: NetworkLoadBalancedServiceRecordType.ALIAS
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. One of taskImageOptions or taskDefinition must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory reserved.
        :param placement_constraints: The placement constraints to use for tasks in the service. For more information, see `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_. Default: - No constraints.
        :param placement_strategies: The placement strategies to use for tasks in the service. For more information, see `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_. Default: - No strategies.
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both.. [disable-awslint:ref-via-interface] Default: - none

        :exampleMetadata: infused

        Example::

            # cluster: ecs.Cluster
            
            load_balanced_ecs_service = ecs_patterns.NetworkLoadBalancedEc2Service(self, "Service",
                cluster=cluster,
                memory_limit_mi_b=1024,
                task_image_options=ecsPatterns.NetworkLoadBalancedTaskImageOptions(
                    image=ecs.ContainerImage.from_registry("test"),
                    environment={
                        "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
                        "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
                    }
                ),
                desired_count=2
            )
        '''
        if isinstance(circuit_breaker, dict):
            circuit_breaker = _aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker(**circuit_breaker)
        if isinstance(cloud_map_options, dict):
            cloud_map_options = _aws_cdk_aws_ecs_7896c08f.CloudMapOptions(**cloud_map_options)
        if isinstance(deployment_controller, dict):
            deployment_controller = _aws_cdk_aws_ecs_7896c08f.DeploymentController(**deployment_controller)
        if isinstance(task_image_options, dict):
            task_image_options = NetworkLoadBalancedTaskImageOptions(**task_image_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b18c0352629253352bbe5f8fd1a8542c94d90cdd1b29f3ce374703aedd1996ba)
            check_type(argname="argument circuit_breaker", value=circuit_breaker, expected_type=type_hints["circuit_breaker"])
            check_type(argname="argument cloud_map_options", value=cloud_map_options, expected_type=type_hints["cloud_map_options"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument deployment_controller", value=deployment_controller, expected_type=type_hints["deployment_controller"])
            check_type(argname="argument desired_count", value=desired_count, expected_type=type_hints["desired_count"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_zone", value=domain_zone, expected_type=type_hints["domain_zone"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument health_check_grace_period", value=health_check_grace_period, expected_type=type_hints["health_check_grace_period"])
            check_type(argname="argument listener_port", value=listener_port, expected_type=type_hints["listener_port"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument max_healthy_percent", value=max_healthy_percent, expected_type=type_hints["max_healthy_percent"])
            check_type(argname="argument min_healthy_percent", value=min_healthy_percent, expected_type=type_hints["min_healthy_percent"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument public_load_balancer", value=public_load_balancer, expected_type=type_hints["public_load_balancer"])
            check_type(argname="argument record_type", value=record_type, expected_type=type_hints["record_type"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument task_image_options", value=task_image_options, expected_type=type_hints["task_image_options"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument memory_reservation_mib", value=memory_reservation_mib, expected_type=type_hints["memory_reservation_mib"])
            check_type(argname="argument placement_constraints", value=placement_constraints, expected_type=type_hints["placement_constraints"])
            check_type(argname="argument placement_strategies", value=placement_strategies, expected_type=type_hints["placement_strategies"])
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if circuit_breaker is not None:
            self._values["circuit_breaker"] = circuit_breaker
        if cloud_map_options is not None:
            self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None:
            self._values["cluster"] = cluster
        if deployment_controller is not None:
            self._values["deployment_controller"] = deployment_controller
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if domain_zone is not None:
            self._values["domain_zone"] = domain_zone
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None:
            self._values["health_check_grace_period"] = health_check_grace_period
        if listener_port is not None:
            self._values["listener_port"] = listener_port
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if max_healthy_percent is not None:
            self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None:
            self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if public_load_balancer is not None:
            self._values["public_load_balancer"] = public_load_balancer
        if record_type is not None:
            self._values["record_type"] = record_type
        if service_name is not None:
            self._values["service_name"] = service_name
        if task_image_options is not None:
            self._values["task_image_options"] = task_image_options
        if vpc is not None:
            self._values["vpc"] = vpc
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None:
            self._values["memory_reservation_mib"] = memory_reservation_mib
        if placement_constraints is not None:
            self._values["placement_constraints"] = placement_constraints
        if placement_strategies is not None:
            self._values["placement_strategies"] = placement_strategies
        if task_definition is not None:
            self._values["task_definition"] = task_definition

    @builtins.property
    def circuit_breaker(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker]:
        '''Whether to enable the deployment circuit breaker.

        If this property is defined, circuit breaker will be implicitly
        enabled.

        :default: - disabled
        '''
        result = self._values.get("circuit_breaker")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker], result)

    @builtins.property
    def cloud_map_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions]:
        '''The options for configuring an Amazon ECS service to use service discovery.

        :default: - AWS Cloud Map service discovery is not enabled.
        '''
        result = self._values.get("cloud_map_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions], result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster]:
        '''The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster], result)

    @builtins.property
    def deployment_controller(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentController]:
        '''Specifies which deployment controller to use for the service.

        For more information, see
        `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_

        :default: - Rolling update (ECS)
        '''
        result = self._values.get("deployment_controller")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentController], result)

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        :default:

        - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1;
        if true, the default is 1 for all new services and uses the existing services desired count
        when updating an existing service.
        '''
        result = self._values.get("desired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name for the service, e.g. "api.example.com.".

        :default: - No domain name.
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_zone(self) -> typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone]:
        '''The Route53 hosted zone for the domain, e.g. "example.com.".

        :default: - No Route53 hosted domain zone.
        '''
        result = self._values.get("domain_zone")
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone], result)

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        :default: false
        '''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def health_check_grace_period(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        '''
        result = self._values.get("health_check_grace_period")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        '''Listener port of the network load balancer that will serve traffic to the service.

        :default: 80
        '''
        result = self._values.get("listener_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def load_balancer(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancer]:
        '''The network load balancer that will serve traffic to the service.

        If the load balancer has been imported, the vpc attribute must be specified
        in the call to fromNetworkLoadBalancerAttributes().

        [disable-awslint:ref-via-interface]

        :default: - a new load balancer will be created.
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancer], result)

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        :default: - 100 if daemon, otherwise 200
        '''
        result = self._values.get("max_healthy_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        :default: - 0 if daemon, otherwise 50
        '''
        result = self._values.get("min_healthy_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def propagate_tags(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource]:
        '''Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        :default: - none
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource], result)

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[builtins.bool]:
        '''Determines whether the Load Balancer will be internet-facing.

        :default: true
        '''
        result = self._values.get("public_load_balancer")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def record_type(self) -> typing.Optional[NetworkLoadBalancedServiceRecordType]:
        '''Specifies whether the Route53 record should be a CNAME, an A record using the Alias feature or no record at all.

        This is useful if you need to work with DNS systems that do not support alias records.

        :default: NetworkLoadBalancedServiceRecordType.ALIAS
        '''
        result = self._values.get("record_type")
        return typing.cast(typing.Optional[NetworkLoadBalancedServiceRecordType], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        :default: - CloudFormation-generated name.
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def task_image_options(
        self,
    ) -> typing.Optional[NetworkLoadBalancedTaskImageOptions]:
        '''The properties required to create a new task definition.

        One of taskImageOptions or taskDefinition must be specified.

        :default: - none
        '''
        result = self._values.get("task_image_options")
        return typing.cast(typing.Optional[NetworkLoadBalancedTaskImageOptions], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        :default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        :default: none
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        :default: - No memory limit.
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        '''The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under contention, Docker attempts to keep the
        container memory within the limit. If the container requires more memory,
        it can consume up to the value specified by the Memory property or all of
        the available memory on the container instance—whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        :default: - No memory reserved.
        '''
        result = self._values.get("memory_reservation_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def placement_constraints(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]]:
        '''The placement constraints to use for tasks in the service.

        For more information, see
        `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_.

        :default: - No constraints.
        '''
        result = self._values.get("placement_constraints")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]], result)

    @builtins.property
    def placement_strategies(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]]:
        '''The placement strategies to use for tasks in the service.

        For more information, see
        `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_.

        :default: - No strategies.
        '''
        result = self._values.get("placement_strategies")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]], result)

    @builtins.property
    def task_definition(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition]:
        '''The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both..

        [disable-awslint:ref-via-interface]

        :default: - none
        '''
        result = self._values.get("task_definition")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkLoadBalancedEc2ServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkLoadBalancedFargateService(
    NetworkLoadBalancedServiceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancedFargateService",
):
    '''A Fargate service running on an ECS cluster fronted by a network load balancer.

    :exampleMetadata: infused

    Example::

        # cluster: ecs.Cluster
        
        load_balanced_fargate_service = ecs_patterns.NetworkLoadBalancedFargateService(self, "Service",
            cluster=cluster,
            memory_limit_mi_b=1024,
            cpu=512,
            task_image_options=ecsPatterns.NetworkLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
        task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition] = None,
        task_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        domain_name: typing.Optional[builtins.str] = None,
        domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancer] = None,
        max_healthy_percent: typing.Optional[jsii.Number] = None,
        min_healthy_percent: typing.Optional[jsii.Number] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        public_load_balancer: typing.Optional[builtins.bool] = None,
        record_type: typing.Optional[NetworkLoadBalancedServiceRecordType] = None,
        service_name: typing.Optional[builtins.str] = None,
        task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''Constructs a new instance of the NetworkLoadBalancedFargateService class.

        :param scope: -
        :param id: -
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both. [disable-awslint:ref-via-interface] Default: - none
        :param task_subnets: The subnets to associate with the service. Default: - Public subnets if ``assignPublicIp`` is set, otherwise the first available one of Private, Isolated, Public, in that order.
        :param circuit_breaker: Whether to enable the deployment circuit breaker. If this property is defined, circuit breaker will be implicitly enabled. Default: - disabled
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the network load balancer that will serve traffic to the service. Default: 80
        :param load_balancer: The network load balancer that will serve traffic to the service. If the load balancer has been imported, the vpc attribute must be specified in the call to fromNetworkLoadBalancerAttributes(). [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param record_type: Specifies whether the Route53 record should be a CNAME, an A record using the Alias feature or no record at all. This is useful if you need to work with DNS systems that do not support alias records. Default: NetworkLoadBalancedServiceRecordType.ALIAS
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. One of taskImageOptions or taskDefinition must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ffe0ada1d1350a9e5669c0a36d033f579dbbdbf615e781571262ab7dd179e2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NetworkLoadBalancedFargateServiceProps(
            assign_public_ip=assign_public_ip,
            cpu=cpu,
            memory_limit_mib=memory_limit_mib,
            platform_version=platform_version,
            task_definition=task_definition,
            task_subnets=task_subnets,
            circuit_breaker=circuit_breaker,
            cloud_map_options=cloud_map_options,
            cluster=cluster,
            deployment_controller=deployment_controller,
            desired_count=desired_count,
            domain_name=domain_name,
            domain_zone=domain_zone,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            health_check_grace_period=health_check_grace_period,
            listener_port=listener_port,
            load_balancer=load_balancer,
            max_healthy_percent=max_healthy_percent,
            min_healthy_percent=min_healthy_percent,
            propagate_tags=propagate_tags,
            public_load_balancer=public_load_balancer,
            record_type=record_type,
            service_name=service_name,
            task_image_options=task_image_options,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "assignPublicIp"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _aws_cdk_aws_ecs_7896c08f.FargateService:
        '''The Fargate service in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.FargateService, jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition:
        '''The Fargate task definition in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition, jsii.get(self, "taskDefinition"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancedFargateServiceProps",
    jsii_struct_bases=[NetworkLoadBalancedServiceBaseProps],
    name_mapping={
        "circuit_breaker": "circuitBreaker",
        "cloud_map_options": "cloudMapOptions",
        "cluster": "cluster",
        "deployment_controller": "deploymentController",
        "desired_count": "desiredCount",
        "domain_name": "domainName",
        "domain_zone": "domainZone",
        "enable_ecs_managed_tags": "enableECSManagedTags",
        "health_check_grace_period": "healthCheckGracePeriod",
        "listener_port": "listenerPort",
        "load_balancer": "loadBalancer",
        "max_healthy_percent": "maxHealthyPercent",
        "min_healthy_percent": "minHealthyPercent",
        "propagate_tags": "propagateTags",
        "public_load_balancer": "publicLoadBalancer",
        "record_type": "recordType",
        "service_name": "serviceName",
        "task_image_options": "taskImageOptions",
        "vpc": "vpc",
        "assign_public_ip": "assignPublicIp",
        "cpu": "cpu",
        "memory_limit_mib": "memoryLimitMiB",
        "platform_version": "platformVersion",
        "task_definition": "taskDefinition",
        "task_subnets": "taskSubnets",
    },
)
class NetworkLoadBalancedFargateServiceProps(NetworkLoadBalancedServiceBaseProps):
    def __init__(
        self,
        *,
        circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        domain_name: typing.Optional[builtins.str] = None,
        domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancer] = None,
        max_healthy_percent: typing.Optional[jsii.Number] = None,
        min_healthy_percent: typing.Optional[jsii.Number] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        public_load_balancer: typing.Optional[builtins.bool] = None,
        record_type: typing.Optional[NetworkLoadBalancedServiceRecordType] = None,
        service_name: typing.Optional[builtins.str] = None,
        task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
        task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition] = None,
        task_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''The properties for the NetworkLoadBalancedFargateService service.

        :param circuit_breaker: Whether to enable the deployment circuit breaker. If this property is defined, circuit breaker will be implicitly enabled. Default: - disabled
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the network load balancer that will serve traffic to the service. Default: 80
        :param load_balancer: The network load balancer that will serve traffic to the service. If the load balancer has been imported, the vpc attribute must be specified in the call to fromNetworkLoadBalancerAttributes(). [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param record_type: Specifies whether the Route53 record should be a CNAME, an A record using the Alias feature or no record at all. This is useful if you need to work with DNS systems that do not support alias records. Default: NetworkLoadBalancedServiceRecordType.ALIAS
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. One of taskImageOptions or taskDefinition must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both. [disable-awslint:ref-via-interface] Default: - none
        :param task_subnets: The subnets to associate with the service. Default: - Public subnets if ``assignPublicIp`` is set, otherwise the first available one of Private, Isolated, Public, in that order.

        :exampleMetadata: infused

        Example::

            # cluster: ecs.Cluster
            
            load_balanced_fargate_service = ecs_patterns.NetworkLoadBalancedFargateService(self, "Service",
                cluster=cluster,
                memory_limit_mi_b=1024,
                cpu=512,
                task_image_options=ecsPatterns.NetworkLoadBalancedTaskImageOptions(
                    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
                )
            )
        '''
        if isinstance(circuit_breaker, dict):
            circuit_breaker = _aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker(**circuit_breaker)
        if isinstance(cloud_map_options, dict):
            cloud_map_options = _aws_cdk_aws_ecs_7896c08f.CloudMapOptions(**cloud_map_options)
        if isinstance(deployment_controller, dict):
            deployment_controller = _aws_cdk_aws_ecs_7896c08f.DeploymentController(**deployment_controller)
        if isinstance(task_image_options, dict):
            task_image_options = NetworkLoadBalancedTaskImageOptions(**task_image_options)
        if isinstance(task_subnets, dict):
            task_subnets = _aws_cdk_aws_ec2_67de8e8d.SubnetSelection(**task_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8536b89b38ccdef3d903c70985e3b4f7fa640dbe49879d54df3cda15a9bab51)
            check_type(argname="argument circuit_breaker", value=circuit_breaker, expected_type=type_hints["circuit_breaker"])
            check_type(argname="argument cloud_map_options", value=cloud_map_options, expected_type=type_hints["cloud_map_options"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument deployment_controller", value=deployment_controller, expected_type=type_hints["deployment_controller"])
            check_type(argname="argument desired_count", value=desired_count, expected_type=type_hints["desired_count"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_zone", value=domain_zone, expected_type=type_hints["domain_zone"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument health_check_grace_period", value=health_check_grace_period, expected_type=type_hints["health_check_grace_period"])
            check_type(argname="argument listener_port", value=listener_port, expected_type=type_hints["listener_port"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument max_healthy_percent", value=max_healthy_percent, expected_type=type_hints["max_healthy_percent"])
            check_type(argname="argument min_healthy_percent", value=min_healthy_percent, expected_type=type_hints["min_healthy_percent"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument public_load_balancer", value=public_load_balancer, expected_type=type_hints["public_load_balancer"])
            check_type(argname="argument record_type", value=record_type, expected_type=type_hints["record_type"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument task_image_options", value=task_image_options, expected_type=type_hints["task_image_options"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
            check_type(argname="argument task_subnets", value=task_subnets, expected_type=type_hints["task_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if circuit_breaker is not None:
            self._values["circuit_breaker"] = circuit_breaker
        if cloud_map_options is not None:
            self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None:
            self._values["cluster"] = cluster
        if deployment_controller is not None:
            self._values["deployment_controller"] = deployment_controller
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if domain_zone is not None:
            self._values["domain_zone"] = domain_zone
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None:
            self._values["health_check_grace_period"] = health_check_grace_period
        if listener_port is not None:
            self._values["listener_port"] = listener_port
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if max_healthy_percent is not None:
            self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None:
            self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if public_load_balancer is not None:
            self._values["public_load_balancer"] = public_load_balancer
        if record_type is not None:
            self._values["record_type"] = record_type
        if service_name is not None:
            self._values["service_name"] = service_name
        if task_image_options is not None:
            self._values["task_image_options"] = task_image_options
        if vpc is not None:
            self._values["vpc"] = vpc
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if platform_version is not None:
            self._values["platform_version"] = platform_version
        if task_definition is not None:
            self._values["task_definition"] = task_definition
        if task_subnets is not None:
            self._values["task_subnets"] = task_subnets

    @builtins.property
    def circuit_breaker(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker]:
        '''Whether to enable the deployment circuit breaker.

        If this property is defined, circuit breaker will be implicitly
        enabled.

        :default: - disabled
        '''
        result = self._values.get("circuit_breaker")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker], result)

    @builtins.property
    def cloud_map_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions]:
        '''The options for configuring an Amazon ECS service to use service discovery.

        :default: - AWS Cloud Map service discovery is not enabled.
        '''
        result = self._values.get("cloud_map_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions], result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster]:
        '''The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster], result)

    @builtins.property
    def deployment_controller(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentController]:
        '''Specifies which deployment controller to use for the service.

        For more information, see
        `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_

        :default: - Rolling update (ECS)
        '''
        result = self._values.get("deployment_controller")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentController], result)

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        :default:

        - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1;
        if true, the default is 1 for all new services and uses the existing services desired count
        when updating an existing service.
        '''
        result = self._values.get("desired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name for the service, e.g. "api.example.com.".

        :default: - No domain name.
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_zone(self) -> typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone]:
        '''The Route53 hosted zone for the domain, e.g. "example.com.".

        :default: - No Route53 hosted domain zone.
        '''
        result = self._values.get("domain_zone")
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone], result)

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        :default: false
        '''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def health_check_grace_period(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        '''
        result = self._values.get("health_check_grace_period")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        '''Listener port of the network load balancer that will serve traffic to the service.

        :default: 80
        '''
        result = self._values.get("listener_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def load_balancer(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancer]:
        '''The network load balancer that will serve traffic to the service.

        If the load balancer has been imported, the vpc attribute must be specified
        in the call to fromNetworkLoadBalancerAttributes().

        [disable-awslint:ref-via-interface]

        :default: - a new load balancer will be created.
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancer], result)

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        :default: - 100 if daemon, otherwise 200
        '''
        result = self._values.get("max_healthy_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        :default: - 0 if daemon, otherwise 50
        '''
        result = self._values.get("min_healthy_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def propagate_tags(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource]:
        '''Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        :default: - none
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource], result)

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[builtins.bool]:
        '''Determines whether the Load Balancer will be internet-facing.

        :default: true
        '''
        result = self._values.get("public_load_balancer")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def record_type(self) -> typing.Optional[NetworkLoadBalancedServiceRecordType]:
        '''Specifies whether the Route53 record should be a CNAME, an A record using the Alias feature or no record at all.

        This is useful if you need to work with DNS systems that do not support alias records.

        :default: NetworkLoadBalancedServiceRecordType.ALIAS
        '''
        result = self._values.get("record_type")
        return typing.cast(typing.Optional[NetworkLoadBalancedServiceRecordType], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        :default: - CloudFormation-generated name.
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def task_image_options(
        self,
    ) -> typing.Optional[NetworkLoadBalancedTaskImageOptions]:
        '''The properties required to create a new task definition.

        One of taskImageOptions or taskDefinition must be specified.

        :default: - none
        '''
        result = self._values.get("task_image_options")
        return typing.cast(typing.Optional[NetworkLoadBalancedTaskImageOptions], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        :default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        '''Determines whether the service will be assigned a public IP address.

        :default: false
        '''
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        :default: 256
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''The amount (in MiB) of memory used by the task.

        This field is required and you must use one of the following values, which determines your range of valid values
        for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)

        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)

        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)

        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)

        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        This default is set in the underlying FargateTaskDefinition construct.

        :default: 512
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def platform_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion]:
        '''The platform version on which to run your service.

        If one is not specified, the LATEST platform version is used by default. For more information, see
        `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_
        in the Amazon Elastic Container Service Developer Guide.

        :default: Latest
        '''
        result = self._values.get("platform_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion], result)

    @builtins.property
    def task_definition(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition]:
        '''The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both.

        [disable-awslint:ref-via-interface]

        :default: - none
        '''
        result = self._values.get("task_definition")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition], result)

    @builtins.property
    def task_subnets(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection]:
        '''The subnets to associate with the service.

        :default: - Public subnets if ``assignPublicIp`` is set, otherwise the first available one of Private, Isolated, Public, in that order.
        '''
        result = self._values.get("task_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkLoadBalancedFargateServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkMultipleTargetGroupsEc2Service(
    NetworkMultipleTargetGroupsServiceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecs-patterns.NetworkMultipleTargetGroupsEc2Service",
):
    '''An EC2 service running on an ECS cluster fronted by a network load balancer.

    :exampleMetadata: infused

    Example::

        # Two network load balancers, each with their own listener and target group.
        # cluster: ecs.Cluster
        
        load_balanced_ec2_service = ecs_patterns.NetworkMultipleTargetGroupsEc2Service(self, "Service",
            cluster=cluster,
            memory_limit_mi_b=256,
            task_image_options=ecsPatterns.NetworkLoadBalancedTaskImageProps(
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
            ),
            load_balancers=[ecsPatterns.NetworkLoadBalancerProps(
                name="lb1",
                listeners=[ecsPatterns.NetworkListenerProps(
                    name="listener1"
                )
                ]
            ), ecsPatterns.NetworkLoadBalancerProps(
                name="lb2",
                listeners=[ecsPatterns.NetworkListenerProps(
                    name="listener2"
                )
                ]
            )
            ],
            target_groups=[ecsPatterns.NetworkTargetProps(
                container_port=80,
                listener="listener1"
            ), ecsPatterns.NetworkTargetProps(
                container_port=90,
                listener="listener2"
            )
            ]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        memory_reservation_mib: typing.Optional[jsii.Number] = None,
        placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
        placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
        task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition] = None,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        load_balancers: typing.Optional[typing.Sequence[typing.Union[NetworkLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        service_name: typing.Optional[builtins.str] = None,
        target_groups: typing.Optional[typing.Sequence[typing.Union[NetworkTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''Constructs a new instance of the NetworkMultipleTargetGroupsEc2Service class.

        :param scope: -
        :param id: -
        :param cpu: The minimum number of CPU units to reserve for the container. Valid values, which determines your range of valid values for the memory parameter: Default: - No minimum CPU units reserved.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Note that this setting will be ignored if TaskImagesOptions is specified. Default: - No memory reserved.
        :param placement_constraints: The placement constraints to use for tasks in the service. For more information, see `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_. Default: - No constraints.
        :param placement_strategies: The placement strategies to use for tasks in the service. For more information, see `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_. Default: - No strategies.
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The network load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: Name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify NLB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3415f6bc936d3b435e7f10ecb24842c31d4764541d2e445476c313ede26ee1de)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NetworkMultipleTargetGroupsEc2ServiceProps(
            cpu=cpu,
            memory_limit_mib=memory_limit_mib,
            memory_reservation_mib=memory_reservation_mib,
            placement_constraints=placement_constraints,
            placement_strategies=placement_strategies,
            task_definition=task_definition,
            cloud_map_options=cloud_map_options,
            cluster=cluster,
            desired_count=desired_count,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            health_check_grace_period=health_check_grace_period,
            load_balancers=load_balancers,
            propagate_tags=propagate_tags,
            service_name=service_name,
            target_groups=target_groups,
            task_image_options=task_image_options,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _aws_cdk_aws_ecs_7896c08f.Ec2Service:
        '''The EC2 service in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.Ec2Service, jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkTargetGroup:
        '''The default target group for the service.'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkTargetGroup, jsii.get(self, "targetGroup"))

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition:
        '''The EC2 Task Definition in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition, jsii.get(self, "taskDefinition"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.NetworkMultipleTargetGroupsEc2ServiceProps",
    jsii_struct_bases=[NetworkMultipleTargetGroupsServiceBaseProps],
    name_mapping={
        "cloud_map_options": "cloudMapOptions",
        "cluster": "cluster",
        "desired_count": "desiredCount",
        "enable_ecs_managed_tags": "enableECSManagedTags",
        "health_check_grace_period": "healthCheckGracePeriod",
        "load_balancers": "loadBalancers",
        "propagate_tags": "propagateTags",
        "service_name": "serviceName",
        "target_groups": "targetGroups",
        "task_image_options": "taskImageOptions",
        "vpc": "vpc",
        "cpu": "cpu",
        "memory_limit_mib": "memoryLimitMiB",
        "memory_reservation_mib": "memoryReservationMiB",
        "placement_constraints": "placementConstraints",
        "placement_strategies": "placementStrategies",
        "task_definition": "taskDefinition",
    },
)
class NetworkMultipleTargetGroupsEc2ServiceProps(
    NetworkMultipleTargetGroupsServiceBaseProps,
):
    def __init__(
        self,
        *,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        load_balancers: typing.Optional[typing.Sequence[typing.Union[NetworkLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        service_name: typing.Optional[builtins.str] = None,
        target_groups: typing.Optional[typing.Sequence[typing.Union[NetworkTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        memory_reservation_mib: typing.Optional[jsii.Number] = None,
        placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
        placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
        task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition] = None,
    ) -> None:
        '''The properties for the NetworkMultipleTargetGroupsEc2Service service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The network load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: Name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify NLB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param cpu: The minimum number of CPU units to reserve for the container. Valid values, which determines your range of valid values for the memory parameter: Default: - No minimum CPU units reserved.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Note that this setting will be ignored if TaskImagesOptions is specified. Default: - No memory reserved.
        :param placement_constraints: The placement constraints to use for tasks in the service. For more information, see `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_. Default: - No constraints.
        :param placement_strategies: The placement strategies to use for tasks in the service. For more information, see `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_. Default: - No strategies.
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none

        :exampleMetadata: infused

        Example::

            # Two network load balancers, each with their own listener and target group.
            # cluster: ecs.Cluster
            
            load_balanced_ec2_service = ecs_patterns.NetworkMultipleTargetGroupsEc2Service(self, "Service",
                cluster=cluster,
                memory_limit_mi_b=256,
                task_image_options=ecsPatterns.NetworkLoadBalancedTaskImageProps(
                    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
                ),
                load_balancers=[ecsPatterns.NetworkLoadBalancerProps(
                    name="lb1",
                    listeners=[ecsPatterns.NetworkListenerProps(
                        name="listener1"
                    )
                    ]
                ), ecsPatterns.NetworkLoadBalancerProps(
                    name="lb2",
                    listeners=[ecsPatterns.NetworkListenerProps(
                        name="listener2"
                    )
                    ]
                )
                ],
                target_groups=[ecsPatterns.NetworkTargetProps(
                    container_port=80,
                    listener="listener1"
                ), ecsPatterns.NetworkTargetProps(
                    container_port=90,
                    listener="listener2"
                )
                ]
            )
        '''
        if isinstance(cloud_map_options, dict):
            cloud_map_options = _aws_cdk_aws_ecs_7896c08f.CloudMapOptions(**cloud_map_options)
        if isinstance(task_image_options, dict):
            task_image_options = NetworkLoadBalancedTaskImageProps(**task_image_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beed0d34499b4616d384c73b6562321c4f68a8e97bb4f69884b297b233b61d2a)
            check_type(argname="argument cloud_map_options", value=cloud_map_options, expected_type=type_hints["cloud_map_options"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument desired_count", value=desired_count, expected_type=type_hints["desired_count"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument health_check_grace_period", value=health_check_grace_period, expected_type=type_hints["health_check_grace_period"])
            check_type(argname="argument load_balancers", value=load_balancers, expected_type=type_hints["load_balancers"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument target_groups", value=target_groups, expected_type=type_hints["target_groups"])
            check_type(argname="argument task_image_options", value=task_image_options, expected_type=type_hints["task_image_options"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument memory_reservation_mib", value=memory_reservation_mib, expected_type=type_hints["memory_reservation_mib"])
            check_type(argname="argument placement_constraints", value=placement_constraints, expected_type=type_hints["placement_constraints"])
            check_type(argname="argument placement_strategies", value=placement_strategies, expected_type=type_hints["placement_strategies"])
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_map_options is not None:
            self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None:
            self._values["cluster"] = cluster
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None:
            self._values["health_check_grace_period"] = health_check_grace_period
        if load_balancers is not None:
            self._values["load_balancers"] = load_balancers
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if service_name is not None:
            self._values["service_name"] = service_name
        if target_groups is not None:
            self._values["target_groups"] = target_groups
        if task_image_options is not None:
            self._values["task_image_options"] = task_image_options
        if vpc is not None:
            self._values["vpc"] = vpc
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None:
            self._values["memory_reservation_mib"] = memory_reservation_mib
        if placement_constraints is not None:
            self._values["placement_constraints"] = placement_constraints
        if placement_strategies is not None:
            self._values["placement_strategies"] = placement_strategies
        if task_definition is not None:
            self._values["task_definition"] = task_definition

    @builtins.property
    def cloud_map_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions]:
        '''The options for configuring an Amazon ECS service to use service discovery.

        :default: - AWS Cloud Map service discovery is not enabled.
        '''
        result = self._values.get("cloud_map_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions], result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster]:
        '''The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster], result)

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        :default:

        - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1;
        if true, the default is 1 for all new services and uses the existing services desired count
        when updating an existing service.
        '''
        result = self._values.get("desired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        :default: false
        '''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def health_check_grace_period(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        '''
        result = self._values.get("health_check_grace_period")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def load_balancers(self) -> typing.Optional[typing.List[NetworkLoadBalancerProps]]:
        '''The network load balancer that will serve traffic to the service.

        :default: - a new load balancer with a listener will be created.
        '''
        result = self._values.get("load_balancers")
        return typing.cast(typing.Optional[typing.List[NetworkLoadBalancerProps]], result)

    @builtins.property
    def propagate_tags(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource]:
        '''Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        :default: - none
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''Name of the service.

        :default: - CloudFormation-generated name.
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List[NetworkTargetProps]]:
        '''Properties to specify NLB target groups.

        :default: - default portMapping registered as target group and attached to the first defined listener
        '''
        result = self._values.get("target_groups")
        return typing.cast(typing.Optional[typing.List[NetworkTargetProps]], result)

    @builtins.property
    def task_image_options(self) -> typing.Optional[NetworkLoadBalancedTaskImageProps]:
        '''The properties required to create a new task definition.

        Only one of TaskDefinition or TaskImageOptions must be specified.

        :default: - none
        '''
        result = self._values.get("task_image_options")
        return typing.cast(typing.Optional[NetworkLoadBalancedTaskImageProps], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        :default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of CPU units to reserve for the container.

        Valid values, which determines your range of valid values for the memory parameter:

        :default: - No minimum CPU units reserved.
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''The amount (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        :default: - No memory limit.
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        '''The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under heavy contention, Docker attempts to keep the
        container memory to this soft limit. However, your container can consume more
        memory when it needs to, up to either the hard limit specified with the memory
        parameter (if applicable), or all of the available memory on the container
        instance, whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        Note that this setting will be ignored if TaskImagesOptions is specified.

        :default: - No memory reserved.
        '''
        result = self._values.get("memory_reservation_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def placement_constraints(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]]:
        '''The placement constraints to use for tasks in the service.

        For more information, see
        `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_.

        :default: - No constraints.
        '''
        result = self._values.get("placement_constraints")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]], result)

    @builtins.property
    def placement_strategies(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]]:
        '''The placement strategies to use for tasks in the service.

        For more information, see
        `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_.

        :default: - No strategies.
        '''
        result = self._values.get("placement_strategies")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]], result)

    @builtins.property
    def task_definition(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition]:
        '''The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified.

        [disable-awslint:ref-via-interface]

        :default: - none
        '''
        result = self._values.get("task_definition")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkMultipleTargetGroupsEc2ServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkMultipleTargetGroupsFargateService(
    NetworkMultipleTargetGroupsServiceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecs-patterns.NetworkMultipleTargetGroupsFargateService",
):
    '''A Fargate service running on an ECS cluster fronted by a network load balancer.

    :exampleMetadata: infused

    Example::

        # Two network load balancers, each with their own listener and target group.
        # cluster: ecs.Cluster
        
        load_balanced_fargate_service = ecs_patterns.NetworkMultipleTargetGroupsFargateService(self, "Service",
            cluster=cluster,
            memory_limit_mi_b=512,
            task_image_options=ecsPatterns.NetworkLoadBalancedTaskImageProps(
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
            ),
            load_balancers=[ecsPatterns.NetworkLoadBalancerProps(
                name="lb1",
                listeners=[ecsPatterns.NetworkListenerProps(
                    name="listener1"
                )
                ]
            ), ecsPatterns.NetworkLoadBalancerProps(
                name="lb2",
                listeners=[ecsPatterns.NetworkListenerProps(
                    name="listener2"
                )
                ]
            )
            ],
            target_groups=[ecsPatterns.NetworkTargetProps(
                container_port=80,
                listener="listener1"
            ), ecsPatterns.NetworkTargetProps(
                container_port=90,
                listener="listener2"
            )
            ]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
        task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition] = None,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        load_balancers: typing.Optional[typing.Sequence[typing.Union[NetworkLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        service_name: typing.Optional[builtins.str] = None,
        target_groups: typing.Optional[typing.Sequence[typing.Union[NetworkTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''Constructs a new instance of the NetworkMultipleTargetGroupsFargateService class.

        :param scope: -
        :param id: -
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The network load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: Name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify NLB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c051a8e5d0edc0e6798d0748cc001dec067b7d1d7b56b4a2cc1398cfb4ecaa20)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NetworkMultipleTargetGroupsFargateServiceProps(
            assign_public_ip=assign_public_ip,
            cpu=cpu,
            memory_limit_mib=memory_limit_mib,
            platform_version=platform_version,
            task_definition=task_definition,
            cloud_map_options=cloud_map_options,
            cluster=cluster,
            desired_count=desired_count,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            health_check_grace_period=health_check_grace_period,
            load_balancers=load_balancers,
            propagate_tags=propagate_tags,
            service_name=service_name,
            target_groups=target_groups,
            task_image_options=task_image_options,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> builtins.bool:
        '''Determines whether the service will be assigned a public IP address.'''
        return typing.cast(builtins.bool, jsii.get(self, "assignPublicIp"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _aws_cdk_aws_ecs_7896c08f.FargateService:
        '''The Fargate service in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.FargateService, jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkTargetGroup:
        '''The default target group for the service.'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkTargetGroup, jsii.get(self, "targetGroup"))

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition:
        '''The Fargate task definition in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition, jsii.get(self, "taskDefinition"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.NetworkMultipleTargetGroupsFargateServiceProps",
    jsii_struct_bases=[NetworkMultipleTargetGroupsServiceBaseProps],
    name_mapping={
        "cloud_map_options": "cloudMapOptions",
        "cluster": "cluster",
        "desired_count": "desiredCount",
        "enable_ecs_managed_tags": "enableECSManagedTags",
        "health_check_grace_period": "healthCheckGracePeriod",
        "load_balancers": "loadBalancers",
        "propagate_tags": "propagateTags",
        "service_name": "serviceName",
        "target_groups": "targetGroups",
        "task_image_options": "taskImageOptions",
        "vpc": "vpc",
        "assign_public_ip": "assignPublicIp",
        "cpu": "cpu",
        "memory_limit_mib": "memoryLimitMiB",
        "platform_version": "platformVersion",
        "task_definition": "taskDefinition",
    },
)
class NetworkMultipleTargetGroupsFargateServiceProps(
    NetworkMultipleTargetGroupsServiceBaseProps,
):
    def __init__(
        self,
        *,
        cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        load_balancers: typing.Optional[typing.Sequence[typing.Union[NetworkLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        service_name: typing.Optional[builtins.str] = None,
        target_groups: typing.Optional[typing.Sequence[typing.Union[NetworkTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
        task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
        task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition] = None,
    ) -> None:
        '''The properties for the NetworkMultipleTargetGroupsFargateService service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the default is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The network load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: Name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify NLB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none

        :exampleMetadata: infused

        Example::

            # Two network load balancers, each with their own listener and target group.
            # cluster: ecs.Cluster
            
            load_balanced_fargate_service = ecs_patterns.NetworkMultipleTargetGroupsFargateService(self, "Service",
                cluster=cluster,
                memory_limit_mi_b=512,
                task_image_options=ecsPatterns.NetworkLoadBalancedTaskImageProps(
                    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
                ),
                load_balancers=[ecsPatterns.NetworkLoadBalancerProps(
                    name="lb1",
                    listeners=[ecsPatterns.NetworkListenerProps(
                        name="listener1"
                    )
                    ]
                ), ecsPatterns.NetworkLoadBalancerProps(
                    name="lb2",
                    listeners=[ecsPatterns.NetworkListenerProps(
                        name="listener2"
                    )
                    ]
                )
                ],
                target_groups=[ecsPatterns.NetworkTargetProps(
                    container_port=80,
                    listener="listener1"
                ), ecsPatterns.NetworkTargetProps(
                    container_port=90,
                    listener="listener2"
                )
                ]
            )
        '''
        if isinstance(cloud_map_options, dict):
            cloud_map_options = _aws_cdk_aws_ecs_7896c08f.CloudMapOptions(**cloud_map_options)
        if isinstance(task_image_options, dict):
            task_image_options = NetworkLoadBalancedTaskImageProps(**task_image_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13a3c1bd8d9747565417a45ccb9268f395ff7db84f9efbeb74a205e4aa51ae12)
            check_type(argname="argument cloud_map_options", value=cloud_map_options, expected_type=type_hints["cloud_map_options"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument desired_count", value=desired_count, expected_type=type_hints["desired_count"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument health_check_grace_period", value=health_check_grace_period, expected_type=type_hints["health_check_grace_period"])
            check_type(argname="argument load_balancers", value=load_balancers, expected_type=type_hints["load_balancers"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument target_groups", value=target_groups, expected_type=type_hints["target_groups"])
            check_type(argname="argument task_image_options", value=task_image_options, expected_type=type_hints["task_image_options"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_map_options is not None:
            self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None:
            self._values["cluster"] = cluster
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None:
            self._values["health_check_grace_period"] = health_check_grace_period
        if load_balancers is not None:
            self._values["load_balancers"] = load_balancers
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if service_name is not None:
            self._values["service_name"] = service_name
        if target_groups is not None:
            self._values["target_groups"] = target_groups
        if task_image_options is not None:
            self._values["task_image_options"] = task_image_options
        if vpc is not None:
            self._values["vpc"] = vpc
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if platform_version is not None:
            self._values["platform_version"] = platform_version
        if task_definition is not None:
            self._values["task_definition"] = task_definition

    @builtins.property
    def cloud_map_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions]:
        '''The options for configuring an Amazon ECS service to use service discovery.

        :default: - AWS Cloud Map service discovery is not enabled.
        '''
        result = self._values.get("cloud_map_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions], result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster]:
        '''The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster], result)

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        :default:

        - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1;
        if true, the default is 1 for all new services and uses the existing services desired count
        when updating an existing service.
        '''
        result = self._values.get("desired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        :default: false
        '''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def health_check_grace_period(
        self,
    ) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        '''
        result = self._values.get("health_check_grace_period")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def load_balancers(self) -> typing.Optional[typing.List[NetworkLoadBalancerProps]]:
        '''The network load balancer that will serve traffic to the service.

        :default: - a new load balancer with a listener will be created.
        '''
        result = self._values.get("load_balancers")
        return typing.cast(typing.Optional[typing.List[NetworkLoadBalancerProps]], result)

    @builtins.property
    def propagate_tags(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource]:
        '''Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        :default: - none
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''Name of the service.

        :default: - CloudFormation-generated name.
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List[NetworkTargetProps]]:
        '''Properties to specify NLB target groups.

        :default: - default portMapping registered as target group and attached to the first defined listener
        '''
        result = self._values.get("target_groups")
        return typing.cast(typing.Optional[typing.List[NetworkTargetProps]], result)

    @builtins.property
    def task_image_options(self) -> typing.Optional[NetworkLoadBalancedTaskImageProps]:
        '''The properties required to create a new task definition.

        Only one of TaskDefinition or TaskImageOptions must be specified.

        :default: - none
        '''
        result = self._values.get("task_image_options")
        return typing.cast(typing.Optional[NetworkLoadBalancedTaskImageProps], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        :default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        '''Determines whether the service will be assigned a public IP address.

        :default: false
        '''
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        :default: 256
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''The amount (in MiB) of memory used by the task.

        This field is required and you must use one of the following values, which determines your range of valid values
        for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)

        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)

        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)

        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)

        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        This default is set in the underlying FargateTaskDefinition construct.

        :default: 512
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def platform_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion]:
        '''The platform version on which to run your service.

        If one is not specified, the LATEST platform version is used by default. For more information, see
        `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_
        in the Amazon Elastic Container Service Developer Guide.

        :default: Latest
        '''
        result = self._values.get("platform_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion], result)

    @builtins.property
    def task_definition(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition]:
        '''The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified.

        [disable-awslint:ref-via-interface]

        :default: - none
        '''
        result = self._values.get("task_definition")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkMultipleTargetGroupsFargateServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QueueProcessingEc2Service(
    QueueProcessingServiceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecs-patterns.QueueProcessingEc2Service",
):
    '''Class to create a queue processing EC2 service.

    :exampleMetadata: infused

    Example::

        # cluster: ecs.Cluster
        
        queue_processing_ec2_service = ecs_patterns.QueueProcessingEc2Service(self, "Service",
            cluster=cluster,
            memory_limit_mi_b=1024,
            image=ecs.ContainerImage.from_registry("test"),
            command=["-c", "4", "amazon.com"],
            enable_logging=False,
            desired_task_count=2,
            environment={
                "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
                "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
            },
            max_scaling_capacity=5,
            container_name="test"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        container_name: typing.Optional[builtins.str] = None,
        cpu: typing.Optional[jsii.Number] = None,
        gpu_count: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        memory_reservation_mib: typing.Optional[jsii.Number] = None,
        placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
        placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
        image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
        capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_7896c08f.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
        circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
        desired_task_count: typing.Optional[jsii.Number] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        family: typing.Optional[builtins.str] = None,
        log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
        max_healthy_percent: typing.Optional[jsii.Number] = None,
        max_receive_count: typing.Optional[jsii.Number] = None,
        max_scaling_capacity: typing.Optional[jsii.Number] = None,
        min_healthy_percent: typing.Optional[jsii.Number] = None,
        min_scaling_capacity: typing.Optional[jsii.Number] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        queue: typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue] = None,
        retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        scaling_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval, typing.Dict[builtins.str, typing.Any]]]] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
        service_name: typing.Optional[builtins.str] = None,
        visibility_timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''Constructs a new instance of the QueueProcessingEc2Service class.

        :param scope: -
        :param id: -
        :param container_name: Optional name for the container added. Default: - QueueProcessingContainer
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: none
        :param gpu_count: Gpu count for container in task definition. Set this if you want to use gpu based instances. Default: - No GPUs assigned.
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        :param placement_constraints: The placement constraints to use for tasks in the service. For more information, see `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_. Default: - No constraints.
        :param placement_strategies: The placement strategies to use for tasks in the service. For more information, see `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_. Default: - No strategies.
        :param image: The image used to start a container.
        :param capacity_provider_strategies: A list of Capacity Provider strategies used to place a service. Default: - undefined
        :param circuit_breaker: Whether to enable the deployment circuit breaker. If this property is defined, circuit breaker will be implicitly enabled. Default: - disabled
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_task_count: (deprecated) The desired number of instantiations of the task definition to keep running on the service. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the minScalingCapacity is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. The variable ``QUEUE_NAME`` with value ``queue.queueName`` will always be passed. Default: 'QUEUE_NAME: queue.queueName'
        :param family: The name of a family that the task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - default from underlying service.
        :param max_receive_count: The maximum number of times that a message can be received by consumers. When this value is exceeded for a message the message will be automatically sent to the Dead Letter Queue. Default: 3
        :param max_scaling_capacity: Maximum capacity to scale to. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is (desiredTaskCount * 2); if true, the default is 2.
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - default from underlying service.
        :param min_scaling_capacity: Minimum capacity to scale to. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is the desiredTaskCount; if true, the default is 1.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ Default: 'SQSQueue with CloudFormation-generated name'
        :param retention_period: The number of seconds that Dead Letter Queue retains a message. Default: Duration.days(14)
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. See `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_ Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param visibility_timeout: Timeout of processing a single message. After dequeuing, the processor has this much time to handle the message and delete it from the queue before it becomes visible again for dequeueing by another processor. Values must be between 0 and (12 hours). Default: Duration.seconds(30)
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e1e7cb058505452d49bf91b80b165103b2a7de8eb52b22c92299601eae89e7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = QueueProcessingEc2ServiceProps(
            container_name=container_name,
            cpu=cpu,
            gpu_count=gpu_count,
            memory_limit_mib=memory_limit_mib,
            memory_reservation_mib=memory_reservation_mib,
            placement_constraints=placement_constraints,
            placement_strategies=placement_strategies,
            image=image,
            capacity_provider_strategies=capacity_provider_strategies,
            circuit_breaker=circuit_breaker,
            cluster=cluster,
            command=command,
            deployment_controller=deployment_controller,
            desired_task_count=desired_task_count,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            enable_logging=enable_logging,
            environment=environment,
            family=family,
            log_driver=log_driver,
            max_healthy_percent=max_healthy_percent,
            max_receive_count=max_receive_count,
            max_scaling_capacity=max_scaling_capacity,
            min_healthy_percent=min_healthy_percent,
            min_scaling_capacity=min_scaling_capacity,
            propagate_tags=propagate_tags,
            queue=queue,
            retention_period=retention_period,
            scaling_steps=scaling_steps,
            secrets=secrets,
            service_name=service_name,
            visibility_timeout=visibility_timeout,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _aws_cdk_aws_ecs_7896c08f.Ec2Service:
        '''The EC2 service in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.Ec2Service, jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition:
        '''The EC2 task definition in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition, jsii.get(self, "taskDefinition"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.QueueProcessingEc2ServiceProps",
    jsii_struct_bases=[QueueProcessingServiceBaseProps],
    name_mapping={
        "image": "image",
        "capacity_provider_strategies": "capacityProviderStrategies",
        "circuit_breaker": "circuitBreaker",
        "cluster": "cluster",
        "command": "command",
        "deployment_controller": "deploymentController",
        "desired_task_count": "desiredTaskCount",
        "enable_ecs_managed_tags": "enableECSManagedTags",
        "enable_logging": "enableLogging",
        "environment": "environment",
        "family": "family",
        "log_driver": "logDriver",
        "max_healthy_percent": "maxHealthyPercent",
        "max_receive_count": "maxReceiveCount",
        "max_scaling_capacity": "maxScalingCapacity",
        "min_healthy_percent": "minHealthyPercent",
        "min_scaling_capacity": "minScalingCapacity",
        "propagate_tags": "propagateTags",
        "queue": "queue",
        "retention_period": "retentionPeriod",
        "scaling_steps": "scalingSteps",
        "secrets": "secrets",
        "service_name": "serviceName",
        "visibility_timeout": "visibilityTimeout",
        "vpc": "vpc",
        "container_name": "containerName",
        "cpu": "cpu",
        "gpu_count": "gpuCount",
        "memory_limit_mib": "memoryLimitMiB",
        "memory_reservation_mib": "memoryReservationMiB",
        "placement_constraints": "placementConstraints",
        "placement_strategies": "placementStrategies",
    },
)
class QueueProcessingEc2ServiceProps(QueueProcessingServiceBaseProps):
    def __init__(
        self,
        *,
        image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
        capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_7896c08f.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
        circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
        desired_task_count: typing.Optional[jsii.Number] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        family: typing.Optional[builtins.str] = None,
        log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
        max_healthy_percent: typing.Optional[jsii.Number] = None,
        max_receive_count: typing.Optional[jsii.Number] = None,
        max_scaling_capacity: typing.Optional[jsii.Number] = None,
        min_healthy_percent: typing.Optional[jsii.Number] = None,
        min_scaling_capacity: typing.Optional[jsii.Number] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        queue: typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue] = None,
        retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        scaling_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval, typing.Dict[builtins.str, typing.Any]]]] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
        service_name: typing.Optional[builtins.str] = None,
        visibility_timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
        container_name: typing.Optional[builtins.str] = None,
        cpu: typing.Optional[jsii.Number] = None,
        gpu_count: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        memory_reservation_mib: typing.Optional[jsii.Number] = None,
        placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
        placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
    ) -> None:
        '''The properties for the QueueProcessingEc2Service service.

        :param image: The image used to start a container.
        :param capacity_provider_strategies: A list of Capacity Provider strategies used to place a service. Default: - undefined
        :param circuit_breaker: Whether to enable the deployment circuit breaker. If this property is defined, circuit breaker will be implicitly enabled. Default: - disabled
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_task_count: (deprecated) The desired number of instantiations of the task definition to keep running on the service. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the minScalingCapacity is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. The variable ``QUEUE_NAME`` with value ``queue.queueName`` will always be passed. Default: 'QUEUE_NAME: queue.queueName'
        :param family: The name of a family that the task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - default from underlying service.
        :param max_receive_count: The maximum number of times that a message can be received by consumers. When this value is exceeded for a message the message will be automatically sent to the Dead Letter Queue. Default: 3
        :param max_scaling_capacity: Maximum capacity to scale to. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is (desiredTaskCount * 2); if true, the default is 2.
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - default from underlying service.
        :param min_scaling_capacity: Minimum capacity to scale to. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is the desiredTaskCount; if true, the default is 1.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ Default: 'SQSQueue with CloudFormation-generated name'
        :param retention_period: The number of seconds that Dead Letter Queue retains a message. Default: Duration.days(14)
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. See `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_ Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param visibility_timeout: Timeout of processing a single message. After dequeuing, the processor has this much time to handle the message and delete it from the queue before it becomes visible again for dequeueing by another processor. Values must be between 0 and (12 hours). Default: Duration.seconds(30)
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param container_name: Optional name for the container added. Default: - QueueProcessingContainer
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: none
        :param gpu_count: Gpu count for container in task definition. Set this if you want to use gpu based instances. Default: - No GPUs assigned.
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        :param placement_constraints: The placement constraints to use for tasks in the service. For more information, see `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_. Default: - No constraints.
        :param placement_strategies: The placement strategies to use for tasks in the service. For more information, see `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_. Default: - No strategies.

        :exampleMetadata: infused

        Example::

            # cluster: ecs.Cluster
            
            queue_processing_ec2_service = ecs_patterns.QueueProcessingEc2Service(self, "Service",
                cluster=cluster,
                memory_limit_mi_b=1024,
                image=ecs.ContainerImage.from_registry("test"),
                command=["-c", "4", "amazon.com"],
                enable_logging=False,
                desired_task_count=2,
                environment={
                    "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
                    "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
                },
                max_scaling_capacity=5,
                container_name="test"
            )
        '''
        if isinstance(circuit_breaker, dict):
            circuit_breaker = _aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker(**circuit_breaker)
        if isinstance(deployment_controller, dict):
            deployment_controller = _aws_cdk_aws_ecs_7896c08f.DeploymentController(**deployment_controller)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__796d722d4db4012290f080c5a0abe7b824b69f58f2eb31f1fc1b309cb98881fc)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument capacity_provider_strategies", value=capacity_provider_strategies, expected_type=type_hints["capacity_provider_strategies"])
            check_type(argname="argument circuit_breaker", value=circuit_breaker, expected_type=type_hints["circuit_breaker"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument deployment_controller", value=deployment_controller, expected_type=type_hints["deployment_controller"])
            check_type(argname="argument desired_task_count", value=desired_task_count, expected_type=type_hints["desired_task_count"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
            check_type(argname="argument log_driver", value=log_driver, expected_type=type_hints["log_driver"])
            check_type(argname="argument max_healthy_percent", value=max_healthy_percent, expected_type=type_hints["max_healthy_percent"])
            check_type(argname="argument max_receive_count", value=max_receive_count, expected_type=type_hints["max_receive_count"])
            check_type(argname="argument max_scaling_capacity", value=max_scaling_capacity, expected_type=type_hints["max_scaling_capacity"])
            check_type(argname="argument min_healthy_percent", value=min_healthy_percent, expected_type=type_hints["min_healthy_percent"])
            check_type(argname="argument min_scaling_capacity", value=min_scaling_capacity, expected_type=type_hints["min_scaling_capacity"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
            check_type(argname="argument scaling_steps", value=scaling_steps, expected_type=type_hints["scaling_steps"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument visibility_timeout", value=visibility_timeout, expected_type=type_hints["visibility_timeout"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument gpu_count", value=gpu_count, expected_type=type_hints["gpu_count"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument memory_reservation_mib", value=memory_reservation_mib, expected_type=type_hints["memory_reservation_mib"])
            check_type(argname="argument placement_constraints", value=placement_constraints, expected_type=type_hints["placement_constraints"])
            check_type(argname="argument placement_strategies", value=placement_strategies, expected_type=type_hints["placement_strategies"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if capacity_provider_strategies is not None:
            self._values["capacity_provider_strategies"] = capacity_provider_strategies
        if circuit_breaker is not None:
            self._values["circuit_breaker"] = circuit_breaker
        if cluster is not None:
            self._values["cluster"] = cluster
        if command is not None:
            self._values["command"] = command
        if deployment_controller is not None:
            self._values["deployment_controller"] = deployment_controller
        if desired_task_count is not None:
            self._values["desired_task_count"] = desired_task_count
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if environment is not None:
            self._values["environment"] = environment
        if family is not None:
            self._values["family"] = family
        if log_driver is not None:
            self._values["log_driver"] = log_driver
        if max_healthy_percent is not None:
            self._values["max_healthy_percent"] = max_healthy_percent
        if max_receive_count is not None:
            self._values["max_receive_count"] = max_receive_count
        if max_scaling_capacity is not None:
            self._values["max_scaling_capacity"] = max_scaling_capacity
        if min_healthy_percent is not None:
            self._values["min_healthy_percent"] = min_healthy_percent
        if min_scaling_capacity is not None:
            self._values["min_scaling_capacity"] = min_scaling_capacity
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if queue is not None:
            self._values["queue"] = queue
        if retention_period is not None:
            self._values["retention_period"] = retention_period
        if scaling_steps is not None:
            self._values["scaling_steps"] = scaling_steps
        if secrets is not None:
            self._values["secrets"] = secrets
        if service_name is not None:
            self._values["service_name"] = service_name
        if visibility_timeout is not None:
            self._values["visibility_timeout"] = visibility_timeout
        if vpc is not None:
            self._values["vpc"] = vpc
        if container_name is not None:
            self._values["container_name"] = container_name
        if cpu is not None:
            self._values["cpu"] = cpu
        if gpu_count is not None:
            self._values["gpu_count"] = gpu_count
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None:
            self._values["memory_reservation_mib"] = memory_reservation_mib
        if placement_constraints is not None:
            self._values["placement_constraints"] = placement_constraints
        if placement_strategies is not None:
            self._values["placement_strategies"] = placement_strategies

    @builtins.property
    def image(self) -> _aws_cdk_aws_ecs_7896c08f.ContainerImage:
        '''The image used to start a container.'''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.ContainerImage, result)

    @builtins.property
    def capacity_provider_strategies(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.CapacityProviderStrategy]]:
        '''A list of Capacity Provider strategies used to place a service.

        :default: - undefined
        '''
        result = self._values.get("capacity_provider_strategies")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.CapacityProviderStrategy]], result)

    @builtins.property
    def circuit_breaker(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker]:
        '''Whether to enable the deployment circuit breaker.

        If this property is defined, circuit breaker will be implicitly
        enabled.

        :default: - disabled
        '''
        result = self._values.get("circuit_breaker")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker], result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster]:
        '''The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        :default: - CMD value built into container image.
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deployment_controller(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentController]:
        '''Specifies which deployment controller to use for the service.

        For more information, see
        `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_

        :default: - Rolling update (ECS)
        '''
        result = self._values.get("deployment_controller")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentController], result)

    @builtins.property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) The desired number of instantiations of the task definition to keep running on the service.

        :default:

        - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1;
        if true, the minScalingCapacity is 1 for all new services and uses the existing services desired count
        when updating an existing service.

        :deprecated: - Use ``minScalingCapacity`` or a literal object instead.

        :stability: deprecated
        '''
        result = self._values.get("desired_task_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        :default: false
        '''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''Flag to indicate whether to enable logging.

        :default: true
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The environment variables to pass to the container.

        The variable ``QUEUE_NAME`` with value ``queue.queueName`` will
        always be passed.

        :default: 'QUEUE_NAME: queue.queueName'
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def family(self) -> typing.Optional[builtins.str]:
        '''The name of a family that the task definition is registered to.

        A family groups multiple versions of a task definition.

        :default: - Automatically generated name.
        '''
        result = self._values.get("family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_driver(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver]:
        '''The log driver to use.

        :default: - AwsLogDriver if enableLogging is true
        '''
        result = self._values.get("log_driver")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver], result)

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        :default: - default from underlying service.
        '''
        result = self._values.get("max_healthy_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_receive_count(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of times that a message can be received by consumers.

        When this value is exceeded for a message the message will be automatically sent to the Dead Letter Queue.

        :default: 3
        '''
        result = self._values.get("max_receive_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_scaling_capacity(self) -> typing.Optional[jsii.Number]:
        '''Maximum capacity to scale to.

        :default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is (desiredTaskCount * 2); if true, the default is 2.
        '''
        result = self._values.get("max_scaling_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        :default: - default from underlying service.
        '''
        result = self._values.get("min_healthy_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_scaling_capacity(self) -> typing.Optional[jsii.Number]:
        '''Minimum capacity to scale to.

        :default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is the desiredTaskCount; if true, the default is 1.
        '''
        result = self._values.get("min_scaling_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def propagate_tags(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource]:
        '''Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        :default: - none
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource], result)

    @builtins.property
    def queue(self) -> typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue]:
        '''A queue for which to process items from.

        If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See
        `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_

        :default: 'SQSQueue with CloudFormation-generated name'
        '''
        result = self._values.get("queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue], result)

    @builtins.property
    def retention_period(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The number of seconds that Dead Letter Queue retains a message.

        :default: Duration.days(14)
        '''
        result = self._values.get("retention_period")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def scaling_steps(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval]]:
        '''The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric.

        Maps a range of metric values to a particular scaling behavior. See
        `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_

        :default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        '''
        result = self._values.get("scaling_steps")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval]], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]]:
        '''The secret to expose to the container as an environment variable.

        :default: - No secret environment variables.
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        :default: - CloudFormation-generated name.
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def visibility_timeout(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''Timeout of processing a single message.

        After dequeuing, the processor has this much time to handle the message and delete it from the queue
        before it becomes visible again for dequeueing by another processor. Values must be between 0 and (12 hours).

        :default: Duration.seconds(30)
        '''
        result = self._values.get("visibility_timeout")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        :default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    @builtins.property
    def container_name(self) -> typing.Optional[builtins.str]:
        '''Optional name for the container added.

        :default: - QueueProcessingContainer
        '''
        result = self._values.get("container_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        :default: none
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def gpu_count(self) -> typing.Optional[jsii.Number]:
        '''Gpu count for container in task definition.

        Set this if you want to use gpu based instances.

        :default: - No GPUs assigned.
        '''
        result = self._values.get("gpu_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        :default: - No memory limit.
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        '''The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under contention, Docker attempts to keep the
        container memory within the limit. If the container requires more memory,
        it can consume up to the value specified by the Memory property or all of
        the available memory on the container instance—whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        :default: - No memory reserved.
        '''
        result = self._values.get("memory_reservation_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def placement_constraints(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]]:
        '''The placement constraints to use for tasks in the service.

        For more information, see
        `Amazon ECS Task Placement Constraints <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html>`_.

        :default: - No constraints.
        '''
        result = self._values.get("placement_constraints")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]], result)

    @builtins.property
    def placement_strategies(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]]:
        '''The placement strategies to use for tasks in the service.

        For more information, see
        `Amazon ECS Task Placement Strategies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html>`_.

        :default: - No strategies.
        '''
        result = self._values.get("placement_strategies")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QueueProcessingEc2ServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QueueProcessingFargateService(
    QueueProcessingServiceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecs-patterns.QueueProcessingFargateService",
):
    '''Class to create a queue processing Fargate service.

    :exampleMetadata: infused

    Example::

        # cluster: ecs.Cluster
        
        cluster.enable_fargate_capacity_providers()
        
        queue_processing_fargate_service = ecs_patterns.QueueProcessingFargateService(self, "Service",
            cluster=cluster,
            memory_limit_mi_b=512,
            image=ecs.ContainerImage.from_registry("test"),
            capacity_provider_strategies=[ecs.CapacityProviderStrategy(
                capacity_provider="FARGATE_SPOT",
                weight=2
            ), ecs.CapacityProviderStrategy(
                capacity_provider="FARGATE",
                weight=1
            )
            ]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        container_name: typing.Optional[builtins.str] = None,
        cpu: typing.Optional[jsii.Number] = None,
        health_check: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
        task_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
        capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_7896c08f.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
        circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
        desired_task_count: typing.Optional[jsii.Number] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        family: typing.Optional[builtins.str] = None,
        log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
        max_healthy_percent: typing.Optional[jsii.Number] = None,
        max_receive_count: typing.Optional[jsii.Number] = None,
        max_scaling_capacity: typing.Optional[jsii.Number] = None,
        min_healthy_percent: typing.Optional[jsii.Number] = None,
        min_scaling_capacity: typing.Optional[jsii.Number] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        queue: typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue] = None,
        retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        scaling_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval, typing.Dict[builtins.str, typing.Any]]]] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
        service_name: typing.Optional[builtins.str] = None,
        visibility_timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''Constructs a new instance of the QueueProcessingFargateService class.

        :param scope: -
        :param id: -
        :param assign_public_ip: Specifies whether the task's elastic network interface receives a public IP address. If true, each task will receive a public IP address. Default: false
        :param container_name: Optional name for the container added. Default: - QueueProcessingContainer
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param health_check: The health check command and associated configuration parameters for the container. Default: - Health check configuration from container.
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU) 1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU) 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU) Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU) Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param security_groups: The security groups to associate with the service. If you do not specify a security group, a new security group is created. Default: - A new security group is created.
        :param task_subnets: The subnets to associate with the service. Default: - Public subnets if ``assignPublicIp`` is set, otherwise the first available one of Private, Isolated, Public, in that order.
        :param image: The image used to start a container.
        :param capacity_provider_strategies: A list of Capacity Provider strategies used to place a service. Default: - undefined
        :param circuit_breaker: Whether to enable the deployment circuit breaker. If this property is defined, circuit breaker will be implicitly enabled. Default: - disabled
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_task_count: (deprecated) The desired number of instantiations of the task definition to keep running on the service. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the minScalingCapacity is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. The variable ``QUEUE_NAME`` with value ``queue.queueName`` will always be passed. Default: 'QUEUE_NAME: queue.queueName'
        :param family: The name of a family that the task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - default from underlying service.
        :param max_receive_count: The maximum number of times that a message can be received by consumers. When this value is exceeded for a message the message will be automatically sent to the Dead Letter Queue. Default: 3
        :param max_scaling_capacity: Maximum capacity to scale to. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is (desiredTaskCount * 2); if true, the default is 2.
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - default from underlying service.
        :param min_scaling_capacity: Minimum capacity to scale to. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is the desiredTaskCount; if true, the default is 1.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ Default: 'SQSQueue with CloudFormation-generated name'
        :param retention_period: The number of seconds that Dead Letter Queue retains a message. Default: Duration.days(14)
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. See `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_ Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param visibility_timeout: Timeout of processing a single message. After dequeuing, the processor has this much time to handle the message and delete it from the queue before it becomes visible again for dequeueing by another processor. Values must be between 0 and (12 hours). Default: Duration.seconds(30)
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eae27ad501ead113b2e31fc54240c9a38a6550f7bcccba1281149617f18bb58e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = QueueProcessingFargateServiceProps(
            assign_public_ip=assign_public_ip,
            container_name=container_name,
            cpu=cpu,
            health_check=health_check,
            memory_limit_mib=memory_limit_mib,
            platform_version=platform_version,
            security_groups=security_groups,
            task_subnets=task_subnets,
            image=image,
            capacity_provider_strategies=capacity_provider_strategies,
            circuit_breaker=circuit_breaker,
            cluster=cluster,
            command=command,
            deployment_controller=deployment_controller,
            desired_task_count=desired_task_count,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            enable_logging=enable_logging,
            environment=environment,
            family=family,
            log_driver=log_driver,
            max_healthy_percent=max_healthy_percent,
            max_receive_count=max_receive_count,
            max_scaling_capacity=max_scaling_capacity,
            min_healthy_percent=min_healthy_percent,
            min_scaling_capacity=min_scaling_capacity,
            propagate_tags=propagate_tags,
            queue=queue,
            retention_period=retention_period,
            scaling_steps=scaling_steps,
            secrets=secrets,
            service_name=service_name,
            visibility_timeout=visibility_timeout,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _aws_cdk_aws_ecs_7896c08f.FargateService:
        '''The Fargate service in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.FargateService, jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition:
        '''The Fargate task definition in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition, jsii.get(self, "taskDefinition"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.QueueProcessingFargateServiceProps",
    jsii_struct_bases=[QueueProcessingServiceBaseProps],
    name_mapping={
        "image": "image",
        "capacity_provider_strategies": "capacityProviderStrategies",
        "circuit_breaker": "circuitBreaker",
        "cluster": "cluster",
        "command": "command",
        "deployment_controller": "deploymentController",
        "desired_task_count": "desiredTaskCount",
        "enable_ecs_managed_tags": "enableECSManagedTags",
        "enable_logging": "enableLogging",
        "environment": "environment",
        "family": "family",
        "log_driver": "logDriver",
        "max_healthy_percent": "maxHealthyPercent",
        "max_receive_count": "maxReceiveCount",
        "max_scaling_capacity": "maxScalingCapacity",
        "min_healthy_percent": "minHealthyPercent",
        "min_scaling_capacity": "minScalingCapacity",
        "propagate_tags": "propagateTags",
        "queue": "queue",
        "retention_period": "retentionPeriod",
        "scaling_steps": "scalingSteps",
        "secrets": "secrets",
        "service_name": "serviceName",
        "visibility_timeout": "visibilityTimeout",
        "vpc": "vpc",
        "assign_public_ip": "assignPublicIp",
        "container_name": "containerName",
        "cpu": "cpu",
        "health_check": "healthCheck",
        "memory_limit_mib": "memoryLimitMiB",
        "platform_version": "platformVersion",
        "security_groups": "securityGroups",
        "task_subnets": "taskSubnets",
    },
)
class QueueProcessingFargateServiceProps(QueueProcessingServiceBaseProps):
    def __init__(
        self,
        *,
        image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
        capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_7896c08f.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
        circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
        desired_task_count: typing.Optional[jsii.Number] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        family: typing.Optional[builtins.str] = None,
        log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
        max_healthy_percent: typing.Optional[jsii.Number] = None,
        max_receive_count: typing.Optional[jsii.Number] = None,
        max_scaling_capacity: typing.Optional[jsii.Number] = None,
        min_healthy_percent: typing.Optional[jsii.Number] = None,
        min_scaling_capacity: typing.Optional[jsii.Number] = None,
        propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
        queue: typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue] = None,
        retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        scaling_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval, typing.Dict[builtins.str, typing.Any]]]] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
        service_name: typing.Optional[builtins.str] = None,
        visibility_timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        container_name: typing.Optional[builtins.str] = None,
        cpu: typing.Optional[jsii.Number] = None,
        health_check: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
        task_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''The properties for the QueueProcessingFargateService service.

        :param image: The image used to start a container.
        :param capacity_provider_strategies: A list of Capacity Provider strategies used to place a service. Default: - undefined
        :param circuit_breaker: Whether to enable the deployment circuit breaker. If this property is defined, circuit breaker will be implicitly enabled. Default: - disabled
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param deployment_controller: Specifies which deployment controller to use for the service. For more information, see `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_ Default: - Rolling update (ECS)
        :param desired_task_count: (deprecated) The desired number of instantiations of the task definition to keep running on the service. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1; if true, the minScalingCapacity is 1 for all new services and uses the existing services desired count when updating an existing service.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. The variable ``QUEUE_NAME`` with value ``queue.queueName`` will always be passed. Default: 'QUEUE_NAME: queue.queueName'
        :param family: The name of a family that the task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - default from underlying service.
        :param max_receive_count: The maximum number of times that a message can be received by consumers. When this value is exceeded for a message the message will be automatically sent to the Dead Letter Queue. Default: 3
        :param max_scaling_capacity: Maximum capacity to scale to. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is (desiredTaskCount * 2); if true, the default is 2.
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - default from underlying service.
        :param min_scaling_capacity: Minimum capacity to scale to. Default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is the desiredTaskCount; if true, the default is 1.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ Default: 'SQSQueue with CloudFormation-generated name'
        :param retention_period: The number of seconds that Dead Letter Queue retains a message. Default: Duration.days(14)
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. See `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_ Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param visibility_timeout: Timeout of processing a single message. After dequeuing, the processor has this much time to handle the message and delete it from the queue before it becomes visible again for dequeueing by another processor. Values must be between 0 and (12 hours). Default: Duration.seconds(30)
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param assign_public_ip: Specifies whether the task's elastic network interface receives a public IP address. If true, each task will receive a public IP address. Default: false
        :param container_name: Optional name for the container added. Default: - QueueProcessingContainer
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param health_check: The health check command and associated configuration parameters for the container. Default: - Health check configuration from container.
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU) 1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU) 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU) Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU) Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param security_groups: The security groups to associate with the service. If you do not specify a security group, a new security group is created. Default: - A new security group is created.
        :param task_subnets: The subnets to associate with the service. Default: - Public subnets if ``assignPublicIp`` is set, otherwise the first available one of Private, Isolated, Public, in that order.

        :exampleMetadata: infused

        Example::

            # cluster: ecs.Cluster
            
            cluster.enable_fargate_capacity_providers()
            
            queue_processing_fargate_service = ecs_patterns.QueueProcessingFargateService(self, "Service",
                cluster=cluster,
                memory_limit_mi_b=512,
                image=ecs.ContainerImage.from_registry("test"),
                capacity_provider_strategies=[ecs.CapacityProviderStrategy(
                    capacity_provider="FARGATE_SPOT",
                    weight=2
                ), ecs.CapacityProviderStrategy(
                    capacity_provider="FARGATE",
                    weight=1
                )
                ]
            )
        '''
        if isinstance(circuit_breaker, dict):
            circuit_breaker = _aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker(**circuit_breaker)
        if isinstance(deployment_controller, dict):
            deployment_controller = _aws_cdk_aws_ecs_7896c08f.DeploymentController(**deployment_controller)
        if isinstance(health_check, dict):
            health_check = _aws_cdk_aws_ecs_7896c08f.HealthCheck(**health_check)
        if isinstance(task_subnets, dict):
            task_subnets = _aws_cdk_aws_ec2_67de8e8d.SubnetSelection(**task_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2405bec3da832145d18db507a410fccdeaef352a66898fe0764108cfba5207a5)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument capacity_provider_strategies", value=capacity_provider_strategies, expected_type=type_hints["capacity_provider_strategies"])
            check_type(argname="argument circuit_breaker", value=circuit_breaker, expected_type=type_hints["circuit_breaker"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument deployment_controller", value=deployment_controller, expected_type=type_hints["deployment_controller"])
            check_type(argname="argument desired_task_count", value=desired_task_count, expected_type=type_hints["desired_task_count"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument family", value=family, expected_type=type_hints["family"])
            check_type(argname="argument log_driver", value=log_driver, expected_type=type_hints["log_driver"])
            check_type(argname="argument max_healthy_percent", value=max_healthy_percent, expected_type=type_hints["max_healthy_percent"])
            check_type(argname="argument max_receive_count", value=max_receive_count, expected_type=type_hints["max_receive_count"])
            check_type(argname="argument max_scaling_capacity", value=max_scaling_capacity, expected_type=type_hints["max_scaling_capacity"])
            check_type(argname="argument min_healthy_percent", value=min_healthy_percent, expected_type=type_hints["min_healthy_percent"])
            check_type(argname="argument min_scaling_capacity", value=min_scaling_capacity, expected_type=type_hints["min_scaling_capacity"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
            check_type(argname="argument scaling_steps", value=scaling_steps, expected_type=type_hints["scaling_steps"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument visibility_timeout", value=visibility_timeout, expected_type=type_hints["visibility_timeout"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument task_subnets", value=task_subnets, expected_type=type_hints["task_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if capacity_provider_strategies is not None:
            self._values["capacity_provider_strategies"] = capacity_provider_strategies
        if circuit_breaker is not None:
            self._values["circuit_breaker"] = circuit_breaker
        if cluster is not None:
            self._values["cluster"] = cluster
        if command is not None:
            self._values["command"] = command
        if deployment_controller is not None:
            self._values["deployment_controller"] = deployment_controller
        if desired_task_count is not None:
            self._values["desired_task_count"] = desired_task_count
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if environment is not None:
            self._values["environment"] = environment
        if family is not None:
            self._values["family"] = family
        if log_driver is not None:
            self._values["log_driver"] = log_driver
        if max_healthy_percent is not None:
            self._values["max_healthy_percent"] = max_healthy_percent
        if max_receive_count is not None:
            self._values["max_receive_count"] = max_receive_count
        if max_scaling_capacity is not None:
            self._values["max_scaling_capacity"] = max_scaling_capacity
        if min_healthy_percent is not None:
            self._values["min_healthy_percent"] = min_healthy_percent
        if min_scaling_capacity is not None:
            self._values["min_scaling_capacity"] = min_scaling_capacity
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if queue is not None:
            self._values["queue"] = queue
        if retention_period is not None:
            self._values["retention_period"] = retention_period
        if scaling_steps is not None:
            self._values["scaling_steps"] = scaling_steps
        if secrets is not None:
            self._values["secrets"] = secrets
        if service_name is not None:
            self._values["service_name"] = service_name
        if visibility_timeout is not None:
            self._values["visibility_timeout"] = visibility_timeout
        if vpc is not None:
            self._values["vpc"] = vpc
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if container_name is not None:
            self._values["container_name"] = container_name
        if cpu is not None:
            self._values["cpu"] = cpu
        if health_check is not None:
            self._values["health_check"] = health_check
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if platform_version is not None:
            self._values["platform_version"] = platform_version
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if task_subnets is not None:
            self._values["task_subnets"] = task_subnets

    @builtins.property
    def image(self) -> _aws_cdk_aws_ecs_7896c08f.ContainerImage:
        '''The image used to start a container.'''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.ContainerImage, result)

    @builtins.property
    def capacity_provider_strategies(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.CapacityProviderStrategy]]:
        '''A list of Capacity Provider strategies used to place a service.

        :default: - undefined
        '''
        result = self._values.get("capacity_provider_strategies")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.CapacityProviderStrategy]], result)

    @builtins.property
    def circuit_breaker(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker]:
        '''Whether to enable the deployment circuit breaker.

        If this property is defined, circuit breaker will be implicitly
        enabled.

        :default: - disabled
        '''
        result = self._values.get("circuit_breaker")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker], result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster]:
        '''The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        :default: - CMD value built into container image.
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deployment_controller(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentController]:
        '''Specifies which deployment controller to use for the service.

        For more information, see
        `Amazon ECS Deployment Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`_

        :default: - Rolling update (ECS)
        '''
        result = self._values.get("deployment_controller")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.DeploymentController], result)

    @builtins.property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) The desired number of instantiations of the task definition to keep running on the service.

        :default:

        - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is 1;
        if true, the minScalingCapacity is 1 for all new services and uses the existing services desired count
        when updating an existing service.

        :deprecated: - Use ``minScalingCapacity`` or a literal object instead.

        :stability: deprecated
        '''
        result = self._values.get("desired_task_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        :default: false
        '''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''Flag to indicate whether to enable logging.

        :default: true
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The environment variables to pass to the container.

        The variable ``QUEUE_NAME`` with value ``queue.queueName`` will
        always be passed.

        :default: 'QUEUE_NAME: queue.queueName'
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def family(self) -> typing.Optional[builtins.str]:
        '''The name of a family that the task definition is registered to.

        A family groups multiple versions of a task definition.

        :default: - Automatically generated name.
        '''
        result = self._values.get("family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_driver(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver]:
        '''The log driver to use.

        :default: - AwsLogDriver if enableLogging is true
        '''
        result = self._values.get("log_driver")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver], result)

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        :default: - default from underlying service.
        '''
        result = self._values.get("max_healthy_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_receive_count(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of times that a message can be received by consumers.

        When this value is exceeded for a message the message will be automatically sent to the Dead Letter Queue.

        :default: 3
        '''
        result = self._values.get("max_receive_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_scaling_capacity(self) -> typing.Optional[jsii.Number]:
        '''Maximum capacity to scale to.

        :default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is (desiredTaskCount * 2); if true, the default is 2.
        '''
        result = self._values.get("max_scaling_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        :default: - default from underlying service.
        '''
        result = self._values.get("min_healthy_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_scaling_capacity(self) -> typing.Optional[jsii.Number]:
        '''Minimum capacity to scale to.

        :default: - If the feature flag, ECS_REMOVE_DEFAULT_DESIRED_COUNT is false, the default is the desiredTaskCount; if true, the default is 1.
        '''
        result = self._values.get("min_scaling_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def propagate_tags(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource]:
        '''Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        :default: - none
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource], result)

    @builtins.property
    def queue(self) -> typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue]:
        '''A queue for which to process items from.

        If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See
        `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_

        :default: 'SQSQueue with CloudFormation-generated name'
        '''
        result = self._values.get("queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue], result)

    @builtins.property
    def retention_period(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The number of seconds that Dead Letter Queue retains a message.

        :default: Duration.days(14)
        '''
        result = self._values.get("retention_period")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def scaling_steps(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval]]:
        '''The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric.

        Maps a range of metric values to a particular scaling behavior. See
        `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_

        :default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        '''
        result = self._values.get("scaling_steps")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval]], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]]:
        '''The secret to expose to the container as an environment variable.

        :default: - No secret environment variables.
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        :default: - CloudFormation-generated name.
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def visibility_timeout(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''Timeout of processing a single message.

        After dequeuing, the processor has this much time to handle the message and delete it from the queue
        before it becomes visible again for dequeueing by another processor. Values must be between 0 and (12 hours).

        :default: Duration.seconds(30)
        '''
        result = self._values.get("visibility_timeout")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        :default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether the task's elastic network interface receives a public IP address.

        If true, each task will receive a public IP address.

        :default: false
        '''
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def container_name(self) -> typing.Optional[builtins.str]:
        '''Optional name for the container added.

        :default: - QueueProcessingContainer
        '''
        result = self._values.get("container_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        :default: 256
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.HealthCheck]:
        '''The health check command and associated configuration parameters for the container.

        :default: - Health check configuration from container.
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.HealthCheck], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''The amount (in MiB) of memory used by the task.

        This field is required and you must use one of the following values, which determines your range of valid values
        for the cpu parameter:

        0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU)

        1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU)

        2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU)

        Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU)

        Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU)

        This default is set in the underlying FargateTaskDefinition construct.

        :default: 512
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def platform_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion]:
        '''The platform version on which to run your service.

        If one is not specified, the LATEST platform version is used by default. For more information, see
        `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_
        in the Amazon Elastic Container Service Developer Guide.

        :default: Latest
        '''
        result = self._values.get("platform_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]]:
        '''The security groups to associate with the service.

        If you do not specify a security group, a new security group is created.

        :default: - A new security group is created.
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]], result)

    @builtins.property
    def task_subnets(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection]:
        '''The subnets to associate with the service.

        :default: - Public subnets if ``assignPublicIp`` is set, otherwise the first available one of Private, Isolated, Public, in that order.
        '''
        result = self._values.get("task_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QueueProcessingFargateServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ScheduledEc2Task(
    ScheduledTaskBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledEc2Task",
):
    '''A scheduled EC2 task that will be initiated off of CloudWatch Events.

    :exampleMetadata: infused

    Example::

        # Instantiate an Amazon EC2 Task to run at a scheduled interval
        # cluster: ecs.Cluster
        
        ecs_scheduled_task = ecs_patterns.ScheduledEc2Task(self, "ScheduledTask",
            cluster=cluster,
            scheduled_ec2_task_image_options=ecsPatterns.ScheduledEc2TaskImageOptions(
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                memory_limit_mi_b=256,
                environment={"name": "TRIGGER", "value": "CloudWatch Events"}
            ),
            schedule=appscaling.Schedule.expression("rate(1 minute)"),
            enabled=True,
            rule_name="sample-scheduled-task-rule"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        scheduled_ec2_task_definition_options: typing.Optional[typing.Union[ScheduledEc2TaskDefinitionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        scheduled_ec2_task_image_options: typing.Optional[typing.Union["ScheduledEc2TaskImageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: _aws_cdk_aws_applicationautoscaling_a31e8c21.Schedule,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        desired_task_count: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        rule_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''Constructs a new instance of the ScheduledEc2Task class.

        :param scope: -
        :param id: -
        :param scheduled_ec2_task_definition_options: The properties to define if using an existing TaskDefinition in this construct. ScheduledEc2TaskDefinitionOptions or ScheduledEc2TaskImageOptions must be defined, but not both. Default: none
        :param scheduled_ec2_task_image_options: The properties to define if the construct is to create a TaskDefinition. ScheduledEc2TaskDefinitionOptions or ScheduledEc2TaskImageOptions must be defined, but not both. Default: none
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch User Guide.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_.
        :param security_groups: Existing security groups to use for your service. Default: - a new security group will be created.
        :param subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3817049e832518f5bd5127d62c81691c6a48b7acecb0266bd5cdb237d76bf4b4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ScheduledEc2TaskProps(
            scheduled_ec2_task_definition_options=scheduled_ec2_task_definition_options,
            scheduled_ec2_task_image_options=scheduled_ec2_task_image_options,
            schedule=schedule,
            cluster=cluster,
            desired_task_count=desired_task_count,
            enabled=enabled,
            rule_name=rule_name,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="task")
    def task(self) -> _aws_cdk_aws_events_targets_3ef2ed32.EcsTask:
        '''The ECS task in this construct.'''
        return typing.cast(_aws_cdk_aws_events_targets_3ef2ed32.EcsTask, jsii.get(self, "task"))

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition:
        '''The EC2 task definition in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition, jsii.get(self, "taskDefinition"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledEc2TaskImageOptions",
    jsii_struct_bases=[ScheduledTaskImageProps],
    name_mapping={
        "image": "image",
        "command": "command",
        "environment": "environment",
        "log_driver": "logDriver",
        "secrets": "secrets",
        "cpu": "cpu",
        "memory_limit_mib": "memoryLimitMiB",
        "memory_reservation_mib": "memoryReservationMiB",
    },
)
class ScheduledEc2TaskImageOptions(ScheduledTaskImageProps):
    def __init__(
        self,
        *,
        image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        memory_reservation_mib: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''The properties for the ScheduledEc2Task using an image.

        :param image: The image used to start a container. Image or taskDefinition must be specified, but not both. Default: - none
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param environment: The environment variables to pass to the container. Default: none
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param cpu: The minimum number of CPU units to reserve for the container. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.

        :exampleMetadata: infused

        Example::

            # Instantiate an Amazon EC2 Task to run at a scheduled interval
            # cluster: ecs.Cluster
            
            ecs_scheduled_task = ecs_patterns.ScheduledEc2Task(self, "ScheduledTask",
                cluster=cluster,
                scheduled_ec2_task_image_options=ecsPatterns.ScheduledEc2TaskImageOptions(
                    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                    memory_limit_mi_b=256,
                    environment={"name": "TRIGGER", "value": "CloudWatch Events"}
                ),
                schedule=appscaling.Schedule.expression("rate(1 minute)"),
                enabled=True,
                rule_name="sample-scheduled-task-rule"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3036d3298f587a6fd28873f6e42fb1f608fbaa6e35e34304f14e46f9b7293490)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument log_driver", value=log_driver, expected_type=type_hints["log_driver"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument memory_reservation_mib", value=memory_reservation_mib, expected_type=type_hints["memory_reservation_mib"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if command is not None:
            self._values["command"] = command
        if environment is not None:
            self._values["environment"] = environment
        if log_driver is not None:
            self._values["log_driver"] = log_driver
        if secrets is not None:
            self._values["secrets"] = secrets
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None:
            self._values["memory_reservation_mib"] = memory_reservation_mib

    @builtins.property
    def image(self) -> _aws_cdk_aws_ecs_7896c08f.ContainerImage:
        '''The image used to start a container.

        Image or taskDefinition must be specified, but not both.

        :default: - none
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.ContainerImage, result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        :default: - CMD value built into container image.
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The environment variables to pass to the container.

        :default: none
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def log_driver(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver]:
        '''The log driver to use.

        :default: - AwsLogDriver if enableLogging is true
        '''
        result = self._values.get("log_driver")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]]:
        '''The secret to expose to the container as an environment variable.

        :default: - No secret environment variables.
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of CPU units to reserve for the container.

        :default: none
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        :default: - No memory limit.
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        '''The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under contention, Docker attempts to keep the
        container memory within the limit. If the container requires more memory,
        it can consume up to the value specified by the Memory property or all of
        the available memory on the container instance—whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        :default: - No memory reserved.
        '''
        result = self._values.get("memory_reservation_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduledEc2TaskImageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledEc2TaskProps",
    jsii_struct_bases=[ScheduledTaskBaseProps],
    name_mapping={
        "schedule": "schedule",
        "cluster": "cluster",
        "desired_task_count": "desiredTaskCount",
        "enabled": "enabled",
        "rule_name": "ruleName",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
        "scheduled_ec2_task_definition_options": "scheduledEc2TaskDefinitionOptions",
        "scheduled_ec2_task_image_options": "scheduledEc2TaskImageOptions",
    },
)
class ScheduledEc2TaskProps(ScheduledTaskBaseProps):
    def __init__(
        self,
        *,
        schedule: _aws_cdk_aws_applicationautoscaling_a31e8c21.Schedule,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        desired_task_count: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        rule_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
        scheduled_ec2_task_definition_options: typing.Optional[typing.Union[ScheduledEc2TaskDefinitionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        scheduled_ec2_task_image_options: typing.Optional[typing.Union[ScheduledEc2TaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''The properties for the ScheduledEc2Task task.

        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch User Guide.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_.
        :param security_groups: Existing security groups to use for your service. Default: - a new security group will be created.
        :param subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param scheduled_ec2_task_definition_options: The properties to define if using an existing TaskDefinition in this construct. ScheduledEc2TaskDefinitionOptions or ScheduledEc2TaskImageOptions must be defined, but not both. Default: none
        :param scheduled_ec2_task_image_options: The properties to define if the construct is to create a TaskDefinition. ScheduledEc2TaskDefinitionOptions or ScheduledEc2TaskImageOptions must be defined, but not both. Default: none

        :exampleMetadata: infused

        Example::

            # Instantiate an Amazon EC2 Task to run at a scheduled interval
            # cluster: ecs.Cluster
            
            ecs_scheduled_task = ecs_patterns.ScheduledEc2Task(self, "ScheduledTask",
                cluster=cluster,
                scheduled_ec2_task_image_options=ecsPatterns.ScheduledEc2TaskImageOptions(
                    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                    memory_limit_mi_b=256,
                    environment={"name": "TRIGGER", "value": "CloudWatch Events"}
                ),
                schedule=appscaling.Schedule.expression("rate(1 minute)"),
                enabled=True,
                rule_name="sample-scheduled-task-rule"
            )
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_67de8e8d.SubnetSelection(**subnet_selection)
        if isinstance(scheduled_ec2_task_definition_options, dict):
            scheduled_ec2_task_definition_options = ScheduledEc2TaskDefinitionOptions(**scheduled_ec2_task_definition_options)
        if isinstance(scheduled_ec2_task_image_options, dict):
            scheduled_ec2_task_image_options = ScheduledEc2TaskImageOptions(**scheduled_ec2_task_image_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87040b77ccdb852585e6341b4df755f8693a3d39ce8c872a1f36b424fbde2623)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument desired_task_count", value=desired_task_count, expected_type=type_hints["desired_task_count"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument scheduled_ec2_task_definition_options", value=scheduled_ec2_task_definition_options, expected_type=type_hints["scheduled_ec2_task_definition_options"])
            check_type(argname="argument scheduled_ec2_task_image_options", value=scheduled_ec2_task_image_options, expected_type=type_hints["scheduled_ec2_task_image_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedule": schedule,
        }
        if cluster is not None:
            self._values["cluster"] = cluster
        if desired_task_count is not None:
            self._values["desired_task_count"] = desired_task_count
        if enabled is not None:
            self._values["enabled"] = enabled
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc
        if scheduled_ec2_task_definition_options is not None:
            self._values["scheduled_ec2_task_definition_options"] = scheduled_ec2_task_definition_options
        if scheduled_ec2_task_image_options is not None:
            self._values["scheduled_ec2_task_image_options"] = scheduled_ec2_task_image_options

    @builtins.property
    def schedule(self) -> _aws_cdk_aws_applicationautoscaling_a31e8c21.Schedule:
        '''The schedule or rate (frequency) that determines when CloudWatch Events runs the rule.

        For more information, see
        `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_
        in the Amazon CloudWatch User Guide.
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(_aws_cdk_aws_applicationautoscaling_a31e8c21.Schedule, result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster]:
        '''The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster], result)

    @builtins.property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        :default: 1
        '''
        result = self._values.get("desired_task_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the rule is enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''A name for the rule.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
        for the rule name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_.
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]]:
        '''Existing security groups to use for your service.

        :default: - a new security group will be created.
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection]:
        '''In what subnets to place the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        :default: Private subnets
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        :default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    @builtins.property
    def scheduled_ec2_task_definition_options(
        self,
    ) -> typing.Optional[ScheduledEc2TaskDefinitionOptions]:
        '''The properties to define if using an existing TaskDefinition in this construct.

        ScheduledEc2TaskDefinitionOptions or ScheduledEc2TaskImageOptions must be defined, but not both.

        :default: none
        '''
        result = self._values.get("scheduled_ec2_task_definition_options")
        return typing.cast(typing.Optional[ScheduledEc2TaskDefinitionOptions], result)

    @builtins.property
    def scheduled_ec2_task_image_options(
        self,
    ) -> typing.Optional[ScheduledEc2TaskImageOptions]:
        '''The properties to define if the construct is to create a TaskDefinition.

        ScheduledEc2TaskDefinitionOptions or ScheduledEc2TaskImageOptions must be defined, but not both.

        :default: none
        '''
        result = self._values.get("scheduled_ec2_task_image_options")
        return typing.cast(typing.Optional[ScheduledEc2TaskImageOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduledEc2TaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ScheduledFargateTask(
    ScheduledTaskBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledFargateTask",
):
    '''A scheduled Fargate task that will be initiated off of CloudWatch Events.

    :exampleMetadata: infused

    Example::

        # cluster: ecs.Cluster
        
        scheduled_fargate_task = ecs_patterns.ScheduledFargateTask(self, "ScheduledFargateTask",
            cluster=cluster,
            scheduled_fargate_task_image_options=ecsPatterns.ScheduledFargateTaskImageOptions(
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                memory_limit_mi_b=512
            ),
            schedule=appscaling.Schedule.expression("rate(1 minute)"),
            platform_version=ecs.FargatePlatformVersion.LATEST
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
        scheduled_fargate_task_definition_options: typing.Optional[typing.Union[ScheduledFargateTaskDefinitionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        scheduled_fargate_task_image_options: typing.Optional[typing.Union["ScheduledFargateTaskImageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        schedule: _aws_cdk_aws_applicationautoscaling_a31e8c21.Schedule,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        desired_task_count: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        rule_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    ) -> None:
        '''Constructs a new instance of the ScheduledFargateTask class.

        :param scope: -
        :param id: -
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param scheduled_fargate_task_definition_options: The properties to define if using an existing TaskDefinition in this construct. ScheduledFargateTaskDefinitionOptions or ScheduledFargateTaskImageOptions must be defined, but not both. Default: none
        :param scheduled_fargate_task_image_options: The properties to define if the construct is to create a TaskDefinition. ScheduledFargateTaskDefinitionOptions or ScheduledFargateTaskImageOptions must be defined, but not both. Default: none
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch User Guide.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_.
        :param security_groups: Existing security groups to use for your service. Default: - a new security group will be created.
        :param subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7777d46bcff0542e36bf882a7f8299da8e737e62b4803d004040ae3eb073c948)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ScheduledFargateTaskProps(
            platform_version=platform_version,
            scheduled_fargate_task_definition_options=scheduled_fargate_task_definition_options,
            scheduled_fargate_task_image_options=scheduled_fargate_task_image_options,
            schedule=schedule,
            cluster=cluster,
            desired_task_count=desired_task_count,
            enabled=enabled,
            rule_name=rule_name,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="task")
    def task(self) -> _aws_cdk_aws_events_targets_3ef2ed32.EcsTask:
        '''The ECS task in this construct.'''
        return typing.cast(_aws_cdk_aws_events_targets_3ef2ed32.EcsTask, jsii.get(self, "task"))

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition:
        '''The Fargate task definition in this construct.'''
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition, jsii.get(self, "taskDefinition"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledFargateTaskImageOptions",
    jsii_struct_bases=[ScheduledTaskImageProps],
    name_mapping={
        "image": "image",
        "command": "command",
        "environment": "environment",
        "log_driver": "logDriver",
        "secrets": "secrets",
        "cpu": "cpu",
        "memory_limit_mib": "memoryLimitMiB",
    },
)
class ScheduledFargateTaskImageOptions(ScheduledTaskImageProps):
    def __init__(
        self,
        *,
        image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
        cpu: typing.Optional[jsii.Number] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''The properties for the ScheduledFargateTask using an image.

        :param image: The image used to start a container. Image or taskDefinition must be specified, but not both. Default: - none
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param environment: The environment variables to pass to the container. Default: none
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. Default: 512

        :exampleMetadata: infused

        Example::

            # cluster: ecs.Cluster
            
            scheduled_fargate_task = ecs_patterns.ScheduledFargateTask(self, "ScheduledFargateTask",
                cluster=cluster,
                scheduled_fargate_task_image_options=ecsPatterns.ScheduledFargateTaskImageOptions(
                    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                    memory_limit_mi_b=512
                ),
                schedule=appscaling.Schedule.expression("rate(1 minute)"),
                platform_version=ecs.FargatePlatformVersion.LATEST
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb8268eb5a0daeacc4062e594f78f0a94bdc0d71550fb39babfca1c3641fda81)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument log_driver", value=log_driver, expected_type=type_hints["log_driver"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if command is not None:
            self._values["command"] = command
        if environment is not None:
            self._values["environment"] = environment
        if log_driver is not None:
            self._values["log_driver"] = log_driver
        if secrets is not None:
            self._values["secrets"] = secrets
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib

    @builtins.property
    def image(self) -> _aws_cdk_aws_ecs_7896c08f.ContainerImage:
        '''The image used to start a container.

        Image or taskDefinition must be specified, but not both.

        :default: - none
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.ContainerImage, result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        :default: - CMD value built into container image.
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The environment variables to pass to the container.

        :default: none
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def log_driver(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver]:
        '''The log driver to use.

        :default: - AwsLogDriver if enableLogging is true
        '''
        result = self._values.get("log_driver")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]]:
        '''The secret to expose to the container as an environment variable.

        :default: - No secret environment variables.
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        :default: 256
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        :default: 512
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduledFargateTaskImageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledFargateTaskProps",
    jsii_struct_bases=[ScheduledTaskBaseProps],
    name_mapping={
        "schedule": "schedule",
        "cluster": "cluster",
        "desired_task_count": "desiredTaskCount",
        "enabled": "enabled",
        "rule_name": "ruleName",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
        "platform_version": "platformVersion",
        "scheduled_fargate_task_definition_options": "scheduledFargateTaskDefinitionOptions",
        "scheduled_fargate_task_image_options": "scheduledFargateTaskImageOptions",
    },
)
class ScheduledFargateTaskProps(ScheduledTaskBaseProps):
    def __init__(
        self,
        *,
        schedule: _aws_cdk_aws_applicationautoscaling_a31e8c21.Schedule,
        cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
        desired_task_count: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
        rule_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
        platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
        scheduled_fargate_task_definition_options: typing.Optional[typing.Union[ScheduledFargateTaskDefinitionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        scheduled_fargate_task_image_options: typing.Optional[typing.Union[ScheduledFargateTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''The properties for the ScheduledFargateTask task.

        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch User Guide.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_.
        :param security_groups: Existing security groups to use for your service. Default: - a new security group will be created.
        :param subnet_selection: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param platform_version: The platform version on which to run your service. If one is not specified, the LATEST platform version is used by default. For more information, see `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the Amazon Elastic Container Service Developer Guide. Default: Latest
        :param scheduled_fargate_task_definition_options: The properties to define if using an existing TaskDefinition in this construct. ScheduledFargateTaskDefinitionOptions or ScheduledFargateTaskImageOptions must be defined, but not both. Default: none
        :param scheduled_fargate_task_image_options: The properties to define if the construct is to create a TaskDefinition. ScheduledFargateTaskDefinitionOptions or ScheduledFargateTaskImageOptions must be defined, but not both. Default: none

        :exampleMetadata: infused

        Example::

            # cluster: ecs.Cluster
            
            scheduled_fargate_task = ecs_patterns.ScheduledFargateTask(self, "ScheduledFargateTask",
                cluster=cluster,
                scheduled_fargate_task_image_options=ecsPatterns.ScheduledFargateTaskImageOptions(
                    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                    memory_limit_mi_b=512
                ),
                schedule=appscaling.Schedule.expression("rate(1 minute)"),
                platform_version=ecs.FargatePlatformVersion.LATEST
            )
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_67de8e8d.SubnetSelection(**subnet_selection)
        if isinstance(scheduled_fargate_task_definition_options, dict):
            scheduled_fargate_task_definition_options = ScheduledFargateTaskDefinitionOptions(**scheduled_fargate_task_definition_options)
        if isinstance(scheduled_fargate_task_image_options, dict):
            scheduled_fargate_task_image_options = ScheduledFargateTaskImageOptions(**scheduled_fargate_task_image_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ca26da6b6e40a10dc1cf1d5fc45d59df83be836f2056705c1f7c1dbc1ea728)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument desired_task_count", value=desired_task_count, expected_type=type_hints["desired_task_count"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
            check_type(argname="argument scheduled_fargate_task_definition_options", value=scheduled_fargate_task_definition_options, expected_type=type_hints["scheduled_fargate_task_definition_options"])
            check_type(argname="argument scheduled_fargate_task_image_options", value=scheduled_fargate_task_image_options, expected_type=type_hints["scheduled_fargate_task_image_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedule": schedule,
        }
        if cluster is not None:
            self._values["cluster"] = cluster
        if desired_task_count is not None:
            self._values["desired_task_count"] = desired_task_count
        if enabled is not None:
            self._values["enabled"] = enabled
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc
        if platform_version is not None:
            self._values["platform_version"] = platform_version
        if scheduled_fargate_task_definition_options is not None:
            self._values["scheduled_fargate_task_definition_options"] = scheduled_fargate_task_definition_options
        if scheduled_fargate_task_image_options is not None:
            self._values["scheduled_fargate_task_image_options"] = scheduled_fargate_task_image_options

    @builtins.property
    def schedule(self) -> _aws_cdk_aws_applicationautoscaling_a31e8c21.Schedule:
        '''The schedule or rate (frequency) that determines when CloudWatch Events runs the rule.

        For more information, see
        `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_
        in the Amazon CloudWatch User Guide.
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(_aws_cdk_aws_applicationautoscaling_a31e8c21.Schedule, result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster]:
        '''The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster], result)

    @builtins.property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running on the service.

        :default: 1
        '''
        result = self._values.get("desired_task_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether the rule is enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''A name for the rule.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
        for the rule name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_.
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]]:
        '''Existing security groups to use for your service.

        :default: - a new security group will be created.
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection]:
        '''In what subnets to place the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        :default: Private subnets
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc]:
        '''The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        :default: - uses the VPC defined in the cluster or creates a new VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc], result)

    @builtins.property
    def platform_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion]:
        '''The platform version on which to run your service.

        If one is not specified, the LATEST platform version is used by default. For more information, see
        `AWS Fargate Platform Versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_
        in the Amazon Elastic Container Service Developer Guide.

        :default: Latest
        '''
        result = self._values.get("platform_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion], result)

    @builtins.property
    def scheduled_fargate_task_definition_options(
        self,
    ) -> typing.Optional[ScheduledFargateTaskDefinitionOptions]:
        '''The properties to define if using an existing TaskDefinition in this construct.

        ScheduledFargateTaskDefinitionOptions or ScheduledFargateTaskImageOptions must be defined, but not both.

        :default: none
        '''
        result = self._values.get("scheduled_fargate_task_definition_options")
        return typing.cast(typing.Optional[ScheduledFargateTaskDefinitionOptions], result)

    @builtins.property
    def scheduled_fargate_task_image_options(
        self,
    ) -> typing.Optional[ScheduledFargateTaskImageOptions]:
        '''The properties to define if the construct is to create a TaskDefinition.

        ScheduledFargateTaskDefinitionOptions or ScheduledFargateTaskImageOptions must be defined, but not both.

        :default: none
        '''
        result = self._values.get("scheduled_fargate_task_image_options")
        return typing.cast(typing.Optional[ScheduledFargateTaskImageOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduledFargateTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ApplicationListenerProps",
    "ApplicationLoadBalancedEc2Service",
    "ApplicationLoadBalancedEc2ServiceProps",
    "ApplicationLoadBalancedFargateService",
    "ApplicationLoadBalancedFargateServiceProps",
    "ApplicationLoadBalancedServiceBase",
    "ApplicationLoadBalancedServiceBaseProps",
    "ApplicationLoadBalancedServiceRecordType",
    "ApplicationLoadBalancedTaskImageOptions",
    "ApplicationLoadBalancedTaskImageProps",
    "ApplicationLoadBalancerProps",
    "ApplicationMultipleTargetGroupsEc2Service",
    "ApplicationMultipleTargetGroupsEc2ServiceProps",
    "ApplicationMultipleTargetGroupsFargateService",
    "ApplicationMultipleTargetGroupsFargateServiceProps",
    "ApplicationMultipleTargetGroupsServiceBase",
    "ApplicationMultipleTargetGroupsServiceBaseProps",
    "ApplicationTargetProps",
    "NetworkListenerProps",
    "NetworkLoadBalancedEc2Service",
    "NetworkLoadBalancedEc2ServiceProps",
    "NetworkLoadBalancedFargateService",
    "NetworkLoadBalancedFargateServiceProps",
    "NetworkLoadBalancedServiceBase",
    "NetworkLoadBalancedServiceBaseProps",
    "NetworkLoadBalancedServiceRecordType",
    "NetworkLoadBalancedTaskImageOptions",
    "NetworkLoadBalancedTaskImageProps",
    "NetworkLoadBalancerProps",
    "NetworkMultipleTargetGroupsEc2Service",
    "NetworkMultipleTargetGroupsEc2ServiceProps",
    "NetworkMultipleTargetGroupsFargateService",
    "NetworkMultipleTargetGroupsFargateServiceProps",
    "NetworkMultipleTargetGroupsServiceBase",
    "NetworkMultipleTargetGroupsServiceBaseProps",
    "NetworkTargetProps",
    "QueueProcessingEc2Service",
    "QueueProcessingEc2ServiceProps",
    "QueueProcessingFargateService",
    "QueueProcessingFargateServiceProps",
    "QueueProcessingServiceBase",
    "QueueProcessingServiceBaseProps",
    "ScheduledEc2Task",
    "ScheduledEc2TaskDefinitionOptions",
    "ScheduledEc2TaskImageOptions",
    "ScheduledEc2TaskProps",
    "ScheduledFargateTask",
    "ScheduledFargateTaskDefinitionOptions",
    "ScheduledFargateTaskImageOptions",
    "ScheduledFargateTaskProps",
    "ScheduledTaskBase",
    "ScheduledTaskBaseProps",
    "ScheduledTaskImageProps",
]

publication.publish()

def _typecheckingstub__f3067da453bdfb236a42f515dab378ee9078b61fce8e228bb295ecf85de24514(
    *,
    name: builtins.str,
    certificate: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
    ssl_policy: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64cef0537f934abf500aadc14d96bae4ddd374777926a6b04a5e374daa372fda(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    certificate: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate] = None,
    circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    domain_name: typing.Optional[builtins.str] = None,
    domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    listener_port: typing.Optional[jsii.Number] = None,
    load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancer] = None,
    load_balancer_name: typing.Optional[builtins.str] = None,
    max_healthy_percent: typing.Optional[jsii.Number] = None,
    min_healthy_percent: typing.Optional[jsii.Number] = None,
    open_listener: typing.Optional[builtins.bool] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
    protocol_version: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocolVersion] = None,
    public_load_balancer: typing.Optional[builtins.bool] = None,
    record_type: typing.Optional[ApplicationLoadBalancedServiceRecordType] = None,
    redirect_http: typing.Optional[builtins.bool] = None,
    service_name: typing.Optional[builtins.str] = None,
    ssl_policy: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy] = None,
    target_protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
    task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee3ce64b0c866a07372c9c74a1d3165d4d06d3f390dbbf6a5e955e28357b0d9(
    service: _aws_cdk_aws_ecs_7896c08f.BaseService,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a5807f3882c0013e0b55ecf11dcbbb3a972022f6139ffd9b66ce12d97a835b(
    prefix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50622e2557761392d3a1274f54e1282c365b271f31b99b698414a01b363c0bc0(
    scope: _aws_cdk_core_f4b25747.Construct,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82f51600f49a1d66311d7d86addbe41bd436f95507e2f35c0462edfcefb6fed(
    *,
    certificate: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate] = None,
    circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    domain_name: typing.Optional[builtins.str] = None,
    domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    listener_port: typing.Optional[jsii.Number] = None,
    load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancer] = None,
    load_balancer_name: typing.Optional[builtins.str] = None,
    max_healthy_percent: typing.Optional[jsii.Number] = None,
    min_healthy_percent: typing.Optional[jsii.Number] = None,
    open_listener: typing.Optional[builtins.bool] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
    protocol_version: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocolVersion] = None,
    public_load_balancer: typing.Optional[builtins.bool] = None,
    record_type: typing.Optional[ApplicationLoadBalancedServiceRecordType] = None,
    redirect_http: typing.Optional[builtins.bool] = None,
    service_name: typing.Optional[builtins.str] = None,
    ssl_policy: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy] = None,
    target_protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
    task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05aaf3feaac7e0a061b38a68c16d0b8804ffb202f7905eb0929220547635e0da(
    *,
    image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
    container_name: typing.Optional[builtins.str] = None,
    container_port: typing.Optional[jsii.Number] = None,
    docker_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    execution_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    family: typing.Optional[builtins.str] = None,
    log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
    task_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c36449e1f00ba60ffc4a815353a98eb5ffcbe30826d188158a6da9d2c203a51(
    *,
    image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
    container_name: typing.Optional[builtins.str] = None,
    container_ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
    docker_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    execution_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    family: typing.Optional[builtins.str] = None,
    log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
    task_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c36e9ce37de9abe32e03123541059975748aa637bdc219b9dd4b048003c55f3a(
    *,
    listeners: typing.Sequence[typing.Union[ApplicationListenerProps, typing.Dict[builtins.str, typing.Any]]],
    name: builtins.str,
    domain_name: typing.Optional[builtins.str] = None,
    domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
    public_load_balancer: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3564cc867433df94aab33ec6839a667de0e7a111caa89a666dbd8bf94880b88(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    load_balancers: typing.Optional[typing.Sequence[typing.Union[ApplicationLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    service_name: typing.Optional[builtins.str] = None,
    target_groups: typing.Optional[typing.Sequence[typing.Union[ApplicationTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39fdfd284662cd903359ba08362455d0a225b3aebfc5fd421c22301bafb4653(
    container: _aws_cdk_aws_ecs_7896c08f.ContainerDefinition,
    targets: typing.Sequence[typing.Union[ApplicationTargetProps, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e54df5373c25b4b95c91584003b8158e5ecbaba3ca5e44f3186ac69a12f3c3(
    prefix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947f8ee5f4b0dca3f170bf6db7dd4997985e1d6abad2a941c89b9ac9f0978468(
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c40bbd7753c10b67c4f32f1cb3f3e00c10880e06b7b11a8886c99f1bb3ea356(
    scope: _constructs_77d1e7e8.Construct,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5f7362e36627303c74ffdfa6958885622b66d4b604e7aa500ad76cb88776e8(
    service: _aws_cdk_aws_ecs_7896c08f.BaseService,
    container: _aws_cdk_aws_ecs_7896c08f.ContainerDefinition,
    targets: typing.Sequence[typing.Union[ApplicationTargetProps, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d43742552dd69939407f4214a661813dce4c1e8c0ae93404d573fabc1a5061e3(
    value: typing.List[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationListener],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abfc91945bf5dc36f7caa9b6e7f0b3262ed07f6d78ac4a06d47e3e16c5f01841(
    value: typing.List[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationTargetGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bfac22edba40356132b69f334f71c4832769fcefd9e52cb6b9ba7326223f746(
    value: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb4d23ed1fd2070304a42718750e8b30644cf0924d289e64003849f0a1d51cb(
    *,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    load_balancers: typing.Optional[typing.Sequence[typing.Union[ApplicationLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    service_name: typing.Optional[builtins.str] = None,
    target_groups: typing.Optional[typing.Sequence[typing.Union[ApplicationTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12abe5f06f1b17c2b185768d66177f4ad029397881b5989ea2bbfd57aac41460(
    *,
    container_port: jsii.Number,
    host_header: typing.Optional[builtins.str] = None,
    listener: typing.Optional[builtins.str] = None,
    path_pattern: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Protocol] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecbd39f4149547628d94220753cb27eb7a24dfdd5fb4d2991028de1b71af154(
    *,
    name: builtins.str,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c864defb4563f36027e80f4be19c87cda5ece2096391fd8c1e272e554b50df(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    domain_name: typing.Optional[builtins.str] = None,
    domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    listener_port: typing.Optional[jsii.Number] = None,
    load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancer] = None,
    max_healthy_percent: typing.Optional[jsii.Number] = None,
    min_healthy_percent: typing.Optional[jsii.Number] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    public_load_balancer: typing.Optional[builtins.bool] = None,
    record_type: typing.Optional[NetworkLoadBalancedServiceRecordType] = None,
    service_name: typing.Optional[builtins.str] = None,
    task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9aa9c0eea11a09b13fe29b8a0b72b4716f7df35dd70ca38bc07b2f2b744e95b(
    service: _aws_cdk_aws_ecs_7896c08f.BaseService,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb2a6e0b70236d9b28dc333cc96a8ef1a77e820bd2ed170e8a2fddd1be5b2b92(
    prefix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0cf0cfc4b1a2a995a5d6728bb49ea80c7a0c47976526da5bc371ecf25629302(
    scope: _aws_cdk_core_f4b25747.Construct,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a4157051083ba2515900e2f450140fe30cc8c2ff9435232d1bc07c3599ba80(
    *,
    circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    domain_name: typing.Optional[builtins.str] = None,
    domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    listener_port: typing.Optional[jsii.Number] = None,
    load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancer] = None,
    max_healthy_percent: typing.Optional[jsii.Number] = None,
    min_healthy_percent: typing.Optional[jsii.Number] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    public_load_balancer: typing.Optional[builtins.bool] = None,
    record_type: typing.Optional[NetworkLoadBalancedServiceRecordType] = None,
    service_name: typing.Optional[builtins.str] = None,
    task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0374062df719f8c3e0e73480f72e5f4757cc946b5b04024835c9f8b671371c7c(
    *,
    image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
    container_name: typing.Optional[builtins.str] = None,
    container_port: typing.Optional[jsii.Number] = None,
    docker_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    execution_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    family: typing.Optional[builtins.str] = None,
    log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
    task_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbcb7341cb40b22a087e9fdea3534d29f47d524f1b1e01b761614eb6f694a0d4(
    *,
    image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
    container_name: typing.Optional[builtins.str] = None,
    container_ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
    docker_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    execution_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    family: typing.Optional[builtins.str] = None,
    log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
    task_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7919b2d9b5e0aebd2d208b368636438029ddfedcfa692a4c68f7033ed6fcc988(
    *,
    listeners: typing.Sequence[typing.Union[NetworkListenerProps, typing.Dict[builtins.str, typing.Any]]],
    name: builtins.str,
    domain_name: typing.Optional[builtins.str] = None,
    domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
    public_load_balancer: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d206b7315599e3d8a578a68ce6cb797f4d346078d3550c92571ea6783168369(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    load_balancers: typing.Optional[typing.Sequence[typing.Union[NetworkLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    service_name: typing.Optional[builtins.str] = None,
    target_groups: typing.Optional[typing.Sequence[typing.Union[NetworkTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb75bfbf1d1997d674de06caa71f633bbc1ee84514d983557db84518314266e(
    container: _aws_cdk_aws_ecs_7896c08f.ContainerDefinition,
    targets: typing.Sequence[typing.Union[NetworkTargetProps, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125c757436a02e6588c8e16dfa29770a89bcb44e2e76ac9c96925e1f866577f8(
    prefix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e737cd82b0b818a2a41eee2ca7098026dbacf121c10ef98fd453e9fcb743f7(
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1572e84655425eb85cd862e552e8f7731bd2ad77e15e0064d77df3a437820483(
    scope: _constructs_77d1e7e8.Construct,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99add5c434d77b4d4e4658b80c1eeb9146226e78b2dae1cfe95b4cc42f6b9004(
    service: _aws_cdk_aws_ecs_7896c08f.BaseService,
    container: _aws_cdk_aws_ecs_7896c08f.ContainerDefinition,
    targets: typing.Sequence[typing.Union[NetworkTargetProps, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ca8bfb0679467f7d12a551e67b8b65cccd73c0807c3befd0494d263a0375e3(
    value: typing.List[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkListener],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d6d2afa98cdba3cd3e2148fc9f1ac440bbd4fd52fb30bc71f7f4269d2976226(
    value: typing.List[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.NetworkTargetGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d05dd501f24dc65a80429b327cb50464fdefedaea6a6ba3ab2589bed733524e6(
    value: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52c25650d1aeba8f094edeb0b7cb5e8cc102f662f61d3f9d169883bb74c174f2(
    *,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    load_balancers: typing.Optional[typing.Sequence[typing.Union[NetworkLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    service_name: typing.Optional[builtins.str] = None,
    target_groups: typing.Optional[typing.Sequence[typing.Union[NetworkTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a025dde5ba84036c647d7a71a65cbaa81877f51ed8f92c98d9c80342cbe9d9b0(
    *,
    container_port: jsii.Number,
    listener: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c4667215185f9aac504de66063e19233242bd897b690593b8482de022f9ee3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
    capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_7896c08f.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
    circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
    desired_task_count: typing.Optional[jsii.Number] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    family: typing.Optional[builtins.str] = None,
    log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
    max_healthy_percent: typing.Optional[jsii.Number] = None,
    max_receive_count: typing.Optional[jsii.Number] = None,
    max_scaling_capacity: typing.Optional[jsii.Number] = None,
    min_healthy_percent: typing.Optional[jsii.Number] = None,
    min_scaling_capacity: typing.Optional[jsii.Number] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    queue: typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue] = None,
    retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    scaling_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval, typing.Dict[builtins.str, typing.Any]]]] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
    service_name: typing.Optional[builtins.str] = None,
    visibility_timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0cd6787347fb77f1086bfe3a6bb7e691881b9281799ca3fbb92ec63905b2218(
    service: _aws_cdk_aws_ecs_7896c08f.BaseService,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded2e8bb80b5710d47088763eb8e4db6258ddba4ced85427b6cbcf01ddaba503(
    scope: _constructs_77d1e7e8.Construct,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce63b3f7e49f8867b3ad775d86279487cf9973c7ce8f465f597874929dd683c(
    service: _aws_cdk_aws_ecs_7896c08f.BaseService,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c682d33923fe884e4a8dbd393aeb9b3b7d5a38a2a50a934a7375f703b45cf9(
    *,
    image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
    capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_7896c08f.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
    circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
    desired_task_count: typing.Optional[jsii.Number] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    family: typing.Optional[builtins.str] = None,
    log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
    max_healthy_percent: typing.Optional[jsii.Number] = None,
    max_receive_count: typing.Optional[jsii.Number] = None,
    max_scaling_capacity: typing.Optional[jsii.Number] = None,
    min_healthy_percent: typing.Optional[jsii.Number] = None,
    min_scaling_capacity: typing.Optional[jsii.Number] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    queue: typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue] = None,
    retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    scaling_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval, typing.Dict[builtins.str, typing.Any]]]] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
    service_name: typing.Optional[builtins.str] = None,
    visibility_timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f9043838648ba66f337b8e8eb6102a2dd574988a6641ad03674eac625feeb4(
    *,
    task_definition: _aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc8a83aae9ace58f8e94ffbc7b5b82a7f444c7b4b21e91a12434f57fe023795(
    *,
    task_definition: _aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb5878ed966887ad6b48c3d5dde4d7674dd004380184dbe56803969fb69bbb2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    schedule: _aws_cdk_aws_applicationautoscaling_a31e8c21.Schedule,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    desired_task_count: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
    rule_name: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d0959a125b494a3a9272cbc0d8c7deebbb7da6e9c18cc132ac70a841137009(
    ecs_task_target: _aws_cdk_aws_events_targets_3ef2ed32.EcsTask,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5594af5d8c06660a4565b856ad9968199f382c4e0ab141ca08ada0efe954acc5(
    task_definition: _aws_cdk_aws_ecs_7896c08f.TaskDefinition,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5bf15bd25cf5fef77f57d5a52a0bfe3419040bf720324153d22cf6d62ac9e4b(
    prefix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b0adcc42fc3c2b0f85bf46ef6e980efb8b45352b08a808fe7b756571a43b40(
    scope: _aws_cdk_core_f4b25747.Construct,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d95e4023ee9b3e5b2533a632471a9a356c3a9b1e0f66676f11458ac37c9b258(
    *,
    schedule: _aws_cdk_aws_applicationautoscaling_a31e8c21.Schedule,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    desired_task_count: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
    rule_name: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd2f39459e853466df230873bdf5ca27afa15c60fa103d8e8042a9214f53077(
    *,
    image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e4ae5bbd924f174122acbc2af61b1f67f7d61969f57e8671472e64fd9deb2f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    memory_reservation_mib: typing.Optional[jsii.Number] = None,
    placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
    placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
    task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition] = None,
    certificate: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate] = None,
    circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    domain_name: typing.Optional[builtins.str] = None,
    domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    listener_port: typing.Optional[jsii.Number] = None,
    load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancer] = None,
    load_balancer_name: typing.Optional[builtins.str] = None,
    max_healthy_percent: typing.Optional[jsii.Number] = None,
    min_healthy_percent: typing.Optional[jsii.Number] = None,
    open_listener: typing.Optional[builtins.bool] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
    protocol_version: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocolVersion] = None,
    public_load_balancer: typing.Optional[builtins.bool] = None,
    record_type: typing.Optional[ApplicationLoadBalancedServiceRecordType] = None,
    redirect_http: typing.Optional[builtins.bool] = None,
    service_name: typing.Optional[builtins.str] = None,
    ssl_policy: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy] = None,
    target_protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
    task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b145ea706712b94e1d19bc34152617d9aee6772222ed5db90f966863e271e2d1(
    *,
    certificate: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate] = None,
    circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    domain_name: typing.Optional[builtins.str] = None,
    domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    listener_port: typing.Optional[jsii.Number] = None,
    load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancer] = None,
    load_balancer_name: typing.Optional[builtins.str] = None,
    max_healthy_percent: typing.Optional[jsii.Number] = None,
    min_healthy_percent: typing.Optional[jsii.Number] = None,
    open_listener: typing.Optional[builtins.bool] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
    protocol_version: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocolVersion] = None,
    public_load_balancer: typing.Optional[builtins.bool] = None,
    record_type: typing.Optional[ApplicationLoadBalancedServiceRecordType] = None,
    redirect_http: typing.Optional[builtins.bool] = None,
    service_name: typing.Optional[builtins.str] = None,
    ssl_policy: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy] = None,
    target_protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
    task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    memory_reservation_mib: typing.Optional[jsii.Number] = None,
    placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
    placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
    task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d8973f4b6cc15ae4ca3c237489d80bd19d510b9ae5eeae12b6236dd0e44342(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
    task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition] = None,
    task_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate] = None,
    circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    domain_name: typing.Optional[builtins.str] = None,
    domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    listener_port: typing.Optional[jsii.Number] = None,
    load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancer] = None,
    load_balancer_name: typing.Optional[builtins.str] = None,
    max_healthy_percent: typing.Optional[jsii.Number] = None,
    min_healthy_percent: typing.Optional[jsii.Number] = None,
    open_listener: typing.Optional[builtins.bool] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
    protocol_version: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocolVersion] = None,
    public_load_balancer: typing.Optional[builtins.bool] = None,
    record_type: typing.Optional[ApplicationLoadBalancedServiceRecordType] = None,
    redirect_http: typing.Optional[builtins.bool] = None,
    service_name: typing.Optional[builtins.str] = None,
    ssl_policy: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy] = None,
    target_protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
    task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7db0768517b85af0818a09d0288b9ca5ef25c386c71cca4ec9f6c0475d2544d(
    *,
    certificate: typing.Optional[_aws_cdk_aws_certificatemanager_1662be0d.ICertificate] = None,
    circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    domain_name: typing.Optional[builtins.str] = None,
    domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    listener_port: typing.Optional[jsii.Number] = None,
    load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.IApplicationLoadBalancer] = None,
    load_balancer_name: typing.Optional[builtins.str] = None,
    max_healthy_percent: typing.Optional[jsii.Number] = None,
    min_healthy_percent: typing.Optional[jsii.Number] = None,
    open_listener: typing.Optional[builtins.bool] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
    protocol_version: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocolVersion] = None,
    public_load_balancer: typing.Optional[builtins.bool] = None,
    record_type: typing.Optional[ApplicationLoadBalancedServiceRecordType] = None,
    redirect_http: typing.Optional[builtins.bool] = None,
    service_name: typing.Optional[builtins.str] = None,
    ssl_policy: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.SslPolicy] = None,
    target_protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.ApplicationProtocol] = None,
    task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
    task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition] = None,
    task_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55c4425c7e9d9279036389b147894a6689a30b2767b05d0dfe45895e24006667(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    memory_reservation_mib: typing.Optional[jsii.Number] = None,
    placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
    placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
    task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition] = None,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    load_balancers: typing.Optional[typing.Sequence[typing.Union[ApplicationLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    service_name: typing.Optional[builtins.str] = None,
    target_groups: typing.Optional[typing.Sequence[typing.Union[ApplicationTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf0345c737fd1a9b3f21e405848bfd932b8bf7caf70c5278f3921d45ef8ae93(
    *,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    load_balancers: typing.Optional[typing.Sequence[typing.Union[ApplicationLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    service_name: typing.Optional[builtins.str] = None,
    target_groups: typing.Optional[typing.Sequence[typing.Union[ApplicationTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    memory_reservation_mib: typing.Optional[jsii.Number] = None,
    placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
    placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
    task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79aa857fd1297986686754fafef1b42bfe6bfd00943a5aaa24d88b612e96d3fa(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
    task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition] = None,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    load_balancers: typing.Optional[typing.Sequence[typing.Union[ApplicationLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    service_name: typing.Optional[builtins.str] = None,
    target_groups: typing.Optional[typing.Sequence[typing.Union[ApplicationTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6eb13e970c39657e8d031ba170122f99503d4f0f895eb40b5de7cf4b247490(
    *,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    load_balancers: typing.Optional[typing.Sequence[typing.Union[ApplicationLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    service_name: typing.Optional[builtins.str] = None,
    target_groups: typing.Optional[typing.Sequence[typing.Union[ApplicationTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_image_options: typing.Optional[typing.Union[ApplicationLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
    task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b6979d35fe5bf1f0adf4ee8cfe57979c99a6da0307d75b8b0261cb95bc0f20(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    memory_reservation_mib: typing.Optional[jsii.Number] = None,
    placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
    placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
    task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition] = None,
    circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    domain_name: typing.Optional[builtins.str] = None,
    domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    listener_port: typing.Optional[jsii.Number] = None,
    load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancer] = None,
    max_healthy_percent: typing.Optional[jsii.Number] = None,
    min_healthy_percent: typing.Optional[jsii.Number] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    public_load_balancer: typing.Optional[builtins.bool] = None,
    record_type: typing.Optional[NetworkLoadBalancedServiceRecordType] = None,
    service_name: typing.Optional[builtins.str] = None,
    task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18c0352629253352bbe5f8fd1a8542c94d90cdd1b29f3ce374703aedd1996ba(
    *,
    circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    domain_name: typing.Optional[builtins.str] = None,
    domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    listener_port: typing.Optional[jsii.Number] = None,
    load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancer] = None,
    max_healthy_percent: typing.Optional[jsii.Number] = None,
    min_healthy_percent: typing.Optional[jsii.Number] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    public_load_balancer: typing.Optional[builtins.bool] = None,
    record_type: typing.Optional[NetworkLoadBalancedServiceRecordType] = None,
    service_name: typing.Optional[builtins.str] = None,
    task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    memory_reservation_mib: typing.Optional[jsii.Number] = None,
    placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
    placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
    task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ffe0ada1d1350a9e5669c0a36d033f579dbbdbf615e781571262ab7dd179e2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
    task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition] = None,
    task_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    domain_name: typing.Optional[builtins.str] = None,
    domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    listener_port: typing.Optional[jsii.Number] = None,
    load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancer] = None,
    max_healthy_percent: typing.Optional[jsii.Number] = None,
    min_healthy_percent: typing.Optional[jsii.Number] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    public_load_balancer: typing.Optional[builtins.bool] = None,
    record_type: typing.Optional[NetworkLoadBalancedServiceRecordType] = None,
    service_name: typing.Optional[builtins.str] = None,
    task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8536b89b38ccdef3d903c70985e3b4f7fa640dbe49879d54df3cda15a9bab51(
    *,
    circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    domain_name: typing.Optional[builtins.str] = None,
    domain_zone: typing.Optional[_aws_cdk_aws_route53_f47b29d4.IHostedZone] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    listener_port: typing.Optional[jsii.Number] = None,
    load_balancer: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_e93c784f.INetworkLoadBalancer] = None,
    max_healthy_percent: typing.Optional[jsii.Number] = None,
    min_healthy_percent: typing.Optional[jsii.Number] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    public_load_balancer: typing.Optional[builtins.bool] = None,
    record_type: typing.Optional[NetworkLoadBalancedServiceRecordType] = None,
    service_name: typing.Optional[builtins.str] = None,
    task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
    task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition] = None,
    task_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3415f6bc936d3b435e7f10ecb24842c31d4764541d2e445476c313ede26ee1de(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    memory_reservation_mib: typing.Optional[jsii.Number] = None,
    placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
    placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
    task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition] = None,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    load_balancers: typing.Optional[typing.Sequence[typing.Union[NetworkLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    service_name: typing.Optional[builtins.str] = None,
    target_groups: typing.Optional[typing.Sequence[typing.Union[NetworkTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beed0d34499b4616d384c73b6562321c4f68a8e97bb4f69884b297b233b61d2a(
    *,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    load_balancers: typing.Optional[typing.Sequence[typing.Union[NetworkLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    service_name: typing.Optional[builtins.str] = None,
    target_groups: typing.Optional[typing.Sequence[typing.Union[NetworkTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    memory_reservation_mib: typing.Optional[jsii.Number] = None,
    placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
    placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
    task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.Ec2TaskDefinition] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c051a8e5d0edc0e6798d0748cc001dec067b7d1d7b56b4a2cc1398cfb4ecaa20(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
    task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition] = None,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    load_balancers: typing.Optional[typing.Sequence[typing.Union[NetworkLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    service_name: typing.Optional[builtins.str] = None,
    target_groups: typing.Optional[typing.Sequence[typing.Union[NetworkTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a3c1bd8d9747565417a45ccb9268f395ff7db84f9efbeb74a205e4aa51ae12(
    *,
    cloud_map_options: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.CloudMapOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    load_balancers: typing.Optional[typing.Sequence[typing.Union[NetworkLoadBalancerProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    service_name: typing.Optional[builtins.str] = None,
    target_groups: typing.Optional[typing.Sequence[typing.Union[NetworkTargetProps, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_image_options: typing.Optional[typing.Union[NetworkLoadBalancedTaskImageProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
    task_definition: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargateTaskDefinition] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e1e7cb058505452d49bf91b80b165103b2a7de8eb52b22c92299601eae89e7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    container_name: typing.Optional[builtins.str] = None,
    cpu: typing.Optional[jsii.Number] = None,
    gpu_count: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    memory_reservation_mib: typing.Optional[jsii.Number] = None,
    placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
    placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
    image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
    capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_7896c08f.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
    circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
    desired_task_count: typing.Optional[jsii.Number] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    family: typing.Optional[builtins.str] = None,
    log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
    max_healthy_percent: typing.Optional[jsii.Number] = None,
    max_receive_count: typing.Optional[jsii.Number] = None,
    max_scaling_capacity: typing.Optional[jsii.Number] = None,
    min_healthy_percent: typing.Optional[jsii.Number] = None,
    min_scaling_capacity: typing.Optional[jsii.Number] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    queue: typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue] = None,
    retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    scaling_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval, typing.Dict[builtins.str, typing.Any]]]] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
    service_name: typing.Optional[builtins.str] = None,
    visibility_timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796d722d4db4012290f080c5a0abe7b824b69f58f2eb31f1fc1b309cb98881fc(
    *,
    image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
    capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_7896c08f.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
    circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
    desired_task_count: typing.Optional[jsii.Number] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    family: typing.Optional[builtins.str] = None,
    log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
    max_healthy_percent: typing.Optional[jsii.Number] = None,
    max_receive_count: typing.Optional[jsii.Number] = None,
    max_scaling_capacity: typing.Optional[jsii.Number] = None,
    min_healthy_percent: typing.Optional[jsii.Number] = None,
    min_scaling_capacity: typing.Optional[jsii.Number] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    queue: typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue] = None,
    retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    scaling_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval, typing.Dict[builtins.str, typing.Any]]]] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
    service_name: typing.Optional[builtins.str] = None,
    visibility_timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    container_name: typing.Optional[builtins.str] = None,
    cpu: typing.Optional[jsii.Number] = None,
    gpu_count: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    memory_reservation_mib: typing.Optional[jsii.Number] = None,
    placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementConstraint]] = None,
    placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_7896c08f.PlacementStrategy]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae27ad501ead113b2e31fc54240c9a38a6550f7bcccba1281149617f18bb58e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    container_name: typing.Optional[builtins.str] = None,
    cpu: typing.Optional[jsii.Number] = None,
    health_check: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
    task_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
    capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_7896c08f.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
    circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
    desired_task_count: typing.Optional[jsii.Number] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    family: typing.Optional[builtins.str] = None,
    log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
    max_healthy_percent: typing.Optional[jsii.Number] = None,
    max_receive_count: typing.Optional[jsii.Number] = None,
    max_scaling_capacity: typing.Optional[jsii.Number] = None,
    min_healthy_percent: typing.Optional[jsii.Number] = None,
    min_scaling_capacity: typing.Optional[jsii.Number] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    queue: typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue] = None,
    retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    scaling_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval, typing.Dict[builtins.str, typing.Any]]]] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
    service_name: typing.Optional[builtins.str] = None,
    visibility_timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2405bec3da832145d18db507a410fccdeaef352a66898fe0764108cfba5207a5(
    *,
    image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
    capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_7896c08f.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
    circuit_breaker: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentCircuitBreaker, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    deployment_controller: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.DeploymentController, typing.Dict[builtins.str, typing.Any]]] = None,
    desired_task_count: typing.Optional[jsii.Number] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    family: typing.Optional[builtins.str] = None,
    log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
    max_healthy_percent: typing.Optional[jsii.Number] = None,
    max_receive_count: typing.Optional[jsii.Number] = None,
    max_scaling_capacity: typing.Optional[jsii.Number] = None,
    min_healthy_percent: typing.Optional[jsii.Number] = None,
    min_scaling_capacity: typing.Optional[jsii.Number] = None,
    propagate_tags: typing.Optional[_aws_cdk_aws_ecs_7896c08f.PropagatedTagSource] = None,
    queue: typing.Optional[_aws_cdk_aws_sqs_48bffef9.IQueue] = None,
    retention_period: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    scaling_steps: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_applicationautoscaling_a31e8c21.ScalingInterval, typing.Dict[builtins.str, typing.Any]]]] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
    service_name: typing.Optional[builtins.str] = None,
    visibility_timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    container_name: typing.Optional[builtins.str] = None,
    cpu: typing.Optional[jsii.Number] = None,
    health_check: typing.Optional[typing.Union[_aws_cdk_aws_ecs_7896c08f.HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
    task_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3817049e832518f5bd5127d62c81691c6a48b7acecb0266bd5cdb237d76bf4b4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    scheduled_ec2_task_definition_options: typing.Optional[typing.Union[ScheduledEc2TaskDefinitionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduled_ec2_task_image_options: typing.Optional[typing.Union[ScheduledEc2TaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: _aws_cdk_aws_applicationautoscaling_a31e8c21.Schedule,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    desired_task_count: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
    rule_name: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3036d3298f587a6fd28873f6e42fb1f608fbaa6e35e34304f14e46f9b7293490(
    *,
    image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    memory_reservation_mib: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87040b77ccdb852585e6341b4df755f8693a3d39ce8c872a1f36b424fbde2623(
    *,
    schedule: _aws_cdk_aws_applicationautoscaling_a31e8c21.Schedule,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    desired_task_count: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
    rule_name: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    scheduled_ec2_task_definition_options: typing.Optional[typing.Union[ScheduledEc2TaskDefinitionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduled_ec2_task_image_options: typing.Optional[typing.Union[ScheduledEc2TaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7777d46bcff0542e36bf882a7f8299da8e737e62b4803d004040ae3eb073c948(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
    scheduled_fargate_task_definition_options: typing.Optional[typing.Union[ScheduledFargateTaskDefinitionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduled_fargate_task_image_options: typing.Optional[typing.Union[ScheduledFargateTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    schedule: _aws_cdk_aws_applicationautoscaling_a31e8c21.Schedule,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    desired_task_count: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
    rule_name: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8268eb5a0daeacc4062e594f78f0a94bdc0d71550fb39babfca1c3641fda81(
    *,
    image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    log_driver: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LogDriver] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ecs_7896c08f.Secret]] = None,
    cpu: typing.Optional[jsii.Number] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ca26da6b6e40a10dc1cf1d5fc45d59df83be836f2056705c1f7c1dbc1ea728(
    *,
    schedule: _aws_cdk_aws_applicationautoscaling_a31e8c21.Schedule,
    cluster: typing.Optional[_aws_cdk_aws_ecs_7896c08f.ICluster] = None,
    desired_task_count: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[builtins.bool] = None,
    rule_name: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IVpc] = None,
    platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
    scheduled_fargate_task_definition_options: typing.Optional[typing.Union[ScheduledFargateTaskDefinitionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    scheduled_fargate_task_image_options: typing.Optional[typing.Union[ScheduledFargateTaskImageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
