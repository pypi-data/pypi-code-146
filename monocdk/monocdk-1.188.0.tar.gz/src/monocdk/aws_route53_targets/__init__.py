'''
# Route53 Alias Record Targets for the CDK Route53 Library

This library contains Route53 Alias Record targets for:

* API Gateway custom domains

  ```python
  import monocdk as apigw

  # zone: route53.HostedZone
  # rest_api: apigw.LambdaRestApi


  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(targets.ApiGateway(rest_api))
  )
  ```
* API Gateway V2 custom domains

  ```python
  import monocdk as apigwv2

  # zone: route53.HostedZone
  # domain_name: apigwv2.DomainName


  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(targets.ApiGatewayv2DomainProperties(domain_name.regional_domain_name, domain_name.regional_hosted_zone_id))
  )
  ```
* CloudFront distributions

  ```python
  import monocdk as cloudfront

  # zone: route53.HostedZone
  # distribution: cloudfront.CloudFrontWebDistribution


  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution))
  )
  ```
* ELBv2 load balancers

  ```python
  import monocdk as elbv2

  # zone: route53.HostedZone
  # lb: elbv2.ApplicationLoadBalancer


  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(targets.LoadBalancerTarget(lb))
  )
  ```
* Classic load balancers

  ```python
  import monocdk as elb

  # zone: route53.HostedZone
  # lb: elb.LoadBalancer


  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(targets.ClassicLoadBalancerTarget(lb))
  )
  ```

**Important:** Based on [AWS documentation](https://aws.amazon.com/de/premiumsupport/knowledge-center/alias-resource-record-set-route53-cli/), all alias record in Route 53 that points to a Elastic Load Balancer will always include *dualstack* for the DNSName to resolve IPv4/IPv6 addresses (without *dualstack* IPv6 will not resolve).

For example, if the Amazon-provided DNS for the load balancer is `ALB-xxxxxxx.us-west-2.elb.amazonaws.com`, CDK will create alias target in Route 53 will be `dualstack.ALB-xxxxxxx.us-west-2.elb.amazonaws.com`.

* GlobalAccelerator

  ```python
  import monocdk as globalaccelerator

  # zone: route53.HostedZone
  # accelerator: globalaccelerator.Accelerator


  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(targets.GlobalAcceleratorTarget(accelerator))
  )
  ```

**Important:** If you use GlobalAcceleratorDomainTarget, passing a string rather than an instance of IAccelerator, ensure that the string is a valid domain name of an existing Global Accelerator instance.
See [the documentation on DNS addressing](https://docs.aws.amazon.com/global-accelerator/latest/dg/dns-addressing-custom-domains.dns-addressing.html) with Global Accelerator for more info.

* InterfaceVpcEndpoints

**Important:** Based on the CFN docs for VPCEndpoints - [see here](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpoint.html#aws-resource-ec2-vpcendpoint-return-values) - the attributes returned for DnsEntries in CloudFormation is a combination of the hosted zone ID and the DNS name. The entries are ordered as follows: regional public DNS, zonal public DNS, private DNS, and wildcard DNS. This order is not enforced for AWS Marketplace services, and therefore this CDK construct is ONLY guaranteed to work with non-marketplace services.

```python
import monocdk as ec2

# zone: route53.HostedZone
# interface_vpc_endpoint: ec2.InterfaceVpcEndpoint


route53.ARecord(self, "AliasRecord",
    zone=zone,
    target=route53.RecordTarget.from_alias(targets.InterfaceVpcEndpointTarget(interface_vpc_endpoint))
)
```

* S3 Bucket Website:

**Important:** The Bucket name must strictly match the full DNS name.
See [the Developer Guide](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/getting-started.html) for more info.

```python
import monocdk as s3


record_name = "www"
domain_name = "example.com"

bucket_website = s3.Bucket(self, "BucketWebsite",
    bucket_name=[record_name, domain_name].join("."),  # www.example.com
    public_read_access=True,
    website_index_document="index.html"
)

zone = route53.HostedZone.from_lookup(self, "Zone", domain_name=domain_name) # example.com

route53.ARecord(self, "AliasRecord",
    zone=zone,
    record_name=record_name,  # www
    target=route53.RecordTarget.from_alias(targets.BucketWebsiteTarget(bucket_website))
)
```

* User pool domain

  ```python
  import monocdk as cognito

  # zone: route53.HostedZone
  # domain: cognito.UserPoolDomain

  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(targets.UserPoolDomainTarget(domain))
  )
  ```
* Route 53 record

  ```python
  # zone: route53.HostedZone
  # record: route53.ARecord

  route53.ARecord(self, "AliasRecord",
      zone=zone,
      target=route53.RecordTarget.from_alias(targets.Route53RecordTarget(record))
  )
  ```
* Elastic Beanstalk environment:

**Important:** Only supports Elastic Beanstalk environments created after 2016 that have a regional endpoint.

```python
# zone: route53.HostedZone
# ebs_environment_url: str


route53.ARecord(self, "AliasRecord",
    zone=zone,
    target=route53.RecordTarget.from_alias(targets.ElasticBeanstalkEnvironmentEndpointTarget(ebs_environment_url))
)
```

See the documentation of `@aws-cdk/aws-route53` for more information.
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

from .. import IConstruct as _IConstruct_5a0f9c5e
from ..aws_apigateway import (
    IDomainName as _IDomainName_2f71106c, RestApiBase as _RestApiBase_8be2daa9
)
from ..aws_cloudfront import IDistribution as _IDistribution_685deca5
from ..aws_cognito import UserPoolDomain as _UserPoolDomain_18478017
from ..aws_ec2 import IInterfaceVpcEndpoint as _IInterfaceVpcEndpoint_6081623d
from ..aws_elasticloadbalancing import LoadBalancer as _LoadBalancer_a7de240f
from ..aws_elasticloadbalancingv2 import ILoadBalancerV2 as _ILoadBalancerV2_f1c75d72
from ..aws_globalaccelerator import IAccelerator as _IAccelerator_8b90cb82
from ..aws_route53 import (
    AliasRecordTargetConfig as _AliasRecordTargetConfig_5788d785,
    IAliasRecordTarget as _IAliasRecordTarget_f7c401c2,
    IHostedZone as _IHostedZone_78d5a9c9,
    IRecordSet as _IRecordSet_133a645a,
)
from ..aws_s3 import IBucket as _IBucket_73486e29


@jsii.implements(_IAliasRecordTarget_f7c401c2)
class ApiGatewayDomain(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53_targets.ApiGatewayDomain",
):
    '''(experimental) Defines an API Gateway domain name as the alias target.

    Use the ``ApiGateway`` class if you wish to map the alias to an REST API with a
    domain name defined through the ``RestApiProps.domainName`` prop.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # hosted_zone_for_example_com: Any
        # domain_name: apigateway.DomainName
        
        import monocdk as route53
        import monocdk as targets
        
        
        route53.ARecord(self, "CustomDomainAliasRecord",
            zone=hosted_zone_for_example_com,
            target=route53.RecordTarget.from_alias(targets.ApiGatewayDomain(domain_name))
        )
    '''

    def __init__(self, domain_name: _IDomainName_2f71106c) -> None:
        '''
        :param domain_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d49a8136c756c219e2234eff358adabd8c6eaf00f32c3c9bc927841203cf6800)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
        jsii.create(self.__class__, self, [domain_name])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: _IRecordSet_133a645a,
        _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
    ) -> _AliasRecordTargetConfig_5788d785:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        :param _zone: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec5f0b4bb0e51294b23f7531a18b10e0d2b15196b95cec34c20020a09c64b25)
            check_type(argname="argument _record", value=_record, expected_type=type_hints["_record"])
            check_type(argname="argument _zone", value=_zone, expected_type=type_hints["_zone"])
        return typing.cast(_AliasRecordTargetConfig_5788d785, jsii.invoke(self, "bind", [_record, _zone]))


@jsii.implements(_IAliasRecordTarget_f7c401c2)
class ApiGatewayv2DomainProperties(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53_targets.ApiGatewayv2DomainProperties",
):
    '''(experimental) Defines an API Gateway V2 domain name as the alias target.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as apigwv2
        
        # zone: route53.HostedZone
        # domain_name: apigwv2.DomainName
        
        
        route53.ARecord(self, "AliasRecord",
            zone=zone,
            target=route53.RecordTarget.from_alias(targets.ApiGatewayv2DomainProperties(domain_name.regional_domain_name, domain_name.regional_hosted_zone_id))
        )
    '''

    def __init__(
        self,
        regional_domain_name: builtins.str,
        regional_hosted_zone_id: builtins.str,
    ) -> None:
        '''
        :param regional_domain_name: the domain name associated with the regional endpoint for this custom domain name.
        :param regional_hosted_zone_id: the region-specific Amazon Route 53 Hosted Zone ID of the regional endpoint.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b057fb1f1fb3519cab268ae870b598023b551eaf0140b6e94b729292c272c59)
            check_type(argname="argument regional_domain_name", value=regional_domain_name, expected_type=type_hints["regional_domain_name"])
            check_type(argname="argument regional_hosted_zone_id", value=regional_hosted_zone_id, expected_type=type_hints["regional_hosted_zone_id"])
        jsii.create(self.__class__, self, [regional_domain_name, regional_hosted_zone_id])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: _IRecordSet_133a645a,
        _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
    ) -> _AliasRecordTargetConfig_5788d785:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        :param _zone: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a484e5fd65f7e7ec8c5c2c3d1d5129d912f9d6096b0c6e450bd42cc6d5e499f0)
            check_type(argname="argument _record", value=_record, expected_type=type_hints["_record"])
            check_type(argname="argument _zone", value=_zone, expected_type=type_hints["_zone"])
        return typing.cast(_AliasRecordTargetConfig_5788d785, jsii.invoke(self, "bind", [_record, _zone]))


@jsii.implements(_IAliasRecordTarget_f7c401c2)
class BucketWebsiteTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53_targets.BucketWebsiteTarget",
):
    '''(experimental) Use a S3 as an alias record target.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as s3
        
        
        record_name = "www"
        domain_name = "example.com"
        
        bucket_website = s3.Bucket(self, "BucketWebsite",
            bucket_name=[record_name, domain_name].join("."),  # www.example.com
            public_read_access=True,
            website_index_document="index.html"
        )
        
        zone = route53.HostedZone.from_lookup(self, "Zone", domain_name=domain_name) # example.com
        
        route53.ARecord(self, "AliasRecord",
            zone=zone,
            record_name=record_name,  # www
            target=route53.RecordTarget.from_alias(targets.BucketWebsiteTarget(bucket_website))
        )
    '''

    def __init__(self, bucket: _IBucket_73486e29) -> None:
        '''
        :param bucket: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f2bd2957df209ee46123eb47d59cb035d243fc5fdebbe52f7d34d6a50319ed)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        jsii.create(self.__class__, self, [bucket])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: _IRecordSet_133a645a,
        _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
    ) -> _AliasRecordTargetConfig_5788d785:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        :param _zone: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9eee7913b1a69e16f5b9371e592bf811c86499540699c17825620be3175f380)
            check_type(argname="argument _record", value=_record, expected_type=type_hints["_record"])
            check_type(argname="argument _zone", value=_zone, expected_type=type_hints["_zone"])
        return typing.cast(_AliasRecordTargetConfig_5788d785, jsii.invoke(self, "bind", [_record, _zone]))


@jsii.implements(_IAliasRecordTarget_f7c401c2)
class ClassicLoadBalancerTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53_targets.ClassicLoadBalancerTarget",
):
    '''(experimental) Use a classic ELB as an alias record target.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as elb
        
        # zone: route53.HostedZone
        # lb: elb.LoadBalancer
        
        
        route53.ARecord(self, "AliasRecord",
            zone=zone,
            target=route53.RecordTarget.from_alias(targets.ClassicLoadBalancerTarget(lb))
        )
    '''

    def __init__(self, load_balancer: _LoadBalancer_a7de240f) -> None:
        '''
        :param load_balancer: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82858a0ded466991ff0a8c731f2777292e6b64988ef3fa287f1bf2ad446b45f0)
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
        jsii.create(self.__class__, self, [load_balancer])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: _IRecordSet_133a645a,
        _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
    ) -> _AliasRecordTargetConfig_5788d785:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        :param _zone: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0066533578d6c9458d6a61050194acd9259ec182113264b7ad46461e524168f4)
            check_type(argname="argument _record", value=_record, expected_type=type_hints["_record"])
            check_type(argname="argument _zone", value=_zone, expected_type=type_hints["_zone"])
        return typing.cast(_AliasRecordTargetConfig_5788d785, jsii.invoke(self, "bind", [_record, _zone]))


@jsii.implements(_IAliasRecordTarget_f7c401c2)
class CloudFrontTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53_targets.CloudFrontTarget",
):
    '''(experimental) Use a CloudFront Distribution as an alias record target.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as cloudfront
        
        # my_zone: route53.HostedZone
        # distribution: cloudfront.CloudFrontWebDistribution
        
        route53.AaaaRecord(self, "Alias",
            zone=my_zone,
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution))
        )
    '''

    def __init__(self, distribution: _IDistribution_685deca5) -> None:
        '''
        :param distribution: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec082d244330e3f8c0e5c1c1d4b8f80248f5f86bc80d1daaa567205a6efc1b1e)
            check_type(argname="argument distribution", value=distribution, expected_type=type_hints["distribution"])
        jsii.create(self.__class__, self, [distribution])

    @jsii.member(jsii_name="getHostedZoneId")
    @builtins.classmethod
    def get_hosted_zone_id(cls, scope: _IConstruct_5a0f9c5e) -> builtins.str:
        '''(experimental) Get the hosted zone id for the current scope.

        :param scope: - scope in which this resource is defined.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07e07a82be8846e9ad6df684b99605a8f6cbf3ffdfddfdf7c0fa50b0952b35af)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getHostedZoneId", [scope]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: _IRecordSet_133a645a,
        _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
    ) -> _AliasRecordTargetConfig_5788d785:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        :param _zone: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0711b704f94eb0a950aadf03ce10909d3b0641258775b9cf1466e460e1c32f87)
            check_type(argname="argument _record", value=_record, expected_type=type_hints["_record"])
            check_type(argname="argument _zone", value=_zone, expected_type=type_hints["_zone"])
        return typing.cast(_AliasRecordTargetConfig_5788d785, jsii.invoke(self, "bind", [_record, _zone]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CLOUDFRONT_ZONE_ID")
    def CLOUDFRONT_ZONE_ID(cls) -> builtins.str:
        '''(experimental) The hosted zone Id if using an alias record in Route53.

        This value never changes.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "CLOUDFRONT_ZONE_ID"))


@jsii.implements(_IAliasRecordTarget_f7c401c2)
class ElasticBeanstalkEnvironmentEndpointTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53_targets.ElasticBeanstalkEnvironmentEndpointTarget",
):
    '''(experimental) Use an Elastic Beanstalk environment URL as an alias record target. E.g. mysampleenvironment.xyz.us-east-1.elasticbeanstalk.com or mycustomcnameprefix.us-east-1.elasticbeanstalk.com.

    Only supports Elastic Beanstalk environments created after 2016 that have a regional endpoint.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # zone: route53.HostedZone
        # ebs_environment_url: str
        
        
        route53.ARecord(self, "AliasRecord",
            zone=zone,
            target=route53.RecordTarget.from_alias(targets.ElasticBeanstalkEnvironmentEndpointTarget(ebs_environment_url))
        )
    '''

    def __init__(self, environment_endpoint: builtins.str) -> None:
        '''
        :param environment_endpoint: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a988c89f12ade1b00aaccbe41983cd80b2f49b4a9bb267e56102c6808ecf3682)
            check_type(argname="argument environment_endpoint", value=environment_endpoint, expected_type=type_hints["environment_endpoint"])
        jsii.create(self.__class__, self, [environment_endpoint])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: _IRecordSet_133a645a,
        _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
    ) -> _AliasRecordTargetConfig_5788d785:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        :param _zone: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea3a4e065a4c470b592fe64c22eaf1a5155152d956bbacf82776625c09ccb51d)
            check_type(argname="argument _record", value=_record, expected_type=type_hints["_record"])
            check_type(argname="argument _zone", value=_zone, expected_type=type_hints["_zone"])
        return typing.cast(_AliasRecordTargetConfig_5788d785, jsii.invoke(self, "bind", [_record, _zone]))


@jsii.implements(_IAliasRecordTarget_f7c401c2)
class GlobalAcceleratorDomainTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53_targets.GlobalAcceleratorDomainTarget",
):
    '''(experimental) Use a Global Accelerator domain name as an alias record target.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53_targets as route53_targets
        
        global_accelerator_domain_target = route53_targets.GlobalAcceleratorDomainTarget("acceleratorDomainName")
    '''

    def __init__(self, accelerator_domain_name: builtins.str) -> None:
        '''(experimental) Create an Alias Target for a Global Accelerator domain name.

        :param accelerator_domain_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c773859bc9453d4b7973806936a58e7e1be860d98395b64a50b68fb8898ba96)
            check_type(argname="argument accelerator_domain_name", value=accelerator_domain_name, expected_type=type_hints["accelerator_domain_name"])
        jsii.create(self.__class__, self, [accelerator_domain_name])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: _IRecordSet_133a645a,
        _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
    ) -> _AliasRecordTargetConfig_5788d785:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        :param _zone: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41e911cb0718b9e46f01cc873ba75ab24a15a1ea3d91b7531573bb117bf7317e)
            check_type(argname="argument _record", value=_record, expected_type=type_hints["_record"])
            check_type(argname="argument _zone", value=_zone, expected_type=type_hints["_zone"])
        return typing.cast(_AliasRecordTargetConfig_5788d785, jsii.invoke(self, "bind", [_record, _zone]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GLOBAL_ACCELERATOR_ZONE_ID")
    def GLOBAL_ACCELERATOR_ZONE_ID(cls) -> builtins.str:
        '''(experimental) The hosted zone Id if using an alias record in Route53.

        This value never changes.
        Ref: https://docs.aws.amazon.com/general/latest/gr/global_accelerator.html

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "GLOBAL_ACCELERATOR_ZONE_ID"))


class GlobalAcceleratorTarget(
    GlobalAcceleratorDomainTarget,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53_targets.GlobalAcceleratorTarget",
):
    '''(experimental) Use a Global Accelerator instance domain name as an alias record target.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as globalaccelerator
        
        # zone: route53.HostedZone
        # accelerator: globalaccelerator.Accelerator
        
        
        route53.ARecord(self, "AliasRecord",
            zone=zone,
            target=route53.RecordTarget.from_alias(targets.GlobalAcceleratorTarget(accelerator))
        )
    '''

    def __init__(self, accelerator: _IAccelerator_8b90cb82) -> None:
        '''(experimental) Create an Alias Target for a Global Accelerator instance.

        :param accelerator: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74bb7f7db426fcd739812d69f4cf7698d57d3a5896229aef480e58686edf4b8b)
            check_type(argname="argument accelerator", value=accelerator, expected_type=type_hints["accelerator"])
        jsii.create(self.__class__, self, [accelerator])


@jsii.implements(_IAliasRecordTarget_f7c401c2)
class InterfaceVpcEndpointTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53_targets.InterfaceVpcEndpointTarget",
):
    '''(experimental) Set an InterfaceVpcEndpoint as a target for an ARecord.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as ec2
        
        # zone: route53.HostedZone
        # interface_vpc_endpoint: ec2.InterfaceVpcEndpoint
        
        
        route53.ARecord(self, "AliasRecord",
            zone=zone,
            target=route53.RecordTarget.from_alias(targets.InterfaceVpcEndpointTarget(interface_vpc_endpoint))
        )
    '''

    def __init__(self, vpc_endpoint: _IInterfaceVpcEndpoint_6081623d) -> None:
        '''
        :param vpc_endpoint: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1433099182e18c518cf95bd4df9a2c3ca2f0178c1003342d9f2d82d10a13e8a3)
            check_type(argname="argument vpc_endpoint", value=vpc_endpoint, expected_type=type_hints["vpc_endpoint"])
        jsii.create(self.__class__, self, [vpc_endpoint])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: _IRecordSet_133a645a,
        _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
    ) -> _AliasRecordTargetConfig_5788d785:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        :param _zone: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a184ac7fe32db7550de9c978701385bf46cd0b98e076c84f9967c87fa186484f)
            check_type(argname="argument _record", value=_record, expected_type=type_hints["_record"])
            check_type(argname="argument _zone", value=_zone, expected_type=type_hints["_zone"])
        return typing.cast(_AliasRecordTargetConfig_5788d785, jsii.invoke(self, "bind", [_record, _zone]))


@jsii.implements(_IAliasRecordTarget_f7c401c2)
class LoadBalancerTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53_targets.LoadBalancerTarget",
):
    '''(experimental) Use an ELBv2 as an alias record target.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as elbv2
        
        # zone: route53.HostedZone
        # lb: elbv2.ApplicationLoadBalancer
        
        
        route53.ARecord(self, "AliasRecord",
            zone=zone,
            target=route53.RecordTarget.from_alias(targets.LoadBalancerTarget(lb))
        )
    '''

    def __init__(self, load_balancer: _ILoadBalancerV2_f1c75d72) -> None:
        '''
        :param load_balancer: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0845c0220d6c4f72bb7a6cc8fa3fbc18a27cf5b2898702f9a2c5df81a85aebc8)
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
        jsii.create(self.__class__, self, [load_balancer])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: _IRecordSet_133a645a,
        _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
    ) -> _AliasRecordTargetConfig_5788d785:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        :param _zone: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7600ff54d517da9b2c0c94e3519602bb6a87554f0b6a528c2a5f1d4eda39b941)
            check_type(argname="argument _record", value=_record, expected_type=type_hints["_record"])
            check_type(argname="argument _zone", value=_zone, expected_type=type_hints["_zone"])
        return typing.cast(_AliasRecordTargetConfig_5788d785, jsii.invoke(self, "bind", [_record, _zone]))


@jsii.implements(_IAliasRecordTarget_f7c401c2)
class Route53RecordTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53_targets.Route53RecordTarget",
):
    '''(experimental) Use another Route 53 record as an alias record target.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # zone: route53.HostedZone
        # record: route53.ARecord
        
        route53.ARecord(self, "AliasRecord",
            zone=zone,
            target=route53.RecordTarget.from_alias(targets.Route53RecordTarget(record))
        )
    '''

    def __init__(self, record: _IRecordSet_133a645a) -> None:
        '''
        :param record: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0132b09b963b953ebbcc3d485ab80b82e1cfb0ea66540a36a70106082d90f1d)
            check_type(argname="argument record", value=record, expected_type=type_hints["record"])
        jsii.create(self.__class__, self, [record])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: _IRecordSet_133a645a,
        zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
    ) -> _AliasRecordTargetConfig_5788d785:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        :param zone: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b03a54fa3b25e122b58a0ff3618e7e8030b4db7ae0608ce084c2282059e57a49)
            check_type(argname="argument _record", value=_record, expected_type=type_hints["_record"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        return typing.cast(_AliasRecordTargetConfig_5788d785, jsii.invoke(self, "bind", [_record, zone]))


@jsii.implements(_IAliasRecordTarget_f7c401c2)
class UserPoolDomainTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53_targets.UserPoolDomainTarget",
):
    '''(experimental) Use a user pool domain as an alias record target.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as cognito
        
        # zone: route53.HostedZone
        # domain: cognito.UserPoolDomain
        
        route53.ARecord(self, "AliasRecord",
            zone=zone,
            target=route53.RecordTarget.from_alias(targets.UserPoolDomainTarget(domain))
        )
    '''

    def __init__(self, domain: _UserPoolDomain_18478017) -> None:
        '''
        :param domain: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__730d5a98f195e20f202e35618e3d52f2183495b4e33eb8fd0b5c53655433170d)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        jsii.create(self.__class__, self, [domain])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _record: _IRecordSet_133a645a,
        _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
    ) -> _AliasRecordTargetConfig_5788d785:
        '''(experimental) Return hosted zone ID and DNS name, usable for Route53 alias targets.

        :param _record: -
        :param _zone: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b240eb68449c4b26242e4c4dcc7658e18335f918577e97402931b85dd9054046)
            check_type(argname="argument _record", value=_record, expected_type=type_hints["_record"])
            check_type(argname="argument _zone", value=_zone, expected_type=type_hints["_zone"])
        return typing.cast(_AliasRecordTargetConfig_5788d785, jsii.invoke(self, "bind", [_record, _zone]))


class ApiGateway(
    ApiGatewayDomain,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53_targets.ApiGateway",
):
    '''(experimental) Defines an API Gateway REST API as the alias target. Requires that the domain name will be defined through ``RestApiProps.domainName``.

    You can direct the alias to any ``apigateway.DomainName`` resource through the
    ``ApiGatewayDomain`` class.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as route53
        import monocdk as targets
        
        # api: apigateway.RestApi
        # hosted_zone_for_example_com: Any
        
        
        route53.ARecord(self, "CustomDomainAliasRecord",
            zone=hosted_zone_for_example_com,
            target=route53.RecordTarget.from_alias(targets.ApiGateway(api))
        )
    '''

    def __init__(self, api: _RestApiBase_8be2daa9) -> None:
        '''
        :param api: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6044517e388ef5f586931fcc45296518ce903a316ec6848b60b25b3ce6845f8f)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
        jsii.create(self.__class__, self, [api])


__all__ = [
    "ApiGateway",
    "ApiGatewayDomain",
    "ApiGatewayv2DomainProperties",
    "BucketWebsiteTarget",
    "ClassicLoadBalancerTarget",
    "CloudFrontTarget",
    "ElasticBeanstalkEnvironmentEndpointTarget",
    "GlobalAcceleratorDomainTarget",
    "GlobalAcceleratorTarget",
    "InterfaceVpcEndpointTarget",
    "LoadBalancerTarget",
    "Route53RecordTarget",
    "UserPoolDomainTarget",
]

publication.publish()

def _typecheckingstub__d49a8136c756c219e2234eff358adabd8c6eaf00f32c3c9bc927841203cf6800(
    domain_name: _IDomainName_2f71106c,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec5f0b4bb0e51294b23f7531a18b10e0d2b15196b95cec34c20020a09c64b25(
    _record: _IRecordSet_133a645a,
    _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b057fb1f1fb3519cab268ae870b598023b551eaf0140b6e94b729292c272c59(
    regional_domain_name: builtins.str,
    regional_hosted_zone_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a484e5fd65f7e7ec8c5c2c3d1d5129d912f9d6096b0c6e450bd42cc6d5e499f0(
    _record: _IRecordSet_133a645a,
    _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f2bd2957df209ee46123eb47d59cb035d243fc5fdebbe52f7d34d6a50319ed(
    bucket: _IBucket_73486e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9eee7913b1a69e16f5b9371e592bf811c86499540699c17825620be3175f380(
    _record: _IRecordSet_133a645a,
    _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82858a0ded466991ff0a8c731f2777292e6b64988ef3fa287f1bf2ad446b45f0(
    load_balancer: _LoadBalancer_a7de240f,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0066533578d6c9458d6a61050194acd9259ec182113264b7ad46461e524168f4(
    _record: _IRecordSet_133a645a,
    _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec082d244330e3f8c0e5c1c1d4b8f80248f5f86bc80d1daaa567205a6efc1b1e(
    distribution: _IDistribution_685deca5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07e07a82be8846e9ad6df684b99605a8f6cbf3ffdfddfdf7c0fa50b0952b35af(
    scope: _IConstruct_5a0f9c5e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0711b704f94eb0a950aadf03ce10909d3b0641258775b9cf1466e460e1c32f87(
    _record: _IRecordSet_133a645a,
    _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a988c89f12ade1b00aaccbe41983cd80b2f49b4a9bb267e56102c6808ecf3682(
    environment_endpoint: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea3a4e065a4c470b592fe64c22eaf1a5155152d956bbacf82776625c09ccb51d(
    _record: _IRecordSet_133a645a,
    _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c773859bc9453d4b7973806936a58e7e1be860d98395b64a50b68fb8898ba96(
    accelerator_domain_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e911cb0718b9e46f01cc873ba75ab24a15a1ea3d91b7531573bb117bf7317e(
    _record: _IRecordSet_133a645a,
    _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74bb7f7db426fcd739812d69f4cf7698d57d3a5896229aef480e58686edf4b8b(
    accelerator: _IAccelerator_8b90cb82,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1433099182e18c518cf95bd4df9a2c3ca2f0178c1003342d9f2d82d10a13e8a3(
    vpc_endpoint: _IInterfaceVpcEndpoint_6081623d,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a184ac7fe32db7550de9c978701385bf46cd0b98e076c84f9967c87fa186484f(
    _record: _IRecordSet_133a645a,
    _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0845c0220d6c4f72bb7a6cc8fa3fbc18a27cf5b2898702f9a2c5df81a85aebc8(
    load_balancer: _ILoadBalancerV2_f1c75d72,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7600ff54d517da9b2c0c94e3519602bb6a87554f0b6a528c2a5f1d4eda39b941(
    _record: _IRecordSet_133a645a,
    _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0132b09b963b953ebbcc3d485ab80b82e1cfb0ea66540a36a70106082d90f1d(
    record: _IRecordSet_133a645a,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03a54fa3b25e122b58a0ff3618e7e8030b4db7ae0608ce084c2282059e57a49(
    _record: _IRecordSet_133a645a,
    zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730d5a98f195e20f202e35618e3d52f2183495b4e33eb8fd0b5c53655433170d(
    domain: _UserPoolDomain_18478017,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b240eb68449c4b26242e4c4dcc7658e18335f918577e97402931b85dd9054046(
    _record: _IRecordSet_133a645a,
    _zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6044517e388ef5f586931fcc45296518ce903a316ec6848b60b25b3ce6845f8f(
    api: _RestApiBase_8be2daa9,
) -> None:
    """Type checking stubs"""
    pass
